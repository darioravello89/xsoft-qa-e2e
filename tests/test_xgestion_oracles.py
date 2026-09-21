import subprocess
import sys
import unittest
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

from products.xgestion.oracles import (
    Snapshot,
    XGestionOracle,
    assert_cancelled,
    assert_sale,
    assert_unchanged,
)

FIXTURE = {
    "context": {"empresa": 91, "sucursal": 2, "computadora": 3, "usuario_id": 7},
    "product": {"id": 11, "quantity": 2, "unit_price": "1000.00"},
    "sale": {"cash_payment_id": 1, "non_fiscal_document_id": 99},
}


class OracleTests(unittest.TestCase):
    def setUp(self):
        self.before = Snapshot(frozenset({4}), Decimal("20"), Decimal("50"))
        self.after = Snapshot(frozenset({4, 5}), Decimal("18"), Decimal("2050"))
        self.sale = {
            "venId": 5, "venTotal": Decimal("2000"), "venEstado": 1,
            "venUsuario": 7, "venPago": 1, "ID_TipoComprobante": 99,
            "CAENumero": "", "activo": 1,
            "Pagado": Decimal("2000"), "Vuelto": Decimal("0"), "esPagoMultiple": 0,
        }
        self.lines = [{"vecCodigo": "11", "vecCantidad": Decimal("2"),
                       "vecPrecio": Decimal("1000"), "vecTotal": Decimal("2000"), "activo": 1}]
        self.payments = []
        self.stock = [{"moaArticuloCodigo": 11, "moaCantidad": Decimal("-2"), "activo": 1}]
        self.cash = [{"mofPago": 1, "mofIngreso": Decimal("2000"), "mofEgreso": Decimal("0"),
                      "mofEstado": 1, "mofConcepto": 2, "ID_VentaPago": 0, "activo": 1}]

    def check(self, **kwargs):
        return assert_sale(FIXTURE, self.before, self.after, self.sale,
                           self.lines, self.payments, self.stock, self.cash, **kwargs)

    def test_exact_sale_stock_cash_and_payment(self):
        self.assertEqual(self.check(), 5)

    def test_rejects_unrelated_extra_sale(self):
        self.after = Snapshot(frozenset({4, 5, 6}), Decimal("18"), Decimal("2050"))
        with self.assertRaisesRegex(AssertionError, "exactamente una"):
            self.check()

    def test_rejects_fiscal_cae_even_when_total_matches(self):
        self.sale["CAENumero"] = "123"
        with self.assertRaisesRegex(AssertionError, "fiscal"):
            self.check()

    def test_rejects_wrong_payment_and_product(self):
        self.cash[0]["mofPago"] = 8
        with self.assertRaisesRegex(AssertionError, "efectivo"):
            self.check()
        self.cash[0]["mofPago"] = 1
        self.lines[0]["vecCodigo"] = "12"
        with self.assertRaisesRegex(AssertionError, "producto"):
            self.check()

    def test_received_money_and_change_do_not_inflate_sale_or_cash(self):
        self.sale.update(Pagado=Decimal("3000"), Vuelto=Decimal("1000"))
        self.assertEqual(self.check(received=Decimal("3000")), 5)
        self.sale["Vuelto"] = Decimal("0")
        with self.assertRaisesRegex(AssertionError, "vuelto"):
            self.check(received=Decimal("3000"))

    def test_simple_payment_rejects_even_inactive_multiple_payment_rows(self):
        self.payments = [{"ID_Pago": 1, "Cantidad": Decimal("2000"), "EsPagoACobrar": 0, "activo": 0}]
        with self.assertRaisesRegex(AssertionError, "ventas_pagos"):
            self.check()

    def test_zero_net_extra_cash_and_stock_movements_are_not_accepted(self):
        self.cash += [dict(self.cash[0], mofIngreso=Decimal("100")),
                      dict(self.cash[0], mofIngreso=Decimal("0"), mofEgreso=Decimal("100"))]
        with self.assertRaisesRegex(AssertionError, "movimiento.*caja"):
            self.check()
        self.cash = self.cash[:1]
        self.stock += [dict(self.stock[0], moaCantidad=Decimal("1")),
                       dict(self.stock[0], moaCantidad=Decimal("-1"))]
        with self.assertRaisesRegex(AssertionError, "movimiento.*stock"):
            self.check()

    def test_inactive_or_wrong_product_stock_is_not_accepted(self):
        self.stock[0]["activo"] = 0
        with self.assertRaisesRegex(AssertionError, "stock"):
            self.check()
        self.stock[0].update(activo=1, moaArticuloCodigo=999)
        with self.assertRaisesRegex(AssertionError, "stock"):
            self.check()

    def test_cash_with_correct_net_but_wrong_received_structure_is_rejected(self):
        self.cash[0].update(mofIngreso=Decimal("3000"), mofEgreso=Decimal("1000"))
        with self.assertRaisesRegex(AssertionError, "[Cc]aja"):
            self.check()

    def test_second_operation_cannot_substitute_the_first_sale_identity(self):
        self.assertEqual(self.check(expected_sale_id=5), 5)
        with self.assertRaisesRegex(AssertionError, "identidad"):
            self.check(expected_sale_id=6)

    def test_unchanged_detects_new_business_rows_with_unchanged_totals(self):
        before = Snapshot(frozenset({4}), Decimal("20"), Decimal("50"),
                          business_state=(("ventas_pagos", 0, "empty"),))
        after = Snapshot(before.sale_ids, before.stock, before.cash,
                         business_state=(("ventas_pagos", 1, "changed"),))
        with self.assertRaisesRegex(AssertionError, "registros"):
            assert_unchanged(before, after)
        with self.assertRaisesRegex(AssertionError, "registros"):
            assert_cancelled(before, after)
        assert_unchanged(before, before)

    def test_new_sale_rejects_orphan_payment_elsewhere_in_same_scope(self):
        counts = {"ventas": 1, "ventas_cuerpo": 1, "ventas_pagos": 0,
                  "movimientos_articulos": 2, "movimientos_finanzas": 1}
        before_state = tuple((table, count, "before") for table, count in counts.items())
        after_state = tuple((table, count + 1, "after") for table, count in counts.items())
        self.before = Snapshot(self.before.sale_ids, self.before.stock, self.before.cash, before_state)
        self.after = Snapshot(self.after.sale_ids, self.after.stock, self.after.cash, after_state)
        with self.assertRaisesRegex(AssertionError, "registros.*ventas_pagos"):
            self.check()

    def test_snapshot_detects_orphans_compensated_movements_and_updates_without_logging_rows(self):
        oracle = XGestionOracle(None, FIXTURE)
        tables = {"ventas": [{"venId": 4, "venTotal": Decimal("123")}, {"venId": 3, "venTotal": Decimal("42")}],
                  "ventas_cuerpo": [], "ventas_pagos": [], "movimientos_articulos": [], "movimientos_finanzas": []}

        def query(sql, params):
            if "COALESCE(SUM(" in sql:
                return [{"total": Decimal("10")}]
            return tables[sql.split(" FROM ", 1)[1].split()[0]]

        oracle.query = query
        before = oracle.snapshot()
        tables["ventas"].reverse()
        assert_unchanged(before, oracle.snapshot())
        tables["ventas_pagos"].append({"ID_VentaPago": 9, "Cantidad": Decimal("2000"), "ID_Venta": 999})
        with patch("products.xgestion.oracles.assertion_failed") as failure:
            with self.assertRaisesRegex(AssertionError, "registros"):
                assert_unchanged(before, oracle.snapshot())
            self.assertNotIn("999", str(failure.call_args))
        tables["ventas_pagos"].clear()
        tables["movimientos_articulos"] = [{"moaId": 1, "moaCantidad": Decimal("1")},
                                           {"moaId": 2, "moaCantidad": Decimal("-1")}]
        with self.assertRaisesRegex(AssertionError, "registros"):
            assert_unchanged(before, oracle.snapshot())
        tables["movimientos_articulos"].clear()
        tables["ventas"][0]["venTotal"] = Decimal("43")
        with self.assertRaisesRegex(AssertionError, "registros"):
            assert_unchanged(before, oracle.snapshot())

    def test_verify_sale_queries_all_sale_rows_and_forwards_received_and_identity(self):
        oracle = XGestionOracle(None, FIXTURE)
        oracle.snapshot = lambda: self.after
        calls = []
        table_rows = {"ventas": [dict(self.sale, Pagado=Decimal("3000"), Vuelto=Decimal("1000"))],
                      "ventas_cuerpo": self.lines, "ventas_pagos": self.payments,
                      "movimientos_articulos": self.stock, "movimientos_finanzas": self.cash}

        def query(sql, params):
            calls.append((sql, params))
            return table_rows[sql.split(" FROM ", 1)[1].split()[0]]

        oracle.query = query
        self.assertEqual(oracle.verify_sale(self.before, received=Decimal("3000"), expected_sale_id=5), 5)
        self.assertEqual(len(calls), 5)
        for sql, params in calls:
            self.assertEqual(params, (91, 2, 3, 5))
            self.assertNotIn("activo=1", sql)
            self.assertNotIn("SUM(", sql)
        with self.assertRaisesRegex(AssertionError, "identidad"):
            oracle.verify_sale(self.before, received=Decimal("3000"), expected_sale_id=6)

    def test_cancel_asserts_stock_and_money_also(self):
        assert_cancelled(self.before, self.before)
        with self.assertRaisesRegex(AssertionError, "caja"):
            assert_cancelled(self.before, Snapshot(frozenset({4}), Decimal("20"), Decimal("51")))

    def test_wrong_sale_user_is_not_accepted(self):
        self.sale["venUsuario"] = 999
        with self.assertRaisesRegex(AssertionError, "usuario"):
            self.check()

    def test_oracle_refuses_writes_before_opening_cursor(self):
        oracle = XGestionOracle(None, FIXTURE)
        with self.assertRaisesRegex(ValueError, "SELECT"):
            oracle.query("DELETE FROM ventas", ())

    def test_snapshot_uses_scope_parameters_and_product_id(self):
        oracle = XGestionOracle(None, FIXTURE)
        calls = []

        def query(sql, params):
            calls.append((sql, params))
            if sql.startswith("SELECT venId"):
                return [{"venId": 4}]
            return [{"total": Decimal("10")}]

        oracle.query = query
        oracle.snapshot()
        self.assertEqual(calls[0][1], (91, 2, 3))
        self.assertEqual(calls[1][1], (91, 2, 11))
        self.assertEqual(calls[2][1], (91, 2, 3, 1))
        for sql, params in calls:
            self.assertEqual(sql.count("%s"), len(params))
            self.assertNotIn("91", sql)

    def test_wrong_sale_total_is_rejected_under_python_optimization(self):
        code = (
            "import sys;sys.path.insert(0,'tests');"
            "from test_xgestion_oracles import OracleTests;"
            "test=OracleTests();test.setUp();test.sale['venTotal']=1;test.check()"
        )
        result = subprocess.run([sys.executable, "-O", "-c", code],
                                cwd=Path(__file__).resolve().parents[1],
                                capture_output=True, text=True, check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Total persistido", result.stderr)


if __name__ == "__main__":
    unittest.main()
