"""Datos exactos de recorridos; no contiene reglas de cálculo de promociones."""

from dataclasses import dataclass, field
from decimal import Decimal

PAYMENT_METHODS = {
    "cash": (989901, "QA-PRM-EFECTIVO"),
    "transfer": (989902, "QA-PRM-TRANSFERENCIA"),
    "card": (989903, "QA-PRM-TARJETA"),
}


@dataclass(frozen=True)
class Product:
    ref: str
    id: int
    code: str
    price: str = "1000.00"
    family: int = 980001
    subfamily: int = 980001
    sector: int = 980001
    brand: str = "QA-SEED"
    unit: int = 1
    currency: str = "ARS"


@dataclass(frozen=True)
class Offer:
    id: int
    name: str
    scope: int
    target: int | str
    formula: str
    discount: str = "0"
    minimum: int = 0
    pay: str = "0"
    grouped: bool = False
    active: bool = True
    start_days: int = -365
    end_days: int = 365
    components: tuple[tuple[int, str], ...] = ()
    payment_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class Line:
    product: str
    quantity: str
    discount: str = "0"
    offer_id: int = 0
    price: str = "1000.00"
    manual: str = "0"
    price_list_id: int = 0
    original_price: str | None = None
    original_discount: str | None = None

    @property
    def gross(self):
        return Decimal(self.quantity) * Decimal(self.price)

    @property
    def total(self):
        return self.gross - Decimal(self.discount) - Decimal(self.manual)


@dataclass(frozen=True)
class Step:
    action: str
    product: str = ""
    value: str = ""
    expected: tuple[Line, ...] = ()


@dataclass(frozen=True)
class PriceList:
    ref: str
    id: int
    name: str
    prices: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class Variant:
    name: str
    products: tuple[Product, ...]
    offers: tuple[Offer, ...]
    steps: tuple[Step, ...]
    requirements: tuple[str, ...] = ()
    price_lists: tuple[PriceList, ...] = ()
    exchange_rate: str | None = None


@dataclass(frozen=True)
class Journey:
    id: str
    variants: tuple[Variant, ...]
    source_commit: str = "4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a"
    notes: tuple[str, ...] = field(default=())
