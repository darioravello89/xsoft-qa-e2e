---
{"id":"XG-FIN-014","title":"Cerrar turno con venta USD cobrada en ARS","product":"xgestion","module":"conciliacion","priority":"P0","tags":["xgestion","regression","circuitos-completos","conciliacion","p0","escritura","caja","libro-diario","stock"],"status":"implemented","test":"products/xgestion/suites/circuitos.robot","seed":"catalogo-comercial-v1"}
---

# XG-FIN-014 — Cerrar turno con venta USD cobrada en ARS

## Objetivo y estado

Automatizado (`implemented`); validación real del JAR pendiente.

Seguir la operación completa desde las acciones del usuario hasta sus saldos, sin duplicaciones.

## Precondiciones y datos

Windows QA exclusivo/offline y escritorio desbloqueado; JAR y paquete identificados, perfil `circuitos-comerciales-v1`, tasa 1500 ARS/USD, IVA 0%, comprobante 99, efectivo ARS ID 1, sin ofertas, listas, financiación ni impresión.

Seed `catalogo-comercial-v1`, productos QA-CIR, controles y configuración del [circuito completo](../../docs/circuitos-completos.md). Sin VM, paquete y calibración no hay aceptación real.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Abrir Turno con credenciales QA; cancelar el diálogo de ingreso inicial. | Una apertura activa, fondo cero, sin ingreso de dinero. |
| 2 | Vender una unidad QA-CIR-USD-FIJO; cancelar y retomar cobro ARS exacto. | Total ARS 150.000, stock −1 y un ingreso neto; cancelación sin efectos. |
| 3 | Cerrar Turno con credenciales QA. | Un cierre asociado a la apertura; no repite venta, stock ni finanzas. |
| 4 | Leer puesto, turno y rubros del balance; salir con Escape. | Efectivo/total ARS 150.000; ingresos iniciales, egresos y otros medios 0. No imprime. |
| 5 | Abrir nuevamente el reporte del turno cerrado y salir. | Mismos importes y registros; ningún efecto adicional. |

## Variantes y límites

Esta ficha tiene **un perfil obligatorio**, con todos los pasos anteriores. Otras cotizaciones, impuestos, promociones/listas, anulación, recepción parcial, deuda/cobro USD, cierre ciego y concurrencia siguen pendientes en la [matriz de variantes](../../docs/circuitos-completos.md#variantes-que-aún-faltan). No reemplaza las fichas FIN-001..010, REM, CCC o CAJ.

## Evidencia y recuperación

INFO: resultado y fallo detallado; DEBUG: acciones de negocio; TRACE: diagnóstico saneado. Comparar identidades y deltas de venta, stock, finanzas, deuda, precios y turnos según cada paso. No publicar filas completas, credenciales ni capturas de autenticación. Conservar informe privado y restaurar baseline desde qa.cmd antes de repetir; no corregir saldos con SQL.

## Anexo técnico

Fuente XGestion2 `0adea394095e4ceff54344bf38cbf21b7c01a5e8`: FormVenta/TicketVenta, FormCargaDeRemito/Compra/CompraDetalle/Articulo, CtaCteCliente, MovimientoFinanzas y Turno/FormCierreDeCaja. Oráculos en `circuits/oracles.py`; consultas SELECT por Empresa/Sucursal/Computadora e identidad de documento. Libro Diario se verifica en persistencia; FIN-014 también lee el balance en UI. Guardar SHA256, versión, paquete, perfil, fecha y reporte para acreditar validación real.
