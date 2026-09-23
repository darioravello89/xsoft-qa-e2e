"""No aprobar el importe de la captura ni inferir moneda de un número sin unidad."""

from copy import deepcopy
from datetime import date
from decimal import Decimal
from unittest.mock import Mock

import pytest
from test_offer_journey_library import assets

from framework.errors import QAError
from products.xgestion import library as base
from products.xgestion.offer_journeys.catalog import get_journey
from products.xgestion.offer_journeys.contracts import validate_calibration
from products.xgestion.offer_journeys.library import XGestionOfferJourneysLibrary


def usd_assets():
    fixtures, locators = assets()
    fixtures["offer_usd"] = {"schema_version": 1, "product_currency": "USD", "row_currency": "USD",
                             "document_currency": "ARS", "payment_currency": "ARS",
                             "exchange_rate": "1500.00"}
    locators["calibration"]["verified_features"].append("ofertas-usd-v1")
    for alias in ("editor.remove", "sale.usd_rate", "payment.total_currency",
                  "payment.amount_currency", "payment.change_currency"):
        locators["elements"][alias] = {"window": "main", "query": f"name:{alias}"}
    return fixtures, locators


@pytest.fixture
def usd_basket(monkeypatch):
    monkeypatch.setattr(base, "UI_TIMEOUT", 0)
    lib = XGestionOfferJourneysLibrary()
    lib.variant = get_journey("XG-PRM-080").variants[0]
    lib.fixtures, locators = usd_assets()
    lib.journeys = lib.keyboard_sales = True
    lib.driver = Mock()
    lib.driver.locators = locators
    lib.driver.table_rows.return_value = [[lib.variant.products[0].code, lib.variant.products[0].code,
                                          "1.0", "USD 100,00", "USD 50,00", "USD 100,00", "USD 50,00"]]
    values = {"sale.total": "$ 75.000,00", "sale.usd_rate": "1500.00",
              "payment.total_currency": "ARS", "payment.amount_currency": "ARS",
              "payment.change_currency": "ARS", "payment.total": "75000.00",
              "payment.amount": "75000.00", "payment.change": "0.00"}
    lib.driver.text.side_effect = values.__getitem__
    lib.test_values = values
    return lib


def test_usd_grid_and_ars_total_pass(usd_basket):
    usd_basket._assert_basket(usd_basket.variant.steps[1].expected)


@pytest.mark.parametrize("change", ["reported_bug", "double_conversion", "duplicated_discount",
                                   "wrong_row_currency", "wrong_total_currency", "bare_total", "private_text"])
def test_currency_and_amount_mismatch_cannot_pass(usd_basket, change):
    row = usd_basket.driver.table_rows.return_value[0]
    if change == "reported_bug":
        row[4], row[6] = "USD 0,03", "USD 99,97"
        usd_basket.test_values["sale.total"] = "$ 50,00"
    elif change == "double_conversion":
        usd_basket.test_values["sale.total"] = "$ 112.500.000,00"
    elif change == "duplicated_discount":
        row[6] = "USD 100,00"
    elif change == "wrong_row_currency":
        row[3] = "$ 100,00"
    elif change == "wrong_total_currency":
        usd_basket.test_values["sale.total"] = "USD 75.000,00"
    elif change == "bare_total":
        usd_basket.test_values["sale.total"] = "75.000,00"
    else:
        row[3] = "PRIVATE-NAME-CANARY"
    with pytest.raises(AssertionError) as error:
        usd_basket._assert_basket(usd_basket.variant.steps[1].expected)
    assert "PRIVATE-NAME-CANARY" not in str(error.value)
    if change == "reported_bug":
        assert "ARS" in str(error.value) and "75000" in str(error.value) and "50" in str(error.value)


def test_wrong_live_exchange_rate_is_blocked(usd_basket):
    usd_basket.test_values["sale.usd_rate"] = "1000.00"
    with pytest.raises(QAError, match="cotización"):
        usd_basket._assert_basket(usd_basket.variant.steps[1].expected)


@pytest.mark.parametrize("change", ["feature", "rate", "profile", "row", "payment_locator"])
def test_missing_or_incompatible_usd_calibration_is_blocked(change):
    fixtures, locators = usd_assets()
    if change == "feature":
        locators["calibration"]["verified_features"].remove("ofertas-usd-v1")
    elif change == "profile":
        del fixtures["offer_usd"]
    elif change == "rate":
        fixtures["offer_usd"]["exchange_rate"] = "1"
    elif change == "row":
        fixtures["offer_usd"]["row_currency"] = "ARS"
    else:
        del locators["elements"]["payment.amount_currency"]
    with pytest.raises(QAError):
        validate_calibration(fixtures, locators, get_journey("XG-PRM-080").variants[0])


def test_valid_calibration_does_not_mutate_ars_or_usd_assets():
    fixtures, locators = usd_assets()
    before = deepcopy((fixtures, locators))
    validate_calibration(fixtures, locators, get_journey("XG-PRM-080").variants[0])
    assert before == (fixtures, locators)


def test_payment_checks_currency_as_well_as_numbers_before_confirmation(usd_basket):
    usd_basket._enter_payment("75000.00", total=Decimal(75000))
    usd_basket.test_values["payment.amount_currency"] = "USD"
    with pytest.raises(QAError, match="ARS"):
        usd_basket._enter_payment("75000.00", total=Decimal(75000))
    usd_basket.driver.click.assert_not_called()


@pytest.mark.parametrize("number,count", [(80, 2), (81, 3), (82, 3), (83, 3), (84, 2)])
def test_usd_case_runs_every_required_variant_without_profile_omission(monkeypatch, number, count):
    monkeypatch.setenv("XSOFT_QA_SEED", "catalogo-comercial-v1")
    monkeypatch.setenv("XSOFT_QA_SEED_DATE", date.today().isoformat())
    monkeypatch.delenv("XSOFT_QA_OFFER_VARIANT", raising=False)
    monkeypatch.delenv("XSOFT_QA_OFFER_PROFILE", raising=False)
    library = XGestionOfferJourneysLibrary()
    library.start, library.login, library._perform, library.stop = Mock(), Mock(), Mock(), Mock()
    identifier = f"XG-PRM-{number:03}"
    library.run_journey(identifier)
    assert library.start.call_count == library.stop.call_count == count
    assert [call.args[0] for call in library._perform.call_args_list] == [
        step for variant in get_journey(identifier).variants for step in variant.steps]


@pytest.mark.parametrize("cancel", [True, False])
def test_cash_flow_checks_real_oracle_contract_and_preserves_cancelled_basket(usd_basket, cancel):
    from test_offer_usd_oracles import evidence

    from products.xgestion.offer_journeys.model import Step

    variant, before, after = evidence()
    usd_basket.before = before
    usd_basket.payment_id = 1
    usd_basket.fixtures["context"] = {"usuario_id": 5}
    usd_basket._oracle = Mock()
    usd_basket._oracle.return_value.snapshot.return_value = before if cancel else after
    usd_basket._open_payment = Mock()
    usd_basket._confirm_payment = Mock()
    usd_basket._collect(Step("cancel_payment" if cancel else "pay", expected=variant.steps[-1].expected))
    assert usd_basket._confirm_payment.call_count == (0 if cancel else 1)
    assert usd_basket._oracle.return_value.snapshot.call_count == 1
