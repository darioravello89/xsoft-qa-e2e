"""Capacidades calibradas por JAR; un ejemplo draft nunca habilita una pantalla."""

from framework.errors import QAError
from products.xgestion.contracts import has_verified_feature, validate_elements
from products.xgestion.offer_journeys.usd import validate_profile

COMMON = ("sale.usd_rate", "sale.lines")
PURCHASE = ("menu.purchases", "menu.receipt", "purchase.provider", "purchase.provider_option",
            "purchase.document", "purchase.paid", "purchase.code", "purchase.name", "purchase.quantity",
            "purchase.cost", "purchase.discount", "purchase.add", "purchase.lines", "purchase.total",
            "purchase.rate", "purchase.stock", "purchase.update_price", "purchase.bonus_price",
            "purchase.confirm", "purchase.reject", "purchase.accept", "purchase.supplier_debt")
TURN = ("menu.shift", "shift.user", "shift.password", "shift.confirm", "fund.cancel",
        "menu.cash_report", "cash.turn", "cash.computer", "cash.income", "cash.expense",
        "cash.cash", "cash.credit", "cash.debit", "cash.other", "cash.total")


def validate_table(locators, alias, names):
    try:
        table = locators["elements"][alias]
        count = table["column_count"]
        columns = [table["columns"][key] for key in names]
        if (type(count) is not int or not len(names) <= count <= 30 or len(set(columns)) != len(names)
                or any(type(c) is not int or not 0 <= c < count for c in columns)):
            raise ValueError()
    except (KeyError, TypeError, ValueError):
        raise QAError(f"Falta calibrar las columnas accesibles de {alias}.") from None


def validate(fixtures, locators, config, case):
    validate_profile(fixtures, locators)
    profile = fixtures.get("circuits", {})
    if (not has_verified_feature(locators, "circuitos-comerciales-v1")
            or not isinstance(profile, dict)
            or type(profile.get("schema_version")) is not int or profile["schema_version"] != 1
            or profile.get("operator_role") != "administrator"
            or fixtures.get("sale", {}).get("cash_payment_id") != 1):
        raise QAError("Falta perfil circuitos-comerciales-v1: operador administrador y efectivo ARS ID 1.")
    required = {"venta.convertirProductosUsdAPesos": "false", "pedirPagoAlCerrarTicket": "true"}
    aliases = COMMON
    feature = None
    validate_table(locators, "sale.lines", ("code", "name", "quantity", "unit_price", "total",
                                           "gross_total", "offer_discount"))
    if case == "XG-FIN-013":
        aliases += PURCHASE
        feature = "remitos-circuito-v1"
        validate_table(locators, "purchase.lines", ("code", "name", "quantity", "unit_price", "total"))
    if case == "XG-FIN-014":
        aliases += TURN
        feature = "caja-circuito-v1"
        required.update({"venta.habilitarCierreAperturaTurno": "true", "venta.habilitarCierreCiego": "false",
                         "ventas.cerrarSistemaConCierreDeTurno": "false"})
        label = profile.get("cash_computer_label")
        if not isinstance(label, str) or not label.strip() or "CALIBRAR" in label.upper():
            raise QAError("Calibrar la identidad visible del puesto para el cierre de caja.")
    if feature and not has_verified_feature(locators, feature):
        raise QAError(f"Falta calibrar {feature} para este JAR.")
    validate_elements(locators, aliases)
    for key, value in required.items():
        if config.get(key, "").lower() != value:
            raise QAError(f"Perfil incompatible: preparar {key}={value} en el paquete de circuitos.")
