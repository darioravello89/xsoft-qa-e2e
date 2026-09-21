from datetime import date
from decimal import Decimal

import pytest

from framework.errors import QAError
from products.xgestion.seeds.model import SeedContext, SeedTable, merge_tables


def test_context_rejects_missing_or_nonpositive_ids():
    for value in (0, -1, True, "1"):
        with pytest.raises(QAError):
            SeedContext(value, 1, 1, 1, date(2026, 9, 21))


def test_tables_merge_rows_without_losing_identity_or_accepting_duplicate_ids():
    first = SeedTable("articulos", ("Empresa", "artId"), ("artCodigo",),
                      [{"Empresa": 1, "artId": 980001, "artCodigo": "QA-SEED-A"}])
    second = SeedTable("articulos", first.keys, first.identity,
                       [{"Empresa": 1, "artId": 980002, "artCodigo": "QA-SEED-B"}])
    merged = merge_tables([first, second])
    assert len(merged) == 1
    assert [row["artId"] for row in merged[0].rows] == [980001, 980002]
    with pytest.raises(QAError, match="duplicada"):
        merge_tables([first, first])


def test_table_rejects_injected_identifiers_before_any_sql():
    with pytest.raises(QAError):
        SeedTable("articulos; DROP DATABASE other", ("id",), ("code",), [{"id": 1, "code": "QA"}])


def test_merge_rejects_conflicting_ownership_contract():
    first = SeedTable("articulos", ("id",), ("code",), [{"id": 1, "code": "QA"}])
    second = SeedTable("articulos", ("id",), ("name",), [{"id": 2, "name": "QA"}])
    with pytest.raises(QAError):
        merge_tables([first, second])


@pytest.mark.parametrize("value", [Decimal("NaN"), Decimal("Infinity"), Decimal("-Infinity"), True])
def test_reject_nonfinite_and_boolean_values(value):
    with pytest.raises(QAError):
        SeedTable("items", ("id",), ("code",), [{"id": 1, "code": "QA", "price": value}])
