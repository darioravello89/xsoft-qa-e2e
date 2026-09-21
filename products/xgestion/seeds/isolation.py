"""Reject baseline relationships that could change the public seed expectations.

Source f342381: OfertaLineaService, OfertaComboService, ListaPrecioDetalle,
Articulo.getProductoPorCodigo and ProductoHijo.getProductosHijosVentaDetalle.
Existing rows are never disabled or deleted to make this catalog fit.
"""

import json

from framework.errors import QAError
from products.xgestion.seeds.engine import query


def placeholders(values):
    return ",".join("%s" for _ in values)


def check_isolation(connection, context, tables):
    owned = {table.name: table for table in tables}
    articles = owned["articulos"].rows
    product_ids = [row["artId"] for row in articles]
    codes = [row["artCodigo"] for row in articles]
    components = sorted({row["prhProductoHijo"] for row in owned["productos_hijos"].rows})
    if query(connection, "SELECT artId FROM articulos WHERE Empresa<>%s "
             f"AND artId IN ({placeholders(components)}) LIMIT 1 FOR UPDATE", (context.empresa, *components)):
        raise QAError("ID de composición repetido en otra empresa; los joins heredados requieren un baseline aislado.")
    references, values = [], []
    for field in ("artFamilia", "artSubfamilia", "artUbicacion", "artMarca", "ID_ProductoPadre"):
        targets = (product_ids if field == "ID_ProductoPadre" else sorted({row[field] for row in articles}))
        references.append(f"`{field}` IN ({placeholders(targets)})")
        values.extend(targets)
    if query(connection, "SELECT artId FROM articulos WHERE Empresa=%s "
             f"AND artId NOT IN ({placeholders(product_ids)}) AND ({' OR '.join(references)}) LIMIT 1 FOR UPDATE",
             (context.empresa, *product_ids, *values)):
        raise QAError("Producto ajeno referencia categorías, marca o padres del seed; revisar el baseline.")
    aliases = query(connection, "SELECT TABLE_NAME FROM information_schema.TABLES "
                    "WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME='producto_codigo'")
    if aliases and query(connection, "SELECT ID_ProductoCodigo FROM producto_codigo WHERE Empresa=%s "
                        f"AND Codigo IN ({placeholders(codes)}) LIMIT 1 FOR UPDATE", (context.empresa, *codes)):
        raise QAError("Un código QA-SEED ya existe como código alternativo; revisar el baseline.")

    # Parent composition reads include inactive rows; one legacy read even omits
    # Empresa. Check every tenant for extras instead of concealing that ERP risk.
    for name, parent in (("productos_hijos", "prhProducto"), ("productos_opciones", "ID_Producto"),
                         ("t_fin_listapreciodetalle", "ID_Producto"),
                         ("t_fin_listapreciodetalle", "ID_ListaPrecio")):
        table = owned[name]
        keys = {tuple(str(row[key]) for key in table.keys) for row in table.rows}
        target_ids = ([row["ID_ListaPrecio"] for row in owned["t_fin_listaprecio"].rows]
                      if parent == "ID_ListaPrecio" else product_ids)
        tenant_filter = "" if name == "productos_hijos" else "Empresa=%s AND "
        parameters = tuple(target_ids) if not tenant_filter else (context.empresa, *target_ids)
        existing = query(connection, f"SELECT * FROM `{name}` WHERE {tenant_filter}"
                         f"`{parent}` IN ({placeholders(target_ids)}) FOR UPDATE", parameters)
        if any(tuple(str(row[key]) for key in table.keys) not in keys for row in existing):
            raise QAError(f"Relación ajena al catálogo en {name}; no se puede garantizar el escenario.")

    offers = owned["ofertas"].rows
    offer_ids = [row["ofeId"] for row in offers]
    # SQL performs text matching using the effective column collation, as ERP
    # does. Do not approximate code/brand equivalence with Python case folding.
    scopes, values = [], []
    for kind, field in ((1, "artUbicacion"), (2, "artFamilia"), (3, "artSubfamilia"),
                        (4, "artId"), (5, "artMarca")):
        codes = sorted({str(row[field]) for row in articles})
        scopes.append(f"(ofeTipo=%s AND ofeCodigo IN ({placeholders(codes)}))")
        values.extend((kind, *codes))
    base = ("SELECT ofeId,ofeTipo,Configuracion FROM ofertas WHERE Empresa=%s AND activo=1 "
            "AND CURDATE() BETWEEN ofeDesde AND ofeHasta "
            f"AND ofeId NOT IN ({placeholders(offer_ids)}) ")
    branch = "(FIND_IN_SET('0',Sucursal)>0 OR FIND_IN_SET(%s,Sucursal)>0)"
    parameters = (context.empresa, *offer_ids, str(context.sucursal), *values)
    if query(connection, base + f"AND {branch} AND ({' OR '.join(scopes)}) FOR UPDATE", parameters):
        raise QAError("Oferta ajena vigente alcanza productos del seed; revisar el baseline sin desactivarla.")
    combos = query(connection, base + f"AND ofeTipo=6 AND ({branch} OR Sucursal IS NULL OR Sucursal='') "
                   "FOR UPDATE", (context.empresa, *offer_ids, str(context.sucursal)))
    for combo in combos:
        try:
            data = json.loads(combo["Configuracion"] or "{}")
            components = data["combo"]["productos"]
            overlaps = any(int(item["idProducto"]) in product_ids for item in components)
        except (ValueError, TypeError, KeyError, AttributeError):
            raise QAError("Oferta combo ajena con configuración no verificable; revisar el baseline.") from None
        if overlaps:
            raise QAError("Oferta combo ajena alcanza productos del seed; revisar el baseline sin desactivarla.")
