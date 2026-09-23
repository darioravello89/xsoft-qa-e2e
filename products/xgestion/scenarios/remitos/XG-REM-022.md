---
{"id":"XG-REM-022","title":"Conservar o actualizar cotización según estado del remito","product":"xgestion","module":"remitos","tags":["xgestion","regression","compras","remitos","remitos-costos","monedas","recuperacion"],"status":"planned"}
---

# XG-REM-022 — Conservar o actualizar cotización según estado del remito

## Objetivo

Conservar o actualizar cotización según estado del remito, desde el trabajo de la persona que recibe mercadería o administra compras.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 6 del roadmap.** Ficha del [mapa de remitos](../../docs/remitos.md). No tiene suite Robot ni validación real. Remito de **compra/recepción**, distinto del remito emitido desde Venta.

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete privado autorizado y baseline recuperable. Ejecución real pendiente.
- Perfil base: ARS, remito de compra local, sin emisión fiscal/impresión; proveedor QA, sin listas, impuestos, bonificaciones ni costo universal salvo variante explícita. Factor de bulto 0 para unidades. Suma stock y Recibido activados; ambas opciones de actualizar precio desactivadas.
- Todos los códigos QA-REM y documentos citados son datos sintéticos **pendientes de seed/baseline**; no están garantizados por `catalogo-comercial-v1`. Preparar identidades y controles de colisiones antes de automatizar; no escribir SQL comercial durante el recorrido.
- Borrador U × 2 a USD 10, cotización guardada $1.500; vigente $1.600. Baselines separados conversión ON/OFF, vacío/con líneas/cerrado. No cambiar datos de una instalación habitual.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Reabrir borrador con líneas a $1.500. | No reemplaza automáticamente por $1.600; conserva foto e importes. |
| Con conversión ON/líneas pedir Actualizar hoy. | Advierte que no puede reinterpretar precios guardados en ARS; mantiene $1.500/ARS $30.000. |
| En perfil OFF con líneas USD originales pedir Actualizar hoy. | Acepta $1.600, conserva USD 20 y equivalencia ARS $32.000. |
| Guardar/reabrir y consultar variante cerrada. | Cotización aceptada persiste en borrador; cerrado no permite actualizar. |

## Variantes y dependencias

Vacío reutilizado adopta configuración monetaria vigente; con detalle conserva foto. Cotización inválida rechazada incluso vacío. Salir sin guardar después de actualizar debe restaurar foto original del borrador editado.

## Evidencia y recuperación

Contrastar documento, detalle, inventario, costos/listas y cuenta del proveedor según el caso, por identidad y deltas. Un borrador puede persistir: comprobar ausencia de recepción, no ausencia absoluta de filas. Conservar el informe antes de salir por la interfaz y restaurar baseline antes de otra variante. No usar anulación como limpieza equivalente a restaurar precios e historial.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a esa revisión de XGestion2:

- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:1813-1864`.
- `src/ModuloStocks/Vistas/CompraCotizacionRemitoPolicy.java:14-33`.
- `test/ModuloStocks/Vistas/CompraCotizacionRemitoPolicyTest.java:16-51`.

Los tests citados orientan las reglas; no acreditan ejecución E2E. Selectores/atajos y oráculos de compras pendientes de calibrar. Registrar SHA256 del JAR, paquete, perfil, variante y reporte privado. INFO resume; DEBUG muestra pasos; TRACE aporta diagnóstico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia, o causa no determinada; no registrar secretos ni filas completas.

