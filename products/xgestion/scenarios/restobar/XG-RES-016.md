---
{"id":"XG-RES-016","title":"Quitar ingredientes de una receta respetando su límite","product":"xgestion","module":"restobar","tags":["xgestion","regression","restobar","restobar-recetas","restobar-opciones","stock"],"status":"planned"}
---

# XG-RES-016 — Quitar ingredientes de una receta respetando su límite

## Objetivo

Quitar ingredientes de una receta respetando su límite, desde la perspectiva del mozo, cajero o supervisor que opera el pedido.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 5.**
Referencia de planificación: **Recetas**. Ver [mapa de Restobar](../../docs/restobar.md).
No tiene suite Robot, seed automático ni validación real del JAR. Los resultados siguientes son criterios esperados, no resultados obtenidos.

## Precondiciones y datos

- Paquete QA sintético, Windows exclusivo y escritorio visible. La preparación de carta, mesas, ingredientes, permisos y perfiles de este caso está **pendiente**; `catalogo-comercial-v1` no certifica estos datos.
- Perfil local por defecto: ARS, comprobante interno no fiscal, impuestos y cubiertos $0 salvo indicación, sin ofertas, listas ni beneficios adicionales. Las integraciones se habilitan solo en el laboratorio indicado.
- PLATO-REC con queso 0,05 kg por unidad y dos opciones negativas: Sin parte A -0,03 kg y Sin parte B -0,02 kg. Opción Exceso -0,06 kg; precio comercial $1.000 y negativas sin cargo.
- El límite usa la receta del producto y el ingrediente seleccionado; no un máximo genérico.
- Preparar y registrar antes de ejecutar los IDs propios de empresa, sucursal, puesto, cuenta, mesa y productos. Mantener una operación de control ajena al caso para verificar aislamiento.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Elegir Sin parte A y Sin parte B para un plato. | Se permite quitar exactamente 0,05 kg y el plato mantiene precio $1.000. |
| Intentar agregar otra reducción o elegir Exceso desde baseline. | Se avisa que supera la receta; la opción inválida no queda seleccionada ni modifica el pedido. |
| Desmarcar una reducción y volver a elegir una combinación válida. | El acumulado se actualiza y se permite continuar sin retener el rechazo. |
| Cobrar la variante que quita exactamente la receta. | Consumo neto de queso 0; no se crea stock extra ni se reduce dos veces el ingrediente. |

## Variantes y límites

Multiplicador x2 que excede el límite, límite exacto, receta inexistente y cantidad de receta 0; receta moderna tiene prioridad sobre legacy. El stock con cantidad de platos 2 se combina con RES-015.

## Dependencias para automatizar

Preparar el baseline privado reproducible y sus datos, declarar el perfil, calibrar acciones accesibles sobre el SHA256 del JAR y construir comprobaciones por identidad. Utilizar atajos/acciones accesibles verificados; no tomar una posición de pantalla como identidad. Si el control o laboratorio no está disponible, mantener el caso pendiente y explicar el bloqueo.

## Evidencia y límites

Conservar UI y valores esperados/observados de cada transición. En una cuenta abierta distinguir lo guardado de lo cobrado: salir de la pantalla no es abandonar la venta. Registrar por separado **estado de cuenta, ocupación de mesa y estado de cocina** cuando apliquen.

Comparar operaciones, consumos, opciones, importes y efectos de stock/pagos por identidad y deltas según el caso, con lecturas autorizadas y saneadas. Las salidas de cocina, fiscalización y dispositivos requieren evidencia del extremo receptor; un log o test unitario no la sustituye. Registrar versión/SHA256 del JAR, commit del harness, paquete, perfil, IDs y reporte privado.

## Recuperación

Ante una discrepancia conservar primero la evidencia y cancelar o retomar por la interfaz según los pasos del caso. No borrar ni corregir registros comerciales para obtener un resultado aprobado. Restaurar el baseline QA antes de otra variante; para un cierre de resultado ambiguo conciliar la operación antes de reintentar, evitando cobrar o consumir ingredientes dos veces.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas relativas a XGestion2:

- `src/Utilidades/Pickers/FormProductoOpcionesPicker.java`
- `src/ModuloVentas/Entidades/TicketVenta.java`
- `src/ModuloProductos/Entidades/ProductoHijo.java`

La lectura de fuente/tests orienta el riesgo y el criterio; no acredita la ejecución del artefacto. INFO resume, DEBUG describe acciones de negocio y TRACE añade diagnóstico saneado. Un fallo conserva paso, esperado, observado, categoría y evidencia; causa no determinada si falta prueba causal. No registrar credenciales, filas completas ni configuración privada.

