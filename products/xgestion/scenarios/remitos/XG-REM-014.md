---
{"id":"XG-REM-014","title":"Separar recibido de sumar stock por renglón y selección masiva","product":"xgestion","module":"remitos","tags":["xgestion","regression","compras","remitos","remitos-stock","stock"],"status":"planned"}
---

# XG-REM-014 — Separar recibido de sumar stock por renglón y selección masiva

## Objetivo

Separar recibido de sumar stock por renglón y selección masiva, desde el trabajo de la persona que recibe mercadería o administra compras.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 6 del roadmap.** Ficha del [mapa de remitos](../../docs/remitos.md). No tiene suite Robot ni validación real. Remito de **compra/recepción**, distinto del remito emitido desde Venta.

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete privado autorizado y baseline recuperable. Ejecución real pendiente.
- Perfil base: ARS, remito de compra local, sin emisión fiscal/impresión; proveedor QA, sin listas, impuestos, bonificaciones ni costo universal salvo variante explícita. Factor de bulto 0 para unidades. Suma stock y Recibido activados; ambas opciones de actualizar precio desactivadas.
- Todos los códigos QA-REM y documentos citados son datos sintéticos **pendientes de seed/baseline**; no están garantizados por `catalogo-comercial-v1`. Preparar identidades y controles de colisiones antes de automatizar; no escribir SQL comercial durante el recorrido.
- A/B/C stock 10, costo $600. Cargar A × 2 a $1.000, B × 3 a $500, C × 1 a $700. A recibido/suma stock; B recibido/no suma; C no recibido.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Cargar y configurar Recibido y Suma stock. | A/B integran total $3.500; C visible no suma al total por no recibido. |
| Alternar encabezado Recibido para todas y restaurar la selección indicada. | Filas siguen encabezado; al desmarcar C deja de indicar todas seleccionadas y total vuelve a $3.500. |
| Confirmar y rechazar cuenta corriente. | Stock A 12/B 10/C 10; Suma stock no reemplaza Recibido. |
| Consultar detalle/inventario/costos. | Flags y movimientos corresponden a cada identidad; C no recibido no altera costo ni stock. |

## Variantes y dependencias

Repetir encabezado Suma stock ON/OFF y mezcla por fila. Borrador conserva flags. Los encabezados masivos necesitan acceso accesible/teclado verificado antes de automatizar, sin coordenadas fijas.

## Evidencia y recuperación

Contrastar documento, detalle, inventario, costos/listas y cuenta del proveedor según el caso, por identidad y deltas. Un borrador puede persistir: comprobar ausencia de recepción, no ausencia absoluta de filas. Conservar el informe antes de salir por la interfaz y restaurar baseline antes de otra variante. No usar anulación como limpieza equivalente a restaurar precios e historial.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a esa revisión de XGestion2:

- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:1978-1997`.
- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:2324-2349`.
- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:2461-2532`.
- `src/ModuloProductos/Entidades/CompraDetalle.java:103-190`.

Los tests citados orientan las reglas; no acreditan ejecución E2E. Selectores/atajos y oráculos de compras pendientes de calibrar. Registrar SHA256 del JAR, paquete, perfil, variante y reporte privado. INFO resume; DEBUG muestra pasos; TRACE aporta diagnóstico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia, o causa no determinada; no registrar secretos ni filas completas.

