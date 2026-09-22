---
{"id":"XG-PRM-007","title":"Conservar el precio normal cuando la promoción está desactivada","product":"xgestion","module":"promociones","tags":["xgestion","regression","promociones","escritura"],"status":"implemented","test":"products/xgestion/suites/promociones.robot","seed":"catalogo-comercial-v1"}
---

# XG-PRM-007 — Conservar el precio normal cuando la promoción está desactivada

## Objetivo y estado

El vendedor comprueba que una promoción inactiva no rebaja el precio al cargar un artículo, corregir su cantidad y cobrarlo una sola vez después de cancelar el primer intento de cobro.

**Automatización implementada; ejecución real sobre el JAR pendiente.** Pertenece a la etapa 2, grupo `promociones`. La [especificación](../../../../docs/specs/005-promociones.md) delimita el lote; escribir la ficha, pasar un test del framework o un dry-run no acredita PASS sobre XGestion.

## Perfil, precondiciones y datos

- Windows QA exclusivo, offline, escritorio desbloqueado y ejecución serial mediante el runner; paquete legítimo y licencia vigente.
- Contexto QA propio de empresa, sucursal, computadora y usuario. No compartir credenciales ni modificar configuración comercial desde las acciones del test.
- Baseline restaurado y seed `catalogo-comercial-v1` aplicado antes de abrir el JAR. El runner lo prepara automáticamente al seleccionar este caso por su ID, grupo o menú; `--seed` también permite pedirlo explícitamente. Ejemplo público `INACTIVA`, artículo `QA-SEED-INACTIVA`, precio base $1.000 ARS y stock suficiente.
- La oferta existe pero está inactiva; no debe aplicarse.
- Comprobante interno 99, efectivo exacto, sin impresión ni fiscalización; otros descuentos y recargos en cero, fidelización deshabilitada.
- Lista visible **Ninguna Lista**, ID 0; el cliente y el turno no asignan otra lista. No cambiar cliente, turno ni lista durante el caso.
- Paquete y localizadores calibrados para el SHA256 exacto del JAR con `promociones-v1`, `ventas-etapa1` y `ventas-teclado-v1`; grilla, columna de oferta, importes, editor y cobro observados por JAB. Ver el [contrato de promociones](../../docs/promociones.md).

Ejecutar desde el repositorio:

```powershell
.\qa.cmd run --product xgestion --scenario XG-PRM-007 --seed catalogo-comercial-v1 --log-level DEBUG
```

## Pasos y resultados esperados

1. Ingresar como QA y abrir una venta nueva con el comprobante interno. **Esperado:** contexto correcto y operación vacía, sin listas ni descuentos adicionales.
   Antes de probar la oferta inactiva, cargar una unidad de `QA-SEED-PCT`: **esperado**, bruto $1.000, oferta $100 y neto $900 ARS. Abandonar ese control positivo y comprobar que no persiste ninguna venta ni cambia stock/caja; comenzar luego una venta vacía. Si ese control falla, el caso se detiene: que no se aplique ninguna promoción no demuestra que se respete la vigencia o actividad.
2. Cargar `QA-SEED-INACTIVA` con cantidad **2**. **Esperado:** una sola línea del artículo correcto; precio unitario $1.000, subtotal bruto $2.000, oferta $0 y total neto **$2.000 ARS**.
3. Seleccionar esa misma línea, abrir su editor mediante **Ctrl+E**, cambiar cantidad a **1** y guardar. **Esperado:** se conserva la identidad del artículo y una sola línea; precio base $1.000, subtotal bruto $1.000, oferta $0 y total neto **$1.000 ARS**. La edición no agrega otro producto ni aplica dos veces el beneficio.
4. Abrir el cobro y cancelarlo antes de confirmar. **Esperado:** vuelve la venta con la cantidad 1 y el neto $1.000; todavía no se registra venta, cobro ni movimiento de stock/caja.
5. Retomar el cobro, entregar el importe exacto **$1.000 ARS** y confirmar una vez. **Esperado:** operación cerrada por ese importe y vuelto cero.
6. Contrastar el resultado guardado. **Esperado:** una sola venta y un único cobro por $1.000; stock del artículo **−1** y caja **+$1.000**. No hay descuentos adicionales ni duplicados del intento cancelado.

## Evidencia y recuperación

Comparar los valores visibles al cargar, editar y volver del cobro cancelado. Tras confirmar, contrastar identidad, importes y efectos mediante lecturas acotadas al contexto y a esa operación. Conservar el informe privado si una comprobación falla; no continuar como si hubiera aprobado ni borrar filas para corregir el resultado.

El runner cierra únicamente su JAR al terminar. La siguiente ejecución restaura el baseline y prepara el seed solicitado; preservar antes cualquier evidencia que se necesite. INFO resume, DEBUG muestra pasos de usuario y TRACE diagnóstico saneado. Un fallo siempre identifica paso, esperado, observado, categoría y evidencia, o «causa no determinada» cuando corresponda. Capturas solamente de ventanas QA autenticadas, sin credenciales.

## Anexo técnico y trazabilidad

En la línea persistida se exige `vecPrecio=1000`, `vecCantidad=1`, `vecTotal=1000` **bruto** y `vecOferta=0` como descuento automático; el encabezado conserva `venTotal=1000` **neto**. Verificar identidad de oferta según su aplicabilidad, ausencia de descuentos manuales/globales/de pago y del beneficio de puntos. El cobro simple se contrasta con pagado/vuelto y el ingreso neto de caja; no inferir que deba existir una fila en `ventas_pagos`.

En UI, `total` es el neto de la línea; `gross_total` expone su subtotal bruto y `offer_discount` el descuento automático. No comparar ese neto visible contra `vecTotal` como si ambos fueran el mismo importe. Las consultas son SELECT acotados a empresa/sucursal/computadora, artículo y operación; no usar escrituras de negocio para preparar un resultado durante el recorrido. Registrar SHA256/build JAR, paquete, fecha de referencia del seed y perfil en la evidencia privada.

Fuente ERP: commit `925589278503f2d339beeb0a79f773c605512dd8`; `src/ModuloVentas/Vistas/FormVenta.java` y `src/ModuloVentas/Entidades/TicketVenta.java` para presentación/persistencia. Regla de vigencia y actividad: `src/ModuloFinanzas/Entidades/OfertaLineaService.java`. Datos y expectativa estática: [pricing.py](../../seeds/pricing.py), ejemplo `INACTIVA`. Las referencias orientan el caso; no demuestran equivalencia ni aceptación del JAR.

No cubre listas comerciales, moneda USD, combos, fracciones, otras condiciones de oferta, descuentos combinados, fidelización, Restobar, pagos externos, fiscalización ni impresión.
