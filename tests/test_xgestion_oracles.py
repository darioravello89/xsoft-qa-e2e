import subprocess
import sys
import unittest
from decimal import Decimal
from pathlib import Path

from products.xgestion.oracles import Snapshot, XGestionOracle, assert_cancelled, assert_sale

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
        }
        self.lines = [{"vecCodigo": "11", "vecCantidad": Decimal("2"),
                       "vecPrecio": Decimal("1000"), "vecTotal": Decimal("2000")}]
        self.payments = [{"ID_Pago": 1, "Cantidad": Decimal("2000"), "EsPagoACobrar": 0}]

    def check(self):
        return assert_sale(FIXTURE, self.before, self.after, self.sale,
                           self.lines, self.payments, Decimal("-2"), Decimal("2000"))

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
        self.payments[0]["ID_Pago"] = 8
        with self.assertRaisesRegex(AssertionError, "efectivo"):
            self.check()
        self.payments[0]["ID_Pago"] = 1
        self.lines[0]["vecCodigo"] = "12"
        with self.assertRaisesRegex(AssertionError, "producto"):
            self.check()

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
