"""Contratos explícitos para recorridos de ofertas y su calibración privada."""

import re
from decimal import Decimal, InvalidOperation

from framework.errors import QAError
from products.xgestion.contracts import has_verified_feature, validate_elements
from products.xgestion.offer_journeys.model import PAYMENT_METHODS
from products.xgestion.promotions import validate_promotions

FEATURE = "promociones-canastas-v1"
ACTIONS = {"open", "add", "edit", "remove", "check", "cancel_payment", "pay", "abandon", "price_list",
           "payment_method", "manual", "manual_blocked"}


def _amount(value, *, positive=False):
    if not isinstance(value, str) or not re.fullmatch(r"\d+(?:\.\d{1,3})?", value):
        raise ValueError()
    result = Decimal(value)
    if not result.is_finite() or result < 0 or (positive and result == 0):
        raise ValueError()
    return result


def validate_journey(journey):
    try:
        if not re.fullmatch(r"XG-PRM-\d{3}", journey.id) or not journey.variants:
            raise ValueError()
        if len({variant.name for variant in journey.variants}) != len(journey.variants):
            raise ValueError()
        for variant in journey.variants:
            products = {product.ref: product for product in variant.products}
            offers = {offer.id for offer in variant.offers}
            if (not variant.name or not products or len(products) != len(variant.products)
                    or len({p.id for p in variant.products}) != len(products)
                    or len({p.code for p in variant.products}) != len(products)
                    or len(offers) != len(variant.offers) or not variant.steps):
                raise ValueError()
            for product in variant.products:
                if type(product.id) is not int or product.id <= 0 or not product.code.startswith("QA-"):
                    raise ValueError()
                _amount(product.price, positive=True)
                if product.currency not in {"ARS", "USD"}:
                    raise ValueError()
            usd = any(p.currency == "USD" for p in variant.products)
            if usd:
                if (variant.exchange_rate != "1500.00"
                        or any(p.currency != "USD" for p in variant.products) or variant.price_lists):
                    raise ValueError()
            elif variant.exchange_rate is not None:
                raise ValueError()
            for offer in variant.offers:
                if (len(set(offer.payment_refs)) != len(offer.payment_refs)
                        or not set(offer.payment_refs) <= PAYMENT_METHODS.keys()):
                    raise ValueError()
            lists = {item.ref: item for item in variant.price_lists}
            if (len(lists) != len(variant.price_lists)
                    or len({item.id for item in variant.price_lists}) != len(lists)):
                raise ValueError()
            for item in variant.price_lists:
                if type(item.id) is not int or item.id <= 0 or not item.name.startswith("QA-"):
                    raise ValueError()
                if len({ref for ref, price in item.prices}) != len(item.prices):
                    raise ValueError()
                for ref, price in item.prices:
                    if ref not in products:
                        raise ValueError()
                    _amount(price, positive=True)
            opened = False
            current = ()
            for step in variant.steps:
                if step.action not in ACTIONS:
                    raise ValueError()
                if step.action == "open":
                    if opened or step.expected:
                        raise ValueError()
                    opened, current = True, ()
                    continue
                if not opened:
                    raise ValueError()
                if step.action in {"add", "edit", "remove"} and step.product not in products:
                    raise ValueError()
                if step.action in {"add", "edit"}:
                    _amount(step.value, positive=True)
                if len({line.product for line in step.expected}) != len(step.expected):
                    raise ValueError()
                for line in step.expected:
                    if line.product not in products or type(line.offer_id) is not int:
                        raise ValueError()
                    if line.offer_id != 0 and line.offer_id not in offers:
                        raise ValueError()
                    if (type(line.price_list_id) is not int
                            or line.price_list_id not in {0, *(item.id for item in variant.price_lists)}):
                        raise ValueError()
                    _amount(line.quantity, positive=True)
                    _amount(line.price, positive=True)
                    _amount(line.discount)
                    _amount(line.manual)
                    if usd:
                        rate = _amount(variant.exchange_rate, positive=True)
                        if (_amount(line.original_price, positive=True) * rate != _amount(line.price)
                                or _amount(line.original_discount) * rate != _amount(line.discount)
                                or _amount(line.manual) != 0 or line.price_list_id != 0):
                            raise ValueError()
                    elif line.original_price is not None or line.original_discount is not None:
                        raise ValueError()
                    if line.total < 0:
                        raise ValueError()
                if step.action in {"add", "edit", "remove"}:
                    old = {line.product: Decimal(line.quantity) for line in current}
                    if step.action == "add":
                        old[step.product] = old.get(step.product, Decimal(0)) + Decimal(step.value)
                    elif step.product not in old:
                        raise ValueError()
                    elif step.action == "edit":
                        old[step.product] = Decimal(step.value)
                    else:
                        del old[step.product]
                    if old != {line.product: Decimal(line.quantity) for line in step.expected}:
                        raise ValueError()
                    current = step.expected
                elif step.action in {"price_list", "payment_method", "manual", "manual_blocked"}:
                    if step.action == "price_list" and step.value not in lists:
                        raise ValueError()
                    if step.action == "payment_method" and (step.value not in PAYMENT_METHODS
                            or "manual-payments" not in variant.requirements):
                        raise ValueError()
                    if step.action in {"manual", "manual_blocked"}:
                        _amount(step.value)
                        if step.product not in {line.product for line in current}:
                            raise ValueError()
                        if step.action == "manual_blocked" and step.expected != current:
                            raise ValueError()
                        if step.action == "manual" and next(line.manual for line in step.expected
                                                           if line.product == step.product) != step.value:
                            raise ValueError()
                    if step.action == "manual" and "manual-discount" not in variant.requirements:
                        raise ValueError()
                    if {line.product: line.quantity for line in current} != {
                            line.product: line.quantity for line in step.expected}:
                        raise ValueError()
                    current = step.expected
                elif step.action != "abandon" and step.expected != current:
                    raise ValueError()
                if step.action in {"pay", "cancel_payment"} and not current:
                    raise ValueError()
                if step.action in {"pay", "abandon"}:
                    opened, current = False, ()
            if opened:
                raise ValueError()
    except (AttributeError, KeyError, TypeError, ValueError, InvalidOperation):
        raise QAError("Recorrido de ofertas incompleto o incoherente: revisar productos, pasos y esperados fijos.") from None


def validate_calibration(fixtures, locators, variant):
    validate_promotions(fixtures, locators)
    if variant.exchange_rate is not None:
        from products.xgestion.offer_journeys.usd import validate_profile

        validate_profile(fixtures, locators)
    try:
        profile = fixtures["offer_journeys"]
        if (not has_verified_feature(locators, FEATURE)
                or type(profile["schema_version"]) is not int or profile["schema_version"] != 1
                or profile["item_removal_requires_supervisor"] is not False
                or fixtures["sales_journeys"]["repeated_product_rows"] != 1):
            raise ValueError()
    except (KeyError, TypeError, ValueError):
        raise QAError("Falta calibración promociones-canastas-v1: canastas por código único, "
                      "productos repetidos consolidados y eliminación sin supervisor.") from None
    if any(step.action == "remove" for step in variant.steps):
        validate_elements(locators, ("editor.remove",))


    if any(step.action in {"manual", "manual_blocked"} for step in variant.steps):
        if profile.get("manual_amount_mode") is not True:
            raise QAError("Calibrar el editor de descuento manual como importe total, sin porcentaje.")
        validate_elements(locators, ("editor.manual", "editor.manual_percent"))
    if {"warning-on", "warning-off"} & set(variant.requirements):
        try:
            observation = profile["manual_warning_observation"]
            duration = observation["duration_seconds"]
            minimum = observation["minimum_visible_seconds"]
            gap = observation["max_sample_gap_seconds"]
            if (observation["verified"] is not True
                    or any(type(value) not in {int, float} for value in (duration, minimum, gap))
                    or not 4 <= duration <= 10 or not 1 <= minimum <= 3 or not 0.25 <= gap < minimum):
                raise ValueError()
        except (KeyError, TypeError, ValueError):
            raise QAError("Falta calibrar observación continua del aviso manual: duración y visibilidad mínima.") from None
        validate_elements(locators, ("editor.manual_warning",))
    if any(step.action in {"pay", "cancel_payment"} for step in variant.steps):
        if profile.get("choose_payment_on_close") is not True:
            raise QAError("Calibrar la selección de medio al cerrar: pedirPagoAlCerrarTicket=true.")
        validate_elements(locators, ("payment.method", "payment_picker.lines", "payment_picker.search"))
        try:
            picker = locators["elements"]["payment_picker.lines"]
            columns = [picker["columns"][key] for key in ("id", "name", "discount")]
            if (type(picker["column_count"]) is not int or picker["column_count"] != 3
                    or len(set(columns)) != 3
                    or any(type(column) is not int or not 0 <= column < 3 for column in columns)):
                raise ValueError()
        except (KeyError, TypeError, ValueError):
            raise QAError("Calibrar identidad, nombre y descuento del selector de medios QA.") from None
    if "manual-payments" in variant.requirements:
        if profile.get("manual_payments_offline") is not True:
            raise QAError("Calibrar los tres medios QA manuales offline y su selector de cobro simple.")
        validate_elements(locators, ("sale.choose_payment", "sale.payment_method", "payment.method",
                                    "payment_picker.lines", "payment_picker.search"))
    if variant.price_lists:
        if profile.get("manual_price_list_enabled") is not True:
            raise QAError("El perfil debe habilitar la elección manual de listas.")
        if ("recalculate-price-list" in variant.requirements
                and profile.get("recalculate_price_list") is not True):
            raise QAError("El perfil debe recalcular productos al cambiar la lista de precios.")
        validate_elements(locators, ("sale.choose_price_list", "list_picker.lines", "list_picker.search"))
        try:
            table = locators["elements"]["list_picker.lines"]
            columns = [table["columns"][key] for key in ("id", "name")]
            if (type(table["column_count"]) is not int or table["column_count"] != 2
                    or len(set(columns)) != 2
                    or any(type(column) is not int or not 0 <= column < 2 for column in columns)):
                raise ValueError()
        except (KeyError, TypeError, ValueError):
            raise QAError("Faltan las columnas de identidad y nombre del selector de listas.") from None
