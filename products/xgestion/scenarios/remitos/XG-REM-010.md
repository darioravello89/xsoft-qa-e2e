---
{"id":"XG-REM-010","title":"Cancelar la salida y conservar los cambios para continuar","product":"xgestion","module":"remitos","tags":["xgestion","regression","compras","remitos","remitos-correccion","recuperacion"],"status":"planned"}
---

# XG-REM-010 — Cancelar la salida y conservar los cambios para continuar

## Objetivo

Cancelar la salida y conservar los cambios para continuar, desde el trabajo de la persona que recibe mercadería o administra compras.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P1, etapa 6 del roadmap.** Ficha del [mapa de remitos](../../docs/remitos.md). No tiene suite Robot ni validación real. Remito de **compra/recepción**, distinto del remito emitido desde Venta.

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete privado autorizado y baseline recuperable. Ejecución real pendiente.
- Perfil base: ARS, remito de compra local, sin emisión fiscal/impresión; proveedor QA, sin listas, impuestos, bonificaciones ni costo universal salvo variante explícita. Factor de bulto 0 para unidades. Suma stock y Recibido activados; ambas opciones de actualizar precio desactivadas.
- Todos los códigos QA-REM y documentos citados son datos sintéticos **pendientes de seed/baseline**; no están garantizados por `catalogo-comercial-v1`. Preparar identidades y controles de colisiones antes de automatizar; no escribir SQL comercial durante el recorrido.
- Remito nuevo A × 2 a $1.000, nota Seguir cargando; stock A/B 10, total $2.000.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Solicitar salir con cambios. | Aparecen Guardar, Salir sin guardar y Cancelar. |
| Elegir Cancelar o cerrar el diálogo. | Carga abierta con A × 2 y nota modificada, sin confirmar ni descartar. |
| Agregar B × 1 a $500. | Total $2.500 manteniendo identidad del remito. |
| Guardar como borrador al salir y reabrir. | Las dos líneas/nota siguen presentes; abierto, sin recepción. |

## Variantes y dependencias

Ejecutar por cierre de ventana y Escape solo después de calibrar sus controles; no enviar Escape a un diálogo distinto.

## Evidencia y recuperación

Contrastar documento, detalle, inventario, costos/listas y cuenta del proveedor según el caso, por identidad y deltas. Un borrador puede persistir: comprobar ausencia de recepción, no ausencia absoluta de filas. Conservar el informe antes de salir por la interfaz y restaurar baseline antes de otra variante. No usar anulación como limpieza equivalente a restaurar precios e historial.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a esa revisión de XGestion2:

- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:270-291`.
- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:1498-1524`.

Los tests citados orientan las reglas; no acreditan ejecución E2E. Selectores/atajos y oráculos de compras pendientes de calibrar. Registrar SHA256 del JAR, paquete, perfil, variante y reporte privado. INFO resume; DEBUG muestra pasos; TRACE aporta diagnóstico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia, o causa no determinada; no registrar secretos ni filas completas.

