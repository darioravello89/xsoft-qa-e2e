"""Fronteras y condiciones comerciales con importes de referencia explícitos."""

from products.xgestion.offer_journeys.model import Journey, Line, Offer, Product, Step, Variant


def _finish(steps, lines):
    return (*steps, Step("cancel_payment", expected=lines), Step("pay", expected=lines))


def _fraction(case_number, minimum):
    variants = []
    specs = (("precio-final", "LXO+$CU", "0", "800"),
             ("porcentaje", "LXO+%", "0", "20"), ("importe", "LXO+$", "0", "200"))
    expected = (("0.500", "100"), ("0.001", "0.20"), ("1.500", "300"), ("0.500", "100"))
    if minimum:
        expected = (("0.500", "0"), ("0.999", "0"), ("1.000", "200"), ("1.500", "300"), ("0.500", "0"))
    for index, (name, formula, discount, pay) in enumerate(specs):
        base = 981000 + case_number * 100 + index * 10
        product = Product("A", base + 1, f"QA-PRM-{case_number}-{name.upper()}", unit=2)
        offer = Offer(base, f"QA-PRM-{case_number}-{name.upper()}", 4, product.id, formula,
                      discount, minimum, pay)
        steps = [Step("open")]
        for position, (quantity, amount) in enumerate(expected):
            lines = (Line("A", quantity, amount, base if amount != "0" else 0),)
            steps.append(Step("add" if position == 0 else "edit", "A", quantity, lines))
        variants.append(Variant(name, (product,), (offer,), _finish(steps, lines)))
    return Journey(f"XG-PRM-{case_number:03}", tuple(variants))


def _scope_priority():
    variants = []
    for index, grouped in enumerate((False, True)):
        base = 987700 + index * 10
        brand = f"QA-PRM-067-MARCA-{index}"
        products = tuple(
            Product(ref, base + offset, f"QA-PRM-067-{index}-{ref}", family=base if offset < 5 else base + 6,
                    subfamily=base if offset < 4 else base + offset,
                    sector=base, brand=brand if offset < 3 else f"QA-PRM-067-{index}-OTRA-{ref}")
            for offset, ref in enumerate("ABCDE", start=1))
        offers = (
            Offer(base, f"QA-PRM-067-{index}-PRODUCTO", 4, products[0].id, "%", "5"),
            Offer(base + 1, f"QA-PRM-067-{index}-MARCA", 5, brand, "%", "10", grouped=grouped),
            Offer(base + 2, f"QA-PRM-067-{index}-SUBFAMILIA", 3, base, "%", "15", grouped=grouped),
            Offer(base + 3, f"QA-PRM-067-{index}-FAMILIA", 2, base, "%", "20", grouped=grouped),
            Offer(base + 4, f"QA-PRM-067-{index}-SECTOR", 1, base, "%", "25"),
        )
        lines = tuple(Line(ref, "1", amount, base + index) for index, (ref, amount)
                      in enumerate(zip("ABCDE", ("50", "100", "150", "200", "250"), strict=True)))
        steps = [Step("open"), *(Step("add", ref, "1", lines[:index + 1]) for index, ref in enumerate("ABCDE"))]
        steps.extend((Step("edit", "A", "2", (Line("A", "2", "100", base), *lines[1:])),
                      Step("edit", "A", "1", lines)))
        variants.append(Variant("agrupacion-on" if grouped else "agrupacion-off", products, offers,
                                _finish(steps, lines)))
    return Journey("XG-PRM-067", tuple(variants))


def _quantity_priority():
    base = 987800
    product = Product("A", base + 1, "QA-PRM-068-PRIORIDAD")
    offers = (
        Offer(base, "QA-PRM-068-MIN2", 4, product.id, "LXO+$CU", minimum=2, pay="900", start_days=-30),
        Offer(base + 1, "QA-PRM-068-MIN3-ANTERIOR", 4, product.id, "LXO+$CU",
              minimum=3, pay="850", start_days=-20),
        Offer(base + 2, "QA-PRM-068-MIN3-RECIENTE", 4, product.id, "LXO+$CU",
              minimum=3, pay="800", start_days=-10),
    )
    expected = (("1", "0", 0), ("2", "200", base), ("3", "600", base + 2), ("4", "800", base + 2),
                ("2", "200", base), ("1", "0", 0), ("3", "600", base + 2))
    steps = [Step("open")]
    for index, (quantity, discount, offer_id) in enumerate(expected):
        lines = (Line("A", quantity, discount, offer_id),)
        steps.append(Step("add" if index == 0 else "edit", "A", quantity, lines))
    return Journey("XG-PRM-068", (Variant("cantidad-y-fecha", (product,), offers, _finish(steps, lines)),))


def _date_boundaries():
    base = 987900
    refs = ("CONTROL", "INICIO", "FIN", "ANTES", "DESPUES")
    products = tuple(Product(ref, base + index + 1, f"QA-PRM-069-{ref}") for index, ref in enumerate(refs))
    offers = tuple(Offer(base + index, f"QA-PRM-069-{ref}", 4, products[index].id, "%", "10",
                         start_days=start, end_days=end)
                   for index, (ref, (start, end)) in enumerate(zip(refs, ((-1, 1), (0, 1), (-1, 0),
                                                                         (1, 2), (-2, -1)), strict=True)))
    lines = tuple(Line(ref, "1", "100" if index < 3 else "0", base + index if index < 3 else 0)
                  for index, ref in enumerate(refs))
    steps = [Step("open"), *(Step("add", ref, "1", lines[:index + 1]) for index, ref in enumerate(refs))]
    steps.extend((Step("edit", "INICIO", "2", (lines[0], Line("INICIO", "2", "200", base + 1), *lines[2:])),
                  Step("edit", "INICIO", "1", lines)))
    return Journey("XG-PRM-069", (Variant("limites-inclusivos", products, offers, _finish(steps, lines)),))


CASES = {journey.id: journey for journey in (
    _fraction(65, 0), _fraction(66, 1), _scope_priority(), _quantity_priority(), _date_boundaries(),
)}

