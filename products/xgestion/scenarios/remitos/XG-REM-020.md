---
{"id":"XG-REM-020","title":"Distinguir IVA de otros impuestos en detalle y total","product":"xgestion","module":"remitos","tags":["xgestion","regression","compras","remitos","remitos-costos","precios","comprobantes"],"status":"planned"}
---

# XG-REM-020 — Distinguir IVA de otros impuestos en detalle y total

## Objetivo

Distinguir IVA de otros impuestos en detalle y total, desde el trabajo de la persona que recibe mercadería o administra compras.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 6 del roadmap.** Ficha del [mapa de remitos](../../docs/remitos.md). No tiene suite Robot ni validación real. Remito de **compra/recepción**, distinto del remito emitido desde Venta.

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete privado autorizado y baseline recuperable. Ejecución real pendiente.
- Perfil base: ARS, remito de compra local, sin emisión fiscal/impresión; proveedor QA, sin listas, impuestos, bonificaciones ni costo universal salvo variante explícita. Factor de bulto 0 para unidades. Suma stock y Recibido activados; ambas opciones de actualizar precio desactivadas.
- Todos los códigos QA-REM y documentos citados son datos sintéticos **pendientes de seed/baseline**; no están garantizados por `catalogo-comercial-v1`. Preparar identidades y controles de colisiones antes de automatizar; no escribir SQL comercial durante el recorrido.
- Variantes independientes: A costo $100, cantidad 2, IVA21%, otro impuesto fijo $7,50/unidad. B costo $100, cantidad 2, sin IVA, otro impuesto 5%. Adicional de compra opcional $3,33 con fixture propio.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Cargar A × 2 en primera variante. | Base $200, IVA $42, otros $15, impuestos $57, total $257. |
| Abrir detalle y editar A a 3. | Base $300, IVA $63, otros $22,50, total $385,50; recalcula una vez. |
| Restaurar baseline y cargar B × 2 sin IVA. | IVA $0, otros $10, total $210; apagar IVA no elimina los otros impuestos. |
| Añadir adicional fijo $3,33 en variante habilitada y guardar/reabrir. | Otros producto $10 y adicional $3,33 separados, total $213,33; no suma también al IVA. |

## Variantes y dependencias

Fijo/porcentaje, cantidad fraccionaria y cero. El administrador de impuestos necesita seed de tributos y selectores propios. ARS/USD se complementa con REM-021/022, sin inferir que repetir importes valida su moneda.

## Evidencia y recuperación

Contrastar documento, detalle, inventario, costos/listas y cuenta del proveedor según el caso, por identidad y deltas. Un borrador puede persistir: comprobar ausencia de recepción, no ausencia absoluta de filas. Conservar el informe antes de salir por la interfaz y restaurar baseline antes de otra variante. No usar anulación como limpieza equivalente a restaurar precios e historial.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a esa revisión de XGestion2:

- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:2024-2094`.
- `src/ModuloStocks/Vistas/CompraDetalleImpuestosPresentacionPolicy.java:1-67`.
- `test/ModuloStocks/Vistas/CompraDetalleImpuestosPresentacionPolicyTest.java:12-49`.
- `test/ModuloProductos/Entidades/CompraDetalleImpuestosTest.java:15-33`.

Los tests citados orientan las reglas; no acreditan ejecución E2E. Selectores/atajos y oráculos de compras pendientes de calibrar. Registrar SHA256 del JAR, paquete, perfil, variante y reporte privado. INFO resume; DEBUG muestra pasos; TRACE aporta diagnóstico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia, o causa no determinada; no registrar secretos ni filas completas.

