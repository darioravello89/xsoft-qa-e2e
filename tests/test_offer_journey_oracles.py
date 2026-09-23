"""El oráculo debe detectar efectos incorrectos sin depender de un JAR ni DB."""

from copy import deepcopy
from decimal import Decimal

import pytest

from products.xgestion.offer_journeys.model import Line, Product
from products.xgestion.offer_journeys.oracles import (
    BasketSnapshot,
    assert_basket_sale,
    assert_basket_unchanged,
)
from products.xgestion.oracles import STATE_COLUMNS


def evidence():
    products = (Product("A", 981801, "QA-A"), Product("B", 981802, "QA-B"), Product("E", 981809, "QA-E"))
    lines = (Line("A", "2", "200", 981800), Line("B", "1", "100", 981800))
    before = BasketSnapshot(frozenset(), {p.id: Decimal(100) for p in products}, Decimal(0),
                            {table: () for table in STATE_COLUMNS})
    sale = dict(venId=7, venTotal="2700", venEstado=1, venUsuario=5, venPago=1, activo=1,
                ID_TipoComprobante=99, CAENumero="", Pagado="2700", Vuelto="0", esPagoMultiple=0,
                venDescuentos="300", descuentoOfertas="300", descuentoManual="0",
                descuentoPago="0", descuentoCliente="0")
    details = [dict(vecId=i, item=i, venId=7, vecCodigo=p.id, vecCantidad=line.quantity,
                    vecPrecio=line.price, vecTotal=str(line.gross), vecOferta=line.discount,
                    ID_Oferta=line.offer_id, ID_ListaPrecio=0, vecOfertaManual="0", Puntos_Acumulados=0,
                    Puntos_Utilizados=0, activo=1)
               for i, (p, line) in enumerate(zip(products, lines, strict=False), start=1)]
    stocks = [dict(moaId=i, ID_Venta=7, moaArticuloCodigo=p.id, moaCantidad=str(-Decimal(line.quantity)),
                   activo=1) for i, (p, line) in enumerate(zip(products, lines, strict=False), start=1)]
    cash = [dict(mofId=1, ID_Venta=7, ID_VentaPago=0, mofPago=1, mofIngreso="2700", mofEgreso="0",
                 mofEstado=1, mofConcepto=2, activo=1)]
    rows = {"ventas": (sale,), "ventas_cuerpo": tuple(details), "ventas_pagos": (),
            "movimientos_articulos": tuple(stocks), "movimientos_finanzas": tuple(cash)}
    after = BasketSnapshot(frozenset({7}), {981801: Decimal(98), 981802: Decimal(99), 981809: Decimal(100)},
                           Decimal(2700), rows)
    return products, lines, before, after


def verify(state):
    products, lines, before, after = state
    return assert_basket_sale(products, lines, before, after, user_id=5, payment_id=1, received=Decimal(2700))


def test_basket_oracle_accepts_exact_sale_and_unchanged_excluded_product():
    assert verify(evidence()) == 7
    assert_basket_unchanged(evidence()[2], evidence()[2])


@pytest.mark.parametrize("change", ["line_quantity", "offer", "offer_id", "duplicate_line", "wrong_product",
                                   "stock_excluded", "duplicate_cash", "extra_sale", "payment", "missing",
                                   "old_sale_changed", "manual", "fiscal", "nan"])
def test_basket_oracle_rejects_wrong_or_incomplete_evidence(change):
    state = list(deepcopy(evidence()))
    before, after = state[2:]
    rows = after.rows
    if change in {"line_quantity", "offer", "offer_id", "wrong_product", "manual", "nan"}:
        field, value = {"line_quantity": ("vecCantidad", "1"), "offer": ("vecOferta", "100"),
                        "offer_id": ("ID_Oferta", 9), "wrong_product": ("vecCodigo", 981809),
                        "manual": ("vecOfertaManual", "10"), "nan": ("vecOferta", "NaN")}[change]
        rows["ventas_cuerpo"][0][field] = value
    elif change == "duplicate_line":
        rows["ventas_cuerpo"] += (deepcopy(rows["ventas_cuerpo"][0]),)
    elif change == "stock_excluded":
        after.stock[981809] = Decimal(99)
    elif change == "duplicate_cash":
        rows["movimientos_finanzas"] *= 2
    elif change == "extra_sale":
        rows["ventas"] += (dict(rows["ventas"][0], venId=8),)
    elif change == "payment":
        rows["ventas_pagos"] = ({"ID_Venta": 7},)
    elif change == "missing":
        del rows["ventas_cuerpo"][0]["vecOferta"]
    elif change == "fiscal":
        rows["ventas"][0]["CAENumero"] = "unexpected"
    elif change == "old_sale_changed":
        before.rows["ventas"] = ({"venId": 3, "venTotal": "10"},)
        rows["ventas"] += ({"venId": 3, "venTotal": "20"},)
    with pytest.raises(AssertionError):
        verify(state)


def test_cancel_rejects_changed_non_primary_product_and_business_records():
    before = evidence()[2]
    after = deepcopy(before)
    after.stock[981802] -= 1
    with pytest.raises(AssertionError):
        assert_basket_unchanged(before, after)
    after = deepcopy(before)
    after.rows["ventas_pagos"] = ({"ID_Venta": 3},)
    with pytest.raises(AssertionError):
        assert_basket_unchanged(before, after)


def test_mysql_bit_fields_and_decimal_values_keep_their_types():
    state = list(deepcopy(evidence()))
    for table in ("ventas", "ventas_cuerpo", "movimientos_articulos", "movimientos_finanzas"):
        for row in state[3].rows[table]:
            row["activo"] = b"\x01"
    state[3].rows["ventas"][0]["esPagoMultiple"] = b"\x00"
    assert verify(state) == 7


def test_manual_and_automatic_discounts_are_checked_separately():
    products, _, before, after = deepcopy(evidence())
    lines = (Line("A", "2", "190", 981800, manual="100"), Line("B", "1", "100", 981800))
    sale = after.rows["ventas"][0]
    sale.update(venTotal="2610", Pagado="2610", venDescuentos="390",
                descuentoOfertas="290", descuentoManual="100")
    detail = after.rows["ventas_cuerpo"][0]
    detail.update(vecOferta="190", vecOfertaManual="100")
    after.rows["movimientos_finanzas"][0]["mofIngreso"] = "2610"
    after = BasketSnapshot(after.sale_ids, after.stock, Decimal(2610), after.rows)
    assert assert_basket_sale(products, lines, before, after, user_id=5, payment_id=1,
                              received=Decimal(2610)) == 7
    detail.update(vecOferta="290", vecOfertaManual="0")
    with pytest.raises(AssertionError):
        assert_basket_sale(products, lines, before, after, user_id=5, payment_id=1, received=Decimal(2610))


@pytest.mark.parametrize("field,value,expected,label", [
    ("ID_Oferta", 9, "981800", "oferta aplicada"),
    ("vecCantidad", "1", "2", "cantidad"),
    ("vecOferta", "100", "200", "descuento automático ARS"),
])
def test_line_discrepancy_identifies_public_product_field_and_scalar_values_without_private_row(
        monkeypatch, field, value, expected, label):
    import products.xgestion.oracles as base_oracles

    failures = []
    monkeypatch.setattr(base_oracles, "assertion_failed", lambda message, **details:
                        failures.append({"message": message, **details}))
    state = list(deepcopy(evidence()))
    row = state[3].rows["ventas_cuerpo"][0]
    row.update({field: value, "vecNombre": "PRIVATE-NAME-CANARY", "Notas": "PRIVATE-ROW-CANARY"})

    with pytest.raises(AssertionError) as error:
        verify(state)

    failure = failures[-1]
    assert "QA-A" in failure["message"] and field in failure["message"] and label in failure["message"]
    assert failure["expected"] == expected and failure["observed"] == str(value)
    assert "PRIVATE-" not in str(error.value) + repr(failure)
    assert "vecNombre" not in repr(failure) and "Notas" not in repr(failure)


def test_line_order_is_irrelevant_but_duplicate_product_cannot_replace_another(monkeypatch):
    import products.xgestion.oracles as base_oracles

    state = list(deepcopy(evidence()))
    state[3].rows["ventas_cuerpo"] = tuple(reversed(state[3].rows["ventas_cuerpo"]))
    assert verify(state) == 7
    first = state[3].rows["ventas_cuerpo"][1]
    state[3].rows["ventas_cuerpo"] = (first, dict(first, vecId=2, item=2))
    failures = []
    monkeypatch.setattr(base_oracles, "assertion_failed", lambda message, **details:
                        failures.append({"message": message, **details}))
    with pytest.raises(AssertionError):
        verify(state)
    assert "QA-A" in failures[-1]["message"] and "renglones" in failures[-1]["message"]
    assert failures[-1]["expected"] == "1" and failures[-1]["observed"] == "2"


def test_unknown_product_identity_reports_only_count_without_exposing_database_value(monkeypatch):
    import products.xgestion.oracles as base_oracles

    state = list(deepcopy(evidence()))
    state[3].rows["ventas_cuerpo"][0].update(vecCodigo=71234567, vecNombre="PRIVATE-NAME-CANARY")
    failures = []
    monkeypatch.setattr(base_oracles, "assertion_failed", lambda message, **details:
                        failures.append({"message": message, **details}))
    with pytest.raises(AssertionError):
        verify(state)
    assert "no declarado" in failures[-1]["message"]
    assert failures[-1]["expected"] == "0" and failures[-1]["observed"] == "1"
    assert "71234567" not in repr(failures) and "PRIVATE-" not in repr(failures)

