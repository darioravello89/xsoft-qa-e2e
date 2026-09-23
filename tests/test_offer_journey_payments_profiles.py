"""Perfiles y cobros tienen recorridos completos, nunca medios externos."""
from decimal import Decimal

import pytest

from products.xgestion.offer_journeys.contracts import validate_journey
from products.xgestion.offer_journeys.payments import CASES
from products.xgestion.offer_journeys.profiled import CASES as PROFILES


def test_four_payment_scenarios_and_fixed_destinations():
    assert set(CASES) == {f"XG-PRM-{n:03}" for n in range(73, 77)}
    for journey in CASES.values():
        validate_journey(journey)
        for variant in journey.variants:
            assert "manual-payments" in variant.requirements
            assert all(step.value in {"cash", "card", "transfer"} for step in variant.steps
                       if step.action == "payment_method")


def test_all_selected_and_excluded_payment_types():
    for case_id, totals in (("XG-PRM-073", [1800, 1800, 1800]), ("XG-PRM-075", [1800, 1800, 2000])):
        assert [sum(line.total for line in v.steps[-1].expected) for v in CASES[case_id].variants] == totals


def test_switching_payment_and_cancelling_does_not_duplicate_discount():
    steps = CASES["XG-PRM-076"].variants[0].steps
    assert [sum(line.total for line in s.expected) for s in steps if s.action == "cancel_payment"] == [1800, 2000]
    assert sum(line.total for line in steps[-1].expected) == Decimal(1800)


def test_all_profile_phases_are_explicit_and_closed():
    for journey in PROFILES.values():
        validate_journey(journey)
    assert [v.name for v in PROFILES["XG-PRM-070"].variants] == ["active", "inactive", "active-again"]
    assert [v.name for v in PROFILES["XG-PRM-079"].variants] == [
        "general-off", "offers-off", "allowed-warning-on", "allowed-warning-off"]
    for v in PROFILES["XG-PRM-079"].variants:
        last = v.steps[-1]
        if v.name.startswith("allowed"):
            assert last.action == "pay" and sum(line.total for line in last.expected) == Decimal(1710)
        else:
            assert any(step.action == "manual_blocked" for step in v.steps)
            assert last.action == "abandon"


@pytest.mark.parametrize("case_id", ["XG-PRM-077", "XG-PRM-078"])
def test_multicontext_cases_are_not_falsely_automated(case_id):
    assert case_id not in CASES and case_id not in PROFILES

