"""Importes de frontera acordados para cantidades, prioridades y vigencias."""

from decimal import Decimal

from products.xgestion.offer_journeys.conditions import CASES
from products.xgestion.offer_journeys.contracts import validate_journey


def totals(variant):
    return [sum((line.total for line in step.expected), Decimal(0)) for step in variant.steps
            if step.action in {"add", "edit"}]


def test_fractional_minimum_boundaries_have_exact_expected_amounts():
    for variant in CASES["XG-PRM-065"].variants:
        assert totals(variant) == list(map(Decimal, ["400", "0.80", "1200", "400"]))
        assert all(product.unit == 2 for product in variant.products)
    for variant in CASES["XG-PRM-066"].variants:
        assert totals(variant) == list(map(Decimal, ["500", "999", "800", "1200", "500"]))
        assert variant.steps[-1].expected[0].offer_id == 0
    assert len(CASES["XG-PRM-065"].variants) == len(CASES["XG-PRM-066"].variants) == 3


def test_scope_priority_does_not_choose_the_largest_discount():
    for variant in CASES["XG-PRM-067"].variants:
        assert totals(variant) == list(map(Decimal, [950, 1850, 2700, 3500, 4250, 5200, 4250]))
        assert [line.discount for line in variant.steps[-1].expected] == ["50", "100", "150", "200", "250"]


def test_priority_and_inclusive_dates_use_fixed_boundaries():
    assert totals(CASES["XG-PRM-068"].variants[0]) == list(map(Decimal, [1000, 1800, 2400, 3200, 1800, 1000, 2400]))
    dates = CASES["XG-PRM-069"].variants[0]
    assert totals(dates) == list(map(Decimal, [900, 1800, 2700, 3700, 4700, 5600, 4700]))
    assert [(offer.start_days, offer.end_days) for offer in dates.offers] == [
        (-1, 1), (0, 1), (-1, 0), (1, 2), (-2, -1)]


def test_every_condition_journey_is_complete():
    for journey in CASES.values():
        validate_journey(journey)

