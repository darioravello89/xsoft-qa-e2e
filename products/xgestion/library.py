"""Keywords públicos sin argumentos secretos. Importación segura para robot --dryrun."""

import os
import re
import time
from decimal import Decimal, InvalidOperation
from pathlib import Path

from robot.api.deco import keyword

from framework.errors import QAError
from products.xgestion.contracts import load_assets
from products.xgestion.driver import JarProcess, SemanticDriver, create_bridge, private_input
from products.xgestion.oracles import XGestionOracle, assert_cancelled


def parse_ars(text):
    cleaned = re.sub(r"\s|ARS|\$", "", text, flags=re.IGNORECASE)
    if not re.fullmatch(r"-?\d{1,3}(?:\.\d{3})*(?:,\d{1,2})?|-?\d+(?:,\d{1,2})?", cleaned):
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

    @keyword("Iniciar XGestion QA")
    def start(self):
        from framework.config import load_profile

        if not __debug__:
            raise QAError("No ejecutar la suite con PYTHONOPTIMIZE: las aserciones deben estar activas.")
        root = Path(os.environ.get("XSOFT_QA_ROOT", Path(__file__).resolve().parents[2]))
        self.profile = load_profile(root)
        self.fixtures, locators = load_assets(self.profile)
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
        with private_input():
            self.driver.type("login.user", "__QA_USUARIO_INEXISTENTE__", secret=True)
            self.driver.type("login.password", "__QA_CLAVE_INVALIDA__", secret=True)
            self.driver.click("login.submit")
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
        context = self.fixtures["context"]
        self.driver.expect("main.company", context["empresa_label"], timeout=120)
        self.driver.expect("main.branch", context["sucursal_label"])
        self.driver.expect("main.user", context["usuario_label"])

    @keyword("Buscar Producto Conocido")
    def known_product(self):
        self._open_products()
        self.driver.type("products.search", self.fixtures["product"]["code"])
        self.driver.click("products.search_button")
        self.driver.expect("products.known_result", self.fixtures["product"]["name"])

    @keyword("Buscar Producto Inexistente")
    def unknown_product(self):
        self._open_products()
        self.driver.type("products.search", self.fixtures["nonexistent_product_code"])
        self.driver.click("products.search_button")
        self.driver.expect("products.empty_result", self.fixtures["ui"]["products_empty_text"])

    def _open_products(self):
        self.verify_context()
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
        self.verify_context()
        self.before = self._oracle().snapshot()
        self.driver.click("menu.sales")
        self.driver.click("menu.new_sale")
        self.driver.click("sale.document")
        self.driver.click("sale.non_fiscal_option")
        self.driver.type("sale.quantity", "2")
        self.driver.type("sale.code", self.fixtures["product"]["code"], enter=True)
        deadline = time.monotonic() + 20
        while parse_ars(self.driver.text("sale.total")) != Decimal("2000.00"):
            if time.monotonic() >= deadline:
                raise AssertionError("La venta UI debe sumar 2 × 1000 = 2000 ARS antes de cobrar.")
            time.sleep(0.25)

    @keyword("Cobrar Venta En Efectivo")
    def collect_sale(self):
        if self.before is None:
            raise QAError("Preparar Venta Basica debe ejecutarse antes del cobro.")
        self.driver.click("sale.close")
        self.driver.click("payment.cash_option")
        self.driver.click("payment.cash_accept")
        self.driver.type("payment.amount", "2000")
        self.driver.click("payment.confirm")
        self.driver.wait_gone("payment.confirm", timeout=40)

    @keyword("Verificar Venta Persistida")
    def verify_sale(self):
        if self.before is None:
            raise QAError("Falta snapshot anterior a la venta.")
        deadline = time.monotonic() + 20
        while True:
            try:
                return self._oracle().verify_sale(self.before)
            except AssertionError:
                if time.monotonic() >= deadline:
                    raise
                time.sleep(0.25)

    @keyword("Cancelar Venta Basica")
    def cancel_sale(self):
        self.driver.click("sale.cancel")
        self.driver.click("sale.cancel_confirm")
        self.driver.wait_gone("sale.code")
        self.driver.find("sale.closed_indicator")

    @keyword("Verificar Cancelacion Sin Persistencia")
    def verify_cancel(self):
        if self.before is None:
            raise QAError("Falta snapshot anterior a la cancelación.")
        assert_cancelled(self.before, self._oracle().snapshot())

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
