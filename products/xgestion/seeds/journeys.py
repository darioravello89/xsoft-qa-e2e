"""Datos públicos de recorridos; toda aplicación conserva el motor y sus guards."""

import json
from collections.abc import Mapping
from dataclasses import replace
from datetime import timedelta
from decimal import Decimal, InvalidOperation

from framework.errors import QAError
from products.xgestion.seeds.model import SeedContext, SeedTable
from products.xgestion.seeds.pricing import _detail, _offer
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

JOURNEY_SOURCE_COMMIT = "4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a"
_DEFAULT_CATEGORY = 980001
_SCOPE_NAMES = {1: "Sector", 2: "Familia", 3: "Subfamilia", 4: "Producto", 5: "Marca", 6: "Combo"}
_PROFILE_NAMES = {
    "XG-PRM-070": {"active", "inactive", "active-again"},
    "XG-PRM-079": {"general-off", "offers-off", "allowed-warning-on", "allowed-warning-off"},
}
_TABLES = (
    ("_familias", FAMILY_KEYS, FAMILY_IDENTITY, FAMILY_NATURAL_KEYS),
    ("_subfamilias", SUBFAMILY_KEYS, SUBFAMILY_IDENTITY, SUBFAMILY_NATURAL_KEYS),
    ("_ubicaciones", LOCATION_KEYS, LOCATION_IDENTITY, LOCATION_NATURAL_KEYS),
    ("articulos", ARTICLE_KEYS, ARTICLE_IDENTITY, ARTICLE_NATURAL_KEYS),
    ("movimientos_articulos", STOCK_KEYS, STOCK_IDENTITY, ()),
    ("_pagos", ("Empresa", "pagId"), ("pagNombre",), (("Empresa", "pagNombre"),)),
    ("ofertas", ("Empresa", "ofeId"), ("ofeNombre",), ()),
    ("t_fin_listaprecio", ("Empresa", "Sucursal", "ID_ListaPrecio"), ("Nombre_ListaPrecio",),
     (("Empresa", "ID_ListaPrecio"), ("Empresa", "Nombre_ListaPrecio"))),
    ("t_fin_listapreciodetalle", ("Empresa", "Sucursal", "ID_ListaPrecioDetalle"),
     ("ID_ListaPrecio", "ID_Producto", "Codigo_Proveedor"), ()),
)


def _quantity(value):
    try:
        amount = Decimal(value)
        if not amount.is_finite() or amount <= 0:
            raise ValueError
        # JSON requires a number; ensure its representation retains the declared value.
        number = int(amount) if amount == amount.to_integral_value() else float(amount)
        if Decimal(str(number)) != amount:
            raise ValueError
        return number
    except (ValueError, TypeError, InvalidOperation, OverflowError):
        raise QAError("La cantidad de combo debe ser positiva, finita y representable exactamente.") from None


def _selected_variants(journey, profile):
    if journey.id != "XG-PRM-070":
        return journey.variants
    variants = {variant.name: variant for variant in journey.variants}
    if len(variants) != 3 or set(variants) != _PROFILE_NAMES["XG-PRM-070"]:
        raise QAError("El perfil 070 requiere active, inactive y active-again sin duplicados.")
    baseline = variants["active"]
    toggled = {offer.id for offer in variants["inactive"].offers if offer.active is False}
    if len(toggled) != 1 or any(offer.active is not True for offer in baseline.offers):
        raise QAError("El perfil 070 debe alternar una sola oferta y conservar los controles activos.")
    for name, variant in variants.items():
        normalized = tuple(replace(offer, active=True) for offer in variant.offers)
        if (variant.products != baseline.products or variant.price_lists != baseline.price_lists
                or normalized != baseline.offers
                or any(offer.active is not (name != "inactive" or offer.id not in toggled)
                       for offer in variant.offers)):
            raise QAError("El perfil 070 solo puede cambiar la activación de las mismas ofertas y productos.")
    return (variants[profile[1] if profile and profile[0] == journey.id else "active"],)


def build_journey_tables(ctx: SeedContext, journeys, *, journey_profile=None) -> list[SeedTable]:
    """Deduplicar identidades iguales y rechazar reglas incompatibles antes de SQL."""
    from products.xgestion.offer_journeys.model import PAYMENT_METHODS

    items = tuple(journeys.values() if isinstance(journeys, Mapping) else journeys)
    if journey_profile is not None:
        if (type(journey_profile) is not tuple or len(journey_profile) != 2
                or any(type(value) is not str for value in journey_profile)
                or journey_profile[0] not in _PROFILE_NAMES
                or journey_profile[1] not in _PROFILE_NAMES[journey_profile[0]]):
            raise QAError("Perfil de seed de recorridos desconocido o inválido.")
        matches = [item for item in items if item.id == journey_profile[0]]
        if len(matches) != 1 or journey_profile[1] not in {item.name for item in matches[0].variants}:
            raise QAError("El perfil solicitado no corresponde al catálogo de recorridos.")

    rows = {name: {} for name, *_ in _TABLES}
    natural_owners = {name: {} for name, *_ in _TABLES}
    specs = {name: (keys, natural) for name, keys, _, natural in _TABLES}

    def add(table, row):
        keys, natural = specs[table]
        key = tuple(row[field] for field in keys)
        previous = rows[table].get(key)
        if previous is not None:
            if previous != row:
                raise QAError(f"Definiciones incompatibles en {table}, clave {key}.")
            return
        for fields in natural:
            identity = (fields, tuple(row[field] for field in fields))
            owner = natural_owners[table].get(identity)
            if owner is not None and owner != key:
                raise QAError(f"Identidad natural repetida en el catálogo de {table}.")
            natural_owners[table][identity] = key
        rows[table][key] = row

    def add_product(product):
        if product.currency not in {"ARS", "USD"}:
            raise QAError("Moneda de producto no soportada por el seed.")
        fields = {"artFamilia": product.family, "artSubfamilia": product.subfamily,
                  "artUbicacion": product.sector, "artMarca": product.brand, "artUme": product.unit,
                  "ID_Moneda": {"ARS": 1, "USD": 2}[product.currency]}
        if product.family != _DEFAULT_CATEGORY:
            name = f"QA-PRM-FAMILIA-{product.family}"
            add("_familias", {"Empresa": ctx.empresa, "famId": product.family, "famNombre": name, "activo": 1})
            fields["artFamiliaNombre"] = name
        if product.subfamily != _DEFAULT_CATEGORY:
            name = f"QA-PRM-SUBFAMILIA-{product.subfamily}"
            add("_subfamilias", {"Empresa": ctx.empresa, "subId": product.subfamily, "subNombre": name,
                                  "famId": product.family, "activo": 1})
            fields["artSubfamiliaNombre"] = name
        elif product.family != _DEFAULT_CATEGORY:
            raise QAError("Una familia nueva no puede reasignar la subfamilia base 980001.")
        if product.sector != _DEFAULT_CATEGORY:
            name = f"QA-PRM-SECTOR-{product.sector}"
            add("_ubicaciones", {"Empresa": ctx.empresa, "ubiId": product.sector, "ubiNombre": name, "activo": 1})
            fields["artUbicacionNombre"] = name
        add("articulos", article(ctx, product.id, product.code, product.code, price=product.price, **fields))
        movement = stock_row(ctx, product.id, product.id, "100.000")
        movement["moaArticuloNombre"] = product.code
        add("movimientos_articulos", movement)

    timestamp = ctx.reference_date.isoformat() + " 00:00:00"
    for order, (identifier, name) in enumerate(PAYMENT_METHODS.values(), start=1):
        add("_pagos", {"Empresa": ctx.empresa, "Empresa_Nombre": "QA-SEED-EMPRESA", "pagId": identifier,
                       "pagNombre": name, "pagPorcentajeDescuento": "0.00", "activo": 1,
                       "fecha_insert": timestamp, "usuario_insert": "QA-SEED", "fecha_update": timestamp,
                       "usuario_update": "QA-SEED", "fecha_sync": None, "ID_TipoPago": 1,
                       "pagComisionMedioPago": "0.00", "Orden": order,
                       "ID_PedidosYa": "", "ID_TiendaNube": "", "Configuracion": "{}"})

    for journey in items:
        for variant in _selected_variants(journey, journey_profile):
            by_ref = {product.ref: product for product in variant.products}
            by_id = {product.id: product for product in variant.products}
            if len(by_ref) != len(variant.products) or len(by_id) != len(variant.products):
                raise QAError(f"Productos repetidos en {journey.id}/{variant.name}.")
            for product in variant.products:
                add_product(product)
            for offer in variant.offers:
                if offer.scope not in _SCOPE_NAMES or offer.grouped and offer.scope not in {2, 3, 5}:
                    raise QAError("Alcance o agrupación de oferta no soportados.")
                if (offer.scope == 6) != (offer.formula == "COMBO"):
                    raise QAError("Alcance Combo y fórmula COMBO deben coincidir.")
                config = {"agrupada": True} if offer.grouped else {}
                if offer.formula == "COMBO":
                    components, ids = [], set()
                    for product_id, quantity in offer.components:
                        if type(product_id) is not int:
                            raise QAError("Los componentes de combo requieren IDs enteros.")
                        if product_id not in by_id or product_id in ids:
                            raise QAError("Componente de combo desconocido o repetido.")
                        ids.add(product_id)
                        components.append({"idProducto": product_id, "cantidad": _quantity(quantity)})
                    if not components:
                        raise QAError("Una oferta COMBO necesita componentes.")
                    config["combo"] = {"version": 1, "productos": components}
                elif offer.components:
                    raise QAError("Solo COMBO puede declarar componentes.")
                refs = offer.payment_refs
                if len(set(refs)) != len(refs) or any(ref not in PAYMENT_METHODS for ref in refs):
                    raise QAError("Referencia de medio de pago desconocida o repetida en una oferta.")
                payment_ids = [PAYMENT_METHODS[ref][0] for ref in refs]
                payment_id = payment_ids[0] if len(payment_ids) == 1 else 0
                if len(payment_ids) > 1:
                    payment_id = -1
                    config["tiposCobro"] = {"version": 1, "ids": payment_ids}
                add("ofertas", _offer(
                    ctx, offer.id, offer.name, offer.target, formula=offer.formula,
                    discount=offer.discount, minimum=offer.minimum, pay=offer.pay,
                    ofeNombre=offer.name, ofeTipo=offer.scope, ofeTipoNombre=_SCOPE_NAMES[offer.scope],
                    ofeCodigo=str(offer.target), ofeCodigoNombre=offer.name, ID_Pago=payment_id,
                    ofeDesde=(ctx.reference_date + timedelta(days=offer.start_days)).isoformat(),
                    ofeHasta=(ctx.reference_date + timedelta(days=offer.end_days)).isoformat(),
                    Configuracion=json.dumps(config, ensure_ascii=False, separators=(",", ":")), activo=int(offer.active),
                ))
            for price_list in variant.price_lists:
                if len(price_list.prices) > 1:
                    raise QAError("Este catálogo reserva como máximo un detalle por lista de precio.")
                add("t_fin_listaprecio", {"Empresa": ctx.empresa, "Sucursal": 0, "ID_ListaPrecio": price_list.id,
                                         "ID_Proveedor": 980001, "Nombre_ListaPrecio": price_list.name, "activo": 1,
                                         "usuario_insert": "QA-SEED", "usuario_update": "QA-SEED"})
                if price_list.prices:
                    ref, price = price_list.prices[0]
                    if ref not in by_ref:
                        raise QAError(f"Producto de lista desconocido en {journey.id}/{variant.name}.")
                    add("t_fin_listapreciodetalle", _detail(ctx, price_list.id, price_list.id, by_ref[ref].id, price))
    return [SeedTable(name, keys, identity, [rows[name][key] for key in sorted(rows[name])], natural_keys=natural)
            for name, keys, identity, natural in _TABLES if rows[name]]
