"""La UI debe probar cada componente de la canasta, aunque el total coincida."""

from copy import deepcopy
from decimal import Decimal
from unittest.mock import Mock

import pytest
from test_xgestion_promotions import promotion_assets

from framework.errors import QAError
from products.xgestion import library as base
from products.xgestion.offer_journeys.contracts import FEATURE, validate_calibration, validate_journey
from products.xgestion.offer_journeys.library import XGestionOfferJourneysLibrary
from products.xgestion.offer_journeys.model import Journey, Line, Offer, Product, Step, Variant


def journey():
    products = (Product("A", 981801, "QA-A"), Product("B", 981802, "QA-B"), Product("E", 981809, "QA-E"))
    offers = (Offer(981800, "QA-OFERTA", 2, 980001, "%", "10"),)
    lines = (Line("A", "2", "200", 981800), Line("B", "1", "100", 981800))
    steps = (Step("open"), Step("add", "A", "2", lines[:1]),
             Step("add", "B", "1", lines), Step("cancel_payment", expected=lines),
             Step("pay", expected=lines))
    return Journey("XG-PRM-018", (Variant("principal", products, offers, steps),))


def assets():
    fixtures, locators = promotion_assets()
    fixtures["offer_journeys"] = {"schema_version": 1, "item_removal_requires_supervisor": False,
                                  "choose_payment_on_close": True}
    locators["windows"]["payment_picker"] = "Medios QA"
    for alias in ("payment.method", "payment_picker.lines", "payment_picker.search"):
        locators["elements"][alias] = {"window": "payment_picker", "query": f"name:{alias}"}
    locators["elements"]["payment_picker.lines"].update(
        column_count=3, columns={"id": 0, "name": 1, "discount": 2})
    fixtures["sales_journeys"]["repeated_product_rows"] = 1
    locators["calibration"]["verified_features"].append(FEATURE)
    return fixtures, locators


def test_journey_and_calibration_are_complete_and_do_not_mutate_inputs():
    example = journey()
    fixtures, locators = assets()
    previous = deepcopy((fixtures, locators))
    validate_journey(example)
    validate_calibration(fixtures, locators, example.variants[0])
    assert previous == (fixtures, locators)


@pytest.mark.parametrize("change", ["feature", "profile", "supervisor", "repeated"])
def test_missing_new_calibration_is_blocked(change):
    fixtures, locators = assets()
    if change == "feature":
        locators["calibration"]["verified_features"].remove(FEATURE)
    elif change == "profile":
        del fixtures["offer_journeys"]
    elif change == "supervisor":
        fixtures["offer_journeys"]["item_removal_requires_supervisor"] = True
    else:
        fixtures["sales_journeys"]["repeated_product_rows"] = 2
    with pytest.raises(QAError):
        validate_calibration(fixtures, locators, journey().variants[0])


@pytest.mark.parametrize("change", ["missing_picker", "no_close_choice", "missing_id", "wrong_columns"])
def test_cash_journey_requires_verified_native_payment_picker(change):
    fixtures, locators = assets()
    if change == "missing_picker":
        del locators["elements"]["payment_picker.search"]
    elif change == "no_close_choice":
        fixtures["offer_journeys"]["choose_payment_on_close"] = False
    elif change == "missing_id":
        del locators["elements"]["payment_picker.lines"]["columns"]["id"]
    else:
        locators["elements"]["payment_picker.lines"]["column_count"] = 2
    with pytest.raises(QAError):
        validate_calibration(fixtures, locators, journey().variants[0])


@pytest.mark.parametrize("steps", [
    (Step("open"), Step("sql", value="UPDATE")),
    (Step("open"), Step("add", "MISSING", "1", (Line("A", "1"),)), Step("abandon")),
    (Step("open"), Step("add", "A", "NaN", (Line("A", "1"),)), Step("abandon")),
    (Step("open"), Step("add", "A", "1", (Line("A", "1", "2000"),)), Step("abandon")),
    (Step("open"), Step("add", "A", "1", (Line("A", "1", "10", 13),)), Step("abandon")),
    (Step("open"), Step("add", "A", "1", (Line("A", "1"),))),
])
def test_incomplete_or_incoherent_journey_cannot_be_executed(steps):
    original = journey().variants[0]
    candidate = Journey("XG-PRM-018", (Variant("principal", original.products, original.offers, steps),))
    with pytest.raises(QAError):
        validate_journey(candidate)


@pytest.fixture
def basket(monkeypatch):
    monkeypatch.setattr(base, "UI_TIMEOUT", 0)
    library = XGestionOfferJourneysLibrary()
    library.variant = journey().variants[0]
    library.expected = library.variant.steps[-1].expected
    library.fixtures, locators = assets()
    library.journeys = library.keyboard_sales = True
    library.driver = Mock()
    library.driver.locators = locators
    library.driver.table_rows.return_value = [
        ["QA-B", "QA-B", "1.0", "1.000,00", "900,00", "1.000,00", "100,00"],
        ["QA-A", "QA-A", "2.0", "1.000,00", "1.800,00", "2.000,00", "200,00"],
    ]
    library.driver.text.return_value = "2.700,00"
    return library


def test_basket_matches_products_independently_of_visual_order(basket):
    basket._assert_basket(basket.expected)


@pytest.mark.parametrize("change", ["wrong_discount", "swapped_codes", "duplicate", "extra", "non_numeric"])
def test_correct_total_does_not_hide_incorrect_lines(basket, change):
    rows = basket.driver.table_rows.return_value
    if change == "wrong_discount":
        rows[0][6], rows[1][6] = "200,00", "100,00"
    elif change == "swapped_codes":
        rows[0][0], rows[1][0] = rows[1][0], rows[0][0]
    elif change == "duplicate":
        rows[0][0] = rows[1][0]
    elif change == "extra":
        rows.append(rows[0][:])
    else:
        rows[0][6] = "PRIVATE-VALUE"
    with pytest.raises(AssertionError) as error:
        basket._assert_basket(basket.expected)
    assert "PRIVATE-VALUE" not in str(error.value)


def test_visible_discount_includes_manual_but_expected_components_remain_separate(basket):
    basket.driver.table_rows.return_value = [
        ["QA-A", "QA-A", "1.0", "1.000,00", "810,00", "1.000,00", "190,00"],
    ]
    basket.driver.text.return_value = "810,00"
    expected = (Line("A", "1", "90", 981800, manual="100"),)
    basket._assert_basket(expected)
    assert Decimal(expected[0].discount) == 90


def test_unknown_case_or_missing_seed_never_launches_process(monkeypatch):
    library = XGestionOfferJourneysLibrary()
    library.start = Mock()
    monkeypatch.delenv("XSOFT_QA_SEED", raising=False)
    with pytest.raises(QAError):
        library.run_journey("UNKNOWN")
    library.start.assert_not_called()

