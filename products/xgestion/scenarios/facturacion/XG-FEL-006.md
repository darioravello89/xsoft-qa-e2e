---
{"id":"XG-FEL-006","title":"Vincular una nota de crédito con la factura y sus importes originales","product":"xgestion","module":"fiscal","tags":["xgestion","regression","fiscal","comprobantes","devoluciones","recuperacion"],"status":"planned"}
---

# XG-FEL-006 — Vincular una nota de crédito con la factura y sus importes originales

## Objetivo

Anular fiscalmente una operación identificada conservando su composición histórica y sin confundir la nota de crédito con devolución de dinero.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 6.** Ver [mapa de facturación y pagos externos](../../docs/facturacion-pagos-externos.md). Sin suite Robot, seed nuevo ni validación real del JAR. Los resultados son criterios por comprobar, no resultados obtenidos.

Anulación total desde Ventas sobre una factura autorizada. El vínculo fiscal y el estado comercial se contrastan por separado. Parciales, cuotas, reembolsos del proveedor de pago y notas de débito requieren contratos/fichas propios.

## Precondiciones y datos

- **Laboratorio futuro, todavía no disponible:** Windows QA exclusivo, JAR/paquete identificados, base sintética y servicios de homologación/sandbox. Faltan adaptación del runner, política de red acotada, perfiles, oráculos y calibración. La v1 exige red desconectada: estas fichas no autorizan reconectar la VM, desactivar guardas ni operar contra producción.
- Los alias QA-FEL/QA-PEX son datos propuestos **NO creados**; no representan identidades fiscales, cuentas de pago, certificados ni credenciales válidas. El seed comercial actual no prepara esta batería. El paquete privado deberá aportar las identidades de prueba aceptadas y su manifiesto.
- Declarar empresa, sucursal, puesto, operador, cliente, moneda, medio e identidad de la operación. Mantener otra operación de control. Sin promociones, cuenta corriente, cuotas, emisión combinada con pago externo ni impresión/envío de comprobantes salvo una variante definida.
- Preparar una consulta independiente y autorizada del estado remoto por identidad y su correspondencia local. Si falta esa consulta, el caso queda BLOQUEADO: el mensaje de la UI, un request o un mock no acreditan autorización/cobro.
- QA-FEL-NC: factura de homologación ya autorizada por ARS 1.000, neto gravado ARS 826,45 e IVA ARS 173,55, una alícuota del 21%; total ya cobrado. Factura distinta QA-FEL-CTRL por ARS 500 como control.
- Número/punto/tipo/emisor y fecha del original obtenidos del servicio de pruebas. Precio/lista actual del artículo diferente, ARS 1.200, para verificar que no reemplaza el importe histórico.
- Motivo QA acordado y rol autorizado para anular desde la sucursal original. Ruta exacta, oráculo de vínculo remoto, fallos de autorización/guardado y tratamiento financiero pendientes de laboratorio.

## Pasos y resultados esperados

| Acción del usuario | Resultado esperado |
| --- | --- |
| Seleccionar la factura original y abrir la anulación; cancelar antes de confirmar el motivo. | Factura vigente por ARS 1.000, sin nota de crédito nueva ni devolución de dinero/stock por cancelar. |
| Confirmar la anulación total con el motivo QA preparado. | Se solicita una nota de crédito relacionada con el original correcto; conserva total ARS 1.000, neto ARS 826,45 e IVA ARS 173,55, aunque el precio actual sea ARS 1.200. |
| Consultar autorización y vínculo de la nota en ambos extremos. | Una nota autorizada del tipo correspondiente con referencia al número/punto/tipo y emisor de la factura original; no se asocia a QA-FEL-CTRL. Si el vínculo remoto no puede verificarse, no aprobar. |
| Consultar estados comerciales y financieros por separado. | La anulación se explica por la nota y motivo. No inferir devolución de ARS 1.000 en caja ni reembolso externo por tener una nota autorizada; comparar con el contrato financiero explícito. |
| Volver a consultar o intentar anular el original ya anulado mediante la ruta disponible. | No se obtiene una segunda nota por el mismo objetivo ni se repite una reversión. La factura de control mantiene estado e importes. |

## Variantes, límites y recuperación del recorrido

- Rechazo explícito de la nota, autorización con guardado fallido y timeout necesitan perfiles separados. No afirmar que falla toda la operación de manera atómica: conciliar original, nota, stock y dinero antes de recuperar.
- La fuente construye un snapshot fiscal y transmite datos asociados al original; eso no acredita el vínculo aceptado por homologación ni todas las variantes A/B/C o USD. Su contrato exacto queda pendiente antes de ejecutar.
- Para USD, conservar importe/moneda/cotización del original y definir la regla fiscal de la nota antes de automatizar; no usar cotización o precio actual por conveniencia.
- La advertencia de la fuente contiene una indicación temporal; esta ficha no la convierte en asesoramiento ni requisito legal vigente.

## Evidencia y recuperación común

Registrar por separado solicitud, estado remoto y estado local, con importe, moneda, identidad completa y marcas de tiempo; comprobar otra operación sin cambios. Una confirmación ambigua requiere conciliación antes de reintentar. No cargar otro cobro, volver a emitir ni corregir registros para obtener un aprobado.

Conservar evidencia antes de recuperar el baseline. Restaurar la base local no borra comprobantes ni pagos del servicio de pruebas: el procedimiento del laboratorio debe tratar ambos extremos y conservar sus vínculos. No publicar certificados, tokens, credenciales, documentos personales, XML/payloads fiscales, QR utilizables ni respuestas/filas completas. Los logs crudos del ERP permanecen privados y deben sanearse antes de incorporarlos al informe.

Antes de automatizar: preparar datos/oráculos, calibrar controles accesibles sobre el SHA256 del JAR y acordar el procedimiento de fallo/recuperación. No usar coordenadas fijas ni ampliar a estas pantallas el permiso de doble clic de Venta. INFO resume, DEBUG describe pasos y TRACE aporta diagnóstico saneado. Un fallo conserva paso, esperado, observado, categoría y evidencia; causa no determinada si falta prueba causal.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Rutas relativas a XGestion2:

- `src/ModuloVentas/Vistas/FormVentas.java:1340-1439`: origen, motivo, datos asociados y separación de devolución.
- `src/ModuloVentas/Entidades/NotaCreditoFiscalSnapshot.java:17-36`: composición histórica.
- `test/ModuloVentas/Entidades/NotaCreditoFiscalSnapshotTest.java:15-55`: bases/IVA y persistencia sin clonar detalle.
- `src/ModuloVentas/Entidades/TicketVenta.java`: método crearNotaCreditoDebito; autorización y vínculo deben verificarse en el JAR.

Los tests citados descubren reglas y riesgos; no prueban la integración de extremo a extremo. Registrar además commit del harness, versión/SHA256 del JAR, paquete, perfil y reporte privado. La disponibilidad y el contrato vigente de cada servicio de pruebas deben verificarse antes de habilitarlo; esta ficha no certifica su disponibilidad actual.
