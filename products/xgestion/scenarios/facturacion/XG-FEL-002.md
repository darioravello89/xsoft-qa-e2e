---
{"id":"XG-FEL-002","title":"Autorizar una factura y conservar una sola emisión al volver a consultarla","product":"xgestion","module":"fiscal","tags":["xgestion","regression","fiscal","comprobantes","recuperacion"],"status":"planned"}
---

# XG-FEL-002 — Autorizar una factura y conservar una sola emisión al volver a consultarla

## Objetivo

Obtener el comprobante fiscal de una venta ya cobrada y mantener la misma autorización al consultar o intentar repetir la acción.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 6.** Ver [mapa de facturación y pagos externos](../../docs/facturacion-pagos-externos.md). Sin suite Robot, seed nuevo ni validación real del JAR. Los resultados son criterios por comprobar, no resultados obtenidos.

Caso base desde Ventas sobre una operación comercial cerrada. Emisión directa desde Venta y pedido Restobar requieren sus propios estados previos; reutilizar [RES-030](../restobar/XG-RES-030.md) para ese origen.

## Precondiciones y datos

- **Laboratorio futuro, todavía no disponible:** Windows QA exclusivo, JAR/paquete identificados, base sintética y servicios de homologación/sandbox. Faltan adaptación del runner, política de red acotada, perfiles, oráculos y calibración. La v1 exige red desconectada: estas fichas no autorizan reconectar la VM, desactivar guardas ni operar contra producción.
- Los alias QA-FEL/QA-PEX son datos propuestos **NO creados**; no representan identidades fiscales, cuentas de pago, certificados ni credenciales válidas. El seed comercial actual no prepara esta batería. El paquete privado deberá aportar las identidades de prueba aceptadas y su manifiesto.
- Declarar empresa, sucursal, puesto, operador, cliente, moneda, medio e identidad de la operación. Mantener otra operación de control. Sin promociones, cuenta corriente, cuotas, emisión combinada con pago externo ni impresión/envío de comprobantes salvo una variante definida.
- Preparar una consulta independiente y autorizada del estado remoto por identidad y su correspondencia local. Si falta esa consulta, el caso queda BLOQUEADO: el mensaje de la UI, un request o un mock no acreditan autorización/cobro.
- QA-FEL-OK: venta cerrada y pagada ARS 2.420, neto ARS 2.000 e IVA ARS 420; sin comprobante fiscal previo. Caja y stock ya reflejan el cierre y sus saldos se registran antes de emitir.
- Un único proveedor de homologación activo, receptor válido y punto de venta de pruebas. Número autorizado y CAE se obtienen del extremo fiscal de pruebas; no se inventan valores aceptados.

## Pasos y resultados esperados

| Acción del usuario | Resultado esperado |
| --- | --- |
| Seleccionar la venta por su identidad y revisar cliente, total y tipo antes de emitir. | La selección corresponde a QA-FEL-OK, ARS 2.420; todavía no se confunde la venta cerrada con factura autorizada. |
| Solicitar emisión una vez y esperar su resultado observable. | Se informa autorización con número de comprobante; el extremo de homologación y el registro local corresponden a la misma operación, tipo, punto, importe y moneda. |
| Consultar nuevamente desde Ventas sin imprimir ni enviar. | Conserva número, autorización y total; la consulta no genera un nuevo cobro, salida de stock ni factura. |
| Intentar nuevamente emitir la venta ya informada mediante la acción disponible. | La operación se bloquea por estar informada o la acción no se ofrece; no se registra una segunda autorización. Conservar evidencia del control real, sin exigir un botón inexistente. |
| Reiniciar dentro del procedimiento QA y volver a consultar. | Persiste la misma autorización y el mismo vínculo; los saldos comerciales previos se mantienen. |

## Variantes, límites y recuperación del recorrido

- A/B/C y variantes de receptor son perfiles independientes con datos y oráculos fiscales previos; no asumir que basta cambiar la etiqueta del comprobante.
- USD, impuestos mixtos, redondeos y exentos requieren valores de origen/conversión separados y un contrato de homologación; no sumar monedas nominalmente.
- Una respuesta aprobada sin persistencia pertenece a [FEL-005](XG-FEL-005.md), no aprueba este caso. El mensaje final o una impresión no sustituyen la consulta remota por identidad.

## Evidencia y recuperación común

Registrar por separado solicitud, estado remoto y estado local, con importe, moneda, identidad completa y marcas de tiempo; comprobar otra operación sin cambios. Una confirmación ambigua requiere conciliación antes de reintentar. No cargar otro cobro, volver a emitir ni corregir registros para obtener un aprobado.

Conservar evidencia antes de recuperar el baseline. Restaurar la base local no borra comprobantes ni pagos del servicio de pruebas: el procedimiento del laboratorio debe tratar ambos extremos y conservar sus vínculos. No publicar certificados, tokens, credenciales, documentos personales, XML/payloads fiscales, QR utilizables ni respuestas/filas completas. Los logs crudos del ERP permanecen privados y deben sanearse antes de incorporarlos al informe.

Antes de automatizar: preparar datos/oráculos, calibrar controles accesibles sobre el SHA256 del JAR y acordar el procedimiento de fallo/recuperación. No usar coordenadas fijas ni ampliar a estas pantallas el permiso de doble clic de Venta. INFO resume, DEBUG describe pasos y TRACE aporta diagnóstico saneado. Un fallo conserva paso, esperado, observado, categoría y evidencia; causa no determinada si falta prueba causal.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Rutas relativas a XGestion2:

- `src/Integraciones/FacturacionElectronica/Service/EmisionFacturaElectronicaService.java:156-160,426-473`: guard de venta informada y persistencia de autorización.
- `src/ModuloVentas/Vistas/FormVenta.java:5536-5559`: resultado visible.
- `test/Integraciones/FacturacionElectronica/Service/FacturacionElectronicaMonedaPolicyTest.java`: contrato técnico de importes/moneda.

Los tests citados descubren reglas y riesgos; no prueban la integración de extremo a extremo. Registrar además commit del harness, versión/SHA256 del JAR, paquete, perfil y reporte privado. La disponibilidad y el contrato vigente de cada servicio de pruebas deben verificarse antes de habilitarlo; esta ficha no certifica su disponibilidad actual.
