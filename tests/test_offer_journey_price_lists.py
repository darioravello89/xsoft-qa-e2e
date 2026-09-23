"""Selección de listas sobre precio efectivo, sin duplicar el motor del ERP."""

from decimal import Decimal

from products.xgestion.offer_journeys.model import Line
from products.xgestion.offer_journeys.price_lists import CASES


def test_selected_price_is_the_base_of_the_offer():
    variant = CASES["XG-PRM-071"].variants[0]
    loaded = [step.expected[0] for step in variant.steps if step.action == "add"]
    assert [(line.price, line.discount, line.total) for line in loaded] == [
        ("1000.00", "100", Decimal(900)), ("750", "75", Decimal(675)), ("1200", "240", Decimal(2160))]
    assert loaded[1].price_list_id == variant.price_lists[0].id
    assert loaded[2].price_list_id == variant.price_lists[1].id


def test_missing_list_item_restores_base_price_and_next_sale_starts_without_list():
    variant = CASES["XG-PRM-072"].variants[0]
    switches = [step for step in variant.steps if step.action == "price_list"]
    assert [sum((line.total for line in step.expected), Decimal(0)) for step in switches] == [
        Decimal(1350), Decimal(1800), Decimal(1350)]
    assert variant.price_lists[1].prices == ()
    assert variant.steps[-2].expected == (Line("A", "1", "100", 988200),)
    assert variant.steps[-1].action == "abandon"



def test_price_list_journeys_pass_the_same_completeness_contract():
    from products.xgestion.offer_journeys.contracts import validate_journey

    for journey in CASES.values():
        validate_journey(journey)


def test_enter_is_limited_to_the_verified_picker_search_controls():
    from unittest.mock import Mock

    import pytest

    from framework.errors import QAError
    from products.xgestion.driver import SemanticDriver

    driver = SemanticDriver(Mock(), 123, {})
    driver._focus_element = Mock()
    driver.keys("list_picker.search", "enter")
    driver.bridge.press_keys.assert_called_once_with("enter")
    with pytest.raises(QAError):
        driver.keys("sale.code", "enter")


def test_picker_confirms_current_selection_without_retyping_search():
    from unittest.mock import Mock

    from products.xgestion.offer_journeys.library import XGestionOfferJourneysLibrary

    library = XGestionOfferJourneysLibrary()
    library.variant = CASES["XG-PRM-071"].variants[0]
    library.driver = Mock()
    library.driver.locators = {"elements": {"list_picker.lines": {"columns": {"name": 1}}}}
    library._choose_price_list("QA-A")
    name = library.variant.price_lists[0].name
    library.driver.select_sale_row.assert_called_once_with("list_picker.lines", 1, name)
    library.driver.keys.assert_called_once_with("list_picker.search", "enter")
    library.driver.type.assert_not_called()
    library.driver.expect.assert_called_once_with("sale.price_list", name)

