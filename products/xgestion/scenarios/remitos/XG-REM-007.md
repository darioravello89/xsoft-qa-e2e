---
{"id":"XG-REM-007","title":"Rechazar la confirmación y continuar el mismo remito","product":"xgestion","module":"remitos","tags":["xgestion","regression","compras","remitos","remitos-correccion","recuperacion","stock"],"status":"planned"}
---

# XG-REM-007 — Rechazar la confirmación y continuar el mismo remito

## Objetivo

Rechazar la confirmación y continuar el mismo remito, desde el trabajo de la persona que recibe mercadería o administra compras.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 6 del roadmap.** Ficha del [mapa de remitos](../../docs/remitos.md). No tiene suite Robot ni validación real. Remito de **compra/recepción**, distinto del remito emitido desde Venta.

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete privado autorizado y baseline recuperable. Ejecución real pendiente.
- Perfil base: ARS, remito de compra local, sin emisión fiscal/impresión; proveedor QA, sin listas, impuestos, bonificaciones ni costo universal salvo variante explícita. Factor de bulto 0 para unidades. Suma stock y Recibido activados; ambas opciones de actualizar precio desactivadas.
- Todos los códigos QA-REM y documentos citados son datos sintéticos **pendientes de seed/baseline**; no están garantizados por `catalogo-comercial-v1`. Preparar identidades y controles de colisiones antes de automatizar; no escribir SQL comercial durante el recorrido.
- Remito abierto A × 2 a $1.000, stock A/B 10, costo previo $600, total $2.000. B a $500 como agregado posterior.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Confirmar la carga y responder No. | Sigue abierto por $2.000; no suma stock ni registra deuda. |
| Agregar B × 1 a $500. | El mismo documento conserva A y totaliza $2.500. |
| Confirmar y rechazar cuenta corriente. | Una recepción de A × 2/B × 1; no duplica A por el intento anterior. |
| Consultar documento e inventario. | Cerrado por $2.500, stock A 12/B 11, cantidades aceptadas una sola vez. |

## Variantes y dependencias

Rechazar repetidamente o cerrar el diálogo no confirma ni acumula efectos. Preparar cada repetición desde baseline.

## Evidencia y recuperación

Contrastar documento, detalle, inventario, costos/listas y cuenta del proveedor según el caso, por identidad y deltas. Un borrador puede persistir: comprobar ausencia de recepción, no ausencia absoluta de filas. Conservar el informe antes de salir por la interfaz y restaurar baseline antes de otra variante. No usar anulación como limpieza equivalente a restaurar precios e historial.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a esa revisión de XGestion2:

- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:1439-1473`.
- `src/ModuloProductos/Entidades/Compra.java:513-531`.

Los tests citados orientan las reglas; no acreditan ejecución E2E. Selectores/atajos y oráculos de compras pendientes de calibrar. Registrar SHA256 del JAR, paquete, perfil, variante y reporte privado. INFO resume; DEBUG muestra pasos; TRACE aporta diagnóstico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia, o causa no determinada; no registrar secretos ni filas completas.

