---
{"id":"XG-FEL-003","title":"Resolver un rechazo fiscal explícito y reintentar sobre la misma venta","product":"xgestion","module":"fiscal","tags":["xgestion","regression","fiscal","comprobantes","recuperacion"],"status":"planned"}
---

# XG-FEL-003 — Resolver un rechazo fiscal explícito y reintentar sobre la misma venta

## Objetivo

Entender un rechazo del servicio fiscal, corregir la causa declarada y emitir una sola factura sin volver a cobrar.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 6.** Ver [mapa de facturación y pagos externos](../../docs/facturacion-pagos-externos.md). Sin suite Robot, seed nuevo ni validación real del JAR. Los resultados son criterios por comprobar, no resultados obtenidos.

Distingue rechazo explícito de ARCA de error técnico o respuesta incierta. El caso base parte de una venta cerrada, cuya deuda/caja/stock no se deshacen por el rechazo fiscal.

## Precondiciones y datos

- **Laboratorio futuro, todavía no disponible:** Windows QA exclusivo, JAR/paquete identificados, base sintética y servicios de homologación/sandbox. Faltan adaptación del runner, política de red acotada, perfiles, oráculos y calibración. La v1 exige red desconectada: estas fichas no autorizan reconectar la VM, desactivar guardas ni operar contra producción.
- Los alias QA-FEL/QA-PEX son datos propuestos **NO creados**; no representan identidades fiscales, cuentas de pago, certificados ni credenciales válidas. El seed comercial actual no prepara esta batería. El paquete privado deberá aportar las identidades de prueba aceptadas y su manifiesto.
- Declarar empresa, sucursal, puesto, operador, cliente, moneda, medio e identidad de la operación. Mantener otra operación de control. Sin promociones, cuenta corriente, cuotas, emisión combinada con pago externo ni impresión/envío de comprobantes salvo una variante definida.
- Preparar una consulta independiente y autorizada del estado remoto por identidad y su correspondencia local. Si falta esa consulta, el caso queda BLOQUEADO: el mensaje de la UI, un request o un mock no acreditan autorización/cobro.
- QA-FEL-RECH: venta cerrada y pagada ARS 2.420 aún no informada; otro comprobante de control autorizado sin relación.
- Escenario de rechazo reproducible permitido por homologación (por ejemplo condición fiscal del receptor incompatible), con datos concretos y mecanismo aún pendientes. Dos proveedores declarados solo si ambos son de prueba: el rechazo debe ser terminal para ese intento.

## Pasos y resultados esperados

| Acción del usuario | Resultado esperado |
| --- | --- |
| Solicitar la emisión con el perfil que produce rechazo explícito. | El extremo de pruebas devuelve rechazo identificable, sin CAE aprobado; la UI informa revisar los datos fiscales, no presenta éxito. |
| Consultar venta, pagos y evidencia de intentos. | Continúa la misma venta cerrada/cobrada por ARS 2.420, sin duplicar efectos. No se intenta otro proveedor como consecuencia del rechazo explícito. |
| Corregir el dato definido por el perfil a través de la ruta permitida y revisar la venta. | Destinatario y comprobante son los acordados; la corrección no altera importes históricos ni crea otra venta. |
| Reintentar una sola vez, tras acreditar que el rechazo no autorizó el comprobante. | Una autorización válida vinculada a la venta original; no hay otro cobro ni otro documento fiscal por el intento rechazado. |
| Consultar el comprobante de control. | Conserva su identidad, autorización e importes. |

## Variantes, límites y recuperación del recorrido

- Si la respuesta no distingue rechazo de autorización desconocida, pasar a [FEL-004](XG-FEL-004.md); no inferir rechazo por timeout.
- Errores de certificado, configuración o datos locales se registran con su propia causa y sin fingir respuesta de ARCA. La disponibilidad de un rechazo real controlable en homologación es requisito pendiente.
- La recuperación no fuerza datos fiscales mediante SQL ni modifica comprobantes ya autorizados.

## Evidencia y recuperación común

Registrar por separado solicitud, estado remoto y estado local, con importe, moneda, identidad completa y marcas de tiempo; comprobar otra operación sin cambios. Una confirmación ambigua requiere conciliación antes de reintentar. No cargar otro cobro, volver a emitir ni corregir registros para obtener un aprobado.

Conservar evidencia antes de recuperar el baseline. Restaurar la base local no borra comprobantes ni pagos del servicio de pruebas: el procedimiento del laboratorio debe tratar ambos extremos y conservar sus vínculos. No publicar certificados, tokens, credenciales, documentos personales, XML/payloads fiscales, QR utilizables ni respuestas/filas completas. Los logs crudos del ERP permanecen privados y deben sanearse antes de incorporarlos al informe.

Antes de automatizar: preparar datos/oráculos, calibrar controles accesibles sobre el SHA256 del JAR y acordar el procedimiento de fallo/recuperación. No usar coordenadas fijas ni ampliar a estas pantallas el permiso de doble clic de Venta. INFO resume, DEBUG describe pasos y TRACE aporta diagnóstico saneado. Un fallo conserva paso, esperado, observado, categoría y evidencia; causa no determinada si falta prueba causal.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Rutas relativas a XGestion2:

- `src/Integraciones/FacturacionElectronica/Service/EmisionFacturaElectronicaService.java:232-245,465-469,532-538`: rechazo terminal y mensaje.
- `src/Integraciones/FacturacionElectronica/Service/TipoFallaEmisionFacturaElectronica.java:3-18`: rechazo sin fallback.
- `test/Integraciones/FacturacionElectronica/Service/FacturacionElectronicaFailureUxWiringTest.java:71-81,114-121`: clasificación y mensaje saneado.

Los tests citados descubren reglas y riesgos; no prueban la integración de extremo a extremo. Registrar además commit del harness, versión/SHA256 del JAR, paquete, perfil y reporte privado. La disponibilidad y el contrato vigente de cada servicio de pruebas deben verificarse antes de habilitarlo; esta ficha no certifica su disponibilidad actual.
