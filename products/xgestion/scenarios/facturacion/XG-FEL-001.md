---
{"id":"XG-FEL-001","title":"Corregir datos fiscales y cancelar antes de solicitar la emisión","product":"xgestion","module":"fiscal","tags":["xgestion","regression","fiscal","comprobantes","permisos","recuperacion"],"status":"planned"}
---

# XG-FEL-001 — Corregir datos fiscales y cancelar antes de solicitar la emisión

## Objetivo

Revisar destinatario y tipo de comprobante antes de autorizar una factura, conservando la venta cuando faltan datos o se cancela.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 6.** Ver [mapa de facturación y pagos externos](../../docs/facturacion-pagos-externos.md). Sin suite Robot, seed nuevo ni validación real del JAR. Los resultados son criterios por comprobar, no resultados obtenidos.

Venta de mostrador y emisión desde Ventas, con perfiles separados. El recorrido de pedido/mesa sigue en [RES-030](../restobar/XG-RES-030.md); no se duplica el cierre Restobar.

## Precondiciones y datos

- **Laboratorio futuro, todavía no disponible:** Windows QA exclusivo, JAR/paquete identificados, base sintética y servicios de homologación/sandbox. Faltan adaptación del runner, política de red acotada, perfiles, oráculos y calibración. La v1 exige red desconectada: estas fichas no autorizan reconectar la VM, desactivar guardas ni operar contra producción.
- Los alias QA-FEL/QA-PEX son datos propuestos **NO creados**; no representan identidades fiscales, cuentas de pago, certificados ni credenciales válidas. El seed comercial actual no prepara esta batería. El paquete privado deberá aportar las identidades de prueba aceptadas y su manifiesto.
- Declarar empresa, sucursal, puesto, operador, cliente, moneda, medio e identidad de la operación. Mantener otra operación de control. Sin promociones, cuenta corriente, cuotas, emisión combinada con pago externo ni impresión/envío de comprobantes salvo una variante definida.
- Preparar una consulta independiente y autorizada del estado remoto por identidad y su correspondencia local. Si falta esa consulta, el caso queda BLOQUEADO: el mensaje de la UI, un request o un mock no acreditan autorización/cobro.
- QA-FEL-A: dos unidades de un artículo con precio final ARS 1.210, total ARS 2.420; neto ARS 2.000 e IVA ARS 420 según el perfil sintético acordado. Cliente y tipo de factura compatibles con el emisor de homologación, todavía por preparar.
- Baselines independientes: venta nueva aún sin cobrar y venta ya cerrada/cobrada sin emisión. Cliente válido de prueba y variante con número de documento no numérico; selección fiscal/certificados de homologación pendientes.

## Pasos y resultados esperados

| Acción del usuario | Resultado esperado |
| --- | --- |
| Abrir opciones de Factura electrónica, revisar importe y destinatario y cancelar antes de confirmar. | No se registra una solicitud fiscal. El documento conserva el estado comercial previo de su baseline; cancelar la emisión no cobra ni revierte la venta cerrada. |
| En el perfil de datos inválidos, intentar confirmar la emisión. | Se explica el dato fiscal inválido y no aparece autorización ni número de comprobante nuevo; el diagnóstico no muestra configuración privada. |
| Corregir con el cliente válido de prueba y volver a revisar. | Conserva los dos artículos y ARS 2.420; muestra destinatario/tipo declarados. Corregir no constituye emisión. |
| Cancelar otra vez y consultar la misma venta y la operación de control. | Ambas mantienen sus importes/identidades; no hay doble venta, cobro o movimiento de stock por las revisiones. |

## Variantes, límites y recuperación del recorrido

- Variar tipo no soportado, cliente incompleto y proveedor fiscal sin configurar como perfiles distintos; el paquete debe fijar el resultado de cada validación.
- Factura B con receptor RI tiene una decisión visible de cancelar o usar consumidor final en la fuente; no convertir automáticamente al cliente ni extrapolar esa opción a todos los tipos. Su criterio fiscal de homologación queda pendiente de aprobación funcional.
- Rol restringido: identificar permiso real antes de incluir la variante; no inventar una autorización de supervisor para saltar validaciones. No afirmar que un rechazo fiscal mantiene siempre la venta abierta: se comprueba el estado previo de cada ruta.

## Evidencia y recuperación común

Registrar por separado solicitud, estado remoto y estado local, con importe, moneda, identidad completa y marcas de tiempo; comprobar otra operación sin cambios. Una confirmación ambigua requiere conciliación antes de reintentar. No cargar otro cobro, volver a emitir ni corregir registros para obtener un aprobado.

Conservar evidencia antes de recuperar el baseline. Restaurar la base local no borra comprobantes ni pagos del servicio de pruebas: el procedimiento del laboratorio debe tratar ambos extremos y conservar sus vínculos. No publicar certificados, tokens, credenciales, documentos personales, XML/payloads fiscales, QR utilizables ni respuestas/filas completas. Los logs crudos del ERP permanecen privados y deben sanearse antes de incorporarlos al informe.

Antes de automatizar: preparar datos/oráculos, calibrar controles accesibles sobre el SHA256 del JAR y acordar el procedimiento de fallo/recuperación. No usar coordenadas fijas ni ampliar a estas pantallas el permiso de doble clic de Venta. INFO resume, DEBUG describe pasos y TRACE aporta diagnóstico saneado. Un fallo conserva paso, esperado, observado, categoría y evidencia; causa no determinada si falta prueba causal.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Rutas relativas a XGestion2:

- `src/ModuloVentas/Vistas/FormVenta.java:5290-5325`: validación y decisión de receptor.
- `src/Integraciones/FacturacionElectronica/Service/EmisionFacturaElectronicaService.java:62-168`: datos, tipo y configuración.
- `test/Integraciones/FacturacionElectronica/Service/ResultadoEmisionFacturaElectronicaPolicyTest.java`: clasificación de resultados.

Los tests citados descubren reglas y riesgos; no prueban la integración de extremo a extremo. Registrar además commit del harness, versión/SHA256 del JAR, paquete, perfil y reporte privado. La disponibilidad y el contrato vigente de cada servicio de pruebas deben verificarse antes de habilitarlo; esta ficha no certifica su disponibilidad actual.
