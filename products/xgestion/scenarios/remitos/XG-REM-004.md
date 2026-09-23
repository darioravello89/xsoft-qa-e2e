---
{"id":"XG-REM-004","title":"Corregir cantidad o costo faltante antes de agregar","product":"xgestion","module":"remitos","tags":["xgestion","regression","compras","remitos","remitos-carga","recuperacion"],"status":"planned"}
---

# XG-REM-004 — Corregir cantidad o costo faltante antes de agregar

## Objetivo

Corregir cantidad o costo faltante antes de agregar, desde el trabajo de la persona que recibe mercadería o administra compras.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P1, etapa 6 del roadmap.** Ficha del [mapa de remitos](../../docs/remitos.md). No tiene suite Robot ni validación real. Remito de **compra/recepción**, distinto del remito emitido desde Venta.

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete privado autorizado y baseline recuperable. Ejecución real pendiente.
- Perfil base: ARS, remito de compra local, sin emisión fiscal/impresión; proveedor QA, sin listas, impuestos, bonificaciones ni costo universal salvo variante explícita. Factor de bulto 0 para unidades. Suma stock y Recibido activados; ambas opciones de actualizar precio desactivadas.
- Todos los códigos QA-REM y documentos citados son datos sintéticos **pendientes de seed/baseline**; no están garantizados por `catalogo-comercial-v1`. Preparar identidades y controles de colisiones antes de automatizar; no escribir SQL comercial durante el recorrido.
- A = QA-REM-UNIDAD, factor de bulto 0, sin detalle inicial. Cantidad vacía/0/-1/texto inválido si el control lo admite y costo vacío. Recuperación: cantidad 2, costo $1.000.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Seleccionar A e intentar agregar cantidades inválidas. | Se rechaza o se impide digitarlas; no aparece detalle. Cero con factor 0 no se convierte en una unidad. |
| Ingresar 2, vaciar costo e intentar agregar. | Solicita precio de costo; no usa silenciosamente el de otra selección. |
| Completar costo $1.000 y agregar. | Exactamente A × 2, total $2.000. |
| Salir sin guardar. | No quedan recepción ni movimientos de stock/costos por los intentos rechazados. |

## Variantes y dependencias

Distinguir bloqueo de digitación de rechazo al aceptar. No se fija una regla no verificada sobre costo negativo/cero: resolverla antes de agregar esas variantes.

## Evidencia y recuperación

Contrastar documento, detalle, inventario, costos/listas y cuenta del proveedor según el caso, por identidad y deltas. Un borrador puede persistir: comprobar ausencia de recepción, no ausencia absoluta de filas. Conservar el informe antes de salir por la interfaz y restaurar baseline antes de otra variante. No usar anulación como limpieza equivalente a restaurar precios e historial.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a esa revisión de XGestion2:

- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:1282-1359`.
- `src/ModuloStocks/Vistas/CompraCantidadCargaPolicy.java:35-72`.
- `test/ModuloStocks/Vistas/CompraCantidadCargaPolicyTest.java:15-45`.

Los tests citados orientan las reglas; no acreditan ejecución E2E. Selectores/atajos y oráculos de compras pendientes de calibrar. Registrar SHA256 del JAR, paquete, perfil, variante y reporte privado. INFO resume; DEBUG muestra pasos; TRACE aporta diagnóstico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia, o causa no determinada; no registrar secretos ni filas completas.

