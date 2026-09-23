---
{"id":"XG-REM-009","title":"Salir sin guardar y recuperar el contenido original","product":"xgestion","module":"remitos","tags":["xgestion","regression","compras","remitos","remitos-correccion","recuperacion","stock"],"status":"planned"}
---

# XG-REM-009 — Salir sin guardar y recuperar el contenido original

## Objetivo

Salir sin guardar y recuperar el contenido original, desde el trabajo de la persona que recibe mercadería o administra compras.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 6 del roadmap.** Ficha del [mapa de remitos](../../docs/remitos.md). No tiene suite Robot ni validación real. Remito de **compra/recepción**, distinto del remito emitido desde Venta.

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete privado autorizado y baseline recuperable. Ejecución real pendiente.
- Perfil base: ARS, remito de compra local, sin emisión fiscal/impresión; proveedor QA, sin listas, impuestos, bonificaciones ni costo universal salvo variante explícita. Factor de bulto 0 para unidades. Suma stock y Recibido activados; ambas opciones de actualizar precio desactivadas.
- Todos los códigos QA-REM y documentos citados son datos sintéticos **pendientes de seed/baseline**; no están garantizados por `catalogo-comercial-v1`. Preparar identidades y controles de colisiones antes de automatizar; no escribir SQL comercial durante el recorrido.
- Baseline con borrador A × 1 a $1.000, nota Original y fecha 22/09/2026. Stock A/B 10, sin recepción.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Reabrir, cambiar nota/cantidad A a 3 y agregar B × 1 a $500. | Se ven cambios en curso, total $3.500. |
| Salir sin guardar. | Cierra descartando cambios de esta edición. |
| Reabrir el mismo borrador. | Vuelve A × 1, nota/fecha originales y total $1.000; B no integra detalle activo. |
| Consultar existencias/costos. | Conservan baseline; descartar no anuló una recepción. |

## Variantes y dependencias

En remito nuevo descartado se admite remito vacío pendiente reutilizable, pero ninguna recepción. Repetir con eliminación/bonificación para comprobar restauración completa del detalle.

## Evidencia y recuperación

Contrastar documento, detalle, inventario, costos/listas y cuenta del proveedor según el caso, por identidad y deltas. Un borrador puede persistir: comprobar ausencia de recepción, no ausencia absoluta de filas. Conservar el informe antes de salir por la interfaz y restaurar baseline antes de otra variante. No usar anulación como limpieza equivalente a restaurar precios e historial.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a esa revisión de XGestion2:

- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:1498-1524`.
- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:1586-1779`.

Los tests citados orientan las reglas; no acreditan ejecución E2E. Selectores/atajos y oráculos de compras pendientes de calibrar. Registrar SHA256 del JAR, paquete, perfil, variante y reporte privado. INFO resume; DEBUG muestra pasos; TRACE aporta diagnóstico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia, o causa no determinada; no registrar secretos ni filas completas.

