---
{"id":"XG-REM-006","title":"Editar un renglón y eliminar otro antes de recibir","product":"xgestion","module":"remitos","tags":["xgestion","regression","compras","remitos","remitos-correccion","stock","precios"],"status":"planned"}
---

# XG-REM-006 — Editar un renglón y eliminar otro antes de recibir

## Objetivo

Editar un renglón y eliminar otro antes de recibir, desde el trabajo de la persona que recibe mercadería o administra compras.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 6 del roadmap.** Ficha del [mapa de remitos](../../docs/remitos.md). No tiene suite Robot ni validación real. Remito de **compra/recepción**, distinto del remito emitido desde Venta.

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete privado autorizado y baseline recuperable. Ejecución real pendiente.
- Perfil base: ARS, remito de compra local, sin emisión fiscal/impresión; proveedor QA, sin listas, impuestos, bonificaciones ni costo universal salvo variante explícita. Factor de bulto 0 para unidades. Suma stock y Recibido activados; ambas opciones de actualizar precio desactivadas.
- Todos los códigos QA-REM y documentos citados son datos sintéticos **pendientes de seed/baseline**; no están garantizados por `catalogo-comercial-v1`. Preparar identidades y controles de colisiones antes de automatizar; no escribir SQL comercial durante el recorrido.
- Remito abierto A × 2 a $1.000 y B × 1 a $500, total $2.500. Stock inicial 10 por producto. Sin impuestos/bultos/actualización de costos.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Seleccionar A y abrir edición. | El editor identifica A con cantidad 2/costo $1.000, sin editar B. |
| Cambiar A a 3 unidades a $900 y aceptar. | A $2.700, B $500, total $3.200. |
| Abrir B y usar Eliminar. | B deja de integrar detalle activo; A se conserva, total $2.700. |
| Confirmar y rechazar cuenta corriente. | Recibe solo A × 3: stock A 13/B 10, ligado a una recepción. |

## Variantes y dependencias

Cancelar el editor conserva la línea previa. Variante bultos conserva factor/cantidad base. La fuente abre el editor por doble clic: falta atajo/acción accesible confirmada, sin coordenadas fijas ni reutilizar automáticamente autorización de otra pantalla.

## Evidencia y recuperación

Contrastar documento, detalle, inventario, costos/listas y cuenta del proveedor según el caso, por identidad y deltas. Un borrador puede persistir: comprobar ausencia de recepción, no ausencia absoluta de filas. Conservar el informe antes de salir por la interfaz y restaurar baseline antes de otra variante. No usar anulación como limpieza equivalente a restaurar precios e historial.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a esa revisión de XGestion2:

- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:2297-2315`.
- `src/ModuloStocks/Vistas/FormOrdenCompraDetalle.java:448-483`.
- `src/ModuloStocks/Vistas/FormOrdenCompraDetalle.java:619-698`.

Los tests citados orientan las reglas; no acreditan ejecución E2E. Selectores/atajos y oráculos de compras pendientes de calibrar. Registrar SHA256 del JAR, paquete, perfil, variante y reporte privado. INFO resume; DEBUG muestra pasos; TRACE aporta diagnóstico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia, o causa no determinada; no registrar secretos ni filas completas.

