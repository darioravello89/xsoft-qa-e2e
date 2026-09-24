"""Datos de circuito: costos originales, stock real y aislamiento de ofertas."""

from datetime import date
from decimal import Decimal

from products.xgestion.seeds.engine import catalog
from products.xgestion.seeds.model import SeedContext

CONTEXT = SeedContext(90001, 1, 1, 90001, date(2026, 9, 24))


def circuit_rows():
    tables = {table.name: table.rows for table in catalog(CONTEXT)}
    products = {row["artCodigo"]: row for row in tables["articulos"]
                if row["artCodigo"].startswith("QA-CIR-")}
    return tables, products


def test_circuit_products_cover_original_currency_price_modes_and_stock_types():
    tables, products = circuit_rows()
    assert set(products) == {"QA-CIR-ARS-FIJO", "QA-CIR-USD-FIJO", "QA-CIR-ARS-CALCULADO",
                             "QA-CIR-USD-CALCULADO", "QA-CIR-USD-KG", "QA-CIR-USD-BULTO",
                             "QA-CIR-USD-SERVICIO", "QA-CIR-CONTROL"}
    for code, currency, price, cost in (("ARS", 1, "1000", "500"), ("USD", 2, "100", "50")):
        for mode in ("FIJO", "CALCULADO"):
            product = products[f"QA-CIR-{code}-{mode}"]
            assert product["ID_Moneda"] == currency
            assert Decimal(product["artPrecioVenta"]) == Decimal(price)
            assert Decimal(product["artPrecioCosto"]) == Decimal(cost)
            assert product["esPrecioCalculado"] == int(mode == "CALCULADO")
            assert Decimal(product["artPrecioPorcentaje"]) == (100 if mode == "CALCULADO" else 0)
    assert products["QA-CIR-USD-KG"]["artUme"] == 2
    assert Decimal(products["QA-CIR-USD-KG"]["artPrecioVenta"]) == Decimal("10.01")
    assert Decimal(products["QA-CIR-USD-BULTO"]["artLoteHabitual"]) == 12
    service = products["QA-CIR-USD-SERVICIO"]
    assert service["artStockeable"] == 0
    assert all(row["moaArticuloCodigo"] != service["artId"] for row in tables["movimientos_articulos"])


def test_circuit_stock_is_initial_movements_not_a_reset_of_product_cache():
    tables, products = circuit_rows()
    expected = {"ARS-FIJO": "20", "USD-FIJO": "20", "ARS-CALCULADO": "20",
                "USD-CALCULADO": "20", "USD-KG": "10.500", "USD-BULTO": "24", "CONTROL": "7"}
    for suffix, quantity in expected.items():
        product = products[f"QA-CIR-{suffix}"]
        assert "artStock" not in product
        rows = [row for row in tables["movimientos_articulos"] if row["moaArticuloCodigo"] == product["artId"]]
        assert len(rows) == 1
        assert Decimal(rows[0]["moaCantidad"]) == Decimal(quantity)
        assert (rows[0]["Empresa"], rows[0]["Sucursal"], rows[0]["Computadora"]) == (90001, 1, 1)
        assert rows[0]["ID_Venta"] == rows[0]["ID_Compra"] == 0


def test_circuit_categories_are_independent_and_do_not_add_global_currency_rows():
    from products.xgestion.seeds.circuits import circuit_tables

    tables, products = circuit_rows()
    added = circuit_tables(CONTEXT)
    assert len(products) == 8
    assert {table.name for table in added} == {
        "_familias", "_subfamilias", "_ubicaciones", "articulos", "movimientos_articulos"}
    assert {p["artFamilia"] for p in products.values()} == {990100}
    assert {p["artMarca"] for p in products.values()} == {"QA-CIR-MARCA"}
    identities = {row["artId"] for row in products.values()}
    assert len(identities) == 8
    assert all(row["artCodigo"].startswith("QA-CIR-") for row in tables["articulos"]
               if row["artId"] in identities)
    from products.xgestion.seeds.products import product_tables

    for table in product_tables(CONTEXT):
        for original in table.rows:
            assert original in tables[table.name]
