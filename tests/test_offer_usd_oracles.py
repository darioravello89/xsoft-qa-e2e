"""La evidencia monetaria original debe coincidir aunque el total ARS sea correcto."""

from copy import deepcopy
from decimal import Decimal
from unittest.mock import Mock

import pytest

from framework.errors import QAError
from products.xgestion.offer_journeys.catalog import get_journey
from products.xgestion.offer_journeys.oracles import (
    BasketOracle,
    BasketSnapshot,
    assert_basket_sale,
    assert_basket_unchanged,
)
from products.xgestion.oracles import STATE_COLUMNS


def evidence():
    variant = get_journey("XG-PRM-080").variants[0]
    a, excluded = variant.products
    before = BasketSnapshot(frozenset(), {a.id: Decimal(100), excluded.id: Decimal(100)}, Decimal(0),
                            {table: () for table in STATE_COLUMNS})
    rows = {
        "ventas": ({"venId": 7, "venTotal": "75000", "venEstado": 1, "venUsuario": 5, "venPago": 1,
                    "ID_TipoComprobante": 99, "Pagado": "75000", "Vuelto": "0", "esPagoMultiple": 0,
                    "venDescuentos": "75000", "descuentoOfertas": "75000", "descuentoManual": "0",
                    "descuentoPago": "0", "descuentoCliente": "0", "activo": 1, "CAENumero": "",
                    "ID_Moneda": 1, "Cotizacion_USD": "1500", "ID_Moneda_Pago": 1,
                    "Pagado_Original": "75000", "ID_Moneda_Vuelto": 1, "Vuelto_Original": "0"},),
        "ventas_cuerpo": ({"vecId": 1, "item": 1, "venId": 7, "vecCodigo": a.id, "vecCantidad": "1",
                           "vecPrecio": "150000", "vecTotal": "150000", "vecOferta": "75000",
                           "ID_Oferta": variant.offers[0].id, "vecOfertaManual": "0", "ID_ListaPrecio": 0,
                           "Puntos_Acumulados": "0", "Puntos_Utilizados": "0", "activo": 1,
                           "ID_Moneda": 2, "vecPrecioOriginal": "100", "vecTotalOriginal": "100",
                           "vecOfertaOriginal": "50", "vecOfertaManualOriginal": "0",
                           "vecImporteIvaOriginal": "0", "vecOtrosImpuestosOriginal": "0"},),
        "ventas_pagos": (),
        "movimientos_articulos": ({"moaId": 1, "ID_Venta": 7, "moaArticuloCodigo": a.id,
                                   "moaCantidad": "-1", "activo": 1},),
        "movimientos_finanzas": ({"mofId": 1, "ID_Venta": 7, "ID_VentaPago": 0, "mofPago": 1,
                                  "mofIngreso": "75000", "mofEgreso": "0", "mofEstado": 1,
                                  "mofConcepto": 2, "activo": 1},),
    }
    after = BasketSnapshot(frozenset({7}), {a.id: Decimal(99), excluded.id: Decimal(100)}, Decimal(75000), rows)
    return variant, before, after


def verify(state):
    variant, before, after = state
    return assert_basket_sale(variant.products, variant.steps[-1].expected, before, after,
                              user_id=5, payment_id=1, received=Decimal(75000), exchange_rate="1500.00")


def test_correct_original_and_operational_amounts_pass():
    assert verify(evidence()) == 7


@pytest.mark.parametrize("table,key,value", [
    ("ventas", "ID_Moneda", 2), ("ventas", "Cotizacion_USD", "1"),
    ("ventas", "ID_Moneda_Pago", 2), ("ventas", "ID_Moneda_Vuelto", 2),
    ("ventas", "Pagado_Original", "50"), ("ventas", "Vuelto_Original", "1"),
    ("ventas_cuerpo", "ID_Moneda", 1), ("ventas_cuerpo", "vecPrecioOriginal", "150000"),
    ("ventas_cuerpo", "vecTotalOriginal", "150000"), ("ventas_cuerpo", "vecOfertaOriginal", "99.97"),
    ("ventas_cuerpo", "vecOfertaOriginal", "100"), ("ventas_cuerpo", "vecOfertaManualOriginal", "50"),
    ("ventas_cuerpo", "vecImporteIvaOriginal", "10.50"),
    ("ventas_cuerpo", "vecOtrosImpuestosOriginal", "10"),
    ("ventas_cuerpo", "vecPrecioOriginal", None), ("ventas", "Cotizacion_USD", "NaN"),
])
def test_correct_ars_total_cannot_hide_wrong_currency_snapshot(table, key, value):
    state = evidence()
    row = state[2].rows[table][0]
    if value is None:
        del row[key]
    else:
        row[key] = value
    with pytest.raises(AssertionError):
        verify(state)


def test_usd_evidence_cannot_be_checked_without_declared_exchange_rate():
    variant, before, after = evidence()
    with pytest.raises(AssertionError):
        assert_basket_sale(variant.products, variant.steps[-1].expected, before, after,
                           user_id=5, payment_id=1, received=Decimal(75000))


def test_cancel_detects_changed_currency_even_when_amounts_stay_identical():
    original = evidence()[2]
    modified = deepcopy(original)
    modified.rows["ventas_cuerpo"][0]["ID_Moneda"] = 1
    with pytest.raises(AssertionError):
        assert_basket_unchanged(original, modified)


def test_snapshot_projects_currency_fields_only_for_usd_and_checks_schema():
    from dataclasses import replace

    from products.xgestion.offer_journeys.usd import LINE_COLUMNS, SALE_COLUMNS

    variant = evidence()[0]
    fixtures = {"context": {"empresa": 90001, "sucursal": 1, "computadora": 1},
                "sale": {"cash_payment_id": 1}}
    for currency in ("ARS", "USD"):
        oracle = BasketOracle(Mock(), fixtures, tuple(replace(p, currency=currency) for p in variant.products))
        statements = []

        def query(sql, params):
            statements.append((sql, params))
            if "information_schema" in sql:
                return [{"name": name} for name in (SALE_COLUMNS if params == ("ventas",) else LINE_COLUMNS)]
            return [{"total": "0"}] if "SUM(" in sql else []

        oracle.query = query
        if currency == "USD":
            oracle.validate_currency_schema()
        oracle.snapshot()
        projection = " ".join(sql for sql, _ in statements)
        assert ("vecPrecioOriginal" in projection) is (currency == "USD")
        assert ("Cotizacion_USD" in projection) is (currency == "USD")
        assert all(sql.startswith("SELECT ") and "SELECT *" not in sql for sql, _ in statements)
    oracle.query = Mock(return_value=[])
    with pytest.raises(QAError, match="Paquete incompatible"):
        oracle.validate_currency_schema()
