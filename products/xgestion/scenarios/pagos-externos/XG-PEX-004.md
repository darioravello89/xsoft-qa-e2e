---
{"id":"XG-PEX-004","title":"Resolver cancelación, vencimiento y confirmación tardía de un QR","product":"xgestion","module":"pagos-externos","tags":["xgestion","regression","pagos-externos","cobros","recuperacion","integridad-operaciones"],"status":"planned"}
---

# XG-PEX-004 — Resolver cancelación, vencimiento y confirmación tardía de un QR

## Objetivo

Continuar una venta cuyo diálogo QR terminó sin confirmación local, evitando cobrar de nuevo un pago que pudo completarse remotamente.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 6.** Ver [mapa de facturación y pagos externos](../../docs/facturacion-pagos-externos.md). Sin suite Robot, seed nuevo ni validación real del JAR. Los resultados son criterios por comprobar, no resultados obtenidos.

Perfiles independientes de cancelación previa al pago, timeout sin pago y confirmación remota tardía. Cerrar el diálogo y solicitar cancelar la orden no prueban que el proveedor haya cancelado el pago.

## Precondiciones y datos

- **Laboratorio futuro, todavía no disponible:** Windows QA exclusivo, JAR/paquete identificados, base sintética y servicios de homologación/sandbox. Faltan adaptación del runner, política de red acotada, perfiles, oráculos y calibración. La v1 exige red desconectada: estas fichas no autorizan reconectar la VM, desactivar guardas ni operar contra producción.
- Los alias QA-FEL/QA-PEX son datos propuestos **NO creados**; no representan identidades fiscales, cuentas de pago, certificados ni credenciales válidas. El seed comercial actual no prepara esta batería. El paquete privado deberá aportar las identidades de prueba aceptadas y su manifiesto.
- Declarar empresa, sucursal, puesto, operador, cliente, moneda, medio e identidad de la operación. Mantener otra operación de control. Sin promociones, cuenta corriente, cuotas, emisión combinada con pago externo ni impresión/envío de comprobantes salvo una variante definida.
- Preparar una consulta independiente y autorizada del estado remoto por identidad y su correspondencia local. Si falta esa consulta, el caso queda BLOQUEADO: el mensaje de la UI, un request o un mock no acreditan autorización/cobro.
- QA-PEX-QRT: venta ARS 2.000, orden O1 sin pago al inicio y operación O2 de control.
- Baselines separados: cancelación aceptada antes de pagar; contador vencido sin pago; cancelación remota fallida; pago confirmado en sandbox cuya respuesta llega después de cerrar/vencer el diálogo.
- Mecanismo autorizado de demora/errores, consulta independiente y ruta de recuperación de pago tardío aún pendientes. No cancelar ni alterar órdenes reales.

## Pasos y resultados esperados

| Acción del usuario | Resultado esperado |
| --- | --- |
| Abrir QR y cancelar antes de pagar en la variante de cancelación aceptada. | El diálogo se cierra y la venta no queda pagada por ese intento. La consulta sandbox acredita el estado de O1; la cancelación local por sí sola no basta. |
| Desde otro baseline, dejar vencer el contador sin realizar el pago. | No informa pago confirmado ni cierra comercialmente por timeout; los productos y ARS 2.000 siguen disponibles para retomar según el estado del diálogo padre. |
| En la variante de error al cancelar, cerrar el diálogo y consultar el proveedor. | Se registra el error de cancelación y se determina si la orden sigue activa. No se afirma que dejó de poder pagarse ni se crea otra orden a ciegas. |
| En la variante tardía, hacer llegar la confirmación preparada después del timeout/cierre y consultar por identidad. | Se reconoce el pago remoto ARS 2.000 sin cobrar otra vez ni aplicarlo a O2. La recuperación del vínculo/cierre local requiere el procedimiento acordado; si falta, registrar BLOQUEADO. |
| Con el estado resuelto como impago/cancelado, retomar la venta con un nuevo intento permitido. | Una única operación finalmente pagada. Conservar las identidades y estados de ambos intentos; si O1 ya estaba pagada, este paso no se ejecuta y se concilia O1. |

## Variantes, límites y recuperación del recorrido

- Un rechazo explícito del pago y una orden pendiente que expira no son equivalentes; preparar el estado del proveedor y comparar con su significado, sin exigir que el QR tenga un mensaje de rechazo no verificado.
- La fuente solicita cancelar órdenes pendientes y puede informar que falló la cancelación. No se ha acreditado una reconciliación automática de pagos tardíos; no inventar botón de recuperación ni fallback manual.
- Si llega dos veces la confirmación tardía, aplicar el criterio de efecto único de [PEX-003](XG-PEX-003.md); repetir eventos con un mecanismo futuro no equivale a una prueba ya ejecutada.

## Evidencia y recuperación común

Registrar por separado solicitud, estado remoto y estado local, con importe, moneda, identidad completa y marcas de tiempo; comprobar otra operación sin cambios. Una confirmación ambigua requiere conciliación antes de reintentar. No cargar otro cobro, volver a emitir ni corregir registros para obtener un aprobado.

Conservar evidencia antes de recuperar el baseline. Restaurar la base local no borra comprobantes ni pagos del servicio de pruebas: el procedimiento del laboratorio debe tratar ambos extremos y conservar sus vínculos. No publicar certificados, tokens, credenciales, documentos personales, XML/payloads fiscales, QR utilizables ni respuestas/filas completas. Los logs crudos del ERP permanecen privados y deben sanearse antes de incorporarlos al informe.

Antes de automatizar: preparar datos/oráculos, calibrar controles accesibles sobre el SHA256 del JAR y acordar el procedimiento de fallo/recuperación. No usar coordenadas fijas ni ampliar a estas pantallas el permiso de doble clic de Venta. INFO resume, DEBUG describe pasos y TRACE aporta diagnóstico saneado. Un fallo conserva paso, esperado, observado, categoría y evidencia; causa no determinada si falta prueba causal.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Rutas relativas a XGestion2:

- `src/ModuloVentas/Vistas/Dialogs/QR/DialogMercadoPagoQR.java:228-297`: timeout, cierre y solicitud de cancelación.
- `src/ModuloVentas/Vistas/Dialogs/formTicketCierre.java:990-1020`: retorno del diálogo y comprobación de confirmación.
- `test/ModuloVentas/Vistas/Dialogs/MercadoPagoQrFlowPolicyTest.java:13-20`: timeout según estado final.

Los tests citados descubren reglas y riesgos; no prueban la integración de extremo a extremo. Registrar además commit del harness, versión/SHA256 del JAR, paquete, perfil y reporte privado. La disponibilidad y el contrato vigente de cada servicio de pruebas deben verificarse antes de habilitarlo; esta ficha no certifica su disponibilidad actual.

