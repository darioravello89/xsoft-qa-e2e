---
{"id":"XG-CON-004","title":"Resolver un conflicto de sincronización eligiendo el origen correcto","product":"xgestion","module":"concurrencia","tags":["xgestion","regression","concurrencia","varios-puestos","sincronizacion","recuperacion"],"status":"planned"}
---

# XG-CON-004 — Resolver un conflicto de sincronización eligiendo el origen correcto

## Objetivo

Permitir que un responsable revise una discrepancia local/nube y aplique la versión elegida solo al alcance que confirmó.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P0.** Ver [continuidad operativa](../../docs/continuidad-operativa.md). Sin Robot, seed ni evidencia del JAR. Revisión explícita de conflictos ambiguos V2; distinta de la retransmisión sin cambios de [CON-003](XG-CON-003.md). No presupone que V1 muestre este diálogo ni que exista una política universal «último en guardar gana».

## Precondiciones y datos

- Laboratorio V2 con backend QA aislado, integridad/revisión habilitadas, rol responsable y navegación del diálogo pendientes. No se contacta servicio alguno en esta entrega.
- Producto QA-CON-A con la misma identidad en ambos extremos, precio local ARS 1.000 y nube ARS 1.200, misma fecha efectiva para provocar ambigüedad; producto control B = ARS 500 en ambos. Sin ventas abiertas ni escritores concurrentes durante la resolución básica.
- Preparar otro conflicto en distinto mes/tabla para control de alcance, con datos y permisos explícitos. Las claves técnicas se mantienen iguales en el caso básico; no incluir automáticamente conflictos de ID_ComputadoraModifica.
- Todos los fixtures mencionados son sintéticos y **NO están creados por esta entrega**. Faltan paquete, controles accesibles, perfiles y lectores por identidad. No escribir SQL comercial durante el recorrido ni debilitar las guardas del runner.

## Pasos y resultados esperados

| Acción del usuario o responsable QA | Resultado esperado |
| --- | --- |
| Abrir la revisión de conflictos ambigua y seleccionar A. | Muestra identidad, campo de precio y valores local 1.000/nube 1.200 distinguibles; B no aparece como discrepancia falsa. |
| Cerrar sin aplicar y volver a revisar. | Ambos valores permanecen; consultar/cerrar no elige una versión por el usuario. |
| En un baseline, elegir Usar nube en este registro y esperar la revalidación. | A adopta ARS 1.200 localmente y coincide con nube; B y el conflicto de otro ámbito no cambian. El resultado informa aplicados/omitidos y pendientes. |
| En otro baseline, elegir Usar local en este registro. | A converge a ARS 1.000 en los dos extremos según el contrato del servicio; no duplicar el producto ni extender la selección al mes completo. |
| Preparar resolución por página o tabla/mes y rechazar su confirmación. | No se aplica esa resolución masiva; conserva las discrepancias del alcance rechazado. |

## Variantes y dependencias

- La acción por registro no muestra la misma confirmación masiva en la fuente. Calibrar el control exacto y no afirmar un diálogo adicional inexistente.
- Cambio remoto entre revisión y aplicación requiere contrato de revalidación pendiente antes de probar; no aceptar sobrescritura silenciosa por observar que se produjo.
- Conflictos de claves técnicas pueden ser omitidos por no ser canónicos; no exigir que Usar local/nube siempre los resuelva.
- Interrupción de la resolución y alcance de varios registros necesitan evidencia por cada resultado; no declarar rollback de todo el lote.

## Evidencia y límites

Identidad, diferencias de campos permitidos, elección, alcance, estado final en ambos extremos y controles ajenos. El resultado «aplicado» requiere revalidación; no publicar snapshots completos ni tokens.

Un perfil, procedimiento u oráculo faltante produce BLOQUEADO antes de la acción dependiente. Ningún resultado observado se adopta como esperado para aprobar. INFO resume y explica fallos; DEBUG muestra acciones de negocio; TRACE agrega diagnóstico saneado. Conservar paso, esperado/observado y causa no determinada si no está demostrada.

## Recuperación

Si quedan omitidos o pendientes, conservarlos y detener operaciones dependientes de ese precio hasta resolver su criterio. No repetir masivamente para ocultar el conflicto ni usar SQL; restaurar únicamente el laboratorio QA tras guardar evidencia.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: commit `daa002d597d0fa7380ace204d3727085c52d1415`. Las rutas siguientes son relativas a XGestion2; las clases/tests describen reglas y riesgos, no ejecuciones E2E.

- `src/ModuloPrincipal/Vistas/Dialogs/DialogSyncV2AmbiguousConflicts.java:78-87,354-448`: selección, alcance y confirmación masiva.
- `src/Integraciones/Sincronizador/Sincronizacion/Integridad/SyncV2IntegrityConflictReviewService.java:35-91,94-140`: ambigüedad, prioridades y revalidación.
- `src/Integraciones/Sincronizador/Sincronizacion/SincronizacionBackendV2Registry.java:24`: artículo en el registro V2.
- `test/ModuloPrincipal/Vistas/Dialogs/DialogSyncV2AmbiguousConflictsLayoutTest.java` y `test/Integraciones/Sincronizador/Sincronizacion/SyncV2IntegrityConflictReviewServiceTest.java`.

Registrar SHA256/build del JAR, paquete, perfil, ámbito, IDs y reporte privado. No publicar credenciales, configuración completa, copias de bases, payloads, filas completas ni logs crudos.
