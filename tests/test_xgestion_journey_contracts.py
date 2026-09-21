"""Los recorridos nuevos no se habilitan con una calibración anterior incompleta."""

import copy

import pytest

from framework.errors import QAError
from products.xgestion.contracts import JOURNEY_ELEMENTS, KEYBOARD_ELEMENTS, validate_journeys


def journey_assets():
    fixtures = {"sales_journeys": {
        "schema_version": 1, "currency": "ARS", "cash_dialog": True,
        "abandon_requires_supervisor": False, "unknown_notice": "status",
        "unknown_notice_text": "Codigo inexistente.", "repeated_product_rows": 1,
        "defaults": {"customer": "Consumidor final", "price_list": "General", "document": "Interno"},
    }}
    locators = {
        "calibration": {"verified_features": ["ventas-etapa1"]},
        "windows": {"main": "QA"},
        "elements": {alias: {"window": "main", "query": f"role:label and name:{alias}"}
                     for alias in JOURNEY_ELEMENTS},
    }
    locators["elements"]["sale.lines"].update({"column_count": 5,
        "columns": {"code": 0, "name": 1, "quantity": 2, "unit_price": 3, "total": 4}})
    return fixtures, locators


def test_accepts_only_explicit_profile_and_observed_table_columns():
    fixtures, locators = journey_assets()
    previous = copy.deepcopy((fixtures, locators))
    validate_journeys(fixtures, locators)
    assert (fixtures, locators) == previous


@pytest.mark.parametrize("change", [
    "missing_feature", "draft_alias", "missing_alias", "duplicate_column", "missing_column",
    "negative_column", "out_of_bounds", "bool_column", "currency", "cash_dialog",
    "supervisor", "missing_defaults", "draft_default", "notice", "missing_dismiss", "rows",
])
def test_incomplete_or_incompatible_profile_blocks(change):
    fixtures, locators = journey_assets()
    profile = fixtures["sales_journeys"]
    table = locators["elements"]["sale.lines"]
    if change == "missing_feature":
        locators["calibration"].pop("verified_features")
    elif change == "draft_alias":
        locators["elements"]["payment.change"]["query"] = "CALIBRAR vuelto"
    elif change == "missing_alias":
        locators["elements"].pop("payment.cancel")
    elif change == "duplicate_column":
        table["columns"]["code"] = table["columns"]["quantity"]
    elif change == "missing_column":
        table["columns"].pop("total")
    elif change == "negative_column":
        table["columns"]["code"] = -1
    elif change == "out_of_bounds":
        table["columns"]["code"] = 5
    elif change == "bool_column":
        table["columns"]["code"] = True
    elif change == "currency":
        profile["currency"] = "USD"
    elif change == "cash_dialog":
        profile["cash_dialog"] = False
    elif change == "supervisor":
        profile["abandon_requires_supervisor"] = True
    elif change == "missing_defaults":
        profile["defaults"].pop("document")
    elif change == "draft_default":
        profile["defaults"]["customer"] = "CALIBRAR cliente"
    elif change == "notice":
        profile["unknown_notice"] = "sound_only"
    elif change == "missing_dismiss":
        profile["unknown_notice"] = "dialog"
    elif change == "rows":
        profile["repeated_product_rows"] = 0
    with pytest.raises(QAError):
        validate_journeys(fixtures, locators)


def test_dialog_profile_requires_its_own_dismiss_alias():
    fixtures, locators = journey_assets()
    fixtures["sales_journeys"]["unknown_notice"] = "dialog"
    locators["elements"]["sale.unknown_dismiss"] = {"window": "main", "query": "role:push button and name:OK"}
    validate_journeys(fixtures, locators)


def test_keyboard_feature_requires_its_own_verified_aliases():
    fixtures, locators = journey_assets()
    locators["calibration"]["verified_features"].append("ventas-teclado-v1")
    for alias in KEYBOARD_ELEMENTS:
        locators["elements"][alias] = {"window": "main", "query": f"role:push button and name:{alias}"}
    validate_journeys(fixtures, locators)
    locators["elements"].pop("editor.cancel")
    with pytest.raises(QAError):
        validate_journeys(fixtures, locators)
