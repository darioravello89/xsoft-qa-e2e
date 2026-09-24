---
{"id":"XG-FIN-011","title":"Vender productos USD y conciliar stock y Libro Diario","product":"xgestion","module":"conciliacion","priority":"P0","tags":["xgestion","regression","circuitos-completos","conciliacion","p0","escritura","libro-diario","stock","caja"],"status":"implemented","test":"products/xgestion/suites/circuitos.robot","seed":"catalogo-comercial-v1"}
---

# XG-FIN-011 — Vender productos USD y conciliar stock y Libro Diario

## Objetivo y estado

Automatizado (`implemented`); validación real del JAR pendiente.

Seguir la operación completa desde las acciones del usuario hasta sus saldos, sin duplicaciones.

## Precondiciones y datos

Windows QA exclusivo/offline y escritorio desbloqueado; JAR y paquete identificados, perfil `circuitos-comerciales-v1`, tasa 1500 ARS/USD, IVA 0%, comprobante 99, efectivo ARS ID 1, sin ofertas, listas, financiación ni impresión.

Seed `catalogo-comercial-v1`, productos QA-CIR, controles y configuración del [circuito completo](../../docs/circuitos-completos.md). Sin VM, paquete y calibración no hay aceptación real.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Cargar dos unidades QA-CIR-USD-FIJO a USD 100. | Renglón USD 200, sin descuentos; total ARS 300.000 a cotización 1500. |
| 2 | Abrir cobro efectivo ARS, ingresar 350000 y cancelar. | Vuelto ARS 50.000; se conserva la venta sin registros, stock, deuda ni dinero nuevos. |
| 3 | Retomar el cobro y confirmar una vez. | Una venta activa, stock −2, un ingreso neto al Libro Diario ARS 300.000; monedas y valores originales correctos. |
| 4 | Comprobar venta nueva vacía y salir con Escape. | No repite la venta ni movimientos; compras, precios y cuentas corrientes intactas. |

## Variantes y límites

Esta ficha tiene **un perfil obligatorio**, con todos los pasos anteriores. Otras cotizaciones, impuestos, promociones/listas, anulación, recepción parcial, deuda/cobro USD, cierre ciego y concurrencia siguen pendientes en la [matriz de variantes](../../docs/circuitos-completos.md#variantes-que-aún-faltan). No reemplaza las fichas FIN-001..010, REM, CCC o CAJ.

## Evidencia y recuperación

INFO: resultado y fallo detallado; DEBUG: acciones de negocio; TRACE: diagnóstico saneado. Comparar identidades y deltas de venta, stock, finanzas, deuda, precios y turnos según cada paso. No publicar filas completas, credenciales ni capturas de autenticación. Conservar informe privado y restaurar baseline desde qa.cmd antes de repetir; no corregir saldos con SQL.

## Anexo técnico

Fuente XGestion2 `0adea394095e4ceff54344bf38cbf21b7c01a5e8`: FormVenta/TicketVenta, FormCargaDeRemito/Compra/CompraDetalle/Articulo, CtaCteCliente, MovimientoFinanzas y Turno/FormCierreDeCaja. Oráculos en `circuits/oracles.py`; consultas SELECT por Empresa/Sucursal/Computadora e identidad de documento. Libro Diario se verifica en persistencia; FIN-014 también lee el balance en UI. Guardar SHA256, versión, paquete, perfil, fecha y reporte para acreditar validación real.
