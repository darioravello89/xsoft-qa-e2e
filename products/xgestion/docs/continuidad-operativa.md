# Continuidad operativa: recuperar, coordinar y actualizar

Este mapa agrega **12 fichas planned**, todas P0: cuatro de recuperación, cuatro de concurrencia/sincronización y cuatro de actualización. Documenta resultados de negocio y requisitos del laboratorio; no agrega Robot, seed, cortes de procesos ni conexiones.

Consultar el [roadmap general](roadmap.md), la [cobertura](cobertura.md) y los [circuitos críticos](circuitos-criticos.md). El grupo `recuperacion` sigue siendo transversal: una prueba de recuperación de Venta no acredita una restauración, una migración o un conflicto entre puestos.

## Recorridos

| ID | Qué debe poder hacer QA | Grupo específico | Estado |
| --- | --- | --- | --- |
| [XG-REC-001](../scenarios/recuperacion/XG-REC-001.md) | Retomar una venta guardada después de interrumpir la interfaz | `recuperacion` | planned |
| [XG-REC-002](../scenarios/recuperacion/XG-REC-002.md) | Reconocer un guardado fallido antes de confirmar el presupuesto | `recuperacion` | planned |
| [XG-REC-003](../scenarios/recuperacion/XG-REC-003.md) | Retomar el cierre de Venta tras un fallo de base anterior al commit | `recuperacion` | planned |
| [XG-REC-004](../scenarios/recuperacion/XG-REC-004.md) | Reconocer una venta ya cobrada cuando se pierde la confirmación visual | `recuperacion` | planned |
| [XG-CON-001](../scenarios/concurrencia/XG-CON-001.md) | Disputar la última unidad desde dos puestos sin ocultar una sobreventa | `concurrencia` | planned |
| [XG-CON-002](../scenarios/concurrencia/XG-CON-002.md) | Reabrir un presupuesto en dos puestos sin perder cambios ni cobrarlo dos veces | `concurrencia` | planned |
| [XG-CON-003](../scenarios/concurrencia/XG-CON-003.md) | Retransmitir una venta tras perder la confirmación de sincronización | `concurrencia` | planned |
| [XG-CON-004](../scenarios/concurrencia/XG-CON-004.md) | Resolver un conflicto de sincronización eligiendo el origen correcto | `concurrencia` | planned |
| [XG-ACT-001](../scenarios/actualizacion/XG-ACT-001.md) | Abrir una versión nueva sobre una copia de la base anterior | `actualizacion` | planned |
| [XG-ACT-002](../scenarios/actualizacion/XG-ACT-002.md) | Reiniciar la versión actual sin repetir efectos de migraciones aplicadas | `actualizacion` | planned |
| [XG-ACT-003](../scenarios/actualizacion/XG-ACT-003.md) | Recuperar una actualización interrumpida sin asumir rollback ni downgrade | `actualizacion` | planned |
| [XG-ACT-004](../scenarios/actualizacion/XG-ACT-004.md) | Conservar documentos y monedas históricas después de actualizar | `actualizacion` | planned |

```powershell
qa.cmd list --product xgestion --group recuperacion
qa.cmd list --product xgestion --group concurrencia
qa.cmd list --product xgestion --group sincronizacion
qa.cmd list --product xgestion --group actualizacion
```

Estas fichas todavía no son ejecutables. Los filtros `varios-puestos`, `ventas`, `stock`, `cobros`, `comprobantes` y `monedas` cruzan los riesgos sin duplicar IDs. El grupo recuperación contiene también fichas anteriores; no interpretar su cantidad como 4 casos totales.

## Diferencias respecto del backlog existente

- [FIN-004](../scenarios/conciliacion/XG-FIN-004.md) recupera un **cobro manual de deuda**. REC-002 prepara un guardado de presupuesto fallido; REC-003 prueba la transacción de cierre de **Venta**.
- [FIN-009](../scenarios/conciliacion/XG-FIN-009.md) prueba confirmación repetida y una variante de cuota concurrente. REC-004 pierde la **confirmación visual tras commit**; CON-001 disputa stock y CON-002 comparte un presupuesto.
- [RES-040](../scenarios/restobar/XG-RES-040.md) conserva cuenta, mesa, ingredientes y pago tras cierre fallido. REC no extrapola ese contrato a Venta ni viceversa.
- [BKP-001](../scenarios/respaldos/XG-BKP-001.md) verifica una exportación y [BKP-002](../scenarios/respaldos/XG-BKP-002.md) exige recuperación exacta en VM descartable. ACT verifica además **compatibilidad del paquete/schema, migraciones y preservación de históricos**.
- [INV-003](../scenarios/inventario/XG-INV-003.md) prueba cierre anual. Reiniciar un JAR actualizado no equivale a repetir una apertura de stock.

## Preparación y orden de avance

| Lote | Preparación pendiente | Aceptación |
| --- | --- | --- |
| REC-001/002 | Presupuesto guardado, controles de consulta, punto de fallo anterior a la primera escritura y conservación del estado entre reinicios. | Recuperar la misma identidad o demostrar ausencia antes de guardar otra vez. |
| REC-003/004 | Oráculo de cabecera/detalle/pago/stock y fallos antes/después del commit, observables desde el JAR. | Efectos completos una sola vez; distinguir rollback comprobado de resultado desconocido. |
| CON-001/002 | Dos puestos propios, topología de base, barreras y política de stock/edición acordadas. | Resultado coherente con esa política, sin confundir dos intenciones legítimas con duplicados. |
| CON-003/004 | Backend QA dedicado, contrato receptor, red aislada y perfiles separados V1/V2. | Convergencia y alcance verificados en los dos extremos; pendientes/omitidos visibles. |
| ACT-001..004 | JAR origen/destino con hash, copia anterior, manifest, registro de migraciones y snapshot recuperable. | Actualización completa, reinicio sin efectos repetidos y recuperación demostrada ante fallo. |

No se asignan fechas. El lote local puede prepararse antes que red/concurrencia. Los códigos, saldos y documentos de las fichas son requisitos de fixtures **NO creados**, y no se presuponen parte del seed comercial actual.

## Contratos que deben quedar explícitos

**Persistencia e interfaz.** Guardar presupuesto tiene una validación de lo persistido, pero no muestra la misma transacción explícita del cobro. Un error de guardado no acredita rollback integral. Una ventana cerrada o un mensaje perdido tampoco acredita que no se guardó. Si no puede saberse qué persistió, detener el reintento y conservar evidencia.

**Estado entre fases.** Las fichas de corte/reinicio necesitan consultar la misma base después del corte. La restauración automática entre fases destruiría esa evidencia. El procedimiento de laboratorio correspondiente está pendiente; no omitir las guardas ni invocar Robot directamente para conseguir continuidad.

**Stock concurrente.** El bloqueo comercial sin stock no demuestra reserva atómica entre dos puestos, y dos bases con sincronización pendiente no equivalen a una base autoritativa compartida. CON-001 requiere acordar el contrato antes de su mutación concurrente. Un perfil que permite stock negativo puede admitir dos ventas; no se cambia el esperado después de observarlo.

**Presupuesto compartido.** Recargar muestra lo persistido, pero no demuestra bloqueo de una pantalla obsoleta. La regla de rechazo/resolución de cambios simultáneos queda pendiente; no inventar refresh automático, exclusión o política de último escritor.

**Sincronización.** V1 y V2 son perfiles distintos. El cliente V1 confirma envío y retira pendientes, y la recepción usa upserts; eso no acredita idempotencia completa del backend. La revisión V2 sí tiene controles de elegir local/nube y alcances registro/página/tabla-mes. La confirmación masiva no se presume presente para un registro individual. Conflictos técnicos pueden quedar omitidos.

Los casos CON-003/004 **requieren una política de laboratorio de red propia, aún pendiente**. El entorno inicial continúa offline; documentar un caso no habilita nube, producción ni sincronización sin conectividad.

**Migraciones.** El arranque puede omitir trabajo o usar PENDING_ONLY; este modo omite APPLIED. FULL puede revisitar pasos aplicados. ACT-002 exige ausencia de efectos comerciales repetidos y evalúa los contadores según el modo: no promete que toda verificación deje todos los metadatos idénticos.

**Recuperación de versión.** Un fallo de DDL puede dejar cambios parciales. Reponer un JAR antiguo no restaura schema, configuración y datos, y no se presume downgrade compatible. ACT-003 necesita reintento compatible o snapshot completo demostrado. Importar .xbd mediante upserts no sustituye ese procedimiento.

## Criterios de evidencia

Por fase, conservar instante, identidad/contexto, estado visible y deltas de documento, pago, deuda y stock. En sincronización, contrastar los dos extremos; en actualización, registrar versiones/hashes y manifest semántico antes/después. No basta un número total: los errores de entidades distintas pueden compensarse.

Los históricos mantienen importes/monedas/relaciones según su contrato; los cambios técnicos autorizados de schema o fotografía legacy no se rechazan por ser diferentes byte a byte. Un presupuesto editable conserva sus reglas propias y no se trata como histórico cerrado.

INFO resume y explica fallos; DEBUG describe acciones; TRACE añade solo diagnóstico saneado. Resultado incierto, laboratorio ausente u oráculo pendiente implica bloqueo de las acciones dependientes, nunca aprobación. Ninguna prueba del framework, test de texto o JDBC simulado sustituye la ejecución del JAR.

## Fuente y mantenimiento

Fuente inspeccionada: XGestion2, commit **`daa002d597d0fa7380ace204d3727085c52d1415`**. Se preservan las referencias históricas de otras fichas a versiones anteriores; no se actualizan por analogía. Para `AppXGestion.java` se leyó el contenido de ese commit mediante `git show`, ya que su checkout tenía cambios concurrentes.

Las fichas citan rangos y tests concretos de FormVenta/TicketVenta, DatabaseMigrationRunner/DBVerifyScheduler, envío/recepción y resolución de conflictos V2. Esas fuentes orientan contratos y riesgos; no prueban una ejecución real ni el receptor de red.

Al automatizar, mantener los IDs, definir datos/perfil y oráculos, calibrar controles, actualizar estado/Robot y regenerar cobertura. Si una variante conserva un contrato pendiente, declarar ese alcance sin acreditar la ficha completa. No publicar paquetes privados, copias, credenciales ni payloads.

