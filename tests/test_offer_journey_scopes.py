"""Cobertura de alcances y fronteras de cantidad, independiente del ERP."""

from decimal import Decimal

from products.xgestion.offer_journeys.contracts import validate_journey
from products.xgestion.offer_journeys.scopes import CASES


def test_all_scope_cases_are_complete_and_keep_excluded_product_without_discount():
    assert set(CASES) == {f"XG-PRM-{number:03}" for number in range(8, 39)}
    for journey in CASES.values():
        validate_journey(journey)
        variant = journey.variants[0]
        assert all(not offer.grouped for offer in variant.offers)
        final = variant.steps[-1].expected
        excluded = next(line for line in final if line.product == "E")
        assert excluded.quantity == "1" and excluded.discount == "0" and excluded.offer_id == 0
        assert variant.steps[-2].action == "cancel_payment"
        assert variant.steps[-1].action == "pay"
        assert variant.steps[-2].expected == final


def test_scope_final_totals_cover_seven_distinct_formulas():
    expected = [3700, 3550, 3000, 3500, 3800, 3700, 3600]
    for first in (11, 18, 25, 32):
        observed = []
        for number in range(first, first + 7):
            final = CASES[f"XG-PRM-{number:03}"].variants[0].steps[-1].expected
            observed.append(sum((line.total for line in final), Decimal(0)))
        assert observed == list(map(Decimal, expected))
    assert [sum((line.total for line in CASES[f"XG-PRM-{number:03}"].variants[0].steps[-1].expected),
                Decimal(0)) for number in (8, 9, 10)] == list(map(Decimal, (2800, 2700, 2600)))


def test_minimum_is_per_product_with_grouping_disabled():
    for number in (15, 16, 17, 22, 23, 24, 29, 30, 31, 36, 37, 38):
        variant = CASES[f"XG-PRM-{number:03}"].variants[0]
        added_b = next(step for step in variant.steps if step.action == "add" and step.product == "B")
        assert all(line.discount == "0" for line in added_b.expected)

