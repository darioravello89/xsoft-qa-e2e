---
{"id":"XG-FIN-013","title":"Recibir remito mixto actualizar costos y vender","product":"xgestion","module":"conciliacion","priority":"P0","tags":["xgestion","regression","circuitos-completos","conciliacion","p0","escritura","remitos","stock"],"status":"implemented","test":"products/xgestion/suites/circuitos.robot","seed":"catalogo-comercial-v1"}
---

# XG-FIN-013 — Recibir remito mixto actualizar costos y vender

## Objetivo y estado

Automatizado (`implemented`); validación real del JAR pendiente.

Seguir la operación completa desde las acciones del usuario hasta sus saldos, sin duplicaciones.

## Precondiciones y datos

Windows QA exclusivo/offline y escritorio desbloqueado; JAR y paquete identificados, perfil `circuitos-comerciales-v1`, tasa 1500 ARS/USD, IVA 0%, comprobante 99, efectivo ARS ID 1, sin ofertas, listas, financiación ni impresión.

Seed `catalogo-comercial-v1`, productos QA-CIR, controles y configuración del [circuito completo](../../docs/circuitos-completos.md). Sin VM, paquete y calibración no hay aceptación real.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Elegir proveedor QA-SEED-PROVEEDOR y comprobante QA-CIR-REM-001, pagado 0. | Nuevo borrador del contexto QA; sin deuda ni recepción todavía. |
| 2 | Cargar dos unidades de ARS-FIJO, USD-FIJO, ARS-CALCULADO, USD-CALCULADO del prefijo QA-CIR-. | Costos 600 ARS, 60 USD, 600 ARS y 60 USD; total ARS 362.400, Suma stock y Actualiza precio activos. |
| 3 | Cargar Remito y rechazar la confirmación. | Borrador conservado; stock, costos, precios, caja y deuda sin cambios. |
| 4 | Confirmar Cargar Remito y enviar el importe a cuenta corriente del proveedor. | Una compra cerrada, cuatro ingresos +2; costos 600/60; precios fijos 1000/100, calculados 1200/120. Una deuda proveedor ARS 362.400; sin egreso de caja. |
| 5 | Vender una unidad QA-CIR-USD-CALCULADO a USD 120; cancelar y retomar cobro exacto. | ARS 180.000; una venta y un ingreso de caja; stock −1 de ese producto. Compra y deuda proveedor no cambian. |

## Variantes y límites

Esta ficha tiene **un perfil obligatorio**, con todos los pasos anteriores. Otras cotizaciones, impuestos, promociones/listas, anulación, recepción parcial, deuda/cobro USD, cierre ciego y concurrencia siguen pendientes en la [matriz de variantes](../../docs/circuitos-completos.md#variantes-que-aún-faltan). No reemplaza las fichas FIN-001..010, REM, CCC o CAJ.

## Evidencia y recuperación

INFO: resultado y fallo detallado; DEBUG: acciones de negocio; TRACE: diagnóstico saneado. Comparar identidades y deltas de venta, stock, finanzas, deuda, precios y turnos según cada paso. No publicar filas completas, credenciales ni capturas de autenticación. Conservar informe privado y restaurar baseline desde qa.cmd antes de repetir; no corregir saldos con SQL.

## Anexo técnico

Fuente XGestion2 `0adea394095e4ceff54344bf38cbf21b7c01a5e8`: FormVenta/TicketVenta, FormCargaDeRemito/Compra/CompraDetalle/Articulo, CtaCteCliente, MovimientoFinanzas y Turno/FormCierreDeCaja. Oráculos en `circuits/oracles.py`; consultas SELECT por Empresa/Sucursal/Computadora e identidad de documento. Libro Diario se verifica en persistencia; FIN-014 también lee el balance en UI. Guardar SHA256, versión, paquete, perfil, fecha y reporte para acreditar validación real.
