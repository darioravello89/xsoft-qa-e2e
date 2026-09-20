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
    windows = locators.get("windows", {})
    elements = locators.get("elements", {})
    for alias in REQUIRED_ELEMENTS:
        entry = elements.get(alias, {})
        title = windows.get(entry.get("window"))
        query = entry.get("query")
        if not isinstance(title, str) or not title.strip() or not isinstance(query, str) or not query.strip():
            raise QAError(f"Falta locator semántico y ventana verificada: {alias}")
        if "CALIBRAR" in query.upper() or "CALIBRAR" in title.upper():
            raise QAError(f"El locator {alias} sigue siendo una plantilla sin calibrar.")
        if "index" in entry:
            raise QAError(f"El locator {alias} debe identificar un único elemento, sin índice arbitrario.")
    return fixtures, locators
