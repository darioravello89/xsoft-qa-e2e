"""Los errores conservan valores útiles sin volcar autenticación ni filas SQL."""

from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest

from products.xgestion.driver import SemanticDriver
from products.xgestion.library import XGestionLibrary
from products.xgestion.oracles import Snapshot, XGestionOracle, assert_cancelled


def test_ui_mismatch_records_expected_and_last_observation():
    driver = SemanticDriver(Mock(), 42, {})
    driver.text = Mock(return_value="1.000,00")
    with patch("products.xgestion.driver.assertion_failed", create=True) as record:
        with pytest.raises(AssertionError, match="Texto inesperado"):
            driver.expect("sale.total", "2.000,00", timeout=0)
    assert record.call_args.kwargs == {"expected": "2.000,00", "observed": "1.000,00"}


@pytest.mark.parametrize("alias", ["login.user", "login.password"])
def test_authentication_values_never_reach_diagnostics(alias):
    driver = SemanticDriver(Mock(), 42, {})
    driver.text = Mock(return_value="UNKNOWN_PRIVATE_VALUE")
    with patch("products.xgestion.driver.assertion_failed", create=True) as record:
        with pytest.raises(AssertionError):
            driver.expect(alias, "ANOTHER_PRIVATE_VALUE", timeout=0)
    assert record.called
    assert "PRIVATE_VALUE" not in str(record.call_args)
    assert record.call_args.kwargs["expected"] == "[CAMPO DE ACCESO OMITIDO]"
    assert record.call_args.kwargs["observed"] == "[CAMPO DE ACCESO OMITIDO]"


def test_typing_trace_never_contains_entered_value():
    driver = SemanticDriver(Mock(), 42, {})
    driver.find = Mock(return_value=SimpleNamespace(enabled=True))
    with patch("products.xgestion.driver.diagnostic", create=True) as record:
        driver.type("products.search", "PRIVATE_PRODUCT_CODE")
    assert record.called
    assert "PRIVATE_PRODUCT_CODE" not in str(record.call_args_list)


def test_cancelled_sale_mismatch_reports_delta_instead_of_full_snapshot():
    before = Snapshot(frozenset({901, 902}), Decimal("20"), Decimal("50"))
    after = Snapshot(before.sale_ids, before.stock, Decimal("51"))
    with patch("products.xgestion.oracles.assertion_failed", create=True) as record:
        with pytest.raises(AssertionError, match="caja"):
            assert_cancelled(before, after)
    assert record.call_args.kwargs == {"expected": "0 ARS", "observed": "1 ARS"}
    assert "901" not in str(record.call_args)


def test_query_trace_has_counts_not_row_values_or_parameters():
    cursor = Mock()
    cursor.fetchall.return_value = [{"private_column": "PRIVATE_ROW_VALUE"}]
    connection = Mock()
    connection.cursor.return_value.__enter__ = Mock(return_value=cursor)
    connection.cursor.return_value.__exit__ = Mock(return_value=False)
    oracle = XGestionOracle(connection, {"context": {"empresa": 1, "sucursal": 2, "computadora": 3}})
    with patch("products.xgestion.oracles.diagnostic", create=True) as record:
        assert oracle.query("SELECT private_column FROM ventas WHERE Empresa=%s", ("PRIVATE_PARAMETER",))
    assert record.called
    assert record.call_args.kwargs["row_count"] == 1
    assert "PRIVATE_" not in str(record.call_args_list)
    assert "SELECT" not in str(record.call_args_list)


def test_sale_total_failure_records_the_actual_visible_total():
    library = XGestionLibrary()
    library.verify_context = Mock()
    library._oracle = Mock()
    library.fixtures = {"product": {"code": "SYNTHETIC"}}
    library.driver = Mock()
    library.driver.text.return_value = "1.000,00"
    with patch("products.xgestion.library.time.monotonic", side_effect=[0, 21]), \
         patch("products.xgestion.library.business_step") as step, \
         patch("products.xgestion.library.assertion_failed", create=True) as record:
        with pytest.raises(AssertionError, match="2000 ARS"):
            library.prepare_sale()
    assert record.call_args.kwargs == {"expected": "2000.00 ARS", "observed": "1000.00 ARS"}
    assert step.call_args.args == ("Comprobar el total antes de cobrar: $2.000,00 ARS",)
