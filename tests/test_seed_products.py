from datetime import date
from decimal import Decimal

from products.xgestion.seeds.products import REQUISITES, article, product_tables, stock_row


def context(reference_date=date(2026, 9, 21)):
    from products.xgestion.seeds.model import SeedContext

    return SeedContext(empresa=51, sucursal=7, computadora=3, usuario_id=12, reference_date=reference_date)


def tables(ctx=None):
    return {table.name: table for table in product_tables(ctx or context())}


def by_code():
    return {row["artCodigo"]: row for row in tables()["articulos"].rows}


def test_same_seed_input_is_deterministic_and_has_no_duplicate_primary_keys():
    first = product_tables(context())
    assert first == product_tables(context())
    for table in first:
        keys = [tuple(row[key] for key in table.keys) for row in table.rows]
        assert len(keys) == len(set(keys)), table.name
        assert all(row["Empresa"] == 51 for row in table.rows)
        assert all(all(key in row for key in table.identity) for row in table.rows)


def test_seed_is_separate_from_current_fixture_and_does_not_overwrite_global_catalogues():
    seeded = tables()
    assert not {"t_sis_iva", "t_sis_moneda", "articulos_ume", "_empresa", "_sucursales", "_usuarios"} & seeded.keys()
    articles = seeded["articulos"]
    assert articles.natural_keys == (("Empresa", "artCodigo"),)
    assert all(980001 <= row["artId"] <= 980099 for row in articles.rows)
    assert all(row["artCodigo"].startswith("QA-SEED-") for row in articles.rows)
    assert all(row["artNombre"].startswith("QA-SEED-") for row in articles.rows)
    assert len({row["artCodigo"] for row in articles.rows}) == len(articles.rows)
    assert all("artStock" not in row for row in articles.rows), "No resetear el cache operativo al repetir."


def test_stock_seed_is_fixed_ledger_entry_scoped_to_current_context():
    seeded = tables()
    articles = by_code()
    movements = {row["moaArticuloCodigo"]: row for row in seeded["movimientos_articulos"].rows}
    for code, expected in [("STOCK-CERO", "0"), ("STOCK-UNO", "1"), ("STOCK-NEGATIVO", "-3")]:
        row = movements[articles["QA-SEED-" + code]["artId"]]
        assert Decimal(row["moaCantidad"]) == Decimal(expected)
        assert row["ID_Venta"] == row["ID_Compra"] == row["ID_ComputadoraModifica"] == 0
        assert (row["Sucursal"], row["Computadora"], row["moaUsuario"]) == (7, 3, 12)
        assert row["moaFechaHora"] == "2026-09-21 00:00:00"
    assert seeded["movimientos_articulos"].keys == (
        "Empresa", "Sucursal", "Computadora", "moaId", "ID_ComputadoraModifica"
    )


def test_reference_date_changes_dates_without_changing_stock_amounts_or_identity():
    old = tables(context(date(2026, 1, 1)))["movimientos_articulos"].rows
    new = tables(context(date(2027, 1, 1)))["movimientos_articulos"].rows
    assert [(row["moaId"], row["moaArticuloCodigo"], row["moaCantidad"]) for row in old] == [
        (row["moaId"], row["moaArticuloCodigo"], row["moaCantidad"]) for row in new
    ]
    assert {row["moaFechaHora"] for row in new} == {"2027-01-01 00:00:00"}


def test_catalogue_contains_meaningful_product_and_stock_variants():
    articles = by_code()
    assert articles["QA-SEED-NORMAL"]["artPrecioVenta"] == "1000.00"
    assert articles["QA-SEED-KG"]["artUme"] == 2
    assert articles["QA-SEED-KG"]["balanza"] == ""
    assert articles["QA-SEED-BULTO"]["artLoteHabitual"] == "12.000"
    assert articles["QA-SEED-BULTO"]["artPrecioBulto"] == "10800.000"
    assert articles["QA-SEED-INACTIVO"]["activo"] == 0
    assert articles["QA-SEED-USD"]["ID_Moneda"] == 2
    assert articles["QA-SEED-REDONDEO"]["artPrecioVenta"] == "10.01"
    assert articles["QA-SEED-CARNICERIA"]["ID_TipoProducto"] == 3
    assert articles["QA-SEED-SERVICIO"]["artStockeable"] == 0


def test_tax_variants_have_consistent_net_tax_and_final_price():
    articles = by_code()
    for suffix, iva_id, final, tax in [("IVA105", 4, "110.50", "10.50"),
                                       ("IVA21", 5, "121.00", "21.00"),
                                       ("IVA27", 6, "127.00", "27.00")]:
        row = articles["QA-SEED-" + suffix]
        assert row["ID_Iva"] == iva_id
        assert Decimal(row["PrecioNeto"]) == Decimal("100.00")
        assert Decimal(row["CantidadIva"]) == Decimal(tax)
        assert Decimal(row["CantidadImpuestos"]) == Decimal(row["CantidadItc"]) == 0
        assert Decimal(row["PrecioNeto"]) + Decimal(row["CantidadIva"]) == Decimal(final)
        assert Decimal(row["artPrecioVenta"]) == Decimal(final)
    for suffix, iva_id in [("NORMAL", 3), ("NO-GRAVADO", 1), ("EXENTO", 2)]:
        row = articles["QA-SEED-" + suffix]
        assert row["ID_Iva"] == iva_id
        assert Decimal(row["PrecioNeto"]) == Decimal(row["artPrecioVenta"])


def test_variants_resolve_to_seeded_parent_colours_and_sizes_without_stock_on_parent():
    seeded = tables()
    articles = by_code()
    parent = articles["QA-SEED-PADRE"]
    variants = {row["ID_Variante"]: row for row in seeded["variantes"].rows}
    children = [row for row in articles.values() if row["ID_ProductoPadre"] == parent["artId"]]
    assert parent["ID_TipoProducto"] == 1 and parent["EsProductoConVariantes"] == 1
    assert len(children) == 2
    for row in children:
        assert row["ID_TipoProducto"] == 2 and row["EsProductoConVariantes"] == 0
        assert variants[row["ID_Variante1"]]["ID_TipoVariante"] == 1
        assert variants[row["ID_Variante2"]]["ID_TipoVariante"] == 2
    assert parent["artId"] not in {row["moaArticuloCodigo"] for row in seeded["movimientos_articulos"].rows}


def test_compositions_and_options_reference_only_owned_seed_articles():
    seeded = tables()
    articles = {row["artId"]: row for row in seeded["articulos"].rows}
    links = seeded["productos_hijos"].rows
    assert any(articles[row["prhProductoHijo"]]["esMateriaPrima"] == 1 for row in links)
    for row in links:
        assert row["prhProducto"] in articles and row["prhProductoHijo"] in articles
        assert row["prhProducto"] != row["prhProductoHijo"]
        assert Decimal(row["prhCantidad"]) > 0
        assert articles[row["prhProducto"]]["EsProductoConSubproductos"] == 1
    for row in seeded["productos_opciones"].rows:
        assert articles[row["ID_Producto"]]["esProductoConOpciones"] == 1
        assert articles[row["ID_MateriaPrimaOrigen"]]["esMateriaPrima"] == 1
        assert row["Opcion"].startswith("QA-SEED-")


def test_requisites_cover_every_global_unit_currency_and_tax_used():
    required = {(table, key, identifier): fields for table, key, identifier, fields in REQUISITES}
    assert required[("articulos_ume", "umeId", 1)]["umeNombre"] == "UN"
    assert required[("articulos_ume", "umeId", 2)]["umeNombre"] == "KG"
    assert required[("articulos_ume", "umeId", 2)]["umeDecimal"] == 1
    assert required[("t_sis_iva", "ID_Iva", 3)]["PorcentajeIva"] == "0.00"
    assert required[("t_sis_moneda", "ID_Moneda", 1)]["Codigo_Afip"] == "PES"
    assert required[("t_sis_moneda", "ID_Moneda", 2)]["Codigo_Afip"] == "DOL"
    for row in tables()["articulos"].rows:
        assert ("articulos_ume", "umeId", row["artUme"]) in required
        assert ("t_sis_iva", "ID_Iva", row["ID_Iva"]) in required
        assert ("t_sis_moneda", "ID_Moneda", row["ID_Moneda"]) in required


def test_helpers_support_pricing_namespace_and_explicit_overrides_without_global_state():
    ctx = context()
    row = article(ctx, 980101, "QA-SEED-PRECIO", "QA-SEED-Precio", "250.00", ID_Moneda=2)
    assert row["Empresa"] == 51 and row["artId"] == 980101 and row["ID_Moneda"] == 2
    assert row["PrecioNeto"] == row["artPrecioVenta"] == "250.00"
    assert row["artFamilia"] == row["artSubfamilia"] == 980001
    movement = stock_row(ctx, 980101, 980101, "17.125")
    assert movement["moaCantidad"] == movement["moaStockFinal"] == "17.125"
    assert movement["moaStockActual"] == "0.000"
