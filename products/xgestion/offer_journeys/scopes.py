"""Recorridos por producto y clasificación, con importes esperados fijos."""
from .model import Journey, Line, Offer, Product, Step, Variant

_FORMULAS = (
    ("%", "10", 0, "0", ("100", "200", "300", "400")),
    ("$", "150", 0, "0", ("150", "300", "450", "600")),
    ("C", "0", 2, "1", ("0", "1000", "1000", "2000")),
    ("C%", "0", 2, "50", ("0", "500", "500", "1000")),
    ("LXO+%", "0", 2, "10", ("0", "200", "300", "400")),
    ("LXO+$", "0", 2, "150", ("0", "300", "450", "600")),
    ("LXO+$CU", "0", 2, "800", ("0", "400", "600", "800")),
)


def _scope_products(number, scope):
    base = 981000 + number * 100
    code = f"QA-PRM-{number:03}"
    if scope == 4:
        return (Product("A", base + 1, f"{code}-A"),
                Product("E", base + 9, f"{code}-E")), base + 1
    if scope == 2:
        return (
            Product("A", base + 1, f"{code}-A", family=base, subfamily=base + 1),
            Product("B", base + 2, f"{code}-B", family=base, subfamily=base + 2),
            Product("E", base + 9, f"{code}-E"),
        ), base
    if scope == 3:
        return (
            Product("A", base + 1, f"{code}-A", family=base, subfamily=base),
            Product("B", base + 2, f"{code}-B", family=base, subfamily=base),
            Product("E", base + 9, f"{code}-E", family=base, subfamily=base + 9),
        ), base
    if scope == 5:
        brand = f"{code}-MARCA"
        return (
            Product("A", base + 1, f"{code}-A", family=base, subfamily=base, brand=brand),
            Product("B", base + 2, f"{code}-B", family=base + 1, subfamily=base + 1, brand=brand),
            Product("E", base + 9, f"{code}-E", family=base, subfamily=base, brand=f"{code}-OTRA-MARCA"),
        ), brand
    if scope == 1:
        return (
            Product("A", base + 1, f"{code}-A", family=base, subfamily=base, sector=base),
            Product("B", base + 2, f"{code}-B", family=base + 1, subfamily=base + 1, sector=base),
            Product("E", base + 9, f"{code}-E", family=base, subfamily=base, sector=base + 9),
        ), base
    raise ValueError("Alcance no contemplado en estos recorridos")


def _journey(number, scope, formula_index):
    base = 981000 + number * 100
    formula, discount, minimum, pay, expected_discounts = _FORMULAS[formula_index]
    products, target = _scope_products(number, scope)
    offer = Offer(base, f"QA-PRM-{number:03}", scope, target, formula,
                  discount=discount, minimum=minimum, pay=pay, grouped=False)
    quantities = {}
    steps = [Step("open")]

    def snapshot():
        return tuple(Line(ref, str(quantity),
                          "0" if ref == "E" else expected_discounts[quantity - 1],
                          0 if ref == "E" or expected_discounts[quantity - 1] == "0" else offer.id)
                     for ref, quantity in quantities.items())

    def change(action, ref, quantity):
        quantities[ref] = quantity
        steps.append(Step(action, ref, str(quantity), snapshot()))

    change("add", "E", 1)
    change("add", "A", 1)
    change("edit", "A", 2)
    change("edit", "A", 3)
    if formula in {"C", "C%"}:
        change("edit", "A", 4)
    change("edit", "A", 1)
    if scope != 4:
        change("add", "B", 1)
    change("edit", "A", 2)
    final = snapshot()
    steps.extend((Step("cancel_payment", expected=final), Step("pay", expected=final)))
    return Journey(f"XG-PRM-{number:03}",
                   (Variant("principal", products, (offer,), tuple(steps)),),
                   notes=("ARS, precio base 1000, stock suficiente y agrupación OFF.",
                          "El producto E conserva su precio sin oferta.",
                          "Cancelar cobro conserva la venta; confirmar cobra una sola vez."))


CASES = {f"XG-PRM-{number:03}": _journey(number, 4, number - 8 + 4) for number in range(8, 11)}
CASES.update({f"XG-PRM-{first + offset:03}": _journey(first + offset, scope, offset)
              for first, scope in ((11, 2), (18, 3), (25, 5), (32, 1)) for offset in range(7)})

