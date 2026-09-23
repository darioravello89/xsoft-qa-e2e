# Cobros combinados, presupuestos y devoluciones

**20 fichas pendientes: 8 de cobros, 6 de presupuestos/preventas y 6 de devoluciones.**
Son **18 P0** y **2 P1**; todas `planned`, sin automatización nueva, seed propio ni validación real.
Complementan [roadmap](roadmap.md), [cobertura](cobertura.md) y [circuitos críticos](circuitos-criticos.md).

## Consultar por grupo

| Grupo | Recorridos | Alcance |
| --- | --- | --- |
| `cobros-combinados` | COB-001..008 | Reparto, corrección, cancelación, monedas, vuelto y recuperación; incluye un control del importe real en el cierre simple. |
| `presupuestos` | PRE-001..006 | Guardar, cancelar, editar, convertir, continuar preventa y proteger históricos. |
| `devoluciones` | DEV-001..006 | Anulación pagada, varios medios, parcial pendiente de contrato, pagos posteriores, contexto y recuperación. |

Consultar con `qa.cmd list --product xgestion --group cobros-combinados`,
`--group presupuestos` o `--group devoluciones`. El grupo devoluciones también
incluye fichas anteriores; un caso con varios tags se cuenta una sola vez.
Estas fichas pendientes no se ofrecen como ejecutables.

## Cobros

| ID | Recorrido | Prioridad | Estado |
| --- | --- | --- | --- |
| [XG-COB-001](../scenarios/cobros-combinados/XG-COB-001.md) | Cobrar una venta repartiendo el total entre dos medios | P0 | Pendiente |
| [XG-COB-002](../scenarios/cobros-combinados/XG-COB-002.md) | Corregir un pago cargado antes de completar el cobro combinado | P0 | Pendiente |
| [XG-COB-003](../scenarios/cobros-combinados/XG-COB-003.md) | Cancelar un cobro combinado y retomarlo sin arrastrar pagos | P0 | Pendiente |
| [XG-COB-004](../scenarios/cobros-combinados/XG-COB-004.md) | Combinar pagos ARS y USD sin convertir dos veces | P0 | Pendiente |
| [XG-COB-005](../scenarios/cobros-combinados/XG-COB-005.md) | Alternar, editar y vaciar el importe recibido sin recuperar valores viejos | P0 | Pendiente |
| [XG-COB-006](../scenarios/cobros-combinados/XG-COB-006.md) | Respetar la habilitación de monedas y rechazar cotizaciones inválidas | P0 | Pendiente |
| [XG-COB-007](../scenarios/cobros-combinados/XG-COB-007.md) | Calcular el vuelto de un cobro combinado sin duplicar dinero | P0 | Pendiente |
| [XG-COB-008](../scenarios/cobros-combinados/XG-COB-008.md) | Recuperar un fallo de cobro combinado sin repetir pagos | P0 | Pendiente |

## Presupuestos y preventas

| ID | Recorrido | Prioridad | Estado |
| --- | --- | --- | --- |
| [XG-PRE-001](../scenarios/presupuestos/XG-PRE-001.md) | Guardar un presupuesto nuevo sin registrar un cobro | P0 | Pendiente |
| [XG-PRE-002](../scenarios/presupuestos/XG-PRE-002.md) | Cancelar la elección de moneda del presupuesto y corregir un rechazo | P0 | Pendiente |
| [XG-PRE-003](../scenarios/presupuestos/XG-PRE-003.md) | Agregar productos a un presupuesto reabierto y conservar una sola propuesta | P1 | Pendiente |
| [XG-PRE-004](../scenarios/presupuestos/XG-PRE-004.md) | Convertir un presupuesto en venta una sola vez | P0 | Pendiente |
| [XG-PRE-005](../scenarios/presupuestos/XG-PRE-005.md) | Completar una preventa editable y llevarla al cierre | P0 | Pendiente |
| [XG-PRE-006](../scenarios/presupuestos/XG-PRE-006.md) | Distinguir propuestas editables de documentos cerrados o anulados | P1 | Pendiente |

## Devoluciones

| ID | Recorrido | Prioridad | Estado |
| --- | --- | --- | --- |
| [XG-DEV-001](../scenarios/devoluciones/XG-DEV-001.md) | Anular una venta pagada devolviendo el neto recibido | P0 | Pendiente |
| [XG-DEV-002](../scenarios/devoluciones/XG-DEV-002.md) | Anular una venta con pagos combinados y conciliar cada medio | P0 | Pendiente |
| [XG-DEV-003](../scenarios/devoluciones/XG-DEV-003.md) | Devolver parte de los productos sin anular toda la venta | P0 | Pendiente |
| [XG-DEV-004](../scenarios/devoluciones/XG-DEV-004.md) | Resolver una devolución cuando hubo anticipo y pagos posteriores | P0 | Pendiente |
| [XG-DEV-005](../scenarios/devoluciones/XG-DEV-005.md) | Cancelar o rechazar una anulación sin afectar otra venta | P0 | Pendiente |
| [XG-DEV-006](../scenarios/devoluciones/XG-DEV-006.md) | Recuperar una anulación incierta sin duplicar reembolsos | P0 | Pendiente |

## Prioridad y condiciones de avance

1. **Reparto y cancelación:** COB-001/003/004/005/006. Hito: importes reales y originales conservados, una venta final, caja/stock conciliados y ausencia de pagos activos del intento cancelado. COB-002 necesita resolver la acción accesible para quitar una línea.
2. **Vida de la propuesta:** PRE-001/002/003/004/005/006, usando LPR-022 como base de lista/moneda. Hito: guardar no cobra, convertir cobra una sola vez y el stock respeta el perfil. Definir tipo local permitido y efectos de cambiar comprobante antes de ejecutar.
3. **Devolución y recuperación:** DEV-001/002/005/006 y COB-007/008. Hito: reintegro neto, contexto correcto y reintento sólo después de reconciliar el estado. El reparto del vuelto y los fallos parciales necesitan oráculo/procedimiento propio.
4. **Contratos todavía abiertos:** DEV-003/004. Identificar soporte y acordar reglas antes de crear automatización de devolución parcial o de asignar abonos posteriores a una venta.

No se fijan fechas hasta preparar datos, accesibilidad y laboratorio. Ningún test fuente,
parser o dry-run sustituye evidencia del JAR. Las variantes bloqueadas no se cuentan
como aprobadas junto a la variante principal.

## Datos propuestos para un futuro baseline

| Perfil | Datos y resultado de negocio |
| --- | --- |
| Reparto ARS | Venta 2.000; efectivo 500/tarjeta manual 1.500; insuficiente hasta completar total. |
| Corrección | Reemplazar tarjeta 1.000 por 800; efectivo 500 + tarjeta 800 + transferencia manual 700 = 2.000. |
| Reparto ARS/USD | ARS 500 + USD 1 a 1.500 = ARS 2.000; conservar originales y equivalentes separados. |
| Vuelto | Recibido 2.500 para total 2.000 => vuelto 500; atribución por medio pendiente de contrato. |
| Presupuesto | A × 2 a 1.000, sin cobro; stock inicial 10; perfil OFF conserva 10, perfil ON necesita momento de descuento declarado. |
| Edición/preventa | Agregar un artículo a propuesta editable y conservar una sola identidad; no invocar la app externa. |
| Anulación pagada | Venta 2.000, recibido 3.000/vuelto 1.000: devolver 2.000, reponer dos unidades una vez. |
| Parcial propuesta | Venta A × 2 a 1.000 + B × 1 a 500; devolver A × 1 => 1.000 sólo si el circuito y regla se confirman. |
| Abonos posteriores | Venta 2.000/anticipo 400/abono 600: acordar devolución frente a crédito global antes de automatizar. |

Estos datos no están instalados ni garantizados por el seed comercial. Preparar
identidades, moneda, formas de cobro, estados, inventario y cuentas de control.
Cada variante usa baseline independiente; no editar registros de negocio durante el
recorrido para fabricar un resultado.

## Contratos y límites que deben quedar resueltos

| Tema | Verificado en fuente | Pendiente antes de automatizar |
| --- | --- | --- |
| Quitar pago | DialogCobroMultiple elimina una fila con doble clic mientras la venta no está cerrada. | Acción accesible/atajo o autorización específica; no extender el permiso del editor de cantidad de Venta. |
| Cierre múltiple | Los pagos se insertan al ingresarlos; Cancelar los anula. Con total exacto puede cerrar automáticamente el diálogo principal. | Lecturas por identidad y procedimiento ante fallo entre ingreso de líneas y cierre. |
| Moneda | Se conservan importe original/operativo y el resumen convierte según moneda visible; multimoneda depende del perfil. | Dominio de caja física/equivalente y cambios de cotización con diálogo abierto. |
| Vuelto | Se calcula recibido menos total y la anulación limita la devolución al neto pagado. | Medio que soporta el vuelto/reintegro; no depender del orden accidental de la consulta de pagos. |
| Presupuesto | Elegir moneda precede a guardar; Guardar no es cobrar; descuento de stock configurable. | Tipo local al convertir, efectos de cambiar comprobante y stock ya descontado, sin activar fiscal. |
| Preventa | El estado editable permite agregar productos; cerrado/anulado deshabilita Agregar. | Origen y trazabilidad preparados; no afirmar integración de red ni protección de todos los controles por un único botón. |
| Parcial | Se verificó anulación completa, no devolución parcial local. | Soporte, UI, documento, cantidades acumuladas, importe y vínculo al original. DEV-003 permanece bloqueado. |
| Abono posterior | Anulación simple usa movimiento asociado y pagado/vuelto del documento. | Imputación del pago global, devolución o saldo a favor; no deducirlo de un saldo observado. DEV-004 permanece bloqueado. |
| Fallos | Hay escrituras por pasos y controles parciales de estado. | No presumir transacción global de anulación o de toda preparación de pagos; definir recuperación por punto de fallo. |

Las integraciones bancarias, devoluciones por pasarela, notas de crédito fiscales,
impresión y sincronización tienen laboratorio propio. Un registro local de devolución
en tarjeta manual no prueba devolución real por una entidad externa.

## Relación con casos existentes

- [LPR-022](../scenarios/listas-precios/XG-LPR-022.md) conserva el detalle de reapertura de lista/moneda. PRE agrega creación, modificación y conversión; no crea otra ficha para el mismo objetivo.
- [CCC-009](../scenarios/ctacte-clientes/XG-CCC-009.md) conserva anulación simple a crédito con/sin anticipo, sin abonos posteriores. DEV-004 delimita justamente ese contrato faltante.
- [FIN-003](../scenarios/conciliacion/XG-FIN-003.md) sigue siendo anulación de crédito sin cobros; DEV-001/002 tratan ventas pagadas.
- [FIN-009](../scenarios/conciliacion/XG-FIN-009.md) trata repetición de confirmación; COB-008/DEV-006 agregan los estados particulares de estos circuitos.
- [RES-019](../scenarios/restobar/XG-RES-019.md) conserva recetas/extras al anular Restobar; no se trasladan sus reglas de inventario a artículos simples.
- Las ofertas con varios medios habilitados no son cobro dividido: ver [canastas de ofertas](canastas-ofertas.md).

## Evidencia y mantenimiento

Cada nueva implementación debe resolver su contrato, preparar seed/baseline autorizado,
calibrar acciones, actualizar ficha y automatización juntas y generar evidencia del
JAR. Separar documentado, implementado y validado sobre versión concreta.
INFO resume, DEBUG describe pasos y TRACE aporta diagnóstico saneado; todo fallo
conserva esperado/observado y evidencia aun con INFO.

## Anexo técnico y trazabilidad

Fuente inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Las fichas usan líneas de esta revisión,
posterior a la utilizada por mapas anteriores. No se reetiquetan referencias antiguas
como si hubieran sido revisadas de nuevo.

- `src/ModuloVentas/Vistas/Dialogs/DialogCobroMultiple.java:309-447`: ingreso y completitud.
- `src/ModuloVentas/Vistas/Dialogs/DialogCobroMultiple.java:536-600`: cancelar, quitar y habilitación de moneda.
- `src/ModuloVentas/Vistas/Dialogs/formTicketCierre.java:572-625`: retorno del reparto y cierre automático exacto.
- `src/ModuloVentas/Vistas/FormVenta.java:5183-5273`: guardar presupuesto y moneda.
- `src/ModuloVentas/Vistas/FormVenta.java:6216-6238`: tipo al convertir y cierre repetido.
- `src/ModuloVentas/Vistas/FormVenta.java:6305-6346`: persistencia de cierre y stock previo.
- `src/ModuloVentas/Vistas/FormVentas.java:1323-1359`: contexto e inicio de anulación.
- `src/ModuloVentas/Vistas/FormVentas.java:1426-1442`: devolución de dinero configurable y estados.
- `src/ModuloVentas/Entidades/TicketVenta.java:3302-3382`: reversión de stock/deuda y reintegro neto.
- `src/ModuloVentas/Entidades/VentaPago.java:121-133`: consulta de pagos sin orden explícito para la anulación.
- `test/ModuloVentas/Entidades/CobroMultipleMonedaCalculadorTest.java:14-81`: agregados y moneda.
- `test/ModuloVentas/Vistas/Dialogs/FormTicketCierreMonedaStateTest.java:72-182`: estado de entrada real.
- `test/ModuloVentas/Entidades/VentaTotalesCalculadorTest.java:87-105`: devolución neta y redondeo.

Las pruebas fuente orientan los escenarios, pero no acreditan ejecución real,
dispositivos, pasarelas ni todas las modalidades propuestas.

