---
{"id":"XG-FEL-004","title":"Conciliar un resultado fiscal incierto antes de repetir la emisión","product":"xgestion","module":"fiscal","tags":["xgestion","regression","fiscal","comprobantes","recuperacion","integridad-operaciones"],"status":"planned"}
---

# XG-FEL-004 — Conciliar un resultado fiscal incierto antes de repetir la emisión

## Objetivo

Conocer si una solicitud llegó a autorizarse cuando se perdió su respuesta, evitando emitir otra factura por la misma venta.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 6.** Ver [mapa de facturación y pagos externos](../../docs/facturacion-pagos-externos.md). Sin suite Robot, seed nuevo ni validación real del JAR. Los resultados son criterios por comprobar, no resultados obtenidos.

Objetivo de integridad, con contrato de recuperación pendiente. La fuente puede intentar otro proveedor después de una falla técnica incluso si el estado remoto anterior es incierto; esta ficha no afirma que ya exista una protección global contra duplicados.

## Precondiciones y datos

- **Laboratorio futuro, todavía no disponible:** Windows QA exclusivo, JAR/paquete identificados, base sintética y servicios de homologación/sandbox. Faltan adaptación del runner, política de red acotada, perfiles, oráculos y calibración. La v1 exige red desconectada: estas fichas no autorizan reconectar la VM, desactivar guardas ni operar contra producción.
- Los alias QA-FEL/QA-PEX son datos propuestos **NO creados**; no representan identidades fiscales, cuentas de pago, certificados ni credenciales válidas. El seed comercial actual no prepara esta batería. El paquete privado deberá aportar las identidades de prueba aceptadas y su manifiesto.
- Declarar empresa, sucursal, puesto, operador, cliente, moneda, medio e identidad de la operación. Mantener otra operación de control. Sin promociones, cuenta corriente, cuotas, emisión combinada con pago externo ni impresión/envío de comprobantes salvo una variante definida.
- Preparar una consulta independiente y autorizada del estado remoto por identidad y su correspondencia local. Si falta esa consulta, el caso queda BLOQUEADO: el mensaje de la UI, un request o un mock no acreditan autorización/cobro.
- QA-FEL-INC: venta cerrada ARS 2.420, aún sin autorización local. Perfil base con un solo proveedor de homologación, sin impresión/correo y consulta remota independiente.
- Preparar dos variantes reproducibles: solicitud recibida/autorizada con respuesta retenida; solicitud que no llegó a autorizarse. El mecanismo de demorar/perder la respuesta y su observabilidad está pendiente; no interrumpir servicios compartidos.
- Variante independiente de dos proveedores de homologación activos, orden declarado y registro de todos los intentos. No reutilizar el resultado de un solo proveedor como prueba de esta variante.

## Pasos y resultados esperados

| Acción del usuario | Resultado esperado |
| --- | --- |
| Solicitar emisión y provocar únicamente la pérdida de respuesta preparada. | Se conserva la identidad de la solicitud; el operador no recibe una autorización local acreditada ni debe interpretar el error como rechazo fiscal. |
| Consultar la venta y el extremo fiscal antes de repetir una acción. | Se distingue estado local de estado remoto: autorizado con número/CAE conocido, no autorizado confirmado, o todavía desconocido. Desconocido se informa BLOQUEADO para cualquier reemisión. |
| En la variante autorizada, seguir el procedimiento de recuperación acordado sin volver a emitir. | Se recupera o escala la conciliación del mismo comprobante. No se genera otra autorización ni otro cobro; la ruta para recuperar persistencia debe estar definida antes de aprobar. |
| En la variante no autorizada de forma concluyente, resolver el fallo y reintentar según el procedimiento. | Se obtiene una sola autorización para la venta, con todos los intentos explicados y sin duplicar efectos comerciales. |
| En el perfil de dos proveedores, conciliar cada intento y todas las autorizaciones remotas. | Como máximo un comprobante fiscal válido para el objetivo de emisión. Un éxito del segundo proveedor no basta: si el primero también autorizó o no se puede resolver su estado, registrar fallo/bloqueo, no aprobar por el mensaje final. |

## Variantes, límites y recuperación del recorrido

- La fuente conserva un indicador de estado remoto desconocido y permite fallback de fallas técnicas. Es un riesgo a reproducir, no un defecto validado sobre el JAR ni una garantía de idempotencia.
- No inventar un botón de consulta remota, reconciliación automática o clave de idempotencia. Son requisitos del laboratorio/contrato antes de automatizar las acciones dependientes.
- Una recuperación manual autorizada debe registrar qué comprobante se vinculó; restaurar la base local no elimina autorizaciones remotas. No reintentar en bucle.

## Evidencia y recuperación común

Registrar por separado solicitud, estado remoto y estado local, con importe, moneda, identidad completa y marcas de tiempo; comprobar otra operación sin cambios. Una confirmación ambigua requiere conciliación antes de reintentar. No cargar otro cobro, volver a emitir ni corregir registros para obtener un aprobado.

Conservar evidencia antes de recuperar el baseline. Restaurar la base local no borra comprobantes ni pagos del servicio de pruebas: el procedimiento del laboratorio debe tratar ambos extremos y conservar sus vínculos. No publicar certificados, tokens, credenciales, documentos personales, XML/payloads fiscales, QR utilizables ni respuestas/filas completas. Los logs crudos del ERP permanecen privados y deben sanearse antes de incorporarlos al informe.

Antes de automatizar: preparar datos/oráculos, calibrar controles accesibles sobre el SHA256 del JAR y acordar el procedimiento de fallo/recuperación. No usar coordenadas fijas ni ampliar a estas pantallas el permiso de doble clic de Venta. INFO resume, DEBUG describe pasos y TRACE aporta diagnóstico saneado. Un fallo conserva paso, esperado, observado, categoría y evidencia; causa no determinada si falta prueba causal.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Rutas relativas a XGestion2:

- `src/Integraciones/FacturacionElectronica/Service/EmisionFacturaElectronicaService.java:184-268`: cadena de proveedores, estado ambiguo y fallback.
- `src/Integraciones/FacturacionElectronica/Service/FacturaElectronicaEstadoRemotoPolicy.java:5-12`: indicador de solicitud fiscal enviada.
- `src/Integraciones/FacturacionElectronica/Service/TipoFallaEmisionFacturaElectronica.java:3-18`: error técnico recuperable.
- `test/Integraciones/FacturacionElectronica/Service/FacturaElectronicaEstadoRemotoPolicyTest.java`: clasificación del estado incierto.
- `test/Integraciones/FacturacionElectronica/Service/FacturacionElectronicaFailureUxWiringTest.java:26-39,71-81`: fallos ambiguos y progreso.

Los tests citados descubren reglas y riesgos; no prueban la integración de extremo a extremo. Registrar además commit del harness, versión/SHA256 del JAR, paquete, perfil y reporte privado. La disponibilidad y el contrato vigente de cada servicio de pruebas deben verificarse antes de habilitarlo; esta ficha no certifica su disponibilidad actual.
