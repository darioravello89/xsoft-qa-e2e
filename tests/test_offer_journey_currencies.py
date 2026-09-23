"""Regresión USD: expectativas externas al ERP y datos originales sin conversión previa."""

from dataclasses import replace
from datetime import date
from decimal import Decimal

import pytest

from framework.errors import QAError
from products.xgestion.offer_journeys.catalog import get_journey
from products.xgestion.offer_journeys.contracts import validate_journey
from products.xgestion.seeds.journeys import build_journey_tables
from products.xgestion.seeds.model import SeedContext

IDS = tuple(f"XG-PRM-{number:03}" for number in range(80, 85))


def test_five_scopes_have_thirteen_required_variants_with_cash_retry():
    cases = [get_journey(identifier) for identifier in IDS]
    assert [len(case.variants) for case in cases] == [2, 3, 3, 3, 2]
    assert [case.variants[0].offers[0].scope for case in cases] == [4, 2, 3, 5, 1]
    for case in cases:
        validate_journey(case)
        for variant in case.variants:
            assert variant.exchange_rate == "1500.00"
            assert all(p.currency == "USD" and p.price == "100.00" for p in variant.products)
            assert [s.action for s in variant.steps][-2:] == ["cancel_payment", "pay"]
            assert any(s.action == "remove" and s.product == "E" for s in variant.steps)
            assert variant.offers[0].pay == "50.00"


def test_reported_single_product_defect_has_literal_usd_and_ars_expectations():
    variant = get_journey(IDS[0]).variants[0]
    changes = [s for s in variant.steps if s.product == "A" and s.action in {"add", "edit"}]
    assert [s.value for s in changes[:3]] == ["1", "2", "1"]
    for step, gross, discount, net, original in zip(
            changes[:3], (150000, 300000, 150000), (75000, 150000, 75000),
            (75000, 150000, 75000), (50, 100, 50), strict=True):
        line = next(line for line in step.expected if line.product == "A")
        assert (line.gross, Decimal(line.discount), line.total) == (gross, discount, net)
        assert line.original_price == "100.00" and Decimal(line.original_discount) == original


@pytest.mark.parametrize("identifier", IDS[1:4])
def test_two_different_products_reach_minimum_only_when_grouped(identifier):
    case = get_journey(identifier)
    for variant, expected in ((case.variants[1], (0, 0)), (case.variants[2], (75000, 75000))):
        pair = next(s for s in variant.steps if s.action == "add" and s.product == "B")
        assert [(line.product, line.quantity) for line in pair.expected] == [("A", "1"), ("B", "1")]
        assert tuple(Decimal(line.discount) for line in pair.expected) == expected
        after_remove = next(s for s in variant.steps if s.action == "remove" and s.product == "B")
        assert after_remove.expected[0].quantity == "1"
        assert Decimal(after_remove.expected[0].discount) == 0


def test_usd_seed_preserves_original_hundred_and_fixed_fifty_in_every_scope():
    ctx = SeedContext(90001, 1, 1, 90001, date(2026, 9, 23))
    tables = {t.name: t.rows for t in build_journey_tables(ctx, [get_journey(i) for i in IDS])}
    assert len(tables["ofertas"]) == 13
    assert all(r["ID_Moneda"] == 2 and Decimal(r["artPrecioVenta"]) == 100 for r in tables["articulos"])
    assert all(Decimal(r["Paga"]) == 50 and r["TipoDescuento"] == "LXO+$CU" for r in tables["ofertas"])
    assert "t_sis_moneda" not in tables


@pytest.mark.parametrize("change", ["currency", "rate", "original", "inconsistent"])
def test_incomplete_currency_contract_is_rejected(change):
    case = get_journey(IDS[0])
    variant = case.variants[0]
    if change == "currency":
        variant = replace(variant, products=(replace(variant.products[0], currency="EUR"), *variant.products[1:]))
    elif change == "rate":
        variant = replace(variant, exchange_rate=None)
    else:
        step = variant.steps[1]
        line = replace(step.expected[0], original_discount=None if change == "original" else "99.97")
        variant = replace(variant, steps=(variant.steps[0], replace(step, expected=(line,)), *variant.steps[2:]))
    with pytest.raises(QAError):
        validate_journey(replace(case, variants=(variant,)))
