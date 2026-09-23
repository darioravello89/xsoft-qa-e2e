---
{"id":"XG-REM-023","title":"Recibir en sucursal destino sin sumar también en origen","product":"xgestion","module":"remitos","tags":["xgestion","regression","compras","remitos","remitos-stock","stock","varios-puestos"],"status":"planned"}
---

# XG-REM-023 — Recibir en sucursal destino sin sumar también en origen

## Objetivo

Recibir en sucursal destino sin sumar también en origen, desde el trabajo de la persona que recibe mercadería o administra compras.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 6 del roadmap.** Ficha del [mapa de remitos](../../docs/remitos.md). No tiene suite Robot ni validación real. Remito de **compra/recepción**, distinto del remito emitido desde Venta.

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete privado autorizado y baseline recuperable. Ejecución real pendiente.
- Perfil base: ARS, remito de compra local, sin emisión fiscal/impresión; proveedor QA, sin listas, impuestos, bonificaciones ni costo universal salvo variante explícita. Factor de bulto 0 para unidades. Suma stock y Recibido activados; ambas opciones de actualizar precio desactivadas.
- Todos los códigos QA-REM y documentos citados son datos sintéticos **pendientes de seed/baseline**; no están garantizados por `catalogo-comercial-v1`. Preparar identidades y controles de colisiones antes de automatizar; no escribir SQL comercial durante el recorrido.
- Paquete multi-sucursal pendiente: empresa E, sucursales A/B, puesto de A. P stock A 10/B 20, recibir 3 unidades a $1.000 en destino B. Sin actualización de costos/listas/deuda.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Abrir en A y elegir destino B. | Emisor A/destino B visibles; producto de empresa QA. |
| Cargar P × 3 y rechazar primera confirmación. | Abierto, stocks A 10/B 20. |
| Confirmar y rechazar cuenta corriente. | Stock B 23/A 10; total $3.000 y recepción atribuible al documento. |
| Consultar documento y ambas existencias. | Origen/destino identificados, sin recepción en otra empresa/sucursal. |

## Variantes y dependencias

Destino igual a origen: A 13/B 20. Otra empresa como control requiere fixture propio y no debe mezclarse como destino. Bloqueado hasta disponer del paquete multicontexto; no se reutilizan sucursales reales.

## Evidencia y recuperación

Contrastar documento, detalle, inventario, costos/listas y cuenta del proveedor según el caso, por identidad y deltas. Un borrador puede persistir: comprobar ausencia de recepción, no ausencia absoluta de filas. Conservar el informe antes de salir por la interfaz y restaurar baseline antes de otra variante. No usar anulación como limpieza equivalente a restaurar precios e historial.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a esa revisión de XGestion2:

- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:1476-1482`.
- `src/ModuloProductos/Entidades/CompraDetalle.java:182-190`.

Los tests citados orientan las reglas; no acreditan ejecución E2E. Selectores/atajos y oráculos de compras pendientes de calibrar. Registrar SHA256 del JAR, paquete, perfil, variante y reporte privado. INFO resume; DEBUG muestra pasos; TRACE aporta diagnóstico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia, o causa no determinada; no registrar secretos ni filas completas.

