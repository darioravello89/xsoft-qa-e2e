---
{"id":"XG-REM-024","title":"Anular una recepción y revertir stock y deuda sin restaurar precios","product":"xgestion","module":"remitos","tags":["xgestion","regression","compras","remitos","remitos-correccion","remitos-stock","stock","devoluciones","cuenta-corriente","permisos"],"status":"planned"}
---

# XG-REM-024 — Anular una recepción y revertir stock y deuda sin restaurar precios

## Objetivo

Anular una recepción y revertir stock y deuda sin restaurar precios, desde el trabajo de la persona que recibe mercadería o administra compras.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 6 del roadmap.** Ficha del [mapa de remitos](../../docs/remitos.md). No tiene suite Robot ni validación real. Remito de **compra/recepción**, distinto del remito emitido desde Venta.

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete privado autorizado y baseline recuperable. Ejecución real pendiente.
- Perfil base: ARS, remito de compra local, sin emisión fiscal/impresión; proveedor QA, sin listas, impuestos, bonificaciones ni costo universal salvo variante explícita. Factor de bulto 0 para unidades. Suma stock y Recibido activados; ambas opciones de actualizar precio desactivadas.
- Todos los códigos QA-REM y documentos citados son datos sintéticos **pendientes de seed/baseline**; no están garantizados por `catalogo-comercial-v1`. Preparar identidades y controles de colisiones antes de automatizar; no escribir SQL comercial durante el recorrido.
- Remito cerrado QA-R-024: A × 2 a $1.000. Stock inicial 10/recibido 12, costo anterior $600/actualizado $1.000. Cuenta proveedor: compra $2.000/pagado $500/deuda $1.500. Operador con Anular Orden habilitado.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Pedir Anular Orden y rechazar confirmación. | Sigue cerrado, stock 12/deuda $1.500; ninguna reversión. |
| Repetir, leer advertencia, aceptar con motivo Recepción QA anulada. | Anulado con motivo, stock 10/deuda del remito compensada. |
| Consultar costo y precio del producto. | Costo conserva $1.000: la advertencia informa que precios modificados no vuelven atrás. |
| Consultar documento/cuenta nuevamente. | Trazabilidad vincula original/anulación; no hay movimientos extra por el intento rechazado. |

## Variantes y dependencias

Con/sin cuenta corriente; Suma stock OFF no revierte existencias; bultos revierten cantidad base guardada aunque cambie factor actual. La regla de rol restringido necesita permiso concreto calibrado. No usar anulación como restauración de baseline.

## Evidencia y recuperación

Contrastar documento, detalle, inventario, costos/listas y cuenta del proveedor según el caso, por identidad y deltas. Un borrador puede persistir: comprobar ausencia de recepción, no ausencia absoluta de filas. Conservar el informe antes de salir por la interfaz y restaurar baseline antes de otra variante. No usar anulación como limpieza equivalente a restaurar precios e historial.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a esa revisión de XGestion2:

- `src/ModuloStocks/Vistas/FormListadoOrdenesCompras.java:538-561`.
- `src/ModuloProductos/Entidades/Compra.java:652-700`.
- `src/ModuloProductos/Entidades/CompraDetalle.java:214-269`.
- `test/ModuloProductos/Entidades/CompraDetalleBultosPersistencePolicyTest.java:39-45`.

Los tests citados orientan las reglas; no acreditan ejecución E2E. Selectores/atajos y oráculos de compras pendientes de calibrar. Registrar SHA256 del JAR, paquete, perfil, variante y reporte privado. INFO resume; DEBUG muestra pasos; TRACE aporta diagnóstico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia, o causa no determinada; no registrar secretos ni filas completas.

