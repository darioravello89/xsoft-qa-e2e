---
{"id":"XG-REM-015","title":"Elegir si el costo se actualiza con o sin bonificación","product":"xgestion","module":"remitos","tags":["xgestion","regression","compras","remitos","remitos-costos","precios"],"status":"planned"}
---

# XG-REM-015 — Elegir si el costo se actualiza con o sin bonificación

## Objetivo

Elegir si el costo se actualiza con o sin bonificación, desde el trabajo de la persona que recibe mercadería o administra compras.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 6 del roadmap.** Ficha del [mapa de remitos](../../docs/remitos.md). No tiene suite Robot ni validación real. Remito de **compra/recepción**, distinto del remito emitido desde Venta.

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete privado autorizado y baseline recuperable. Ejecución real pendiente.
- Perfil base: ARS, remito de compra local, sin emisión fiscal/impresión; proveedor QA, sin listas, impuestos, bonificaciones ni costo universal salvo variante explícita. Factor de bulto 0 para unidades. Suma stock y Recibido activados; ambas opciones de actualizar precio desactivadas.
- Todos los códigos QA-REM y documentos citados son datos sintéticos **pendientes de seed/baseline**; no están garantizados por `catalogo-comercial-v1`. Preparar identidades y controles de colisiones antes de automatizar; no escribir SQL comercial durante el recorrido.
- A/B/C/D costo actual $600, venta fija $1.500, precio calculado/costo universal OFF, ninguna lista. Una unidad de cada uno a bruto $1.000 y bonificación 10%: neto $900.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Asignar flags: A ninguno; B Actualiza precio; C solo con bonificación; D ambos. | Cada línea $900, total $3.600; todavía no cambia catálogo. |
| Guardar borrador y reabrir. | Conserva los cuatro pares de flags, costos aún $600. |
| Confirmar y rechazar cuenta corriente. | Costos A $600/B $1.000/C $900/D $900; venta fija de todos $1.500. |
| Consultar historial de costos. | Solo B/C/D registran cambios asociados a la recepción y criterio elegido. |

## Variantes y dependencias

Bonificación cero conserva bruto. Precio calculado requiere perfil separado con fórmula/esperado aprobado. Lista seleccionada y costo universal tienen rutas independientes: no asumir que desmarcar flags impide modificar esas listas.

## Evidencia y recuperación

Contrastar documento, detalle, inventario, costos/listas y cuenta del proveedor según el caso, por identidad y deltas. Un borrador puede persistir: comprobar ausencia de recepción, no ausencia absoluta de filas. Conservar el informe antes de salir por la interfaz y restaurar baseline antes de otra variante. No usar anulación como limpieza equivalente a restaurar precios e historial.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a esa revisión de XGestion2:

- `src/ModuloProductos/Entidades/CompraDetalle.java:145-194`.
- `test/ModuloProductos/Entidades/CompraActualizaPrecioPersistencePolicyTest.java:14-33`.
- `test/ModuloProductos/Entidades/CompraDetalleActualizacionPrecioMonedaPolicyTest.java:16-35`.

Los tests citados orientan las reglas; no acreditan ejecución E2E. Selectores/atajos y oráculos de compras pendientes de calibrar. Registrar SHA256 del JAR, paquete, perfil, variante y reporte privado. INFO resume; DEBUG muestra pasos; TRACE aporta diagnóstico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia, o causa no determinada; no registrar secretos ni filas completas.

