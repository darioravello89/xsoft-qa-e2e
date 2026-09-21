"""Validate public commercial fixtures without running XGestion or a database."""

import json
from datetime import date, timedelta
from decimal import Decimal

import pytest

from products.xgestion.seeds.model import SeedContext, merge_tables
from products.xgestion.seeds.pricing import PRICING_CASES, pricing_tables
from products.xgestion.seeds.products import product_tables


@pytest.fixture
def context():
    return SeedContext(empresa=7, sucursal=3, computadora=2, usuario_id=5, reference_date=date(2026, 9, 21))


def rows(context, table):
    return [row for item in pricing_tables(context) if item.name == table for row in item.rows]


def test_catalog_is_repeatable_and_never_writes_operating_configuration(context):
    first = pricing_tables(context)
    assert first == pricing_tables(context)
    assert {table.name for table in first} <= {
        "_familias", "_subfamilias", "_ubicaciones", "articulos", "movimientos_articulos",
        "ofertas", "t_fin_listaprecio", "t_fin_listapreciodetalle",
    }
    for table in first:
        for row in table.rows:
            assert row["Empresa"] == 7
            assert all(field in row for field in table.keys + table.identity)
    products = rows(context, "articulos")
    assert all(980101 <= row["artId"] <= 980199 for row in products)
    assert all(row["artCodigo"].startswith("QA-SEED-") for row in products)
    assert len({row["artCodigo"] for row in products}) == len(products)


def test_commercial_and_product_catalogs_merge_without_identity_or_natural_key_collision(context):
    merged = merge_tables(product_tables(context) + pricing_tables(context))
    assert len([table for table in merged if table.name == "articulos"]) == 1
    assert len(next(table.rows for table in merged if table.name == "articulos")) > 23


@pytest.mark.parametrize(("code", "formula", "discount", "minimum", "pay"), [
    ("PCT", "%", "10", 0, "0"),
    ("IMP", "$", "150", 0, "0"),
    ("2X1", "C", "0", 2, "1"),
    ("2DA50", "C%", "0", 2, "50"),
    ("MIN-PCT", "LXO+%", "0", 2, "10"),
    ("MIN-IMP", "LXO+$", "0", 2, "150"),
    ("MIN-PRECIO", "LXO+$CU", "0", 2, "800"),
])
def test_seven_formulas_use_the_actual_persisted_fields(context, code, formula, discount, minimum, pay):
    product = next(row for row in rows(context, "articulos") if row["artCodigo"] == f"QA-SEED-{code}")
    offer = next(row for row in rows(context, "ofertas") if row["ofeNombre"] == f"QA-SEED-{code}")
    assert offer["ofeTipo"] == 4
    assert offer["ofeCodigo"] == str(product["artId"])
    assert offer["TipoDescuento"] == formula
    assert Decimal(offer["ofeDescuentoPorcentaje"]) == Decimal(discount)
    assert offer["Lleva"] == minimum
    assert Decimal(offer["Paga"]) == Decimal(pay)
    assert offer["Sucursal"] == "3"
    assert offer["ID_Pago"] == 0


def test_date_variants_follow_reference_date_including_leap_day(context):
    for anchor in (context.reference_date, date(2028, 2, 29)):
        ctx = SeedContext(7, 3, 2, 5, anchor)
        offers = {row["ofeNombre"]: row for row in rows(ctx, "ofertas")}
        assert offers["QA-SEED-EXPIRADA"]["ofeHasta"] == (anchor - timedelta(days=1)).isoformat()
        assert offers["QA-SEED-FUTURA"]["ofeDesde"] == (anchor + timedelta(days=1)).isoformat()
        assert offers["QA-SEED-INACTIVA"]["activo"] == 0
        assert offers["QA-SEED-PCT"]["ofeDesde"] <= anchor.isoformat() <= offers["QA-SEED-PCT"]["ofeHasta"]


def test_scope_targets_only_owned_categories_and_products(context):
    offers = rows(context, "ofertas")
    products = rows(context, "articulos")
    owned = {
        1: {str(row["ubiId"]) for row in rows(context, "_ubicaciones")},
        2: {str(row["famId"]) for row in rows(context, "_familias")},
        3: {str(row["subId"]) for row in rows(context, "_subfamilias")},
        4: {str(row["artId"]) for row in products},
        5: {row["artMarca"] for row in products if row["artMarca"].startswith("QA-SEED-")},
    }
    assert {row["ofeTipo"] for row in offers} == {1, 2, 3, 4, 5, 6}
    for row in offers:
        if row["ofeTipo"] != 6:
            assert row["ofeCodigo"] in owned[row["ofeTipo"]]
    grouped = next(row for row in offers if row["ofeNombre"] == "QA-SEED-AGRUPADA-3X2")
    assert json.loads(grouped["Configuracion"])["agrupada"] is True
    assert len([row for row in products if str(row["artFamilia"]) == grouped["ofeCodigo"]]) == 3


def test_combo_has_two_owned_components_and_traditional_offer_for_leftover(context):
    offers = rows(context, "ofertas")
    combo = next(row for row in offers if row["TipoDescuento"] == "COMBO")
    assert combo["ofeTipo"] == 6
    assert combo["Lleva"] == 0
    assert combo["ofeCodigo"] == "0"
    assert Decimal(combo["Paga"]) == Decimal("1500")
    config = json.loads(combo["Configuracion"])["combo"]
    assert config["version"] == 1
    products = {row["artId"]: row for row in rows(context, "articulos")}
    ids = [row["idProducto"] for row in config["productos"]]
    assert len(set(ids)) == 2
    assert all(product_id in products for product_id in ids)
    assert all(item["cantidad"] == 1 for item in config["productos"])
    assert any(row["ofeTipo"] == 4 and row["ofeCodigo"] == str(ids[0]) for row in offers)


def test_fractional_offers_have_decimal_ume_and_distinct_zero_one_thresholds(context):
    products = {row["artCodigo"]: row for row in rows(context, "articulos")}
    offers = {row["ofeNombre"]: row for row in rows(context, "ofertas")}
    for suffix, minimum in (("KG-MIN0", 0), ("KG-MIN1", 1)):
        assert products[f"QA-SEED-{suffix}"]["artUme"] == 2
        assert offers[f"QA-SEED-{suffix}"]["Lleva"] == minimum
        assert offers[f"QA-SEED-{suffix}"]["TipoDescuento"] == "LXO+$CU"


def test_lists_are_company_unique_global_and_complete_including_real_unique_key(context):
    headers = rows(context, "t_fin_listaprecio")
    details = rows(context, "t_fin_listapreciodetalle")
    assert all(row["Sucursal"] == 0 for row in headers + details)
    assert len({row["ID_ListaPrecio"] for row in headers}) == len(headers)
    unique = [(row["Empresa"], row["ID_ListaPrecio"], row["ID_Producto"]) for row in details]
    assert len(set(unique)) == len(unique)
    assert {row["ID_Moneda"] for row in details} == {1, 2}
    for row in details:
        assert {"ImporteGanancia", "PorcentajeIva", "ImporteIva", "PrecioNeto", "ID_Moneda", "Cantidad"} <= row.keys()
    inactive = next(row for row in headers if row["Nombre_ListaPrecio"] == "QA-SEED-LISTA-INACTIVA")
    assert inactive["activo"] == 0
    assert all(row["activo"] == 0 for row in details if row["ID_ListaPrecio"] == inactive["ID_ListaPrecio"])
    tiers = [row for row in details if Decimal(row["Cantidad"]) > 0]
    assert {(Decimal(row["Cantidad"]), Decimal(row["PrecioVenta"])) for row in tiers} == {
        (Decimal("2"), Decimal("900")), (Decimal("5"), Decimal("800")),
    }
    assert len({row["ID_ListaPrecio"] for row in tiers}) == 2


def test_expected_examples_keep_stock_ready_and_do_not_claim_executed_coverage(context):
    products = {row["artId"]: row for row in rows(context, "articulos")}
    movements = rows(context, "movimientos_articulos")
    assert {row["moaArticuloCodigo"] for row in movements} == products.keys()
    assert all(Decimal(row["moaCantidad"]) == Decimal("100") for row in movements)
    assert all(row["moaArticuloNombre"] == products[row["moaArticuloCodigo"]]["artNombre"] for row in movements)
    assert PRICING_CASES
    assert all(case["status"] == "manual_pending" and case["source"] for case in PRICING_CASES)
    examples = {case["id"]: case for case in PRICING_CASES}
    assert examples["COMBO-SOBRANTE"]["expected_total"] == "2400.00"
    assert examples["KG-MIN0-0500"]["expected_total"] == "400.00"
    assert examples["KG-MIN1-0500"]["expected_total"] == "500.00"
    assert examples["2DA50-Q3"]["expected_total"] == "2500.00"
    assert all(set(case["quantities"]) <= {row["artCodigo"] for row in products.values()} for case in PRICING_CASES)
    json.dumps(PRICING_CASES)
