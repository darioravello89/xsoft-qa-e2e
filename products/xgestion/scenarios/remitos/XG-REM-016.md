---
{"id":"XG-REM-016","title":"Repetir una compra bonificada sin descontar dos veces el costo","product":"xgestion","module":"remitos","tags":["xgestion","regression","compras","remitos","remitos-costos","precios","descuentos"],"status":"planned"}
---

# XG-REM-016 — Repetir una compra bonificada sin descontar dos veces el costo

## Objetivo

Repetir una compra bonificada sin descontar dos veces el costo, desde el trabajo de la persona que recibe mercadería o administra compras.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 6 del roadmap.** Ficha del [mapa de remitos](../../docs/remitos.md). No tiene suite Robot ni validación real. Remito de **compra/recepción**, distinto del remito emitido desde Venta.

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete privado autorizado y baseline recuperable. Ejecución real pendiente.
- Perfil base: ARS, remito de compra local, sin emisión fiscal/impresión; proveedor QA, sin listas, impuestos, bonificaciones ni costo universal salvo variante explícita. Factor de bulto 0 para unidades. Suma stock y Recibido activados; ambas opciones de actualizar precio desactivadas.
- Todos los códigos QA-REM y documentos citados son datos sintéticos **pendientes de seed/baseline**; no están garantizados por `catalogo-comercial-v1`. Preparar identidades y controles de colisiones antes de automatizar; no escribir SQL comercial durante el recorrido.
- Producto QA-REM-BRUTO del proveedor A, sin lista/impuestos. Primera compra: bruto $1.255,72, bonificación 55%, costo actualizado neto $565,07. Fixture debe conservar referencia exacta de origen.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Confirmar una unidad actualizando costo con bonificación. | Neto y nuevo costo $565,07; conserva bruto $1.255,72 y descuento 55% en documento. |
| Abrir otro remito del mismo proveedor y seleccionar producto. | Sugiere bruto $1.255,72; no toma $565,07 como nuevo bruto. |
| Aplicar 55% una sola vez a una unidad. | Neto $565,07; no vuelve a descontar el costo neto. |
| Confirmar segunda compra y consultar ambas. | Cada una conserva bruto/bonificación/neto; costo permanece $565,07. |

## Variantes y dependencias

Variante bruto $3.838,16/neto $1.727,17. Referencia nueva y legado no ambiguo. Otro proveedor/costo manual/antecedente sin actualización bonificada no recupera bruto ajeno; legado ambiguo exige precio explícito.

## Evidencia y recuperación

Contrastar documento, detalle, inventario, costos/listas y cuenta del proveedor según el caso, por identidad y deltas. Un borrador puede persistir: comprobar ausencia de recepción, no ausencia absoluta de filas. Conservar el informe antes de salir por la interfaz y restaurar baseline antes de otra variante. No usar anulación como limpieza equivalente a restaurar precios e historial.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a esa revisión de XGestion2:

- `src/ModuloProductos/Entidades/CompraPrecioSugerido.java:1-130`.
- `test/ModuloProductos/Entidades/CompraPrecioSugeridoTest.java:58-135`.
- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:1872-1947`.

Los tests citados orientan las reglas; no acreditan ejecución E2E. Selectores/atajos y oráculos de compras pendientes de calibrar. Registrar SHA256 del JAR, paquete, perfil, variante y reporte privado. INFO resume; DEBUG muestra pasos; TRACE aporta diagnóstico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia, o causa no determinada; no registrar secretos ni filas completas.

