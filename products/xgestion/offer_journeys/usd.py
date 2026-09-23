"""Calibración y evidencia monetaria P0; nunca normaliza el resultado del ERP."""

import re
from decimal import Decimal

from framework.errors import QAError
from framework.events import business_step, diagnostic
from products.xgestion.contracts import has_verified_feature, validate_elements
from products.xgestion.library import BusinessMismatch, parse_ars, parse_payment, parse_quantity

from .currencies import FEATURE

PAYMENT_CURRENCIES = ("payment.total_currency", "payment.amount_currency", "payment.change_currency")
PROFILE = {"schema_version": 1, "product_currency": "USD", "row_currency": "USD",
           "document_currency": "ARS", "payment_currency": "ARS", "exchange_rate": "1500.00"}
SALE_COLUMNS = ("ID_Moneda", "Cotizacion_USD", "ID_Moneda_Pago", "Pagado_Original",
                "ID_Moneda_Vuelto", "Vuelto_Original")
LINE_COLUMNS = ("ID_Moneda", "vecPrecioOriginal", "vecTotalOriginal", "vecOfertaOriginal",
                "vecOfertaManualOriginal", "vecImporteIvaOriginal", "vecOtrosImpuestosOriginal")


def validate_profile(fixtures, locators):
    profile = fixtures.get("offer_usd")
    if (not has_verified_feature(locators, FEATURE) or not isinstance(profile, dict)
            or type(profile.get("schema_version")) is not int
            or any(profile.get(key) != value for key, value in PROFILE.items())):
        raise QAError("Falta calibración ofertas-usd-v1: productos/renglones USD, documento/cobro ARS "
                      "y cotización 1500 ARS/USD. Ver docs/ofertas-usd.md del producto.")
    validate_elements(locators, ("sale.usd_rate", *PAYMENT_CURRENCIES))


def money(text):
    # Sólo devolver tokens/valores monetarios conocidos, nunca texto privado de UI.
    match = re.fullmatch(r"\s*(USD|ARS|\$)\s*(-?[\d.,]+)\s*", text)
    if not match:
        raise BusinessMismatch("Formato monetario visible", "Moneda e importe calibrados",
                               "[VALOR NO MONETARIO OMITIDO]")
    currency = "ARS" if match[1] == "$" else match[1]
    return currency, parse_ars(match[2], private=True)


def assert_money(text, amount, currency, label, *, equivalent=None):
    observed_currency, observed = money(text)
    if observed_currency != currency or observed != amount:
        expected = f"{currency} {amount}"
        if equivalent is not None:
            expected = f"USD {equivalent} equivalentes a {expected}; cotización 1500 ARS/USD"
        raise BusinessMismatch(label, expected, f"{observed_currency} {observed}")
    return observed


def check_rate(library):
    try:
        rate = parse_payment(library.driver.text("sale.usd_rate"))
    except AssertionError:
        raise QAError("No se pudo verificar la cotización visible: calibrar ofertas-usd-v1.") from None
    if rate != Decimal(library.variant.exchange_rate):
        raise QAError("Perfil incompatible: la cotización visible debe ser 1500 ARS/USD; "
                      "preparar el paquete QA y repetir. No se modifica durante la prueba.")
    diagnostic("Cotización comprobada", rate_ars_per_usd=str(rate))


def assert_basket(library, expected):
    columns = library.driver.locators["elements"]["sale.lines"]["columns"]
    products = {p.ref: p for p in library.variant.products}
    total = sum((line.total for line in expected), Decimal(0))
    original_total = sum((Decimal(line.original_price) * Decimal(line.quantity)
                          - Decimal(line.original_discount) for line in expected), Decimal(0))
    business_step(f"Comprobar oferta: USD {original_total} equivalentes a ARS {total}, cotización 1500")

    def check():
        check_rate(library)
        rows = library.driver.table_rows("sale.lines")
        count = library.driver.locators["elements"]["sale.lines"]["column_count"]
        if any(len(row) != count for row in rows):
            raise QAError("La grilla USD no coincide con las columnas JAB calibradas.")
        observed_total = assert_money(library.driver.text("sale.total"), total, "ARS",
                                      "Comprobar total antes de cobrar", equivalent=original_total)
        library._equal(len(rows), len(expected), "Cantidad de renglones USD")
        for line in expected:
            product = products[line.product]
            matches = [row for row in rows if row[columns["code"]] == product.code]
            library._equal(len(matches), 1, f"Renglón único de {product.code}")
            row = matches[0]
            library._equal(row[columns["name"]] == product.code, True, "Nombre del producto esperado")
            library._equal(parse_quantity(row[columns["quantity"]]), Decimal(line.quantity),
                           f"Cantidad de {product.code}")
            price, discount = Decimal(line.original_price), Decimal(line.original_discount)
            gross = price * Decimal(line.quantity)
            for field, amount, label in (("unit_price", price, "Precio unitario"),
                                         ("gross_total", gross, "Bruto"),
                                         ("offer_discount", discount, "Descuento"),
                                         ("total", gross - discount, "Neto")):
                assert_money(row[columns[field]], amount, "USD", f"{product.code}: {label} USD")
        return tuple(tuple(row) for row in rows), observed_total

    return library._wait_check(check)


def check_payment_currencies(library):
    for alias in PAYMENT_CURRENCIES:
        if library.driver.text(alias).strip() != "ARS":
            raise QAError("El cobro USD requiere total, recibido y vuelto en ARS. "
                          "Revisar los selectores del perfil; no confirmar el cobro.")
    diagnostic("Monedas de total, recibido y vuelto comprobadas: ARS")
