# Cuentas corrientes y cuotas: mapa de circuitos críticos

**24 fichas pendientes: 10 de clientes, 8 de proveedores y 6 de cuotas.**
Prioridades: **21 P0** sobre dinero/estado y **3 P1** de consulta y presentación.
Todas tienen `status: planned`; no agregan tests ejecutables ni datos de seed y no acreditan validación del JAR.

Este mapa complementa [roadmap](roadmap.md), [cobertura](cobertura.md), [remitos](remitos.md) y [Restobar](restobar.md). El QA elige un recorrido por su objetivo y usa los pasos de su ficha; los nombres de tablas y métodos quedan en trazabilidad.

## Grupos para QA

| Grupo | Propósito | Fichas |
| --- | --- | --- |
| `ctacte-clientes` | Vender a crédito, recibir abonos, corregir y consultar deuda. | CCC-001..010 |
| `ctacte-proveedores` | Reconocer compras, registrar pagos y conciliar deuda del proveedor. | CCP-001..008 |
| `cuotas` | Financiar, cobrar, actualizar mora y conservar el cronograma. | CUO-001..006 |

Todos pertenecen también a `cuenta-corriente` y `regression`. Consultar con
`qa.cmd list --product xgestion --group ctacte-clientes`,
`--group ctacte-proveedores` o `--group cuotas`.
Los grupos sólo pendientes se consultan; no se ofrecen como ejecutables.

## Clientes

| ID | Recorrido | Prioridad | Estado |
| --- | --- | --- | --- |
| [XG-CCC-001](../scenarios/ctacte-clientes/XG-CCC-001.md) | Vender a crédito con y sin anticipo | P0 | Pendiente |
| [XG-CCC-002](../scenarios/ctacte-clientes/XG-CCC-002.md) | Registrar un abono parcial a la cuenta del cliente | P0 | Pendiente |
| [XG-CCC-003](../scenarios/ctacte-clientes/XG-CCC-003.md) | Saldar la deuda del cliente con el importe exacto | P0 | Pendiente |
| [XG-CCC-004](../scenarios/ctacte-clientes/XG-CCC-004.md) | Conservar un pago mayor a la deuda como saldo a favor | P0 | Pendiente |
| [XG-CCC-005](../scenarios/ctacte-clientes/XG-CCC-005.md) | Respetar límites de crédito y permisos sin perder la venta | P0 | Pendiente |
| [XG-CCC-006](../scenarios/ctacte-clientes/XG-CCC-006.md) | Mantener separadas las deudas y los pagos en ARS y USD | P0 | Pendiente |
| [XG-CCC-007](../scenarios/ctacte-clientes/XG-CCC-007.md) | Corregir una deuda manual conservando su historia monetaria | P0 | Pendiente |
| [XG-CCC-008](../scenarios/ctacte-clientes/XG-CCC-008.md) | Cancelar un pago en preparación y dar de baja una deuda manual | P0 | Pendiente |
| [XG-CCC-009](../scenarios/ctacte-clientes/XG-CCC-009.md) | Anular una venta a crédito revirtiendo sólo su deuda y su cobro | P0 | Pendiente |
| [XG-CCC-010](../scenarios/ctacte-clientes/XG-CCC-010.md) | Consultar y exportar una cuenta de cliente sin mezclar monedas | P1 | Pendiente |

## Proveedores

| ID | Recorrido | Prioridad | Estado |
| --- | --- | --- | --- |
| [XG-CCP-001](../scenarios/ctacte-proveedores/XG-CCP-001.md) | Reconocer la deuda de una compra recibida y su pago inicial | P0 | Pendiente |
| [XG-CCP-002](../scenarios/ctacte-proveedores/XG-CCP-002.md) | Registrar pagos manuales parciales y totales al proveedor | P0 | Pendiente |
| [XG-CCP-003](../scenarios/ctacte-proveedores/XG-CCP-003.md) | Pagar desde caja y elegir si afecta la cuenta del proveedor | P0 | Pendiente |
| [XG-CCP-004](../scenarios/ctacte-proveedores/XG-CCP-004.md) | Cancelar un pago y retirar una deuda manual errónea | P0 | Pendiente |
| [XG-CCP-005](../scenarios/ctacte-proveedores/XG-CCP-005.md) | Conciliar la anulación de compra cuando hubo un anticipo | P0 | Pendiente |
| [XG-CCP-006](../scenarios/ctacte-proveedores/XG-CCP-006.md) | Distinguir saldos del proveedor por moneda | P0 | Pendiente |
| [XG-CCP-007](../scenarios/ctacte-proveedores/XG-CCP-007.md) | Editar movimientos manuales y proteger los originados por compra | P0 | Pendiente |
| [XG-CCP-008](../scenarios/ctacte-proveedores/XG-CCP-008.md) | Consultar deuda, saldo a favor y resumen del proveedor | P1 | Pendiente |

## Cuotas

| ID | Recorrido | Prioridad | Estado |
| --- | --- | --- | --- |
| [XG-CUO-001](../scenarios/cuotas/XG-CUO-001.md) | Crear un plan con anticipo y redondeo exacto de las cuotas | P0 | Pendiente |
| [XG-CUO-002](../scenarios/cuotas/XG-CUO-002.md) | Cobrar una cuota completa conservando moneda de deuda y de cobro | P0 | Pendiente |
| [XG-CUO-003](../scenarios/cuotas/XG-CUO-003.md) | Aplicar mora una sola vez y respetar gracia y tolerancia | P0 | Pendiente |
| [XG-CUO-004](../scenarios/cuotas/XG-CUO-004.md) | Evitar cobrar dos veces la misma cuota | P0 | Pendiente |
| [XG-CUO-005](../scenarios/cuotas/XG-CUO-005.md) | Rechazar un cobro inválido o fallido sin perder la cuota | P0 | Pendiente |
| [XG-CUO-006](../scenarios/cuotas/XG-CUO-006.md) | Reabrir el historial de cuotas y conservar el plan original | P1 | Pendiente |

## Orden propuesto y condiciones de avance

1. **Saldos y dinero básico:** CCC-001..004 y CCP-001..003. Acordar dominios de caja y origen de cada pago; preparar baselines, controles por identidad y medio. Hito: un cargo/pago produce una sola variación esperada y el cliente/proveedor de control no cambia.
2. **Límites, moneda y correcciones:** CCC-005..009 y CCP-004..007. Separar nuevo/editable/histórico, cancelación previa/anulación posterior, deuda/dinero. Hito: rechazos preservan operación y los importes históricos no se recotizan.
3. **Financiación:** CUO-001..005. Disponer de planes, cotizaciones y calendario reproducibles; preparar errores controlados y declarar alcance de concurrencia. Hito: anticipo y redondeos exactos, una sola cancelación, mora idempotente y recuperación sin estados parciales.
4. **Consulta y entrega:** CCC-010, CCP-008 y CUO-006. Hito: filtros, saldos y artefactos locales coinciden con el baseline; visualización no modifica deuda.

No hay fechas comprometidas. Cada hito necesita evidencia por JAR/paquete/perfil; automatización disponible y validación real son estados separados.

## Datos fijos propuestos, todavía no instalados

| Perfil | Valores que debe preparar el baseline |
| --- | --- |
| Cliente ARS | Venta 2.000, anticipo 500, deuda 1.500; abonos parcial/exacto; pago 1.200 sobre deuda 1.000 y siguiente cargo 500. |
| Límites | Saldo 1.500/límite 2.000; cierre 500 permitido y 500,01 rechazado; ARS/USD independientes; roles con permisos documentados. |
| Monedas | Deuda ARS 15.000 + USD 25; pago USD 10 a 1.200; cotizaciones histórica/actual distintas. |
| Proveedor | Compra 2.000/pagado 500; manuales 500/1.500; egreso 500 con/sin envío a cuenta; compra anulable y deuda de control 700. |
| Edición | Cliente: deuda 2.000/pago 500, corregir deuda a 3.000 => 2.500; proveedor con pago 750 => 2.250. |
| Plan | Venta 120/anticipo 20/financiado 100; redondeo a dos decimales, cuotas 33,33 + 33,33 + 33,34, sin intereses. |
| Cobro de cuota | Deuda USD 10 de origen 1.200; cobro ARS 15.000 a 1.500; cambio a 1.800 exige reconfirmar ARS 18.000. |
| Mora | Capital 1.000; dos días al 1% diario + fijo 5 => 1.025; repetir mantiene 1.025; día siguiente 1.035. |

No reutilizar nombres como si fueran identidades existentes. Preparar manifiesto de IDs, fechas, permisos, cuentas de control y oráculos antes del seed. Los datos nuevos no forman parte del catálogo comercial vigente. La restauración y los fallos controlados deben pertenecer al laboratorio privado; las fichas no habilitan mutaciones del ERP compartido.

## Reglas verificadas en fuente y límites de lo afirmado

| Tema | Fuente inspeccionada | Criterio / límite para E2E |
| --- | --- | --- |
| Signo del saldo | Cliente: deuda menos pago. Proveedor: deuda menos pago aunque sus columnas técnicas usan signos opuestos. | Deuda 2.000/pago 500 => saldo 1.500; pago mayor deja saldo a favor. No equiparar nombres técnicos con ingreso/egreso de caja. |
| Pago manual cliente | La ruta individual registra cuenta corriente e ingreso financiero en una transacción. | CCC-002/003 concilian ambos; los dos botones Nuevo Pago de la cuenta abren circuitos distintos. |
| Pago manual proveedor | El editor individual registra cuenta corriente. | No prometer egreso financiero automático ni volver a cargarlo por caja sin regla declarada. |
| Egreso a proveedor | Egreso de caja registra dominios/conceptos y opcional movimiento de proveedor. | CCP-003 necesita oráculo por dominio; dos filas no prueban dos salidas físicas. Recuperación entre escrituras pendiente de laboratorio. |
| Límite | Igualdad permitida, exceso rechazado; ARS y USD separados; error conserva venta. | No se verificó bypass de supervisor por superar límite. El perfil restringido necesita permiso concreto. |
| Edición/baja | Actualización y baja reencadenan cuenta corriente. Proveedor bloquea editar movimientos de remito/factura. | Editar o eliminar un pago no demuestra corregir/devolver automáticamente caja. Circuito pendiente de definición. |
| Anulación cliente | Invierte importe operativo y original del movimiento asociado; devolución de dinero es una opción separada. | CCC-009 es venta simple; no generalizar a cuotas, múltiples movimientos asociados ni pagos posteriores. |
| Anulación proveedor | Compensa total/pagado de compra; stock/precios se rigen por REM-024. | El destino del anticipo y su eventual reintegro requieren regla independiente. No inferir devolución por saldo cero. |
| Moneda | Cliente resume por moneda; editores guardan moneda/cotización histórica; proveedor distingue moneda en detalle. | Tarjetas e informes de proveedor necesitan contrato multimoneda previo; no aprobar un total ambiguo. |
| Cuotas | Pago completo, estado protegido, cancelación en moneda de deuda, foto de cobro separada y mora incremental. | No documentar abonos parciales de cuota como disponibles. La ruta leída de cuotas no demuestra ingreso financiero automático. |

**Imputación por comprobante:** los pagos manuales descritos reducen una cuenta global.
No se afirma imputación FIFO, aplicación a facturas seleccionadas, refinanciación o
distribución de un abono entre cuotas. Si el negocio necesita esos recorridos,
primero identificar el circuito y acordar su resultado. No generar casos aprobados
por la simple existencia de una referencia a venta o de un saldo total.

**Aislamiento:** preparar empresas, personas y puestos con identidades distintas.
El saldo de una persona puede consolidar sucursales dentro de su empresa; declarar
el alcance de cada consulta. La protección de doble cobro en una base no acredita
concurrencia entre bases desconectadas ni sincronización.

## Cruces con fichas ya documentadas

- [REM-001](../scenarios/remitos/XG-REM-001.md) y [REM-021](../scenarios/remitos/XG-REM-021.md): carga/recepción de compra; CCP-001 añade deuda y pago inicial.
- [REM-024](../scenarios/remitos/XG-REM-024.md): anulación de recepción, stock y conservación de precios; CCP-005 añade conciliación de deuda/anticipo.
- [RES-029](../scenarios/restobar/XG-RES-029.md): cuenta de Restobar a crédito; CCC-005 fija límites comprobados sin trasladar estados de mesa/cocina a Venta.
- CCC-009 no sustituye una futura anulación de financiación; CUO-006 conserva explícito ese límite.
- Libro diario y Caja requieren sus propios mapas y dominios de consulta; estas fichas sólo comprueban los efectos relacionados al recorrido.

## Evidencia y mantenimiento

Antes de habilitar una ficha: definir baseline y variantes, resolver los oráculos
señalados, calibrar acciones accesibles, implementar comprobaciones por identidad
y actualizar grupo, documentación y mapa. Conservar fuente y JAR/SHA256 utilizados.

En una ejecución futura, INFO informa caso/resultado; DEBUG muestra pasos y TRACE
diagnóstico saneado. Cualquier fallo conserva esperado, observado, categoría y
evidencia aun en INFO. Ante confirmación ambigua, conciliar antes de reintentar.
No compensar a mano para obtener un resultado aprobado. El Excel del mapa público
no debe incorporar credenciales, saldos privados ni reportes reales.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`.
Cada ficha incluye rutas y líneas de su regla. Referencias principales:

- `src/ModuloFinanzas/Entidades/CtaCteCliente.java:130-207`: pago manual e ingreso financiero transaccional.
- `src/ModuloFinanzas/Entidades/CtaCteCliente.java:458-512`: edición/baja de cuenta corriente.
- `src/ModuloFinanzas/Entidades/CuentaCorrienteSaldoService.java:41-109`: reencadenamiento cliente/proveedor.
- `src/ModuloFinanzas/Vistas/ValidacionLimiteCtaCteDialog.java:25-77`: límite y recuperación.
- `src/ModuloFinanzas/Vistas/FormCuentaCorrienteCliente.java:385-409`: dos accesos Nuevo Pago.
- `src/ModuloProveedores/Entidades/CtaCteProveedor.java:57-94`: movimiento manual.
- `src/ModuloProveedores/Vistas/FormCuentaCorriente.java:731-758`: bloqueo de edición de origen compra.
- `src/ModuloVentas/Vistas/FormEgresoDeCaja.java:299-370`: egreso y proveedor.
- `src/ModuloVentas/Entidades/TicketVenta.java:3315-3346`: anulación de cuenta y devolución separada.
- `src/ModuloProductos/Entidades/Compra.java:652-700`: compensación al anular compra.
- `src/ModuloVentas/Servicios/VentaCuotasService.java:129-273`: plan y mora.
- `src/ModuloVentas/Servicios/VentaCuotasService.java:488-542`: cobro de cuota.
- `src/ModuloVentas/Servicios/VentaCuotasRepository.java:33-59`: cuenta corriente de cuotas.
- `test/ModuloVentas/Servicios/VentaCuotasPersistenciaTest.java:14-104`: fotos, duplicados, errores, moneda e idempotencia.

Lectura de fuentes y tests es descubrimiento de reglas/riesgos; no valida el ERP
ejecutado, la base privada, Excel/PDF, impresión ni integración financiera.
