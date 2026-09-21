"""Contract tests against an owned disposable MySQL 5.7; never an installed service."""

import os
from pathlib import Path

import pytest
from seed_mysql_runtime import EphemeralMySQL

from framework.errors import QAError
from products.xgestion.seeds.engine import apply_tables, query
from products.xgestion.seeds.model import SeedTable

pytestmark = pytest.mark.skipif(not os.environ.get("XSOFT_SEED_MYSQL_BIN"),
                                reason="Integración MySQL opt-in: configurar XSOFT_SEED_MYSQL_BIN.")


@pytest.fixture(scope="module")
def server():
    with EphemeralMySQL(Path(__file__).resolve().parents[1]) as running:
        yield running


@pytest.fixture
def connection(server):
    with server.connection(dict_cursor=True) as conn:
        query(conn, "DROP TABLE IF EXISTS articulos")
        query(conn, "CREATE TABLE articulos (Empresa INT NOT NULL, artId INT NOT NULL, "
                    "artCodigo VARCHAR(255) NOT NULL, artNombre VARCHAR(100) NOT NULL, price DECIMAL(8,2), "
                    "PRIMARY KEY(Empresa,artId), UNIQUE(artNombre)) ENGINE=InnoDB")
        conn.commit()
        yield conn


def catalog(*rows):
    return [SeedTable("articulos", ("Empresa", "artId"), ("artCodigo",), list(rows),
                      (("Empresa", "artCodigo"),))]


def row(id=980001, **extra):
    return {"Empresa": 90001, "artId": id, "artCodigo": f"QA-SEED-{id}",
            "artNombre": f"QA-SEED-PRODUCTO-{id}", "price": "1000.00", **extra}


def test_mysql_upserts_are_repeatable_and_repair_owned_values(connection):
    tables = catalog(row())
    first = apply_tables(connection, tables)
    second = apply_tables(connection, tables)
    assert first["counts"] == {"inserted": 1, "updated": 0, "unchanged": 0}
    assert second["counts"] == {"inserted": 0, "updated": 0, "unchanged": 1}
    query(connection, "UPDATE articulos SET price=999 WHERE Empresa=90001 AND artId=980001")
    connection.commit()
    assert apply_tables(connection, tables)["counts"]["updated"] == 1
    assert query(connection, "SELECT COUNT(*) AS n, SUM(price) AS total FROM articulos")[0] == {
        "n": 1, "total": 1000}


@pytest.mark.parametrize("foreign", [
    row(980002, artCodigo="AJENO"),
    row(900, artCodigo="QA-SEED-980002"),
    row(900, Empresa=123, artNombre="QA-SEED-PRODUCTO-980002"),
])
def test_mysql_preflight_rejects_pk_code_and_global_unique_collisions(connection, foreign):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO articulos VALUES (%s,%s,%s,%s,%s)", tuple(foreign.values()))
    connection.commit()
    with pytest.raises(QAError, match="[Cc]olisi"):
        apply_tables(connection, catalog(row(), row(980002)))
    actual = query(connection, "SELECT * FROM articulos")
    assert len(actual) == 1
    assert actual[0]["artCodigo"] == foreign["artCodigo"]
    assert actual[0]["Empresa"] == foreign["Empresa"]


def test_mysql_error_mid_batch_rolls_back_prior_successful_insert(connection):
    with pytest.raises(QAError):
        apply_tables(connection, catalog(row(), row(980002, price="1000000000.00")))
    assert query(connection, "SELECT COUNT(*) AS n FROM articulos")[0]["n"] == 0


def test_mysql_nontransactional_table_is_rejected_without_writes(connection):
    query(connection, "ALTER TABLE articulos ENGINE=MyISAM")
    with pytest.raises(QAError, match="InnoDB"):
        apply_tables(connection, catalog(row()))
    assert query(connection, "SELECT COUNT(*) AS n FROM articulos")[0]["n"] == 0


def test_mysql_generated_unique_key_is_rejected_before_upsert(connection):
    query(connection, "ALTER TABLE articulos ADD generated_code VARCHAR(3) "
                      "GENERATED ALWAYS AS (LEFT(artCodigo,3)) STORED, ADD UNIQUE(generated_code)")
    with pytest.raises(QAError, match="[Íí]ndice"):
        apply_tables(connection, catalog(row()))
    assert query(connection, "SELECT COUNT(*) AS n FROM articulos")[0]["n"] == 0


def test_mysql_uncertified_foreign_keys_are_rejected_before_writes(connection):
    query(connection, "CREATE TABLE external_link (tenant INT, product INT, "
                      "FOREIGN KEY(tenant,product) REFERENCES articulos(Empresa,artId) "
                      "ON UPDATE CASCADE) ENGINE=InnoDB")
    try:
        with pytest.raises(QAError, match="[Cc]lave foránea"):
            apply_tables(connection, catalog(row()))
        assert query(connection, "SELECT COUNT(*) AS n FROM articulos")[0]["n"] == 0
    finally:
        query(connection, "DROP TABLE external_link")
