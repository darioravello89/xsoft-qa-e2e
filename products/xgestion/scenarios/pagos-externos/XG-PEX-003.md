---
{"id":"XG-PEX-003","title":"Cobrar por QR sólo después de confirmar el pago de esa operación","product":"xgestion","module":"pagos-externos","tags":["xgestion","regression","pagos-externos","cobros","recuperacion","integridad-operaciones"],"status":"planned"}
---

# XG-PEX-003 — Cobrar por QR sólo después de confirmar el pago de esa operación

## Objetivo

Distinguir la creación del QR del pago confirmado y cerrar la venta una sola vez con el ID externo correcto.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 6.** Ver [mapa de facturación y pagos externos](../../docs/facturacion-pagos-externos.md). Sin suite Robot, seed nuevo ni validación real del JAR. Los resultados son criterios por comprobar, no resultados obtenidos.

QR de cobro desde el diálogo de cierre. Pedido por QR/mozo y liberación de mesa/cocina permanecen en [RES-035](../restobar/XG-RES-035.md); no se acreditan por pagar esta venta.

## Precondiciones y datos

- **Laboratorio futuro, todavía no disponible:** Windows QA exclusivo, JAR/paquete identificados, base sintética y servicios de homologación/sandbox. Faltan adaptación del runner, política de red acotada, perfiles, oráculos y calibración. La v1 exige red desconectada: estas fichas no autorizan reconectar la VM, desactivar guardas ni operar contra producción.
- Los alias QA-FEL/QA-PEX son datos propuestos **NO creados**; no representan identidades fiscales, cuentas de pago, certificados ni credenciales válidas. El seed comercial actual no prepara esta batería. El paquete privado deberá aportar las identidades de prueba aceptadas y su manifiesto.
- Declarar empresa, sucursal, puesto, operador, cliente, moneda, medio e identidad de la operación. Mantener otra operación de control. Sin promociones, cuenta corriente, cuotas, emisión combinada con pago externo ni impresión/envío de comprobantes salvo una variante definida.
- Preparar una consulta independiente y autorizada del estado remoto por identidad y su correspondencia local. Si falta esa consulta, el caso queda BLOQUEADO: el mensaje de la UI, un request o un mock no acreditan autorización/cobro.
- QA-PEX-QR: venta ARS 2.000 con stock inicial 10 para el artículo de dos unidades. Cuenta y comprador sandbox preparados, todavía no disponibles; orden O1 ligada a la identidad completa de la venta.
- Perfil con pago pendiente inicial y posterior confirmación remota por ARS 2.000. Otra orden O2 de control con importe distinto ARS 500; consulta remota por orden/pago/contexto.
- Ventana de confirmación cerca del fin del contador y repetición de la misma respuesta/evento requieren mecanismo de laboratorio reproducible; no depender de acertar un clic a tiempo.

## Pasos y resultados esperados

| Acción del usuario | Resultado esperado |
| --- | --- |
| Abrir QR y esperar que se muestre la orden. | Se crea/identifica O1 para ARS 2.000, pero sigue sin pago confirmado; tener QR visible o request aceptado no cierra la venta. |
| Mantener el pago pendiente y consultar el estado comercial. | Continúa pendiente; no se consume un cobro anterior ni el pago de O2. |
| Completar el pago sandbox de O1 y esperar confirmación observable. | Un pago confirmado ARS 2.000 del contexto correcto; la venta conserva su ID externo y puede cerrar una sola vez, con stock final 8 y efecto financiero definido por el medio. |
| Reabrir la consulta y recibir/consultar nuevamente la misma confirmación mediante el laboratorio preparado. | El mismo pago no genera otra venta/cobro ni otro egreso de stock; no se mezcla la identidad con O2. |
| En variante independiente, confirmar antes del vencimiento observable del contador y dejar que éste llegue a cero. | Un pago ya finalizado no se reclasifica como vencido/cancelado por el contador; conserva evidencia de confirmación y cierre. |

## Variantes, límites y recuperación del recorrido

- QR cargado, respuesta HTTP aceptada y cambio de estado técnico son pasos intermedios; la aceptación requiere pago remoto y vínculo local por identidad/importe.
- La fuente considera válida una actualización idempotente con cero filas afectadas; eso no demuestra idempotencia de todo el cierre ni valida callbacks repetidos. Los deltas comerciales deben verificarse.
- Una respuesta sin ID externo o perteneciente a otra operación no acredita el cobro. El rechazo exacto visible y el método de reproducir esos datos están pendientes de contrato/calibración.
- Cancelación, timeout y confirmación posterior al cierre del diálogo pertenecen a [PEX-004](XG-PEX-004.md).

## Evidencia y recuperación común

Registrar por separado solicitud, estado remoto y estado local, con importe, moneda, identidad completa y marcas de tiempo; comprobar otra operación sin cambios. Una confirmación ambigua requiere conciliación antes de reintentar. No cargar otro cobro, volver a emitir ni corregir registros para obtener un aprobado.

Conservar evidencia antes de recuperar el baseline. Restaurar la base local no borra comprobantes ni pagos del servicio de pruebas: el procedimiento del laboratorio debe tratar ambos extremos y conservar sus vínculos. No publicar certificados, tokens, credenciales, documentos personales, XML/payloads fiscales, QR utilizables ni respuestas/filas completas. Los logs crudos del ERP permanecen privados y deben sanearse antes de incorporarlos al informe.

Antes de automatizar: preparar datos/oráculos, calibrar controles accesibles sobre el SHA256 del JAR y acordar el procedimiento de fallo/recuperación. No usar coordenadas fijas ni ampliar a estas pantallas el permiso de doble clic de Venta. INFO resume, DEBUG describe pasos y TRACE aporta diagnóstico saneado. Un fallo conserva paso, esperado, observado, categoría y evidencia; causa no determinada si falta prueba causal.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Rutas relativas a XGestion2:

- `src/ModuloVentas/Vistas/Dialogs/QR/DialogMercadoPagoQR.java:180-259,310-340`: consulta, confirmación y orden.
- `src/ModuloVentas/Vistas/Dialogs/formTicketCierre.java:1991-2011`: asignación de identidad del pago QR.
- `test/ModuloVentas/Vistas/Dialogs/MercadoPagoQrFlowPolicyTest.java:13-36`: contador e idempotencia de actualización.

Los tests citados descubren reglas y riesgos; no prueban la integración de extremo a extremo. Registrar además commit del harness, versión/SHA256 del JAR, paquete, perfil y reporte privado. La disponibilidad y el contrato vigente de cada servicio de pruebas deben verificarse antes de habilitarlo; esta ficha no certifica su disponibilidad actual.

