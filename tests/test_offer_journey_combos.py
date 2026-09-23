"""Canastas literales de combos: sobrantes, competencia y centavos exactos."""

from decimal import Decimal

from products.xgestion.offer_journeys.combos import CASES
from products.xgestion.offer_journeys.contracts import validate_journey


def _total(step):
    return sum((line.total for line in step.expected), Decimal(0))


def test_combo_catalog_has_five_complete_journeys_and_separate_variant_products():
    assert set(CASES) == {f"XG-PRM-{number:03}" for number in range(60, 65)}
    ids = []
    codes = []
    for journey in CASES.values():
        validate_journey(journey)
        for variant in journey.variants:
            ids.extend(product.id for product in variant.products)
            codes.extend(product.code for product in variant.products)
            products = {product.id for product in variant.products}
            for offer in variant.offers:
                if offer.formula == "COMBO":
                    assert offer.scope == 6 and offer.target == 0
                    assert len(offer.components) >= 2
                    assert all(product in products for product, quantity in offer.components)
    assert len(ids) == len(set(ids))
    assert len(codes) == len(set(codes))


def test_final_cash_totals_and_canceled_payment_baskets_are_exact():
    expected_totals = [1500, 3900, 170, 20, 100]
    for number, expected in zip(range(60, 65), expected_totals, strict=True):
        steps = CASES[f"XG-PRM-{number:03}"].variants[0].steps
        assert steps[-2].action == "cancel_payment"
        assert steps[-1].action == "pay"
        assert steps[-2].expected == steps[-1].expected
        assert _total(steps[-1]) == expected


def test_incomplete_and_non_beneficial_combos_keep_only_individual_offer():
    variants = CASES["XG-PRM-060"].variants
    first_a = variants[0].steps[1]
    assert _total(first_a) == 900
    for variant in variants[1:]:
        pair = next(step for step in variant.steps if step.action == "add" and step.product == "B")
        automatic = [Decimal(line.discount) for line in pair.expected]
        assert automatic == [100, 0]
        assert _total(pair) == 1900
        individual = next(offer for offer in variant.offers if offer.formula == "%")
        assert pair.expected[0].offer_id == individual.id
        assert pair.expected[1].offer_id == 0
        assert variant.steps[-1].action == "abandon"


def test_repeated_combo_adds_individual_discount_only_to_remainder():
    variant = CASES["XG-PRM-061"].variants[0]
    states = [step for step in variant.steps if step.action == "edit"]
    assert [_total(step) for step in states] == [3000, 3900, 3300, 3900]
    assert [[Decimal(line.discount) for line in step.expected] for step in states] == [
        [500, 500], [600, 500], [450, 250], [600, 500],
    ]
    combo = next(offer for offer in variant.offers if offer.formula == "COMBO")
    assert all(line.offer_id == combo.id for step in states for line in step.expected)


def test_competing_combo_releases_previous_offer_and_tie_is_independent_of_loading_order():
    competing, tie = CASES["XG-PRM-062"].variants
    winning = next(step for step in competing.steps if step.action == "add" and step.product == "C")
    assert _total(winning) == 170
    assert [Decimal(line.discount) for line in winning.expected] == [25, 0, 15]
    assert winning.expected[1].offer_id == 0
    pair_states = [step for step in tie.steps if step.action == "add" and len(step.expected) == 2]
    assert [[line.product for line in step.expected] for step in pair_states] == [["A", "B"], ["B", "A"]]
    lower_id = min(offer.id for offer in tie.offers)
    for step in pair_states:
        assert _total(step) == 130
        assert all(line.offer_id == lower_id for line in step.expected)
        assert {line.product: Decimal(line.discount) for line in step.expected} == {
            "A": Decimal("13.33"), "B": Decimal("6.67"),
        }
    # Los importes iguales no distinguen el ganador; cada orden debe persistir el ID menor.
    paid = [step for step in tie.steps if step.action == "pay"]
    assert len(paid) == 2
    assert [step.expected for step in paid] == [step.expected for step in pair_states]
    assert all(line.offer_id == lower_id for step in paid for line in step.expected)


def test_rounding_residue_and_manual_discount_use_net_base_without_double_subtraction():
    base, manual = CASES["XG-PRM-063"].variants
    final = base.steps[-1]
    assert [Decimal(line.discount) for line in final.expected] == list(map(Decimal, ["3.33", "3.33", "3.34"]))
    assert manual.requirements == ("manual-discount",)
    apply, remove = [step for step in manual.steps if step.action == "manual"]
    assert [Decimal(line.discount) for line in apply.expected] == list(map(Decimal, ["2.79", "3.10", "3.11"]))
    assert [Decimal(line.manual) for line in apply.expected] == [1, 0, 0]
    assert [line.total for line in apply.expected] == list(map(Decimal, ["6.21", "6.90", "6.89"]))
    assert _total(apply) == _total(remove) == 20
    assert all(Decimal(line.manual) == 0 for line in remove.expected)


def test_fractional_combo_includes_intermediate_edit_and_exact_second_combo_boundary():
    variant = CASES["XG-PRM-064"].variants[0]
    assert {p.ref: p.unit for p in variant.products} == {"A": 2, "B": 2, "E": 1}
    edits = [step for step in variant.steps if step.action == "edit"]
    assert [_total(step) for step in edits] == list(map(Decimal, ["40", "70", "100", "94.80", "90", "100"]))
    assert [[Decimal(line.discount) for line in step.expected] for step in edits] == [
        list(map(Decimal, amounts)) for amounts in (
            ("2.22", "2.78"), ("2.22", "2.78"), ("4.44", "5.56"),
            ("2.22", "2.78"), ("4.44", "5.56"), ("4.44", "5.56"),
        )
    ]
    assert [(line.product, Decimal(line.quantity)) for line in variant.steps[-1].expected] == [
        ("A", Decimal("1.250")), ("B", Decimal("3.000")),
    ]
