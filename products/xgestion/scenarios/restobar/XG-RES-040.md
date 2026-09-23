---
{"id":"XG-RES-040","title":"Recuperar un cierre fallido conservando cuenta, ingredientes y pago","product":"xgestion","module":"restobar","tags":["xgestion","regression","restobar","recuperacion","cobros","restobar-recetas","stock"],"status":"planned"}
---

# XG-RES-040 — Recuperar un cierre fallido conservando cuenta, ingredientes y pago

## Objetivo

Recuperar un cierre fallido conservando cuenta, ingredientes y pago, desde la perspectiva del mozo, cajero o supervisor que opera el pedido.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 5.**
Referencia de planificación: **Recuperación**. Ver [mapa de Restobar](../../docs/restobar.md).
No tiene suite Robot, seed automático ni validación real del JAR. Los resultados siguientes son criterios esperados, no resultados obtenidos.

## Precondiciones y datos

- Paquete QA sintético, Windows exclusivo y escritorio visible. La preparación de carta, mesas, ingredientes, permisos y perfiles de este caso está **pendiente**; `catalogo-comercial-v1` no certifica estos datos.
- Perfil local por defecto: ARS, comprobante interno no fiscal, impuestos y cubiertos $0 salvo indicación, sin ofertas, listas ni beneficios adicionales. Las integraciones se habilitan solo en el laboratorio indicado.
- Cuenta $2.000 con receta y extras identificados, caja inicial y stock registrados. Laboratorio capaz de provocar fallo transaccional de persistencia sin modificar lógica ni conectar producción.
- Inyección de fallos y oráculo transaccional pendientes; no matar procesos ajenos ni relajar aislamiento.
- Preparar y registrar antes de ejecutar los IDs propios de empresa, sucursal, puesto, cuenta, mesa y productos. Mantener una operación de control ajena al caso para verificar aislamiento.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Intentar confirmar el cobro mientras se produce el fallo controlado. | Se informa el fallo o bloqueo; no se presenta un cierre completo sin evidencia. |
| Consultar cuenta, mesa, pago y existencias. | No queda cierre parcial: la cuenta puede retomarse y no hay ingredientes/pago definitivos duplicados. |
| Restablecer el recurso y retomar la operación por UI. | Se muestra el estado comprobado; no se corrige la base para fabricar continuidad. |
| Confirmar una vez y consultar nuevamente. | Una venta cerrada, un efecto financiero y los ingredientes exactos del pedido; mesa consistente con el cierre. |

## Variantes y límites

Timeout, error antes/después de confirmar y pérdida de evidencia. Resultado ambiguo requiere conciliar identidad de operación antes de reintentar; evidencia incompleta se informa como bloqueo, nunca OK.

## Dependencias para automatizar

Preparar el baseline privado reproducible y sus datos, declarar el perfil, calibrar acciones accesibles sobre el SHA256 del JAR y construir comprobaciones por identidad. Utilizar atajos/acciones accesibles verificados; no tomar una posición de pantalla como identidad. Si el control o laboratorio no está disponible, mantener el caso pendiente y explicar el bloqueo.

## Evidencia y límites

Conservar UI y valores esperados/observados de cada transición. En una cuenta abierta distinguir lo guardado de lo cobrado: salir de la pantalla no es abandonar la venta. Registrar por separado **estado de cuenta, ocupación de mesa y estado de cocina** cuando apliquen.

Comparar operaciones, consumos, opciones, importes y efectos de stock/pagos por identidad y deltas según el caso, con lecturas autorizadas y saneadas. Las salidas de cocina, fiscalización y dispositivos requieren evidencia del extremo receptor; un log o test unitario no la sustituye. Registrar versión/SHA256 del JAR, commit del harness, paquete, perfil, IDs y reporte privado.

## Recuperación

Ante una discrepancia conservar primero la evidencia y cancelar o retomar por la interfaz según los pasos del caso. No borrar ni corregir registros comerciales para obtener un resultado aprobado. Restaurar el baseline QA antes de otra variante; para un cierre de resultado ambiguo conciliar la operación antes de reintentar, evitando cobrar o consumir ingredientes dos veces.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas relativas a XGestion2:

- `src/ModuloVentas/Entidades/TicketVenta.java`
- `src/ModuloRestobar/Vistas/formTicket.java`
- `test/ModuloVentas/Entidades/TicketVentaRollbackMonedaTest.java`

La lectura de fuente/tests orienta el riesgo y el criterio; no acredita la ejecución del artefacto. INFO resume, DEBUG describe acciones de negocio y TRACE añade diagnóstico saneado. Un fallo conserva paso, esperado, observado, categoría y evidencia; causa no determinada si falta prueba causal. No registrar credenciales, filas completas ni configuración privada.

