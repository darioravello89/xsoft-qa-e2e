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
        deadline = time.monotonic() + timeout
        while True:
            if self._select_window(entry["window"]):
                found = self.bridge.get_elements(entry["query"], java_elements=True, strict=True)
                showing = [element for element in found if element.showing]
                if len(showing) > 1:
                    raise QAError(f"Locator ambiguo: {alias}. Calibrar un único control visible.")
                if len(showing) == 1:
                    return showing[0]
            if time.monotonic() >= deadline:
                raise QAError(f"No apareció el control semántico: {alias}.")
            time.sleep(0.25)

    def click(self, alias):
        element = self.find(alias)
        if not element.enabled:
            raise QAError(f"Control deshabilitado: {alias}.")
        # Acción accesible del control; nunca método de dominio ni coordenadas fijas.
        self.bridge.click_element(element, action=True)

    def type(self, alias, text, *, enter=False, secret=False):
        element = self.find(alias)
        if not element.enabled:
            raise QAError(f"Campo deshabilitado: {alias}.")
        try:
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

    def expect(self, alias, expected, timeout=20):
        deadline = time.monotonic() + timeout
        while True:
            if self.text(alias) == expected:
                return
            if time.monotonic() >= deadline:
                raise AssertionError(f"Texto inesperado en {alias}; revisar fixture y evidencia UI.")
            time.sleep(0.25)

    def wait_gone(self, alias, timeout=20):
        entry = self.locators["elements"][alias]
        deadline = time.monotonic() + timeout
        while True:
            if not self._select_window(entry["window"]):
                return
            elements = self.bridge.get_elements(entry["query"], java_elements=True, strict=True)
            if not any(element.showing for element in elements):
                return
            if time.monotonic() >= deadline:
                raise QAError(f"El control {alias} permanece abierto.")
            time.sleep(0.25)
