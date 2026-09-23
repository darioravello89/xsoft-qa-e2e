---
{"id":"XG-REM-005","title":"Cargar bultos y conservar su equivalencia en unidades","product":"xgestion","module":"remitos","tags":["xgestion","regression","compras","remitos","remitos-carga","remitos-stock","stock"],"status":"planned"}
---

# XG-REM-005 — Cargar bultos y conservar su equivalencia en unidades

## Objetivo

Cargar bultos y conservar su equivalencia en unidades, desde el trabajo de la persona que recibe mercadería o administra compras.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 6 del roadmap.** Ficha del [mapa de remitos](../../docs/remitos.md). No tiene suite Robot ni validación real. Remito de **compra/recepción**, distinto del remito emitido desde Venta.

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete privado autorizado y baseline recuperable. Ejecución real pendiente.
- Perfil base: ARS, remito de compra local, sin emisión fiscal/impresión; proveedor QA, sin listas, impuestos, bonificaciones ni costo universal salvo variante explícita. Factor de bulto 0 para unidades. Suma stock y Recibido activados; ambas opciones de actualizar precio desactivadas.
- Todos los códigos QA-REM y documentos citados son datos sintéticos **pendientes de seed/baseline**; no están garantizados por `catalogo-comercial-v1`. Preparar identidades y controles de colisiones antes de automatizar; no escribir SQL comercial durante el recorrido.
- B = QA-REM-BULTO, 16 unidades por bulto, stock 20 unidades, costo por unidad base $100. Recibir 5 bultos = 80 unidades, total $8.000. A = QA-REM-UNIDAD, factor 0.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Seleccionar B. | Cantidad se presenta como BULTOS y muestra equivalencia. |
| Ingresar 5 bultos a costo $100 por unidad base. | Resumen 5 × 16 = 80 unidades, detalle de 80 y total $8.000. |
| Confirmar y consultar detalle/stock. | Conserva ingreso 5 bultos/factor 16/cantidad base 80; stock 100 unidades. |
| En otra carga seleccionar A. | Vuelve a cantidad directa y no arrastra factor ni resumen de B. |

## Variantes y dependencias

Variantes autónomas: 1,5 bultos × 2,5 kg = 3,750 kg; 1,111 × 1,111 = 1,234 unidades, tres decimales. Bultos 0/negativos se rechazan. Factor nulo/cero/negativo no habilita modo bultos automático.

## Evidencia y recuperación

Contrastar documento, detalle, inventario, costos/listas y cuenta del proveedor según el caso, por identidad y deltas. Un borrador puede persistir: comprobar ausencia de recepción, no ausencia absoluta de filas. Conservar el informe antes de salir por la interfaz y restaurar baseline antes de otra variante. No usar anulación como limpieza equivalente a restaurar precios e historial.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a esa revisión de XGestion2:

- `src/ModuloStocks/Vistas/CompraCantidadCargaPolicy.java:31-89`.
- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:2639-2678`.
- `test/ModuloStocks/Vistas/CompraCantidadCargaPolicyTest.java:54-116`.
- `test/ModuloProductos/Entidades/CompraDetalleBultosPersistencePolicyTest.java:16-45`.

Los tests citados orientan las reglas; no acreditan ejecución E2E. Selectores/atajos y oráculos de compras pendientes de calibrar. Registrar SHA256 del JAR, paquete, perfil, variante y reporte privado. INFO resume; DEBUG muestra pasos; TRACE aporta diagnóstico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia, o causa no determinada; no registrar secretos ni filas completas.

