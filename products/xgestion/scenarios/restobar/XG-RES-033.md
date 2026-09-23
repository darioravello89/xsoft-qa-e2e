---
{"id":"XG-RES-033","title":"Recibir una ronda de mozo y tolerar retransmisión","product":"xgestion","module":"restobar","tags":["xgestion","regression","restobar","mozos-qr","mesas","preparacion","varios-puestos"],"status":"planned"}
---

# XG-RES-033 — Recibir una ronda de mozo y tolerar retransmisión

## Objetivo

Recibir una ronda de mozo y tolerar retransmisión, desde la perspectiva del mozo, cajero o supervisor que opera el pedido.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 5 con dependencia de laboratorio de etapa 6.**
Referencia de planificación: **R18**. Ver [mapa de Restobar](../../docs/restobar.md).
No tiene suite Robot, seed automático ni validación real del JAR. Los resultados siguientes son criterios esperados, no resultados obtenidos.

## Precondiciones y datos

- Paquete QA sintético, Windows exclusivo y escritorio visible. La preparación de carta, mesas, ingredientes, permisos y perfiles de este caso está **pendiente**; `catalogo-comercial-v1` no certifica estos datos.
- Perfil local por defecto: ARS, comprobante interno no fiscal, impuestos y cubiertos $0 salvo indicación, sin ofertas, listas ni beneficios adicionales. Las integraciones se habilitan solo en el laboratorio indicado.
- Canal mozo QA habilitado, mesa con cuenta abierta, ronda identificada de un plato con opciones y bebida; usuario mozo autorizado.
- Red y canal de pruebas aislados, fuera de la VM offline inicial.
- Preparar y registrar antes de ejecutar los IDs propios de empresa, sucursal, puesto, cuenta, mesa y productos. Mantener una operación de control ajena al caso para verificar aislamiento.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Enviar la ronda desde el canal y recibirla en XGestión. | Aparecen los dos consumos, personalizaciones y responsable en la cuenta correcta. |
| Retransmitir la misma ronda con su identidad original. | Se mantiene un solo conjunto de consumos; no se suman nuevamente importes. |
| Enviar una segunda ronda con nueva identidad. | Solo la segunda agrega consumos adicionales a la misma cuenta abierta. |
| Retomar la mesa y consultar cocina. | Cuenta y cocina conservan identidades de ronda y cantidades esperadas sin duplicación. |

## Variantes y límites

Respuesta perdida tras aceptación, canal desconectado y reenvío; misma mesa distinta cuenta ya cerrada requiere proteger el nuevo contexto. No asumir que XMozo Angular y Mozos Flutter son el mismo canal.

## Dependencias para automatizar

Preparar el baseline privado reproducible y sus datos, declarar el perfil, calibrar acciones accesibles sobre el SHA256 del JAR y construir comprobaciones por identidad. Utilizar atajos/acciones accesibles verificados; no tomar una posición de pantalla como identidad. Si el control o laboratorio no está disponible, mantener el caso pendiente y explicar el bloqueo.

## Evidencia y límites

Conservar UI y valores esperados/observados de cada transición. En una cuenta abierta distinguir lo guardado de lo cobrado: salir de la pantalla no es abandonar la venta. Registrar por separado **estado de cuenta, ocupación de mesa y estado de cocina** cuando apliquen.

Comparar operaciones, consumos, opciones, importes y efectos de stock/pagos por identidad y deltas según el caso, con lecturas autorizadas y saneadas. Las salidas de cocina, fiscalización y dispositivos requieren evidencia del extremo receptor; un log o test unitario no la sustituye. Registrar versión/SHA256 del JAR, commit del harness, paquete, perfil, IDs y reporte privado.

## Recuperación

Ante una discrepancia conservar primero la evidencia y cancelar o retomar por la interfaz según los pasos del caso. No borrar ni corregir registros comerciales para obtener un resultado aprobado. Restaurar el baseline QA antes de otra variante; para un cierre de resultado ambiguo conciliar la operación antes de reintentar, evitando cobrar o consumir ingredientes dos veces.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas relativas a XGestion2:

- `src/ModuloRestobar/AppMozo/AppMozoRoundProcessor.java`
- `test/ModuloRestobar/AppMozo/MesaCierreProteccionTest.java`

La lectura de fuente/tests orienta el riesgo y el criterio; no acredita la ejecución del artefacto. INFO resume, DEBUG describe acciones de negocio y TRACE añade diagnóstico saneado. Un fallo conserva paso, esperado, observado, categoría y evidencia; causa no determinada si falta prueba causal. No registrar credenciales, filas completas ni configuración privada.

