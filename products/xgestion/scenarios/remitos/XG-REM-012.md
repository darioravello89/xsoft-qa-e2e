---
{"id":"XG-REM-012","title":"Advertir un comprobante repetido sin bloquear la carga","product":"xgestion","module":"remitos","tags":["xgestion","regression","compras","remitos","remitos-carga","comprobantes"],"status":"planned"}
---

# XG-REM-012 — Advertir un comprobante repetido sin bloquear la carga

## Objetivo

Advertir un comprobante repetido sin bloquear la carga, desde el trabajo de la persona que recibe mercadería o administra compras.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P1, etapa 6 del roadmap.** Ficha del [mapa de remitos](../../docs/remitos.md). No tiene suite Robot ni validación real. Remito de **compra/recepción**, distinto del remito emitido desde Venta.

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete privado autorizado y baseline recuperable. Ejecución real pendiente.
- Perfil base: ARS, remito de compra local, sin emisión fiscal/impresión; proveedor QA, sin listas, impuestos, bonificaciones ni costo universal salvo variante explícita. Factor de bulto 0 para unidades. Suma stock y Recibido activados; ambas opciones de actualizar precio desactivadas.
- Todos los códigos QA-REM y documentos citados son datos sintéticos **pendientes de seed/baseline**; no están garantizados por `catalogo-comercial-v1`. Preparar identidades y controles de colisiones antes de automatizar; no escribir SQL comercial durante el recorrido.
- Advertencia de duplicado ON. Documento activo QA-DUP-012 del proveedor A. Nuevo remito del proveedor B con mismo número, A × 1 a $1.000. Perfil adicional con advertencia OFF.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Escribir QA-DUP-012 y salir del campo. | Advierte que ya existe en la empresa y puede ser de otro proveedor; permite continuar. |
| Corregir a QA-NUEVO-012 antes de terminar otra consulta pendiente. | No presenta una respuesta anterior como aviso del número nuevo. |
| Volver al duplicado, cargar A × 1 y confirmar conscientemente. | Permite cerrar segundo documento por $1.000 sin sobrescribir el existente. |
| Consultar ambos documentos. | Cada identidad conserva proveedor/fecha/detalle. |

## Variantes y dependencias

Mismo/otro proveedor; espacios exteriores; sin coincidencia; excluir documento actual al editar; OFF sin aviso. Documentos anulados/inactivos no sirven como control positivo de duplicado.

## Evidencia y recuperación

Contrastar documento, detalle, inventario, costos/listas y cuenta del proveedor según el caso, por identidad y deltas. Un borrador puede persistir: comprobar ausencia de recepción, no ausencia absoluta de filas. Conservar el informe antes de salir por la interfaz y restaurar baseline antes de otra variante. No usar anulación como limpieza equivalente a restaurar precios e historial.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a esa revisión de XGestion2:

- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:1364-1419`.
- `src/ModuloProductos/Entidades/Compra.java:141-181`.
- `test/ModuloProductos/Entidades/CompraComprobanteDuplicadoTest.java:16-78`.

Los tests citados orientan las reglas; no acreditan ejecución E2E. Selectores/atajos y oráculos de compras pendientes de calibrar. Registrar SHA256 del JAR, paquete, perfil, variante y reporte privado. INFO resume; DEBUG muestra pasos; TRACE aporta diagnóstico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia, o causa no determinada; no registrar secretos ni filas completas.

