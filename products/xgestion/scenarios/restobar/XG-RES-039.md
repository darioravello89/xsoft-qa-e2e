---
{"id":"XG-RES-039","title":"Seguir estados de cocina sin confundirlos con mesa y cobro","product":"xgestion","module":"restobar","tags":["xgestion","regression","restobar","kds","preparacion","mesas"],"status":"planned"}
---

# XG-RES-039 — Seguir estados de cocina sin confundirlos con mesa y cobro

## Objetivo

Seguir estados de cocina sin confundirlos con mesa y cobro, desde la perspectiva del mozo, cajero o supervisor que opera el pedido.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P1; etapa 5.**
Referencia de planificación: **Cocina**. Ver [mapa de Restobar](../../docs/restobar.md).
No tiene suite Robot, seed automático ni validación real del JAR. Los resultados siguientes son criterios esperados, no resultados obtenidos.

## Precondiciones y datos

- Paquete QA sintético, Windows exclusivo y escritorio visible. La preparación de carta, mesas, ingredientes, permisos y perfiles de este caso está **pendiente**; `catalogo-comercial-v1` no certifica estos datos.
- Perfil local por defecto: ARS, comprobante interno no fiscal, impuestos y cubiertos $0 salvo indicación, sin ofertas, listas ni beneficios adicionales. Las integraciones se habilitan solo en el laboratorio indicado.
- Pedido recibido en KDS QA con cuenta abierta y mesa ocupada; roles caja/cocina, estados habilitados y transiciones del perfil identificados.
- Receptor real de QA necesario; tests de estados aislados no acreditan sincronización.
- Preparar y registrar antes de ejecutar los IDs propios de empresa, sucursal, puesto, cuenta, mesa y productos. Mantener una operación de control ajena al caso para verificar aislamiento.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Consultar el pedido antes de preparar. | Se distinguen cuenta abierta, mesa ocupada y preparación pendiente. |
| Avanzar preparación con el operador de cocina. | Cambia el estado de cocina esperado; no se cobra ni libera la mesa por ese cambio. |
| Volver a consultar desde caja y cocina. | Ambos ven la misma preparación del pedido y sus consumos. |
| Cobrar en caja y refrescar ambos extremos. | La cuenta y mesa reflejan el cierre; el estado de cocina sigue la política específica, sin inventar que cobrar equivale a entregar. |

## Variantes y límites

Rol sin permiso, transición no permitida, reapertura/entrega según política; usar nombres de estados calibrados, no números de enum como pasos del QA.

## Dependencias para automatizar

Preparar el baseline privado reproducible y sus datos, declarar el perfil, calibrar acciones accesibles sobre el SHA256 del JAR y construir comprobaciones por identidad. Utilizar atajos/acciones accesibles verificados; no tomar una posición de pantalla como identidad. Si el control o laboratorio no está disponible, mantener el caso pendiente y explicar el bloqueo.

## Evidencia y límites

Conservar UI y valores esperados/observados de cada transición. En una cuenta abierta distinguir lo guardado de lo cobrado: salir de la pantalla no es abandonar la venta. Registrar por separado **estado de cuenta, ocupación de mesa y estado de cocina** cuando apliquen.

Comparar operaciones, consumos, opciones, importes y efectos de stock/pagos por identidad y deltas según el caso, con lecturas autorizadas y saneadas. Las salidas de cocina, fiscalización y dispositivos requieren evidencia del extremo receptor; un log o test unitario no la sustituye. Registrar versión/SHA256 del JAR, commit del harness, paquete, perfil, IDs y reporte privado.

## Recuperación

Ante una discrepancia conservar primero la evidencia y cancelar o retomar por la interfaz según los pasos del caso. No borrar ni corregir registros comerciales para obtener un resultado aprobado. Restaurar el baseline QA antes de otra variante; para un cierre de resultado ambiguo conciliar la operación antes de reintentar, evitando cobrar o consumir ingredientes dos veces.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas relativas a XGestion2:

- `src/ModuloRestobar/Entidades/KDSEstado.java`
- `src/ModuloRestobar/Entidades/KDSReglas.java`
- `test/ModuloRestobar/Entidades/KDSReglasTest.java`
- `test/ModuloRestobar/Entidades/KDSServiceTest.java`

La lectura de fuente/tests orienta el riesgo y el criterio; no acredita la ejecución del artefacto. INFO resume, DEBUG describe acciones de negocio y TRACE añade diagnóstico saneado. Un fallo conserva paso, esperado, observado, categoría y evidencia; causa no determinada si falta prueba causal. No registrar credenciales, filas completas ni configuración privada.

