"""Productos independientes para conciliar compras, ventas, stock y dinero."""

from products.xgestion.seeds.model import SeedTable
from products.xgestion.seeds.products import (
    ARTICLE_IDENTITY,
    ARTICLE_KEYS,
    ARTICLE_NATURAL_KEYS,
    FAMILY_IDENTITY,
    FAMILY_KEYS,
    FAMILY_NATURAL_KEYS,
    LOCATION_IDENTITY,
    LOCATION_KEYS,
    LOCATION_NATURAL_KEYS,
    STOCK_IDENTITY,
    STOCK_KEYS,
    SUBFAMILY_IDENTITY,
    SUBFAMILY_KEYS,
    SUBFAMILY_NATURAL_KEYS,
    _audit,
    article,
    stock_row,
)

SOURCE_COMMIT = "0adea394095e4ceff54344bf38cbf21b7c01a5e8"
CATEGORY = 990100
# Precio/costo siempre en moneda del artículo. La cantidad es stock inicial base.
PRODUCTS = (
    (990101, "ARS-FIJO", "1000.00", "500.00", "20.000", {}),
    (990102, "USD-FIJO", "100.00", "50.00", "20.000", {"ID_Moneda": 2}),
    (990103, "ARS-CALCULADO", "1000.00", "500.00", "20.000",
     {"esPrecioCalculado": 1, "artPrecioPorcentaje": "100.00"}),
    (990104, "USD-CALCULADO", "100.00", "50.00", "20.000",
     {"ID_Moneda": 2, "esPrecioCalculado": 1, "artPrecioPorcentaje": "100.00"}),
    (990105, "USD-KG", "10.01", "5.00", "10.500", {"ID_Moneda": 2, "artUme": 2}),
    (990106, "USD-BULTO", "100.00", "50.00", "24.000",
     {"ID_Moneda": 2, "artLoteHabitual": "12.000", "artPrecioBulto": "1200.000"}),
    (990107, "USD-SERVICIO", "50.00", "0.00", None, {"ID_Moneda": 2, "artStockeable": 0}),
    (990108, "CONTROL", "900.00", "450.00", "7.000", {}),
)


def circuit_tables(ctx):
    audit = _audit(ctx)
    result = [
        SeedTable("_familias", FAMILY_KEYS, FAMILY_IDENTITY,
                  [{"Empresa": ctx.empresa, "famId": CATEGORY, "famNombre": "QA-CIR-FAMILIA",
                    "activo": 1, "orden": CATEGORY, "EsParaCocina": 0, **audit}], FAMILY_NATURAL_KEYS),
        SeedTable("_subfamilias", SUBFAMILY_KEYS, SUBFAMILY_IDENTITY,
                  [{"Empresa": ctx.empresa, "subId": CATEGORY, "famId": CATEGORY,
                    "subNombre": "QA-CIR-SUBFAMILIA", "activo": 1, "orden": CATEGORY, **audit}],
                  SUBFAMILY_NATURAL_KEYS),
        SeedTable("_ubicaciones", LOCATION_KEYS, LOCATION_IDENTITY,
                  [{"Empresa": ctx.empresa, "ubiId": CATEGORY, "ubiNombre": "QA-CIR-SECTOR",
                    "activo": 1, **audit}], LOCATION_NATURAL_KEYS),
    ]
    products, stock = [], []
    for identifier, suffix, price, cost, quantity, overrides in PRODUCTS:
        code = "QA-CIR-" + suffix
        products.append(article(ctx, identifier, code, code, price, artPrecioCosto=cost,
                                artFamilia=CATEGORY, artFamiliaNombre="QA-CIR-FAMILIA",
                                artSubfamilia=CATEGORY, artSubfamiliaNombre="QA-CIR-SUBFAMILIA",
                                artUbicacion=CATEGORY, artUbicacionNombre="QA-CIR-SECTOR",
                                artMarca="QA-CIR-MARCA", **overrides))
        if quantity is not None:
            movement = stock_row(ctx, identifier, identifier, quantity)
            movement["moaArticuloNombre"] = code
            stock.append(movement)
    result.extend((SeedTable("articulos", ARTICLE_KEYS, ARTICLE_IDENTITY, products, ARTICLE_NATURAL_KEYS),
                   SeedTable("movimientos_articulos", STOCK_KEYS, STOCK_IDENTITY, stock)))
    return result
