---
{"id":"XG-REC-003","title":"Retomar el cierre de Venta tras un fallo de base anterior al commit","product":"xgestion","module":"recuperacion","tags":["xgestion","regression","recuperacion","ventas","cobros","stock"],"status":"planned"}
---

# XG-REC-003 — Retomar el cierre de Venta tras un fallo de base anterior al commit

## Objetivo

Recuperar un cierre de Venta rechazado antes de persistir definitivamente, conservando una sola venta, un pago y un egreso de stock al reintentar.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P0.** Ver [continuidad operativa](../../docs/continuidad-operativa.md). Sin Robot, seed ni evidencia del JAR. Venta de mostrador simple. [FIN-004](../conciliacion/XG-FIN-004.md) cubre cobro manual de deuda; [RES-040](../restobar/XG-RES-040.md) cubre cuenta/mesa/recetas. Esta ficha verifica la ruta de cierre de FormVenta.

## Precondiciones y datos

- Windows QA exclusivo offline, A stockeable a ARS 1.000, stock 10; A × 2, cobro exacto ARS 2.000, fondo ARS 5.000. Sin deuda, impuestos, cuotas, descuentos, fiscal, impresión ni red.
- Fallo de escritura local preparado antes del commit, en movimiento financiero o de stock; demostrar que la transacción no se confirmó. Inyección, observación del punto de corte y recuperación de conexión aún pendientes.
- Base transaccional del paquete autorizado, pantalla de venta viva y controles calibrados. No generalizar el resultado a otros motores/tablas ni a caída después del commit.
- Todos los fixtures mencionados son sintéticos y **NO están creados por esta entrega**. Faltan paquete, controles accesibles, perfiles y lectores por identidad. No escribir SQL comercial durante el recorrido ni debilitar las guardas del runner.

## Pasos y resultados esperados

| Acción del usuario o responsable QA | Resultado esperado |
| --- | --- |
| Preparar A × 2 e intentar cobrar ARS 2.000 con el fallo activo. | Se informa error o cierre no confirmado; el intento no produce una venta cerrada parcial. |
| Consultar el estado del intento antes de repetir. | No hay pago/venta cerrada definitivos ni egreso de stock: A = 10 y efectivo de la operación = 0. Si no puede verificarse, BLOQUEADO. |
| Desactivar el fallo mediante el procedimiento de laboratorio y retomar la canasta restaurada. | Cantidad 2, precio ARS 1.000 y total ARS 2.000; identidad/estado aptos para volver a intentar según la UI, sin dar por realizada la venta. |
| Cobrar una sola vez y consultar el comprobante. | Una venta cerrada y un cobro de ARS 2.000; A = 8. El efectivo comercial suma ARS 2.000, sin duplicación del intento anterior. |
| Abrir otra venta y cancelarla antes del cobro. | El sistema puede continuar; no arrastra pago, estado cerrado ni renglones de la operación recuperada. |

## Variantes y dependencias

- Fallo financiero y fallo de stock en baselines separados. La restauración de moneda se verifica con perfil USD aparte, sin extrapolar el ARS básico.
- Una desconexión que impida saber si ocurrió el commit pertenece al resultado incierto de REC-004; no forzar el esperado de rollback.
- Si la UI conserva memoria pero la conexión quedó inutilizable, no atribuir reconexión automática: procedimiento pendiente y bloqueo antes de reintentar.

## Evidencia y límites

Cabecera/detalle, pago, stock y total de caja por identidad/delta; punto de fallo y resultado de la transacción. El mensaje de error solo no demuestra ausencia de efectos.

Un perfil, procedimiento u oráculo faltante produce BLOQUEADO antes de la acción dependiente. Ningún resultado observado se adopta como esperado para aprobar. INFO resume y explica fallos; DEBUG muestra acciones de negocio; TRACE agrega diagnóstico saneado. Conservar paso, esperado/observado y causa no determinada si no está demostrada.

## Recuperación

Conciliar el intento antes de volver a cobrar. Si el recurso se recupera y la ausencia está demostrada, reintentar una vez por UI. Ante estado indeterminado, conservar evidencia y detener la operación; no compensar manualmente.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: commit `daa002d597d0fa7380ace204d3727085c52d1415`. Las rutas siguientes son relativas a XGestion2; las clases/tests describen reglas y riesgos, no ejecuciones E2E.

- `src/ModuloVentas/Vistas/FormVenta.java:6293-6380`: transacción, validación, commit, excepciones y restauración de estado.
- `src/ModuloVentas/Entidades/TicketVenta.java:526-562`: stock obligatorio y receta de cierre.
- `test/ModuloVentas/Entidades/TicketVentaRollbackMonedaTest.java` y `test/ModuloVentas/Vistas/FormVentaCierreCobroPolicyTest.java`.

Registrar SHA256/build del JAR, paquete, perfil, ámbito, IDs y reporte privado. No publicar credenciales, configuración completa, copias de bases, payloads, filas completas ni logs crudos.

