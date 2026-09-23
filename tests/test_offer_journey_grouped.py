"""Fronteras de agrupación y reparto de centavos en canastas."""
from decimal import Decimal

from products.xgestion.offer_journeys.contracts import validate_journey
from products.xgestion.offer_journeys.grouped import CASES


def test_all_grouped_journeys_have_on_off_and_complete_transitions():
    assert set(CASES) == {f"XG-PRM-{n:03}" for n in range(39, 60)}
    for journey in CASES.values():
        validate_journey(journey)
        assert [v.name for v in journey.variants[:2]] == ["agrupacion-on", "agrupacion-off"]
        assert journey.variants[0].offers[0].grouped
        assert not journey.variants[1].offers[0].grouped
        assert journey.variants[0].steps[-1].action == "pay"
        assert all(v.steps[-1].action == "abandon" for v in journey.variants[1:])


def test_grouped_expected_cash_totals_are_independent_constants():
    for first in (39, 46, 53):
        totals = [sum((line.total for line in CASES[f"XG-PRM-{n:03}"].variants[0].steps[-1].expected),
                      Decimal(0)) for n in range(first, first + 7)]
        assert totals == [1800, 1700, 2000, 1500, 1800, 1700, 1600]


def test_three_for_two_preserves_last_cent_and_net_base_for_different_prices():
    for n in (41, 48, 55):
        variants = CASES[f"XG-PRM-{n:03}"].variants
        final = variants[0].steps[-1].expected
        assert [Decimal(line.discount) for line in final] == list(map(Decimal, ["333.33", "333.33", "333.34"]))
        different = next(s.expected for s in variants[2].steps if s.action == "add" and s.product == "C")
        assert [Decimal(line.discount) for line in different] == list(map(Decimal, ["333.33", "666.67", "1000"]))
        assert sum(line.total for line in different) == 4000


def test_three_for_two_exclusion_keeps_the_actual_loading_order_before_removal():
    for number in (41, 48, 55):
        variant = CASES[f"XG-PRM-{number:03}"].variants[0]
        third_add = next(step for step in variant.steps
                         if step.action == "add" and step.product == "B")
        assert [line.product for line in third_add.expected] == ["A", "E", "B"]
        assert all(line.offer_id == 0 and line.discount == "0" for line in third_add.expected)


def test_grouped_second_unit_discount_is_distributed_over_full_mixed_basket():
    for number in (42, 49, 56):
        on, off = CASES[f"XG-PRM-{number:03}"].variants
        on_edit = next(step for step in on.steps if step.action == "edit" and step.value == "2")
        off_edit = next(step for step in off.steps if step.action == "edit")
        assert [Decimal(line.discount) for line in on_edit.expected] == list(map(Decimal, ["333.33", "166.67"]))
        assert [Decimal(line.discount) for line in off_edit.expected] == [500, 0]
        assert sum(line.total for line in on_edit.expected) == sum(line.total for line in off_edit.expected) == 2500


def test_grouped_fixtures_distinguish_the_declared_scope_from_every_other_classification():
    fields = {2: "family", 3: "subfamily", 5: "brand"}
    for journey in CASES.values():
        for variant in journey.variants:
            included = {product.ref for product in variant.products if product.ref != "E"}
            product_a = next(product for product in variant.products if product.ref == "A")
            target_field = fields[variant.offers[0].scope]
            for field in ("family", "subfamily", "sector", "brand"):
                same_classification = {product.ref for product in variant.products
                                       if getattr(product, field) == getattr(product_a, field)}
                if field == target_field:
                    assert same_classification == included, (journey.id, variant.name, field)
                else:
                    assert same_classification != included, (journey.id, variant.name, field)


def test_grouped_families_are_isolated_between_variants_and_keep_valid_subfamily_parents():
    from products.xgestion.offer_journeys.catalog import get_journeys

    occupied = {product.family for journey in get_journeys() if journey.id not in CASES
                for variant in journey.variants for product in variant.products}
    parents = {}
    for journey in CASES.values():
        for variant in journey.variants:
            families = {product.family for product in variant.products}
            assert not occupied & families, (journey.id, variant.name)
            occupied.update(families)
            for product in variant.products:
                assert parents.setdefault(product.subfamily, product.family) == product.family

