"""Expectativas del primer lote: ejemplos fijos, sin replicar calculadores del ERP."""

from dataclasses import dataclass
from decimal import Decimal

from framework.errors import QAError
from products.xgestion.contracts import KEYBOARD_FEATURE, has_verified_feature, validate_journeys

FEATURE = "promociones-v1"
SEED = "catalogo-comercial-v1"


@dataclass(frozen=True)
class PromotionCase:
    seed_id: str
    product_id: int
    code: str
    initial_quantity: int
    initial_total: Decimal
    quantity: int
    total: Decimal

    def product(self):
        return {"id": self.product_id, "code": self.code, "name": self.code,
                "quantity": self.quantity, "unit_price": "1000.00"}

    def expected(self, quantity):
        if quantity == self.initial_quantity:
            total = self.initial_total
        elif quantity == self.quantity:
            total = self.total
        else:
            raise QAError("Cantidad fuera del ejemplo comercial documentado.")
        discount = Decimal(quantity) * 1000 - total
        return {"total": total, "offer_discount": discount,
                "offer_id": self.product_id if discount else 0}


CASES = {case.seed_id: case for case in (
    PromotionCase("PCT-Q3", 980101, "QA-SEED-PCT", 1, Decimal(900), 3, Decimal(2700)),
    PromotionCase("IMP-Q3", 980102, "QA-SEED-IMP", 1, Decimal(850), 3, Decimal(2550)),
    PromotionCase("2X1-Q3", 980103, "QA-SEED-2X1", 1, Decimal(1000), 3, Decimal(2000)),
    PromotionCase("2DA50-Q3", 980104, "QA-SEED-2DA50", 1, Decimal(1000), 3, Decimal(2500)),
    PromotionCase("EXPIRADA", 980110, "QA-SEED-EXPIRADA", 2, Decimal(2000), 1, Decimal(1000)),
    PromotionCase("FUTURA", 980111, "QA-SEED-FUTURA", 2, Decimal(2000), 1, Decimal(1000)),
    PromotionCase("INACTIVA", 980112, "QA-SEED-INACTIVA", 2, Decimal(2000), 1, Decimal(1000)),
)}


def validate_promotions(fixtures, locators):
    validate_journeys(fixtures, locators)
    try:
        profile = fixtures["promotions"]
        columns = locators["elements"]["sale.lines"]["columns"]
        count = locators["elements"]["sale.lines"]["column_count"]
        selected = [columns[key] for key in ("code", "name", "quantity", "unit_price", "total",
                                              "gross_total", "offer_discount")]
        if (not has_verified_feature(locators, FEATURE) or not has_verified_feature(locators, KEYBOARD_FEATURE)
                or type(profile["schema_version"]) is not int or profile["schema_version"] != 1
                or profile["currency"] != "ARS" or type(profile["price_list_id"]) is not int
                or profile["price_list_id"] != 0 or profile["other_discounts"] is not False
                or profile["loyalty"] is not False or profile["customer_and_shift_lists"] is not False
                or profile["price_list_text"] != "Ninguna Lista"
                or fixtures["sales_journeys"]["defaults"]["price_list"] != profile["price_list_text"]
                or len(set(selected)) != 7
                or any(type(column) is not int or not 0 <= column < count for column in selected)):
            raise ValueError()
    except (KeyError, TypeError, ValueError):
        raise QAError("Falta perfil/calibración promociones-v1: ARS, Ninguna Lista, sin otros descuentos, "
                      "teclado y columnas separadas de bruto, oferta y neto. "
                      "Ver products/xgestion/docs/promociones.md.") from None
