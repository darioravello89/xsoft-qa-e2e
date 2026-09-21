# Datos y localizadores privados

El manifest común incorpora `fixtures.json` y `locators.json` por ruta y SHA256. Partir de `../examples/fixtures.example.json` y `../examples/locators.example.json`, rellenarlos dentro del paquete privado y recalcular el manifest. No guardar los valores reales en Git.

`fixtures.json`, versión 1:

- `context`: IDs numéricos positivos `empresa`, `sucursal`, `computadora`, `usuario_id`, y textos visibles exactos `empresa_label`, `sucursal_label`, `usuario_label`.
- `product`: `id` de `articulos.artId`, `code` de `artCodigo` único, `name` visible, `unit_price: "1000.00"`, `quantity: 2`. Producto ARS stockeable, sin variantes, descuentos, recargos, ofertas ni listas que alteren precio final; stock suficiente.
- `sale`: `cash_payment_id` correspondiente al efectivo inmediato del fixture y `non_fiscal_document_id: 99`. El documento interno 99 se cobra/cierra sin emitir factura ni CAE. No usar F9.
- `nonexistent_product_code`: código garantizado ausente en el dump.
- `ui.products_empty_text`: texto exacto de un indicador accesible de búsqueda vacía observado al calibrar; no se presupone una frase.

La licencia QA debe ser válida, estar vigente y corresponder a los IDs del dump. Usar usuario QA normal, no bypass de soporte. Preparar módulos/menús y permisos suficientes, tipo de comprobante no fiscal disponible, picker de forma de cobro al cerrar y confirmación al descartar una venta cargada. Esos flujos corresponden a esta v1; cualquier diferencia exige actualizar escenarios/localizadores y recalibrar.

La grilla presenta importes ARS como `2.000,00`; el diálogo de cobro de la fuente usa decimales con punto como `2000.00`. Calibrar la representación de cada control sin interpretar ambos formatos como equivalentes a ciegas. El oráculo usa `Decimal` y valores SQL. El dump debe tener política de servicio válida offline y sincronización V2/integridad desactivadas en la configuración de la computadora. El laboratorio bloquea tráfico externo; `sincronizadorActiva=false` por sí solo no impide todas las llamadas cloud del ERP.

`locators.json`, versión 1:

- `calibration.status` comienza como `draft`; sólo pasa a `verified` después del recorrido real. Registrar `app_sha256`, `verified_by`, `verified_at` ISO8601 y `jab_version` reales.
- `windows`: clave → título literal exacto. La selección verifica PID propio y rechaza títulos coincidentes de otra instancia.
- `elements`: alias → `{ "window": "clave", "query": "selector JAB observado" }`. Debe haber un único control visible para cada alias. No hay fallback por índice, imagen ni coordenadas fijas.

La lista obligatoria reside en `contracts.REQUIRED_ELEMENTS`. Los selectores `sale.non_fiscal_option` y `payment.cash_option` deben identificar las opciones reales 99 y efectivo del fixture. `products.known_result` identifica la celda con el nombre del producto; `products.empty_result` el indicador vacío. `sale.closed_indicator` identifica un control visible del escritorio luego de cancelar. Esas equivalencias se verifican durante calibración y se prueban de nuevo por oráculo al ejecutar.

## Extensión privada de Venta cotidiana

Los casos XG-VEN-003 a XG-VEN-009 inician con el perfil `ventas-etapa1`. Se valida la extensión antes de iniciar el JAR; tener los siete casos iniciales calibrados no habilita automáticamente estos controles. Los paquetes con el contrato anterior siguen sirviendo para esos siete casos.

Agregar a `fixtures.json` el objeto `sales_journeys`:

| Campo | Contrato |
| --- | --- |
| `schema_version` | Entero `1`. |
| `currency` | `ARS`. |
| `cash_dialog` | Booleano `true`: el cobro presenta el diálogo. |
| `abandon_requires_supervisor` | Booleano `false`: el perfil permite abandonar sin autorización adicional. |
| `unknown_notice` | `status` para el texto de estado o `dialog` para aviso modal, según lo observado. |
| `unknown_notice_text` | Texto exacto no vacío del aviso accesible; el sonido solo no acredita el resultado. |
| `repeated_product_rows` | Entero `1` o `2`, cantidad de filas observadas al agregar dos veces una unidad del mismo artículo. |
| `defaults.customer` | Texto exacto visible del cliente al iniciar/reiniciar Venta. |
| `defaults.price_list` | Texto exacto visible de la lista predeterminada. |
| `defaults.document` | Texto exacto visible del comprobante predeterminado. No suponer que siempre es 99. |

Preparar turno/caja abierto, `cartelPagoVuelto=true` y `venta.codigoParaAnulacion=false`. Configurar el aviso conforme al fixture: `venta.avisarProductoInexistentePorSonido=true` corresponde al estado textual más sonido; `false` abre un diálogo. Mantener el perfil sin promociones, descuentos, puntos, percepciones, extras ni impresión; revisar `pedirPagoAlCerrarTicket` y `venta.imprimirOrdenPago` para no agregar pantallas fuera del flujo calibrado. Las declaraciones del fixture no cambian por sí solas la configuración del ERP.

El reinicio de Venta carga defaults según el perfil. Si `venta.activarUltimoTipoComprobante` está desactivado, la fuente elige B/C según la empresa; si está activo usa `venta.ultimoTipoComprobante`. El caso observa el default declarado y después selecciona explícitamente el documento no fiscal 99 cuando inicia la siguiente operación.

Extender `locators.elements` con `sale.lines`, `sale.customer`, `sale.price_list`, `sale.unknown_notice`, `payment.total`, `payment.change`, `payment.cancel`, `sale.cancel_reject`, `editor.quantity`, `editor.save` y `editor.product`; para `unknown_notice: dialog`, agregar también `sale.unknown_dismiss`. Cada alias conserva `window` y `query` observados y debe identificar un único control.

`sale.lines` incluye además:

- `column_count`: entero con el número completo de columnas que expone JAB, incluidas las ocultas si aparecen en su modelo.
- `columns`: objeto con `code`, `name`, `quantity`, `unit_price` y `total`; cada valor es un índice entero distinto, comenzando en cero, observado dentro de ese modelo. `total` representa el importe final de la línea; `code` identifica el código del fixture y no el ID interno oculto.

En el editor del perfil normal, la cantidad se expone como decimal con punto (`1.0`, `2.0`), igual que la cantidad de la grilla. `editor.product` lee el nombre del artículo en un campo no editable; `editor.save` guarda. El botón Cancelar del editor existe en la fuente, pero estos casos no lo ejercitan ni exigen un alias para él. `sale.cancel_reject` rechaza el abandono en su propia confirmación: no debe apuntar al botón Cancelar de pago ni del editor.

Estos índices describen **columnas de una tabla identificada inequívocamente**; no autorizan escoger el primer control coincidente. No copiar índices desde Java sin comprobar cómo los expone el JAR. La lectura exige dimensiones y filas completas; una grilla inaccesible o incompleta bloquea la comprobación, aunque el total general coincida.

Después de verificar la extensión con el JAR, agregar `ventas-etapa1` a la lista `locators.calibration.verified_features`, además de `status: verified`, hash, persona, fecha y versión JAB. No marcar ese alcance solamente porque los selectores iniciales estaban verificados. Para XG-VEN-003/007 verificar también el doble clic autorizado sobre la celda identificada por JAB, sin coordenadas fijas, y todos los controles del editor. No alcanza con copiar una verificación anterior que solo incluía cobro/aviso/defaults.

La fuente fijada `f34238183d494259bed1279dd7d9aac0ce16a3ae` describe una ventana de cobro “Forma de pago”, botones “Cobrar (enter)”/“Cancelar (esc)” y una confirmación de abandono “Confirmar” con “Aceptar”/“Cancelar”. Son referencias para la persona que calibra, **no selectores aprobados**. En cobro simple, `ventas.Pagado` y `Vuelto` conservan recibido/vuelto, caja registra el total aplicado y no se generan filas de pago múltiple en `ventas_pagos`.

Cambiar fixtures requiere preparar un paquete privado actualizado con sus hashes e importarlo en un nuevo clon normal, conservando el anterior. `qa.cmd calibrate` solo actualiza el mapa de localizadores; no añade ni modifica `sales_journeys` en los fixtures importados.

Los secretos entran sólo por `.env.local`: nunca se pasan como argumentos de keywords ni al proceso Java. Su stdout/stderr se descarta porque el ERP puede registrar datos sensibles; las evidencias generadas por el framework no sustituyen los logs privados de diagnóstico del ERP. No publicar `log.html`, capturas ni árbol JAB sin revisar su contenido.
