---
{"id":"XG-REM-021","title":"Recibir artículos ARS y USD según la conversión configurada","product":"xgestion","module":"remitos","tags":["xgestion","regression","compras","remitos","remitos-costos","monedas","precios","cuenta-corriente"],"status":"planned"}
---

# XG-REM-021 — Recibir artículos ARS y USD según la conversión configurada

## Objetivo

Recibir artículos ARS y USD según la conversión configurada, desde el trabajo de la persona que recibe mercadería o administra compras.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 6 del roadmap.** Ficha del [mapa de remitos](../../docs/remitos.md). No tiene suite Robot ni validación real. Remito de **compra/recepción**, distinto del remito emitido desde Venta.

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete privado autorizado y baseline recuperable. Ejecución real pendiente.
- Perfil base: ARS, remito de compra local, sin emisión fiscal/impresión; proveedor QA, sin listas, impuestos, bonificaciones ni costo universal salvo variante explícita. Factor de bulto 0 para unidades. Suma stock y Recibido activados; ambas opciones de actualizar precio desactivadas.
- Todos los códigos QA-REM y documentos citados son datos sintéticos **pendientes de seed/baseline**; no están garantizados por `catalogo-comercial-v1`. Preparar identidades y controles de colisiones antes de automatizar; no escribir SQL comercial durante el recorrido.
- U = QA-REM-USD a USD 10, A = QA-REM-ARS a $1.000. Cotización guardada $1.500/USD. Recibir U × 2 y opcional A × 1, sin impuestos/bonificación/actualización de costos. Perfiles conversión ON/OFF.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Con conversión ON cargar U × 2. | Unidad ARS $15.000 y total ARS $30.000; convierte una vez. |
| Restaurar perfil OFF y cargar U × 2. | Detalle USD 10/unidad y total mostrado USD 20. |
| En una variante OFF adicional agregar A × 1. | Documento mixto ARS $31.000, conservando moneda de cada línea. |
| Guardar/reabrir y confirmar las variantes. | Solo USD sin conversión cierra en USD; mixto o conversión activa en ARS. Cuenta del proveedor, si se acepta, conserva importe original/cotización/moneda. |

## Variantes y dependencias

Cotización cero/ausente bloquea línea USD sin agregar detalle parcial. Actualización de costos requiere matriz separada USD→USD, USD→ARS y ARS→USD, usando cotización guardada y evitando doble conversión.

## Evidencia y recuperación

Contrastar documento, detalle, inventario, costos/listas y cuenta del proveedor según el caso, por identidad y deltas. Un borrador puede persistir: comprobar ausencia de recepción, no ausencia absoluta de filas. Conservar el informe antes de salir por la interfaz y restaurar baseline antes de otra variante. No usar anulación como limpieza equivalente a restaurar precios e historial.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a esa revisión de XGestion2:

- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:1804-1810`.
- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:2558-2562`.
- `src/ModuloStocks/Vistas/CompraCotizacionRemitoPolicy.java:27-39`.
- `test/ModuloProductos/Entidades/CompraMonedaCalculadorTest.java:14-86`.
- `src/ModuloProductos/Entidades/CompraDetalle.java:120-173`.

Los tests citados orientan las reglas; no acreditan ejecución E2E. Selectores/atajos y oráculos de compras pendientes de calibrar. Registrar SHA256 del JAR, paquete, perfil, variante y reporte privado. INFO resume; DEBUG muestra pasos; TRACE aporta diagnóstico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia, o causa no determinada; no registrar secretos ni filas completas.

