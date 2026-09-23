# Complemento de cobertura crítica

Este mapa agrega **50 fichas pendientes de automatización** a los circuitos ya
documentados. El catálogo queda en **298 fichas: 96 implementadas y 202 pendientes**.
No hay nueva automatización ni validación del JAR en esta entrega.

## Baterías y selección

| Circuito | IDs nuevos | Grupo para QA | Mapa y requisitos |
| --- | --- | --- | --- |
| Cobros combinados y monedas | COB-001..008 (8) | `cobros-combinados` | [Cobros y documentos](cobros-documentos.md) |
| Presupuesto y preventa hasta la venta | PRE-001..006 (6) | `presupuestos` | [Cobros y documentos](cobros-documentos.md) |
| Devoluciones y anulaciones | DEV-001..006 (6) | `devoluciones` | [Cobros y documentos](cobros-documentos.md); nota de crédito fiscal en FEL-006 |
| Facturación electrónica | FEL-001..006 (6) | `fiscal` | [Facturación y pagos externos](facturacion-pagos-externos.md) |
| Confirmación de pagos externos | PEX-001..006 (6) | `pagos-externos` | [Facturación y pagos externos](facturacion-pagos-externos.md) |
| Operación interrumpida | REC-001..004 (4) | `recuperacion` | [Continuidad operativa](continuidad-operativa.md) |
| Varios puestos y sincronización | CON-001..004 (4) | `concurrencia`, `sincronizacion` | [Continuidad operativa](continuidad-operativa.md) |
| Actualización de versión | ACT-001..004 (4) | `actualizacion` | [Continuidad operativa](continuidad-operativa.md) |
| Descuentos, impuestos y puntos | BEN-001..006 (6) | `beneficios`, `impuestos`, `fidelizacion` | [Beneficios e impuestos](beneficios-impuestos.md) |

Los grupos pueden incluir fichas anteriores: son filtros, no denominadores
adicionales. Las variantes son parte de la ficha; no suman casos. Consultar el
[Excel de cobertura](../../../docs/coverage/xgestion-cobertura.xlsx) y la
[matriz funcional](cobertura.md). En Excel, filtrar Automatización por Pendiente
y Grupos para QA por el nombre o ID del grupo; abrir el enlace a la ficha.
La prioridad del Excel se hereda de la etapa; la ficha declara el riesgo concreto.

```text
qa.cmd list --product xgestion --groups
qa.cmd list --product xgestion --group cobros-combinados
qa.cmd list --product xgestion --group presupuestos
qa.cmd list --product xgestion --group devoluciones
qa.cmd list --product xgestion --group fiscal
qa.cmd list --product xgestion --group pagos-externos
qa.cmd list --product xgestion --group recuperacion
qa.cmd list --product xgestion --group concurrencia
qa.cmd list --product xgestion --group actualizacion
qa.cmd list --product xgestion --group beneficios
```

Estas fichas no se pasan a `run` mientras estén `planned`. `recuperacion`
también contiene pruebas implementadas anteriores: ejecutarlo no ejecuta REC.

## Orden propuesto y aceptación

| Hito | Preparación | Criterio de avance |
| --- | --- | --- |
| 0. Aceptar la base | Paquete privado, calibración y baseline de los 96 casos implementados. | Evidencia real por JAR/perfil, distinta de lint o dry-run. |
| 1. Cobros combinados | Medios manuales QA, cotización fija, control accesible de pagos. | Un cierre con importes por medio/moneda coherentes; cancelar/reintentar no duplica efectos. |
| 2. Documentos | Presupuestos/preventas y ventas previas con historia conocida. Definir qué documento se edita y cómo se devuelve dinero. | Convertir o revertir una sola vez; saldos, stock y documentos quedan relacionados. Contratos parciales no definidos bloquean su variante. |
| 3. Beneficios | Precios/tasas, descuentos, clientes y puntos con saldo/fecha conocidos. | Cálculo independiente coincide con pantalla, cobro e histórico; no se trasladan puntos de otro cliente. |
| 4. Interrupción y actualización | Inyección de falla controlada, copias descartables y recuperación comprobada; versiones de origen/destino. | Se distingue pendiente, confirmado y fallido; no se repite una operación incierta ni se pierde historia al actualizar. |
| 5. Integraciones y concurrencia | Homologación fiscal, sandbox de pagos, dos puestos, protocolo de sincronización y política de aislamiento específica. | Estado local/remoto conciliado, identidad completa y ausencia de duplicación tras reintentos/conflictos. |

Los hitos no tienen fechas. Fiscal y pagos son **P0 cuando se usan en el negocio**:
la dependencia de otro laboratorio no reduce su impacto. Los circuitos
financieros previos siguen su [roadmap](circuitos-criticos.md); no quedan sustituidos.

## Relaciones con fichas anteriores

- [LPR-022](../scenarios/listas-precios/XG-LPR-022.md) cubre reapertura con
  precios/moneda; PRE añade decisiones y efectos de guardar/convertir.
- [FIN-003](../scenarios/conciliacion/XG-FIN-003.md) anula crédito sin cobros;
  DEV exige definir parciales, devolución de dinero y documentos relacionados.
- [FIN-004](../scenarios/conciliacion/XG-FIN-004.md) prueba fallo de cobro manual;
  REC distingue guardar borrador, cerrar venta y perder la respuesta.
- [FIN-009](../scenarios/conciliacion/XG-FIN-009.md) prueba confirmación repetida;
  CON requiere dos actores y, según caso, sincronización real.
- RES conserva cuenta/mesa/cocina y sus canales; FEL/PEX describen los estados
  de los servicios, sin afirmar que aprobar Venta aprueba Restobar.
- BKP diferencia exportar/importar/restaurar; ACT comprueba cambio de versión.
- PRM-079 cubre descuento de artículo sobre oferta; BEN amplía globales,
  impuestos y puntos. Permisos y contexto son variantes transversales.

## Dependencias y mantenimiento

Los fixtures adicionales, accesibilidad, oráculos por identidad y mecanismos
de fallos todavía deben implementarse. El seed comercial no garantiza todos
estos datos. PRM-077/078 siguen pendientes del paquete multicontexto.

El laboratorio actual conserva Windows exclusivo y offline. Estas fichas no
autorizan desactivar controles, conectar servicios productivos, emitir fiscal
real ni cobrar dinero real. Una restauración local tampoco revierte un efecto
remoto: el laboratorio ampliado necesita conciliación y limpieza propia.

Toda automatización futura actualiza ficha, grupo, datos, variantes y
referencias, y registra JAR/build, perfil, entorno y evidencia. INFO resume,
DEBUG muestra pasos y TRACE diagnóstico saneado; un fallo siempre conserva
esperado/observado. Las referencias fuente de este complemento usan el commit
`daa002d597d0fa7380ace204d3727085c52d1415`; no actualizan retrospectivamente los
anexos antiguos ni acreditan ejecución real.
