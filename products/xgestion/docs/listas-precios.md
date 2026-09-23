# Listas de precios: mapa de escenarios de usuario

Hay **28 fichas planificadas, XG-LPR-001 a XG-LPR-028**. Ninguna incorpora Robot ni se considera aprobada. El objetivo es separar selección de lista, precio aplicado al producto, contexto, moneda y estado del documento para que QA pueda identificar qué está pendiente.

Consultar [cobertura general](cobertura.md), [roadmap](roadmap.md) y [datos comerciales](seed.md). El grupo `listas-precios` muestra este backlog; los filtros `listas-sucursal`, `listas-cliente`, `listas-horario` y `listas-prioridad` cruzan sus temas sin duplicar fichas.

```powershell
.\qa.cmd list --product xgestion --group listas-precios
.\qa.cmd list --product xgestion --group listas-horario
```

**Todavía no usar `run` para estos IDs:** requieren implementación, datos/perfiles y calibración. Una variante con oráculo pendiente se bloquea antes de ejecutar acciones dependientes; el resultado que aparezca no se convierte en esperado.

## Qué ya existe y qué agrega este mapa

- [XG-PRM-071](../scenarios/promociones/XG-PRM-071.md) automatiza una oferta de 10 % sobre precio normal y dos listas elegidas, con cobro y cancelación.
- [XG-PRM-072](../scenarios/promociones/XG-PRM-072.md) automatiza cambiar lista con recálculo ON y volver a precio normal cuando la lista no contiene el producto, sin escala por cantidad.
- Estas implementaciones **no acreditan ejecución real** ni todos los cruces de cliente, turno, sucursal, cantidad, moneda o Restobar.
- Las fichas LPR aíslan esos comportamientos. LPR-019/020 incorporan los ejemplos de lista ARS/USD sin oferta; LPR-016/017 incorporan las escalas y su competencia con lista elegida.
- [XG-RES-021](../scenarios/restobar/XG-RES-021.md) conserva el cruce Restobar de lista con extras. LPR-025 lo referencia y prueba recálculo ON/OFF sin extras.

## Matriz de fichas

| ID | Recorrido del usuario | Filtros | Prioridad | Estado |
| --- | --- | --- | --- | --- |
| [XG-LPR-001](../scenarios/listas-precios/XG-LPR-001.md) | Abrir una venta con la lista de su sucursal | `listas-sucursal`, `listas-prioridad` | P1 | planned |
| [XG-LPR-002](../scenarios/listas-precios/XG-LPR-002.md) | Separar las listas entre sucursales y reconocer el alcance global | `listas-sucursal` | P1 | planned |
| [XG-LPR-003](../scenarios/listas-precios/XG-LPR-003.md) | Elegir una lista fija por empresa sobre el default de sucursal | `listas-sucursal`, `listas-prioridad` | P1 | planned |
| [XG-LPR-004](../scenarios/listas-precios/XG-LPR-004.md) | Trabajar sin lista base sin anular las condiciones del cliente o turno | `listas-prioridad` | P1 | planned |
| [XG-LPR-005](../scenarios/listas-precios/XG-LPR-005.md) | Aplicar la lista del cliente antes que turno y base | `listas-cliente`, `listas-prioridad` | P1 | planned |
| [XG-LPR-006](../scenarios/listas-precios/XG-LPR-006.md) | Cambiar o quitar el cliente y recalcular las condiciones de la venta | `listas-cliente` | P1 | planned |
| [XG-LPR-007](../scenarios/listas-precios/XG-LPR-007.md) | Recuperar una lista automática cuando la del cliente no es válida | `listas-cliente`, `listas-prioridad` | P1 | planned |
| [XG-LPR-008](../scenarios/listas-precios/XG-LPR-008.md) | Aplicar la lista del horario antes que fija o sucursal | `listas-horario`, `listas-prioridad` | P1 | planned |
| [XG-LPR-009](../scenarios/listas-precios/XG-LPR-009.md) | Respetar los minutos de inicio y fin de un precio diurno | `listas-horario` | P1 | planned |
| [XG-LPR-010](../scenarios/listas-precios/XG-LPR-010.md) | Mantener el precio de un horario que cruza medianoche | `listas-horario` | P1 | planned |
| [XG-LPR-011](../scenarios/listas-precios/XG-LPR-011.md) | Resolver de forma estable el minuto compartido por dos horarios | `listas-horario`, `listas-prioridad` | P1 | planned |
| [XG-LPR-012](../scenarios/listas-precios/XG-LPR-012.md) | Ignorar horarios inactivos, incompletos o de otra empresa | `listas-horario` | P1 | planned |
| [XG-LPR-013](../scenarios/listas-precios/XG-LPR-013.md) | Distinguir una lista fija inexistente de volver al default de sucursal | `listas-prioridad`, `listas-sucursal` | P1 | planned |
| [XG-LPR-014](../scenarios/listas-precios/XG-LPR-014.md) | Cancelar la elección manual de lista sin alterar la venta | `listas-prioridad` | P1 | planned |
| [XG-LPR-015](../scenarios/listas-precios/XG-LPR-015.md) | Cambiar la lista sin recalcular los productos ya cargados | `listas-prioridad` | P0 | planned |
| [XG-LPR-016](../scenarios/listas-precios/XG-LPR-016.md) | Aplicar escalas de precio al alcanzar cantidades mínimas | `listas-prioridad` | P1 | planned |
| [XG-LPR-017](../scenarios/listas-precios/XG-LPR-017.md) | Priorizar la lista elegida sobre una escala al cargar productos | `listas-prioridad` | P1 | planned |
| [XG-LPR-018](../scenarios/listas-precios/XG-LPR-018.md) | Usar la escala cuando la lista elegida no contiene el producto | `listas-prioridad` | P1 | planned |
| [XG-LPR-019](../scenarios/listas-precios/XG-LPR-019.md) | Cobrar un precio ARS de lista sin promociones | `listas-prioridad` | P1 | planned |
| [XG-LPR-020](../scenarios/listas-precios/XG-LPR-020.md) | Convertir el precio USD de una lista a la moneda de la venta | `listas-prioridad` | P0 | planned |
| [XG-LPR-021](../scenarios/listas-precios/XG-LPR-021.md) | Rechazar una lista USD sin cotización y recuperar la venta | `listas-prioridad` | P0 | planned |
| [XG-LPR-022](../scenarios/listas-precios/XG-LPR-022.md) | Reabrir un presupuesto con su lista, moneda y precios guardados | `listas-prioridad` | P1 | planned |
| [XG-LPR-023](../scenarios/listas-precios/XG-LPR-023.md) | Consultar una venta histórica sin recalcular sus listas | `listas-prioridad` | P0 | planned |
| [XG-LPR-024](../scenarios/listas-precios/XG-LPR-024.md) | Distinguir fechas de auditoría de la vigencia de una lista | `listas-prioridad` | P1 | planned |
| [XG-LPR-025](../scenarios/listas-precios/XG-LPR-025.md) | Cambiar la lista de una cuenta Restobar abierta | `listas-prioridad` | P1 | planned |
| [XG-LPR-026](../scenarios/listas-precios/XG-LPR-026.md) | Distinguir la lista del mozo o cadete de cambiar el cliente en Restobar | `listas-cliente`, `listas-prioridad` | P1 | planned |
| [XG-LPR-027](../scenarios/listas-precios/XG-LPR-027.md) | Reabrir una cuenta Restobar editable y preservar las históricas | `listas-prioridad` | P0 | planned |
| [XG-LPR-028](../scenarios/listas-precios/XG-LPR-028.md) | Acordar la prioridad entre lista elegida y cantidad en Restobar | `listas-prioridad` | P1 | planned |

Prioridad por ficha: P0 para conservación de importes, moneda o históricos y P1 para resolución de condiciones. Si el Excel usa prioridad heredada de etapa, prevalece el detalle de la ficha para organizar el trabajo del equipo.

## Reglas verificadas y límites del oráculo

**Venta nueva o cambio de cliente.** Se evalúan cliente y luego turno. Si ninguno es válido, la configuración fija define la base: positiva usa esa lista, -1 consulta la sucursal, 0 deja Ninguna. Una fija positiva inválida no vuelve automáticamente a sucursal. Ninguna como base no suprime cliente/turno. Una clave por empresa prevalece sobre la global.

La búsqueda del default de sucursal requiere una lista activa de esa sucursal. Una lista global es válida como candidata explícita, pero no es fallback automático de una sucursal sin lista propia. Si hay varias listas activas propias, la consulta usa `LIMIT 1` sin ordenar: **no hay un precio determinista acordado para esa combinación**. El laboratorio inicial debe tener exactamente una por sucursal.

**Horario.** La selección usa el reloj local de Java, precisión de minuto e inicio/fin inclusivos. Admite cruce de medianoche. Ante dos turnos aplicables gana el menor ID. Compartir un extremo no cuenta como superposición de duración, aunque ambos puedan aplicar en ese minuto. La consulta revisada filtra empresa y estado activo; no usa día de semana ni fecha de caja. No afirmar refresco automático de una ventana abierta: se verificó resolución al abrir venta o cambiar cliente.

**Cantidad y lista elegida.** La carga/consolidación de FormVenta consulta la lista elegida antes que la escala global. En cambio, el recálculo de TicketVenta consulta la escala antes que la lista general cuando no preserva una lista propia del detalle; la prevalidación USD también consulta cantidad primero. No son rutas equivalentes. LPR-017 fija el esperado de carga y registra la variante de cambio posterior como oráculo pendiente.

El detalle seleccionado exige estado activo y mínimo alcanzado. La escala global elige el mayor mínimo alcanzado; los empates entre listas no tienen desempate completo en la consulta. No inventar una prioridad entre sucursal/global con el mismo mínimo. La cabecera y el detalle tienen estados diferentes y deben prepararse por separado.

La carga directa de una cantidad en una venta vacía tampoco equivale a sumar unidades a un renglón existente: la consolidación exige que su precio efectivo coincida. LPR-016 fija los importes de cargas directas; deja pendientes los oráculos de agregados que crucen una escala y de edición de cantidad. No aprobar esos recorridos usando por analogía el total de una carga única.

**Moneda.** Moneda de la lista, moneda contable del documento y moneda de pago son conceptos distintos. LPR-020 declara lista USD, documento ARS y pago ARS con cotización fija de laboratorio; LPR-022 declara presupuesto USD. Los importes originales y equivalentes se verifican por separado. No usar cotización real de mercado ni conectarse a servicios.

**Fecha.** Las fechas de alta/actualización son auditoría, no una vigencia desde/hasta de lista en las consultas inspeccionadas. Los horarios por día de semana presentes en el modelo no intervienen en la selección revisada. Si se requiere esa función, primero definir su regla y fuente; no derivarla del nombre de un campo.

**Restobar.** Cuenta, mesa y cocina mantienen estados independientes. La elección de mozo/cadete aplica su lista; cambiar cliente por el picker no usa el resolvedor automático de FormVenta. Al abrir una cuenta editable, el ticket puede recalcular su lista según configuración; los cerrados/anulados conservan el histórico. Su consolidación y cambio de lista tampoco se asumen equivalentes a Venta. LPR-028 exige un oráculo acordado para las vías de carga y la prioridad con cantidad.

## Datos disponibles y datos pendientes

Los siguientes son ejemplos públicos del seed, no resultados ejecutados:

| Ejemplo del seed | Datos | Ficha que lo incorpora |
| --- | --- | --- |
| LISTA-ARS | QA-SEED-LISTAS, lista 980101, ARS 750/u. | LPR-019 |
| LISTA-USD | QA-SEED-LISTAS, lista 980102, USD 2,50/u; falta perfil de cotización. | LPR-020 |
| CANTIDAD-Q1 | QA-SEED-CANTIDAD, 1 u, total ARS 1.000. | LPR-016 |
| CANTIDAD-Q2 | QA-SEED-CANTIDAD, 2 u a 900, total ARS 1.800. | LPR-016 |
| CANTIDAD-Q5 | QA-SEED-CANTIDAD, 5 u a 800, total ARS 4.000. | LPR-016 |
| LISTA-PRIORIDAD | QA-SEED-CANTIDAD, lista 980101 a 950, 5 u, total ARS 4.750. | LPR-017 |

Los restantes nombres A/B, C1/C2, S1/S2, T1/T2, F1/F2, M/D y listas QA-LPR son **fixtures nuevos pendientes de preparar**; sus importes están definidos en cada ficha. No tienen IDs reservados ni upserts nuevos en esta entrega. Los clientes, sucursales, empresas, turnos, responsables, documentos guardados y perfiles temporales requieren un paquete autorizado y reproducible.

No cambiar el reloj del host ni datos comerciales durante una venta. Para límites horarios preparar cada instante antes del JAR en un laboratorio temporal controlado, con Windows/MySQL y fecha del seed coherentes. Preservar las guardas actuales: un perfil temporal ausente es bloqueo de entorno.

## Avance recomendado

1. Preparar datos/contextos de Venta y cerrar LPR-001..008,013..015: elección automática, cliente y cambios de lista.
2. Automatizar LPR-016..021 con los ejemplos de seed y perfiles monetarios. Resolver antes los cruces de prioridad que no tienen oráculo uniforme.
3. Preparar ejecución temporal para LPR-009..012,024; documentos persistidos para LPR-022/023.
4. Habilitar el laboratorio Restobar para LPR-025..028, junto con RES-021. No extenderlo automáticamente a App Mozos, QR, cocina, dispositivos o red.

Cada implementación mantiene su ID y actualiza datos, perfil, controles accesibles, oráculos y ficha. La primera aceptación requiere evidencia de todos los pasos/variantes sobre JAR identificado. Si una variante conserva un oráculo pendiente, no acreditar la ficha completa.

## Anexo de fuentes

Fuente inspeccionada: **XGestion2, commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`**. Las fichas incluyen rutas y líneas específicas. Principales reglas y tests de apoyo:

- `src/ModuloVentas/Servicios/VentaListaPrecioPrioridadPolicy.java:37-74`; `test/ModuloVentas/Servicios/VentaListaPrecioPrioridadPolicyTest.java`.
- `src/ModuloVentas/Vistas/FormVenta.java:3413-3575`, `:2267-2281` y `:1916-1962`; tests `FormVentaListaPrecioAutomaticaWiringTest` y `FormVentaListaPrecioPrioridadPolicyTest`.
- `src/ModuloVentas/Vistas/FormVenta.java:2298-2302` y `src/ModuloVentas/Vistas/PrecioBultoVentaPolicy.java:33-39`: condición de igualdad de precio antes de consolidar.
- `src/ModuloConfiguracion/Servicios/TurnoListaPrecioHorarioPolicy.java:12-66`, `src/ModuloConfiguracion/Entidades/Turno.java:207-237`; tests `TurnoListaPrecioHorarioPolicyTest` y `TurnoListaPrecioConsultaPolicyTest`.
- `src/ModuloProveedores/Entidades/ListaPrecio.java:240-287`; `ListaPrecioDetalle.java:1310-1327,1402-1433`.
- `src/ModuloVentas/Entidades/TicketVenta.java:2974-3045,3207-3235`; tests `TicketVentaListaPrecioOfertaPolicyTest` y `TicketVentaPresupuestoCotizacionTest`.
- `src/ModuloRestobar/Vistas/formTicket.java:348-362,2220-2264,5288-5325,5571-5652`.

Los tests fuente descubren reglas y riesgos; no sustituyen las acciones del usuario ni la evidencia del laboratorio.
