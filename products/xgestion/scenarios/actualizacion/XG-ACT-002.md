---
{"id":"XG-ACT-002","title":"Reiniciar la versión actual sin repetir efectos de migraciones aplicadas","product":"xgestion","module":"actualizacion","tags":["xgestion","regression","actualizacion","recuperacion"],"status":"planned"}
---

# XG-ACT-002 — Reiniciar la versión actual sin repetir efectos de migraciones aplicadas

## Objetivo

Volver a abrir el sistema actualizado conservando datos y saldos, sin ejecutar de nuevo cambios pendientes ya completados.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P0.** Ver [continuidad operativa](../../docs/continuidad-operativa.md). Sin Robot, seed ni evidencia del JAR. Reinicio e idempotencia del mismo paquete, posterior a [ACT-001](XG-ACT-001.md). No confundir verificación de schema con repetir una venta o el cierre anual de [INV-003](../inventario/XG-INV-003.md).

## Precondiciones y datos

- Snapshot QA con V1 ya actualizada y manifest comprobado; misma huella del FAT JAR, configuración y versión. Sin migraciones pendientes, estado fallido ni schema drift preparado.
- A stock 9, histórico H de ARS 2.000 y venta nueva N de ARS 1.000; cliente 600/proveedor 400, como final de ACT-001. Sin escritores, nube, fiscal o impresión.
- Perfil de arranque normal que puede omitir verificación o ejecutar PENDING_ONLY. Identificar la decisión real del scheduler antes de evaluar intentos; FULL manual es una variante distinta.
- Todos los fixtures mencionados son sintéticos y **NO están creados por esta entrega**. Faltan paquete, controles accesibles, perfiles y lectores por identidad. No escribir SQL comercial durante el recorrido ni debilitar las guardas del runner.

## Pasos y resultados esperados

| Acción del usuario o responsable QA | Resultado esperado |
| --- | --- |
| Registrar el estado completo de V1 y sus operaciones antes de cerrar. | Migraciones requeridas completas y manifest comercial definido; ninguna operación por confirmar. |
| Cerrar y abrir de nuevo el mismo JAR dos veces según el procedimiento QA. | Saldos, documentos y cantidades no cambian por reiniciar; no hay filas comerciales nuevas atribuidas al arranque. |
| Comprobar la decisión de verificación en cada arranque. | En PENDING_ONLY se omiten migraciones APPLIED; si el scheduler omite trabajo, no inventar una nueva ejecución. No aparece un intento nuevo de una migración aplicada por esa ruta. |
| Consultar H y N y abrir/cancelar una venta vacía. | Históricos disponibles y operación normal; stock 9, deudas 600/400, sin nuevo cobro. |
| En otra copia, ejecutar la variante FULL autorizada y revalidar el manifest. | FULL puede revisar nuevamente pasos ya aplicados: exigir ausencia de efectos comerciales repetidos y resultado coherente, no contador de intentos invariable. |

## Variantes y dependencias

- Una migración nueva en otro JAR debe ejecutarse aunque existan anteriores APPLIED; no confundir esa actualización con reinicio.
- Checksum de migración aplicada discrepante: preparar otra copia y una verificación FULL autorizada/calibrada que inicialice el registro; esa ejecución debe informar estado inválido/error. Un arranque que legítimamente omite la verificación no ejecuta la comprobación de checksum y no tiene este esperado.
- Si otra verificación conserva el lock, estado ocupado no acredita completado. Segundo proceso solo en laboratorio de concurrencia, sin abrirlo sobre una base habitual.

## Evidencia y límites

Huella/versión y modo de verificación, estados/intent counts antes/después según la ruta, más manifest de documentos/saldos. Los logs de un chequeo pueden cambiar legítimamente; no tratarlos como duplicación comercial.

Un perfil, procedimiento u oráculo faltante produce BLOQUEADO antes de la acción dependiente. Ningún resultado observado se adopta como esperado para aprobar. INFO resume y explica fallos; DEBUG muestra acciones de negocio; TRACE agrega diagnóstico saneado. Conservar paso, esperado/observado y causa no determinada si no está demostrada.

## Recuperación

Si se repiten efectos, detener nuevas operaciones y conservar el estado. No editar el registro de migraciones ni borrar intentos; restaurar el snapshot íntegro del laboratorio y diagnosticar la decisión de ejecución.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: commit `daa002d597d0fa7380ace204d3727085c52d1415`. Las rutas siguientes son relativas a XGestion2; las clases/tests describen reglas y riesgos, no ejecuciones E2E.

- `src/ModuloPrincipal/Entidades/DatabaseMigrationRunner.java:152-223`: lock, checksum y omisión de APPLIED solo en PENDING_ONLY.
- `src/ModuloPrincipal/Entidades/DBVerifyScheduler.java:101-150,153-188`: huellas, decisión y verificación.
- `src/ModuloPrincipal/Entidades/VerificadorDeBaseDeDatos.java:215-232`: guarda previa y modos de ejecución.
- `test/ModuloPrincipal/Entidades/DatabaseMigrationRunnerTest.java` y `VerificadorDeBaseDeDatosArranqueTest.java`: reintentos/guardas; no acreditan el JAR.

Registrar SHA256/build del JAR, paquete, perfil, ámbito, IDs y reporte privado. No publicar credenciales, configuración completa, copias de bases, payloads, filas completas ni logs crudos.
