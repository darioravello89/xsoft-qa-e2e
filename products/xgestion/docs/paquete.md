# Datos y localizadores privados

El manifest común incorpora `fixtures.json` y `locators.json` por ruta y SHA256. Partir de `../examples/fixtures.example.json` y `../examples/locators.example.json`, rellenarlos dentro del paquete privado y recalcular el manifest. No guardar los valores reales en Git.

`fixtures.json`, versión 1:

- `context`: IDs numéricos positivos `empresa`, `sucursal`, `computadora`, `usuario_id`, y textos visibles exactos `empresa_label`, `sucursal_label`, `usuario_label`.
- `product`: `id` de `articulos.artId`, `code` de `artCodigo` único, `name` visible, `unit_price: "1000.00"`, `quantity: 2`. Producto ARS stockeable, sin variantes, descuentos, recargos, ofertas ni listas que alteren precio final; stock suficiente.
- `sale`: `cash_payment_id` correspondiente al efectivo inmediato del fixture y `non_fiscal_document_id: 99`. El documento interno 99 se cobra/cierra sin emitir factura ni CAE. No usar F9.
- `nonexistent_product_code`: código garantizado ausente en el dump.
- `ui.products_empty_text`: texto exacto de un indicador accesible de búsqueda vacía observado al calibrar; no se presupone una frase.

La licencia QA debe ser válida, estar vigente y corresponder a los IDs del dump. Usar usuario QA normal, no bypass de soporte. Preparar módulos/menús y permisos suficientes, tipo de comprobante no fiscal disponible, picker de forma de cobro al cerrar y confirmación al descartar una venta cargada. Esos flujos corresponden a esta v1; cualquier diferencia exige actualizar escenarios/localizadores y recalibrar.

El precio UI usa formato argentino (`2.000,00`); el oráculo usa `Decimal` y valores SQL. El dump debe tener política de servicio válida offline y sincronización V2/integridad desactivadas en la configuración de la computadora. El laboratorio bloquea tráfico externo; `sincronizadorActiva=false` por sí solo no impide todas las llamadas cloud del ERP.

`locators.json`, versión 1:

- `calibration.status` comienza como `draft`; sólo pasa a `verified` después del recorrido real. Registrar `app_sha256`, `verified_by`, `verified_at` ISO8601 y `jab_version` reales.
- `windows`: clave → título literal exacto. La selección verifica PID propio y rechaza títulos coincidentes de otra instancia.
- `elements`: alias → `{ "window": "clave", "query": "selector JAB observado" }`. Debe haber un único control visible para cada alias. No hay fallback por índice, imagen ni coordenadas fijas.

La lista obligatoria reside en `contracts.REQUIRED_ELEMENTS`. Los selectores `sale.non_fiscal_option` y `payment.cash_option` deben identificar las opciones reales 99 y efectivo del fixture. `products.known_result` identifica la celda con el nombre del producto; `products.empty_result` el indicador vacío. `sale.closed_indicator` identifica un control visible del escritorio luego de cancelar. Esas equivalencias se verifican durante calibración y se prueban de nuevo por oráculo al ejecutar.

Los secretos entran sólo por `.env.local`: nunca se pasan como argumentos de keywords ni al proceso Java. Su stdout/stderr se descarta porque el ERP puede registrar datos sensibles; las evidencias generadas por el framework no sustituyen los logs privados de diagnóstico del ERP. No publicar `log.html`, capturas ni árbol JAB sin revisar su contenido.
