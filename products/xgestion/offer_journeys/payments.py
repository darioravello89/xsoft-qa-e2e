"""Medios internos QA: todos, uno, varios habilitados y cambio antes del cobro."""
from .model import Journey, Line, Offer, Product, Step, Variant


def _variant(number, index, medium):
    base = 981000 + number * 100 + index * 10
    products = (Product("A", base + 1, f"QA-PRM-{number:03}-V{index}-A"),)
    refs = () if number == 73 else ("cash", "transfer") if number == 75 else ("cash",)
    offers = (Offer(base, f"QA-PRM-{number:03}-V{index}", 4, base + 1, "%",
                    discount="10", payment_refs=refs),)

    def lines(quantity, enabled):
        return (Line("A", str(quantity), {1: "100", 2: "200"}[quantity] if enabled else "0",
                     base if enabled else 0),)

    applies = not refs or medium in refs
    one, two = lines(1, applies), lines(2, applies)
    steps = [Step("open"), Step("payment_method", value=medium),
             Step("add", "A", "1", one), Step("add", "A", "1", two)]
    if number == 74:
        steps += [Step("abandon"), Step("open"), Step("payment_method", value=medium),
                  Step("add", "A", "2", two), Step("edit", "A", "1", one),
                  Step("cancel_payment", expected=one), Step("pay", expected=one)]
        # Control positivo independiente en el mismo medio.
        control = Product("B", base + 2, f"QA-PRM-074-V{index}-CONTROL")
        products += (control,)
        offers += (Offer(base + 1, f"QA-PRM-074-V{index}-TODOS", 4, control.id, "%", discount="10"),)
        steps += [Step("open"), Step("payment_method", value=medium),
                  Step("add", "B", "1", (Line("B", "1", "100", base + 1),)), Step("abandon")]
    elif number == 76:
        card, cash = lines(2, False), lines(2, True)
        steps += [Step("payment_method", value="card", expected=card),
                  Step("payment_method", value="cash", expected=cash),
                  Step("cancel_payment", expected=cash),
                  Step("payment_method", value="card", expected=card),
                  Step("cancel_payment", expected=card),
                  Step("payment_method", value="cash", expected=cash), Step("pay", expected=cash)]
    else:
        steps += [Step("cancel_payment", expected=two), Step("pay", expected=two)]
    return Variant(medium, products, offers, tuple(steps), requirements=("manual-payments",))


CASES = {f"XG-PRM-{number:03}": Journey(
    f"XG-PRM-{number:03}", tuple(_variant(number, index, medium) for index, medium in enumerate(media)),
    notes=("Medios propios del seed, tipo Cobrado, sin red ni porcentajes adicionales.",
           "Cobro simple: el movimiento financiero conserva el ID del medio elegido."),
) for number, media in ((73, ("cash", "transfer", "card")), (74, ("cash", "card")),
                         (75, ("cash", "transfer", "card")), (76, ("cash",)))}

