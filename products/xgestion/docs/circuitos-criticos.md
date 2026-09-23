# Roadmap de circuitos críticos: deuda, dinero e integridad

Este mapa agrega **58 fichas pendientes de automatización**. Describe qué debe
comprobar QA antes de aceptar los circuitos de mayor riesgo. No modifica el ERP,
no instala datos y no acredita ejecución real. El catálogo general contiene
298 fichas: 96 implementadas y 202 pendientes; las variantes no suman otros IDs.

Consultar el [Excel de cobertura](../../../docs/coverage/xgestion-cobertura.xlsx),
el [roadmap general](roadmap.md) y la [matriz](cobertura.md).

## Baterías y grupos

| Circuito | Grupo principal | Fichas nuevas | Mapa detallado |
| --- | --- | --- | --- |
| Clientes | `ctacte-clientes` | XG-CCC-001..010: 10 | [Cuentas corrientes](cuentas-corrientes.md) |
| Proveedores | `ctacte-proveedores` | XG-CCP-001..008: 8 | [Cuentas corrientes](cuentas-corrientes.md) |
| Cuotas y financiación | `cuotas` | XG-CUO-001..006: 6 | [Cuentas corrientes](cuentas-corrientes.md) |
| Libro Diario | `libro-diario` | XG-LDI-001..008: 8 | [Libro Diario y caja](libro-diario-caja.md) |
| Caja y cierre | `caja`, `cierre-caja` | XG-CAJ-001..010: 10 | [Libro Diario y caja](libro-diario-caja.md) |
| Conciliación y controles transversales | `conciliacion`, `integridad-operaciones` | XG-FIN-001..010: 10 | Tabla siguiente |
| Ajustes, traslados y cierre de inventario | `inventario` | XG-INV-001..004: 4 | [Inventario y respaldos](inventario-respaldos.md) |
| Respaldos y recuperación | `respaldos` | XG-BKP-001..002: 2 | [Inventario y respaldos](inventario-respaldos.md) |

Los grupos se superponen: por ejemplo, Caja también incluye conciliaciones FIN.
La cantidad de fichas de una familia no siempre coincide con todos los miembros
de su grupo. `cuenta-corriente`, `monedas`, `permisos`, `devoluciones`, `stock` y
`recuperacion` conservan su uso transversal y los IDs anteriores.

```text
qa.cmd list --product xgestion --groups
qa.cmd list --product xgestion --group ctacte-clientes
qa.cmd list --product xgestion --group ctacte-proveedores
qa.cmd list --product xgestion --group cuotas
qa.cmd list --product xgestion --group libro-diario
qa.cmd list --product xgestion --group caja
qa.cmd list --product xgestion --group conciliacion
qa.cmd list --product xgestion --group inventario
qa.cmd list --product xgestion --group respaldos
```

Estos grupos nuevos son consultables y permanecen no ejecutables mientras sólo
contengan `planned`. `run --group regression` sigue seleccionando 96 casos
implementados. Los nuevos escenarios no se incluyen como aprobados en un dry-run.

## Hitos de implementación y aceptación

No se asignan fechas. Cada hito requiere evidencia del JAR/build, perfil y datos
utilizados. P0 significa riesgo de dinero, saldos, stock, autorización o pérdida
de datos; P1 corresponde a consultas/variantes sin ese efecto, según cada ficha.

| Orden | Trabajo y dependencia | Criterio para avanzar |
| --- | --- | --- |
| 0. Laboratorio financiero | Preparar baseline descartable y forma comprobada de recuperarlo; clientes/proveedores, saldos por moneda, medios, conceptos, roles y turnos. Identificar controles accesibles. | Datos iniciales conocidos, lecturas acotadas por identidad y recuperación verificadas. Sin esto, las pruebas de mutación están bloqueadas. |
| 1. Deuda y cobros de clientes | Venta simple a crédito, anticipo, cobro parcial/total, límites, rechazo y cancelación; CCC y FIN-001. Depende de Venta aceptada. | Deuda correcta y efectos únicos del cobro por la ruta declarada; cancelar/rechazar conserva la operación. ARS y USD no se suman nominalmente. |
| 2. Compras y proveedores | CCP y FIN-002, vinculados a REM-001/021/024. Separar pago manual de pago desde caja. | Recepción, deuda, pago y caja se concilian por origen; el pago de otra persona o la cancelación no altera el saldo elegido. |
| 3. Libro Diario y cierre | LDI/CAJ: movimientos, consultas, bajas, arqueo, turno normal/ciego y diferencias. FIN-010 integra ventas actuales y cobros anteriores. | Sin duplicación por conceptos; turno/medio/puesto correctos; cierre único, con cancelación y evidencia histórica. Impresión depende de laboratorio propio. |
| 4. Cuotas y moneda | CUO: plan/anticipo, cobros, mora y recuperación. Requiere calendario/cotizaciones fijos y contrato de efecto financiero separado del cobro manual. | Capital, deuda y pagos por moneda coherentes; mora y cobro no se repiten; rechazo/fallo no deja efectos parciales. |
| 5. Anulación, permisos y recuperación | FIN-003..009 y variantes transversales; completar identidad, autorización, auditoría, fallos y doble confirmación. | Reversión sólo del origen correcto; sin efectos ajenos, duplicados ni éxito falso. Resultados ambiguos y preparaciones faltantes se identifican como bloqueo, no como aprobación. |
| 6. Inventario y continuidad | INV/BKP; conectar remitos, ventas y recetas ya documentados. Traslados, cierre anual e importación/restauración requieren perfiles propios. | Stock conciliado por movimientos; errores/reintentos no duplican existencias. Recuperación exacta demostrada antes de reutilizar un baseline. |

El orden permite adelantar variantes independientes. Restaurar el baseline de
la VM para desarrollar cualquier lote es una precondición inicial; probar las
funciones de respaldo/importación del producto es otra batería. Varios puestos,
empresas, concurrencia, servicios, impresión y red mantienen sus dependencias
propias. El paquete multicontexto todavía no está disponible.

## Recorridos que cruzan pantallas

| Ficha | Qué comprueba | Prioridad |
| --- | --- | --- |
| [XG-FIN-001](../scenarios/conciliacion/XG-FIN-001.md) | Venta a crédito, cobro manual parcial y sus efectos en deuda/finanzas/caja. | P0 |
| [XG-FIN-002](../scenarios/conciliacion/XG-FIN-002.md) | Remito recibido, deuda proveedor y pago desde caja, sin contar dos egresos. | P0 |
| [XG-FIN-003](../scenarios/conciliacion/XG-FIN-003.md) | Anular una venta simple a crédito sin cobros y conciliar deuda/stock. | P0 |
| [XG-FIN-004](../scenarios/conciliacion/XG-FIN-004.md) | Fallo controlado de cobro manual, estado persistido y reintento. | P0 |
| [XG-FIN-005](../scenarios/conciliacion/XG-FIN-005.md) | Consulta/corrección por identidad completa y conservación de contextos ajenos. | P0 |
| [XG-FIN-006](../scenarios/conciliacion/XG-FIN-006.md) | Abandono con supervisor, rechazo, auditoría y continuación. | P0 |
| [XG-FIN-007](../scenarios/conciliacion/XG-FIN-007.md) | Moneda histórica entre documento, deuda y resumen. | P0 |
| [XG-FIN-008](../scenarios/conciliacion/XG-FIN-008.md) | Movimientos del período, saldo acumulado y exportación del mismo alcance. | P0 |
| [XG-FIN-009](../scenarios/conciliacion/XG-FIN-009.md) | Confirmación repetida, reapertura y variante concurrente sin duplicación. | P0 |
| [XG-FIN-010](../scenarios/conciliacion/XG-FIN-010.md) | Jornada con venta actual, cobro de deuda anterior y pago a proveedor. | P0 |

Estas fichas comprueban relaciones entre circuitos. Las fichas CCC/CCP/CUO/LDI/CAJ
describen sus acciones individuales y variantes. Ejecutar una de ellas no
acredita automáticamente la otra: registrar qué recorrido y perfil se ejecutó.

## Datos fijos que faltan preparar

Los valores siguientes son requisitos, no registros ya creados por el seed actual:

- Clientes y proveedores control con saldo cero, deuda, pago parcial, saldo a
  favor e históricos; identificadores separados por empresa.
- ARS/USD, cotizaciones histórica y vigente, documentos legados y medios
  manuales identificados. No usar cotizaciones reales ni servicios de pago.
- Caja/turno abierto y cerrado, fondo inicial, conceptos de ingreso/egreso,
  deuda de fecha anterior, cierre ciego y diferencia conocida.
- Planes/cuotas pendientes y canceladas, fechas límite y mora; mecanismos para
  preparar tiempos sin alterar el reloj del host durante una prueba.
- Inventario por unidad/fracción, origen/destino y estados de traslado; cierre
  anual previo y pendiente; receta/opciones según las fichas RES.
- Operadores/revisores y permisos efectivos. No inventar un permiso granular
  donde la aplicación sólo configura acceso por menú.
- Fallos controlados con procedimiento entregado, acceso de varios contextos y
  medios de recuperación de VM. Las pruebas de restore no usan la base de trabajo.

Antes de implementar se versionan los contratos de fixtures, sus upserts
autorizados, colisiones y recuperación. Tener productos fijos no prepara deudas,
documentos, turnos o respaldos por sí solo. Ver [seed](seed.md).

## Reglas que evitan resultados engañosos

1. **Deuda, movimiento financiero, caja y stock tienen alcances diferentes.**
   Libro Diario predeterminado excluye `movimientoCaja`; un egreso desde caja
   puede representarse además por su concepto y por el pago al proveedor.
   Conciliar deltas por operación; no sumar todas las filas como dinero extra.
2. **Cobro manual, cobro de cuotas y pago a proveedor son rutas diferentes.**
   No presumir que todas crean un ingreso/egreso financiero ni que un movimiento
   manual implica imputación individual a un comprobante.
3. **Saldos por persona y empresa pueden agrupar varios puestos.** Aislar la
   mutación y su origen no significa partir indebidamente una cuenta empresarial.
4. **Anular no es borrar.** La venta simple sin cobros tiene un contrato distinto
   de la venta con anticipo/cuotas o la recepción que ya cambió costos.
5. **Histórico y período no son lo mismo.** Distinguir neto filtrado, acumulado,
   moneda original, equivalente histórico y una eventual valoración actual.
6. **Importar no prueba restauración exacta.** La importación inspeccionada hace
   upserts; no demuestra eliminar operaciones posteriores a la copia.
7. **Un fallo sin resultado conocido no habilita reintento ciego.** Confirmar
   primero si persistió; los casos de fallo necesitan preparación reproducible.

## Riesgos de fuente pendientes de reproducir

- La baja de `MovimientoFinanzas` recibe computadora, pero su actualización
  inspeccionada no la filtra ni persiste el argumento de motivo. El caso de
  anulación de Libro Diario debe probar identidades homónimas entre puestos y
  trazabilidad. No se declara defecto confirmado sobre el JAR.
- Cobros de cuotas, pantallas de saldo y clasificación de caja requieren un
  contrato por ruta; un test de cobro manual no demuestra sus efectos.
- Respaldos, importaciones y cierre anual tienen estados parciales/reintentos;
  no se asume atomicidad ni bloqueo general de ventas sin fuente y evidencia.

Fuente de esta ampliación: XGestion2
`4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Los anexos de fichas y mapas citan
rutas y tests. Los tests de políticas, JDBC simulado o inspección de texto son
insumos; la aceptación requiere recorrido visible sobre el FAT JAR de QA.

## Mantenimiento y evidencia

Cada implementación conserva el ID, actualiza ficha/Robot, datos, controles y
grupos, y regenera el Excel mediante `qa.cmd coverage`. Un caso documentado,
uno automatizado y uno validado en una versión son hitos distintos. El Excel
hereda prioridad de la etapa; para elegir variantes consultar la prioridad de
la ficha y sus requisitos.

INFO resume; DEBUG muestra acciones; TRACE ofrece diagnóstico saneado. Todo fallo
conserva paso, esperado, observado y evidencia. Registrar build/SHA256 del JAR,
perfil, paquete, fecha, responsable y reporte privado. Mantener consultas,
exportaciones y capturas sin credenciales ni datos de producción en el repositorio.

## Complemento de escenarios críticos

El [mapa complementario](complementos-criticos.md) añade 50 fichas
planned de cobros/documentos, servicios, continuidad y beneficios. Revisar
los filtros del catálogo y del Excel; deben conservar 96 implementados,
202 pendientes y ninguna validación real inferida. Los casos nuevos no se
ejecutan. Datos, accesibilidad y laboratorios propios siguen pendientes.
