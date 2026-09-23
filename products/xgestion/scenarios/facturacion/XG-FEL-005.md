---
{"id":"XG-FEL-005","title":"Recuperar una factura autorizada que no pudo guardarse localmente","product":"xgestion","module":"fiscal","tags":["xgestion","regression","fiscal","comprobantes","recuperacion","integridad-operaciones"],"status":"planned"}
---

# XG-FEL-005 — Recuperar una factura autorizada que no pudo guardarse localmente

## Objetivo

Reconocer que la factura ya existe fiscalmente y recuperar su vínculo local sin solicitar una nueva autorización.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 6.** Ver [mapa de facturación y pagos externos](../../docs/facturacion-pagos-externos.md). Sin suite Robot, seed nuevo ni validación real del JAR. Los resultados son criterios por comprobar, no resultados obtenidos.

Distingue autorización remota de persistencia local. El servicio tiene una clasificación específica para el fallo de guardado; la herramienta/procedimiento de reparación de datos no se presume disponible.

## Precondiciones y datos

- **Laboratorio futuro, todavía no disponible:** Windows QA exclusivo, JAR/paquete identificados, base sintética y servicios de homologación/sandbox. Faltan adaptación del runner, política de red acotada, perfiles, oráculos y calibración. La v1 exige red desconectada: estas fichas no autorizan reconectar la VM, desactivar guardas ni operar contra producción.
- Los alias QA-FEL/QA-PEX son datos propuestos **NO creados**; no representan identidades fiscales, cuentas de pago, certificados ni credenciales válidas. El seed comercial actual no prepara esta batería. El paquete privado deberá aportar las identidades de prueba aceptadas y su manifiesto.
- Declarar empresa, sucursal, puesto, operador, cliente, moneda, medio e identidad de la operación. Mantener otra operación de control. Sin promociones, cuenta corriente, cuotas, emisión combinada con pago externo ni impresión/envío de comprobantes salvo una variante definida.
- Preparar una consulta independiente y autorizada del estado remoto por identidad y su correspondencia local. Si falta esa consulta, el caso queda BLOQUEADO: el mensaje de la UI, un request o un mock no acreditan autorización/cobro.
- QA-FEL-PERS: venta cerrada ARS 2.420 no informada localmente y respuesta de autorización válida de homologación.
- Punto de fallo controlado después de obtener la autorización y antes de persistirla, todavía por implementar/calibrar en laboratorio exclusivo. No cortar la base compartida ni reemplazar por mock la validación E2E.
- Perfil con un segundo proveedor de prueba configurado para comprobar que este error terminal no lo invoca. Reconciliación por número, punto, tipo, emisor e identidad completa de venta.

## Pasos y resultados esperados

| Acción del usuario | Resultado esperado |
| --- | --- |
| Emitir sobre la venta y activar el fallo local preparado después de la autorización. | El extremo fiscal acredita un único comprobante autorizado; la venta local carece de la actualización fiscal completa esperada. |
| Leer el resultado visible y revisar los intentos. | Informa que fue autorizado pero no se pudo guardar, indica no volver a emitir y contactar soporte; no prueba otro proveedor por esta falla. |
| Consultar el estado remoto y conservar evidencia sin volver a presionar Emitir. | Se identifica el mismo comprobante; no aparecen otra factura ni un nuevo cobro. La falta de un dato local no se interpreta como ausencia de autorización. |
| Ejecutar únicamente el procedimiento de conciliación local aprobado, cuando exista. | La venta queda vinculada al comprobante ya autorizado; importes y efectos comerciales se conservan. Si la recuperación no está definida, este paso queda BLOQUEADO. |
| Reabrir Ventas y consultar el vínculo recuperado. | Mismo número/CAE y mismo total; una eventual acción de emisión sobre la venta informada no crea un segundo comprobante. |

## Variantes, límites y recuperación del recorrido

- El punto de inyección interno del servicio sirve para tests de código, no acredita por sí mismo el fallo real del JAR. Preparar un mecanismo reproducible y evidencia en ambos extremos.
- La clasificación terminal corta el fallback en ese intento; no demuestra un bloqueo persistente de reemisión después de reiniciar. Registrar ese riesgo y no probar una nueva emisión mientras siga sin conciliar.
- No escribir CAE/número directamente en la base como parte de los pasos E2E ni inventar una opción de recuperación que no se verificó.

## Evidencia y recuperación común

Registrar por separado solicitud, estado remoto y estado local, con importe, moneda, identidad completa y marcas de tiempo; comprobar otra operación sin cambios. Una confirmación ambigua requiere conciliación antes de reintentar. No cargar otro cobro, volver a emitir ni corregir registros para obtener un aprobado.

Conservar evidencia antes de recuperar el baseline. Restaurar la base local no borra comprobantes ni pagos del servicio de pruebas: el procedimiento del laboratorio debe tratar ambos extremos y conservar sus vínculos. No publicar certificados, tokens, credenciales, documentos personales, XML/payloads fiscales, QR utilizables ni respuestas/filas completas. Los logs crudos del ERP permanecen privados y deben sanearse antes de incorporarlos al informe.

Antes de automatizar: preparar datos/oráculos, calibrar controles accesibles sobre el SHA256 del JAR y acordar el procedimiento de fallo/recuperación. No usar coordenadas fijas ni ampliar a estas pantallas el permiso de doble clic de Venta. INFO resume, DEBUG describe pasos y TRACE aporta diagnóstico saneado. Un fallo conserva paso, esperado, observado, categoría y evidencia; causa no determinada si falta prueba causal.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Rutas relativas a XGestion2:

- `src/Integraciones/FacturacionElectronica/Service/ResultadoEmisionFacturaElectronica.java:47-51`: advertencia específica.
- `src/Integraciones/FacturacionElectronica/Service/EmisionFacturaElectronicaService.java:237-245,454-462,526-549`: guardado, terminación y punto técnico de prueba.
- `src/ModuloVentas/Vistas/FormVenta.java:5536-5554`: presentación del resultado.
- `test/Integraciones/FacturacionElectronica/Service/ResultadoEmisionFacturaElectronicaPolicyTest.java`: política de autorizada sin guardar.

Los tests citados descubren reglas y riesgos; no prueban la integración de extremo a extremo. Registrar además commit del harness, versión/SHA256 del JAR, paquete, perfil y reporte privado. La disponibilidad y el contrato vigente de cada servicio de pruebas deben verificarse antes de habilitarlo; esta ficha no certifica su disponibilidad actual.
