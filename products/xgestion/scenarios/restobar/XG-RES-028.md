---
{"id":"XG-RES-028","title":"Cobrar la mesa y abrir otra cuenta sin arrastrar consumos","product":"xgestion","module":"restobar","tags":["xgestion","regression","restobar","mesas","cobros"],"status":"planned"}
---

# XG-RES-028 — Cobrar la mesa y abrir otra cuenta sin arrastrar consumos

## Objetivo

Cobrar la mesa y abrir otra cuenta sin arrastrar consumos, desde la perspectiva del mozo, cajero o supervisor que opera el pedido.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 5.**
Referencia de planificación: **R13**. Ver [mapa de Restobar](../../docs/restobar.md).
No tiene suite Robot, seed automático ni validación real del JAR. Los resultados siguientes son criterios esperados, no resultados obtenidos.

## Precondiciones y datos

- Paquete QA sintético, Windows exclusivo y escritorio visible. La preparación de carta, mesas, ingredientes, permisos y perfiles de este caso está **pendiente**; `catalogo-comercial-v1` no certifica estos datos.
- Perfil local por defecto: ARS, comprobante interno no fiscal, impuestos y cubiertos $0 salvo indicación, sin ofertas, listas ni beneficios adicionales. Las integraciones se habilitan solo en el laboratorio indicado.
- Mesa A con plato $1.000 y bebida $500; mesa B con pedido de control; efectivo exacto.
- Estados de cuenta, mesa y cocina se registran de manera independiente.
- Preparar y registrar antes de ejecutar los IDs propios de empresa, sucursal, puesto, cuenta, mesa y productos. Mantener una operación de control ajena al caso para verificar aislamiento.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Revisar importe y confirmar el cobro de A por $1.500. | La cuenta de A queda cerrada y el pago identificado una sola vez. |
| Volver al salón. | A está libre, B continúa ocupada y conserva su cuenta. |
| Abrir nuevamente A y cargar una bebida. | Nueva cuenta abierta por $500, con identidad distinta y sin saldo ni opciones del pedido cerrado. |
| Consultar el comprobante anterior. | Conserva consumos, importe y pago originales; no cambia al operar la cuenta nueva. |

## Variantes y límites

Con/sin diálogo de cobro en perfiles separados; con cubiertos y con notas. Pago múltiple o fiscal requieren sus propios datos y laboratorio.

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
- `test/ModuloRestobar/Vistas/FormTicketMesaLifecyclePolicyTest.java`

La lectura de fuente/tests orienta el riesgo y el criterio; no acredita la ejecución del artefacto. INFO resume, DEBUG describe acciones de negocio y TRACE añade diagnóstico saneado. Un fallo conserva paso, esperado, observado, categoría y evidencia; causa no determinada si falta prueba causal. No registrar credenciales, filas completas ni configuración privada.

