---
{"id":"XG-REM-001","title":"Recibir productos y confirmar un remito de compra","product":"xgestion","module":"remitos","tags":["xgestion","regression","compras","remitos","remitos-carga","stock","comprobantes","cuenta-corriente"],"status":"planned"}
---

# XG-REM-001 — Recibir productos y confirmar un remito de compra

## Objetivo

Recibir productos y confirmar un remito de compra, desde el trabajo de la persona que recibe mercadería o administra compras.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 6 del roadmap.** Ficha del [mapa de remitos](../../docs/remitos.md). No tiene suite Robot ni validación real. Remito de **compra/recepción**, distinto del remito emitido desde Venta.

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete privado autorizado y baseline recuperable. Ejecución real pendiente.
- Perfil base: ARS, remito de compra local, sin emisión fiscal/impresión; proveedor QA, sin listas, impuestos, bonificaciones ni costo universal salvo variante explícita. Factor de bulto 0 para unidades. Suma stock y Recibido activados; ambas opciones de actualizar precio desactivadas.
- Todos los códigos QA-REM y documentos citados son datos sintéticos **pendientes de seed/baseline**; no están garantizados por `catalogo-comercial-v1`. Preparar identidades y controles de colisiones antes de automatizar; no escribir SQL comercial durante el recorrido.
- Proveedor QA-REM-PROV-A, número QA-R-001, recepción 22/09/2026, nota Recepción QA. A = QA-REM-UNIDAD: stock 10, costo previo $600 y venta fija $1.500. Recibir 2 unidades a bruto $1.000, total $2.000.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Elegir proveedor, número, fecha y nota en un remito nuevo. | Se muestra una operación abierta del contexto QA con esos datos. |
| Cargar A × 2 a $1.000. | Línea por 2 unidades, total $2.000; stock previo continúa en 10. |
| Confirmar y rechazar el envío a cuenta corriente. | Cierra por $2.000; stock A 12, costo $600 y venta $1.500; sin deuda del proveedor. |
| Consultar el cerrado y abrir una nueva carga. | Conserva cabecera y detalle; la nueva operación no repite las líneas confirmadas. |

## Variantes y dependencias

Corrida independiente aceptando cuenta corriente con pagado $500: compra $2.000, pago $500 y deuda neta $1.500 asociados al remito. El registro no acredita pago bancario externo.

## Evidencia y recuperación

Contrastar documento, detalle, inventario, costos/listas y cuenta del proveedor según el caso, por identidad y deltas. Un borrador puede persistir: comprobar ausencia de recepción, no ausencia absoluta de filas. Conservar el informe antes de salir por la interfaz y restaurar baseline antes de otra variante. No usar anulación como limpieza equivalente a restaurar precios e historial.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a esa revisión de XGestion2:

- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:1430-1485`.
- `src/ModuloProductos/Entidades/Compra.java:448-531`.
- `src/ModuloProductos/Entidades/CompraDetalle.java:100-191`.

Los tests citados orientan las reglas; no acreditan ejecución E2E. Selectores/atajos y oráculos de compras pendientes de calibrar. Registrar SHA256 del JAR, paquete, perfil, variante y reporte privado. INFO resume; DEBUG muestra pasos; TRACE aporta diagnóstico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia, o causa no determinada; no registrar secretos ni filas completas.

