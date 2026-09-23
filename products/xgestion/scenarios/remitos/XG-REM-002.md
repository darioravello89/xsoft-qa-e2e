---
{"id":"XG-REM-002","title":"Buscar productos sin arrastrar una selección cancelada o inexistente","product":"xgestion","module":"remitos","tags":["xgestion","regression","compras","remitos","remitos-carga","productos","recuperacion"],"status":"planned"}
---

# XG-REM-002 — Buscar productos sin arrastrar una selección cancelada o inexistente

## Objetivo

Buscar productos sin arrastrar una selección cancelada o inexistente, desde el trabajo de la persona que recibe mercadería o administra compras.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P1, etapa 6 del roadmap.** Ficha del [mapa de remitos](../../docs/remitos.md). No tiene suite Robot ni validación real. Remito de **compra/recepción**, distinto del remito emitido desde Venta.

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete privado autorizado y baseline recuperable. Ejecución real pendiente.
- Perfil base: ARS, remito de compra local, sin emisión fiscal/impresión; proveedor QA, sin listas, impuestos, bonificaciones ni costo universal salvo variante explícita. Factor de bulto 0 para unidades. Suma stock y Recibido activados; ambas opciones de actualizar precio desactivadas.
- Todos los códigos QA-REM y documentos citados son datos sintéticos **pendientes de seed/baseline**; no están garantizados por `catalogo-comercial-v1`. Preparar identidades y controles de colisiones antes de automatizar; no escribir SQL comercial durante el recorrido.
- A = QA-REM-UNIDAD a $1.000; B = QA-REM-OTRO a $500. Ambos sin bultos. QA-REM-NO-EXISTE es un código ausente. Proveedor A y filtro del picker declarado.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Abrir F1 Ver Productos, elegir A y cargar una unidad. | Grilla con A × 1, total $1.000. |
| Buscar B y cancelar el picker sin aceptar. | B no se agrega y A conserva su cantidad. |
| Ingresar QA-REM-NO-EXISTE por código. | Se informa código inexistente; no reutiliza A/B como producto actual ni cambia el total. |
| Buscar B nuevamente y aceptarlo con cantidad 1/costo $500. | Solo ahora aparece B y el total es $1.500. Salir sin guardar descarta la carga. |

## Variantes y dependencias

Repetir ingreso por código y picker. Alternar proveedor y Ver todos con perfiles preparados, comprobando el filtro declarado; no dar por cubierto el filtro solo por abrir el buscador.

## Evidencia y recuperación

Contrastar documento, detalle, inventario, costos/listas y cuenta del proveedor según el caso, por identidad y deltas. Un borrador puede persistir: comprobar ausencia de recepción, no ausencia absoluta de filas. Conservar el informe antes de salir por la interfaz y restaurar baseline antes de otra variante. No usar anulación como limpieza equivalente a restaurar precios e historial.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a esa revisión de XGestion2:

- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:1139-1254`.
- `test/ModuloStocks/Vistas/FormCargaRemitoFacturaPickerPersistenciaPolicyTest.java:13-51`.

Los tests citados orientan las reglas; no acreditan ejecución E2E. Selectores/atajos y oráculos de compras pendientes de calibrar. Registrar SHA256 del JAR, paquete, perfil, variante y reporte privado. INFO resume; DEBUG muestra pasos; TRACE aporta diagnóstico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia, o causa no determinada; no registrar secretos ni filas completas.

