"""Casos que requieren restaurar datos y reiniciar con cada configuración."""
from .model import Journey, Line, Offer, Product, Step, Variant


def _active():
    products = (Product("A", 988001, "QA-PRM-070-A"), Product("B", 988002, "QA-PRM-070-CONTROL"))
    control = Offer(988001, "QA-PRM-070-CONTROL", 4, 988002, "%", discount="10")
    variants = []
    for name in ("active", "inactive", "active-again"):
        offer = Offer(988000, "QA-PRM-070", 4, 988001, "%", discount="10", active=name != "inactive")
        one = (Line("A", "1", "0" if name == "inactive" else "100", 0 if name == "inactive" else offer.id),)
        steps = [Step("open"), Step("add", "B", "1", (Line("B", "1", "100", control.id),)),
                 Step("abandon"), Step("open"), Step("add", "A", "1", one)]
        if name == "active-again":
            two = (Line("A", "2", "200", offer.id),)
            steps += [Step("add", "A", "1", two), Step("cancel_payment", expected=two), Step("pay", expected=two)]
        else:
            steps.append(Step("abandon"))
        variants.append(Variant(name, products, (offer, control), tuple(steps)))
    return Journey("XG-PRM-070", tuple(variants))


def _manual():
    products = tuple(Product(ref, 988900 + i, f"QA-PRM-079-{ref}", family=988900, subfamily=988900)
                     for i, ref in enumerate(("A", "B"), 1))
    offer = Offer(988900, "QA-PRM-079", 2, 988900, "%", discount="10", grouped=True)
    initial = (Line("A", "1", "100", offer.id), Line("B", "1", "100", offer.id))
    changed = (Line("A", "1", "90", offer.id, manual="100"), initial[1])
    variants = []
    for name in ("general-off", "offers-off", "allowed-warning-on", "allowed-warning-off"):
        allowed = name.startswith("allowed")
        steps = [Step("open"), Step("add", "A", "1", initial[:1]), Step("add", "B", "1", initial),
                 Step("manual" if allowed else "manual_blocked", "A", "100", changed if allowed else initial)]
        steps += ([Step("cancel_payment", expected=changed), Step("pay", expected=changed)]
                  if allowed else [Step("abandon")])
        requirements = ("manual-discount", "warning-on" if name.endswith("-on") else "warning-off") if allowed else ()
        variants.append(Variant(name, products, (offer,), tuple(steps), requirements=requirements))
    return Journey("XG-PRM-079", tuple(variants))


CASES = {"XG-PRM-070": _active(), "XG-PRM-079": _manual()}

