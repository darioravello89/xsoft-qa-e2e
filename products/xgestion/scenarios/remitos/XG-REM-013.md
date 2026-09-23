---
{"id":"XG-REM-013","title":"Consultar remitos cerrados o de otra PC sin modificarlos","product":"xgestion","module":"remitos","tags":["xgestion","regression","compras","remitos","remitos-correccion","permisos","varios-puestos"],"status":"planned"}
---

# XG-REM-013 — Consultar remitos cerrados o de otra PC sin modificarlos

## Objetivo

Consultar remitos cerrados o de otra PC sin modificarlos, desde el trabajo de la persona que recibe mercadería o administra compras.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 6 del roadmap.** Ficha del [mapa de remitos](../../docs/remitos.md). No tiene suite Robot ni validación real. Remito de **compra/recepción**, distinto del remito emitido desde Venta.

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete privado autorizado y baseline recuperable. Ejecución real pendiente.
- Perfil base: ARS, remito de compra local, sin emisión fiscal/impresión; proveedor QA, sin listas, impuestos, bonificaciones ni costo universal salvo variante explícita. Factor de bulto 0 para unidades. Suma stock y Recibido activados; ambas opciones de actualizar precio desactivadas.
- Todos los códigos QA-REM y documentos citados son datos sintéticos **pendientes de seed/baseline**; no están garantizados por `catalogo-comercial-v1`. Preparar identidades y controles de colisiones antes de automatizar; no escribir SQL comercial durante el recorrido.
- Documentos sintéticos: cerrado QA-R-CERRADO con A × 2/$2.000; anulado QA-R-ANULADO; abierto QA-R-OTRAPC perteneciente a otro puesto. Paquete de varios puestos pendiente, no disponible en el baseline general.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Abrir el remito cerrado. | Se consultan cabecera/detalle/totales sin habilitar cambios. |
| Intentar agregar/editar, cambiar flags, proveedor, lista, IVA o cotización. | Acciones deshabilitadas o rechazadas; original sin cambios. |
| Repetir con anulado y abierto de otra PC en perfil autorizado. | Respeta restricción por estado/puesto y no crea versión editable. |
| Consultar nuevamente documento, stock, costos y deuda. | Conservan los valores previos. |

## Variantes y dependencias

La variante donde otro puesto cierra el documento mientras está abierto requiere laboratorio de concurrencia; dejar bloqueada hasta disponer de él. Comprobar tanto estado local como persistido antes de modificar.

## Evidencia y recuperación

Contrastar documento, detalle, inventario, costos/listas y cuenta del proveedor según el caso, por identidad y deltas. Un borrador puede persistir: comprobar ausencia de recepción, no ausencia absoluta de filas. Conservar el informe antes de salir por la interfaz y restaurar baseline antes de otra variante. No usar anulación como limpieza equivalente a restaurar precios e historial.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a esa revisión de XGestion2:

- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:259-262`.
- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:1001-1110`.
- `src/ModuloStocks/Vistas/FormCargaDeRemitoEstadoEdicionPolicy.java:1-36`.
- `test/ModuloStocks/Vistas/FormCargaDeRemitoEstadoEdicionPolicyTest.java:1-110`.

Los tests citados orientan las reglas; no acreditan ejecución E2E. Selectores/atajos y oráculos de compras pendientes de calibrar. Registrar SHA256 del JAR, paquete, perfil, variante y reporte privado. INFO resume; DEBUG muestra pasos; TRACE aporta diagnóstico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia, o causa no determinada; no registrar secretos ni filas completas.

