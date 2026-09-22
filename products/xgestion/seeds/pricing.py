"""Synthetic prices/offers grounded in XGestion2 f342381, never executable E2E results.

Source paths are relative to XGestion2. DATABASE_SCHEMA.sql:1104,1410,1429;
VerificadorDeBaseDeDatos.java:2098 adds list-detail Cantidad. Eight persisted
discount types: Utilidades/Enums/TipoOfertaDescuento.java. Currency/UME IDs
must be checked against the imported private database before applying.
"""

import json
from datetime import timedelta

from products.xgestion.seeds.model import SeedContext, SeedTable
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
    article,
    stock_row,
)

ERP_COMMIT = "f34238183d494259bed1279dd7d9aac0ce16a3ae"
_FIN_TEST = "test/ModuloFinanzas/Entidades/"


def _case(case_id, quantities, expected, source, **extra):
    return {
        "id": case_id, "status": "manual_pending", "quantities": quantities,
        "expected_total": expected, "currency": "ARS", "source": source,
        "erp_commit": ERP_COMMIT, **extra,
    }


# Values are hand-derived examples of source rules, not a second implementation
# of ERP calculations. They require the selected profile and a real UI check.
PRICING_CASES = [
    _case("PCT-Q3", {"QA-SEED-PCT": "3"}, "2700.00", _FIN_TEST + "OfertaPorcentajeTest.java",
          e2e_scenario="XG-PRM-001"),
    _case("IMP-Q3", {"QA-SEED-IMP": "3"}, "2550.00", _FIN_TEST + "OfertaPrecioTest.java",
          e2e_scenario="XG-PRM-002"),
    _case("2X1-Q3", {"QA-SEED-2X1": "3"}, "2000.00", _FIN_TEST + "OfertaLlevaXPagaXTest.java",
          e2e_scenario="XG-PRM-003"),
    _case("2DA50-Q3", {"QA-SEED-2DA50": "3"}, "2500.00", _FIN_TEST + "OfertaCantidadPorcentajeTest.java",
          e2e_scenario="XG-PRM-004"),
    _case("MIN-PCT-Q2", {"QA-SEED-MIN-PCT": "2"}, "1800.00", _FIN_TEST + "OfertaCantidadMayorPorcentajeTest.java"),
    _case("MIN-IMP-Q2", {"QA-SEED-MIN-IMP": "2"}, "1700.00", _FIN_TEST + "OfertaCantidadMayorImporteTest.java"),
    _case("MIN-PRECIO-Q2", {"QA-SEED-MIN-PRECIO": "2"}, "1600.00", _FIN_TEST + "OfertaCantidadMayorPrecioUnitarioTest.java"),
    _case("COMBO", {"QA-SEED-COMBO-A": "1", "QA-SEED-COMBO-B": "1"}, "1500.00",
          _FIN_TEST + "OfertaComboCalculadorTest.java"),
    _case("COMBO-SOBRANTE", {"QA-SEED-COMBO-A": "2", "QA-SEED-COMBO-B": "1"}, "2400.00",
          "src/ModuloVentas/Servicios/OfertaComboService.java", note="Combo primero; 10% en A sobrante."),
    _case("KG-MIN0-0500", {"QA-SEED-KG-MIN0": "0.500"}, "400.00", _FIN_TEST + "OfertaPesableFraccionadoTest.java"),
    _case("KG-MIN1-0500", {"QA-SEED-KG-MIN1": "0.500"}, "500.00", _FIN_TEST + "OfertaPesableFraccionadoTest.java"),
    _case("KG-MIN1-1000", {"QA-SEED-KG-MIN1": "1.000"}, "800.00", _FIN_TEST + "OfertaPesableFraccionadoTest.java"),
    _case("AGRUPADA-3X2", {"QA-SEED-GRUPO-A": "1", "QA-SEED-GRUPO-B": "1", "QA-SEED-GRUPO-C": "1"},
          "2000.00", _FIN_TEST + "OfertaAplicacionCalculadorAgrupacionTest.java"),
    *[_case(name, {f"QA-SEED-{name}": "1"}, "1000.00",
            "src/ModuloFinanzas/Entidades/OfertaLineaService.java", e2e_scenario=f"XG-PRM-{number:03}")
      for number, name in enumerate(("EXPIRADA", "FUTURA", "INACTIVA"), start=5)],
    *[_case(name, {f"QA-SEED-{name}": "1"}, "900.00",
            "src/ModuloFinanzas/Entidades/OfertaAplicacionCalculador.java") for name in ("FAMILIA", "SUBFAMILIA", "MARCA", "SECTOR")],
    _case("LISTA-ARS", {"QA-SEED-LISTAS": "1"}, "750.00",
          "src/ModuloProveedores/Entidades/ListaPrecioDetalle.java", selected_list=980101),
    _case("LISTA-USD", {"QA-SEED-LISTAS": "1"}, "2.50",
          "src/ModuloProveedores/Entidades/ListaPrecioDetalle.java", selected_list=980102,
          currency="USD", note="Precio expresado en USD; conversión depende de la cotización del perfil."),
    _case("CANTIDAD-Q1", {"QA-SEED-CANTIDAD": "1"}, "1000.00",
          "src/ModuloProveedores/Entidades/ListaPrecioDetalle.java", selected_list=0),
    _case("CANTIDAD-Q2", {"QA-SEED-CANTIDAD": "2"}, "1800.00",
          "src/ModuloProveedores/Entidades/ListaPrecioDetalle.java", selected_list=0),
    _case("CANTIDAD-Q5", {"QA-SEED-CANTIDAD": "5"}, "4000.00",
          "src/ModuloProveedores/Entidades/ListaPrecioDetalle.java", selected_list=0),
    _case("LISTA-PRIORIDAD", {"QA-SEED-CANTIDAD": "5"}, "4750.00",
          "test/ModuloVentas/Vistas/FormVentaListaPrecioPrioridadPolicyTest.java", selected_list=980101,
          note="La lista elegida contiene el producto y prevalece sobre el precio por cantidad."),
]
CASES = PRICING_CASES


def _offer(ctx, offer_id, code, product_id, formula="%", discount="10", minimum=0, pay="0", **overrides):
    return {
        "Empresa": ctx.empresa, "ofeId": offer_id, "ofeNombre": f"QA-SEED-{code}",
        "ofeDesde": (ctx.reference_date - timedelta(days=365)).isoformat(),
        "ofeHasta": (ctx.reference_date + timedelta(days=365)).isoformat(),
        "ofeTipo": 4, "ofeTipoNombre": "Producto", "ofeCodigo": str(product_id),
        "ofeCodigoNombre": f"QA-SEED-{code}", "TipoDescuento": formula,
        "ofeDescuentoPorcentaje": discount, "Lleva": minimum, "Paga": pay,
        "Sucursal": str(ctx.sucursal), "ID_Pago": 0, "Configuracion": "{}",
        "activo": 1, "usuario_insert": "QA-SEED", "usuario_update": "QA-SEED", **overrides,
    }


def _detail(ctx, detail_id, list_id, product_id, price, currency=1, quantity="0", active=1):
    return {
        "Empresa": ctx.empresa, "Sucursal": 0, "ID_ListaPrecioDetalle": detail_id,
        "ID_ListaPrecio": list_id, "ID_Producto": product_id, "Codigo_Proveedor": "QA-SEED",
        "PrecioCosto": "0.000", "CostoFlete": "0.000", "PorcentajeGanancia": "0.000",
        "ImporteGanancia": price, "PorcentajeIva": "0.000", "ImporteIva": "0.000",
        "PrecioVenta": price, "PrecioNeto": price, "ID_Moneda": currency,
        "esPrecioCalculado": 0, "Cantidad": quantity, "activo": active,
        "usuario_insert": "QA-SEED", "usuario_update": "QA-SEED",
    }


def pricing_tables(ctx: SeedContext) -> list[SeedTable]:
    """Return owned rows; never read a file, connect, or assign customers/shifts."""
    specs = [
        (101, "PCT"), (102, "IMP"), (103, "2X1"), (104, "2DA50"),
        (105, "MIN-PCT"), (106, "MIN-IMP"), (107, "MIN-PRECIO"),
        (108, "COMBO-A"), (109, "COMBO-B"), (110, "EXPIRADA"),
        (111, "FUTURA"), (112, "INACTIVA"), (113, "FAMILIA"),
        (114, "SUBFAMILIA"), (115, "MARCA"), (116, "SECTOR"),
        (117, "KG-MIN0"), (118, "KG-MIN1"), (119, "GRUPO-A"),
        (120, "GRUPO-B"), (121, "GRUPO-C"), (122, "LISTAS"), (123, "CANTIDAD"),
    ]
    products = [article(ctx, 980000 + suffix, f"QA-SEED-{name}", f"QA-SEED-{name}") for suffix, name in specs]
    by_id = {row["artId"]: row for row in products}
    by_id[980113].update(artFamilia=980113, artFamiliaNombre="QA-SEED-OFERTA-FAMILIA",
                        artSubfamilia=980113, artSubfamiliaNombre="QA-SEED-FAMILIA-DETALLE")
    by_id[980114].update(artSubfamilia=980114, artSubfamiliaNombre="QA-SEED-OFERTA-SUBFAMILIA")
    by_id[980115].update(artMarca="QA-SEED-MARCA-115")
    by_id[980116].update(artUbicacion=980116, artUbicacionNombre="QA-SEED-SECTOR")
    for product_id in (980117, 980118):
        by_id[product_id].update(artUme=2)
    for product_id in (980119, 980120, 980121):
        by_id[product_id].update(artFamilia=980119, artFamiliaNombre="QA-SEED-AGRUPADA",
                                 artSubfamilia=980119, artSubfamiliaNombre="QA-SEED-AGRUPADA-DETALLE")

    formulas = [
        (101, "PCT", "%", "10", 0, "0"), (102, "IMP", "$", "150", 0, "0"),
        (103, "2X1", "C", "0", 2, "1"), (104, "2DA50", "C%", "0", 2, "50"),
        (105, "MIN-PCT", "LXO+%", "0", 2, "10"), (106, "MIN-IMP", "LXO+$", "0", 2, "150"),
        (107, "MIN-PRECIO", "LXO+$CU", "0", 2, "800"),
        (117, "KG-MIN0", "LXO+$CU", "0", 0, "800"), (118, "KG-MIN1", "LXO+$CU", "0", 1, "800"),
    ]
    offers = [_offer(ctx, 980000 + suffix, code, 980000 + suffix, formula, discount, minimum, pay)
              for suffix, code, formula, discount, minimum, pay in formulas]
    offers += [
        _offer(ctx, 980108, "COMBO", 0, "COMBO", "0", 0, "1500", ofeTipo=6, ofeTipoNombre="Combo",
               Configuracion=json.dumps({"combo": {"version": 1, "productos": [
                   {"idProducto": 980108, "cantidad": 1}, {"idProducto": 980109, "cantidad": 1},
               ]}}, separators=(",", ":"))),
        _offer(ctx, 980109, "COMBO-SOBRANTE", 980108),
        _offer(ctx, 980110, "EXPIRADA", 980110, ofeHasta=(ctx.reference_date - timedelta(days=1)).isoformat()),
        _offer(ctx, 980111, "FUTURA", 980111, ofeDesde=(ctx.reference_date + timedelta(days=1)).isoformat()),
        _offer(ctx, 980112, "INACTIVA", 980112, activo=0),
        _offer(ctx, 980113, "FAMILIA", 980113, ofeTipo=2, ofeTipoNombre="Familia",
               ofeCodigoNombre="QA-SEED-OFERTA-FAMILIA"),
        _offer(ctx, 980114, "SUBFAMILIA", 980114, ofeTipo=3, ofeTipoNombre="Subfamilia",
               ofeCodigoNombre="QA-SEED-OFERTA-SUBFAMILIA"),
        _offer(ctx, 980115, "MARCA", "QA-SEED-MARCA-115", ofeTipo=5, ofeTipoNombre="Marca",
               ofeCodigoNombre="QA-SEED-MARCA-115"),
        _offer(ctx, 980116, "SECTOR", 980116, ofeTipo=1, ofeTipoNombre="Sector"),
        _offer(ctx, 980119, "AGRUPADA-3X2", 980119, "C", "0", 3, "2", ofeTipo=2,
               ofeTipoNombre="Familia", Configuracion='{"agrupada":true}'),
    ]
    list_names = [(980101, "ARS"), (980102, "USD"), (980103, "CANTIDAD-2"),
                  (980104, "CANTIDAD-5"), (980105, "INACTIVA")]
    headers = [{"Empresa": ctx.empresa, "Sucursal": 0, "ID_ListaPrecio": list_id,
                "ID_Proveedor": 980001, "Nombre_ListaPrecio": f"QA-SEED-LISTA-{name}",
                "activo": int(name != "INACTIVA"), "usuario_insert": "QA-SEED", "usuario_update": "QA-SEED"}
               for list_id, name in list_names]
    details = [
        _detail(ctx, 980101, 980101, 980122, "750.000"),
        _detail(ctx, 980102, 980102, 980122, "2.500", currency=2),
        _detail(ctx, 980103, 980103, 980123, "900.000", quantity="2.00"),
        _detail(ctx, 980104, 980104, 980123, "800.000", quantity="5.00"),
        _detail(ctx, 980105, 980105, 980122, "500.000", active=0),
        _detail(ctx, 980106, 980101, 980123, "950.000"),
    ]
    return [
        SeedTable("_familias", FAMILY_KEYS, FAMILY_IDENTITY, [
            {"Empresa": ctx.empresa, "famId": 980113, "famNombre": "QA-SEED-OFERTA-FAMILIA", "activo": 1},
            {"Empresa": ctx.empresa, "famId": 980119, "famNombre": "QA-SEED-AGRUPADA", "activo": 1},
        ], natural_keys=FAMILY_NATURAL_KEYS),
        SeedTable("_subfamilias", SUBFAMILY_KEYS, SUBFAMILY_IDENTITY, [
            {"Empresa": ctx.empresa, "subId": 980113, "subNombre": "QA-SEED-FAMILIA-DETALLE", "famId": 980113, "activo": 1},
            {"Empresa": ctx.empresa, "subId": 980114, "subNombre": "QA-SEED-OFERTA-SUBFAMILIA", "famId": 980001, "activo": 1},
            {"Empresa": ctx.empresa, "subId": 980119, "subNombre": "QA-SEED-AGRUPADA-DETALLE", "famId": 980119, "activo": 1},
        ], natural_keys=SUBFAMILY_NATURAL_KEYS),
        SeedTable("_ubicaciones", LOCATION_KEYS, LOCATION_IDENTITY, [
            {"Empresa": ctx.empresa, "ubiId": 980116, "ubiNombre": "QA-SEED-SECTOR", "activo": 1},
        ], natural_keys=LOCATION_NATURAL_KEYS),
        SeedTable("articulos", ARTICLE_KEYS, ARTICLE_IDENTITY, products, natural_keys=ARTICLE_NATURAL_KEYS),
        SeedTable("movimientos_articulos", STOCK_KEYS, STOCK_IDENTITY,
                  [dict(stock_row(ctx, row["artId"], row["artId"], "100.000"),
                        moaArticuloNombre=row["artNombre"]) for row in products]),
        SeedTable("ofertas", ("Empresa", "ofeId"), ("ofeNombre",), offers),
        SeedTable("t_fin_listaprecio", ("Empresa", "Sucursal", "ID_ListaPrecio"), ("Nombre_ListaPrecio",), headers,
                  natural_keys=(("Empresa", "ID_ListaPrecio"), ("Empresa", "Nombre_ListaPrecio"))),
        SeedTable("t_fin_listapreciodetalle", ("Empresa", "Sucursal", "ID_ListaPrecioDetalle"),
                  ("ID_ListaPrecio", "ID_Producto", "Codigo_Proveedor"), details),
    ]
