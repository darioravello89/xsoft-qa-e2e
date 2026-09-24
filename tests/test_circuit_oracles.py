"""Contratos de recepción y cierre: dinero, stock y deuda deben conciliar juntos."""

from copy import deepcopy
from dataclasses import replace
from datetime import datetime
from decimal import Decimal as D

import pytest

from products.xgestion.circuits.oracles import (
    EXTRA_COLUMNS,
    PRODUCT_SET,
    CircuitSnapshot,
    assert_cash_sale,
    assert_purchase,
    assert_turn,
    assert_unchanged,
)
from products.xgestion.offer_journeys.model import Line
from products.xgestion.offer_journeys.oracles import BasketSnapshot
from products.xgestion.oracles import STATE_COLUMNS


def baseline():
    prices = tuple({"artId": 990101+i, "ID_Moneda": 1 if i % 2 == 0 else 2,
                    "artPrecioCosto": "500" if i % 2 == 0 else "50",
                    "artPrecioVenta": "1000" if i % 2 == 0 else "100"} for i in range(8))
    extras = {table: () for table in EXTRA_COLUMNS}
    extras["articulos"] = prices
    return CircuitSnapshot(BasketSnapshot(frozenset(), {990101+i: D(20) for i in range(8)}, D(0),
                                          {table: () for table in STATE_COLUMNS}), extras)


def received():
    before = baseline()
    after = deepcopy(before)
    after.extra["compra"] = ({"comId": 41, "ID_ComputadoraModifica": 0, "comProveedor": 980001,
                              "comTotal": "362400", "comPagado": "0", "comEstado": 2,
                              "comActivo": 1, "ID_Moneda": 1, "Cotizacion_USD": "1500",
                              "Convertir_USD": 0},)
    after.extra["compra_detalle"] = tuple(
        {"codId": i+1, "comId": 41, "ID_ComputadoraModifica": 0, "codMateriaPrima": 990101+i,
         "codCantidad": "2", "codPrecioUnitario": "600" if i % 2 == 0 else "60",
         "codPrecioTotal": "1200" if i % 2 == 0 else "120", "ID_Moneda": 1 if i % 2 == 0 else 2,
         "codRecibido": 1, "codSumaStock": 1, "codActualizaPrecio": 1,
         "codActualizaPrecioConBonificacion": 0, "codDescuento": "0", "activo": 1} for i in range(4))
    after.extra["cuentas_corrientes_proveedores"] = (
        {"cteId": 9, "cteProveedor": 980001, "ID_ComprobanteAsociado": 41, "cteIngresos": "0",
         "cteEgresos": "362400", "ID_Moneda": 1, "cteIngresosOriginal": "0",
         "cteEgresosOriginal": "362400", "Cotizacion_USD": None, "activo": 1},)
    after.extra["articulos"] = tuple(
        ({**row, "artPrecioCosto": "600" if i % 2 == 0 else "60",
          "artPrecioVenta": ("1200" if i % 2 == 0 else "120") if i > 1 else row["artPrecioVenta"]}
         if i < 4 else row)
        for i, row in enumerate(after.extra["articulos"]))
    after.basket.rows["movimientos_articulos"] = tuple(
        {"moaId": i+1, "moaArticuloCodigo": 990101+i, "moaCantidad": "2",
         "ID_Compra": 41, "ID_Venta": 0, "activo": 1} for i in range(4))
    for i in range(4):
        after.basket.stock[990101+i] += 2
    return before, after


def test_receipt_updates_four_costs_only_calculated_prices_and_supplier_debt():
    assert assert_purchase(*received()) == 41


@pytest.mark.parametrize("table,key,value", [
    ("compra", "comTotal", "240"), ("compra", "comEstado", 1),
    ("compra", "Cotizacion_USD", "1"), ("compra", "ID_Moneda", 2),
    ("compra_detalle", "codRecibido", 0), ("compra_detalle", "codSumaStock", 0),
    ("compra_detalle", "ID_ComputadoraModifica", 3), ("compra_detalle", "codPrecioUnitario", "900000"),
    ("cuentas_corrientes_proveedores", "cteEgresos", "0"),
    ("cuentas_corrientes_proveedores", "ID_ComprobanteAsociado", 42),
    ("cuentas_corrientes_proveedores", "cteProveedor", 6),
    ("articulos", "artPrecioVenta", "1200"), ("articulos", "artPrecioCosto", "NaN"),
])
def test_wrong_receipt_cannot_pass(table, key, value):
    before, after = received()
    after.extra[table][0][key] = value
    with pytest.raises(AssertionError):
        assert_purchase(before, after)


@pytest.mark.parametrize("defect", ["missing", "duplicate", "foreign_stock", "cash", "customer_debt", "no_stock"])
def test_debt_alone_does_not_prove_receipt(defect):
    before, after = received()
    if defect == "missing":
        del after.extra["compra_detalle"]
    elif defect == "duplicate":
        after.extra["cuentas_corrientes_proveedores"] *= 2
    elif defect == "foreign_stock":
        after.basket.stock[990108] -= 1
    elif defect == "cash":
        after.basket.rows["movimientos_finanzas"] = ({"mofId": 99},)
    elif defect == "customer_debt":
        after.extra["cuentas_corrientes_clientes"] = ({"cccId": 33},)
    else:
        after.basket.rows["movimientos_articulos"] = ()
    with pytest.raises(AssertionError):
        assert_purchase(before, after)


def test_cancel_requires_all_domains_unchanged():
    state = received()[1]  # Also works on a draft with persisted detail.
    assert_unchanged(state, deepcopy(state))
    changed = deepcopy(state)
    changed.extra["articulos"][0]["artPrecioCosto"] = "601"
    with pytest.raises(AssertionError):
        assert_unchanged(state, changed)


def test_missing_control_products_in_both_snapshots_are_incomplete_evidence():
    before, after = received()
    before.extra["articulos"] = before.extra["articulos"][:4]
    after.extra["articulos"] = after.extra["articulos"][:4]
    with pytest.raises(AssertionError):
        assert_purchase(before, after)


def opened():
    before = baseline()
    after = deepcopy(before)
    after.extra["movimientos_sistema"] = ({"mosId": 50, "mosUsuario": 5, "ID_TipoMovimiento": 1,
                                          "ID_MovimientoSistemaAsociado": 0, "activo": 1,
                                          "mosFechaHora": datetime(2026, 9, 24, 10)},)
    return before, after


def test_turn_open_close_are_linked_and_do_not_repeat_money_or_stock():
    before, after = opened()
    assert assert_turn(before, after, user_id=5) == 50
    closed = deepcopy(after)
    closed.extra["movimientos_sistema"] += ({"mosId": 51, "mosUsuario": 5, "ID_TipoMovimiento": 2,
                                            "ID_MovimientoSistemaAsociado": 50, "activo": 1,
                                            "mosFechaHora": datetime(2026, 9, 24, 11)},)
    assert assert_turn(after, closed, user_id=5, opening=50) == 51
    closed = replace(closed, basket=replace(closed.basket, cash=D(150000)))
    with pytest.raises(AssertionError):
        assert_turn(after, closed, user_id=5, opening=50)


@pytest.mark.parametrize("key,value", [("ID_MovimientoSistemaAsociado", 3), ("mosUsuario", 7),
                                       ("activo", 0), ("ID_TipoMovimiento", 2)])
def test_invalid_opening_rejected(key, value):
    before, after = opened()
    after.extra["movimientos_sistema"][0][key] = value
    with pytest.raises(AssertionError):
        assert_turn(before, after, user_id=5)


def cash_sale():
    # Independent synthetic evidence for 2 x USD100, received ARS350000/change50000.
    from test_offer_usd_oracles import evidence

    _, _, template = evidence()
    before = baseline()
    rows = deepcopy(template.rows)
    rows["ventas"][0].update(venTotal="300000", Pagado="350000", Vuelto="50000",
                             venDescuentos="0", descuentoOfertas="0",
                             Pagado_Original="350000", Vuelto_Original="50000")
    rows["ventas_cuerpo"][0].update(vecCodigo=990102, vecCantidad="2", vecPrecio="150000",
                                    vecTotal="300000", vecOferta="0", ID_Oferta=0,
                                    vecTotalOriginal="200", vecOfertaOriginal="0")
    rows["movimientos_articulos"][0].update(moaArticuloCodigo=990102, moaCantidad="-2")
    rows["movimientos_finanzas"][0].update(mofIngreso="300000", ID_Moneda=1, Cotizacion_USD="1500",
                                          mofIngresoOriginal="300000", mofEgresoOriginal=None)
    stock = {p.id: D(20) for p in PRODUCT_SET}
    stock[990102] -= 2
    after = CircuitSnapshot(BasketSnapshot(frozenset({7}), stock, D(300000), rows), deepcopy(before.extra))
    line = Line("USD-FIJO", "2", price="150000", original_price="100", original_discount="0")
    return before, after, line


def test_cash_usd_sale_conciles_original_amounts_ledger_debt_and_stock():
    assert assert_cash_sale(*cash_sale(), user_id=5, received="350000") == 7


@pytest.mark.parametrize("defect", ["ledger_currency", "ledger_original", "ledger_rate", "missing_original",
                                   "control_stock", "unexpected_debt", "duplicate_cash", "previous_changed"])
def test_cash_usd_sale_rejects_unbalanced_or_incomplete_evidence(defect):
    before, after, line = cash_sale()
    cash = after.basket.rows["movimientos_finanzas"][0]
    if defect == "ledger_currency":
        cash["ID_Moneda"] = 2
    elif defect == "ledger_original":
        cash["mofIngresoOriginal"] = "200"
    elif defect == "ledger_rate":
        cash["Cotizacion_USD"] = "1"
    elif defect == "missing_original":
        del cash["mofEgresoOriginal"]
    elif defect == "control_stock":
        after.basket.stock[990108] -= 1
    elif defect == "unexpected_debt":
        after.extra["cuentas_corrientes_clientes"] = ({"cccId": 5},)
    elif defect == "duplicate_cash":
        after.basket.rows["movimientos_finanzas"] *= 2
    else:
        before.basket.rows["movimientos_finanzas"] = ({"mofId": 9, "mofIngreso": "1"},)
        after.basket.rows["movimientos_finanzas"] += ({"mofId": 9, "mofIngreso": "2"},)
    with pytest.raises(AssertionError):
        assert_cash_sale(before, after, line, user_id=5, received="350000")
