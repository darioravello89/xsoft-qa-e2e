"""Acciones de usuario; sólo el runner restaura/aplica seed, el oráculo sólo lee."""

import os
import re
from datetime import date
from decimal import Decimal
from types import SimpleNamespace

import javaproperties
from robot.api.deco import keyword

from framework.errors import QAError
from framework.events import business_step
from products.xgestion.driver import private_input
from products.xgestion.library import BusinessMismatch, XGestionLibrary, parse_payment, parse_quantity
from products.xgestion.offer_journeys.model import Line
from products.xgestion.offer_journeys.usd import assert_basket, assert_money, check_payment_currencies
from products.xgestion.oracles import enabled

from .contracts import validate
from .oracles import (
    PRODUCT_SET,
    CircuitOracle,
    assert_cash_sale,
    assert_purchase,
    assert_turn,
    assert_unchanged,
    same_extra,
)


def purchase_money(text):
    # La grilla usa MySQL FORMAT(...,2): 1,200.00; Venta usa 1.200,00.
    match = re.fullmatch(r"\s*(USD|\$)\s*(-?(?:\d{1,3}(?:,\d{3})*|\d+)\.\d{2})\s*", text)
    if not match:
        raise BusinessMismatch("Importe del remito", "Moneda y decimal calibrados", "Formato inválido omitido")
    return ("ARS" if match[1] == "$" else "USD"), Decimal(match[2].replace(",", ""))


class XGestionCircuitsLibrary(XGestionLibrary):
    @keyword("Ejecutar Circuito Comercial")
    def run_circuit(self, case):
        if case == "XG-FIN-012":
            raise QAError("Cuenta corriente bloqueada: falta atajo o botón accesible para abrir el cliente "
                          "(XG-ACC-010). Doble clic no autorizado.")
        if case not in {"XG-FIN-011", "XG-FIN-013", "XG-FIN-014"}:
            raise QAError("Circuito sin implementación.")
        if (os.environ.get("XSOFT_QA_SEED") != "catalogo-comercial-v1"
                or os.environ.get("XSOFT_QA_SEED_DATE") != date.today().isoformat()):
            raise QAError("Los circuitos requieren seed verificado hoy por qa.cmd run --seed.")
        self.case = case
        self.start("ventas-etapa1")
        self.login()
        self._oracle().validate_currency_schema()
        if case == "XG-FIN-011":
            self._sell("USD-FIJO", "2", "100", "350000")
        elif case == "XG-FIN-013":
            self._purchase()
        else:
            self._close_turn()

    @keyword("Finalizar Circuito Comercial")
    def finish_circuit(self):
        try:
            self.screenshot()
        finally:
            self.stop()

    def _configure_extension(self, extension, locators):
        super()._configure_extension(extension, locators)
        try:
            with (self.profile.runtime / "app/config.properties").open("rb") as stream:
                config = javaproperties.load(stream)
        except OSError:
            raise QAError("Falta configuración preparada por qa.cmd para circuitos.") from None
        validate(self.fixtures, locators, config, self.case)
        self.variant = SimpleNamespace(products=PRODUCT_SET, exchange_rate="1500.00")

    def _oracle(self):
        return CircuitOracle(super()._oracle().connection, self.fixtures)

    def _assert_sale(self, line):
        return assert_basket(self, (line,))

    def _sell(self, product, quantity, price, received):
        business_step("Comenzar venta USD y tomar saldos de stock, caja y cuentas corrientes")
        before = self._oracle().snapshot()
        selected = next(item for item in PRODUCT_SET if item.ref == product)
        if before.basket.stock.get(selected.id, Decimal(0)) < Decimal(quantity):
            raise QAError("Stock insuficiente para el circuito: restaurar el baseline y aplicar el seed.")
        self.before = before.basket
        line = Line(product, quantity, price=str(Decimal(price)*1500),
                    original_price=price, original_discount="0")
        self._open_sale()
        self.driver.type("sale.quantity", quantity)
        self.driver.type("sale.code", "QA-CIR-" + product, enter=True)
        self._collect(line, received, before)
        self._assert_new_sale()
        after = self._oracle().snapshot()
        business_step("Conciliar una venta, su ingreso al Libro Diario y la salida de stock")
        assert_cash_sale(before, after, line, user_id=self.fixtures["context"]["usuario_id"], received=received)
        # FormVenta.puedeCerrarVenta no pide confirmación cuando no hay renglones.
        self.driver.keys("sale.code", "esc")
        self.driver.wait_gone("sale.code")
        self.driver.find("sale.closed_indicator")
        assert_unchanged(after, self._oracle().snapshot())

    def _collect(self, line, received, before):
        state = self._assert_sale(line)
        self._open_payment()
        check_payment_currencies(self)
        self._enter_payment(received, total=line.total)
        business_step("Cancelar el cobro; conservar venta, caja, deuda y stock")
        self.driver.click("payment.cancel")
        self.driver.wait_gone("payment.confirm")
        self._assert_same_sale(state)
        assert_unchanged(before, self._oracle().snapshot())
        self._assert_sale(line)
        self._open_payment()
        check_payment_currencies(self)
        self._enter_payment(received, total=line.total)
        self._confirm_payment()

    def _purchase_grid(self, expected):
        columns = self.driver.locators["elements"]["purchase.lines"]["columns"]
        count = self.driver.locators["elements"]["purchase.lines"]["column_count"]

        def check():
            rows = self.driver.table_rows("purchase.lines")
            if any(len(row) != count for row in rows):
                raise QAError("Columnas de remito incompatibles con la calibración.")
            self._equal(len(rows), len(expected), "Renglones del remito")
            total = Decimal(0)
            for code, price, currency in expected:
                found = [row for row in rows if row[columns["code"]] == code]
                self._equal(len(found), 1, "Producto recibido único")
                row = found[0]
                self._equal(row[columns["name"]] == code, True, "Nombre del producto recibido")
                self._equal(parse_quantity(row[columns["quantity"]]), Decimal(2), "Cantidad recibida")
                for key, amount in (("unit_price", price), ("total", price*2)):
                    self._equal(purchase_money(row[columns[key]]), (currency, amount), f"{code}: {key}")
                total += price*2*(1500 if currency == "USD" else 1)
            # El primer artículo es ARS; por eso la cabecera de este recorrido siempre es mixta/ARS.
            assert_money(self.driver.text("purchase.total"), total, "ARS", "Total del remito")
        self._wait_check(check)

    def _purchase(self):
        before = self._oracle().snapshot()
        if any(row["comEstado"] == 1 and enabled(row["comActivo"]) for row in before.extra["compra"]):
            raise QAError("Preparar paquete sin remitos abiertos; no reutilizar borradores ajenos al caso.")
        business_step("Cargar remito mixto ARS/USD al proveedor QA, sin pago ni bonificación")
        self.driver.click("menu.purchases")
        self.driver.click("menu.receipt")
        self.driver.click("purchase.provider")
        self.driver.click("purchase.provider_option")
        self.driver.expect_choice("purchase.provider", ("QA-SEED-PROVEEDOR", "980001|QA-SEED-PROVEEDOR"))
        self.driver.type("purchase.document", "QA-CIR-REM-001")
        self.driver.type("purchase.paid", "0")
        if parse_payment(self.driver.text("purchase.rate").strip().removeprefix("$").strip()) != 1500:
            raise QAError("Cotización del remito incompatible: se requiere 1500 ARS/USD.")
        for alias, value in (("purchase.stock", True), ("purchase.update_price", True),
                              ("purchase.bonus_price", False)):
            self.driver.expect_state(alias, "checked", value)
        expected = []
        for suffix in ("ARS-FIJO", "USD-FIJO", "ARS-CALCULADO", "USD-CALCULADO"):
            code, usd = "QA-CIR-" + suffix, suffix.startswith("USD")
            cost = Decimal(60 if usd else 600)
            business_step(f"Recibir dos unidades de {code} a {cost} {'USD' if usd else 'ARS'}")
            self.driver.type("purchase.code", code, enter=True)
            self._wait_check(lambda: self._equal(self.driver.text("purchase.name") == code, True,
                                                "Identidad del producto seleccionado"))
            self.driver.type("purchase.quantity", "2")
            self.driver.type("purchase.cost", str(cost))
            self.driver.type("purchase.discount", "0")
            self.driver.click("purchase.add")
            expected.append((code, cost, "USD" if usd else "ARS"))
            self._purchase_grid(expected)
        draft = self._oracle().snapshot()
        same_extra(before, draft, except_tables=("compra", "compra_detalle"))
        from products.xgestion.offer_journeys.oracles import assert_basket_unchanged

        assert_basket_unchanged(before.basket, draft.basket)
        business_step("Rechazar la carga del remito sin producir recepción, deuda ni cambios de precio")
        self.driver.click("purchase.confirm")
        self.driver.click("purchase.reject")
        self.driver.wait_gone("purchase.reject")
        self._purchase_grid(expected)
        assert_unchanged(draft, self._oracle().snapshot())
        business_step("Confirmar recepción y enviar el importe a cuenta corriente del proveedor")
        self.driver.click("purchase.confirm")
        self.driver.click("purchase.accept")
        self.driver.click("purchase.supplier_debt")
        self.driver.wait_gone("purchase.confirm", timeout=40)
        assert_purchase(before, self._oracle().snapshot())
        business_step("Vender una unidad USD calculada a su nuevo precio: USD 120 / ARS 180000")
        self._sell("USD-CALCULADO", "1", "120", "180000")

    def _shift_auth(self):
        # El login del turno puede quedar detrás de otra ventana modal: no capturarlo.
        self.authenticated = False
        self.driver.click("menu.sales")
        self.driver.click("menu.shift")
        with private_input():
            self.driver.type("shift.user", self.profile.env("QA_LOGIN_USER"), secret=True)
            self.driver.type("shift.password", self.profile.env("QA_LOGIN_PASSWORD"), secret=True)
            self.driver.click("shift.confirm")

    def _cash_report(self, opening, closing):
        start = opening["mosFechaHora"].strftime("%d/%m/%y %H:%M")
        end = closing["mosFechaHora"].strftime("%d/%m/%y %H:%M")
        label = f"{start} a {end}"
        self.driver.expect_choice("cash.turn", (label, f"{opening['mosId']}|{label}"))
        self.driver.expect_choice("cash.computer", (self.fixtures["circuits"]["cash_computer_label"],))
        business_step("Comprobar caja cerrada: efectivo y total ARS 150000, sin otros medios ni egresos")

        def check():
            for field in ("income", "expense", "cash", "credit", "debit", "other", "total"):
                expected = 150000 if field in ("cash", "total") else 0
                self._equal(parse_payment(self.driver.text("cash." + field)), Decimal(expected),
                            f"Caja {field} ARS")
        self._wait_check(check)
        self.driver.keys("cash.total", "esc")
        self.driver.wait_gone("cash.total")

    def _close_turn(self):
        oracle = self._oracle()
        before = oracle.snapshot()
        turns = before.extra["movimientos_sistema"]
        closed = {row["ID_MovimientoSistemaAsociado"] for row in turns
                  if row["ID_TipoMovimiento"] == 2 and enabled(row["activo"])}
        if (any(row["mosFechaHora"].date() == date.today() for row in turns)
                or any(row["ID_TipoMovimiento"] == 1 and enabled(row["activo"])
                       and row["mosId"] not in closed for row in turns)
                or any(row["venEstado"] == 0 and enabled(row["activo"]) for row in before.basket.rows["ventas"])):
            raise QAError("Caja requiere paquete sin turnos de hoy, turnos abiertos ni cuentas/mesas abiertas.")
        latest = max((row["mofFechaHora"] for row in before.basket.rows["movimientos_finanzas"]), default=None)
        if latest is not None:
            self._wait_check(lambda: self._equal(oracle.query("SELECT NOW() AS now", ())[0]["now"] > latest,
                                                True, "Separación temporal del turno anterior"))
        business_step("Abrir un turno nuevo y cancelar el ingreso inicial: fondo cero")
        self._shift_auth()
        self.driver.click("fund.cancel")
        self.driver.wait_gone("shift.confirm")
        self.authenticated = True
        opened = oracle.snapshot()
        opening_id = assert_turn(before, opened, user_id=self.fixtures["context"]["usuario_id"])
        opening = next(row for row in opened.extra["movimientos_sistema"] if row["mosId"] == opening_id)
        self._sell("USD-FIJO", "1", "100", "150000")
        paid = oracle.snapshot()
        business_step("Cerrar el turno una sola vez mediante Abrir/Cerrar Turno")
        self._shift_auth()
        # La ventana de balance se abre luego de persistir; esperarla antes del snapshot definitivo.
        self.driver.find("cash.total")
        finished = oracle.snapshot()
        closing_id = assert_turn(paid, finished, user_id=self.fixtures["context"]["usuario_id"], opening=opening_id)
        closing = next(row for row in finished.extra["movimientos_sistema"] if row["mosId"] == closing_id)
        self._cash_report(opening, closing)
        self.driver.wait_gone("shift.confirm")
        self.authenticated = True
        assert_unchanged(finished, oracle.snapshot())
        business_step("Volver a consultar el turno cerrado sin repetir venta, stock ni dinero")
        self.driver.click("menu.sales")
        self.driver.click("menu.cash_report")
        self._cash_report(opening, closing)
        assert_unchanged(finished, oracle.snapshot())
