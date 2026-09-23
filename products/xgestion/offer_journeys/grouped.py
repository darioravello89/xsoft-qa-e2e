"""Agrupación ON/OFF: canastas y repartos esperados, independientes del ERP."""
from .model import Journey, Line, Offer, Product, Step, Variant

_FORMULAS = (("%", "10", 0, "0"), ("$", "150", 0, "0"), ("C", "0", 3, "2"),
             ("C%", "0", 2, "50"), ("LXO+%", "0", 2, "10"),
             ("LXO+$", "0", 2, "150"), ("LXO+$CU", "0", 2, "800"))
# Descuentos TOTALES: A1, A1+B1, A2+B1, A2.
_ON = {
    "%": (("100",), ("100", "100"), ("200", "100"), ("200",)),
    "$": (("150",), ("150", "150"), ("300", "150"), ("300",)),
    "C%": (("0",), ("250", "250"), ("333.33", "166.67"), ("500",)),
    "LXO+%": (("0",), ("100", "100"), ("200", "100"), ("200",)),
    "LXO+$": (("0",), ("150", "150"), ("300", "150"), ("300",)),
    "LXO+$CU": (("0",), ("200", "200"), ("400", "200"), ("400",)),
}
_OFF = {
    "%": (("100", "100"), ("200", "100")), "$": (("150", "150"), ("300", "150")),
    "C%": (("0", "0"), ("500", "0")), "LXO+%": (("0", "0"), ("200", "0")),
    "LXO+$": (("0", "0"), ("300", "0")), "LXO+$CU": (("0", "0"), ("400", "0")),
}


def _variant(number, scope, formula, index):
    base = 981000 + number * 100 + index * 10
    kind, discount, minimum, pay = formula
    grouped = index != 1
    refs = ("A", "B", "C", "E") if kind == "C" else ("A", "B", "E")
    prices = {"A": "1000.00", "B": "2000.00" if index == 2 else "1000.00",
              "C": "3000.00" if index == 2 else "1000.00", "E": "1000.00"}
    brand = f"QA-PRM-{number:03}-V{index}-MARCA"

    def product(ref):
        offset = {"A": 1, "B": 2, "C": 3, "E": 9}[ref]
        # Solo el alcance declarado puede formar el conjunto A/B/C sin incluir E.
        # Las demás clasificaciones separan incluidos o comparten el ajeno.
        if scope == 2:
            family, subfamily = (base + 9 if ref == "E" else base), base + offset
            product_brand = brand
        elif scope == 3:
            family, subfamily = base, (base + 9 if ref == "E" else base)
            product_brand = f"{brand}-{'A' if ref == 'E' else ref}"
        elif scope == 5:
            family = subfamily = base + (1 if ref == "E" else offset)
            product_brand = f"{brand}-AJENA" if ref == "E" else brand
        else:
            raise ValueError("Solo familia, subfamilia o marca admiten estas canastas agrupadas.")
        return Product(ref, base + offset, f"QA-PRM-{number:03}-V{index}-{ref}",
                       price=prices[ref], family=family, subfamily=subfamily, sector=base, brand=product_brand)

    products = tuple(product(ref) for ref in refs)
    offer = Offer(base, f"QA-PRM-{number:03}-V{index}", scope, brand if scope == 5 else base,
                  kind, discount=discount, minimum=minimum, pay=pay, grouped=grouped)

    def basket(refs, quantities, discounts):
        return tuple(Line(ref, qty, disc, offer.id if disc != "0" else 0, prices[ref])
                     for ref, qty, disc in zip(refs, quantities, discounts, strict=True))

    def step(action, expected, product="", value=""):
        return Step(action, product, value, expected)

    excluded = basket(("E",), ("1",), ("0",))
    if kind != "C":
        one, pair, mixed, double = _ON[kind]
        if not grouped:
            pair, mixed = _OFF[kind]
        one = basket(("A",), ("1",), one)
        pair = basket(("A", "B"), ("1", "1"), pair)
        mixed = basket(("A", "B"), ("2", "1"), mixed)
        double = basket(("A",), ("2",), double)
        if grouped:
            steps = (Step("open"), step("add", one, "A", "1"),
                     step("add", one + excluded, "E", "1"), step("remove", one, "E"),
                     step("add", pair, "B", "1"), step("edit", mixed, "A", "2"),
                     step("remove", double, "B"), step("edit", one, "A", "1"), Step("abandon"),
                     Step("open"), step("add", one, "A", "1"), step("add", pair, "B", "1"),
                     step("cancel_payment", pair), step("pay", pair))
        else:
            steps = (Step("open"), step("add", one, "A", "1"), step("add", pair, "B", "1"),
                     step("edit", mixed, "A", "2"), Step("abandon"))
    else:
        one = basket(("A",), ("1",), ("0",))
        pair = basket(("A", "B"), ("1", "1"), ("0", "0"))
        triple = basket(("A", "B", "C"), ("1", "1", "1"),
                        ("333.33", "333.33", "333.34") if index == 0 else
                        ("333.33", "666.67", "1000") if index == 2 else ("0", "0", "0"))
        if index == 0:
            four = basket(("A", "B", "C"), ("2", "1", "1"), ("500", "250", "250"))
            mixed = basket(("A", "B"), ("2", "1"), ("666.67", "333.33"))
            steps = (Step("open"), step("add", one, "A", "1"),
                     step("add", one + excluded, "E", "1"),
                     step("add", one + excluded + pair[1:], "B", "1"), step("remove", pair, "E"),
                     step("add", triple, "C", "1"), step("edit", four, "A", "2"),
                     step("remove", mixed, "C"), step("edit", pair, "A", "1"), Step("abandon"),
                     Step("open"), step("add", one, "A", "1"), step("add", pair, "B", "1"),
                     step("add", triple, "C", "1"), step("cancel_payment", triple), step("pay", triple))
        elif index == 1:
            independent = basket(("A", "B", "C"), ("3", "1", "1"), ("1000", "0", "0"))
            steps = (Step("open"), step("add", one, "A", "1"), step("add", pair, "B", "1"),
                     step("add", triple, "C", "1"), step("edit", independent, "A", "3"), Step("abandon"))
        else:
            steps = (Step("open"), step("add", one, "A", "1"), step("add", pair, "B", "1"),
                     step("add", triple, "C", "1"), step("remove", pair, "C"),
                     step("add", triple, "C", "1"), Step("abandon"))
    name = ("agrupacion-on", "agrupacion-off", "precios-distintos")[index]
    return Variant(name, products, (offer,), steps)


CASES = {f"XG-PRM-{first + offset:03}": Journey(
    f"XG-PRM-{first + offset:03}",
    tuple(_variant(first + offset, scope, formula, i) for i in range(3 if formula[0] == "C" else 2)),
    notes=("Reparto manual con ajuste de centavos en la última línea.",
           "Los productos comparten o separan clasificaciones alternativas para detectar un alcance incorrecto.",
           "Validación sobre el JAR pendiente."),
) for first, scope in ((39, 2), (46, 3), (53, 5)) for offset, formula in enumerate(_FORMULAS)}

