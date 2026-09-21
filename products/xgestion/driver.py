"""JAR propio y selectores JAB calibrados. No importa RPA al cargar/dry-run."""

import contextlib
import io
import logging
import os
import re
import subprocess
import time
from pathlib import Path

from framework.errors import QAError
from framework.events import assertion_failed, diagnostic


@contextlib.contextmanager
def private_input():
    """Evita que bibliotecas de teclado escriban credenciales en logs de Robot/Python."""
    previous = logging.root.manager.disable
    logging.disable(logging.CRITICAL)
    builtin = None
    level = None
    try:
        try:
            from robot.libraries.BuiltIn import BuiltIn
            builtin = BuiltIn()
            level = builtin.set_log_level("NONE")
        except Exception:
            builtin = None
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            yield
    finally:
        if builtin is not None and level is not None:
            builtin.set_log_level(level)
        logging.disable(previous)


def create_bridge(profile):
    try:
        from RPA.JavaAccessBridge import JavaAccessBridge
        dll = Path(profile.env("QA_JAVA_HOME")) / "bin" / "WindowsAccessBridge-64.dll"
        if not dll.is_file():
            raise QAError("Falta WindowsAccessBridge-64.dll en el JDK seleccionado.")
        return JavaAccessBridge(access_bridge_path=str(dll))
    except Exception:
        raise QAError("Java Access Bridge no está disponible. Ejecutar doctor y revisar JDK/DLL de 64 bits.") from None


class JarProcess:
    def __init__(self, profile):
        self.profile = profile
        self.process = None

    def start(self):
        if self.process is not None:
            raise QAError("Ya existe un JAR administrado por este escenario.")
        java = Path(self.profile.env("QA_JAVA_HOME")) / "bin" / "java.exe"
        cwd = self.profile.runtime / "app"
        jar = self.profile.asset("app").resolve()
        if not java.is_file() or not jar.is_file() or not (cwd / "config.properties").is_file():
            raise QAError("Falta Java, JAR o config.properties preparado por el runner QA.")
        environment = {key: value for key, value in os.environ.items()
                       if not key.upper().startswith(("QA_", "XSOFT_QA_"))
                       and key.upper() not in {"JAVA_TOOL_OPTIONS", "_JAVA_OPTIONS", "JDK_JAVA_OPTIONS", "CLASSPATH"}}
        environment["JAVA_HOME"] = str(java.parent.parent)
        environment["PATH"] = str(java.parent) + os.pathsep + os.environ.get("PATH", "")
        self.process = subprocess.Popen(
            [str(java), "-Xms256m", "-Xmx1536m", "-jar", str(jar)],
            cwd=cwd, env=environment, shell=False, stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        return self.process.pid

    def stop(self):
        process, self.process = self.process, None
        if process is None:
            return
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)


class SemanticDriver:
    def __init__(self, bridge, pid, locators):
        self.bridge = bridge
        self.pid = pid
        self.locators = locators

    def _select_window(self, key):
        title = self.locators["windows"][key]
        windows = list(self.bridge.list_java_windows())
        own = [window for window in windows if window.pid == self.pid and window.title == title]
        if any(window.pid != self.pid and window.title == title for window in windows):
            raise QAError("Hay otra instancia Java con el mismo título. No se interactuará con ella.")
        if len(own) > 1:
            raise QAError("Ventana JAB ambigua dentro del proceso QA.")
        if not own:
            return False
        self.bridge.select_window_by_title("^" + re.escape(title) + "$", timeout=1)
        self.bridge.application_refresh()
        return True

    def find(self, alias, timeout=20):
        entry = self.locators["elements"][alias]
        started = time.monotonic()
        deadline = started + timeout
        diagnostic("Buscar control de la aplicación", control=alias, timeout_seconds=timeout)
        while True:
            if self._select_window(entry["window"]):
                found = self.bridge.get_elements(entry["query"], java_elements=True, strict=True)
                showing = [element for element in found if element.showing]
                if len(showing) > 1:
                    raise QAError(f"Locator ambiguo: {alias}. Calibrar un único control visible.")
                if len(showing) == 1:
                    diagnostic("Control disponible", control=alias,
                               duration_seconds=round(time.monotonic() - started, 3))
                    return showing[0]
            if time.monotonic() >= deadline:
                raise QAError(f"No apareció el control semántico: {alias}.")
            time.sleep(0.25)

    def click(self, alias):
        element = self.find(alias)
        if not element.enabled:
            raise QAError(f"Control deshabilitado: {alias}.")
        # Acción accesible del control; nunca método de dominio ni coordenadas fijas.
        diagnostic("Activar control", control=alias)
        self.bridge.click_element(element, action=True)

    def type(self, alias, text, *, enter=False, secret=False):
        element = self.find(alias)
        if not element.enabled:
            raise QAError(f"Campo deshabilitado: {alias}.")
        try:
            # Ni siquiera TRACE registra lo escrito, aunque no sea un campo secreto.
            diagnostic("Completar campo", control=alias)
            with private_input() if secret else contextlib.nullcontext():
                self.bridge.type_text(element, str(text), clear=True, enter=enter)
        except Exception:
            raise QAError(f"No se pudo completar el campo {alias}.") from None

    def text(self, alias):
        element = self.find(alias)
        value = self.bridge.get_element_text(element)
        if not value and "text" not in str(element.role).lower():
            value = element.name
        return str(value or "").strip()

    def table_rows(self, alias) -> list[list[str]]:
        """Leer todas las celdas sólo si coinciden con las dimensiones nativas JAB."""
        try:
            # Refresh y read_table pueden registrar el árbol y sus datos aun en TRACE.
            with private_input():
                _, cells, row_count, column_count = self._table_cells(alias)
                rows = [[str(cell.text or cell.name or "").strip() for cell in row] for row in cells]
        except QAError:
            raise
        except Exception:
            raise QAError(f"No se pudo leer la tabla {alias}; revisar la calibración JAB.") from None
        diagnostic("Tabla completa leída", control=alias, row_count=row_count, column_count=column_count)
        return rows

    def _table_cells(self, alias):
        """Compartir la lectura estructural; los llamadores deben usar private_input."""
        element = self.find(alias)
        element.node.refresh()
        if element.role != "table":
            raise QAError(f"El control {alias} no es una tabla accesible.")
        native = element.node.table.table
        row_count, column_count = native.rowCount, native.columnCount
        if (type(row_count) is not int or type(column_count) is not int
                or row_count < 0 or column_count < 0 or (row_count and not column_count)):
            raise QAError(f"La tabla {alias} no informa dimensiones válidas.")
        cells = []
        if row_count:
            cells = self.bridge.read_table(element, visible_only=False)
            current = element.node.table.table
            if ((current.rowCount, current.columnCount) != (row_count, column_count)
                    or not isinstance(cells, list) or len(cells) != row_count
                    or any(not isinstance(row, list) or len(row) != column_count for row in cells)):
                raise QAError(f"Lectura incompleta de la tabla {alias}; revisar la calibración.")
        return element, cells, row_count, column_count

    def edit_sale_row(self, alias, code_column, expected_code):
        """Abrir la edición con doble clic en la geometría JAB actual de una fila única."""
        if (type(code_column) is not int or code_column < 0
                or not isinstance(expected_code, str) or not expected_code.strip()):
            raise QAError("La edición requiere una columna calibrada y la identidad del producto.")
        try:
            with private_input():
                table, cells, row_count, column_count = self._table_cells(alias)
                if not table.enabled or code_column >= column_count:
                    raise QAError(f"La tabla {alias} no permite editar la columna calibrada.")
                matches = [row[code_column] for row in cells
                           if str(row[code_column].text or row[code_column].name or "").strip() == expected_code]
                if len(matches) != 1:
                    raise QAError(f"La tabla {alias} no identifica una única fila del producto esperado.")
                selected = matches[0]
                selected.node.refresh()
                # JavaElement copia texto/estados/geometría al construirse. refresh_element
                # de RPA 33 los copia ANTES del refresh; reconstruir después evita datos viejos.
                current = type(selected)(selected.node, scaling_factor=self.bridge.display_scale_factor)
                if str(current.text or current.name or "").strip() != expected_code:
                    raise QAError(f"La identidad de la celda de {alias} cambió antes de editar.")
                geometry = (current.x, current.y, current.width, current.height)
                if (not current.enabled or not current.visible or not current.showing
                        or any(type(value) is not int for value in geometry)
                        or current.x < 0 or current.y < 0 or current.width <= 0 or current.height <= 0):
                    raise QAError(f"La celda de {alias} no tiene geometría visible y habilitada para editar.")
                self.bridge.click_element(current, action=False, click_type="double click")
        except QAError:
            raise
        except Exception:
            raise QAError(f"No se pudo abrir la edición de la fila de {alias}; revisar la calibración JAB.") from None
        diagnostic("Edición de fila solicitada", control=alias, row_count=row_count, column_count=column_count)

    @staticmethod
    def _states(element):
        return {state.strip().lower() for state in element.node.context_info.states.split(",")}

    def _focus_element(self, alias):
        element = self.find(alias)
        if not element.enabled:
            raise QAError(f"Control deshabilitado: {alias}.")
        diagnostic("Esperar foco del control", control=alias)
        deadline = time.monotonic() + 20
        element.node.request_focus()
        while True:
            element.node.refresh()
            if "focused" in self._states(element):
                return element
            if time.monotonic() >= deadline:
                raise QAError(f"No se confirmó el foco del control {alias}.")
            time.sleep(0.25)

    def select_sale_row(self, alias, code_column, expected_code):
        """Seleccionar una fila única sólo con JAB y teclado, sin coordenadas."""
        if (type(code_column) is not int or code_column < 0
                or not isinstance(expected_code, str) or not expected_code.strip()):
            raise QAError("La selección requiere una columna calibrada y la identidad del producto.")
        try:
            with private_input():
                table, cells, row_count, column_count = self._table_cells(alias)
                if not table.enabled or code_column >= column_count:
                    raise QAError(f"La tabla {alias} no permite seleccionar la columna calibrada.")
                matches = [index for index, row in enumerate(cells)
                           if str(row[code_column].text or row[code_column].name or "").strip() == expected_code]
                if len(matches) != 1:
                    raise QAError(f"La tabla {alias} no identifica una única fila del producto esperado.")
                target_row = matches[0]
                self._focus_element(alias)
                self.bridge.press_keys("ctrl", "home")
                for _ in range(target_row):
                    self.bridge.press_keys("down")
                _, refreshed, refreshed_rows, refreshed_columns = self._table_cells(alias)
                if (refreshed_rows != row_count or refreshed_columns != column_count):
                    raise QAError(f"La tabla {alias} cambió mientras se seleccionaba el producto.")
                row = refreshed[target_row]
                if str(row[code_column].text or row[code_column].name or "").strip() != expected_code:
                    raise QAError(f"La identidad de la fila de {alias} cambió durante la selección.")
                selected = False
                for cell in row:
                    cell.node.refresh()
                    selected = selected or "selected" in self._states(cell)
                if not selected:
                    raise QAError(f"JAB no confirmó la selección de la fila en {alias}.")
        except QAError:
            raise
        except Exception:
            raise QAError(f"No se pudo seleccionar la fila de {alias}; revisar la calibración JAB.") from None
        diagnostic("Fila de venta seleccionada", control=alias, row_index=target_row)
        return target_row

    def expect_sale_row_selected(self, alias, code_column, expected_code):
        """Comprobar identidad y estado selected sin cambiar la selección."""
        try:
            with private_input():
                _, cells, _, column_count = self._table_cells(alias)
                if type(code_column) is not int or not 0 <= code_column < column_count:
                    raise QAError(f"Columna calibrada inválida para {alias}.")
                matches = [row for row in cells
                           if str(row[code_column].text or row[code_column].name or "").strip() == expected_code]
                if len(matches) != 1:
                    raise QAError(f"La tabla {alias} no identifica una única fila del producto esperado.")
                selected = False
                for cell in matches[0]:
                    cell.node.refresh()
                    selected = selected or "selected" in self._states(cell)
                if not selected:
                    raise QAError(f"La fila esperada de {alias} no conserva la selección.")
        except QAError:
            raise
        except Exception:
            raise QAError(f"No se pudo comprobar la selección de {alias}.") from None

    def expect_focus(self, alias):
        """Comprobar foco JAB sin forzarlo para no ocultar una regresión de la pantalla."""
        element = self.find(alias)
        deadline = time.monotonic() + 20
        while True:
            element.node.refresh()
            if "focused" in self._states(element):
                diagnostic("Foco conservado", control=alias)
                return
            if time.monotonic() >= deadline:
                raise QAError(f"El control {alias} no conserva el foco esperado.")
            time.sleep(0.25)

    def shortcut(self, alias, shortcut):
        """Enviar únicamente el acorde aprobado para editar una venta."""
        if not isinstance(shortcut, str) or shortcut.lower() != "ctrl+e":
            raise QAError("Sólo se permite el atajo Ctrl+E por esta acción semántica.")
        try:
            with private_input():
                self._focus_element(alias)
                self.bridge.press_keys("ctrl", "e")
        except QAError:
            raise
        except Exception:
            raise QAError(f"No se pudo enviar Ctrl+E al control {alias}.") from None
        diagnostic("Atajo permitido enviado", control=alias, shortcut="Ctrl+E")

    def keys(self, alias, *keys):
        """Enviar Tab o Esc al control propio sólo después de confirmar su foco."""
        # RPA interpreta varios argumentos como un acorde, no como una secuencia.
        if len(keys) != 1 or not isinstance(keys[0], str) or keys[0].lower() not in {"tab", "esc"}:
            raise QAError("Sólo se permite una tecla Tab o Esc por acción semántica.")
        try:
            with private_input():
                self._focus_element(alias)
                self.bridge.press_keys(keys[0].lower())
        except QAError:
            raise
        except Exception:
            raise QAError(f"No se pudo enviar la tecla al control {alias}.") from None
        diagnostic("Tecla permitida enviada", control=alias)

    def expect(self, alias, expected, timeout=20):
        deadline = time.monotonic() + timeout
        while True:
            observed = self.text(alias)
            if observed == expected:
                diagnostic("Comprobación de pantalla correcta", control=alias)
                return
            if time.monotonic() >= deadline:
                message = f"Texto inesperado en {alias}; revisar fixture y evidencia UI."
                # No depender de conocer de antemano el valor sensible para ocultarlo.
                sensitive = alias.startswith("login.") or "password" in alias.lower()
                assertion_failed(message,
                                 expected="[CAMPO DE ACCESO OMITIDO]" if sensitive else expected,
                                 observed="[CAMPO DE ACCESO OMITIDO]" if sensitive else observed)
                raise AssertionError(message)
            time.sleep(0.25)

    def wait_gone(self, alias, timeout=20):
        entry = self.locators["elements"][alias]
        deadline = time.monotonic() + timeout
        diagnostic("Esperar cierre del control", control=alias, timeout_seconds=timeout)
        while True:
            if not self._select_window(entry["window"]):
                return
            elements = self.bridge.get_elements(entry["query"], java_elements=True, strict=True)
            if not any(element.showing for element in elements):
                return
            if time.monotonic() >= deadline:
                raise QAError(f"El control {alias} permanece abierto.")
            time.sleep(0.25)
