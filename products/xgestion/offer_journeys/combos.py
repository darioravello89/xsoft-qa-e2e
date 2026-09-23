"""Combos060..064: canastas literales, sin reproducir el calculador del ERP."""

from .model import Journey, Line, Offer, Product, Step, Variant


def _products(number, variant_index, prices, *, weighted=()):
    base = 981000 + number * 100 + variant_index * 10
    suffixes = {"A": 1, "B": 2, "C": 3, "E": 9}
    products = tuple(Product(
        ref=ref, id=base + suffixes[ref], code=f"QA-PRM-{number:03}-V{variant_index}-{ref}",
        price=price, unit=2 if ref in weighted else 1,
    ) for ref, price in prices.items())
    return base, products


def _combo(offer_id, products, price, components):
    product_ids = {product.ref: product.id for product in products}
    return Offer(
        id=offer_id, name=f"QA-COMBO-{offer_id}", scope=6, target=0, formula="COMBO", pay=price,
        components=tuple((product_ids[ref], quantity) for ref, quantity in components),
    )


def _individual(offer_id, products):
    product_a = next(product for product in products if product.ref == "A")
    return Offer(id=offer_id, name=f"QA-SOBRANTE-{offer_id}", scope=4, target=product_a.id,
                 formula="%", discount="10")


def _variant(name, products, rules, instructions, *, requirements=()):
    prices = {product.ref: product.price for product in products}
    offer_ids = {key: offer.id for key, offer in rules.items()}
    steps = []
    for action, product, value, rows in instructions:
        # Fila: ref, cantidad, descuento automático TOTAL, regla y manual TOTAL opcional.
        expected = tuple(Line(
            product=ref, quantity=quantity, discount=discount,
            offer_id=offer_ids[rule] if rule else 0, price=prices[ref],
            manual=manual[0] if manual else "0",
        ) for ref, quantity, discount, rule, *manual in rows)
        steps.append(Step(action, product, value, expected))
    return Variant(name=name, products=products, offers=tuple(rules.values()),
                   steps=tuple(steps), requirements=requirements)


def _simple_assets(number, variant_index, combo_price="1500.00"):
    base, products = _products(number, variant_index,
                               {"A": "1000.00", "B": "1000.00", "E": "1000.00"})
    rules = {
        "combo": _combo(base, products, combo_price, (("A", "1"), ("B", "1"))),
        "individual": _individual(base + 1, products),
    }
    return products, rules


def _case_060():
    products, rules = _simple_assets(60, 0)
    individual_a = (("A", "1", "100", "individual"),)
    complete = (("A", "1", "250", "combo"), ("B", "1", "250", "combo"))
    base_variant = _variant("completar-quitar-retomar", products, rules, (
        ("open", "", "", ()),
        ("add", "A", "1", individual_a),
        ("add", "E", "1", individual_a + (("E", "1", "0", ""),)),
        ("add", "B", "1", (("A", "1", "250", "combo"), ("E", "1", "0", ""),
                            ("B", "1", "250", "combo"))),
        ("remove", "E", "", complete),
        ("remove", "B", "", individual_a),
        ("add", "B", "1", complete),
        ("abandon", "", "", ()),
        ("open", "", "", ()),
        ("add", "A", "1", individual_a),
        ("add", "B", "1", complete),
        ("cancel_payment", "", "", complete),
        ("pay", "", "", complete),
    ))
    no_saving = []
    for variant_index, price, name in (
        (1, "2000.00", "combo-sin-ahorro"), (2, "2100.00", "combo-mas-caro"),
    ):
        products, rules = _simple_assets(60, variant_index, price)
        # El combo no aplica; A conserva su oferta individual del10%.
        expected = (("A", "1", "100", "individual"), ("B", "1", "0", ""))
        no_saving.append(_variant(name, products, rules, (
            ("open", "", "", ()),
            ("add", "A", "1", individual_a),
            ("add", "B", "1", expected),
            ("abandon", "", "", ()),
        )))
    return Journey("XG-PRM-060", (base_variant, *no_saving), notes=(
        "A incompleto cuesta 900 por su oferta individual; completo, 1500 sin duplicar beneficio.",
        "Los combos sin ahorro dejan total 1900 por la oferta individual de A.",
        "La leyenda visual del combo queda pendiente de accesibilidad y calibración; se verifican importes e ID persistido.",
    ))


def _case_061():
    products, rules = _simple_assets(61, 0)
    two_a = (("A", "2", "200", "individual"),)
    one_combo_with_remainder = (("A", "2", "350", "combo"), ("B", "1", "250", "combo"))
    two_combos = (("A", "2", "500", "combo"), ("B", "2", "500", "combo"))
    two_combos_with_remainder = (("A", "3", "600", "combo"), ("B", "2", "500", "combo"))
    one_combo_with_two_remaining = (("A", "3", "450", "combo"), ("B", "1", "250", "combo"))
    variant = _variant("repeticiones-y-sobrantes", products, rules, (
        ("open", "", "", ()),
        ("add", "A", "2", two_a),
        ("add", "B", "1", one_combo_with_remainder),
        ("add", "E", "1", one_combo_with_remainder + (("E", "1", "0", ""),)),
        ("remove", "E", "", one_combo_with_remainder),
        ("edit", "B", "2", two_combos),
        ("edit", "A", "3", two_combos_with_remainder),
        ("edit", "B", "1", one_combo_with_two_remaining),
        ("edit", "B", "2", two_combos_with_remainder),
        ("cancel_payment", "", "", two_combos_with_remainder),
        ("pay", "", "", two_combos_with_remainder),
    ))
    return Journey("XG-PRM-061", (variant,), notes=(
        "Totales: 2A+B=2400; 2A+2B=3000; 3A+2B=3900; 3A+B=3300.",
        "La línea conserva ID del combo aunque su descuento incluya el beneficio del sobrante.",
    ))


def _case_062():
    base, products = _products(62, 0, {"A": "100.00", "B": "50.00", "C": "60.00", "E": "100.00"})
    rules = {
        "ab": _combo(base, products, "130.00", (("A", "1"), ("B", "1"))),
        "ac": _combo(base + 1, products, "120.00", (("A", "1"), ("C", "1"))),
    }
    only_a = (("A", "1", "0", ""),)
    combo_ab = (("A", "1", "13.33", "ab"), ("B", "1", "6.67", "ab"))
    combo_ac = (("A", "1", "25", "ac"), ("B", "1", "0", ""), ("C", "1", "15", "ac"))
    competing = _variant("mayor-ahorro", products, rules, (
        ("open", "", "", ()),
        ("add", "A", "1", only_a),
        ("add", "E", "1", only_a + (("E", "1", "0", ""),)),
        ("remove", "E", "", only_a),
        ("add", "B", "1", combo_ab),
        ("add", "C", "1", combo_ac),
        ("remove", "C", "", combo_ab),
        ("add", "C", "1", combo_ac),
        ("abandon", "", "", ()),
        ("open", "", "", ()),
        ("add", "A", "1", only_a),
        ("add", "B", "1", combo_ab),
        ("add", "C", "1", combo_ac),
        ("cancel_payment", "", "", combo_ac),
        ("pay", "", "", combo_ac),
    ))
    base, products = _products(62, 1, {"A": "100.00", "B": "50.00"})
    rules = {
        "higher": _combo(base + 1, products, "130.00", (("A", "1"), ("B", "1"))),
        "lower": _combo(base, products, "130.00", (("A", "1"), ("B", "1"))),
    }
    lower_ab = (("A", "1", "13.33", "lower"), ("B", "1", "6.67", "lower"))
    lower_ba = (("B", "1", "6.67", "lower"), ("A", "1", "13.33", "lower"))
    tie = _variant("empate-menor-id", products, rules, (
        ("open", "", "", ()),
        ("add", "A", "1", only_a),
        ("add", "B", "1", lower_ab),
        ("cancel_payment", "", "", lower_ab),
        ("pay", "", "", lower_ab),
        ("open", "", "", ()),
        ("add", "B", "1", (("B", "1", "0", ""),)),
        ("add", "A", "1", lower_ba),
        ("cancel_payment", "", "", lower_ba),
        ("pay", "", "", lower_ba),
    ))
    return Journey("XG-PRM-062", (competing, tie), notes=(
        "AB ahorra 20; AC ahorra 40 y deja total 170 con B sin descuento.",
        "El empate se verifica cobrando las dos ventas AB y BA a 130 cada una: ambas deben guardar el ID menor.",
        "La variante de empate termina con stock A -2, B -2 y dos cobros independientes por un total de 260.",
        "La leyenda visual del combo queda pendiente de accesibilidad y calibración; se verifican importes e ID persistido.",
        "Estos datos no acreditan optimización global de cualquier canasta.",
    ))


def _rounding_assets(variant_index):
    base, products = _products(63, variant_index,
                               {"A": "10.00", "B": "10.00", "C": "10.00", "E": "10.00"})
    rules = {"combo": _combo(base, products, "20.00", (("A", "1"), ("B", "1"), ("C", "1")))}
    return products, rules


def _case_063():
    only_a = (("A", "1", "0", ""),)
    incomplete = (("A", "1", "0", ""), ("B", "1", "0", ""))
    complete = (("A", "1", "3.33", "combo"), ("B", "1", "3.33", "combo"), ("C", "1", "3.34", "combo"))
    products, rules = _rounding_assets(0)
    base_variant = _variant("centavos-exactos", products, rules, (
        ("open", "", "", ()),
        ("add", "A", "1", only_a),
        ("add", "B", "1", incomplete),
        ("add", "C", "1", complete),
        ("add", "E", "1", complete + (("E", "1", "0", ""),)),
        ("remove", "E", "", complete),
        ("remove", "C", "", incomplete),
        ("add", "C", "1", complete),
        ("abandon", "", "", ()),
        ("open", "", "", ()),
        ("add", "A", "1", only_a),
        ("add", "B", "1", incomplete),
        ("add", "C", "1", complete),
        ("cancel_payment", "", "", complete),
        ("pay", "", "", complete),
    ))
    products, rules = _rounding_assets(1)
    with_manual = (("A", "1", "2.79", "combo", "1"),
                   ("B", "1", "3.10", "combo"), ("C", "1", "3.11", "combo"))
    manual_variant = _variant("base-neta-manual", products, rules, (
        ("open", "", "", ()),
        ("add", "A", "1", only_a),
        ("add", "B", "1", incomplete),
        ("add", "C", "1", complete),
        ("manual", "A", "1", with_manual),
        ("manual", "A", "0", complete),
        ("abandon", "", "", ()),
    ), requirements=("manual-discount",))
    return Journey("XG-PRM-063", (base_variant, manual_variant), notes=(
        "Orden ABC: automático 3.33+3.33+3.34=10, neto 20.",
        "Manual A=1: base 29, automático 2.79+3.10+3.11=9, neto 20.",
        "La variante manual exige permisos general y sobre ofertas ON; no comprueba el aviso.",
    ))


def _case_064():
    base, products = _products(64, 0, {"A": "40.00", "B": "20.00", "E": "10.00"}, weighted=("A", "B"))
    rules = {"combo": _combo(base, products, "40.00", (("A", "0.500"), ("B", "1.250")))}
    only_a = (("A", "0.250", "0", ""),)
    incomplete = (("A", "0.250", "0", ""), ("B", "1.250", "0", ""))
    one_combo = (("A", "0.500", "2.22", "combo"), ("B", "1.250", "2.78", "combo"))
    # Estado intermedio: se edita A antes que B. Consumo del combo:A0.500+B1.250.
    one_combo_with_a_remainder = (("A", "1.250", "2.22", "combo"), ("B", "1.250", "2.78", "combo"))
    two_combos_with_remainders = (("A", "1.250", "4.44", "combo"), ("B", "3.000", "5.56", "combo"))
    below_second_combo = (("A", "1.250", "2.22", "combo"), ("B", "2.490", "2.78", "combo"))
    exact_second_combo = (("A", "1.250", "4.44", "combo"), ("B", "2.500", "5.56", "combo"))
    variant = _variant("fracciones-y-limites", products, rules, (
        ("open", "", "", ()),
        ("add", "A", "0.250", only_a),
        ("add", "B", "1.250", incomplete),
        ("add", "E", "1", incomplete + (("E", "1", "0", ""),)),
        ("remove", "E", "", incomplete),
        ("edit", "A", "0.500", one_combo),
        ("edit", "A", "1.250", one_combo_with_a_remainder),
        ("edit", "B", "3.000", two_combos_with_remainders),
        ("edit", "B", "2.490", below_second_combo),
        ("edit", "B", "2.500", exact_second_combo),
        ("edit", "B", "3.000", two_combos_with_remainders),
        ("cancel_payment", "", "", two_combos_with_remainders),
        ("pay", "", "", two_combos_with_remainders),
    ))
    return Journey("XG-PRM-064", (variant,), notes=(
        "Combo: A 0.500 kg + B 1.250 kg por 40; ambos con UME decimal.",
        "Totales: 35, 40, intermedio 70, 100, B 2.490=94.80, B 2.500=90, final 100.",
        "Stock final: A -1.250 kg, B -3.000 kg; sin balanza ni cantidades de más de tres decimales.",
    ))


CASES = {
    "XG-PRM-060": _case_060(),
    "XG-PRM-061": _case_061(),
    "XG-PRM-062": _case_062(),
    "XG-PRM-063": _case_063(),
    "XG-PRM-064": _case_064(),
}
