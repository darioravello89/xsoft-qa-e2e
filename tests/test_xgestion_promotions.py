"""Pruebas sintéticas de promociones; no acreditan ejecución del JAR."""

import copy
from decimal import Decimal
from unittest.mock import Mock

import pytest
from test_xgestion_journey_contracts import journey_assets

from framework.errors import QAError
from products.xgestion import library as base
from products.xgestion.contracts import KEYBOARD_ELEMENTS
from products.xgestion.oracles import Snapshot
from products.xgestion.promotions import CASES, validate_promotions
from products.xgestion.promotions_library import XGestionPromotionsLibrary


def promotion_assets():
    fixtures, locators = journey_assets()
    fixtures["promotions"] = {
        "schema_version": 1, "currency": "ARS", "price_list_id": 0,
        "price_list_text": "Ninguna Lista", "other_discounts": False, "loyalty": False,
        "customer_and_shift_lists": False,
    }
    fixtures["sales_journeys"]["defaults"]["price_list"] = "Ninguna Lista"
    fixtures["product"] = {"id": 90001, "code": "QA", "name": "Producto QA", "quantity": 2,
                           "unit_price": "1000"}
    locators["calibration"]["verified_features"] += ["ventas-teclado-v1", "promociones-v1"]
    for alias in KEYBOARD_ELEMENTS:
        locators["elements"][alias] = {"window": "main", "query": f"name:{alias}"}
    locators["elements"]["sale.lines"]["column_count"] = 7
    locators["elements"]["sale.lines"]["columns"].update(gross_total=5, offer_discount=6)
    return fixtures, locators


def test_profile_requires_explicit_commercial_conditions_and_separate_columns():
    fixtures, locators = promotion_assets()
    before = copy.deepcopy((fixtures, locators))
    validate_promotions(fixtures, locators)
    assert before == (fixtures, locators)


@pytest.mark.parametrize("change", ["feature", "keyboard", "duplicate", "missing", "boolean", "bounds",
                                  "usd", "list", "discount", "loyalty", "customer", "draft", "default"])
def test_incompatible_promotion_profile_is_blocked(change):
    fixtures, locators = promotion_assets()
    profile = fixtures["promotions"]
    columns = locators["elements"]["sale.lines"]["columns"]
    if change in ("feature", "keyboard"):
        locators["calibration"]["verified_features"].remove(
            "promociones-v1" if change == "feature" else "ventas-teclado-v1")
    elif change == "duplicate":
        columns["offer_discount"] = columns["total"]
    elif change == "missing":
        del columns["gross_total"]
    elif change == "boolean":
        columns["gross_total"] = True
    elif change == "bounds":
        columns["gross_total"] = 7
    elif change == "usd":
        profile["currency"] = "USD"
    elif change == "list":
        profile["price_list_id"] = 980101
    elif change == "discount":
        profile["other_discounts"] = True
    elif change == "loyalty":
        profile["loyalty"] = True
    elif change == "customer":
        profile["customer_and_shift_lists"] = True
    elif change == "draft":
        profile["price_list_text"] = "CALIBRAR lista"
    else:
        fixtures["sales_journeys"]["defaults"]["price_list"] = "Lista distinta"
    with pytest.raises(QAError):
        validate_promotions(fixtures, locators)


def test_examples_are_the_seven_fixed_seed_expectations():
    from products.xgestion.seeds.pricing import PRICING_CASES

    examples = {item["id"]: item for item in PRICING_CASES}
    assert len(CASES) == 7
    assert [case.total for case in CASES.values()] == list(map(Decimal, ("2700", "2550", "2000", "2500",
                                                                      "1000", "1000", "1000")))
    for case in CASES.values():
        assert examples[case.seed_id]["quantities"] == {case.code: str(case.quantity)}
        assert Decimal(examples[case.seed_id]["expected_total"]) == case.total


@pytest.fixture
def promotion(monkeypatch):
    monkeypatch.setattr(base, "UI_TIMEOUT", 0)
    library = XGestionPromotionsLibrary()
    library.case = CASES["PCT-Q3"]
    fixtures, locators = promotion_assets()
    library.fixtures = fixtures
    library.fixtures["product"] = library.case.product()
    library.journeys = library.keyboard_sales = True
    library.driver = Mock()
    library.driver.locators = locators
    library.driver.table_rows.return_value = [["QA-SEED-PCT", "QA-SEED-PCT", "3.0", "1.000,00",
                                              "2.700,00", "3.000,00", "300,00"]]
    texts = {"sale.total": "2.700,00", "payment.total": "2700.00", "payment.amount": "2700.00",
             "payment.change": "0.00"}
    library.driver.text.side_effect = lambda alias: texts[alias]
    library.before = Snapshot(frozenset({1}), Decimal(100), Decimal(0))
    oracle = Mock()
    oracle.snapshot.return_value = library.before
    oracle.verify_sale.return_value = 2
    library._oracle = Mock(return_value=oracle)
    library.verify_context = Mock()
    return library, texts, oracle


def test_ui_checks_gross_discount_and_net_separately(promotion):
    library, _, _ = promotion
    library._assert_sale_content(3)


@pytest.mark.parametrize("field,value", [(0, "WRONG"), (2, "2.0"), (3, "900,00"), (4, "3.000,00"),
                                        (5, "2.700,00"), (6, "0,00"), (6, "SECRET-NOT-A-NUMBER")])
def test_wrong_component_is_not_masked_by_correct_final_total(promotion, field, value):
    library, _, _ = promotion
    library.driver.table_rows.return_value[0][field] = value
    with pytest.raises(AssertionError) as error:
        library._assert_sale_content(3)
    assert "SECRET-NOT-A-NUMBER" not in str(error.value)


def test_cancelled_payment_keeps_sale_and_stock_and_cash(promotion):
    library, _, oracle = promotion
    library.cancel_promotion_payment()
    oracle.snapshot.assert_called_once()
    library.driver.click.assert_any_call("payment.cancel")
    assert library.driver.click.call_args_list[-1].args != ("payment.confirm",)


def test_cancelled_payment_rejects_business_mutation(promotion):
    library, _, oracle = promotion
    oracle.snapshot.return_value = Snapshot(frozenset({1, 2}), Decimal(97), Decimal(2700))
    with pytest.raises(AssertionError):
        library.cancel_promotion_payment()


def test_cash_uses_promotion_total_and_passes_expected_discount_to_oracle(promotion):
    library, _, oracle = promotion
    library.collect_promotion()
    library.verify_sale()
    library.driver.type.assert_any_call("payment.amount", "2700")
    assert library.driver.click.call_args_list[-1].args == ("payment.confirm",)
    assert oracle.verify_sale.call_args.kwargs["promotion"] == {
        "total": Decimal(2700), "offer_discount": Decimal(300), "offer_id": 980101}


def test_invalid_case_or_missing_seed_never_launches_jar(monkeypatch):
    library = XGestionPromotionsLibrary()
    start = Mock()
    monkeypatch.setattr(base.JarProcess, "start", start)
    monkeypatch.delenv("XSOFT_QA_SEED", raising=False)
    for seed_id in ("UNKNOWN", "PCT-Q3"):
        with pytest.raises(QAError):
            library.start_promotions(seed_id)
    start.assert_not_called()


def test_edit_recalculates_existing_row_with_keyboard(promotion):
    library, texts, _ = promotion
    final = library.driver.table_rows.return_value
    initial = [["QA-SEED-PCT", "QA-SEED-PCT", "1.0", "1.000,00", "900,00", "1.000,00", "100,00"]]
    library.driver.table_rows.side_effect = [initial, final]
    library.driver.text.side_effect = ["900,00", texts["sale.total"]]
    library.edit_promotion_quantity()
    library.driver.shortcut.assert_called_once_with("sale.lines", "ctrl+e")
    library.driver.type.assert_called_once_with("editor.quantity", "3")
    library.driver.edit_sale_row.assert_not_called()
    library.driver.expect_sale_row_selected.assert_called_once_with("sale.lines", 0, "QA-SEED-PCT")


@pytest.mark.parametrize("seed_id", ["EXPIRADA", "FUTURA", "INACTIVA"])
def test_negative_first_requires_positive_control_and_abandonment(promotion, monkeypatch, seed_id):
    library, _, oracle = promotion
    library.case = CASES[seed_id]
    library.fixtures["product"] = library.case.product()
    monkeypatch.setenv("XSOFT_QA_SEED_DATE", "2026-09-22")
    oracle.query.return_value = [{"today": "2026-09-22"}]
    visits = []
    library._prepare_promotion_sale = lambda: visits.append(library.case.seed_id)
    library.cancel_sale = lambda: visits.append("abandonar")
    library.verify_cancel = lambda: visits.append("sin cambios")
    library.prepare_promotion()
    assert visits == ["PCT-Q3", "abandonar", "sin cambios", seed_id]
    assert library.fixtures["product"]["id"] == library.case.product_id


def test_broken_positive_control_does_not_allow_negative_to_pass(promotion, monkeypatch):
    library, _, oracle = promotion
    library.case = CASES["FUTURA"]
    monkeypatch.setenv("XSOFT_QA_SEED_DATE", "2026-09-22")
    oracle.query.return_value = [{"today": "2026-09-22"}]
    library._prepare_promotion_sale = Mock(side_effect=AssertionError("La oferta vigente no se aplicó"))
    with pytest.raises(AssertionError, match="vigente"):
        library.prepare_promotion()
    assert library.case.seed_id == "FUTURA"
    library._prepare_promotion_sale.assert_called_once()


def test_changed_mysql_day_blocks_before_loading_any_product(promotion, monkeypatch):
    library, _, oracle = promotion
    monkeypatch.setenv("XSOFT_QA_SEED_DATE", "2026-09-22")
    oracle.query.return_value = [{"today": "2026-09-23"}]
    with pytest.raises(QAError, match="fecha"):
        library.prepare_promotion()
    library.driver.type.assert_not_called()
