"""Oráculos SELECT parametrizados. No crean, corrigen ni limpian datos del ERP."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Snapshot:
    sale_ids: frozenset[int]
    stock: Decimal
    cash: Decimal


def decimal(value):
    return Decimal(str(value or 0))


def enabled(value):
    return value in (True, 1, b"\x01")


def _require(condition, message):
    if not condition:
        raise AssertionError(message)


def assert_cancelled(before, after):
    _require(before.sale_ids == after.sale_ids, "Cancelar creó o eliminó ventas.")
    _require(before.stock == after.stock, "Cancelar modificó stock.")
    _require(before.cash == after.cash, "Cancelar modificó caja.")


def assert_sale(fixtures, before, after, sale, lines, payments, sale_stock, sale_cash):
    created = after.sale_ids - before.sale_ids
    _require(len(created) == 1 and before.sale_ids <= after.sale_ids, "Debe persistirse exactamente una venta nueva.")
    sale_id = next(iter(created))
    _require(sale and sale["venId"] == sale_id, "No se encontró la venta nueva por su PK completa.")
    product = fixtures["product"]
    cash_id = fixtures["sale"]["cash_payment_id"]
    quantity = decimal(product["quantity"])
    price = decimal(product["unit_price"])
    total = quantity * price
    _require(sale["venEstado"] == 1 and enabled(sale["activo"]), "La venta no quedó cerrada y activa.")
    _require(sale["venUsuario"] == fixtures["context"]["usuario_id"], "La venta corresponde a otro usuario.")
    _require(sale["venPago"] == cash_id, "La venta no usa el efectivo del fixture.")
    _require(sale["ID_TipoComprobante"] == 99 and not str(sale.get("CAENumero") or "").strip(), "Se detectó comprobante fiscal o CAE.")
    _require(decimal(sale["venTotal"]) == total, "Total persistido distinto de 2000 ARS.")
    _require(len(lines) == 1 and str(lines[0]["vecCodigo"]) == str(product["id"]), "El detalle no corresponde al producto fixture.")
    line = lines[0]
    _require(decimal(line["vecCantidad"]) == quantity, "Cantidad persistida incorrecta.")
    _require(decimal(line["vecPrecio"]) == price and decimal(line["vecTotal"]) == total, "Precio o subtotal del detalle incorrectos.")
    _require(payments and all(p["ID_Pago"] == cash_id and not enabled(p["EsPagoACobrar"]) for p in payments), "El cobro no es efectivo inmediato.")
    _require(sum((decimal(p["Cantidad"]) for p in payments), Decimal(0)) == total, "Pagos persistidos distintos del total.")
    _require(after.stock - before.stock == -quantity and decimal(sale_stock) == -quantity, "Stock no descontó exactamente dos unidades por esta venta.")
    _require(after.cash - before.cash == total and decimal(sale_cash) == total, "Caja no recibió exactamente 2000 ARS por esta venta.")
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
        with self.connection.cursor() as cursor:
            cursor.execute(statement, params)
            return list(cursor.fetchall())

    def snapshot(self):
        rows = self.query("SELECT venId FROM ventas WHERE Empresa=%s AND Sucursal=%s AND Computadora=%s", self.scope)
        stock = self.query(
            "SELECT COALESCE(SUM(moaCantidad),0) AS total FROM movimientos_articulos "
            "WHERE Empresa=%s AND Sucursal=%s AND moaArticuloCodigo=%s AND YEAR(moaFechaHora)=YEAR(CURDATE())",
            self.scope[:2] + (self.fixtures["product"]["id"],),
        )[0]["total"]
        cash = self.query(
            "SELECT COALESCE(SUM(mofIngreso-mofEgreso),0) AS total FROM movimientos_finanzas "
            "WHERE Empresa=%s AND Sucursal=%s AND Computadora=%s AND mofPago=%s AND activo=1",
            self.scope + (self.fixtures["sale"]["cash_payment_id"],),
        )[0]["total"]
        return Snapshot(frozenset(row["venId"] for row in rows), decimal(stock), decimal(cash))

    def verify_sale(self, before):
        after = self.snapshot()
        created = after.sale_ids - before.sale_ids
        _require(len(created) == 1, "Debe persistirse exactamente una venta nueva.")
        pk = self.scope + (next(iter(created)),)
        sales = self.query(
            "SELECT venId,venTotal,venEstado,venUsuario,venPago,ID_TipoComprobante,CAENumero,activo "
            "FROM ventas WHERE Empresa=%s AND Sucursal=%s AND Computadora=%s AND venId=%s", pk)
        lines = self.query(
            "SELECT vecCodigo,vecCantidad,vecPrecio,vecTotal FROM ventas_cuerpo "
            "WHERE Empresa=%s AND Sucursal=%s AND Computadora=%s AND venId=%s AND activo=1", pk)
        payments = self.query(
            "SELECT ID_Pago,Cantidad,EsPagoACobrar FROM ventas_pagos "
            "WHERE Empresa=%s AND Sucursal=%s AND Computadora=%s AND ID_Venta=%s AND activo=1", pk)
        stock = self.query(
            "SELECT COALESCE(SUM(moaCantidad),0) AS total FROM movimientos_articulos "
            "WHERE Empresa=%s AND Sucursal=%s AND Computadora=%s AND ID_Venta=%s AND moaArticuloCodigo=%s",
            pk + (self.fixtures["product"]["id"],))[0]["total"]
        cash = self.query(
            "SELECT COALESCE(SUM(mofIngreso-mofEgreso),0) AS total FROM movimientos_finanzas "
            "WHERE Empresa=%s AND Sucursal=%s AND Computadora=%s AND ID_Venta=%s AND mofPago=%s AND activo=1",
            pk + (self.fixtures["sale"]["cash_payment_id"],))[0]["total"]
        return assert_sale(self.fixtures, before, after, sales[0] if sales else None, lines, payments, stock, cash)
