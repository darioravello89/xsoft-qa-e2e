"""Public reference schema + synthetic context, never a private ERP database."""

import os
from datetime import date
from pathlib import Path

import pytest
from seed_mysql_runtime import EphemeralMySQL

from framework.errors import QAError
from products.xgestion.seeds.engine import apply_to_connection, catalog, query
from products.xgestion.seeds.model import SeedContext
from products.xgestion.seeds.products import REQUISITES

pytestmark = pytest.mark.skipif(not os.environ.get("XSOFT_SEED_MYSQL_BIN"),
                                reason="Integración MySQL opt-in: configurar XSOFT_SEED_MYSQL_BIN.")
ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def server():
    with EphemeralMySQL(ROOT) as running:
        yield running


@pytest.fixture
def database(server):
    with server.connection(dict_cursor=True) as conn:
        for table in query(conn, "SELECT TABLE_NAME AS name FROM information_schema.TABLES "
                           "WHERE TABLE_SCHEMA=DATABASE()"):
            query(conn, f"DROP TABLE `{table['name']}`")
        schema = (ROOT / "tests/fixtures/xgestion_seed_schema.sql").read_text(encoding="utf-8")
        statements = "\n".join(line for line in schema.splitlines() if not line.lstrip().startswith("--"))
        for statement in statements.split(";"):
            if statement.strip():
                query(conn, statement)
        query(conn, "INSERT INTO _empresa(idEmp,empNombreLegal) VALUES(90001,'QA-EMPRESA')")
        query(conn, "INSERT INTO _sucursales(Empresa,sucId) VALUES(90001,1)")
        query(conn, "INSERT INTO _computadoras(Empresa,Sucursal,cpuId) VALUES(90001,1,1)")
        query(conn, "INSERT INTO _usuarios(Empresa,usuId) VALUES(90001,90001)")
        for table, key, identifier, expected in REQUISITES:
            row = {key: identifier, **expected}
            query(conn, f"INSERT INTO `{table}` ({','.join(row)}) VALUES ({','.join('%s' for _ in row)})",
                  tuple(row.values()))
        query(conn, "INSERT INTO t_sis_tipopago(ID_TipoPago,Nombre_TipoPago) VALUES(1,'Cobrado')")
        query(conn, "INSERT INTO _pagos(Empresa,pagId,pagNombre) VALUES(90001,1,'EFECTIVO-ORIGINAL')")
        query(conn, "INSERT INTO articulos(Empresa,artId,artCodigo,artNombre,artPrecioVenta) "
                    "VALUES(90001,90001,'QA-E2E-001','PRODUCTO-ORIGINAL',1000)")
        conn.commit()
        today = query(conn, "SELECT CURDATE() AS today")[0]["today"]
        yield conn, SeedContext(90001, 1, 1, 90001, today)


def snapshot(conn, ctx):
    return {table.name: query(conn, f"SELECT * FROM `{table.name}` ORDER BY {','.join(table.keys)}")
            for table in catalog(ctx)}


def test_full_catalog_is_repeatable_and_preserves_original_fixture(database):
    conn, ctx = database
    first = apply_to_connection(conn, ctx)
    before = snapshot(conn, ctx)
    second = apply_to_connection(conn, ctx)
    assert first["counts"]["inserted"] == sum(len(table.rows) for table in catalog(ctx))
    assert second["counts"] == {"inserted": 0, "updated": 0, "unchanged": first["counts"]["inserted"]}
    assert snapshot(conn, ctx) == before
    assert first["catalog_sha256"] == second["catalog_sha256"]
    declared = {table.name: len(table.rows) for table in catalog(ctx)}
    assert len(before["articulos"]) == declared["articulos"] + 1
    assert len(before["ofertas"]) == declared["ofertas"]
    assert len(before["t_fin_listaprecio"]) == declared["t_fin_listaprecio"]
    assert len(before["_pagos"]) == declared["_pagos"] + 1
    assert query(conn, "SELECT pagNombre FROM _pagos WHERE pagId=1")[0]["pagNombre"] == "EFECTIVO-ORIGINAL"
    assert query(conn, "SELECT artPrecioVenta FROM articulos WHERE artId=90001")[0]["artPrecioVenta"] == 1000
    assert query(conn, "SELECT SUM(moaCantidad) AS amount FROM movimientos_articulos "
                      "WHERE moaArticuloCodigo=980002")[0]["amount"] == 10.5


def test_wrong_global_payment_type_blocks_without_replacing_it(database):
    conn, ctx = database
    query(conn, "UPDATE t_sis_tipopago SET Nombre_TipoPago='A Cobrar' WHERE ID_TipoPago=1")
    conn.commit()
    with pytest.raises(QAError, match="global incompatible"):
        apply_to_connection(conn, ctx)
    assert query(conn, "SELECT Nombre_TipoPago FROM t_sis_tipopago WHERE ID_TipoPago=1")[0][
        "Nombre_TipoPago"] == "A Cobrar"
    assert query(conn, "SELECT COUNT(*) AS n FROM articulos")[0]["n"] == 1
    assert query(conn, "SELECT COUNT(*) AS n FROM _pagos")[0]["n"] == 1


@pytest.mark.parametrize("identifier,name", [(989901, "PAGO-AJENO"), (99, "qa-prm-efectivo ")])
def test_dedicated_payment_identity_or_name_collision_rolls_back_entire_seed(database, identifier, name):
    conn, ctx = database
    query(conn, "INSERT INTO _pagos(Empresa,pagId,pagNombre) VALUES(90001,%s,%s)", (identifier, name))
    conn.commit()
    with pytest.raises(QAError, match="[Cc]olisi"):
        apply_to_connection(conn, ctx)
    assert query(conn, "SELECT COUNT(*) AS n FROM articulos")[0]["n"] == 1
    assert query(conn, "SELECT COUNT(*) AS n FROM _pagos")[0]["n"] == 2


def test_activation_profile_updates_one_row_and_retains_the_control_offer(database):
    conn, ctx = database
    initial = apply_to_connection(conn, ctx)
    before = snapshot(conn, ctx)
    inactive = apply_to_connection(conn, ctx, journey_profile=("XG-PRM-070", "inactive"))
    after = snapshot(conn, ctx)
    assert inactive["counts"]["updated"] == 1
    assert inactive["catalog_sha256"] != initial["catalog_sha256"]
    for table, values in before.items():
        expected = [dict(row, activo=b"\x00") if table == "ofertas" and row["ofeId"] == 988000 else row
                    for row in values]
        assert after[table] == expected
    restored = apply_to_connection(conn, ctx, journey_profile=("XG-PRM-070", "active-again"))
    assert restored["counts"]["updated"] == 1
    assert restored["catalog_sha256"] == initial["catalog_sha256"]
    assert snapshot(conn, ctx) == before


@pytest.mark.parametrize("kind,code,config", [
    (1, "980001", "{}"), (2, "980001", "{}"), (3, "980001", "{}"),
    (4, "980001", "{}"), (5, "QA-SEED", "{}"),
    (6, "0", '{"combo":{"version":1,"productos":[{"idProducto":980001,"cantidad":1},'
               '{"idProducto":90001,"cantidad":1}]}}'),
])
def test_foreign_offer_for_any_seed_scope_blocks_before_writes(database, kind, code, config):
    conn, ctx = database
    query(conn, "INSERT INTO ofertas(Empresa,ofeId,ofeTipo,ofeCodigo,ofeDesde,ofeHasta,Sucursal,Configuracion) "
                "VALUES(90001,1,%s,%s,CURDATE(),CURDATE(),'0',%s)", (kind, code, config))
    conn.commit()
    with pytest.raises(QAError, match="[Oo]ferta"):
        apply_to_connection(conn, ctx)
    assert query(conn, "SELECT COUNT(*) AS n FROM articulos")[0]["n"] == 1


def test_foreign_barcode_alias_blocks_before_writes(database):
    conn, ctx = database
    query(conn, "INSERT INTO producto_codigo(Empresa,ID_ProductoCodigo,ID_Producto,Codigo) "
                "VALUES(90001,1,90001,'QA-SEED-NORMAL')")
    conn.commit()
    with pytest.raises(QAError, match="[Cc]ódigo"):
        apply_to_connection(conn, ctx)
    assert query(conn, "SELECT COUNT(*) AS n FROM articulos")[0]["n"] == 1


def test_wrong_global_currency_blocks_without_replacing_it(database):
    conn, ctx = database
    query(conn, "UPDATE t_sis_moneda SET Codigo_Afip='EUR' WHERE ID_Moneda=2")
    conn.commit()
    with pytest.raises(QAError, match="global incompatible"):
        apply_to_connection(conn, ctx)
    assert query(conn, "SELECT Codigo_Afip FROM t_sis_moneda WHERE ID_Moneda=2")[0]["Codigo_Afip"] == "EUR"
    assert query(conn, "SELECT COUNT(*) AS n FROM articulos")[0]["n"] == 1


def test_list_id_in_another_branch_is_not_treated_as_new_owned_list(database):
    conn, ctx = database
    query(conn, "INSERT INTO t_fin_listaprecio(Empresa,Sucursal,ID_ListaPrecio,Nombre_ListaPrecio) "
                "VALUES(90001,3,980101,'LISTA-AJENA')")
    conn.commit()
    with pytest.raises(QAError, match="[Cc]olisi"):
        apply_to_connection(conn, ctx)
    assert query(conn, "SELECT COUNT(*) AS n FROM articulos")[0]["n"] == 1


def test_wrong_reference_date_blocks_without_writes(database):
    conn, ctx = database
    old = SeedContext(ctx.empresa, ctx.sucursal, ctx.computadora, ctx.usuario_id, date(2020, 1, 1))
    with pytest.raises(QAError, match="fecha"):
        apply_to_connection(conn, old)
    assert query(conn, "SELECT COUNT(*) AS n FROM articulos")[0]["n"] == 1


@pytest.mark.parametrize("tenant,active", [(90001, 0), (123, 1)])
def test_extra_composition_even_inactive_or_other_tenant_blocks(database, tenant, active):
    conn, ctx = database
    query(conn, "INSERT INTO productos_hijos(Empresa,prhId,prhProducto,prhProductoHijo,activo) "
                "VALUES(%s,1,980018,90001,%s)", (tenant, active))
    conn.commit()
    with pytest.raises(QAError, match="Relación ajena"):
        apply_to_connection(conn, ctx)
    assert query(conn, "SELECT COUNT(*) AS n FROM articulos")[0]["n"] == 1


def test_extra_foreign_product_in_seed_price_list_blocks(database):
    conn, ctx = database
    query(conn, "INSERT INTO t_fin_listapreciodetalle(Empresa,Sucursal,ID_ListaPrecioDetalle,ID_ListaPrecio,"
                "ID_Producto,ImporteGanancia,PorcentajeIva,ImporteIva,PrecioNeto,ID_Moneda) "
                "VALUES(90001,3,1,980101,90001,0,0,0,1000,1)")
    conn.commit()
    with pytest.raises(QAError, match="Relación ajena"):
        apply_to_connection(conn, ctx)
    assert query(conn, "SELECT COUNT(*) AS n FROM articulos")[0]["n"] == 1


def test_inactive_alias_collision_uses_database_collation(database):
    conn, ctx = database
    query(conn, "INSERT INTO producto_codigo(Empresa,ID_ProductoCodigo,ID_Producto,Codigo,activo) "
                "VALUES(90001,1,90001,'qa-seed-inactivo ',0)")
    conn.commit()
    with pytest.raises(QAError, match="código"):
        apply_to_connection(conn, ctx)
    assert query(conn, "SELECT COUNT(*) AS n FROM articulos")[0]["n"] == 1


def test_seed_offer_must_not_start_discounting_a_foreign_product(database):
    conn, ctx = database
    query(conn, "UPDATE articulos SET artFamilia=980113 WHERE artId=90001")
    conn.commit()
    with pytest.raises(QAError, match="Producto ajeno"):
        apply_to_connection(conn, ctx)
    assert query(conn, "SELECT COUNT(*) AS n FROM ofertas")[0]["n"] == 0


def test_component_id_in_another_tenant_blocks_legacy_join_ambiguity(database):
    conn, ctx = database
    query(conn, "INSERT INTO articulos(Empresa,artId,artCodigo) VALUES(123,980021,'MATERIA-AJENA')")
    conn.commit()
    with pytest.raises(QAError, match="composición"):
        apply_to_connection(conn, ctx)
    assert query(conn, "SELECT COUNT(*) AS n FROM articulos")[0]["n"] == 2
