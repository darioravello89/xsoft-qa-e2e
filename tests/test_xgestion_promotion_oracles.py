"""Esperados públicos de promociones; filas sintéticas, sin conexión al ERP."""

from copy import deepcopy
from decimal import Decimal
from unittest.mock import patch

import pytest

from products.xgestion.oracles import Snapshot, XGestionOracle, assert_sale, assert_unchanged

D = Decimal
# Nombre, cantidad, bruto, neto, descuento, oferta aplicada.
EXAMPLES = (
    ("porcentaje", 3, "3000", "2700", "300", 980101),
    ("porcentaje_quince", 3, "3000", "2550", "450", 980102),
    ("tres_por_dos", 3, "3000", "2000", "1000", 980103),
    ("importe", 3, "3000", "2500", "500", 980104),
    ("sin_aplicacion", 1, "1000", "1000", "0", 0),
)
HEADER_DISCOUNTS = ("venDescuentos", "descuentoOfertas", "descuentoManual", "descuentoPago", "descuentoCliente")
DETAIL_PROMOTION = ("vecOferta", "ID_Oferta", "vecOfertaManual", "Puntos_Acumulados", "Puntos_Utilizados")


def evidence(example=EXAMPLES[0]):
    _, quantity, gross, total, discount, offer_id = example
    fixture = {
        "context": {"empresa": 91, "sucursal": 2, "computadora": 3, "usuario_id": 7},
        "product": {"id": 980101, "quantity": quantity, "unit_price": "1000.00"},
        "sale": {"cash_payment_id": 1, "non_fiscal_document_id": 99},
    }
    promotion = {"total": D(total), "offer_discount": D(discount), "offer_id": offer_id}
    before = Snapshot(frozenset({4}), D("20"), D("50"))
    after = Snapshot(frozenset({4, 5}), D("20") - quantity, D("50") + D(total))
    sale = {
        "venId": 5, "venTotal": D(total), "venEstado": 1, "venUsuario": 7, "venPago": 1,
        "ID_TipoComprobante": 99, "CAENumero": "", "activo": 1, "Pagado": D("3000"),
        "Vuelto": D("3000") - D(total), "esPagoMultiple": 0,
        "venDescuentos": D(discount), "descuentoOfertas": D(discount),
        "descuentoManual": D("0"), "descuentoPago": D("0"), "descuentoCliente": D("0"),
    }
    lines = [{
        "vecCodigo": "980101", "vecCantidad": D(quantity), "vecPrecio": D("1000"),
        "vecTotal": D(gross), "activo": 1, "vecOferta": D(discount), "ID_Oferta": offer_id,
        "vecOfertaManual": D("0"), "Puntos_Acumulados": D("0"), "Puntos_Utilizados": D("0"),
    }]
    stock = [{"moaArticuloCodigo": 980101, "moaCantidad": -D(quantity), "activo": 1}]
    cash = [{"mofPago": 1, "mofIngreso": D(total), "mofEgreso": D("0"), "mofEstado": 1,
             "mofConcepto": 2, "ID_VentaPago": 0, "activo": 1}]
    return {
        "fixtures": fixture, "before": before, "after": after, "sale": sale, "lines": lines,
        "payments": [], "sale_stock": stock, "sale_cash": cash, "received": D("3000"),
        "promotion": promotion,
    }


@pytest.mark.parametrize("example", EXAMPLES, ids=[row[0] for row in EXAMPLES])
def test_fixed_promotion_totals_preserve_gross_price_stock_and_net_cash(example):
    assert assert_sale(**evidence(example)) == 5


@pytest.mark.parametrize("section,key,value,pattern", (
    ("line", "vecPrecio", D("900"), "Precio"),
    ("line", "vecTotal", D("2700"), "subtotal"),
    ("line", "vecOferta", D("301"), "descuento"),
    ("line", "ID_Oferta", 980199, "oferta"),
    ("line", "vecOfertaManual", D("1"), "manual"),
    ("line", "Puntos_Acumulados", D("1"), "puntos"),
    ("line", "Puntos_Utilizados", D("1"), "puntos"),
    ("sale", "venDescuentos", D("299"), "descuento"),
    ("sale", "descuentoOfertas", D("299"), "descuento"),
    ("sale", "descuentoManual", D("1"), "descuento"),
    ("sale", "descuentoPago", D("1"), "descuento"),
    ("sale", "descuentoCliente", D("1"), "descuento"),
    ("sale", "venTotal", D("2000"), "2700"),
    ("sale", "Vuelto", D("0"), "vuelto"),
))
def test_rejects_wrong_promotion_even_when_other_totals_match(section, key, value, pattern):
    data = evidence()
    target = data["lines"][0] if section == "line" else data["sale"]
    target[key] = value
    with pytest.raises(AssertionError, match=pattern):
        assert_sale(**data)


def test_non_applicable_offer_must_not_leave_an_offer_identity():
    data = evidence(EXAMPLES[-1])
    data["lines"][0]["ID_Oferta"] = 980101
    with pytest.raises(AssertionError, match="oferta"):
        assert_sale(**data)


@pytest.mark.parametrize("column", HEADER_DISCOUNTS + DETAIL_PROMOTION)
@pytest.mark.parametrize("incomplete", ("missing", "null"))
def test_incomplete_promotion_projection_cannot_pass_as_zero(column, incomplete):
    data = evidence(EXAMPLES[-1])
    target = data["sale"] if column in HEADER_DISCOUNTS else data["lines"][0]
    if incomplete == "missing":
        del target[column]
    else:
        target[column] = None
    with pytest.raises(AssertionError, match="incompleta"):
        assert_sale(**data)


@pytest.mark.parametrize("field,value", (
    ("total", D("NaN")), ("total", D("Infinity")), ("total", D("-1")),
    ("offer_discount", D("-1")), ("offer_discount", D("1")),
    ("offer_id", -1), ("offer_id", True),
))
def test_invalid_or_inconsistent_expectation_is_rejected(field, value):
    data = evidence()
    data["promotion"][field] = value
    with pytest.raises(AssertionError, match="esperado"):
        assert_sale(**data)


def test_promotion_rejects_duplicate_or_compensated_payments_and_movements():
    base = evidence()
    variants = []
    data = deepcopy(base)
    data["payments"] = [{"ID_VentaPago": 20, "activo": 0}]
    variants.append((data, "ventas_pagos"))
    data = deepcopy(base)
    data["sale_cash"] += [dict(data["sale_cash"][0], mofIngreso=D("100")),
                          dict(data["sale_cash"][0], mofIngreso=D("0"), mofEgreso=D("100"))]
    variants.append((data, "movimiento.*caja"))
    data = deepcopy(base)
    data["sale_stock"] += [dict(data["sale_stock"][0], moaCantidad=D("1")),
                           dict(data["sale_stock"][0], moaCantidad=D("-1"))]
    variants.append((data, "movimiento.*stock"))
    for data, message in variants:
        with pytest.raises(AssertionError, match=message):
            assert_sale(**data)


def test_three_unit_stock_error_has_quantity_specific_evidence():
    data = evidence()
    data["sale_stock"][0]["moaCantidad"] = D("-2")
    with patch("products.xgestion.oracles.assertion_failed") as failure:
        with pytest.raises(AssertionError, match="3 unidades"):
            assert_sale(**data)
        assert failure.call_args.kwargs["expected"] == "Variación -3 unidades"


def test_verify_sale_fetches_scoped_promotion_columns_and_forwards_expectations():
    data = evidence(EXAMPLES[1])
    oracle = XGestionOracle(None, data["fixtures"])
    oracle.snapshot = lambda: data["after"]
    tables = {"ventas": [data["sale"]], "ventas_cuerpo": data["lines"], "ventas_pagos": [],
              "movimientos_articulos": data["sale_stock"], "movimientos_finanzas": data["sale_cash"]}
    calls = {}

    def query(sql, params):
        assert sql.startswith("SELECT ") and sql.count("%s") == len(params)
        assert params == (91, 2, 3, 5)
        assert "activo=1" not in sql and "SUM(" not in sql
        table = sql.split(" FROM ", 1)[1].split()[0]
        calls[table] = sql.split(" FROM ", 1)[0][7:].strip().split(",")
        return tables[table]

    oracle.query = query
    assert oracle.verify_sale(data["before"], received=D("3000"), expected_sale_id=5,
                              promotion=data["promotion"]) == 5
    assert set(HEADER_DISCOUNTS) <= set(calls["ventas"])
    assert set(DETAIL_PROMOTION) <= set(calls["ventas_cuerpo"])
    assert not any("descuentoFidelizacion" in columns for columns in calls.values())


def test_snapshot_detects_discount_changes_without_changes_to_net_total():
    data = evidence()
    oracle = XGestionOracle(None, data["fixtures"])
    tables = {"ventas": [data["sale"]], "ventas_cuerpo": data["lines"], "ventas_pagos": [],
              "movimientos_articulos": data["sale_stock"], "movimientos_finanzas": data["sale_cash"]}

    def query(sql, params):
        if "COALESCE(SUM(" in sql:
            return [{"total": D("20")}]
        columns, tail = sql[7:].split(" FROM ", 1)
        return [{key: row.get(key) for key in columns.split(",")} for row in tables[tail.split()[0]]]

    oracle.query = query
    before = oracle.snapshot()
    data["lines"][0]["vecOfertaManual"] = D("10")
    with pytest.raises(AssertionError, match="registros"):
        assert_unchanged(before, oracle.snapshot())
