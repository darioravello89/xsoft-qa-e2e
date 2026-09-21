"""Contrato privado de datos y localizadores; ningún selector se supone verificado."""

import hashlib
import json
from datetime import datetime
from decimal import Decimal, InvalidOperation

from framework.errors import QAError

REQUIRED_ELEMENTS = (
    "login.user", "login.password", "login.submit", "login.error", "login.error_ok",
    "main.company", "main.branch", "main.user", "menu.products", "menu.products_list",
    "products.search", "products.search_button", "products.known_result", "products.empty_result",
    "menu.sales", "menu.new_sale", "sale.quantity", "sale.code", "sale.total",
    "sale.document", "sale.non_fiscal_option", "sale.close", "sale.cancel",
    "sale.cancel_confirm", "sale.closed_indicator", "payment.cash_option",
    "payment.cash_accept", "payment.amount", "payment.confirm",
)
JOURNEY_ELEMENTS = (
    "sale.lines", "sale.customer", "sale.price_list", "sale.unknown_notice",
    "payment.total", "payment.change", "payment.cancel",
    "sale.cancel_reject", "editor.product", "editor.quantity", "editor.save",
)


def validate_elements(locators, aliases):
    try:
        windows = locators["windows"]
        elements = locators["elements"]
        for alias in aliases:
            entry = elements.get(alias, {})
            title = windows.get(entry.get("window"))
            query = entry.get("query")
            if not isinstance(title, str) or not title.strip() or not isinstance(query, str) or not query.strip():
                raise QAError(f"Falta locator semántico y ventana verificada: {alias}")
            if "CALIBRAR" in query.upper() or "CALIBRAR" in title.upper():
                raise QAError(f"El locator {alias} sigue siendo una plantilla sin calibrar.")
            if "index" in entry:
                raise QAError(f"El locator {alias} debe identificar un único elemento, sin índice arbitrario.")
    except (KeyError, TypeError, AttributeError):
        raise QAError("Mapa de localizadores con estructura inválida.") from None


def validate_journeys(fixtures, locators):
    """La calibración de los primeros siete casos no habilita los controles nuevos."""
    try:
        features = locators["calibration"].get("verified_features", [])
        if not isinstance(features, list) or "ventas-etapa1" not in features:
            raise ValueError()
        profile = fixtures["sales_journeys"]
        if (profile["schema_version"] != 1 or profile["currency"] != "ARS"
                or profile["cash_dialog"] is not True or profile["abandon_requires_supervisor"] is not False
                or profile["unknown_notice"] not in ("status", "dialog")
                or type(profile["repeated_product_rows"]) is not int or profile["repeated_product_rows"] not in (1, 2)):
            raise ValueError()
        for value in [profile["unknown_notice_text"], *(profile["defaults"][key]
                       for key in ("customer", "price_list", "document"))]:
            if not isinstance(value, str) or not value.strip() or "CALIBRAR" in value.upper():
                raise ValueError()
        table = locators["elements"]["sale.lines"]
        count = table["column_count"]
        columns = [table["columns"][name] for name in ("code", "name", "quantity", "unit_price", "total")]
        if (type(count) is not int or not 5 <= count <= 30 or len(set(columns)) != 5
                or any(type(column) is not int or not 0 <= column < count for column in columns)):
            raise ValueError()
    except (KeyError, TypeError, ValueError, AttributeError):
        raise QAError("Falta perfil/calibración completa ventas-etapa1: revisar sales_journeys, "
                      "defaults, columnas JAB y calibration.verified_features. Ver docs/calibracion.md.") from None
    aliases = JOURNEY_ELEMENTS + (("sale.unknown_dismiss",) if profile["unknown_notice"] == "dialog" else ())
    validate_elements(locators, aliases)


def file_sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path):
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
        if not isinstance(value, dict):
            raise ValueError()
        return value
    except (OSError, ValueError):
        raise QAError(f"Archivo JSON privado inválido o ausente: {path.name}") from None


def validate_fixtures(data):
    def require(condition):
        if not condition:
            raise ValueError()

    try:
        require(data["schema_version"] == 1)
        for key in ("empresa", "sucursal", "computadora", "usuario_id"):
            require(type(data["context"][key]) is int and data["context"][key] > 0)
        for key in ("empresa_label", "sucursal_label", "usuario_label"):
            require(isinstance(data["context"][key], str) and data["context"][key].strip())
        product = data["product"]
        require(type(product["id"]) is int and product["id"] > 0)
        require(type(product["quantity"]) is int and product["quantity"] == 2)
        require(Decimal(str(product["unit_price"])) == Decimal("1000.00"))
        for key in ("code", "name"):
            require(isinstance(product[key], str) and product[key].strip())
        require(isinstance(data["nonexistent_product_code"], str))
        require(data["nonexistent_product_code"].strip())
        require(data["nonexistent_product_code"] != product["code"])
        require(type(data["sale"]["cash_payment_id"]) is int and data["sale"]["cash_payment_id"] > 0)
        require(isinstance(data["ui"]["products_empty_text"], str) and data["ui"]["products_empty_text"].strip())
    except (KeyError, TypeError, ValueError, InvalidOperation):
        raise QAError("fixtures.json no cumple el contrato v1 de contexto y producto 2 × 1000 ARS.") from None
    # Constantes.TipoComprobante.presupuesto=99, cerrado vía Cobrar (sin F9).
    if data.get("sale", {}).get("non_fiscal_document_id") != 99:
        raise QAError("La suite v1 exige comprobante no fiscal interno 99; nunca emitir factura.")


def load_assets(profile):
    fixtures = read_json(profile.asset("fixtures"))
    validate_fixtures(fixtures)
    locators = read_json(profile.asset("locators"))
    calibration = locators.get("calibration", {})
    if locators.get("schema_version") != 1 or calibration.get("status") != "verified":
        raise QAError("Falta calibración JAB verificada. Seguir products/xgestion/docs/calibracion.md.")
    try:
        if not calibration["verified_by"].strip() or not calibration["jab_version"].strip():
            raise ValueError()
        datetime.fromisoformat(calibration["verified_at"].replace("Z", "+00:00"))
    except (KeyError, TypeError, ValueError, AttributeError):
        raise QAError("Falta evidencia de calibración (persona, fecha y versión JAB).") from None
    if calibration.get("app_sha256", "").lower() != file_sha256(profile.asset("app")):
        raise QAError("SHA256 del JAR distinto del utilizado para calibrar locators.json.")
    validate_elements(locators, REQUIRED_ELEMENTS)
    features = calibration.get("verified_features", [])
    if not isinstance(features, list):
        raise QAError("calibration.verified_features debe ser una lista de extensiones verificadas.")
    if "ventas-etapa1" in features:
        validate_journeys(fixtures, locators)
    return fixtures, locators
