---
{"id":"XG-REM-008","title":"Guardar un borrador y retomarlo antes de confirmar","product":"xgestion","module":"remitos","tags":["xgestion","regression","compras","remitos","remitos-correccion","recuperacion","stock"],"status":"planned"}
---

# XG-REM-008 — Guardar un borrador y retomarlo antes de confirmar

## Objetivo

Guardar un borrador y retomarlo antes de confirmar, desde el trabajo de la persona que recibe mercadería o administra compras.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 6 del roadmap.** Ficha del [mapa de remitos](../../docs/remitos.md). No tiene suite Robot ni validación real. Remito de **compra/recepción**, distinto del remito emitido desde Venta.

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete privado autorizado y baseline recuperable. Ejecución real pendiente.
- Perfil base: ARS, remito de compra local, sin emisión fiscal/impresión; proveedor QA, sin listas, impuestos, bonificaciones ni costo universal salvo variante explícita. Factor de bulto 0 para unidades. Suma stock y Recibido activados; ambas opciones de actualizar precio desactivadas.
- Todos los códigos QA-REM y documentos citados son datos sintéticos **pendientes de seed/baseline**; no están garantizados por `catalogo-comercial-v1`. Preparar identidades y controles de colisiones antes de automatizar; no escribir SQL comercial durante el recorrido.
- A × 2 a $1.000, proveedor A, número QA-R-008, fecha 22/09/2026 y nota Borrador QA; stock A/B 10.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Cargar cabecera/detalle, solicitar salir y elegir Guardar. | Cierra guardando borrador abierto de $2.000, sin recibir stock ni crear cuenta corriente. |
| Reabrir ese borrador por identidad. | Conserva fecha/proveedor/número/nota y línea; stock sigue 10. |
| Agregar B × 1 a $500 y confirmar. | Cierra por $2.500; solo entonces recibe A × 2/B × 1. |
| Consultar nuevamente el documento. | No hay un segundo remito confirmado ni recepción duplicada de A. |

## Variantes y dependencias

Borrador nuevo/existente. Verificar reutilización de remito vacío del mismo contexto sin tomar uno con detalle o de otra PC. Persistencia de borrador no implica recepción.

## Evidencia y recuperación

Contrastar documento, detalle, inventario, costos/listas y cuenta del proveedor según el caso, por identidad y deltas. Un borrador puede persistir: comprobar ausencia de recepción, no ausencia absoluta de filas. Conservar el informe antes de salir por la interfaz y restaurar baseline antes de otra variante. No usar anulación como limpieza equivalente a restaurar precios e historial.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a esa revisión de XGestion2:

- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:233-258`.
- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:1426-1485`.
- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:1498-1524`.

Los tests citados orientan las reglas; no acreditan ejecución E2E. Selectores/atajos y oráculos de compras pendientes de calibrar. Registrar SHA256 del JAR, paquete, perfil, variante y reporte privado. INFO resume; DEBUG muestra pasos; TRACE aporta diagnóstico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia, o causa no determinada; no registrar secretos ni filas completas.

