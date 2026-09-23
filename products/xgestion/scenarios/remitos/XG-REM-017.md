---
{"id":"XG-REM-017","title":"Cambiar proveedor o lista de compra sin conservar precio obsoleto","product":"xgestion","module":"remitos","tags":["xgestion","regression","compras","remitos","remitos-costos","precios","recuperacion"],"status":"planned"}
---

# XG-REM-017 — Cambiar proveedor o lista de compra sin conservar precio obsoleto

## Objetivo

Cambiar proveedor o lista de compra sin conservar precio obsoleto, desde el trabajo de la persona que recibe mercadería o administra compras.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P1, etapa 6 del roadmap.** Ficha del [mapa de remitos](../../docs/remitos.md). No tiene suite Robot ni validación real. Remito de **compra/recepción**, distinto del remito emitido desde Venta.

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete privado autorizado y baseline recuperable. Ejecución real pendiente.
- Perfil base: ARS, remito de compra local, sin emisión fiscal/impresión; proveedor QA, sin listas, impuestos, bonificaciones ni costo universal salvo variante explícita. Factor de bulto 0 para unidades. Suma stock y Recibido activados; ambas opciones de actualizar precio desactivadas.
- Todos los códigos QA-REM y documentos citados son datos sintéticos **pendientes de seed/baseline**; no están garantizados por `catalogo-comercial-v1`. Preparar identidades y controles de colisiones antes de automatizar; no escribir SQL comercial durante el recorrido.
- Proveedor A/lista QA-COMP-A ofrece producto a $700; proveedor B/lista QA-COMP-B a $800; costo previo $600. Listas de compra/proveedor, distintas de listas automáticas de venta. Variante de consulta pendiente separada: sin lista, historial QA conocido y mecanismo de laboratorio autorizado que permita observar y demorar reproduciblemente la respuesta; todavía pendiente de preparar.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Elegir A/lista A y producto. | Sugiere bruto $700 de lista explícita sin reconstruir compra bonificada anterior. |
| Cambiar proveedor/lista a B antes de agregar. | No agrega usando silenciosamente la sugerencia anterior $700. |
| Reseleccionar producto y esperar sugerencia actual; cargar una unidad. | Precio $800 y total $800. |
| En la variante sin lista y con respuesta retenida por el laboratorio, escribir manual $850 y luego liberar la respuesta previa. | Respuesta vieja no reemplaza $850; agregar requiere precio explícitamente resuelto. |

## Variantes y dependencias

Error/ambigüedad en sugerencia pide precio manual y conserva operación. La lista explícita diferente del costo evita consultar historial; no sirve como prueba de una respuesta histórica tardía. La variante pendiente permanece bloqueada sin el mecanismo controlado y no depende de la velocidad del operador. Para confirmar con lista seleccionada verificar actualización de esa lista; costo universal requiere perfil, listas control y esperado propio antes de habilitar. No presumir que flags generales frenan ambas rutas.

## Evidencia y recuperación

Contrastar documento, detalle, inventario, costos/listas y cuenta del proveedor según el caso, por identidad y deltas. Un borrador puede persistir: comprobar ausencia de recepción, no ausencia absoluta de filas. Conservar el informe antes de salir por la interfaz y restaurar baseline antes de otra variante. No usar anulación como limpieza equivalente a restaurar precios e historial.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a esa revisión de XGestion2:

- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:946-984`.
- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:1282-1291`.
- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:1872-1947`.
- `test/ModuloStocks/Vistas/SolicitudPrecioCompraTest.java:7-32`.
- `test/ModuloProductos/Entidades/CompraPrecioSugeridoTest.java:69-82`.
- `src/ModuloProductos/Entidades/CompraDetalle.java:178-195`.

Los tests citados orientan las reglas; no acreditan ejecución E2E. Selectores/atajos y oráculos de compras pendientes de calibrar. Registrar SHA256 del JAR, paquete, perfil, variante y reporte privado. INFO resume; DEBUG muestra pasos; TRACE aporta diagnóstico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia, o causa no determinada; no registrar secretos ni filas completas.
