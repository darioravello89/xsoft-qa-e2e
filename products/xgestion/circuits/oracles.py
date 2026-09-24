"""Lecturas acotadas; nunca corrigen ni completan una operación del ERP."""

from collections import Counter
from dataclasses import dataclass, field, replace
from datetime import datetime
from decimal import Decimal

from framework.errors import QAError
from framework.events import diagnostic
from products.xgestion.offer_journeys.model import Product
from products.xgestion.offer_journeys.oracles import (
    BasketOracle,
    BasketSnapshot,
    _encoded,
    _equal,
    _key,
    _number,
    assert_basket_sale,
    assert_basket_unchanged,
)
from products.xgestion.oracles import _require, enabled
from products.xgestion.seeds.circuits import PRODUCTS

PRODUCT_SET = tuple(Product(code, identifier, "QA-CIR-" + code, price, currency=
                            "USD" if options.get("ID_Moneda") == 2 else "ARS")
                    for identifier, code, price, _, _, options in PRODUCTS)
EXTRA_COLUMNS = {
    "compra": "comId,ID_ComputadoraModifica,comProveedor,comTotal,comPagado,comEstado,comActivo,"
              "ID_Moneda,Cotizacion_USD,Convertir_USD",
    "compra_detalle": "codId,comId,ID_ComputadoraModifica,codMateriaPrima,codCantidad,codPrecioUnitario,"
                      "codPrecioTotal,ID_Moneda,codRecibido,codSumaStock,codActualizaPrecio,"
                      "codActualizaPrecioConBonificacion,codDescuento,activo",
    "cuentas_corrientes_clientes": "cccId,cccCliente,cccIngresos,cccEgresos,cccPago,ID_ComprobanteAsociado,"
                                  "ID_Moneda,cccIngresosOriginal,cccEgresosOriginal,Cotizacion_USD,activo",
    "cuentas_corrientes_proveedores": "cteId,cteProveedor,cteIngresos,cteEgresos,ID_ComprobanteAsociado,"
                                     "ID_Moneda,cteIngresosOriginal,cteEgresosOriginal,Cotizacion_USD,activo",
    "movimientos_sistema": "mosId,mosFechaHora,mosUsuario,ID_TipoMovimiento,ID_MovimientoSistemaAsociado,activo",
    "articulos": "artId,ID_Moneda,artPrecioCosto,artPrecioVenta",
}


@dataclass(frozen=True)
class CircuitSnapshot:
    basket: BasketSnapshot
    extra: dict[str, tuple[dict, ...]] = field(repr=False)


def additions(before, after, label):
    old, new = _encoded(before), _encoded(after)
    _require(not old - new, f"Se modificaron o eliminaron registros anteriores: {label}.")
    difference = new - old
    result = []
    for row in after:
        key = _key(row)
        if difference[key]:
            result.append(row)
            difference[key] -= 1
    return result


def same_extra(before, after, *, except_tables=()):
    _require(set(before.extra) == set(after.extra) == set(EXTRA_COLUMNS),
             "Falta evidencia completa de compras, cuentas corrientes, precios o turnos.")
    for table in EXTRA_COLUMNS:
        if table not in except_tables:
            _require(_encoded(before.extra[table]) == _encoded(after.extra[table]),
                     f"La operación modificó {table} fuera del circuito esperado.")


def assert_unchanged(before, after):
    same_extra(before, after)
    assert_basket_unchanged(before.basket, after.basket)


def assert_cash_sale(before, after, line, *, user_id, received):
    same_extra(before, after)
    sale_id = assert_basket_sale(PRODUCT_SET, (line,), before.basket, after.basket, user_id=user_id,
                                payment_id=1, received=Decimal(received), exchange_rate="1500.00")
    cash = additions(before.basket.rows["movimientos_finanzas"],
                     after.basket.rows["movimientos_finanzas"], "Libro Diario")[0]
    for key, value in {"ID_Moneda": 1, "Cotizacion_USD": 1500,
                       "mofIngresoOriginal": line.total}.items():
        _equal(cash, key, value)
    _require("mofEgresoOriginal" in cash and cash["mofEgresoOriginal"] in (None, 0, Decimal(0)),
             "La venta de contado contiene egreso original o falta su evidencia.")
    diagnostic("Libro Diario conciliado en ARS; cuentas corrientes, compras y precios intactos")
    return sale_id


def assert_purchase(before, after):
    same_extra(before, after, except_tables=("compra", "compra_detalle", "articulos",
                                           "cuentas_corrientes_proveedores"))
    # La recepción no cobra, vende ni modifica deuda del cliente.
    unchanged_rows = dict(after.basket.rows)
    unchanged_rows["movimientos_articulos"] = before.basket.rows["movimientos_articulos"]
    assert_basket_unchanged(before.basket, replace(after.basket, rows=unchanged_rows, stock=before.basket.stock))
    headers = additions(before.extra["compra"], after.extra["compra"], "cabecera de compra")
    _require(len(headers) == 1, "La recepción debe crear una única compra completa.")
    header = headers[0]
    purchase_id = _number(header, "comId")
    for key, value in {"comProveedor": 980001, "comTotal": 362400, "comPagado": 0,
                       "comEstado": 2, "ID_Moneda": 1, "Cotizacion_USD": 1500}.items():
        _equal(header, key, value)
    _require(enabled(header.get("comActivo")) and "Convertir_USD" in header
             and header["Convertir_USD"] in (0, False, b"\x00"),
             "El remito debe estar activo y conservar costos originales USD.")
    variant = _number(header, "ID_ComputadoraModifica")
    details = additions(before.extra["compra_detalle"], after.extra["compra_detalle"], "detalle de compra")
    _require(len(details) == 4, "Se requieren cuatro renglones recibidos, sin duplicados.")
    _require(Counter(_number(row, "codMateriaPrima") for row in details)
             == Counter(range(990101, 990105)), "Los productos recibidos no corresponden al circuito.")
    for row in details:
        usd = _number(row, "codMateriaPrima") in (990102, 990104)
        for key, value in {"comId": purchase_id, "ID_ComputadoraModifica": variant, "codCantidad": 2,
                           "codPrecioUnitario": 60 if usd else 600, "codPrecioTotal": 120 if usd else 1200,
                           "ID_Moneda": 2 if usd else 1, "codDescuento": 0}.items():
            _equal(row, key, value)
        _require(all(enabled(row.get(key)) for key in ("activo", "codRecibido", "codSumaStock",
                                                      "codActualizaPrecio")),
                 "El renglón no quedó recibido con stock y actualización de costo.")
        _require(row.get("codActualizaPrecioConBonificacion") in (0, False, b"\x00"),
                 "No corresponde actualizar con bonificación en este perfil.")
    stock = additions(before.basket.rows["movimientos_articulos"], after.basket.rows["movimientos_articulos"],
                      "stock recibido")
    _require(len(stock) == 4, "Debe haber cuatro ingresos de stock, uno por artículo.")
    _require(Counter(_number(row, "moaArticuloCodigo") for row in stock)
             == Counter(range(990101, 990105)), "El stock se asignó a productos incorrectos.")
    for row in stock:
        for key, value in {"ID_Compra": purchase_id, "ID_Venta": 0, "moaCantidad": 2}.items():
            _equal(row, key, value)
        _require(enabled(row.get("activo")), "El movimiento recibido está inactivo.")
    _require(set(before.basket.stock) == set(after.basket.stock) == set(range(990101, 990109)),
             "Falta stock de control.")
    for identifier in before.basket.stock:
        delta = after.basket.stock[identifier] - before.basket.stock[identifier]
        expected = 2 if 990101 <= identifier <= 990104 else 0
        _require(delta == expected, "La recepción alteró incorrectamente el saldo de stock.",
                 expected=str(expected), observed=str(delta))
    debts = additions(before.extra["cuentas_corrientes_proveedores"],
                      after.extra["cuentas_corrientes_proveedores"], "deuda del proveedor")
    _require(len(debts) == 1, "La recepción debe generar una sola deuda de proveedor.")
    for key, value in {"cteProveedor": 980001, "ID_ComprobanteAsociado": purchase_id,
                       "cteIngresos": 0, "cteEgresos": 362400, "ID_Moneda": 1,
                       "cteIngresosOriginal": 0, "cteEgresosOriginal": 362400}.items():
        _equal(debts[0], key, value)
    _require(enabled(debts[0].get("activo")) and "Cotizacion_USD" in debts[0]
             and debts[0]["Cotizacion_USD"] is None, "Foto de deuda ARS inválida.")
    old = {row["artId"]: row for row in before.extra["articulos"]}
    prices = {row["artId"]: row for row in after.extra["articulos"]}
    _require(len(old) == len(before.extra["articulos"]) and len(prices) == len(after.extra["articulos"])
             and old.keys() == prices.keys() == set(range(990101, 990109)),
             "Falta evidencia única de precios antes y después.")
    for identifier, row in prices.items():
        if identifier not in range(990101, 990105):
            _require(row == old[identifier], "Se modificó el precio de un producto excluido.")
            continue
        usd = identifier in (990102, 990104)
        _equal(row, "ID_Moneda", 2 if usd else 1)
        _equal(row, "artPrecioCosto", 60 if usd else 600)
        _equal(row, "artPrecioVenta", {990101: 1000, 990102: 100, 990103: 1200, 990104: 120}[identifier])
    diagnostic("Remito conciliado: cuatro ingresos de stock, costos, precios y deuda ARS 362400 sin egreso")
    return int(purchase_id)


def assert_turn(before, after, *, user_id, opening=None):
    same_extra(before, after, except_tables=("movimientos_sistema",))
    assert_basket_unchanged(before.basket, after.basket)
    rows = additions(before.extra["movimientos_sistema"], after.extra["movimientos_sistema"], "turno")
    _require(len(rows) == 1, "Debe registrarse un único movimiento de apertura o cierre.")
    row = rows[0]
    for key, value in {"mosUsuario": user_id, "ID_TipoMovimiento": 1 if opening is None else 2,
                       "ID_MovimientoSistemaAsociado": opening or 0}.items():
        _equal(row, key, value)
    _require(enabled(row.get("activo")), "El movimiento de turno debe estar activo.")
    _require(isinstance(row.get("mosFechaHora"), datetime), "Falta fecha de apertura/cierre.")
    if opening is not None:
        starts = [item for item in before.extra["movimientos_sistema"]
                  if item.get("mosId") == opening and item.get("ID_TipoMovimiento") == 1]
        _require(len(starts) == 1 and enabled(starts[0].get("activo")), "Falta apertura activa única.")
        _require(row["mosFechaHora"] >= starts[0]["mosFechaHora"], "El cierre es anterior a la apertura.")
    return int(_number(row, "mosId"))


class CircuitOracle(BasketOracle):
    extra_columns = {"movimientos_articulos": "ID_Compra",
                     "movimientos_finanzas": "ID_Moneda,mofIngresoOriginal,mofEgresoOriginal,Cotizacion_USD,mofFechaHora"}

    def __init__(self, connection, fixtures):
        super().__init__(connection, fixtures, PRODUCT_SET, 1)

    def snapshot(self):
        try:
            basket = super().snapshot()
            extra = {}
            for table, columns in EXTRA_COLUMNS.items():
                where, args = "Empresa=%s AND Sucursal=%s AND Computadora=%s", self.scope
                if table == "articulos":
                    where, args = "Empresa=%s AND artId BETWEEN %s AND %s", (self.scope[0], 990101, 990108)
                if table == "movimientos_sistema":
                    where += " AND ID_TipoMovimiento IN (1,2)"
                extra[table] = tuple(self.query(f"SELECT {columns} FROM {table} WHERE {where}", args))
            return CircuitSnapshot(basket, extra)
        except AssertionError:
            raise
        except Exception:
            raise QAError("Paquete incompatible o lectura incompleta de circuitos. Revisar esquema, "
                          "conexión y contrato circuitos-comerciales-v1; no se migra desde el test.") from None
