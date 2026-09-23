---
{"id":"XG-RES-014","title":"Descontar los ingredientes de una receta según los platos cobrados","product":"xgestion","module":"restobar","tags":["xgestion","regression","restobar","restobar-recetas","stock","cobros"],"status":"planned"}
---

# XG-RES-014 — Descontar los ingredientes de una receta según los platos cobrados

## Objetivo

Descontar los ingredientes de una receta según los platos cobrados, desde la perspectiva del mozo, cajero o supervisor que opera el pedido.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 5.**
Referencia de planificación: **Recetas**. Ver [mapa de Restobar](../../docs/restobar.md).
No tiene suite Robot, seed automático ni validación real del JAR. Los resultados siguientes son criterios esperados, no resultados obtenidos.

## Precondiciones y datos

- Paquete QA sintético, Windows exclusivo y escritorio visible. La preparación de carta, mesas, ingredientes, permisos y perfiles de este caso está **pendiente**; `catalogo-comercial-v1` no certifica estos datos.
- Perfil local por defecto: ARS, comprobante interno no fiscal, impuestos y cubiertos $0 salvo indicación, sin ofertas, listas ni beneficios adicionales. Las integraciones se habilitan solo en el laboratorio indicado.
- Receta actual de QA-PLATO-REC a $1.000: harina 0,20 kg y queso 0,05 kg por plato; 10 kg iniciales de cada ingrediente, padre no stockeable, hijos stockeables. Sin extras.
- Seed de recetas y oráculo de ingredientes pendientes; no usar catálogo de ofertas como sustituto.
- Preparar y registrar antes de ejecutar los IDs propios de empresa, sucursal, puesto, cuenta, mesa y productos. Mantener una operación de control ajena al caso para verificar aislamiento.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Cargar dos platos, corregir a 3 y volver a 2. | Precio total final $2.000; la receta no modifica el número de platos ni el precio comercial. |
| Salir, reabrir y cancelar el cobro. | La cuenta sigue abierta por $2.000; no se duplica consumo de ingredientes por consultar o cancelar. |
| Cobrar los dos platos una sola vez. | Consumo final: harina 0,40 kg y queso 0,10 kg; existencias 9,60 y 9,90 kg, respectivamente. |
| Reabrir el comprobante cerrado. | El stock permanece igual al posterior al cobro; no vuelve a consumirse la receta. |

## Variantes y límites

Cantidad 1 y fracción admitida; ingrediente inactivo excluido del perfil; padre stockeable en perfil separado con su propio movimiento esperado. Capturar cuándo cambia stock en el perfil y exigir el delta final, sin sumar reservas dos veces.

## Dependencias para automatizar

Preparar el baseline privado reproducible y sus datos, declarar el perfil, calibrar acciones accesibles sobre el SHA256 del JAR y construir comprobaciones por identidad. Utilizar atajos/acciones accesibles verificados; no tomar una posición de pantalla como identidad. Si el control o laboratorio no está disponible, mantener el caso pendiente y explicar el bloqueo.

## Evidencia y límites

Conservar UI y valores esperados/observados de cada transición. En una cuenta abierta distinguir lo guardado de lo cobrado: salir de la pantalla no es abandonar la venta. Registrar por separado **estado de cuenta, ocupación de mesa y estado de cocina** cuando apliquen.

Comparar operaciones, consumos, opciones, importes y efectos de stock/pagos por identidad y deltas según el caso, con lecturas autorizadas y saneadas. Las salidas de cocina, fiscalización y dispositivos requieren evidencia del extremo receptor; un log o test unitario no la sustituye. Registrar versión/SHA256 del JAR, commit del harness, paquete, perfil, IDs y reporte privado.

## Recuperación

Ante una discrepancia conservar primero la evidencia y cancelar o retomar por la interfaz según los pasos del caso. No borrar ni corregir registros comerciales para obtener un resultado aprobado. Restaurar el baseline QA antes de otra variante; para un cierre de resultado ambiguo conciliar la operación antes de reintentar, evitando cobrar o consumir ingredientes dos veces.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas relativas a XGestion2:

- `src/ModuloRestobar/Vistas/formTicket.java`
- `src/ModuloVentas/Entidades/TicketVenta.java`
- `src/ModuloProductos/Entidades/ProductoHijo.java`

La lectura de fuente/tests orienta el riesgo y el criterio; no acredita la ejecución del artefacto. INFO resume, DEBUG describe acciones de negocio y TRACE añade diagnóstico saneado. Un fallo conserva paso, esperado, observado, categoría y evidencia; causa no determinada si falta prueba causal. No registrar credenciales, filas completas ni configuración privada.

