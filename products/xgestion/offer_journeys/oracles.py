"""Comprobaciones de canastas completas, sin escribir datos del ERP."""

import json
from collections import Counter
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation

from framework.errors import QAError
from framework.events import diagnostic
from products.xgestion.oracles import STATE_COLUMNS, XGestionOracle, _require, enabled

_LINE_FIELDS = (("vecCodigo", "producto"), ("vecCantidad", "cantidad"),
                ("vecPrecio", "precio unitario ARS"), ("vecTotal", "importe bruto ARS"),
                ("vecOferta", "descuento automático ARS"), ("ID_Oferta", "oferta aplicada"),
                ("vecOfertaManual", "descuento manual ARS"), ("ID_ListaPrecio", "lista de precios"))


@dataclass(frozen=True)
class BasketSnapshot:
    sale_ids: frozenset[int]
    stock: dict[int, Decimal]
    cash: Decimal
    rows: dict[str, tuple[dict, ...]] = field(repr=False)


def _key(row):
    return json.dumps(row, sort_keys=True, default=str)


def _encoded(rows):
    return Counter(_key(row) for row in rows)


def _number(row, key):
    try:
        raw = row[key]
        if key == "esPagoMultiple" and raw in (False, True, b"\x00", b"\x01"):
            raw = int(enabled(raw))
        value = Decimal(str(raw))
        valid = value.is_finite()
    except (KeyError, TypeError, ValueError, InvalidOperation):
        valid = False
    _require(valid, "Evidencia numérica incompleta o inválida.",
             expected=f"Columna {key} con un número finito", observed="Valor ausente o inválido")
    return value


def _equal(row, key, expected):
    observed = _number(row, key)
    _require(observed == expected, f"Comprobación de persistencia incorrecta: {key}.",
             expected=str(expected), observed=str(observed))


def _complete(before, after):
    _require(set(before.rows) == set(after.rows) == set(STATE_COLUMNS),
             "Falta evidencia de las cinco tablas comerciales.")
    _require(set(before.stock) == set(after.stock), "Falta evidencia de stock de un producto.")


def assert_basket_unchanged(before, after):
    _complete(before, after)
    _require(before.sale_ids == after.sale_ids, "La operación alteró las ventas persistidas.")
    _require(before.stock == after.stock, "La operación alteró el stock de la canasta.")
    _require(before.cash == after.cash, "La operación alteró el saldo del medio de pago.")
    for table in STATE_COLUMNS:
        _require(_encoded(before.rows[table]) == _encoded(after.rows[table]),
                 f"La operación alteró registros de {table}.")
    diagnostic("Canasta cancelada sin cambios en ventas, detalles, pagos, stock ni caja")


def _new_rows(before, after):
    _complete(before, after)
    result = {}
    for table in STATE_COLUMNS:
        old, new = _encoded(before.rows[table]), _encoded(after.rows[table])
        _require(not old - new, f"La operación modificó o eliminó registros anteriores de {table}.")
        remaining = new - old
        result[table] = []
        for row in after.rows[table]:
            key = _key(row)
            if remaining[key]:
                result[table].append(row)
                remaining[key] -= 1
    return result


def _assert_line_items(products, expected, observed):
    """Keep multiset equality; diagnose only public identities and selected scalars."""
    if Counter(expected) == Counter(observed):
        return
    known = {Decimal(product.id) for product in products}
    foreign = sum(row[0] not in known for row in observed)
    _require(not foreign, "Hay renglones de un producto no declarado en el recorrido.",
             expected="0", observed=str(foreign))
    for product in products:
        wanted = sorted(row for row in expected if row[0] == product.id)
        found = sorted(row for row in observed if row[0] == product.id)
        # The label is from the public journey, never from a database name/code.
        label = f"Producto {product.ref} ({product.code})"
        _require(len(found) == len(wanted), f"{label}: cantidad de renglones persistidos incorrecta.",
                 expected=str(len(wanted)), observed=str(len(found)))
        for wanted_row, found_row in zip(wanted, found, strict=True):
            for index, (key, field_name) in enumerate(_LINE_FIELDS[1:], start=1):
                _require(found_row[index] == wanted_row[index],
                         f"{label}: {field_name} ({key}) persistido no coincide con el escenario.",
                         expected=str(wanted_row[index]), observed=str(found_row[index]))


def assert_basket_sale(products, lines, before, after, *, user_id, payment_id, received, exchange_rate=None):
    usd = any(product.currency == "USD" for product in products)
    _require(not usd or exchange_rate == "1500.00", "Falta cotización explícita del recorrido USD.")
    rows = _new_rows(before, after)
    created = after.sale_ids - before.sale_ids
    _require(len(created) == 1 and before.sale_ids <= after.sale_ids,
             "Debe persistirse exactamente una venta nueva y ninguna eliminada.")
    sale_id = next(iter(created))
    counts = {"ventas": 1, "ventas_cuerpo": len(lines), "ventas_pagos": 0,
              "movimientos_articulos": len(lines), "movimientos_finanzas": 1}
    for table, count in counts.items():
        _require(len(rows[table]) == count, f"Cantidad inesperada de registros nuevos en {table}.",
                 expected=str(count), observed=str(len(rows[table])))
    total = sum((line.total for line in lines), Decimal(0))
    discount = sum((Decimal(line.discount) for line in lines), Decimal(0))
    manual = sum((Decimal(line.manual) for line in lines), Decimal(0))
    _require(received.is_finite() and received >= total, "El recibido no cubre el total de la venta.")
    sale = rows["ventas"][0]
    for key, value in {"venId": sale_id, "venTotal": total, "venEstado": 1, "venUsuario": user_id,
                       "venPago": payment_id, "ID_TipoComprobante": 99, "Pagado": received,
                       "Vuelto": received - total, "esPagoMultiple": 0, "venDescuentos": discount + manual,
                       "descuentoOfertas": discount, "descuentoManual": manual, "descuentoPago": 0,
                       "descuentoCliente": 0}.items():
        _equal(sale, key, value)
    _require(enabled(sale.get("activo")), "La venta no quedó activa.")
    _require("CAENumero" in sale and not str(sale["CAENumero"] or "").strip(),
             "Falta evidencia de comprobante interno sin CAE.")
    by_ref = {product.ref: product for product in products}
    _require(len(by_ref) == len(products) and set(before.stock) == {p.id for p in products},
             "La evidencia de stock no incluye exactamente los productos del recorrido.")
    expected_lines, expected_stock = [], []
    quantities = Counter()
    for line in lines:
        product = by_ref[line.product]
        quantities[product.id] += Decimal(line.quantity)
        expected_lines.append((Decimal(product.id), Decimal(line.quantity), Decimal(line.price), line.gross,
                               Decimal(line.discount), Decimal(line.offer_id), Decimal(line.manual),
                               Decimal(line.price_list_id)))
        expected_stock.append((Decimal(product.id), -Decimal(line.quantity)))
    observed_lines = []
    for row in rows["ventas_cuerpo"]:
        _equal(row, "venId", sale_id)
        _require(enabled(row.get("activo")), "Hay un renglón inactivo.")
        for key in ("Puntos_Acumulados", "Puntos_Utilizados"):
            _equal(row, key, 0)
        observed_lines.append(tuple(_number(row, key) for key, _ in _LINE_FIELDS))
    _assert_line_items(products, expected_lines, observed_lines)
    if usd:
        for key, value in {"ID_Moneda": 1, "Cotizacion_USD": Decimal(exchange_rate), "ID_Moneda_Pago": 1,
                           "Pagado_Original": received, "ID_Moneda_Vuelto": 1,
                           "Vuelto_Original": received - total}.items():
            _equal(sale, key, value)
        by_id = {by_ref[line.product].id: line for line in lines}
        for row in rows["ventas_cuerpo"]:
            line = by_id[_number(row, "vecCodigo")]
            for key, value in {"ID_Moneda": 2, "vecPrecioOriginal": Decimal(line.original_price),
                               "vecTotalOriginal": Decimal(line.original_price) * Decimal(line.quantity),
                               "vecOfertaOriginal": Decimal(line.original_discount),
                               "vecOfertaManualOriginal": 0, "vecImporteIvaOriginal": 0,
                               "vecOtrosImpuestosOriginal": 0}.items():
                _equal(row, key, value)
    observed_stock = []
    for row in rows["movimientos_articulos"]:
        _equal(row, "ID_Venta", sale_id)
        _require(enabled(row.get("activo")), "Hay un movimiento de stock inactivo.")
        observed_stock.append((_number(row, "moaArticuloCodigo"), _number(row, "moaCantidad")))
    _require(Counter(observed_stock) == Counter(expected_stock), "Los movimientos de stock no coinciden.")
    for product in products:
        delta = after.stock[product.id] - before.stock[product.id]
        _require(delta == -quantities[product.id], "Stock incorrecto en un producto incluido o excluido.",
                 expected=str(-quantities[product.id]), observed=str(delta))
    cash = rows["movimientos_finanzas"][0]
    for key, value in {"ID_Venta": sale_id, "ID_VentaPago": 0, "mofPago": payment_id, "mofIngreso": total,
                       "mofEgreso": 0, "mofEstado": 1, "mofConcepto": 2}.items():
        _equal(cash, key, value)
    _require(enabled(cash.get("activo")), "El movimiento de caja no quedó activo.")
    _require(after.cash - before.cash == total, "El saldo del medio de pago no recibió el neto de la canasta.",
             expected=str(total), observed=str(after.cash - before.cash))
    diagnostic("Canasta completa comprobada: venta, renglones, ofertas, stock y cobro único",
               total_ars=str(total), row_count=len(lines))
    return sale_id


class BasketOracle(XGestionOracle):
    def __init__(self, connection, fixtures, products, payment_id=None):
        super().__init__(connection, fixtures)
        self.products = products
        self.payment_id = payment_id or fixtures["sale"]["cash_payment_id"]

    def validate_currency_schema(self):
        from products.xgestion.offer_journeys.usd import LINE_COLUMNS, SALE_COLUMNS

        for table, required in (("ventas", SALE_COLUMNS), ("ventas_cuerpo", LINE_COLUMNS)):
            found = self.query("SELECT COLUMN_NAME AS name FROM information_schema.COLUMNS "
                               "WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME=%s", (table,))
            names = {str(row.get("name", "")).lower() for row in found}
            if not {name.lower() for name in required} <= names:
                raise QAError(f"Paquete incompatible con ofertas-usd-v1: faltan snapshots monetarios en {table}. "
                              "Actualizar el paquete QA antes de ejecutar; no se migra desde el test.")

    def snapshot(self):
        from products.xgestion.offer_journeys.usd import LINE_COLUMNS, SALE_COLUMNS

        usd = any(product.currency == "USD" for product in self.products)
        rows = {}
        for table, columns in STATE_COLUMNS.items():
            if table == "ventas":
                columns += ",CAENumero"
                if usd:
                    columns += "," + ",".join(SALE_COLUMNS)
            elif table == "ventas_cuerpo":
                columns += ",ID_ListaPrecio"
                if usd:
                    columns += "," + ",".join(LINE_COLUMNS)
            rows[table] = tuple(self.query(f"SELECT {columns} FROM {table} "
                                          "WHERE Empresa=%s AND Sucursal=%s AND Computadora=%s", self.scope))
        stock = {}
        for product in self.products:
            found = self.query(
                "SELECT COALESCE(SUM(moaCantidad),0) AS total FROM movimientos_articulos "
                "WHERE Empresa=%s AND Sucursal=%s AND moaArticuloCodigo=%s "
                "AND YEAR(moaFechaHora)=YEAR(CURDATE()) AND activo=1", self.scope[:2] + (product.id,))
            stock[product.id] = _number(found[0], "total")
        cash = self.query(
            "SELECT COALESCE(SUM(mofIngreso-mofEgreso),0) AS total FROM movimientos_finanzas "
            "WHERE Empresa=%s AND Sucursal=%s AND Computadora=%s AND mofPago=%s AND activo=1",
            self.scope + (self.payment_id,))
        return BasketSnapshot(frozenset(row["venId"] for row in rows["ventas"]), stock,
                              _number(cash[0], "total"), rows)


