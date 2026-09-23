# Libro Diario y Caja: dinero registrado, arqueo y cierre

Esta ampliación contiene **18 fichas `planned`**: ocho de Libro Diario, XG-LDI-001..008, y diez de Caja, XG-CAJ-001..010. No agrega automatización ejecutable ni resultados reales. Consultar [roadmap](roadmap.md), [cobertura](cobertura.md) y [Excel de control](../../../docs/coverage/xgestion-cobertura.xlsx).

## Qué comprueba cada circuito

**Libro Diario** es la consulta y carga de movimientos financieros de ingreso/egreso, clasificados por concepto, medio, moneda y contexto. La fuente inspeccionada no establece aquí un libro contable de partida doble; no se inventan asientos de debe/haber ni balances contables.

**Caja** reúne los efectos operativos que corresponden al turno/fecha/puesto/operador y a cada medio. El fondo, las ventas y el dinero cobrado o entregado deben conciliarse con documentos y deudas por origen.

El Libro Diario predeterminado excluye el concepto movimientoCaja (1). Un ingreso de caja puede registrar además un concepto cuando Contabiliza está activado; un egreso genera la representación de caja y del concepto, y opcionalmente afecta la cuenta del proveedor. **No exigir mismas filas ni mismo saldo en Libro Diario y Caja.** Comprobar que una operación mueve dinero/deuda una sola vez en cada circuito que corresponde.

Ejemplo del perfil de LDI-004: caja inicial $1.000 + ingreso $200 − pago proveedor $100 = caja $1.100; deuda proveedor $500 − pago $100 = $400. Las representaciones financieras del pago no significan que salieron $200 de caja.

## Grupos para QA

| Grupo | Alcance | Casos |
| --- | --- | --- |
| `libro-diario` | Altas, validaciones, filtros, conciliación de origen, anulaciones, permisos y recuperación. | LDI-001..008, 8 pendientes |
| `caja` | Fondo, ventas/cobros, ingresos/egresos, proveedor, arqueo y cierre. | CAJ-001..010, 10 pendientes |
| `cierre-caja` | Arqueo, contexto, cierre normal/ciego, fallos y reimpresión. | CAJ-005..010, 6 pendientes |

La tabla identifica las fichas propias de esta batería. El grupo `caja` también
incluye recorridos FIN y de cuentas corrientes, por lo que el listado completo
incluye veinte pendientes. Los grupos transversales se superponen; no
sumarlos como nuevos escenarios.

```powershell
.\qa.cmd list --product xgestion --group libro-diario
.\qa.cmd list --product xgestion --group caja
.\qa.cmd list --product xgestion --group cierre-caja
```

Estos comandos consultan el backlog. Los IDs nuevos no tienen Robot; el menú no debe ofrecer un caso pendiente como ejecutable ni producir PASS por mostrarlo.

## Escenarios

| ID | Recorrido del usuario | Prioridad | Automatización |
| --- | --- | --- | --- |
| [XG-LDI-001](../scenarios/libro-diario/XG-LDI-001.md) | Registrar ingreso y egreso manual con concepto y medio correctos | P0 | Pendiente |
| [XG-LDI-002](../scenarios/libro-diario/XG-LDI-002.md) | Corregir datos inválidos o cancelar un movimiento antes de guardar | P0 | Pendiente |
| [XG-LDI-003](../scenarios/libro-diario/XG-LDI-003.md) | Filtrar movimientos y conciliar totales e importes ARS y USD | P0 | Pendiente |
| [XG-LDI-004](../scenarios/libro-diario/XG-LDI-004.md) | Reconocer el origen de cada movimiento sin duplicar dinero o deuda | P0 | Pendiente |
| [XG-LDI-005](../scenarios/libro-diario/XG-LDI-005.md) | Anular solo el movimiento seleccionado y conservar su trazabilidad | P0 | Pendiente |
| [XG-LDI-006](../scenarios/libro-diario/XG-LDI-006.md) | Respetar el acceso financiero del operador y el contexto autorizado | P0 | Pendiente |
| [XG-LDI-007](../scenarios/libro-diario/XG-LDI-007.md) | Recuperar un fallo al guardar sin acreditar éxito ni duplicar el importe | P0 | Pendiente |
| [XG-LDI-008](../scenarios/libro-diario/XG-LDI-008.md) | Consultar históricos y comprobantes sin alterar el movimiento | P1 | Pendiente |
| [XG-CAJ-001](../scenarios/caja/XG-CAJ-001.md) | Abrir turno y registrar el fondo inicial una sola vez | P0 | Pendiente |
| [XG-CAJ-002](../scenarios/caja/XG-CAJ-002.md) | Conciliar ventas cobradas y vuelto con la caja de cada medio | P0 | Pendiente |
| [XG-CAJ-003](../scenarios/caja/XG-CAJ-003.md) | Registrar ingresos y egresos respetando el saldo del medio elegido | P0 | Pendiente |
| [XG-CAJ-004](../scenarios/caja/XG-CAJ-004.md) | Pagar a un proveedor desde caja y reducir solo su deuda | P0 | Pendiente |
| [XG-CAJ-005](../scenarios/caja/XG-CAJ-005.md) | Arquear cada medio y separar efectivo ARS de USD | P0 | Pendiente |
| [XG-CAJ-006](../scenarios/caja/XG-CAJ-006.md) | Seleccionar el turno y puesto correctos aunque cruce medianoche | P0 | Pendiente |
| [XG-CAJ-007](../scenarios/caja/XG-CAJ-007.md) | Cerrar un turno por el circuito normal y conservar su balance | P0 | Pendiente |
| [XG-CAJ-008](../scenarios/caja/XG-CAJ-008.md) | Cerrar a ciegas registrando diferencias sin inventar dinero | P0 | Pendiente |
| [XG-CAJ-009](../scenarios/caja/XG-CAJ-009.md) | Cancelar o recuperar un cierre fallido sin duplicar sus efectos | P0 | Pendiente |
| [XG-CAJ-010](../scenarios/caja/XG-CAJ-010.md) | Reimprimir el cierre guardado sin recalcularlo con operaciones nuevas | P0 | Pendiente |

## Hitos y criterios de avance

1. **Datos y oráculos financieros.** Preparar conceptos propios, medios manuales, fondos, movimientos por origen, usuarios y documentos/deudas sintéticos. Declarar qué campos muestran recaudación, fondo, saldo operativo o importe original. Exigir identidad completa y deltas; no comparar contra un total calculado por la misma pantalla.
2. **Registrar y conciliar dinero.** LDI-001/002/004 y CAJ-001..004. Aceptación: ingreso, venta y pago único, cancelación sin efectos, vuelto por neto y deuda solo del cliente/proveedor elegido.
3. **Aislamiento y acceso.** LDI-003/005/006 y CAJ-006. Aceptación: filtro/contexto correctos, permiso efectivo, baja de una sola identidad y turno que cruza medianoche. Esperar el paquete multicontexto para sus variantes; no emplear otra instalación real.
4. **Arqueo y cierre.** CAJ-005/007/008. Aceptación: efectivo/otros medios y monedas separados, conteo independiente, diferencia explicable y un único turno cerrado. Resolver el oráculo mixto ARS/USD antes de acreditar esa variante.
5. **Recuperación e históricos.** LDI-007/008 y CAJ-009/010. Aceptación: fallos informados, efectos parciales identificables, recuperación sin duplicación y reimpresión desde snapshot. La impresora y enlaces externos requieren laboratorio propio; las fichas no habilitan esos efectos por sí mismas.

No fijar fechas hasta contar con paquete, calibración y capacidad. La prioridad es P0 para integridad de dinero/deuda/estados; LDI-008 es P1 de consulta histórica. Las variantes pendientes dentro de una ficha impiden acreditar la ficha completa.

## Datos y perfiles pendientes

El seed de productos/ofertas no prepara por sí mismo el contrato de esta batería. Antes de automatizar se necesita una extensión versionada con:

- Conceptos QA de ingreso/egreso, medios de pago manuales con clasificación de arqueo por importe/cantidad/ambos/ninguno y valores control para no mezclar destinos.
- Turno abierto/cerrado, apertura sin fondo y con fondo, período cruzando medianoche, actividades fuera de intervalo, operadores y puestos con números locales coincidentes.
- Cliente/proveedor con deuda inicial conocida; venta/cobro/pago y vínculos de origen, sin datos privados reales.
- Moneda original y operativa ARS/USD, cotización guardada distinta de la actual y perfil que define cómo presenta el total general.
- Configuración efectiva de menú y módulo; cierre normal/ciego, tolerancias, alerta de saldo y salida de proceso declaradas por perfil.
- Fallos controlados locales antes/después de la escritura, snapshot de cierre y salida de impresión de pruebas. Deshabilitar transportes externos o prepararlos mediante laboratorio autorizado.

Cada caso se restaura desde su baseline. No resolver diferencias escribiendo saldos a mano ni eliminando filas; preservar la evidencia primero.

## Riesgos de fuente que requieren reproducción

- **Baja por identidad incompleta:** `MovimientoFinanzas.deleteMovimientoFinanzas` recibe computadora, pero su UPDATE usa empresa/sucursal/número sin computadora. El motivo recibido tampoco se persiste en ese método. LDI-005 establece el criterio de afectar solo el seleccionado y obtener trazabilidad; es un riesgo para reproducir, no un defecto validado sobre el JAR.
- **Alcance de consulta:** las consultas de Libro Diario revisadas no incluyen predicado Empresa en su WHERE. Acordar el alcance autorizado y verificar datos control de otra empresa antes de acreditar aislamiento en LDI-003.
- **Fallo de alta:** el método público de inserción puede devolver cero ante error y la pantalla de alta continúa hasta cerrarse. LDI-007 exige comprobar persistencia/resultado, sin atribuir éxito a la desaparición del formulario.
- **Arqueo antes de cierre:** cierre ciego guarda su movimiento antes de cerrar turno. CAJ-009 no supone rollback atómico; un error exige identificar registros parciales y definir recuperación sin duplicar el cierre.
- **USD y total general:** el cierre ciego presenta conteo USD separado. No sumar su valor nominal a pesos ni asumir cómo concilia el total general; CAJ-005 exige resolver esa variante con un fixture y oráculo propios.
- **Permisos:** hay visibilidad de menú por usuario y habilitación del módulo. No se verificó una política granular independiente de consultar/crear/anular; una variante de solo lectura necesita regla e implementación definidas.
- **Consulta frente a cierre:** imprimir un informe de turno abierto puede ofrecer finalizarlo. La acción elegida debe ser explícita y verificada; omitir/fallar impresión después de cerrar no reabre el turno.

## Evidencia, límites y trazabilidad

Fuente inspeccionada: XGestion2 `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`.

- `src/ModuloFinanzas/Vistas/FormLibroDiario.java:260-425` y `FormLibroDiarioMovimiento.java:254-321`: consulta/alta.
- `src/ModuloFinanzas/Entidades/MovimientoFinanzas.java:190-237,382-395`: errores, reintentos y baja.
- `src/ModuloVentas/Vistas/FormIngresoDeCaja.java:104-176` y `FormEgresoDeCaja.java:299-377`: orígenes de caja y cuentas.
- `src/ModuloVentas/Entidades/CajaValores.java:176-281`: período, contexto y conceptos.
- `src/ModuloVentas/Vistas/FormCierreDeCaja.java:739-806`, `FormCierreCajaCiego.java:284-443,691-701` y `src/ModuloEmpleados/Vistas/FormAbrirCerrarTurno.java:151-211`: turnos, arqueo y cierre.
- `src/ModuloVentas/Servicios/CierreCajaCiegoReimpresionService.java:30-128`: snapshot y reimpresión.
- Tests de apoyo: `CajaSaldoDisponibleServiceTest`, `CajaValoresEsperadoPorPagoTest`, `TurnoCajaSqlBuilderTest`, `CierreCajaCategoriasServiceTest`, `CierreCajaCiegoReimpresionServiceTest` y `MovimientoFinanzasInsertPolicyTest`. Sus rutas y líneas se detallan por ficha. El test de dominio de Libro Diario solo comprueba el enlace externo, no una operación financiera.

La validación real necesita JAR/SHA256, paquete, perfil, casos/variantes y reporte privado saneado. Lint, catálogo y dry-run no prueban dinero ni deuda. INFO resume, DEBUG muestra pasos y TRACE ayuda al diagnóstico; todo fallo conserva esperado/observado y evidencia, sin secretos.

Fuera del alcance de este lote: contabilidad de partida doble, conciliación bancaria externa, fiscalización y pagos reales. Las suites de cuentas corrientes complementarias deben validar su propia imputación, financiación y reversión; no se dan por cubiertas mediante un único saldo de caja.
