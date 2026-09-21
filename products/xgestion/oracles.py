"""Oráculos SELECT parametrizados. No crean, corrigen ni limpian datos del ERP."""

import hashlib
import json
from dataclasses import dataclass, field
from decimal import Decimal
from time import monotonic

from framework.events import assertion_failed, diagnostic


@dataclass(frozen=True)
class Snapshot:
    sale_ids: frozenset[int]
    stock: Decimal
    cash: Decimal
    business_state: tuple[tuple[str, int, str], ...] = field(default=(), repr=False)


# Proyecciones comerciales sin nombres, notas, credenciales ni metadatos de sincronización.
# ID_ComputadoraModifica e ID_Venta/ID_VentaPago pertenecen al esquema migrado de 189-lts.
STATE_COLUMNS = {
    "ventas": "venId,venTotal,venEstado,venUsuario,venPago,ID_TipoComprobante,Pagado,Vuelto,esPagoMultiple,activo",
    "ventas_cuerpo": "vecId,item,venId,vecCodigo,vecCantidad,vecPrecio,vecTotal,activo",
    "ventas_pagos": "ID_VentaPago,ID_ComputadoraModifica,ID_Venta,ID_Pago,Cantidad,Descuento,EsPagoACobrar,esCobrado,activo",
    "movimientos_articulos": "moaId,ID_ComputadoraModifica,ID_Venta,moaArticuloCodigo,moaCantidad,activo",
    "movimientos_finanzas": "mofId,ID_Venta,ID_VentaPago,mofPago,mofIngreso,mofEgreso,mofEstado,mofConcepto,activo",
}


def _record_state(table, rows):
    # Orden estable y multiplicidad conservada: dos filas iguales no desaparecen como en un set.
    encoded = sorted(json.dumps(row, sort_keys=True, default=str, separators=(",", ":")) for row in rows)
    digest = hashlib.sha256(json.dumps(encoded, separators=(",", ":")).encode("utf-8")).hexdigest()
    return table, len(rows), digest


def decimal(value):
    return Decimal(str(value or 0))


def enabled(value):
    return value in (True, 1, b"\x01")


def _require(condition, message, *, expected=None, observed=None):
    if not condition:
        assertion_failed(message, expected=expected, observed=observed)
        raise AssertionError(message)


def _assert_unchanged(before, after, action):
    _require(before.sale_ids == after.sale_ids, f"{action} creó o eliminó ventas.",
             expected="0 ventas creadas o eliminadas",
             observed=f"{len(after.sale_ids - before.sale_ids)} creadas, {len(before.sale_ids - after.sale_ids)} eliminadas")
    _require(before.stock == after.stock, f"{action} modificó stock.",
             expected="0 unidades", observed=f"{after.stock - before.stock} unidades")
    _require(before.cash == after.cash, f"{action} modificó caja.",
             expected="0 ARS", observed=f"{after.cash - before.cash} ARS")
    _require(before.business_state == after.business_state, f"{action} modificó registros de negocio.",
             expected="Sin altas, bajas ni cambios en las proyecciones comerciales del contexto QA",
             observed="Cambió el estado de ventas, detalles, pagos, movimientos de stock o caja")


def assert_unchanged(before, after):
    """Comparar una pausa/cancelación o segunda operación; no interpreta su estado visual."""
    _assert_unchanged(before, after, "La operación")
    diagnostic("Estado comercial comprobado sin cambios en ventas, detalles, pagos, stock ni caja")


def assert_cancelled(before, after):
    _assert_unchanged(before, after, "Cancelar")
    diagnostic("Cancelación comprobada sin cambios en ventas, detalles, pagos, stock ni caja")


def _assert_new_record_counts(before, after):
    # Los snapshots reales siempre incluyen las cinco tablas; conservar construcción histórica de tres campos.
    if not before.business_state and not after.business_state:
        return
    old = {table: count for table, count, _ in before.business_state}
    new = {table: count for table, count, _ in after.business_state}
    _require(set(old) == set(new) == set(STATE_COLUMNS), "Falta evidencia completa de registros comerciales.",
             expected="Conteos de las cinco tablas antes y después", observed="Snapshot incompleto")
    for table, expected in {"ventas": 1, "ventas_cuerpo": 1, "ventas_pagos": 0,
                            "movimientos_articulos": 1, "movimientos_finanzas": 1}.items():
        observed = new[table] - old[table]
        _require(observed == expected, f"Cantidad inesperada de registros nuevos en {table}.",
                 expected=f"Variación {expected} registros", observed=f"Variación {observed} registros")


def assert_sale(fixtures, before, after, sale, lines, payments, sale_stock, sale_cash, *,
                received=Decimal("2000"), expected_sale_id=None):
    created = after.sale_ids - before.sale_ids
    _require(len(created) == 1 and before.sale_ids <= after.sale_ids, "Debe persistirse exactamente una venta nueva.",
             expected="1 venta nueva y 0 eliminadas",
             observed=f"{len(created)} nuevas, {len(before.sale_ids - after.sale_ids)} eliminadas")
    sale_id = next(iter(created))
    _require(expected_sale_id is None or sale_id == expected_sale_id,
             "Cambió la identidad de la venta cobrada al continuar la operación.",
             expected="Misma venta previamente comprobada", observed="Identidad diferente")
    _require(sale and sale["venId"] == sale_id, "No se encontró la venta nueva por su PK completa.",
             expected="Venta de esta operación", observed="Ausente" if not sale else "Identidad diferente")
    product = fixtures["product"]
    cash_id = fixtures["sale"]["cash_payment_id"]
    quantity = decimal(product["quantity"])
    price = decimal(product["unit_price"])
    total = quantity * price
    received = decimal(received)
    _require(received.is_finite() and received >= total, "El importe recibido no cubre la venta simple.",
             expected=f"Al menos {total} ARS", observed=f"{received} ARS")
    _require(sale["venEstado"] == 1 and enabled(sale["activo"]), "La venta no quedó cerrada y activa.",
             expected="Cerrada y activa", observed=f"Estado={sale['venEstado']}; activa={enabled(sale['activo'])}")
    _require(sale["venUsuario"] == fixtures["context"]["usuario_id"], "La venta corresponde a otro usuario.",
             expected="Usuario QA de esta operación", observed="Otro usuario")
    _require(sale["venPago"] == cash_id, "La venta no usa el efectivo del fixture.",
             expected="Medio de pago efectivo del perfil", observed="Otro medio de pago")
    _require(not enabled(sale["esPagoMultiple"]), "La venta simple quedó como pago múltiple.",
             expected="Pago simple", observed="Pago múltiple")
    _require(decimal(sale["Pagado"]) == received and decimal(sale["Vuelto"]) == received - total,
             "El recibido o vuelto persistidos son incorrectos.",
             expected=f"Recibido {received} ARS; vuelto {received - total} ARS",
             observed=f"Recibido {decimal(sale['Pagado'])} ARS; vuelto {decimal(sale['Vuelto'])} ARS")
    fiscal_cae = bool(str(sale.get("CAENumero") or "").strip())
    _require(sale["ID_TipoComprobante"] == 99 and not fiscal_cae, "Se detectó comprobante fiscal o CAE.",
             expected="Comprobante interno 99 sin CAE",
             observed=f"Tipo={sale['ID_TipoComprobante']}; CAE presente={fiscal_cae}")
    _require(decimal(sale["venTotal"]) == total, "Total persistido distinto de 2000 ARS.",
             expected=f"{total} ARS", observed=f"{decimal(sale['venTotal'])} ARS")
    _require(len(lines) == 1 and enabled(lines[0]["activo"]) and str(lines[0]["vecCodigo"]) == str(product["id"]),
             "El detalle no corresponde al producto fixture.", expected="1 renglón del producto QA",
             observed=f"{len(lines)} renglones; producto coincide={bool(lines) and str(lines[0]['vecCodigo']) == str(product['id'])}")
    line = lines[0]
    _require(decimal(line["vecCantidad"]) == quantity, "Cantidad persistida incorrecta.",
             expected=str(quantity), observed=str(decimal(line["vecCantidad"])))
    _require(decimal(line["vecPrecio"]) == price and decimal(line["vecTotal"]) == total,
             "Precio o subtotal del detalle incorrectos.", expected=f"Precio {price} ARS; subtotal {total} ARS",
             observed=f"Precio {decimal(line['vecPrecio'])} ARS; subtotal {decimal(line['vecTotal'])} ARS")
    # El ERP reserva ventas_pagos para pagos desglosados. El efectivo simple vive en ventas y caja.
    _require(not payments, "El cobro simple generó registros inesperados en ventas_pagos.",
             expected="0 registros de pago múltiple, activos o inactivos", observed=f"{len(payments)} registros")
    _require(len(sale_stock) == 1, "Debe existir un solo movimiento de stock por esta venta simple.",
             expected="1 movimiento de stock", observed=f"{len(sale_stock)} movimientos")
    stock = sale_stock[0]
    _require(enabled(stock["activo"]) and stock["moaArticuloCodigo"] == product["id"],
             "El movimiento de stock está inactivo o corresponde a otro producto.",
             expected="Movimiento activo del producto QA", observed="Estado o producto incorrecto")
    _require(after.stock - before.stock == -quantity and decimal(stock["moaCantidad"]) == -quantity,
             "Stock no descontó exactamente dos unidades por esta venta.", expected=f"Variación {-quantity} unidades",
             observed=f"Global={after.stock - before.stock}; venta={decimal(stock['moaCantidad'])} unidades")
    _require(len(sale_cash) == 1, "Debe existir un solo movimiento de caja por esta venta simple.",
             expected="1 movimiento de caja", observed=f"{len(sale_cash)} movimientos")
    cash = sale_cash[0]
    _require(cash["mofPago"] == cash_id, "El movimiento de caja no usa el efectivo del fixture.",
             expected="Medio de pago efectivo del perfil", observed="Otro medio de pago")
    _require(enabled(cash["activo"]) and cash["mofEstado"] == 1 and cash["mofConcepto"] == 2
             and cash["ID_VentaPago"] == 0, "El movimiento de caja no corresponde al cobro simple activo.",
             expected="Ingreso activo de venta simple", observed="Estado, concepto u origen diferente")
    _require(decimal(cash["mofIngreso"]) == total and decimal(cash["mofEgreso"]) == 0,
             "Caja no registró el ingreso neto de la venta simple.",
             expected=f"Ingreso {total} ARS; egreso 0 ARS",
             observed=f"Ingreso {decimal(cash['mofIngreso'])} ARS; egreso {decimal(cash['mofEgreso'])} ARS")
    _require(after.cash - before.cash == total,
             "Caja no recibió exactamente 2000 ARS por esta venta.", expected=f"Variación {total} ARS",
             observed=f"Global={after.cash - before.cash} ARS")
    _assert_new_record_counts(before, after)
    diagnostic("Venta, detalle, pago, stock y caja comprobados", total_ars=str(total), quantity=str(quantity))
    return sale_id


class XGestionOracle:
    """La conexión pertenece al runner de la instancia QA; cada lectura usa autocommit."""

    def __init__(self, connection, fixtures):
        self.connection = connection
        self.fixtures = fixtures
        context = fixtures["context"]
        self.scope = (context["empresa"], context["sucursal"], context["computadora"])

    def query(self, statement, params):
        if not statement.lstrip().upper().startswith("SELECT "):
            raise ValueError("El oráculo sólo acepta SELECT.")
        started = monotonic()
        with self.connection.cursor() as cursor:
            cursor.execute(statement, params)
            rows = list(cursor.fetchall())
        diagnostic("Lectura de persistencia completada", row_count=len(rows),
                   duration_seconds=round(monotonic() - started, 3))
        return rows

    def snapshot(self):
        rows = self.query(f"SELECT {STATE_COLUMNS['ventas']} FROM ventas "
                          "WHERE Empresa=%s AND Sucursal=%s AND Computadora=%s", self.scope)
        stock = self.query(
            "SELECT COALESCE(SUM(moaCantidad),0) AS total FROM movimientos_articulos "
            "WHERE Empresa=%s AND Sucursal=%s AND moaArticuloCodigo=%s AND YEAR(moaFechaHora)=YEAR(CURDATE()) AND activo=1",
            self.scope[:2] + (self.fixtures["product"]["id"],),
        )[0]["total"]
        cash = self.query(
            "SELECT COALESCE(SUM(mofIngreso-mofEgreso),0) AS total FROM movimientos_finanzas "
            "WHERE Empresa=%s AND Sucursal=%s AND Computadora=%s AND mofPago=%s AND activo=1",
            self.scope + (self.fixtures["sale"]["cash_payment_id"],),
        )[0]["total"]
        state = [_record_state("ventas", rows)]
        for table, columns in STATE_COLUMNS.items():
            if table != "ventas":
                business_rows = self.query(f"SELECT {columns} FROM {table} "
                                           "WHERE Empresa=%s AND Sucursal=%s AND Computadora=%s", self.scope)
                state.append(_record_state(table, business_rows))
        return Snapshot(frozenset(row["venId"] for row in rows), decimal(stock), decimal(cash), tuple(state))

    def verify_sale(self, before, *, received=Decimal("2000"), expected_sale_id=None):
        after = self.snapshot()
        created = after.sale_ids - before.sale_ids
        _require(len(created) == 1, "Debe persistirse exactamente una venta nueva.",
                 expected="1 venta nueva", observed=f"{len(created)} ventas nuevas")
        pk = self.scope + (next(iter(created)),)
        sales = self.query(
            "SELECT venId,venTotal,venEstado,venUsuario,venPago,ID_TipoComprobante,CAENumero,activo,"
            "Pagado,Vuelto,esPagoMultiple "
            "FROM ventas WHERE Empresa=%s AND Sucursal=%s AND Computadora=%s AND venId=%s", pk)
        lines = self.query(
            "SELECT vecId,item,vecCodigo,vecCantidad,vecPrecio,vecTotal,activo FROM ventas_cuerpo "
            "WHERE Empresa=%s AND Sucursal=%s AND Computadora=%s AND venId=%s", pk)
        payments = self.query(
            "SELECT ID_VentaPago,ID_ComputadoraModifica,activo FROM ventas_pagos "
            "WHERE Empresa=%s AND Sucursal=%s AND Computadora=%s AND ID_Venta=%s", pk)
        stock = self.query(
            "SELECT moaId,ID_ComputadoraModifica,moaArticuloCodigo,moaCantidad,activo FROM movimientos_articulos "
            "WHERE Empresa=%s AND Sucursal=%s AND Computadora=%s AND ID_Venta=%s", pk)
        cash = self.query(
            "SELECT mofId,mofPago,mofIngreso,mofEgreso,mofEstado,mofConcepto,ID_VentaPago,activo FROM movimientos_finanzas "
            "WHERE Empresa=%s AND Sucursal=%s AND Computadora=%s AND ID_Venta=%s", pk)
        return assert_sale(self.fixtures, before, after, sales[0] if sales else None, lines, payments, stock, cash,
                           received=received, expected_sale_id=expected_sale_id)
