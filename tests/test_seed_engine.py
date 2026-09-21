from datetime import datetime
from decimal import Decimal

from products.xgestion.seeds.engine import equivalent, upsert_sql
from products.xgestion.seeds.model import SeedTable


def test_upsert_keeps_dynamic_values_out_of_sql_and_never_replaces_identity():
    row = {"Empresa": 9, "artId": 980001, "artCodigo": "QA-SEED-'quoted", "price": "1000.00"}
    table = SeedTable("articulos", ("Empresa", "artId"), ("artCodigo",), [row])
    sql, params = upsert_sql(table, row)
    assert "ON DUPLICATE KEY UPDATE" in sql
    assert "REPLACE" not in sql
    assert row["artCodigo"] not in sql
    assert params == (9, 980001, "QA-SEED-'quoted", "1000.00")
    updates = sql.split("UPDATE", 1)[1]
    assert "`Empresa`=" not in updates and "`artId`=" not in updates


def test_comparison_accepts_mysql_exact_decimal_bit_and_datetime_representations():
    assert equivalent(Decimal("1000.000"), "1000.00", "decimal")
    assert equivalent(b"\x01", 1, "bit")
    assert equivalent(datetime(2026, 9, 21), "2026-09-21 00:00:00", "datetime")
    assert not equivalent(Decimal("1000.01"), "1000.00", "decimal")
    assert not equivalent(None, 0, "int")
    assert not equivalent("qa-seed-a", "QA-SEED-A", "varchar")


def test_review_export_supports_exact_decimal_values(monkeypatch):
    from products.xgestion.seeds import engine

    row = {"id": 1, "code": "QA-SEED-DECIMAL", "price": Decimal("0.10")}
    monkeypatch.setattr(engine, "catalog", lambda _: [SeedTable("items", ("id",), ("code",), [row])])
    exported = engine.render_seed()
    assert '"0.10"' in exported
    assert "VALUES (%s,%s,%s)" in exported
