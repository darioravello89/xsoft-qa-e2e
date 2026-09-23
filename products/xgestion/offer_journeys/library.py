"""Recorridos de vendedor con canastas fijas y evidencia por renglón."""

import json
import os
from dataclasses import replace
from datetime import date
from decimal import Decimal

from robot.api.deco import keyword

from framework.errors import QAError
from framework.events import business_step
from products.xgestion.library import XGestionLibrary, parse_ars, parse_quantity
from products.xgestion.offer_journeys.contracts import validate_calibration, validate_journey
from products.xgestion.offer_journeys.model import PAYMENT_METHODS
from products.xgestion.offer_journeys.oracles import BasketOracle, assert_basket_sale, assert_basket_unchanged
from products.xgestion.oracles import enabled
from products.xgestion.promotions import SEED


class XGestionOfferJourneysLibrary(XGestionLibrary):
    @keyword("Ejecutar Recorrido De Ofertas")
    def run_journey(self, case_id):
        if (os.environ.get("XSOFT_QA_SEED") != SEED
                or os.environ.get("XSOFT_QA_SEED_DATE") != date.today().isoformat()):
            raise QAError("Ofertas requiere el seed verificado en esta corrida y fecha. Usar qa.cmd run --seed.")
        from products.xgestion.offer_journeys.catalog import get_journey

        journey = get_journey(case_id)
        validate_journey(journey)
        from framework.profile_runs import PROFILE_VARIANTS

        selected = os.environ.get("XSOFT_QA_OFFER_VARIANT")
        receipt = os.environ.get("XSOFT_QA_OFFER_PROFILE")
        if case_id in PROFILE_VARIANTS:
            try:
                if (selected not in PROFILE_VARIANTS[case_id]
                        or json.loads(receipt or "null") != {"case_id": case_id, "variant": selected}):
                    raise ValueError()
            except (ValueError, TypeError):
                raise QAError("El caso requiere todos sus perfiles preparados por qa.cmd; falta recibo de fase.") from None
        elif selected or receipt:
            raise QAError("No se permite omitir variantes de un caso sin perfiles.")
        variants = [variant for variant in journey.variants if not selected or variant.name == selected]
        if not variants:
            raise QAError("La variante solicitada no pertenece al recorrido de ofertas.")
        for variant in variants:
            self.variant = variant
            self.expected = ()
            business_step(f"{case_id}: comenzar variante {variant.name}")
            self.start("ventas-etapa1")
            self.login()
            for step in variant.steps:
                self._perform(step)
            self.stop()

    @keyword("Finalizar Recorrido De Ofertas")
    def finish_journey(self):
        # Un fallo conserva la ventana hasta el teardown. No captura autenticación.
        try:
            self.screenshot()
        finally:
            self.stop()

    def _configure_extension(self, extension, locators):
        super()._configure_extension(extension, locators)
        validate_calibration(self.fixtures, locators, self.variant)
        self.new_sale_ready = False
        self.payment_id = self.fixtures["sale"]["cash_payment_id"]
        self.payment_ref = None

    def _oracle(self):
        connection = super()._oracle().connection
        return BasketOracle(connection, self.fixtures, self.variant.products, self.payment_id)

    def _assert_basket(self, expected):
        if self.variant.exchange_rate is not None:
            from products.xgestion.offer_journeys.usd import assert_basket

            return assert_basket(self, expected)
        columns = self.driver.locators["elements"]["sale.lines"]["columns"]
        products = {product.ref: product for product in self.variant.products}
        total = sum((line.total for line in expected), Decimal(0))
        business_step(f"Comprobar {len(expected)} renglones, sus descuentos y total {total} ARS")

        def check():
            state = self._sale_state()
            rows, observed_total = state
            self._equal(len(rows), len(expected), "Cantidad de renglones")
            for line in expected:
                product = products[line.product]
                matches = [row for row in rows if row[columns["code"]] == product.code]
                self._equal(len(matches), 1, f"Renglón único de {product.code}")
                row = matches[0]
                self._equal(row[columns["name"]] == product.code, True, "Nombre del producto esperado")
                self._equal(parse_quantity(row[columns["quantity"]]), Decimal(line.quantity),
                            f"Cantidad de {product.code}")
                for field, amount, label in (
                    ("unit_price", Decimal(line.price), "Precio unitario ARS"),
                    ("gross_total", line.gross, "Importe bruto ARS"),
                    # FormVenta.generarTabla muestra automático + manual en Descuentos.
                    ("offer_discount", Decimal(line.discount) + Decimal(line.manual), "Descuentos visibles ARS"),
                    ("total", line.total, "Neto del renglón ARS"),
                ):
                    self._equal(parse_ars(row[columns[field]], private=True), amount, f"{product.code}: {label}")
            self._equal(observed_total, total, "Total de la canasta ARS")
            return state

        return self._wait_check(check)

    def _open_basket(self):
        self.verify_context()
        self.payment_id = self.fixtures["sale"]["cash_payment_id"]
        self.payment_ref = None
        oracle = self._oracle()
        today = oracle.query("SELECT CURDATE() AS today", ())
        if len(today) != 1 or str(today[0]["today"]) != os.environ.get("XSOFT_QA_SEED_DATE"):
            raise QAError("Cambió la fecha del seed. Repetir la corrida desde su preparación.")
        if self.variant.exchange_rate is not None:
            oracle.validate_currency_schema()
        self.before = oracle.snapshot()
        for product in self.variant.products:
            required = max((Decimal(line.quantity) for step in self.variant.steps
                            for line in step.expected if line.product == product.ref), default=Decimal(0))
            if self.before.stock[product.id] < required:
                raise QAError(f"Stock insuficiente para {product.code}; revisar baseline y seed.")
        if self.new_sale_ready:
            self._assert_new_sale()
            self._select_document()
        else:
            self._open_sale()
        self.new_sale_ready = False
        self.expected = ()

    def _open_editor(self, product):
        column = self.driver.locators["elements"]["sale.lines"]["columns"]["code"]
        self.driver.select_sale_row("sale.lines", column, product.code)
        self.driver.shortcut("sale.lines", "ctrl+e")
        self.driver.expect("editor.product", product.code)
        self.driver.expect_focus("editor.quantity")

    def _perform(self, step):
        if step.action == "open":
            self._open_basket()
            return
        products = {product.ref: product for product in self.variant.products}
        if step.action == "add":
            product = products[step.product]
            business_step(f"Agregar {step.value} unidades de {product.code}")
            self.driver.type("sale.quantity", step.value)
            self.driver.type("sale.code", product.code, enter=True)
        elif step.action in {"edit", "remove"}:
            self._assert_basket(self.expected)
            product = products[step.product]
            business_step(f"{'Modificar cantidad de' if step.action == 'edit' else 'Eliminar'} {product.code}")
            self._open_editor(product)
            if step.action == "edit":
                self.driver.type("editor.quantity", step.value)
                self.driver.click("editor.save")
            else:
                self.driver.click("editor.remove")
            self.driver.wait_gone("editor.save")
            if step.action == "edit":
                column = self.driver.locators["elements"]["sale.lines"]["columns"]["code"]
                self.driver.expect_sale_row_selected("sale.lines", column, product.code)
                self.driver.expect_focus("sale.lines")
        elif step.action == "abandon":
            self._assert_basket(self.expected)
            self.cancel_sale()
            assert_basket_unchanged(self.before, self._oracle().snapshot())
            self.expected = ()
            return
        elif step.action in {"pay", "cancel_payment"}:
            self._collect(step)
            return
        elif step.action == "price_list":
            self._choose_price_list(step.value)
        elif step.action == "payment_method":
            self._choose_payment(step.value)
        elif step.action in {"manual", "manual_blocked"}:
            self._edit_manual(step, products[step.product])
        elif step.action != "check":
            raise QAError("Acción de ofertas sin implementación.")
        self._assert_basket(step.expected)
        self.expected = step.expected

    def _edit_manual(self, step, product):
        self._assert_basket(self.expected)
        business_step(f"Comprobar permiso y descuento manual de {product.code}")
        self._open_editor(product)
        allowed = step.action == "manual"
        self.driver.expect_state("editor.manual", "editable", allowed)
        self.driver.expect_state("editor.manual", "focusable", allowed)
        self.driver.expect_state("editor.manual_percent", "enabled", allowed)
        self.driver.expect_state("editor.manual_percent", "checked", False)
        if allowed:
            self.driver.type("editor.manual", step.value)
        def action():
            self.driver.click("editor.save")
        notice = next((r for r in self.variant.requirements if r in {"warning-on", "warning-off"}), None)
        if notice:
            observation = self.fixtures["offer_journeys"]["manual_warning_observation"]
            business_step("Comprobar el aviso de riesgo según el perfil")
            self.driver.observe_notice("editor.manual_warning", action, expected=notice == "warning-on",
                                       duration=observation["duration_seconds"],
                                       max_gap=observation["max_sample_gap_seconds"])
        else:
            action()
        self.driver.wait_gone("editor.save")

    def _pick_payment(self, reference):
        payment_id, name = PAYMENT_METHODS[reference]
        columns = self.driver.locators["elements"]["payment_picker.lines"]["columns"]
        self.driver.select_sale_row("payment_picker.lines", columns["name"], name)
        rows = self.driver.table_rows("payment_picker.lines")
        matches = [row for row in rows if row[columns["name"]] == name]
        self._equal(len(matches), 1, "Medio QA único")
        self._equal(matches[0][columns["id"]], str(payment_id), "Identidad del medio QA")
        self.driver.keys("payment_picker.search", "enter")
        self.driver.wait_gone("payment_picker.search")

    def _choose_payment(self, reference):
        payment_id, name = PAYMENT_METHODS[reference]
        business_step(f"Elegir medio {name} y comprobar el recálculo")
        self.driver.click("sale.choose_payment")
        self._pick_payment(reference)
        self.driver.expect("sale.payment_method", name)
        self.payment_id, self.payment_ref = payment_id, reference
        # El snapshot inicial contiene todos los medios del mismo contexto.
        # Sólo cambia qué saldo inicial se compara, nunca el estado persistido.
        initial = sum((Decimal(str(row["mofIngreso"])) - Decimal(str(row["mofEgreso"]))
                       for row in self.before.rows["movimientos_finanzas"]
                       if row["mofPago"] == payment_id and enabled(row["activo"])), Decimal(0))
        self.before = replace(self.before, cash=initial)

    def _open_payment(self):
        if "manual-payments" not in self.variant.requirements:
            if self.before is None:
                raise QAError("Falta preparar la venta antes de cobrar.")
            business_step("Abrir cobro y seleccionar el efectivo del perfil por su identidad")
            self.driver.click("sale.close")
            columns = self.driver.locators["elements"]["payment_picker.lines"]["columns"]
            identifier = str(self.fixtures["sale"]["cash_payment_id"])
            self.driver.select_sale_row("payment_picker.lines", columns["id"], identifier)
            rows = self.driver.table_rows("payment_picker.lines")
            matches = [row for row in rows if row[columns["id"]] == identifier]
            self._equal(len(matches), 1, "Identidad única del efectivo del perfil")
            name = matches[0][columns["name"]]
            if not isinstance(name, str) or not name.strip():
                raise QAError("Falta el nombre accesible del efectivo seleccionado.")
            self.driver.keys("payment_picker.search", "enter")
            self.driver.wait_gone("payment_picker.search")
            self.driver.expect_choice("payment.method", (name, f"{identifier}|{name}"))
            return
        if self.before is None or self.payment_ref not in PAYMENT_METHODS:
            raise QAError("Falta seleccionar un medio manual QA antes de cobrar.")
        business_step(f"Abrir cobro simple en {PAYMENT_METHODS[self.payment_ref][1]}")
        self.driver.click("sale.close")
        self._pick_payment(self.payment_ref)
        payment_id, name = PAYMENT_METHODS[self.payment_ref]
        self.driver.expect_choice("payment.method", (name, f"{payment_id}|{name}"))

    def _choose_price_list(self, reference):
        selected = next(item for item in self.variant.price_lists if item.ref == reference)
        business_step(f"Elegir lista {selected.name} y comprobar su nombre")
        self.driver.click("sale.choose_price_list")
        column = self.driver.locators["elements"]["list_picker.lines"]["columns"]["name"]
        self.driver.select_sale_row("list_picker.lines", column, selected.name)
        # Enter se procesa en el buscador y confirma la fila seleccionada.
        # Retipar el filtro regeneraría la tabla y podría perder esa selección.
        self.driver.keys("list_picker.search", "enter")
        self.driver.wait_gone("list_picker.search")
        self.driver.expect("sale.price_list", selected.name)

    def _enter_payment(self, received, *, total=Decimal("2000")):
        if self.variant.exchange_rate is not None:
            from products.xgestion.offer_journeys.usd import check_payment_currencies

            check_payment_currencies(self)
        super()._enter_payment(received, total=total)
        if self.variant.exchange_rate is not None:
            check_payment_currencies(self)

    def _collect(self, step):
        state = self._assert_basket(step.expected)
        total = sum((line.total for line in step.expected), Decimal(0))
        self._open_payment()
        self._enter_payment(str(total), total=total)
        if step.action == "cancel_payment":
            business_step("Cancelar el cobro y conservar toda la canasta sin movimientos")
            self.driver.click("payment.cancel")
            self.driver.wait_gone("payment.confirm")
            self._assert_same_sale(state)
            if self.variant.exchange_rate is not None:
                self._assert_basket(step.expected)
            assert_basket_unchanged(self.before, self._oracle().snapshot())
            return
        self._confirm_payment()
        business_step("Comprobar una venta y un cobro, con ofertas y stock correctos por producto")
        self._wait_check(lambda: assert_basket_sale(
            self.variant.products, step.expected, self.before, self._oracle().snapshot(),
            user_id=self.fixtures["context"]["usuario_id"], payment_id=self.payment_id,
            received=self.received, exchange_rate=self.variant.exchange_rate))
        self.expected = ()
        self.new_sale_ready = True

