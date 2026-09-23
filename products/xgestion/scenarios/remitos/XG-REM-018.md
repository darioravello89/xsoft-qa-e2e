---
{"id":"XG-REM-018","title":"Combinar bonificación de producto con descuento o recargo general","product":"xgestion","module":"remitos","tags":["xgestion","regression","compras","remitos","remitos-costos","descuentos","precios"],"status":"planned"}
---

# XG-REM-018 — Combinar bonificación de producto con descuento o recargo general

## Objetivo

Combinar bonificación de producto con descuento o recargo general, desde el trabajo de la persona que recibe mercadería o administra compras.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P1, etapa 6 del roadmap.** Ficha del [mapa de remitos](../../docs/remitos.md). No tiene suite Robot ni validación real. Remito de **compra/recepción**, distinto del remito emitido desde Venta.

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete privado autorizado y baseline recuperable. Ejecución real pendiente.
- Perfil base: ARS, remito de compra local, sin emisión fiscal/impresión; proveedor QA, sin listas, impuestos, bonificaciones ni costo universal salvo variante explícita. Factor de bulto 0 para unidades. Suma stock y Recibido activados; ambas opciones de actualizar precio desactivadas.
- Todos los códigos QA-REM y documentos citados son datos sintéticos **pendientes de seed/baseline**; no están garantizados por `catalogo-comercial-v1`. Preparar identidades y controles de colisiones antes de automatizar; no escribir SQL comercial durante el recorrido.
- A × 2 a bruto $1.000, bonificación 10%, sin impuestos: neto $1.800. Ajuste general por importe $100.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Cargar A con bonificación. | Neto unitario $900; subtotal neto $1.800. |
| Aplicar descuento general $100. | Total $1.700; importe positivo en modo resta, sin alterar cantidad. |
| Cambiar a recargo $100 y guardar borrador. | Total $1.900; importe positivo en modo suma. |
| Reabrir, volver a descuento $100 y confirmar. | Conserva signo al reabrir y termina $1.700; no invierte ni duplica ajuste. |

## Variantes y dependencias

Ajuste cero/descuento/recargo en corridas independientes; bonificación 0%/100%. Valores legacy 99 y 99,99 requieren expectativa específica antes de automatizar; no tratarlos como porcentajes corrientes sin revisar la fuente.

## Evidencia y recuperación

Contrastar documento, detalle, inventario, costos/listas y cuenta del proveedor según el caso, por identidad y deltas. Un borrador puede persistir: comprobar ausencia de recepción, no ausencia absoluta de filas. Conservar el informe antes de salir por la interfaz y restaurar baseline antes de otra variante. No usar anulación como limpieza equivalente a restaurar precios e historial.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a esa revisión de XGestion2:

- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:1332-1339`.
- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:1955-1957`.
- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:2061-2086`.
- `src/ModuloStocks/Vistas/CompraDescuentoRemitoPolicy.java:1-30`.
- `test/ModuloStocks/Vistas/CompraDescuentoRemitoPolicyTest.java:12-45`.

Los tests citados orientan las reglas; no acreditan ejecución E2E. Selectores/atajos y oráculos de compras pendientes de calibrar. Registrar SHA256 del JAR, paquete, perfil, variante y reporte privado. INFO resume; DEBUG muestra pasos; TRACE aporta diagnóstico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia, o causa no determinada; no registrar secretos ni filas completas.

