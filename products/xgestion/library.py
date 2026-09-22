"""Keywords públicos sin argumentos secretos. Importación segura para robot --dryrun."""

import os
import re
import time
from decimal import Decimal, InvalidOperation
from pathlib import Path

from robot.api.deco import keyword

from framework.errors import QAError
from framework.events import assertion_failed, business_step, diagnostic
from products.xgestion.contracts import KEYBOARD_FEATURE, has_verified_feature, load_assets, validate_journeys
from products.xgestion.driver import JarProcess, SemanticDriver, create_bridge, private_input
from products.xgestion.oracles import XGestionOracle, assert_cancelled, assert_unchanged

UI_TIMEOUT = 20


class BusinessMismatch(AssertionError):
    def __init__(self, label, expected, observed):
        self.expected = str(expected)
        self.observed = str(observed)
        super().__init__(f"{label}: esperado {expected}; observado {observed}.")


def parse_quantity(text):
    # FormVenta.generarTabla convierte Util.redondear(cantidad, 3) con String.valueOf.
    if not re.fullmatch(r"\d+(?:\.\d{1,3})?", text.strip()):
        raise AssertionError("Cantidad UI inválida: se esperan hasta tres decimales con punto.")
    return Decimal(text.strip())


def parse_payment(text):
    # formTicketCierre.formatearImporte usa BigDecimal.toPlainString (sin agrupación).
    if not re.fullmatch(r"\d+(?:\.\d{1,2})?", text.strip()):
        raise AssertionError("Importe de cobro inválido: se espera decimal sin agrupación.")
    return Decimal(text.strip())


def parse_ars(text, *, private=False):
    cleaned = re.sub(r"\s|ARS|\$", "", text, flags=re.IGNORECASE)
    if not re.fullmatch(r"-?\d{1,3}(?:\.\d{3})*(?:,\d{1,2})?|-?\d+(?:,\d{1,2})?", cleaned):
        if not private:
            assertion_failed("Formato del importe mostrado incorrecto.",
                             expected="Importe ARS con hasta dos decimales, por ejemplo 2.000,00",
                             observed="[VALOR NO NUMÉRICO OMITIDO]")
        raise AssertionError("Importe UI no tiene el formato ARS calibrado (2.000,00).")
    try:
        return Decimal(cleaned.replace(".", "").replace(",", "."))
    except InvalidOperation:
        raise AssertionError("Importe UI inválido.") from None


class XGestionLibrary:
    ROBOT_LIBRARY_SCOPE = "SUITE"
    ROBOT_AUTO_KEYWORDS = False

    def __init__(self):
        self.process = None
        self.driver = None
        self.bridge = None
        self.connection = None
        self.authenticated = False
        self.before = None
        self.after_paid = None
        self.persisted_sale_id = None
        self.received = Decimal("2000")
        self.journeys = False
        self.keyboard_sales = False

    @keyword("Iniciar XGestion QA")
    def start(self, extension=None):
        from framework.config import load_profile

        if not __debug__:
            raise QAError("No ejecutar la suite con PYTHONOPTIMIZE: las aserciones deben estar activas.")
        root = Path(os.environ.get("XSOFT_QA_ROOT", Path(__file__).resolve().parents[2]))
        self.profile = load_profile(root)
        self.fixtures, locators = load_assets(self.profile)
        self.before = self.after_paid = self.persisted_sale_id = None
        self.received = Decimal("2000")
        self._configure_extension(extension, locators)
        self.authenticated = False
        self.process = JarProcess(self.profile)
        try:
            self.bridge = create_bridge(self.profile)
            pid = self.process.start()
            self.driver = SemanticDriver(self.bridge, pid, locators)
            self.driver.find("login.user", timeout=120)
            self.driver.find("login.password")
            self.driver.find("login.submit")
        except Exception:
            self.stop()
            raise

    def _configure_extension(self, extension, locators):
        self.journeys = extension == "ventas-etapa1"
        self.keyboard_sales = self.journeys and has_verified_feature(locators, KEYBOARD_FEATURE)
        if extension is not None:
            if not self.journeys:
                raise QAError("Extensión de escenarios desconocida.")
            validate_journeys(self.fixtures, locators)

    @keyword("Cerrar XGestion QA")
    def stop(self):
        self.authenticated = False
        try:
            if self.connection is not None:
                self.connection.close()
                self.connection = None
        finally:
            if self.process is not None:
                self.process.stop()
                self.process = None
            if self.bridge is not None:
                try:
                    self.bridge.shutdown_jab()
                except Exception:
                    pass  # Cerrar el puente ya inaccesible no cambia el resultado del escenario.
                self.bridge = None

    @keyword("Verificar Pantalla De Acceso")
    def verify_login(self):
        self.driver.find("login.user")
        self.driver.find("login.password")
        self.driver.find("login.submit")

    @keyword("Rechazar Credenciales Invalidas")
    def invalid_login(self):
        business_step("Intentar acceder con credenciales inválidas")
        with private_input():
            self.driver.type("login.user", "__QA_USUARIO_INEXISTENTE__", secret=True)
            self.driver.type("login.password", "__QA_CLAVE_INVALIDA__", secret=True)
            self.driver.click("login.submit")
        business_step("Comprobar el rechazo del acceso y la limpieza de los campos")
        self.driver.expect("login.error", "Acceso Invalido")
        self.driver.click("login.error_ok")
        self.driver.expect("login.user", "")
        self.driver.expect("login.password", "")

    @keyword("Ingresar Como QA")
    def login(self):
        user = self.profile.env("QA_LOGIN_USER")
        password = self.profile.env("QA_LOGIN_PASSWORD")
        if not user or not password:
            raise QAError("Completar credenciales QA locales antes de iniciar sesión.")
        try:
            with private_input():
                self.driver.type("login.user", user, secret=True)
                self.driver.type("login.password", password, secret=True)
                self.driver.click("login.submit")
        finally:
            password = None
        self.verify_context()
        self.authenticated = True

    @keyword("Verificar Contexto QA")
    def verify_context(self):
        business_step("Comprobar empresa, sucursal y usuario de QA")
        context = self.fixtures["context"]
        self.driver.expect("main.company", context["empresa_label"], timeout=120)
        self.driver.expect("main.branch", context["sucursal_label"])
        self.driver.expect("main.user", context["usuario_label"])

    @keyword("Buscar Producto Conocido")
    def known_product(self):
        self._open_products()
        business_step("Buscar el producto conocido")
        self.driver.type("products.search", self.fixtures["product"]["code"])
        self.driver.click("products.search_button")
        business_step("Comprobar que aparece el producto esperado")
        self.driver.expect("products.known_result", self.fixtures["product"]["name"])

    @keyword("Buscar Producto Inexistente")
    def unknown_product(self):
        self._open_products()
        business_step("Buscar un código inexistente")
        self.driver.type("products.search", self.fixtures["nonexistent_product_code"])
        self.driver.click("products.search_button")
        business_step("Comprobar que no aparecen productos")
        self.driver.expect("products.empty_result", self.fixtures["ui"]["products_empty_text"])

    def _open_products(self):
        self.verify_context()
        business_step("Abrir la consulta de productos")
        self.driver.click("menu.products")
        self.driver.click("menu.products_list")

    def _oracle(self):
        if self.connection is None:
            try:
                import pymysql
                self.connection = pymysql.connect(
                    host="127.0.0.1", port=13317, database="xsoft_qa", user="root",
                    password=self.profile.env("QA_DB_PASSWORD"), cursorclass=pymysql.cursors.DictCursor,
                    autocommit=True, connect_timeout=5, read_timeout=10, write_timeout=10,
                )
            except Exception:
                raise QAError("No se pudo abrir el oráculo de lectura en la instancia QA local.") from None
        return XGestionOracle(self.connection, self.fixtures)

    @keyword("Preparar Venta Basica")
    def prepare_sale(self):
        self._prepare_sale(2)

    @keyword("Preparar Venta De Una Unidad")
    def prepare_single_sale(self):
        self._require_journeys()
        self._prepare_sale(1)

    def _require_journeys(self):
        if not self.journeys:
            raise QAError("Este escenario necesita iniciar con la extensión calibrada ventas-etapa1.")

    def _prepare_sale(self, quantity):
        self.verify_context()
        business_step("Comprobar el estado inicial de stock y caja")
        self.before = self._oracle().snapshot()
        self._open_sale()
        self._add_product(quantity)

    def _select_document(self):
        business_step("Seleccionar el comprobante no fiscal")
        self.driver.click("sale.document")
        self.driver.click("sale.non_fiscal_option")

    def _open_sale(self):
        business_step("Abrir una nueva venta")
        self.driver.click("menu.sales")
        self.driver.click("menu.new_sale")
        if self.journeys:
            self._assert_new_sale()
        self._select_document()

    def _add_product(self, quantity):
        business_step(f"Agregar {quantity} unidades del producto de prueba")
        self.driver.type("sale.quantity", str(quantity))
        self.driver.type("sale.code", self.fixtures["product"]["code"], enter=True)
        if self.journeys:
            return self._assert_sale_content(quantity)
        business_step("Comprobar el total antes de cobrar: $2.000,00 ARS")
        deadline = time.monotonic() + UI_TIMEOUT
        while True:
            observed = parse_ars(self.driver.text("sale.total"))
            if observed == Decimal("2000.00"):
                diagnostic("Total visible comprobado", expected="2000.00 ARS", observed=f"{observed:.2f} ARS")
                break
            if time.monotonic() >= deadline:
                message = "La venta UI debe sumar 2 × 1000 = 2000 ARS antes de cobrar."
                assertion_failed(message, expected="2000.00 ARS", observed=f"{observed:.2f} ARS")
                raise AssertionError(message)
            time.sleep(0.25)

    def _wait_check(self, check):
        deadline = time.monotonic() + UI_TIMEOUT
        while True:
            try:
                return check()
            except AssertionError as error:
                if time.monotonic() >= deadline:
                    assertion_failed(str(error), expected=getattr(error, "expected", "Formato numérico calibrado"),
                                     observed=getattr(error, "observed", "[VALOR NO NUMÉRICO OMITIDO]"))
                    raise
                time.sleep(0.25)

    @staticmethod
    def _equal(observed, expected, label):
        if observed != expected:
            raise BusinessMismatch(label, expected, observed)

    def _sale_state(self):
        rows = self.driver.table_rows("sale.lines")
        count = self.driver.locators["elements"]["sale.lines"]["column_count"]
        if any(len(row) != count for row in rows):
            raise QAError("La grilla de venta no coincide con las columnas JAB calibradas.")
        return tuple(tuple(row) for row in rows), parse_ars(self.driver.text("sale.total"), private=True)

    def _assert_sale_content(self, quantity, rows=1):
        self._require_journeys()
        business_step(f"Comprobar producto, {quantity} unidades, precio, subtotales y total de la venta")
        columns = self.driver.locators["elements"]["sale.lines"]["columns"]

        def check():
            state = self._sale_state()
            lines, total = state
            self._equal(len(lines), rows, "Cantidad de renglones")
            units = Decimal(0)
            for line in lines:
                # No volcar el contenido de la grilla ni nombres privados en eventos.
                self._equal(line[columns["code"]] == self.fixtures["product"]["code"], True,
                            "Código del producto esperado")
                self._equal(line[columns["name"]] == self.fixtures["product"]["name"], True,
                            "Nombre del producto esperado")
                count = parse_quantity(line[columns["quantity"]])
                self._equal(count > 0, True, "Cantidad positiva")
                self._equal(parse_ars(line[columns["unit_price"]], private=True), Decimal("1000"), "Precio unitario ARS")
                self._equal(parse_ars(line[columns["total"]], private=True), count * 1000, "Subtotal ARS")
                units += count
            self._equal(units, Decimal(quantity), "Unidades en la venta")
            self._equal(total, Decimal(quantity) * 1000, "Total ARS")
            return state

        return self._wait_check(check)

    def _assert_same_sale(self, previous):
        def check():
            self._equal(self._sale_state() == previous, True, "Contenido e importes de la venta conservados")
        self._wait_check(check)

    def _assert_new_sale(self):
        self._require_journeys()
        business_step("Comprobar venta vacía, cantidad inicial y condiciones predeterminadas")

        def check():
            lines, total = self._sale_state()
            self._equal(len(lines), 0, "Venta nueva sin renglones anteriores")
            self._equal(total, Decimal(0), "Total inicial ARS")
            self._equal(parse_quantity(self.driver.text("sale.quantity")), Decimal(1), "Cantidad inicial")
        self._wait_check(check)
        self.driver.expect("sale.code", "")
        for field in ("customer", "price_list", "document"):
            expected = self.fixtures["sales_journeys"]["defaults"][field]
            self.driver.expect(f"sale.{field}", expected)

    @keyword("Rechazar Codigo Inexistente Y Continuar")
    def unknown_code_in_sale(self):
        self._require_journeys()
        before_ui = self._assert_sale_content(1)
        business_step("Buscar un código inexistente sin perder el producto ya cargado")
        self.driver.type("sale.code", self.fixtures["nonexistent_product_code"], enter=True)
        profile = self.fixtures["sales_journeys"]
        self.driver.expect("sale.unknown_notice", profile["unknown_notice_text"])
        if profile["unknown_notice"] == "dialog":
            self.driver.click("sale.unknown_dismiss")
        self._assert_same_sale(before_ui)
        assert_unchanged(self.before, self._oracle().snapshot())
        business_step("Agregar otra unidad válida después del rechazo")
        self.driver.type("sale.quantity", "1")
        self.driver.type("sale.code", self.fixtures["product"]["code"], enter=True)
        self._assert_sale_content(2, rows=profile["repeated_product_rows"])

    @keyword("Modificar Cantidad Del Producto Cargado")
    def edit_sale_quantity(self):
        self._require_journeys()
        estado_inicial = self._assert_sale_content(1)
        business_step("Abrir el producto cargado y cambiar su cantidad a dos unidades")
        column = self.driver.locators["elements"]["sale.lines"]["columns"]["code"]
        if self.keyboard_sales:
            self.driver.select_sale_row("sale.lines", column, self.fixtures["product"]["code"])
            self.driver.click("sale.edit")
            self.driver.expect("editor.product", self.fixtures["product"]["name"])
            self.driver.expect_focus("editor.quantity")
            business_step("Cancelar la edición y comprobar que venta, selección y foco se conservan")
            self.driver.click("editor.cancel")
            self.driver.wait_gone("editor.cancel")
            self._assert_same_sale(estado_inicial)
            self.driver.expect_sale_row_selected("sale.lines", column, self.fixtures["product"]["code"])
            self.driver.expect_focus("sale.lines")
            business_step("Reabrir el renglón con Ctrl+E y guardar la cantidad dos")
            self.driver.shortcut("sale.lines", "ctrl+e")
        else:
            # Compatibilidad temporal con paquetes anteriores a ventas-teclado-v1.
            self.driver.edit_sale_row("sale.lines", column, self.fixtures["product"]["code"])
        self.driver.expect("editor.product", self.fixtures["product"]["name"])
        if self.keyboard_sales:
            self.driver.expect_focus("editor.quantity")
        self.driver.type("editor.quantity", "2")
        self.driver.click("editor.save")
        self.driver.wait_gone("editor.save")
        self._assert_sale_content(2)

    @keyword("Rechazar Abandono Conservando La Venta")
    def reject_abandon(self):
        self._require_journeys()
        state = self._assert_sale_content(1)
        business_step("Solicitar salir y elegir continuar con la venta")
        self.driver.keys("sale.code", "esc")
        self.driver.click("sale.cancel_reject")
        self.driver.wait_gone("sale.cancel_reject")
        self._assert_same_sale(state)
        assert_unchanged(self.before, self._oracle().snapshot())

    def _open_payment(self):
        if self.before is None:
            raise QAError("Preparar Venta Basica debe ejecutarse antes del cobro.")
        business_step("Abrir el cobro y seleccionar efectivo")
        self.driver.click("sale.close")
        self.driver.click("payment.cash_option")
        self.driver.click("payment.cash_accept")

    def _enter_payment(self, received, *, total=Decimal("2000")):
        self.received = Decimal(received)
        business_step(f"Ingresar el importe recibido: {received} ARS")
        self.driver.type("payment.amount", str(received))
        if self.journeys:
            self.driver.keys("payment.amount", "tab")

            def check():
                self._equal(parse_payment(self.driver.text("payment.total")), total, "Total de cobro ARS")
                self._equal(parse_payment(self.driver.text("payment.amount")), self.received, "Recibido ARS")
                self._equal(parse_payment(self.driver.text("payment.change")), self.received - total, "Vuelto ARS")
            self._wait_check(check)

    def _confirm_payment(self):
        business_step("Confirmar el cobro y esperar su cierre")
        self.driver.click("payment.confirm")
        self.driver.wait_gone("payment.confirm", timeout=40)

    @keyword("Cobrar Venta En Efectivo")
    def collect_sale(self):
        self._open_payment()
        self._enter_payment("2000")
        self._confirm_payment()

    @keyword("Cobrar En Efectivo Con Vuelto")
    def collect_with_change(self):
        self._require_journeys()
        self._open_payment()
        self._enter_payment("3000")
        self._confirm_payment()

    @keyword("Cancelar Cobro Conservando La Venta")
    def cancel_cash_payment(self):
        self._require_journeys()
        state = self._assert_sale_content(2)
        self._open_payment()
        self._enter_payment("2000")
        business_step("Cancelar el cobro y comprobar que la venta sigue pendiente")
        self.driver.click("payment.cancel")
        self.driver.wait_gone("payment.confirm")
        self._assert_same_sale(state)
        assert_unchanged(self.before, self._oracle().snapshot())

    @keyword("Verificar Venta Persistida")
    def verify_sale(self):
        if self.before is None:
            raise QAError("Falta snapshot anterior a la venta.")
        business_step("Comprobar una sola venta, su pago y los cambios de stock y caja")
        deadline = time.monotonic() + UI_TIMEOUT
        while True:
            try:
                self.persisted_sale_id = self._verify_sale_snapshot()
                if self.journeys:
                    self.after_paid = self._oracle().snapshot()
                return self.persisted_sale_id
            except AssertionError:
                if time.monotonic() >= deadline:
                    raise
                time.sleep(0.25)

    def _verify_sale_snapshot(self):
        return self._oracle().verify_sale(self.before, received=self.received)

    @keyword("Cancelar Venta Basica")
    def cancel_sale(self):
        business_step("Solicitar y confirmar el abandono de la venta")
        if self.journeys:
            self.driver.keys("sale.code", "esc")
        else:
            self.driver.click("sale.cancel")
        self.driver.click("sale.cancel_confirm")
        business_step("Comprobar que se cerró la venta abandonada")
        self.driver.wait_gone("sale.code")
        self.driver.find("sale.closed_indicator")

    @keyword("Verificar Cancelacion Sin Persistencia")
    def verify_cancel(self):
        if self.before is None:
            raise QAError("Falta snapshot anterior a la cancelación.")
        business_step("Comprobar que el abandono no creó ventas ni cambió stock o caja")
        assert_cancelled(self.before, self._oracle().snapshot())

    @keyword("Continuar Con Otra Venta Despues Del Cobro")
    def continue_after_payment(self):
        self._require_journeys()
        if self.persisted_sale_id is None or self.after_paid is None:
            raise QAError("Verificar la primera venta antes de continuar con otra.")
        # FormVenta reinicia la MISMA instancia. Abrir el menú ocultaría un fallo de ese reinicio.
        self._assert_new_sale()
        self._select_document()

    @keyword("Continuar Con Otra Venta Despues Del Abandono")
    def continue_after_abandon(self):
        self._require_journeys()
        self.verify_cancel()
        self._open_sale()

    @keyword("Agregar Una Unidad A La Venta")
    def add_single_product(self):
        self._require_journeys()
        self._add_product(1)

    @keyword("Verificar Que Solo Persiste La Primera Venta")
    def verify_only_first_sale(self):
        if self.before is None or self.after_paid is None or self.persisted_sale_id is None:
            raise QAError("Falta evidencia de la primera venta cobrada.")
        business_step("Comprobar que abandonar la segunda venta conserva sólo la primera y su único cobro")
        oracle = self._oracle()
        assert_unchanged(self.after_paid, oracle.snapshot())
        oracle.verify_sale(self.before, received=Decimal("2000"), expected_sale_id=self.persisted_sale_id)

    @keyword("Capturar Evidencia QA")
    def screenshot(self):
        if not self.authenticated:
            return
        # Nunca login/password ni desktop completo: sólo la ventana propia ya autenticada.
        try:
            import ctypes

            from PIL import ImageGrab
            self.verify_context()
            windows = self.driver.bridge.list_java_windows()
            main = self.driver.locators["windows"][self.driver.locators["elements"]["main.company"]["window"]]
            matches = [w for w in windows if w.pid == self.driver.pid and w.title == main]
            if len(matches) != 1:
                raise QAError("No se encontró ventana propia para evidencia.")
            from ctypes import wintypes
            rect = wintypes.RECT()
            get_rect = ctypes.WinDLL("user32", use_last_error=True).GetWindowRect
            get_rect.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.RECT)]
            get_rect.restype = wintypes.BOOL
            if not get_rect(matches[0].hwnd, ctypes.byref(rect)):
                raise QAError("No se pudo obtener rectángulo de evidencia.")
            directory = Path(os.environ["XSOFT_QA_RUN_DIR"])
            directory.mkdir(parents=True, exist_ok=True)
            from robot.libraries.BuiltIn import BuiltIn
            name = str(BuiltIn().get_variable_value("${TEST NAME}", "evidencia")).split()[0]
            safe = re.sub(r"[^A-Za-z0-9_-]", "_", name)
            ImageGrab.grab(bbox=(rect.left, rect.top, rect.right, rect.bottom)).save(directory / f"{safe}.png")
        except Exception:
            raise QAError("No se pudo capturar evidencia de la ventana QA autenticada.") from None
