"""Known synchronization effects on owned disposable MySQL, never a QA baseline.

DDL below exists only in this test server. Runtime certification never installs
or disables a trigger/routine. Queue DDL: XGestion2 DATABASE_SCHEMA.sql:1577-1596.
"""

import os
import re
from pathlib import Path

import pytest
from seed_mysql_runtime import EphemeralMySQL

from framework.errors import QAError
from products.xgestion.seeds.engine import apply_tables, query
from products.xgestion.seeds.model import SeedTable
from products.xgestion.seeds.triggers import CURRENT_FUNCTION, LEGACY_FUNCTION, check_triggers

pytestmark = pytest.mark.skipif(not os.environ.get("XSOFT_SEED_MYSQL_BIN"),
                                reason="Integración MySQL opt-in: configurar XSOFT_SEED_MYSQL_BIN.")
ROOT = Path(__file__).resolve().parents[1]
QUEUE_DDL = """
CREATE TABLE t_int_sincronizador (
  Empresa INT NOT NULL, Sucursal INT NOT NULL, Computadora INT NOT NULL DEFAULT 0,
  ID INT NOT NULL, Tabla VARCHAR(100) NOT NULL DEFAULT '', Accion VARCHAR(45) NOT NULL,
  SucursalesDestino VARCHAR(45) DEFAULT NULL, ComputadorasDestino VARCHAR(45) DEFAULT NULL,
  ID_Computadora INT NOT NULL DEFAULT 0, fecha_insert DATETIME NOT NULL,
  usuario_insert VARCHAR(45) DEFAULT NULL, fecha_update DATETIME DEFAULT NULL,
  usuario_update VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (Empresa,Sucursal,Computadora,ID,Tabla,ID_Computadora,fecha_insert)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
"""


@pytest.fixture(scope="module")
def server():
    with EphemeralMySQL(ROOT) as running:
        with running.connection(dict_cursor=True) as connection:
            ddl = (ROOT / "tests/fixtures/xgestion_seed_schema.sql").read_text(encoding="utf-8")
            for statement in re.sub(r"(?m)^--[^\n]*", "", ddl).split(";"):
                if statement.strip():
                    query(connection, statement)
            query(connection, QUEUE_DDL)
            connection.commit()
        yield running


@pytest.fixture
def connection(server):
    with server.connection(dict_cursor=True) as connection:
        query(connection, "DROP TRIGGER IF EXISTS articulos_AFTER_INSERT")
        query(connection, "DROP FUNCTION IF EXISTS fEnviarSincronizacion")
        query(connection, "DELETE FROM articulos")
        query(connection, "DELETE FROM t_int_sincronizador")
        connection.commit()
        yield connection


def install_test_only_trigger(connection, body, kind="INT"):
    query(connection, "CREATE FUNCTION fEnviarSincronizacion("
          "p_empresa INT,p_sucursal INT,p_computadora INT,p_id INT,p_tabla VARCHAR(255),"
          f"p_accion VARCHAR(255),p_usuario VARCHAR(255)) RETURNS {kind} "
          "NOT DETERMINISTIC SQL SECURITY DEFINER MODIFIES SQL DATA " + body)
    query(connection, "CREATE TRIGGER articulos_AFTER_INSERT AFTER INSERT ON articulos FOR EACH ROW "
          "BEGIN SELECT fEnviarSincronizacion(NEW.Empresa,0,0,NEW.artId,'articulos','insert',"
          "NEW.usuario_insert) INTO @resultado; END")


def tables(*prices):
    return [SeedTable("articulos", ("Empresa", "artId"), ("artCodigo",), [
        {"Empresa": 90001, "artId": 980001 + position, "artCodigo": f"QA-SEED-{position}",
         "artNombre": f"QA-SEED-{position}", "artPrecioVenta": price,
         "usuario_insert": "QA-SEED", "usuario_update": "QA-SEED"}
        for position, price in enumerate(prices)])]


@pytest.mark.parametrize(("body", "kind", "expected_queue"), [
    ("RETURN 1", "INT", 0), (LEGACY_FUNCTION, "BIT(1)", 1), (CURRENT_FUNCTION, "INT", 1),
])
def test_real_metadata_certifies_source_function_and_repeat_avoids_queue_updates(
        connection, body, kind, expected_queue):
    install_test_only_trigger(connection, body, kind)
    seed = tables("1000.00")
    certify = lambda connection: check_triggers(connection, seed)  # noqa: E731
    assert apply_tables(connection, seed, preflight=certify)["counts"]["inserted"] == 1
    queued = query(connection, "SELECT * FROM t_int_sincronizador")
    assert len(queued) == expected_queue
    assert apply_tables(connection, seed, preflight=certify)["counts"]["unchanged"] == 1
    assert query(connection, "SELECT * FROM t_int_sincronizador") == queued


def test_later_error_rolls_back_insert_and_known_trigger_queue_together(connection):
    install_test_only_trigger(connection, CURRENT_FUNCTION)
    seed = tables("1000.00", "99999999999999.00")
    with pytest.raises(QAError):
        apply_tables(connection, seed, preflight=lambda conn: check_triggers(conn, seed))
    assert query(connection, "SELECT COUNT(*) AS n FROM articulos")[0]["n"] == 0
    assert query(connection, "SELECT COUNT(*) AS n FROM t_int_sincronizador")[0]["n"] == 0


@pytest.mark.parametrize("mode", ["before", "unknown-function"])
def test_real_unknown_automation_is_rejected_before_any_write(connection, mode):
    install_test_only_trigger(connection, "RETURN 2" if mode == "unknown-function" else "RETURN 1")
    if mode == "before":
        query(connection, "DROP TRIGGER articulos_AFTER_INSERT")
        query(connection, "CREATE TRIGGER articulos_AFTER_INSERT BEFORE INSERT ON articulos FOR EACH ROW "
              "SET NEW.artNombre='UNEXPECTED'")
    with pytest.raises(QAError, match="trigger|función"):
        apply_tables(connection, tables("1000.00"))
    assert query(connection, "SELECT COUNT(*) AS n FROM articulos")[0]["n"] == 0
    assert query(connection, "SELECT COUNT(*) AS n FROM t_int_sincronizador")[0]["n"] == 0
