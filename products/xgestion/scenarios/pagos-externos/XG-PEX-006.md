---
{"id":"XG-PEX-006","title":"Recuperar rechazo o espera agotada de Point sin duplicar el cobro","product":"xgestion","module":"pagos-externos","tags":["xgestion","regression","pagos-externos","cobros","dispositivos","recuperacion","integridad-operaciones"],"status":"planned"}
---

# XG-PEX-006 — Recuperar rechazo o espera agotada de Point sin duplicar el cobro

## Objetivo

Resolver un pago Point rechazado, cancelado o de resultado incierto antes de usar Reintentar, y conservar una sola confirmación aunque llegue tarde o repetida.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 6.** Ver [mapa de facturación y pagos externos](../../docs/facturacion-pagos-externos.md). Sin suite Robot, seed nuevo ni validación real del JAR. Los resultados son criterios por comprobar, no resultados obtenidos.

Caso de recuperación integrado, condicionado al laboratorio Point de [PEX-005](XG-PEX-005.md). Un botón Reintentar habilitado no garantiza que el intento anterior sea impago.

## Precondiciones y datos

- **Laboratorio futuro, todavía no disponible:** Windows QA exclusivo, JAR/paquete identificados, base sintética y servicios de homologación/sandbox. Faltan adaptación del runner, política de red acotada, perfiles, oráculos y calibración. La v1 exige red desconectada: estas fichas no autorizan reconectar la VM, desactivar guardas ni operar contra producción.
- Los alias QA-FEL/QA-PEX son datos propuestos **NO creados**; no representan identidades fiscales, cuentas de pago, certificados ni credenciales válidas. El seed comercial actual no prepara esta batería. El paquete privado deberá aportar las identidades de prueba aceptadas y su manifiesto.
- Declarar empresa, sucursal, puesto, operador, cliente, moneda, medio e identidad de la operación. Mantener otra operación de control. Sin promociones, cuenta corriente, cuotas, emisión combinada con pago externo ni impresión/envío de comprobantes salvo una variante definida.
- Preparar una consulta independiente y autorizada del estado remoto por identidad y su correspondencia local. Si falta esa consulta, el caso queda BLOQUEADO: el mensaje de la UI, un request o un mock no acreditan autorización/cobro.
- QA-PEX-POINTR: venta ARS 2.000 sin cobro previo y terminal sandbox dedicado. Identidad completa de venta, intención, pago y cuenta registradas de forma saneada.
- Baselines separados: rechazo explícito; cancelación desde terminal; intento pendiente hasta vencer espera; cierre local del diálogo con estado remoto incierto; aprobación tardía/repetida del intento inicial.
- Mecanismo de estados/demoras reproducible y consulta remota independiente pendientes; acordar reuso/nueva intención e idempotencia antes de automatizar Reintentar. No operar dispositivos o cuentas reales.

## Pasos y resultados esperados

| Acción del usuario | Resultado esperado |
| --- | --- |
| Iniciar el cobro y producir el rechazo explícito preparado. | Se informa rechazo o cancelación sin marcar pago correcto; se conserva la venta ARS 2.000 para decidir cómo continuar. |
| En otro baseline, cancelar desde el terminal y consultar el estado remoto. | Confirma cancelación de ese intento; no crea un cobro por cerrar el diálogo ni por el estado técnico final. |
| En la variante de espera agotada/cierre local, consultar el intento antes de Reintentar. | Distingue impago confirmado de estado todavía desconocido. Desconocido bloquea un nuevo cobro; cancelar el worker local no acredita cancelar remotamente. |
| Solo con rechazo/cancelación/impago confirmado, reintentar según el contrato del laboratorio y completar el pago. | Un único pago aprobado ARS 2.000. Se conservan los vínculos de ambos intentos y no se cobra el anterior. |
| En la variante tardía o repetida, conciliar la aprobación del primer intento y observar la recuperación local. | La misma aprobación no genera dos cobros/cierres; no se crea otro intento para sustituir una respuesta demorada. Sin ruta de reconciliación definida, mantener el paso BLOQUEADO y conservar evidencia. |

## Variantes, límites y recuperación del recorrido

- La fuente distingue pago pendiente/aprobado/rechazado y permite reintentar tras varios errores; no demuestra idempotencia remota ni cancelación al cerrar la ventana. Son riesgos a verificar, no garantías.
- Rechazo del emisor de pago, cancelación del terminal, error de red y timeout de consulta deben conservar categorías distintas aunque compartan un diálogo.
- La aprobación repetida se controla por identidad/deltas, no sólo por cantidad de carteles. Dos puestos, reinicio durante el cobro y reversión bancaria requieren perfiles adicionales.
- No ingresar manualmente ARS 2.000 como pago alternativo mientras el intento Point continúe incierto.

## Evidencia y recuperación común

Registrar por separado solicitud, estado remoto y estado local, con importe, moneda, identidad completa y marcas de tiempo; comprobar otra operación sin cambios. Una confirmación ambigua requiere conciliación antes de reintentar. No cargar otro cobro, volver a emitir ni corregir registros para obtener un aprobado.

Conservar evidencia antes de recuperar el baseline. Restaurar la base local no borra comprobantes ni pagos del servicio de pruebas: el procedimiento del laboratorio debe tratar ambos extremos y conservar sus vínculos. No publicar certificados, tokens, credenciales, documentos personales, XML/payloads fiscales, QR utilizables ni respuestas/filas completas. Los logs crudos del ERP permanecen privados y deben sanearse antes de incorporarlos al informe.

Antes de automatizar: preparar datos/oráculos, calibrar controles accesibles sobre el SHA256 del JAR y acordar el procedimiento de fallo/recuperación. No usar coordenadas fijas ni ampliar a estas pantallas el permiso de doble clic de Venta. INFO resume, DEBUG describe pasos y TRACE aporta diagnóstico saneado. Un fallo conserva paso, esperado, observado, categoría y evidencia; causa no determinada si falta prueba causal.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Rutas relativas a XGestion2:

- `src/Integraciones/MercadoPago/Vistas/DialogMercadoPagoPointSmart.java:181-218,287-321`: errores, estado y reintento.
- `src/Integraciones/MercadoPago/Vistas/DialogMercadoPagoPointSmart.java:489-533,564-597`: finales, pendiente y rechazo.
- `src/Integraciones/MercadoPago/Vistas/DialogMercadoPagoPointSmart.java:639-664`: estados y cierre local del worker.
- `src/ModuloVentas/Vistas/Dialogs/formTicketCierre.java:1032-1045`: resultado del diálogo integrado.

Los tests citados descubren reglas y riesgos; no prueban la integración de extremo a extremo. Registrar además commit del harness, versión/SHA256 del JAR, paquete, perfil y reporte privado. La disponibilidad y el contrato vigente de cada servicio de pruebas deben verificarse antes de habilitarlo; esta ficha no certifica su disponibilidad actual.

