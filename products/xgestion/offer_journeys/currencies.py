"""P0: precio final USD 50; importes esperados literales, sin calculadores del ERP."""

from .model import Journey, Line, Offer, Product, Step, Variant

FEATURE = "ofertas-usd-v1"
SOURCE_COMMIT = "39d6b6d64b12205fbabe29222f72679e875f7031"


def _variant(number, scope, index):
    base = 981000 + number * 100 + index * 10
    prefix = f"QA-PRM-{number:03}-V{index}"
    grouped, minimum = index == 2, 1 if index == 0 else 2
    products = []
    for ref, offset in (("A", 1), ("B", 2), ("E", 9)):
        if ref == "B" and scope == 4:
            continue
        # Alternar las demás clasificaciones evita que un alcance erróneo pase.
        family = base + (9 if ref == "E" else 0) if scope == 2 else base
        subfamily = base + offset if scope == 2 else base + (9 if ref == "E" else 0)
        brand = f"{prefix}-{'AJENA' if ref == 'E' else 'MARCA'}"
        sector = base + (9 if ref == "E" else 0)
        if scope in {1, 5}:
            family = subfamily = base + (1 if ref == "E" else offset)
        if scope != 5:
            brand = f"{prefix}-MARCA-{1 if ref == 'E' else offset}"
        if scope != 1:
            sector = base + (1 if ref == "E" else offset)
        products.append(Product(ref, base + offset, f"{prefix}-{ref}", "100.00",
                                family, subfamily, sector, brand, currency="USD"))
    a = products[0]
    target = {1: a.sector, 2: a.family, 3: a.subfamily, 4: a.id, 5: a.brand}[scope]
    offer = Offer(base, prefix, scope, target, "LXO+$CU", minimum=minimum, pay="50.00", grouped=grouped)

    def line(ref, quantity, discount):
        original = {"0": "0.00", "75000": "50.00", "150000": "100.00"}[discount]
        return Line(ref, quantity, discount, offer.id if discount != "0" else 0,
                    price="150000.00", original_price="100.00", original_discount=original)

    single_discount = "75000" if minimum == 1 else "0"
    one = (line("A", "1", single_discount),)
    double = (line("A", "2", "150000"),)
    excluded = (line("E", "1", "0"),)
    steps = [Step("open"), Step("add", "A", "1", one), Step("edit", "A", "2", double),
             Step("edit", "A", "1", one), Step("add", "E", "1", one + excluded),
             Step("remove", "E", expected=one)]
    if scope != 4:
        pair_discount = "75000" if minimum == 1 or grouped else "0"
        pair = (line("A", "1", pair_discount), line("B", "1", pair_discount))
        steps.append(Step("add", "B", "1", pair))
        if minimum == 2:
            mixed = (line("A", "2", "150000"), line("B", "1", pair_discount))
            steps.extend((Step("edit", "A", "2", mixed), Step("edit", "A", "1", pair)))
        steps.append(Step("remove", "B", expected=one))
    final = one
    if minimum == 2:
        steps.append(Step("edit", "A", "2", double))
        final = double
    steps.extend((Step("cancel_payment", expected=final), Step("pay", expected=final)))
    name = ("desde-una-unidad", "desde-dos-sin-agrupar", "desde-dos-agrupadas")[index]
    return Variant(name, tuple(products), (offer,), tuple(steps), exchange_rate="1500.00")


CASES = {f"XG-PRM-{number:03}": Journey(
    f"XG-PRM-{number:03}", tuple(_variant(number, scope, i) for i in range(3 if scope in {2, 3, 5} else 2)),
    source_commit=SOURCE_COMMIT,
    notes=("P0: USD 100 con precio final USD 50; no reemplazar Paga=50 por 75000 en el seed.",
           "Cotización 1500 ARS/USD. Renglones USD, documento interno y cobro ARS, IVA 0 %.",
           "Un fallo o bloqueo mantiene pendiente la aceptación del circuito de ofertas."),
) for number, scope in ((80, 4), (81, 2), (82, 3), (83, 5), (84, 1))}
