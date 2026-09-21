---
{"id":"XG-VEN-003","title":"Cargar un producto y modificar su cantidad","product":"xgestion","module":"ventas","tags":["xgestion","regression","ventas","escritura","carga-productos","corregir-venta"],"status":"implemented","test":"products/xgestion/suites/ventas.robot"}
---

# XG-VEN-003 — Cargar un producto y modificar su cantidad

## Objetivo

El vendedor cambia la cantidad de una línea ya cargada y ve cómo cambia el total.

## Estado

**Automatización implementada; ejecución real sobre el JAR pendiente.** El caso pertenece a la [etapa 1 — Venta cotidiana](../../docs/roadmap.md) y requiere `sales_journeys`, grilla y editor calibrados. Un `check`, dry-run o test del framework no acredita PASS sobre XGestion.

La apertura del editor usa el doble clic autorizado sobre la celda identificada por JAB, con su posición actual verificada; no usa coordenadas fijas. En la fuente fijada, `FormVenta.java:1748` dispara ese editor y no define un botón Editar ni un atajo propio. La mejora de accesibilidad sigue en el [backlog CSV](../../docs/backlog-accesibilidad.csv); implementarla en el ERP es una tarea distinta. No sustituir la edición por precargar cantidad antes de agregar.

## Perfil, precondiciones y datos

- Windows QA exclusivo, offline, escritorio desbloqueado y ejecución serial por el runner.
- Paquete autorizado, licencia QA vigente, base aislada restaurada y selectores calibrados para el SHA-256 del JAR.
- Usuario, empresa, sucursal y computadora QA definidos en el paquete; credenciales locales privadas.
- Venta local no fiscal en ARS, producto a precio final $1.000 y stock suficiente; cantidad habitual 2 y total $2.000. Efectivo; `cartelPagoVuelto=true`; abandono sin supervisor.
- Sin ofertas, descuentos, puntos, recargos, impresión, facturación ni pagos externos.
- Extensión `sales_journeys` y `calibration.verified_features` con `ventas-etapa1`; comprobar editor, grilla y confirmaciones del [contrato privado](../../docs/paquete.md).
- Calibrar apertura del editor, cantidad y confirmación; no sustituir editar por precargar cantidad antes de agregar.

## Pasos y resultados esperados

1. Abrir venta nueva y elegir comprobante interno no fiscal. **Esperado:** operación sin productos.
2. Cargar una unidad del producto de $1.000. **Esperado:** producto correcto, cantidad 1 e importe $1.000.
3. Abrir la edición de esa línea con doble clic en su celda identificada, comprobar el producto del editor, cambiar cantidad a 2 y guardar. **Esperado:** la misma línea muestra cantidad 2; no aparece otra línea por editar.
4. Revisar el total. **Esperado:** $2.000 ARS, sin descuentos ni cargos adicionales.
5. Abandonar confirmando descarte. **Esperado:** no queda una venta cobrada ni cambian stock/caja.

## Recuperación

Si falla, conservar el reporte privado y el paso observado. El runner cierra solo su proceso y prepara el baseline en la siguiente ejecución. No reparar resultados borrando datos ni modificar controles de seguridad. Las cancelaciones y reintentos descritos son parte del caso, no limpieza oculta. No continuar después de un fallo como si el paso hubiera aprobado.

## Evidencia para QA

INFO muestra ID, resultado y resumen; DEBUG añade pasos; TRACE diagnóstico saneado. En cualquier nivel un fallo debe incluir paso, esperado, observado, categoría y evidencia disponible. Si la causa no está demostrada, informar «causa no determinada». Capturas solo de ventanas QA autenticadas, sin credenciales. Registrar versión/hash del JAR, paquete, perfil y ruta privada del reporte.

## Anexo técnico de evidencia

Comparar antes de abrir y después de abandonar: mismos IDs de ventas, stock y caja. Verificar en UI identidad de línea, cantidad e importe; el oráculo de cancelación solo no demuestra la edición.

Lecturas acotadas a empresa/sucursal/computadora e identidad de artículo/operación. No usar `MAX(venId)` como identidad única ni escribir SQL de negocio. Las consultas son de solo lectura. Los selectores y el doble clic sobre la celda deben calibrarse sobre el JAR; la implementación no acredita ejecución real.

## Trazabilidad y límites

En el commit de referencia: `FormVenta.java:1748` abre el editor por doble clic; `:2081` reemplaza el mismo índice. `FormVentaDetalle.java:137` titula “Item de venta”, `:159` muestra el nombre del producto, `:183` muestra cantidad como decimal con punto y `:578` aplica la cantidad tras validar. `FormVentaProductoCantidadPolicyTest.java` y `FormVentaDetallePrecioUnitarioTest.java` son insumos; bultos, importe y cotización son variantes posteriores.

La [cobertura](../../docs/cobertura.md) identifica la referencia XGestion2 `release/189-lts`, `f34238183d494259bed1279dd7d9aac0ce16a3ae`. Fuente y tests orientan expectativas; no demuestran equivalencia del JAR ni ejecución real. No cubre variantes de otras configuraciones, monedas, permisos o dispositivos.
