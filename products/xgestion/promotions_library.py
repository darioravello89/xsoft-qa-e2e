"""Recorridos de promociones por UI; la DB sólo aporta comprobaciones de lectura."""

import copy
import os
from datetime import date
from decimal import Decimal

from robot.api.deco import keyword

from framework.errors import QAError
from framework.events import business_step
from products.xgestion.library import XGestionLibrary, parse_ars, parse_quantity
from products.xgestion.oracles import assert_unchanged
from products.xgestion.promotions import CASES, SEED, validate_promotions


class XGestionPromotionsLibrary(XGestionLibrary):
    @keyword("Iniciar Promociones QA")
    def start_promotions(self, seed_id):
        if seed_id not in CASES:
            raise QAError("Ejemplo de promoción no documentado.")
        if (os.environ.get("XSOFT_QA_SEED") != SEED
                or os.environ.get("XSOFT_QA_SEED_DATE") != date.today().isoformat()):
            raise QAError("Promociones requiere el seed verificado en esta ejecución y fecha. Usar qa.cmd run.")
        self.case = CASES[seed_id]
        self.start("ventas-etapa1")

    def _configure_extension(self, extension, locators):
        super()._configure_extension(extension, locators)
        validate_promotions(self.fixtures, locators)
        self.fixtures = copy.deepcopy(self.fixtures)
        self.fixtures["product"] = self.case.product()

    def _assert_sale_content(self, quantity, rows=1):
        self._require_journeys()
        expected = self.case.expected(quantity)
        columns = self.driver.locators["elements"]["sale.lines"]["columns"]
        business_step(f"Comprobar {quantity} unidades: bruto {quantity * 1000} ARS, "
                      f"oferta {expected['offer_discount']} ARS y neto {expected['total']} ARS")

        def check():
            state = self._sale_state()
            lines, total = state
            self._equal(len(lines), 1, "Un único renglón del producto")
            line = lines[0]
            self._equal(line[columns["code"]] == self.case.code, True, "Código del producto esperado")
            self._equal(line[columns["name"]] == self.case.code, True, "Nombre del producto esperado")
            self._equal(parse_quantity(line[columns["quantity"]]), Decimal(quantity), "Cantidad de unidades")
            for field, amount, label in (
                ("unit_price", Decimal(1000), "Precio base ARS"),
                ("gross_total", Decimal(quantity) * 1000, "Subtotal bruto ARS"),
                ("offer_discount", expected["offer_discount"], "Descuento de oferta ARS"),
                ("total", expected["total"], "Neto del renglón ARS"),
            ):
                self._equal(parse_ars(line[columns[field]], private=True), amount, label)
            self._equal(total, expected["total"], "Total de venta ARS")
            return state

        return self._wait_check(check)

    @keyword("Preparar Venta Con Promocion")
    def prepare_promotion(self):
        self.verify_context()
        business_step("Comprobar fecha del catálogo y existencias del producto")
        today = self._oracle().query("SELECT CURDATE() AS today", ())
        if len(today) != 1 or str(today[0]["today"]) != os.environ.get("XSOFT_QA_SEED_DATE"):
            raise QAError("Cambió la fecha del catálogo: repetir desde el seed para comprobar vigencias.")
        if self.case.seed_id in ("EXPIRADA", "FUTURA", "INACTIVA"):
            business_step("Comprobar primero una oferta vigente: una unidad con 10% debe costar 900 ARS")
            negative = self.case
            try:
                self.case = CASES["PCT-Q3"]
                self.fixtures["product"] = self.case.product()
                self._prepare_promotion_sale()
                self.cancel_sale()
                self.verify_cancel()
            finally:
                self.case = negative
                self.fixtures["product"] = self.case.product()
        self._prepare_promotion_sale()

    def _prepare_promotion_sale(self):
        self.before = self._oracle().snapshot()
        if self.before.stock < max(self.case.initial_quantity, self.case.quantity):
            raise QAError("Stock insuficiente para el ejemplo de promoción; revisar el baseline y seed.")
        self._open_sale()
        self._add_product(self.case.initial_quantity)

    @keyword("Modificar Cantidad Con Promocion")
    def edit_promotion_quantity(self):
        self._assert_sale_content(self.case.initial_quantity)
        business_step(f"Editar la misma línea con Ctrl+E y cambiar a {self.case.quantity} unidades")
        column = self.driver.locators["elements"]["sale.lines"]["columns"]["code"]
        self.driver.select_sale_row("sale.lines", column, self.case.code)
        self.driver.shortcut("sale.lines", "ctrl+e")
        self.driver.expect("editor.product", self.case.code)
        self.driver.expect_focus("editor.quantity")
        self.driver.type("editor.quantity", str(self.case.quantity))
        self.driver.click("editor.save")
        self.driver.wait_gone("editor.save")
        self._assert_sale_content(self.case.quantity)
        self.driver.expect_sale_row_selected("sale.lines", column, self.case.code)
        self.driver.expect_focus("sale.lines")

    @keyword("Cancelar Cobro De Promocion")
    def cancel_promotion_payment(self):
        state = self._assert_sale_content(self.case.quantity)
        self._open_payment()
        self._enter_payment(str(self.case.total), total=self.case.total)
        business_step("Cancelar el cobro conservando cantidades, oferta y total sin registrar movimientos")
        self.driver.click("payment.cancel")
        self.driver.wait_gone("payment.confirm")
        self._assert_same_sale(state)
        assert_unchanged(self.before, self._oracle().snapshot())

    @keyword("Cobrar Promocion En Efectivo")
    def collect_promotion(self):
        self._assert_sale_content(self.case.quantity)
        self._open_payment()
        self._enter_payment(str(self.case.total), total=self.case.total)
        self._confirm_payment()

    def _verify_sale_snapshot(self):
        return self._oracle().verify_sale(self.before, received=self.received,
                                         promotion=self.case.expected(self.case.quantity))
