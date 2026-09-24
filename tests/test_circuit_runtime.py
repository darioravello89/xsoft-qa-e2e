from copy import deepcopy
from unittest.mock import Mock

import pytest

from framework.errors import QAError
from products.xgestion.circuits.contracts import COMMON, PURCHASE, TURN, validate
from products.xgestion.circuits.library import XGestionCircuitsLibrary
from products.xgestion.offer_journeys.usd import PROFILE


def assets(case):
    from test_offer_usd_runtime import usd_assets

    fixtures, locators = usd_assets()
    fixtures["offer_usd"] = dict(PROFILE)
    fixtures["sale"] = {"cash_payment_id": 1}
    fixtures["circuits"] = {"schema_version": 1, "operator_role": "administrator",
                            "cash_computer_label": "QA-PUESTO"}
    locators["calibration"]["verified_features"].extend(
        ["circuitos-comerciales-v1", "remitos-circuito-v1", "caja-circuito-v1"])
    for alias in (*COMMON, *PURCHASE, *TURN):
        locators["elements"][alias] = {"window": "main", "query": f"name:{alias}"}
    locators["elements"]["sale.lines"].update(column_count=7,
        columns={name: i for i, name in enumerate(("code", "name", "quantity", "unit_price",
                                                  "total", "gross_total", "offer_discount"))})
    locators["elements"]["purchase.lines"].update(column_count=14,
        columns={"code": 1, "name": 2, "quantity": 3, "unit_price": 5, "total": 8})
    config = {"venta.convertirProductosUsdAPesos": "false", "pedirPagoAlCerrarTicket": "true",
              "venta.habilitarCierreAperturaTurno": "true", "venta.habilitarCierreCiego": "false",
              "ventas.cerrarSistemaConCierreDeTurno": "false"}
    return fixtures, locators, config


@pytest.mark.parametrize("case", ["XG-FIN-011", "XG-FIN-013", "XG-FIN-014"])
def test_calibrated_profiles_accepted(case):
    validate(*assets(case), case)


@pytest.mark.parametrize("defect", ["feature", "draft", "cash", "conversion", "blind", "exit", "columns"])
def test_incompatible_profile_blocks_before_start(defect):
    fixtures, locators, config = assets("XG-FIN-014")
    case = "XG-FIN-014"
    if defect == "feature":
        locators["calibration"]["verified_features"] = []
    elif defect == "draft":
        locators["elements"]["shift.user"]["query"] = "CALIBRAR"
    elif defect == "cash":
        fixtures["sale"]["cash_payment_id"] = 9
    elif defect == "conversion":
        config["venta.convertirProductosUsdAPesos"] = "true"
    elif defect == "blind":
        config["venta.habilitarCierreCiego"] = "true"
    elif defect == "exit":
        config["ventas.cerrarSistemaConCierreDeTurno"] = "true"
    else:
        case = "XG-FIN-013"
        locators["elements"]["purchase.lines"]["columns"]["total"] = 30
    with pytest.raises(QAError):
        validate(fixtures, locators, config, case)


def test_customer_account_remains_blocked_without_double_click_or_jar_start():
    library = XGestionCircuitsLibrary()
    library.start = Mock()
    with pytest.raises(QAError, match="atajo"):
        library.run_circuit("XG-FIN-012")
    library.start.assert_not_called()


@pytest.mark.parametrize("bad_profile", [None, [], "private-value"])
def test_malformed_private_profile_is_blocked_without_its_content(bad_profile):
    fixtures, locators, config = assets("XG-FIN-011")
    fixtures["circuits"] = bad_profile
    with pytest.raises(QAError) as error:
        validate(fixtures, locators, config, "XG-FIN-011")
    assert "private-value" not in str(error.value)


def test_sale_grid_needs_currency_discount_and_gross_columns_before_start():
    fixtures, locators, config = assets("XG-FIN-011")
    del locators["elements"]["sale.lines"]["columns"]["gross_total"]
    with pytest.raises(QAError):
        validate(fixtures, locators, config, "XG-FIN-011")


def test_reauthentication_failure_cannot_capture_credentials():
    library = XGestionCircuitsLibrary()
    library.driver, library.profile = Mock(), Mock()
    library.profile.env.return_value = "SECRET-CANARY"
    library.authenticated = True
    library.driver.click.side_effect = RuntimeError("window vanished")
    with pytest.raises(RuntimeError):
        library._shift_auth()
    assert library.authenticated is False


def test_purchase_number_format_is_distinct_from_sale_format():
    from products.xgestion.circuits.library import purchase_money

    assert purchase_money("$ 1,200.00") == ("ARS", 1200)
    assert purchase_money("USD 120.00") == ("USD", 120)
    for value in ("USD 120,00", "SECRET-CANARY", "120.00", "USD NaN"):
        with pytest.raises(AssertionError) as error:
            purchase_money(value)
        assert value not in str(error.value)


def test_cancel_payment_checks_snapshot_before_confirming(monkeypatch):
    from products.xgestion.circuits import library as module

    lib = XGestionCircuitsLibrary()
    lib.fixtures = {"context": {"usuario_id": 5}}
    lib.driver = Mock()
    lib._assert_sale = Mock(return_value=((), 300000))
    lib._open_payment = Mock()
    lib._enter_payment = Mock()
    lib._confirm_payment = Mock()
    lib._assert_same_sale = Mock()
    lib._oracle = Mock()
    lib._oracle.return_value.snapshot.side_effect = AssertionError("cancel changed stock")
    monkeypatch.setattr(module, "check_payment_currencies", Mock())
    with pytest.raises(AssertionError):
        lib._collect(Mock(total=300000), "350000", deepcopy(Mock()))
    lib._confirm_payment.assert_not_called()
