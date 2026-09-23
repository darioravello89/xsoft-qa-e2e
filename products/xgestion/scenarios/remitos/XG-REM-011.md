---
{"id":"XG-REM-011","title":"Exigir fecha de recepción y detalle antes de confirmar","product":"xgestion","module":"remitos","tags":["xgestion","regression","compras","remitos","remitos-carga","comprobantes","recuperacion"],"status":"planned"}
---

# XG-REM-011 — Exigir fecha de recepción y detalle antes de confirmar

## Objetivo

Exigir fecha de recepción y detalle antes de confirmar, desde el trabajo de la persona que recibe mercadería o administra compras.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P1, etapa 6 del roadmap.** Ficha del [mapa de remitos](../../docs/remitos.md). No tiene suite Robot ni validación real. Remito de **compra/recepción**, distinto del remito emitido desde Venta.

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete privado autorizado y baseline recuperable. Ejecución real pendiente.
- Perfil base: ARS, remito de compra local, sin emisión fiscal/impresión; proveedor QA, sin listas, impuestos, bonificaciones ni costo universal salvo variante explícita. Factor de bulto 0 para unidades. Suma stock y Recibido activados; ambas opciones de actualizar precio desactivadas.
- Todos los códigos QA-REM y documentos citados son datos sintéticos **pendientes de seed/baseline**; no están garantizados por `catalogo-comercial-v1`. Preparar identidades y controles de colisiones antes de automatizar; no escribir SQL comercial durante el recorrido.
- Remito nuevo vacío, proveedor QA, número QA-R-011. Fecha primero vacía, luego 22/09/2026. A × 1 a $1.000 para recuperación.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Intentar guardar con fecha vacía. | Solicita fecha de recepción y no confirma. |
| Completar fecha y confirmar el remito nuevo vacío. | Exige al menos un ítem, sin recepción vacía. |
| Agregar A × 1 y guardar como borrador. | Abierto por $1.000 con fecha 22/09/2026. |
| Reabrir y confirmar. | Conserva fecha de recepción y recibe una sola unidad. |

## Variantes y dependencias

Distinguir nuevo vacío de edición de borrador existente que queda sin ítems: este último permite confirmación explícita con advertencia y total cero. Rechazarla conserva el borrador sin cerrar.

## Evidencia y recuperación

Contrastar documento, detalle, inventario, costos/listas y cuenta del proveedor según el caso, por identidad y deltas. Un borrador puede persistir: comprobar ausencia de recepción, no ausencia absoluta de filas. Conservar el informe antes de salir por la interfaz y restaurar baseline antes de otra variante. No usar anulación como limpieza equivalente a restaurar precios e historial.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a esa revisión de XGestion2:

- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:1430-1451`.
- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:1480-1482`.
- `test/ModuloStocks/Vistas/FormCargaDeRemitoFechaRecepcionPolicyTest.java:14-42`.

Los tests citados orientan las reglas; no acreditan ejecución E2E. Selectores/atajos y oráculos de compras pendientes de calibrar. Registrar SHA256 del JAR, paquete, perfil, variante y reporte privado. INFO resume; DEBUG muestra pasos; TRACE aporta diagnóstico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia, o causa no determinada; no registrar secretos ni filas completas.

