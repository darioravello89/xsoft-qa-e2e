---
{"id":"XG-REM-003","title":"Recibir materia prima con cantidad fraccionaria y vencimiento","product":"xgestion","module":"remitos","tags":["xgestion","regression","compras","remitos","remitos-carga","remitos-stock","stock","productos"],"status":"planned"}
---

# XG-REM-003 — Recibir materia prima con cantidad fraccionaria y vencimiento

## Objetivo

Recibir materia prima con cantidad fraccionaria y vencimiento, desde el trabajo de la persona que recibe mercadería o administra compras.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 6 del roadmap.** Ficha del [mapa de remitos](../../docs/remitos.md). No tiene suite Robot ni validación real. Remito de **compra/recepción**, distinto del remito emitido desde Venta.

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete privado autorizado y baseline recuperable. Ejecución real pendiente.
- Perfil base: ARS, remito de compra local, sin emisión fiscal/impresión; proveedor QA, sin listas, impuestos, bonificaciones ni costo universal salvo variante explícita. Factor de bulto 0 para unidades. Suma stock y Recibido activados; ambas opciones de actualizar precio desactivadas.
- Todos los códigos QA-REM y documentos citados son datos sintéticos **pendientes de seed/baseline**; no están garantizados por `catalogo-comercial-v1`. Preparar identidades y controles de colisiones antes de automatizar; no escribir SQL comercial durante el recorrido.
- MP = QA-REM-HARINA, materia prima en kg, factor 0, stock 10 kg, costo $400/kg. Recibir 2,5 kg, vencimiento 31/12/2026; total $1.000. Producto de venta A como control.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Usar F2 Ver Materia Prima y elegir MP. | Identifica la materia prima y unidad kg correctas. |
| Cargar 2,5 kg a $400 y vencimiento 31/12/2026. | Detalle con 2,5 kg/$1.000 y vencimiento conservado. |
| Confirmar y rechazar cuenta corriente. | Stock MP 12,5 kg; A no cambia; no registra producción ni consume receta. |
| Abrir otra carga y seleccionar MP. | No arrastra automáticamente la fecha de vencimiento anterior. |

## Variantes y dependencias

Con/sin vencimiento en corridas separadas. Variante 0,125 kg a $400 = $50. Recibir insumos no acredita consumo de recetas en Restobar.

## Evidencia y recuperación

Contrastar documento, detalle, inventario, costos/listas y cuenta del proveedor según el caso, por identidad y deltas. Un borrador puede persistir: comprobar ausencia de recepción, no ausencia absoluta de filas. Conservar el informe antes de salir por la interfaz y restaurar baseline antes de otra variante. No usar anulación como limpieza equivalente a restaurar precios e historial.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a esa revisión de XGestion2:

- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:1256-1279`.
- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:2617-2635`.
- `src/ModuloProductos/Entidades/CompraDetalle.java:182-190`.

Los tests citados orientan las reglas; no acreditan ejecución E2E. Selectores/atajos y oráculos de compras pendientes de calibrar. Registrar SHA256 del JAR, paquete, perfil, variante y reporte privado. INFO resume; DEBUG muestra pasos; TRACE aporta diagnóstico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia, o causa no determinada; no registrar secretos ni filas completas.

