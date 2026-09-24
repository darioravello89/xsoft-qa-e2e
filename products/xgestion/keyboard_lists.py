"""Recorridos JAB de listados; los esperados provienen del paquete QA privado."""

import time
from pathlib import Path

from robot.api.deco import keyword

from framework.errors import QAError
from framework.events import assertion_failed, business_step
from products.xgestion.contracts import has_verified_feature, validate_elements
from products.xgestion.driver import private_input
from products.xgestion.library import XGestionLibrary

FILTERED = {1, 2, 3, 4, 6, 7, 10, 13}
CASE_IDS = tuple(f"XG-KEY-{number:03}" for number in range(1, 14))
FEATURE = "atajos-listados-v1"


def validate_case(case_id, data, locators):
    """Rechazar una calibración incompleta antes de tocar la aplicación."""
    if case_id not in CASE_IDS or not isinstance(data, dict):
        raise QAError(f"Falta el perfil privado del caso {case_id}.")

    def is_placeholder(value):
        if isinstance(value, str):
            return not value.strip() or "CALIBRAR" in value.upper()
        if isinstance(value, dict):
            return any(is_placeholder(item) for item in value.values())
        if isinstance(value, list):
            return any(is_placeholder(item) for item in value)
        return False

    if is_placeholder(data):
        raise QAError(f"El perfil {case_id} contiene valores de ejemplo sin calibrar.")
    required = ("open", "search", "table", "legend", "detail_identity", "detail_close",
                "identity_column", "none", "one", "many", "rows", "details",
                "sort_control", "sort_keys", "sorted_rows", "legend_evidence", "restricted")
    if any(key not in data for key in required):
        raise QAError(f"Perfil incompleto para {case_id}; faltan variantes N01-N12.")
    if (not isinstance(data["open"], list) or not data["open"]
            or type(data["identity_column"]) is not int or data["identity_column"] < 0
            or any(not isinstance(data[key], str) or not data[key].strip() or "CALIBRAR" in data[key].upper()
                   for key in ("none", "one", "many", "sort_control"))
            or not isinstance(data["rows"], list) or len(data["rows"]) != 3
            or len(set(data["rows"])) != 3 or not isinstance(data["sorted_rows"], list)
            or data["sorted_rows"] == data["rows"] or set(data["sorted_rows"]) != set(data["rows"])
            or not isinstance(data["sort_keys"], list) or not data["sort_keys"]):
        raise QAError(f"Datos de búsqueda/orden ambiguos para {case_id}.")
    if not isinstance(data["legend_evidence"], dict):
        raise QAError(f"Falta evidencia visual de la leyenda para {case_id}.")
    details = data["details"]
    if (not isinstance(details, dict) or set(details) != set(data["rows"])
            or any(not isinstance(value, dict) or len(value) < 2
                   or any(not isinstance(expected, str) or not expected.strip()
                          for expected in value.values()) for value in details.values())):
        raise QAError(f"Falta identidad de destino independiente para {case_id}.")
    if not isinstance(data["restricted"], dict) or not data["restricted"].get("user_label"):
        raise QAError(f"Falta la variante de restricciones de {case_id}.")
    aliases = [*data["open"], *(data[key] for key in
                ("search", "table", "legend", "detail_identity", "detail_close", "sort_control"))]
    aliases += [alias for fields in details.values() for alias in fields]
    if int(case_id[-3:]) in FILTERED:
        modal = data.get("filters")
        if not isinstance(modal, dict) or not modal.get("fields"):
            raise QAError(f"Falta contrato del modal de filtros de {case_id}.")
        if not isinstance(modal.get("focus_order"), list) or len(modal["focus_order"]) < 3:
            raise QAError(f"Falta el orden de Tab de todos los filtros de {case_id}.")
        if any(not isinstance(modal.get(key), list) for key in ("selected_before", "selected_b", "selected_a")):
            raise QAError(f"F09 requiere selección esperada antes/después de filtrar: {case_id}.")
        if len(modal["selected_before"]) != 1 or modal["selected_before"][0] not in modal.get("rows_a", []):
            raise QAError(f"F09 necesita una fila inequívoca seleccionada antes de filtrar: {case_id}.")
        aliases += [modal[key] for key in ("first", "apply", "cancel", "close_x", "reload_revision")]
        aliases += modal["focus_order"]
        aliases += [field["alias"] for field in modal["fields"]]
        special = modal.get("special", {})
        if special.get("kind") == "dates":
            if not isinstance(special.get("rows_empty_from"), list):
                raise QAError(f"F08 requiere filas esperadas con fecha vacía: {case_id}.")
            aliases += [special[key] for key in ("from", "until", "error", "error_dismiss")]
        elif special.get("kind") == "cascade":
            aliases += [special[key] for key in ("parent", "child")]
        elif special.get("kind") != "none":
            raise QAError(f"F08 sin configuración de fechas, cascada o no aplica: {case_id}.")
    if case_id == "XG-KEY-010":
        types = data.get("purchase_types", [])
        if {item.get("type") for item in types} != {"Remito", "Factura", "Transferencia", "Carniceria"}:
            raise QAError("Compras requiere los cuatro tipos de comprobante.")
        aliases += [alias for item in types for alias in [item["close"], *item["details"]]]
    restriction = data["restricted"]
    if restriction.get("outcome") == "notice":
        aliases += [restriction["notice"], restriction["dismiss"]]
    elif restriction.get("outcome") == "read_only":
        aliases += [restriction["save"]]
    else:
        raise QAError(f"La restricción de {case_id} debe declarar aviso o editor de sólo lectura.")
    validate_elements(locators, aliases)
    return data


def assert_single_reload(before, after):
    if not isinstance(before, str) or not isinstance(after, str) or not before.isdecimal() or not after.isdecimal():
        raise QAError("Falta señal accesible de recarga lógica completa.")
    if int(after) != int(before) + 1:
        assertion_failed("Cantidad de recargas lógicas incorrecta", expected="1", observed=str(int(after) - int(before)))
        raise AssertionError("Aplicar filtros provocó cero o varias recargas lógicas.")


class KeyboardListsLibrary(XGestionLibrary):
    ROBOT_LIBRARY_SCOPE = "SUITE"
    ROBOT_AUTO_KEYWORDS = False

    def _configure_extension(self, extension, locators):
        if extension != FEATURE or not has_verified_feature(locators, FEATURE):
            raise QAError("Falta calibración privada atajos-listados-v1 para este SHA256.")
        settings = self.fixtures.get("keyboard_lists")
        if not isinstance(settings, dict) or settings.get("schema_version") != 1:
            raise QAError("Falta keyboard_lists v1 en fixtures privados.")
        cases = settings.get("cases")
        if not isinstance(cases, dict):
            raise QAError("Falta keyboard_lists.cases en fixtures privados.")
        self.keyboard_cases = cases

    @keyword("Ejecutar Atajos Del Listado")
    def run_case(self, case_id):
        data = validate_case(case_id, self.keyboard_cases.get(case_id), self.driver.locators)
        self.verify_context()
        for alias in data["open"]:
            self.driver.click(alias)
        business_step(f"{case_id}: comprobar ayuda y foco del buscador")
        self._legend(data, filtered=int(case_id[-3:]) in FILTERED)
        self.driver._focus_element(data["table"])
        self.driver.press_focused(data["table"], "ctrl+b")
        self.driver.expect_focus(data["search"])
        self._empty(data)
        self._single(data)
        self._multiple(data)
        self._search_enter(data, purchases=case_id == "XG-KEY-010")
        if case_id == "XG-KEY-010":
            self._purchase_types(data)
        self._sort(data)
        if int(case_id[-3:]) in FILTERED:
            self._filters(data)
        else:
            self._no_filter_modal(data)
        self._restricted(data)
        self._legend(data, filtered=int(case_id[-3:]) in FILTERED)

    def _rows(self, data, expected):
        deadline = time.monotonic() + 20
        while True:
            rows = self.driver.table_rows(data["table"])
            column = data["identity_column"]
            if any(column >= len(row) for row in rows):
                raise QAError("JAB no entregó la columna de identidad completa.")
            observed = [row[column] for row in rows]
            if observed == expected:
                return
            if time.monotonic() >= deadline:
                assertion_failed("Filas visibles distintas", expected=expected, observed=observed)
                raise AssertionError("El listado no muestra las identidades y orden esperados.")
            time.sleep(0.25)

    def _search(self, data, term, expected):
        self.driver.type(data["search"], term)
        self._rows(data, expected)
        self.driver.expect_focus(data["search"])

    def _selected(self, data, expected):
        observed = self.driver.selected_row_identity(data["table"], data["identity_column"])
        if observed != expected:
            assertion_failed("Fila elegida por teclado incorrecta", expected=expected, observed=observed)
            raise AssertionError("La navegación seleccionó otro registro.")
        self.driver.expect_focus(data["table"])

    def _open_selected(self, data, identity):
        self._selected(data, identity)
        self.driver.press_focused(data["table"], "enter")
        for alias, expected in data["details"][identity].items():
            self.driver.expect(alias, expected)
        self.driver.click(data["detail_close"])
        self.driver.find(data["search"])

    def _empty(self, data):
        business_step("Buscar sin resultados; flechas no deben abrir ni elegir registros")
        self._search(data, data["none"], [])
        for key in ("down", "up"):
            self.driver.press_focused(data["search"], key)
            self.driver.expect_focus(data["search"])
            self._rows(data, [])
            if self.driver.selected_row_identities(data["table"], data["identity_column"]):
                raise AssertionError("La tabla vacía conserva una selección.")

    def _single(self, data):
        business_step("Una fila: flechas, foco, selección circular y apertura correcta")
        identity = data["rows"][1]
        for key in ("down", "up"):
            self._search(data, data["one"], [identity])
            self.driver.press_focused(data["search"], key)
            self._selected(data, identity)
            for movement in ("up", "down", "down"):
                self.driver.press_focused(data["table"], movement)
                self._selected(data, identity)
            self._open_selected(data, identity)

    def _multiple(self, data):
        business_step("Varias filas: ↑/↓ desde búsqueda, paso circular e identidad al abrir")
        identities = data["rows"]
        for first, expected in (("down", identities[0]), ("up", identities[-1])):
            self._search(data, data["many"], identities)
            self.driver.press_focused(data["search"], first)
            self._selected(data, expected)
        self._search(data, data["many"], identities)
        self.driver.press_focused(data["search"], "down")
        for index in range(1, len(identities) + 1):
            self.driver.press_focused(data["table"], "down")
            self._selected(data, identities[index % len(identities)])
        self.driver.press_focused(data["table"], "up")
        self._selected(data, identities[-1])
        self._search(data, data["many"], identities)
        self.driver.press_focused(data["search"], "down")
        self.driver.press_focused(data["table"], "up")
        self._selected(data, identities[-1])
        for index, identity in enumerate(identities):
            self._search(data, data["many"], identities)
            self.driver.press_focused(data["search"], "down")
            for _ in range(index):
                self.driver.press_focused(data["table"], "down")
            self._open_selected(data, identity)
        # N05: desde la fila intermedia, Ctrl+B no debe olvidar la selección.
        self._search(data, data["many"], identities)
        self.driver.press_focused(data["search"], "down")
        self.driver.press_focused(data["table"], "down")
        self._selected(data, identities[1])
        self.driver.press_focused(data["table"], "ctrl+b")
        self.driver.expect_focus(data["search"])
        self.driver.press_focused(data["search"], "down")
        self._selected(data, identities[2])
        # N08: conservar B al buscarlo, limpiar cuando desaparece y recuperar navegación.
        self._search(data, data["one"], [identities[1]])
        if self.driver.selected_row_identities(data["table"], data["identity_column"]) != [identities[1]]:
            raise AssertionError("La búsqueda que conserva B perdió su selección.")
        self._search(data, data["none"], [])
        if self.driver.selected_row_identities(data["table"], data["identity_column"]):
            raise AssertionError("La búsqueda excluyente conservó una selección inválida.")
        self._search(data, data["many"], identities)
        self.driver.press_focused(data["search"], "up")
        self._selected(data, identities[-1])

    def _search_enter(self, data, purchases):
        business_step("Enter en buscador conserva la acción de búsqueda original")
        for term, expected in ((data["none"], []), (data["many"], data["rows"]),
                               (data["one"], [data["rows"][1]])):
            self._search(data, term, expected)
            self.driver.press_focused(data["search"], "enter")
            if purchases and len(expected) == 1:
                for alias, value in data["details"][expected[0]].items():
                    self.driver.expect(alias, value)
                self.driver.click(data["detail_close"])
            else:
                self._rows(data, expected)
                if self.driver._present(data["detail_identity"]):
                    raise AssertionError("Enter en el buscador abrió un registro inesperado.")

    def _sort(self, data):
        business_step("Cambiar orden desde el control de la aplicación y abrir por identidad")
        self._search(data, data["many"], data["rows"])
        self.driver._focus_element(data["sort_control"])
        for key in data["sort_keys"]:
            self.driver.press_focused(data["sort_control"], key)
        self._rows(data, data["sorted_rows"])
        self.driver._focus_element(data["search"])
        self.driver.press_focused(data["search"], "down")
        self._open_selected(data, data["sorted_rows"][0])

    def _purchase_types(self, data):
        business_step("Abrir por Enter Remito, Factura, Transferencia y Carnicería")
        for item in data["purchase_types"]:
            self._search(data, item["search"], [item["identity"]])
            self.driver.press_focused(data["search"], "down")
            self._selected(data, item["identity"])
            self.driver.press_focused(data["table"], "enter")
            for alias, expected in item["details"].items():
                self.driver.expect(alias, expected)
            self.driver.click(item["close"])

    def _legend(self, data, filtered):
        text = self.driver.text(data["legend"])
        required = ("Ctrl+B", "Enter", "Ctrl+F") if filtered else ("Ctrl+B", "Enter")
        if any(part not in text for part in required) or (not filtered and "Ctrl+F" in text):
            raise AssertionError("La leyenda visible no coincide con los atajos disponibles.")
        self.driver.find(data["legend"])
        # JAB acredita texto/visibilidad; color y ubicación requieren captura revisada.
        evidence = data["legend_evidence"]
        capture = Path(evidence.get("capture", "")).resolve() if isinstance(evidence, dict) else None
        if (not isinstance(evidence, dict)
                or evidence.get("app_sha256") != self.driver.locators["calibration"]["app_sha256"]
                or capture is None or not capture.is_relative_to(self.profile.runtime.resolve())
                or not capture.is_file()):
            raise QAError("Falta evidencia visual de leyenda gris junto al buscador para este JAR.")

    def _no_filter_modal(self, data):
        business_step("Ctrl+F sin filtros no debe abrir un modal vacío")
        for alias in (data["search"], data["table"]):
            self.driver._focus_element(alias)
            self.driver.press_focused(alias, "ctrl+f")
            deadline = time.monotonic() + 2
            while time.monotonic() < deadline:
                if any(window.pid == self.driver.pid and "Filtros -" in window.title
                       for window in self.bridge.list_java_windows()):
                    raise AssertionError("Ctrl+F abrió un modal en un listado sin filtros.")
                time.sleep(0.1)
            self.driver.press_focused(alias, "ctrl+b")
            self.driver.expect_focus(data["search"])

    def _filters(self, data):
        modal = data["filters"]
        business_step("Ctrl+F, cancelar/escapar/cerrar X, aplicar y reabrir filtros")
        for origin in (data["search"], data["table"]):
            before_selection = self.driver.selected_row_identities(data["table"], data["identity_column"])
            self.driver._focus_element(origin)
            self.driver.press_focused(origin, "ctrl+f")
            self.driver.find(modal["first"])
            self._assert_modal(data)
            self.driver.press_focused(modal["first"], "down")
            self._tab_order(modal)
            self._activate_filter(modal, "cancel")
            if self.driver.selected_row_identities(data["table"], data["identity_column"]) != before_selection:
                raise AssertionError("La tabla cambió de selección mientras el modal estaba abierto.")
        # Cada mecanismo se prueba desde el mismo estado A, con todos los campos cambiados.
        for close in ("cancel", "esc", "close_x"):
            self._open_filter(data)
            self._filter_values(modal, "a")
            self._set_filter_values(modal, "b")
            if close == "esc":
                self.driver._focus_element(modal["first"])
                self.driver.press_focused(modal["first"], "esc")
            elif close == "cancel":
                self._activate_filter(modal, "cancel")
            else:
                self.driver.click(modal[close])
            self._rows(data, modal["rows_a"])
            self._open_filter(data)
            self._filter_values(modal, "a")
            self._activate_filter(modal, "cancel")
        self._open_filter(data)
        self._activate_filter(modal, "cancel")
        self.driver._focus_element(data["search"])
        self.driver.press_focused(data["search"], "down")
        self._selected(data, modal["selected_before"][0])
        before = self.driver.text(modal["reload_revision"])
        self._open_filter(data)
        self._set_filter_values(modal, "b")
        self._activate_filter(modal, "apply")
        self._rows(data, modal["rows_b"])
        if self.driver.selected_row_identities(data["table"], data["identity_column"]) != modal["selected_b"]:
            raise AssertionError("El filtro B no conservó/limpió la selección por identidad.")
        after = self.driver.text(modal["reload_revision"])
        assert_single_reload(before, after)
        self._open_filter(data)
        self._filter_values(modal, "b")
        self._activate_filter(modal, "cancel")
        # F07: el Enter predeterminado debe aplicar una vez desde un campo.
        before = self.driver.text(modal["reload_revision"])
        self._open_filter(data)
        self._set_filter_values(modal, "a")
        self.driver._focus_element(modal["first"])
        self.driver.press_focused(modal["first"], "enter")
        self._rows(data, modal["rows_a"])
        if self.driver.selected_row_identities(data["table"], data["identity_column"]) != modal["selected_a"]:
            raise AssertionError("El retorno al filtro A dejó una selección incorrecta.")
        after = self.driver.text(modal["reload_revision"])
        assert_single_reload(before, after)
        self._open_filter(data)
        self._filter_values(modal, "a")
        self._activate_filter(modal, "cancel")
        self._filter_special(data)
        self.driver._focus_element(data["search"])
        self.driver.press_focused(data["search"], "down")
        self._selected(data, modal["rows_a"][0])

    def _filter_special(self, data):
        modal = data["filters"]
        special = modal["special"]
        if special["kind"] == "none":
            return  # F08 no aplica: el modal no contiene fechas ni cascada.
        self._open_filter(data)
        if special["kind"] == "dates":
            self.driver.type(special["from"], special["invalid_from"])
            self.driver.type(special["until"], special["invalid_until"])
            self._activate_filter(modal, "apply")
            self.driver.expect(special["error"], special["error_text"])
            self.driver.click(special["error_dismiss"])
            self.driver.find(modal["first"])
            self._activate_filter(modal, "cancel")
            before = self.driver.text(modal["reload_revision"])
            self._open_filter(data)
            self.driver.type(special["from"], "")
            self._activate_filter(modal, "apply")
            self._rows(data, special["rows_empty_from"])
            assert_single_reload(before, self.driver.text(modal["reload_revision"]))
            self._open_filter(data)
            self._set_filter_values(modal, "a")
            self._activate_filter(modal, "apply")
        else:
            parent = next(field for field in modal["fields"] if field["alias"] == special["parent"])
            self._set_filter_values({"fields": [parent]}, "b")
            self.driver.expect(special["child"], special["child_after_parent"])
            self._activate_filter(modal, "cancel")
        self._rows(data, modal["rows_a"])
        self._open_filter(data)
        self._filter_values(modal, "a")
        self._activate_filter(modal, "cancel")

    def _tab_order(self, modal):
        order = modal["focus_order"]
        self.driver._focus_element(order[0])
        for current, next_alias in zip(order, order[1:] + order[:1]):
            self.driver.press_focused(current, "tab")
            self.driver.expect_focus(next_alias)
        backward = [order[0], *reversed(order[1:])]
        for current, previous in zip(backward, [order[-1], *reversed(order[1:-1]), order[0]]):
            self.driver.press_focused(current, "shift+tab")
            self.driver.expect_focus(previous)

    def _open_filter(self, data):
        self.driver._focus_element(data["search"])
        self.driver.press_focused(data["search"], "ctrl+f")
        self.driver.find(data["filters"]["first"])
        self.driver.expect_focus(data["filters"]["first"])
        self._assert_modal(data)

    def _assert_modal(self, data):
        first = data["filters"]["first"]
        entry = self.driver.locators["elements"][first]
        title = self.driver.locators["windows"][entry["window"]]
        own = [window for window in self.bridge.list_java_windows()
               if window.pid == self.driver.pid and window.title == title]
        if len(own) != 1:
            raise QAError("Ctrl+F no dejó un único modal de filtros del proceso QA.")

    def _activate_filter(self, modal, target):
        """Llegar a Aplicar/Cancelar con Tab y activarlo con Enter."""
        order = modal["focus_order"]
        alias = modal[target]
        if alias not in order:
            raise QAError(f"{target} no figura en el recorrido de Tab del modal.")
        self.driver._focus_element(order[0])
        for current, next_alias in zip(order, order[1:]):
            if current == alias:
                break
            self.driver.press_focused(current, "tab")
            self.driver.expect_focus(next_alias)
        self.driver.expect_focus(alias)
        self.driver.press_focused(alias, "enter")

    def _filter_values(self, modal, variant):
        for field in modal["fields"]:
            self._expect_filter_value(field, variant)

    def _expect_filter_value(self, field, variant):
        observed = (self.driver.choice_text(field["alias"]) if field["kind"] == "choice"
                    else self.driver.text(field["alias"]))
        if observed != field[variant]:
            assertion_failed("Valor de filtro incorrecto", expected=field[variant], observed=observed)
            raise AssertionError(f"El control {field['alias']} no muestra el valor esperado.")

    def _set_filter_values(self, modal, variant):
        for field in modal["fields"]:
            if field["kind"] == "text":
                self.driver.type(field["alias"], field[variant])
            elif field["kind"] == "choice":
                self.driver._focus_element(field["alias"])
                for key in field[f"keys_{variant}"]:
                    self.driver.press_focused(field["alias"], key)
            else:
                raise QAError("Tipo de control de filtro sin calibrar.")
            self._expect_filter_value(field, variant)

    def _restricted(self, data):
        restricted = data["restricted"]
        user = self.profile.env("QA_KEYBOARD_RESTRICTED_USER")
        password = self.profile.env("QA_KEYBOARD_RESTRICTED_PASSWORD")
        if not user or not password:
            raise QAError("N12 necesita credenciales locales del operador restringido.")
        business_step("Reabrir el listado con un operador restringido")
        self.stop()
        self.start(FEATURE)
        try:
            with private_input():
                self.driver.type("login.user", user, secret=True)
                self.driver.type("login.password", password, secret=True)
                self.driver.click("login.submit")
        finally:
            password = None
        self.driver.expect("main.company", self.fixtures["context"]["empresa_label"])
        self.driver.expect("main.branch", self.fixtures["context"]["sucursal_label"])
        self.driver.expect("main.user", restricted["user_label"])
        self.authenticated = True
        for alias in data["open"]:
            self.driver.click(alias)
        self._search(data, restricted["search"], [restricted["identity"]])
        self.driver.press_focused(data["search"], "down")
        self._selected(data, restricted["identity"])
        self.driver.press_focused(data["table"], "enter")
        if restricted["outcome"] == "notice":
            self.driver.expect(restricted["notice"], restricted["expected_notice"])
            self.driver.click(restricted["dismiss"])
        else:
            self.driver.expect(data["detail_identity"], restricted["detail_identity"])
            self.driver.expect_state(restricted["save"], "enabled", False)
            self.driver.click(data["detail_close"])
        self.driver._focus_element(data["table"])
        self.driver.press_focused(data["table"], "ctrl+b")
        self.driver.expect_focus(data["search"])
