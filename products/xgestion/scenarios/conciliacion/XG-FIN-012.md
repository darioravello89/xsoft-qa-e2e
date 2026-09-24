---
{"id":"XG-FIN-012","title":"Vender productos USD a cuenta corriente y cancelar la deuda","product":"xgestion","module":"conciliacion","priority":"P0","tags":["xgestion","regression","circuitos-completos","conciliacion","p0","escritura","cuenta-corriente","ctacte-clientes","caja","stock"],"status":"planned"}
---

# XG-FIN-012 — Vender productos USD a cuenta corriente y cancelar la deuda

## Objetivo y estado

**Pendiente (`planned`), bloqueado por XG-ACC-010. El usuario rechazó el doble clic.** No tiene Robot ni se ejecuta. `3f8648035` incorpora Enter en el listado; falta validar su identidad/foco en el JAR con [KEY-001](../atajos-listados/XG-KEY-001.md) antes de habilitar este circuito.

Seguir la operación completa desde las acciones del usuario hasta sus saldos, sin duplicaciones.

## Precondiciones y datos

Windows QA exclusivo/offline y escritorio desbloqueado; JAR y paquete identificados, perfil `circuitos-comerciales-v1`, tasa 1500 ARS/USD, IVA 0%, comprobante 99, efectivo ARS ID 1, sin ofertas, listas, financiación ni impresión.

Seed `catalogo-comercial-v1`, productos QA-CIR, controles y configuración del [circuito completo](../../docs/circuitos-completos.md). El paquete todavía debe preparar dos clientes QA identificados, sin deuda, con permiso de crédito; el seed no los crea. Sin VM, paquete y calibración no hay aceptación real.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Seleccionar cliente QA exclusivo y vender dos unidades USD 100. | Total ARS 300.000; perfil de deuda ARS, sin ofertas/listas/impuestos. |
| 2 | Enviar a cuenta corriente con anticipo ARS 50.000. | Una venta, stock −2, cargo 300.000 y anticipo 50.000; saldo 250.000 y dinero recibido 50.000. |
| 3 | Abrir la cuenta por Enter una vez validado KEY-001; iniciar abono 100.000 y cancelar. | Sin cambios de saldo, caja, venta ni stock; otro cliente permanece intacto. |
| 4 | Registrar abono 100.000 y luego 150.000. | Saldo 150.000 y luego 0; ingreso acumulado 300.000; no se crean ventas ni salidas de stock adicionales. |
| 5 | Volver a consultar la cuenta y Libro Diario. | Mismas identidades y saldos; monedas originales y operativas coherentes. |

## Variantes y límites

Esta ficha tiene **un perfil obligatorio**, con todos los pasos anteriores. Otras cotizaciones, impuestos, promociones/listas, anulación, recepción parcial, deuda/cobro USD, cierre ciego y concurrencia siguen pendientes en la [matriz de variantes](../../docs/circuitos-completos.md#variantes-que-aún-faltan). No reemplaza las fichas FIN-001..010, REM, CCC o CAJ.

## Evidencia y recuperación

INFO: resultado y fallo detallado; DEBUG: acciones de negocio; TRACE: diagnóstico saneado. Comparar identidades y deltas de venta, stock, finanzas, deuda, precios y turnos según cada paso. No publicar filas completas, credenciales ni capturas de autenticación. Conservar informe privado y restaurar baseline desde qa.cmd antes de repetir; no corregir saldos con SQL.

## Anexo técnico

Fuente XGestion2 `0adea394095e4ceff54344bf38cbf21b7c01a5e8`: FormVenta/TicketVenta, FormCargaDeRemito/Compra/CompraDetalle/Articulo, CtaCteCliente, MovimientoFinanzas y Turno/FormCierreDeCaja. Oráculos en `circuits/oracles.py`; consultas SELECT por Empresa/Sucursal/Computadora e identidad de documento. Libro Diario se verifica en persistencia; FIN-014 también lee el balance en UI. Guardar SHA256, versión, paquete, perfil, fecha y reporte para acreditar validación real.
