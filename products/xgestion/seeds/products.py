"""Datos comerciales sintéticos; no abre conexiones ni calcula un saldo operativo.

Contrato: XGestion2 f34238183, Articulo/ProductoHijo/MovimientoArticulo y su
VerificadorDeBaseDeDatos. El esquema efectivo se valida antes de escribir.
"""

from decimal import ROUND_HALF_UP, Decimal

from products.xgestion.seeds.model import SeedContext, SeedTable

ARTICLE_KEYS = ("Empresa", "artId")
ARTICLE_IDENTITY = ("artCodigo",)
ARTICLE_NATURAL_KEYS = (("Empresa", "artCodigo"),)
STOCK_KEYS = ("Empresa", "Sucursal", "Computadora", "moaId", "ID_ComputadoraModifica")
STOCK_IDENTITY = ("moaArticuloCodigo", "moaNotas")
FAMILY_KEYS = ("Empresa", "famId")
FAMILY_IDENTITY = ("famNombre",)
FAMILY_NATURAL_KEYS = (("Empresa", "famNombre"),)
SUBFAMILY_KEYS = ("Empresa", "subId")
SUBFAMILY_IDENTITY = ("subNombre", "famId")
SUBFAMILY_NATURAL_KEYS = (("Empresa", "famId", "subNombre"),)
LOCATION_KEYS = ("Empresa", "ubiId")
LOCATION_IDENTITY = ("ubiNombre",)
LOCATION_NATURAL_KEYS = (("Empresa", "ubiNombre"),)

# Catálogos globales existentes: validar semántica, nunca sobrescribirlos.
REQUISITES = (
    ("articulos_ume", "umeId", 1, {"umeNombre": "UN", "umeDecimal": 0}),
    ("articulos_ume", "umeId", 2, {"umeNombre": "KG", "umeDecimal": 1}),
    ("t_sis_moneda", "ID_Moneda", 1, {"Codigo_Afip": "PES"}),
    ("t_sis_moneda", "ID_Moneda", 2, {"Codigo_Afip": "DOL"}),
    ("t_sis_iva", "ID_Iva", 1, {"PorcentajeIva": "0.00"}),
    ("t_sis_iva", "ID_Iva", 2, {"PorcentajeIva": "0.00"}),
    ("t_sis_iva", "ID_Iva", 3, {"PorcentajeIva": "0.00"}),
    ("t_sis_iva", "ID_Iva", 4, {"PorcentajeIva": "10.50"}),
    ("t_sis_iva", "ID_Iva", 5, {"PorcentajeIva": "21.00"}),
    ("t_sis_iva", "ID_Iva", 6, {"PorcentajeIva": "27.00"}),
)


def _number(value, scale):
    return format(Decimal(str(value)).quantize(Decimal(1).scaleb(-scale), rounding=ROUND_HALF_UP), "f")


def _audit(ctx):
    timestamp = ctx.reference_date.isoformat() + " 00:00:00"
    return {"fecha_insert": timestamp, "usuario_insert": "QA-SEED",
            "fecha_update": timestamp, "usuario_update": "QA-SEED"}


def article(ctx: SeedContext, id: int, code: str, name: str, price="1000.00", **overrides) -> dict:
    """Construye un artículo independiente; overrides expresan variantes explícitas.

    No incluye artStock: actualizar el catálogo no debe resetear el cache que
    modifica el ERP. La existencia inicial vive en movimientos_articulos.
    """
    row = {
        "Empresa": ctx.empresa, "artId": id, "artCodigo": code, "artNombre": name,
        "artDescripcion": "QA-SEED-DATO-SINTETICO", "artCodigoProveedor": "", "artMarca": "QA-SEED",
        "artFamilia": 980001, "artFamiliaNombre": "QA-SEED-FAMILIA",
        "artSubfamilia": 980001, "artSubfamiliaNombre": "QA-SEED-SUBFAMILIA",
        "artUbicacion": 980001, "artUbicacionNombre": "QA-SEED-UBICACION",
        "artProveedor": 980001, "artProveedorNombre": "QA-SEED-PROVEEDOR",
        "artPrecioVenta": _number(price, 2), "PrecioNeto": _number(price, 2),
        "artPrecioPorcentaje": "0.00", "artPrecioPorcentaje2": "0.00", "artPrecioVenta2": "0.00",
        "CantidadIva": "0.00", "CantidadItc": "0.00", "CantidadImpuestos": "0.00",
        "ImpuestoITC": "0.00", "ImpuestoITC2": "0.00", "Costo_Flete": "0.00", "porcentaje": "0.00",
        "artStockMinimo": "0.000", "artLoteHabitual": "0.000", "artPrecioBulto": "0.000",
        "artUme": 1, "ID_Iva": 3, "ID_Moneda": 1, "artEstado": 1, "artEstadoNombre": "STOCK OK",
        "activo": 1, "artStockeable": 1, "artContabilizable": 1,
        "artIngresoManual": 0, "artNombreManual": 0, "esPrecioCalculado": 0,
        "esPrecioCostoUniversal": 0, "EsPrecioCostoCalculado": 0,
        "esProductoConOpciones": 0, "esMateriaPrima": 0, "balanza": "",
        "esOtrosImpuestosPorcentaje": 0, "ID_TipoTributoOtrosImpuestos": 0,
        "esOtrosImpuestosPorcentaje2": 0, "ID_TipoTributoOtrosImpuestos2": 0,
        "Es_A_Cta_Orden_Proveedor": 0, "ID_Externo": "", "ID_TiendaNube": "", "ID_PedidosYa": "",
        "ID_TipoProducto": 1, "EsProductoConVariantes": 0,
        "ID_ProductoPadre": 0, "ID_Variante1": 0, "ID_Variante2": 0,
        "EsProductoConSubproductos": 0, "Configuracion": "{}", "ID_Sucursales": str(ctx.sucursal),
        **_audit(ctx),
    }
    row.update(overrides)
    if "artPrecioCosto" not in overrides:
        row["artPrecioCosto"] = _number(Decimal(row["PrecioNeto"]) / 2, 2)
    if "Ganancia" not in overrides:
        row["Ganancia"] = _number(Decimal(row["PrecioNeto"]) - Decimal(row["artPrecioCosto"]), 2)
    return row


def stock_row(ctx: SeedContext, id: int, article_id: int, quantity) -> dict:
    """Un movimiento inicial reservado y fijo; no consulta ni corrige el saldo."""
    amount = _number(quantity, 3)
    return {
        "Empresa": ctx.empresa, "Sucursal": ctx.sucursal, "Computadora": ctx.computadora,
        "moaId": id, "ID_ComputadoraModifica": 0,
        "moaFechaHora": ctx.reference_date.isoformat() + " 00:00:00",
        "moaUsuario": ctx.usuario_id, "moaUsuarioNombre": "QA-SEED-USUARIO",
        "moaArticuloCodigo": article_id, "moaArticuloNombre": f"QA-SEED-PRODUCTO-{article_id}",
        "moaStockActual": "0.000", "moaCantidad": amount, "moaStockFinal": amount,
        "moaNotas": f"QA-SEED-STOCK-{id}", "moaNumero": 0,
        "ID_Venta": 0, "ID_Compra": 0, "activo": 1, **_audit(ctx),
    }


def product_tables(ctx: SeedContext) -> list[SeedTable]:
    """Catálogo local 980001..980099; el catálogo de precios usa 980101..980199."""
    audit = _audit(ctx)
    result = [
        SeedTable("_familias", FAMILY_KEYS, FAMILY_IDENTITY,
                  [{"Empresa": ctx.empresa, "famId": 980001, "famNombre": "QA-SEED-FAMILIA",
                    "activo": 1, "orden": 980001, "EsParaCocina": 0, **audit}], FAMILY_NATURAL_KEYS),
        SeedTable("_subfamilias", SUBFAMILY_KEYS, SUBFAMILY_IDENTITY,
                  [{"Empresa": ctx.empresa, "subId": 980001, "famId": 980001,
                    "subNombre": "QA-SEED-SUBFAMILIA", "activo": 1, "orden": 980001, **audit}],
                  SUBFAMILY_NATURAL_KEYS),
        SeedTable("_ubicaciones", LOCATION_KEYS, LOCATION_IDENTITY,
                  [{"Empresa": ctx.empresa, "ubiId": 980001, "ubiNombre": "QA-SEED-UBICACION",
                    "activo": 1, **audit}], LOCATION_NATURAL_KEYS),
        SeedTable("_proveedores", ("Empresa", "proId"), ("proNombre",),
                  [{"Empresa": ctx.empresa, "proId": 980001, "proNombre": "QA-SEED-PROVEEDOR",
                    "activo": 1, **audit}], (("Empresa", "proNombre"),)),
    ]
    variants = [{"Empresa": ctx.empresa, "ID_Variante": id, "Nombre_Variante": name,
                 "ID_TipoVariante": kind, "activo": 1, **audit}
                for id, name, kind in [(980001, "QA-SEED-ROJO", 1), (980002, "QA-SEED-AZUL", 1),
                                       (980003, "QA-SEED-S", 2), (980004, "QA-SEED-M", 2)]]
    result.append(SeedTable("variantes", ("Empresa", "ID_Variante"),
                            ("Nombre_Variante", "ID_TipoVariante"), variants,
                            (("Empresa", "ID_TipoVariante", "Nombre_Variante"),)))

    products = []
    stock = []

    def add(id, suffix, price="1000.00", quantity="100.000", **overrides):
        code = "QA-SEED-" + suffix
        row = article(ctx, id, code, code, price, **overrides)
        products.append(row)
        if quantity is not None:
            movement = stock_row(ctx, id, id, quantity)
            movement["moaArticuloNombre"] = row["artNombre"]
            stock.append(movement)

    add(980001, "NORMAL")
    add(980002, "KG", "2000.00", "10.500", artUme=2)
    add(980003, "BULTO", quantity="120.000", artLoteHabitual="12.000", artPrecioBulto="10800.000")
    add(980004, "STOCK-CERO", quantity="0.000")
    add(980005, "STOCK-UNO", quantity="1.000")
    add(980006, "STOCK-NEGATIVO", quantity="-3.000")
    add(980007, "INACTIVO", quantity="10.000", activo=0)
    add(980008, "USD", "10.00", "20.000", ID_Moneda=2)
    add(980009, "REDONDEO", "10.01", "10.000", artUme=2)
    add(980010, "IVA105", "110.50", ID_Iva=4, PrecioNeto="100.00",
        CantidadIva="10.50")
    add(980011, "IVA21", "121.00", ID_Iva=5, PrecioNeto="100.00",
        CantidadIva="21.00")
    add(980012, "IVA27", "127.00", ID_Iva=6, PrecioNeto="100.00",
        CantidadIva="27.00")
    add(980013, "NO-GRAVADO", "100.00", ID_Iva=1)
    add(980014, "EXENTO", "100.00", ID_Iva=2)
    add(980015, "PADRE", quantity=None, EsProductoConVariantes=1, artStockeable=0)
    add(980016, "VAR-ROJO-S", quantity="10.000", ID_TipoProducto=2, ID_ProductoPadre=980015,
        ID_Variante1=980001, ID_Variante2=980003)
    add(980017, "VAR-AZUL-M", quantity="20.000", ID_TipoProducto=2, ID_ProductoPadre=980015,
        ID_Variante1=980002, ID_Variante2=980004)
    add(980018, "COMPUESTO", "1500.00", quantity=None, EsProductoConSubproductos=1, artStockeable=0)
    add(980019, "COMPONENTE-A", "500.00")
    add(980020, "COMPONENTE-B", "250.00")
    add(980021, "MATERIA-PRIMA", "1000.00", "30.000", esMateriaPrima=1, artUme=2)
    add(980022, "RECETA", "2500.00", quantity=None, EsProductoConSubproductos=1, artStockeable=0)
    add(980023, "CARNICERIA", "8000.00", "15.000", ID_TipoProducto=3, artUme=2)
    add(980024, "SERVICIO", "500.00", quantity=None, artStockeable=0)
    add(980025, "OPCIONES", "2500.00", quantity=None, artStockeable=0, esProductoConOpciones=1)
    result.append(SeedTable("articulos", ARTICLE_KEYS, ARTICLE_IDENTITY, products, ARTICLE_NATURAL_KEYS))

    components = [{"Empresa": ctx.empresa, "prhId": id, "prhProducto": parent,
                   "prhProductoHijo": child, "prhCantidad": quantity, "prhPrecioUnitario": price,
                   "activo": 1, **audit}
                  for id, parent, child, quantity, price in [
                      (980001, 980018, 980019, "2.000", "500.00"),
                      (980002, 980018, 980020, "2.000", "250.00"),
                      (980003, 980022, 980021, "0.250", "1000.00"),
                  ]]
    result.append(SeedTable("productos_hijos", ("Empresa", "prhId"),
                            ("prhProducto", "prhProductoHijo"), components,
                            (("Empresa", "prhProducto", "prhProductoHijo"),)))
    options = [{"Empresa": ctx.empresa, "ID_ProductoOpcion": id, "ID_Producto": 980025,
                "Opcion": name, "Cantidad": quantity, "ID_MateriaPrimaOrigen": 980021,
                "activo": 1, "Orden": position, **audit}
               for position, (id, name, quantity) in enumerate([
                   (980001, "QA-SEED-PORCION-NORMAL", "0.100"),
                   (980002, "QA-SEED-PORCION-DOBLE", "0.200"),
               ], start=1)]
    result.append(SeedTable("productos_opciones", ("Empresa", "ID_ProductoOpcion"),
                            ("ID_Producto", "Opcion", "ID_MateriaPrimaOrigen"), options,
                            (("Empresa", "ID_Producto", "Opcion"),)))
    result.append(SeedTable("movimientos_articulos", STOCK_KEYS, STOCK_IDENTITY, stock))
    return result
