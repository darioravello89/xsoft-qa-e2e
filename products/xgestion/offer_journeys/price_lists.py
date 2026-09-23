"""Listas manuales activas en ARS; los precios esperados son datos fijos."""

from products.xgestion.offer_journeys.model import Journey, Line, Offer, PriceList, Product, Step, Variant


def _selected_before_loading():
    base = 988100
    product = Product("A", base + 1, "QA-PRM-071-PRODUCTO")
    offer = Offer(base, "QA-PRM-071-OFERTA", 4, product.id, "%", "10")
    lists = (PriceList("QA-A", base, "QA-PRM-071-LISTA-A", (("A", "750"),)),
             PriceList("QA-B", base + 1, "QA-PRM-071-LISTA-B", (("A", "1200"),)))
    normal = (Line("A", "1", "100", base),)
    list_a = (Line("A", "1", "75", base, price="750", price_list_id=base),)
    list_b = (Line("A", "2", "240", base, price="1200", price_list_id=base + 1),)
    steps = (Step("open"), Step("add", "A", "1", normal), Step("abandon"),
             Step("open"), Step("price_list", value="QA-A"),
             Step("add", "A", "1", list_a), Step("abandon"),
             Step("open"), Step("price_list", value="QA-B"),
             Step("add", "A", "2", list_b), Step("cancel_payment", expected=list_b), Step("pay", expected=list_b))
    return Journey("XG-PRM-071", (Variant("precio-segun-lista", (product,), (offer,), steps,
                                         requirements=("manual-price-list",), price_lists=lists),))


def _change_open_sale():
    base = 988200
    product = Product("A", base + 1, "QA-PRM-072-PRODUCTO")
    offer = Offer(base, "QA-PRM-072-OFERTA", 4, product.id, "%", "10")
    lists = (PriceList("QA-A", base, "QA-PRM-072-LISTA-A", (("A", "750"),)),
             PriceList("QA-SIN-A", base + 1, "QA-PRM-072-LISTA-SIN-A"))
    normal = (Line("A", "2", "200", base),)
    selected = (Line("A", "2", "150", base, price="750", price_list_id=base),)
    steps = (Step("open"), Step("add", "A", "2", normal),
             Step("price_list", value="QA-A", expected=selected),
             Step("price_list", value="QA-SIN-A", expected=normal),
             Step("price_list", value="QA-A", expected=selected),
             Step("cancel_payment", expected=selected), Step("pay", expected=selected),
             Step("open"), Step("add", "A", "1", (Line("A", "1", "100", base),)), Step("abandon"))
    return Journey("XG-PRM-072", (Variant("cambiar-lista-con-productos", (product,), (offer,), steps,
                                         requirements=("manual-price-list", "recalculate-price-list"),
                                         price_lists=lists),))


CASES = {journey.id: journey for journey in (_selected_before_loading(), _change_open_sale())}

