---
{"id":"XG-REM-019","title":"Revisar IVA por producto al desactivar y reactivar su inclusión","product":"xgestion","module":"remitos","tags":["xgestion","regression","compras","remitos","remitos-costos","precios","comprobantes"],"status":"planned"}
---

# XG-REM-019 — Revisar IVA por producto al desactivar y reactivar su inclusión

## Objetivo

Revisar IVA por producto al desactivar y reactivar su inclusión, desde el trabajo de la persona que recibe mercadería o administra compras.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 6 del roadmap.** Ficha del [mapa de remitos](../../docs/remitos.md). No tiene suite Robot ni validación real. Remito de **compra/recepción**, distinto del remito emitido desde Venta.

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete privado autorizado y baseline recuperable. Ejecución real pendiente.
- Perfil base: ARS, remito de compra local, sin emisión fiscal/impresión; proveedor QA, sin listas, impuestos, bonificaciones ni costo universal salvo variante explícita. Factor de bulto 0 para unidades. Suma stock y Recibido activados; ambas opciones de actualizar precio desactivadas.
- Todos los códigos QA-REM y documentos citados son datos sintéticos **pendientes de seed/baseline**; no están garantizados por `catalogo-comercial-v1`. Preparar identidades y controles de colisiones antes de automatizar; no escribir SQL comercial durante el recorrido.
- Empresa discrimina IVA. A/B/C/D a costo neto $1.000 por unidad, alícuotas 21%/10,5%/27%/0%; una unidad de cada uno. Sin otros impuestos/descuentos. Total $4.585, IVA $585.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Cargar los cuatro productos con IVA habilitado. | IVA por línea $210/$105/$270/$0; costos netos $1.000, total $4.585. |
| Desactivar IVA en remito. | IVA cero, total $4.000; no extrae impuesto del costo ni convierte $1.000 a $826,45. |
| Reactivar IVA y abrir detalle de A. | Recupera importes; A costo $1.000/IVA $210, sin acumulación. |
| Guardar borrador, reabrir y confirmar. | Detalle/resumen/documento conservan base e IVA del perfil. |

## Variantes y dependencias

Exento/no gravado necesitan productos propios y clasificaciones diferentes, aunque ambos sin IVA. Empresa sin discriminación tiene perfil aparte. Agregar redondeo con cantidad/bonificación mediante datos y esperado declarados. Esta ficha no acredita emisión fiscal ni libro IVA.

## Evidencia y recuperación

Contrastar documento, detalle, inventario, costos/listas y cuenta del proveedor según el caso, por identidad y deltas. Un borrador puede persistir: comprobar ausencia de recepción, no ausencia absoluta de filas. Conservar el informe antes de salir por la interfaz y restaurar baseline antes de otra variante. No usar anulación como limpieza equivalente a restaurar precios e historial.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a esa revisión de XGestion2:

- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:957-975`.
- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:2580-2600`.
- `src/ModuloStocks/Vistas/CompraDetalleIvaEdicionPolicy.java:1-143`.
- `test/ModuloStocks/Vistas/CompraDetalleIvaEdicionPolicyTest.java:16-112`.
- `test/ModuloStocks/Vistas/CompraCabeceraFiscalPolicyTest.java:12-76`.

Los tests citados orientan las reglas; no acreditan ejecución E2E. Selectores/atajos y oráculos de compras pendientes de calibrar. Registrar SHA256 del JAR, paquete, perfil, variante y reporte privado. INFO resume; DEBUG muestra pasos; TRACE aporta diagnóstico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia, o causa no determinada; no registrar secretos ni filas completas.

