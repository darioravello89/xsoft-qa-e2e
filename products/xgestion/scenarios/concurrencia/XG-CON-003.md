---
{"id":"XG-CON-003","title":"Retransmitir una venta tras perder la confirmación de sincronización","product":"xgestion","module":"concurrencia","tags":["xgestion","regression","concurrencia","varios-puestos","sincronizacion","recuperacion"],"status":"planned"}
---

# XG-CON-003 — Retransmitir una venta tras perder la confirmación de sincronización

## Objetivo

Propagar una operación ya realizada aunque se pierda la respuesta del servicio, sin duplicar documentos ni efectos comerciales al reenviarla.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P0.** Ver [continuidad operativa](../../docs/continuidad-operativa.md). Sin Robot, seed ni evidencia del JAR. Sincronización de registros, distinta de repetir el cobro en [FIN-009](../conciliacion/XG-FIN-009.md). No se ejecuta en el laboratorio v1 offline actual; requiere backend QA dedicado, sin producción.

## Precondiciones y datos

- Perfil de protocolo definido antes de ejecutar: V1 para la primera variante, V2 como variante independiente. Backend aislado, puestos P1/P2 y política de red QA aún NO preparados; la documentación no los habilita.
- Venta local V de A × 2 a ARS 1.000, cobrada una vez por ARS 2.000; stock inicial 10/final 8. Identidades de cabecera, renglones, pago y movimiento enlazadas; control ajeno sin cambios.
- Pérdida de respuesta después de aceptación remota y antes de retirar la cola local, reproducible sin modificar datos comerciales a mano. Contrato receptor y lector de ambos extremos pendientes; no deducirlos solo del cliente Java.
- Todos los fixtures mencionados son sintéticos y **NO están creados por esta entrega**. Faltan paquete, controles accesibles, perfiles y lectores por identidad. No escribir SQL comercial durante el recorrido ni debilitar las guardas del runner.

## Pasos y resultados esperados

| Acción del usuario o responsable QA | Resultado esperado |
| --- | --- |
| Comprobar V cerrada localmente y preparada para sincronizar. | Una venta/cobro local y stock 8; la operación no vuelve a cobrarse para generar otro envío. |
| Iniciar sincronización y provocar la pérdida de respuesta en el punto definido. | No declarar completado un envío sin confirmación; registrar estado remoto y pendientes locales conocidos, sin borrar cola manualmente. |
| Restablecer el servicio QA y repetir la sincronización por la UI calibrada. | Criterio a validar con el receptor: existe una sola operación comercial V con las mismas identidades; el reenvío no agrega otro pago ni egreso de stock. |
| Sincronizar P2 y consultar V; repetir otra sincronización sin cambios. | Mismo documento, cantidad 2 e importe ARS 2.000; saldos coherentes con la topología declarada. La segunda consulta/sincronización no crea una venta nueva. |
| Comprobar finalización o pendientes que impiden completar. | El resultado distingue confirmado, pendiente y error. Si el servidor confirma pero la cola local no avanza, no queda un ciclo infinito presentado como éxito. |

## Variantes y dependencias

- Fallo antes de aceptación remota, respuesta perdida posterior y recepción repetida en P2 son puntos distintos.
- V2 debe declarar tablas, claves y contrato propios; no heredar los resultados V1. Sin soporte controlado del receptor, la variante permanece bloqueada.
- Validar por separado ventas, detalle, pagos y stock: contar una sola cabecera no descarta detalle duplicado o un cobro perdido.
- Desconexión de internet con venta local no prueba que todas las operaciones del producto admitan modo offline. No se amplía esa capacidad por esta ficha.

## Evidencia y límites

Correlación e identidades en ambos extremos, cantidades de registros esperadas por entidad, confirmaciones y cambios de cola saneados. Una respuesta HTTP o una cola vacía no sustituyen la conciliación comercial.

Un perfil, procedimiento u oráculo faltante produce BLOQUEADO antes de la acción dependiente. Ningún resultado observado se adopta como esperado para aprobar. INFO resume y explica fallos; DEBUG muestra acciones de negocio; TRACE agrega diagnóstico saneado. Conservar paso, esperado/observado y causa no determinada si no está demostrada.

## Recuperación

Consultar ambos extremos antes de reenviar; usar únicamente el mecanismo de sincronización autorizado. No borrar pendientes, copiar IDs ni reenviar pagos externos. Ante incertidumbre, conservar el laboratorio y detener automatización dependiente.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: commit `daa002d597d0fa7380ace204d3727085c52d1415`. Las rutas siguientes son relativas a XGestion2; las clases/tests describen reglas y riesgos, no ejecuciones E2E.

- `src/Integraciones/Sincronizador/UtilsSincronizador/UtilSincronizadorBackend.java:1113-1175,1338-1369`: envío V1, confirmación y avance de cola.
- `src/Integraciones/Sincronizador/Sincronizacion/Sincronizacion.java:3857-3892`: recepción con upsert; no acredita por sí sola idempotencia de todo el backend.
- `src/Integraciones/Sincronizador/Sincronizacion/SincronizacionBackendV2Registry.java:64-86`: identidades de entidades V2.
- `test/Integraciones/Sincronizador/UtilsSincronizador/UtilSincronizadorBackendQueueTest.java` y `test/Integraciones/Sincronizador/Sincronizacion/SincronizacionVentasCuerpoRecepcionV1Test.java`.

Registrar SHA256/build del JAR, paquete, perfil, ámbito, IDs y reporte privado. No publicar credenciales, configuración completa, copias de bases, payloads, filas completas ni logs crudos.

