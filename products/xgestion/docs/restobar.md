# Restobar: pedidos, opciones, recetas y seguimiento

Hay **40 fichas documentadas**, `XG-RES-001..040`, todas **`planned`**: ninguna tiene automatización, seed de Restobar ni validación real sobre un JAR. Las referencias R01–R20 del [roadmap](roadmap.md) se vinculan a estas fichas; no son otros veinte casos. El [Excel general](../../../docs/coverage/xgestion-cobertura.xlsx) incorpora cada ID una vez aunque tenga varios grupos.

El recorrido se organiza por lo que hacen mozos, cajeros y supervisores. Los botones y clases sirven para trazabilidad; no determinan por sí solos la cobertura. Las fórmulas de ofertas de FormVenta ya tienen su batería PRM. Aquí se registran los riesgos propios de una cuenta de Restobar: personalizaciones, ingredientes, rondas, persistencia antes de cobrar y ocupación de mesas.

## Consultar los grupos

Desde la raíz del repositorio:

```text
qa.cmd list --product xgestion --group restobar
qa.cmd list --product xgestion --group restobar-opciones
qa.cmd list --product xgestion --group restobar-recetas
qa.cmd list --product xgestion --groups
```

Estos comandos permiten consultar fichas. Los grupos que solo contienen pendientes no se ofrecen como ejecutables ni muestran casos aprobados. Cada futura automatización deberá respetar INFO como resumen, DEBUG como pasos visibles y TRACE como diagnóstico saneado, conservando detalles de fallos en todos los niveles.

## Orden de implementación

| Lote | Casos | Resultado para QA | Dependencia |
| --- | --- | --- | --- |
| 1. Cuenta y correcciones | RES-001..005, 013, 020, 026..028, 037 | Abrir, editar, retomar, cobrar y consultar sin perder o mezclar cuentas. | Salón sintético, cobro local y controles accesibles calibrados. |
| 2. Personalizaciones e ingredientes | RES-006..012, 014..019, 021 | Elegir extras, cancelar y consumir exactamente los ingredientes vendidos. | Carta con opciones/recetas, seed pendiente y oráculos por consumo. RES-015 es P0. |
| 3. Condiciones comerciales y recuperación | RES-029, 038, 040 | Crédito, descuentos globales y cierre consistente ante un error. | Clientes/límites y laboratorio de fallos controlados. |
| 4. Cocina y comprobantes impresos | RES-022..025, 032, 039 | Comandas, rondas, precuenta y estados reales del receptor. | KDS y salidas de impresión QA. |
| 5. Canales y dispositivos | RES-030..031, 033..036 | Fiscal de pruebas, reparto, mozos/QR, concurrencia y balanza. | Paquetes y aislamiento específicos; no basta con reconectar la VM offline. |

Los lotes expresan dependencias, no fechas ni una aceptación cumplida. Un escenario no se marca implementado por disponer del selector, ni validado por pasar un dry-run.

## Mapa de escenarios

| ID | Recorrido | Prioridad | Referencia |
| --- | --- | --- | --- |
| [XG-RES-001](../scenarios/restobar/XG-RES-001.md) | Abrir mostrador, cobrar y comenzar otro pedido | P0 | R01 |
| [XG-RES-002](../scenarios/restobar/XG-RES-002.md) | Abrir una mesa con cubiertos y retomar su cuenta | P0 | R02 |
| [XG-RES-003](../scenarios/restobar/XG-RES-003.md) | Cancelar los cubiertos y recuperar una mesa libre | P0 | R02 |
| [XG-RES-004](../scenarios/restobar/XG-RES-004.md) | Encontrar platos por código, búsqueda y familia | P1 | R03 |
| [XG-RES-005](../scenarios/restobar/XG-RES-005.md) | Editar cantidad y notas del consumo elegido por teclado | P0 | R04, R06 |
| [XG-RES-006](../scenarios/restobar/XG-RES-006.md) | Elegir opciones descriptivas sin alterar el precio del plato | P1 | R04 |
| [XG-RES-007](../scenarios/restobar/XG-RES-007.md) | Agregar extras con precio y conservar la cantidad de platos | P0 | R04 |
| [XG-RES-008](../scenarios/restobar/XG-RES-008.md) | Usar multiplicadores de extras sin arrastrarlos al próximo agregado | P1 | R04 |
| [XG-RES-009](../scenarios/restobar/XG-RES-009.md) | Cancelar la personalización de un plato nuevo sin dejar extras | P0 | R04 |
| [XG-RES-010](../scenarios/restobar/XG-RES-010.md) | Guardar cambios de opciones sobre un consumo existente | P0 | R04 |
| [XG-RES-011](../scenarios/restobar/XG-RES-011.md) | Cancelar opciones y cancelar el editor restaurando el consumo | P0 | R04 |
| [XG-RES-012](../scenarios/restobar/XG-RES-012.md) | Mantener separados platos con personalizaciones diferentes | P0 | R04 |
| [XG-RES-013](../scenarios/restobar/XG-RES-013.md) | Eliminar un consumo con autorización aceptada o rechazada | P0 | R07 |
| [XG-RES-014](../scenarios/restobar/XG-RES-014.md) | Descontar los ingredientes de una receta según los platos cobrados | P0 | Recetas |
| [XG-RES-015](../scenarios/restobar/XG-RES-015.md) | Consumir extras una sola vez con varios platos y distinto orden | P0 | Recetas |
| [XG-RES-016](../scenarios/restobar/XG-RES-016.md) | Quitar ingredientes de una receta respetando su límite | P0 | Recetas |
| [XG-RES-017](../scenarios/restobar/XG-RES-017.md) | Respetar la receta vigente al validar exclusiones y compatibilidad | P1 | Recetas |
| [XG-RES-018](../scenarios/restobar/XG-RES-018.md) | Crear y corregir una receta y utilizarla en el próximo pedido | P1 | Recetas |
| [XG-RES-019](../scenarios/restobar/XG-RES-019.md) | Anular un pedido cobrado con receta y extras sin duplicar devolución | P0 | Recetas |
| [XG-RES-020](../scenarios/restobar/XG-RES-020.md) | Cambiar cliente y mozo sin mezclar cuentas | P1 | R05 |
| [XG-RES-021](../scenarios/restobar/XG-RES-021.md) | Cambiar lista y medio de pago preservando extras del plato | P1 | R05 |
| [XG-RES-022](../scenarios/restobar/XG-RES-022.md) | Enviar la primera comanda con platos, extras y notas | P0 | R08 |
| [XG-RES-023](../scenarios/restobar/XG-RES-023.md) | Enviar nuevas rondas y reimprimir sin duplicar consumos | P0 | R09 |
| [XG-RES-024](../scenarios/restobar/XG-RES-024.md) | Pedir precuenta, cancelar el menú y continuar consumiendo | P0 | R10 |
| [XG-RES-025](../scenarios/restobar/XG-RES-025.md) | Distribuir la impresión por comensal conservando una sola cuenta | P1 | R11 |
| [XG-RES-026](../scenarios/restobar/XG-RES-026.md) | Trasladar la cuenta a una mesa libre y rechazar destino ocupado | P0 | R12 |
| [XG-RES-027](../scenarios/restobar/XG-RES-027.md) | Cancelar el cobro de la mesa y retomarlo | P0 | R13 |
| [XG-RES-028](../scenarios/restobar/XG-RES-028.md) | Cobrar la mesa y abrir otra cuenta sin arrastrar consumos | P0 | R13 |
| [XG-RES-029](../scenarios/restobar/XG-RES-029.md) | Enviar la cuenta a crédito y recuperar un rechazo por límite | P0 | R14 |
| [XG-RES-030](../scenarios/restobar/XG-RES-030.md) | Emitir factura de un pedido sin repetir cierre ni emisión | P0 | R15 |
| [XG-RES-031](../scenarios/restobar/XG-RES-031.md) | Gestionar delivery separando reparto y cobro | P1 | R16 |
| [XG-RES-032](../scenarios/restobar/XG-RES-032.md) | Cobrar un autopedido impago y habilitar su envío a cocina | P0 | R17 |
| [XG-RES-033](../scenarios/restobar/XG-RES-033.md) | Recibir una ronda de mozo y tolerar retransmisión | P0 | R18 |
| [XG-RES-034](../scenarios/restobar/XG-RES-034.md) | Proteger una mesa cuando llega otra ronda durante el cobro | P0 | R19 |
| [XG-RES-035](../scenarios/restobar/XG-RES-035.md) | Recibir pedidos QR con opciones válidas y política de pago | P0 | R20 |
| [XG-RES-036](../scenarios/restobar/XG-RES-036.md) | Cargar un producto pesable y recuperarse de una lectura fallida | P1 | R06 |
| [XG-RES-037](../scenarios/restobar/XG-RES-037.md) | Consultar pedidos cerrados o anulados sin modificarlos | P0 | Históricos |
| [XG-RES-038](../scenarios/restobar/XG-RES-038.md) | Calcular descuentos globales sobre los consumos ya descontados | P1 | Importes |
| [XG-RES-039](../scenarios/restobar/XG-RES-039.md) | Seguir estados de cocina sin confundirlos con mesa y cobro | P1 | Cocina |
| [XG-RES-040](../scenarios/restobar/XG-RES-040.md) | Recuperar un cierre fallido conservando cuenta, ingredientes y pago | P0 | Recuperación |

## Opciones del menú y sus recorridos

| Acción visible en la fuente | Escenarios | Qué se comprueba |
| --- | --- | --- |
| F1 Platos; código; búsqueda de familias | RES-004..009, 012, 036 | Identidad, cantidades, opciones y recuperación de una búsqueda/lectura fallida. |
| Editar / Ctrl+E; Eliminar | RES-005, 010..013, 037 | Consumo correcto, guardar/cancelar, autorización y bloqueo de históricos. |
| F2 Cliente / F3 Mozo o Cadete | RES-020, 029, 031 | Asignación, cancelación, deuda y responsable de la entrega. |
| F4 Cerrar e imprimir | RES-024, 027 | Cerrar, precuenta y cancelación son acciones distintas; no arrastrar la elección anterior. |
| F5 Cerrar | RES-001, 027..028, 040 | Confirmación única, recuperación y liberación de mesa. |
| F6 Factura electrónica | RES-030 | Tipo de acción, validación y trazabilidad fiscal de homologación. |
| F8 Cuenta corriente | RES-029 | Cliente/límite, deuda única y conservación ante rechazo. |
| F9 Dividir Ticket | RES-025 | Distribución de impresión por comensal; no equivale a separar pagos o cuentas. |
| F10 Lista de precios / F12 Forma de pago | RES-021, 038 | Condición seleccionada, extras y recálculo de importes. Prioridades de lista se detallan en su familia. |
| F11 Enviar a cocina | RES-022..023, 032, 039 | Primera comanda, nuevos/todos, restricción de impagos y estado del receptor. |
| Cambio de mesa desde salón | RES-026 | Origen ocupado, destino libre y rechazo de una mesa ocupada. |

Los atajos figuran en la fuente inspeccionada; la entrega del JAR y su Java Access Bridge todavía requieren calibración. Los botones dinámicos de opciones/platos y el mantenimiento de recetas necesitan revisión adicional de foco, nombre accesible y leyenda. No se resuelve esa dependencia con coordenadas fijas. Ver [backlog de accesibilidad](backlog-accesibilidad.csv).

## Batería fija propuesta para el próximo seed

Esta tabla es el **contrato de datos pendiente**, no un seed ejecutable. No reutilizar los IDs de ofertas ni insertar en una base compartida. El futuro builder debe reservar identidades propias, comprobar colisiones, pertenencia y restauración, y declarar qué perfil prepara cada caso.

| Familia | Datos sintéticos a preparar | Para qué sirven |
| --- | --- | --- |
| Salón | Mostrador, dos mesas libres/ocupadas, mesa de control, dos sectores, dos mozos y un supervisor. | Ciclo de cuenta, cubiertos, permisos, traslado y aislamiento. |
| Carta | Plato $1.000, bebida $500, productos similares, familias/subfamilias paginadas y producto ausente. | Búsqueda y selección correcta desde varias rutas. |
| Opciones | Descriptivas $0, extras de queso/salsa, opción inactiva, multiplicadores x2..x7 y notas diferentes. | Precio, cantidad de platos, cancelación en dos niveles y personalizaciones distintas. |
| Receta actual | Ingredientes stockeables, padre no stockeable, receta por cantidades fraccionarias y stock inicial conocido. | Consumo de receta, extras, cantidades múltiples y reversión. |
| Compatibilidad de receta | Solo actual, solo legacy, ambas con cantidades diferentes y ninguna. | Límite de exclusión de ingrediente; no equiparar los modelos de consumo. |
| Condiciones | Listas y medios manuales sin integración; clientes con/sin crédito y permisos separados. | Conservar extras al recalcular; cobro, deuda y autorización. |
| Operaciones previas | Cuenta abierta, precuenta emitida, primera comanda enviada, pedido cerrado y anulado. | Reapertura, rondas, protección histórica y no duplicación. |
| Laboratorio ampliado | KDS/impresoras, delivery, canal mozo, QR, fiscal sandbox y balanza. | Evidencia real del otro extremo y recuperación específica. |

El precio de cubierto y las preguntas de apertura se declaran por perfil. No se supone que stock insuficiente siempre bloquee: una batería adicional de stock debe fijar la configuración y respuesta esperadas. Para recetas, el consumo y las reservas previas se registran separadamente; la aprobación exige el delta final de lo efectivamente vendido, no solo el importe visible.

## Puntos que requieren cuidado al automatizar

- **Persistencia:** una cuenta abierta puede guardar consumos antes del cobro. Salir de la ventana no demuestra cancelación y no autoriza a esperar ausencia total de registros.
- **Tres estados:** cuenta abierta/cerrada/anulada, mesa libre/ocupada y preparación de cocina se comprueban por separado. Entregar o enviar a cocina no demuestra cobrar.
- **Opciones:** cantidad de extras y cantidad de platos son magnitudes distintas. Cancelar el picker nuevo, el picker de edición y el editor completo son rutas diferentes; RES-009/011 comprueban ausencia de residuos.
- **Recetas:** el mantenimiento actual usa productos/ingredientes; existe un fallback legacy para validar exclusiones. RES-017 verifica la prioridad del límite, sin prometer equivalencia del consumo legacy.
- **Ingredientes compartidos:** RES-015 compara varios renglones, cantidad 2 y órdenes A/B y B/A. La revisión de fuente detecta riesgo de repetir opciones durante el cierre; debe investigarse con el JAR antes de declararlo defecto. El oráculo calcula receta + extras desde la compra del usuario.
- **Impresión:** Nuevos, Todos, reimpresión y distribución por comensal pueden generar distintas salidas del mismo pedido. No deben crear otra venta ni acreditar cuentas/pagos independientes.
- **Concurrencia y QR:** el laboratorio fija el orden de aceptación/cierre y la política de pago. La ficha no inventa una aceptación cuando el canal debe rechazar y permitir reintento.
- **Resultado ambiguo:** consultar la identidad de la operación antes de repetir cobro, stock o emisión. Si falta evidencia, informar bloqueo, nunca aprobación por ausencia de error visible.

## Correspondencia con R01–R20

Los Rxx siguen siendo referencias del roadmap; las fichas formales son las únicas que se cuentan en el catálogo.

| Referencia | XG-RES | Alcance |
| --- | --- | --- |
| R01 | 001 | Mostrador y nueva cuenta |
| R02 | 002, 003 | Apertura, cubiertos y cancelación |
| R03 | 004 | Carta, búsquedas y familias |
| R04 | 005–012 | Cantidad, notas, opciones, extras y cancelaciones |
| R05 | 020, 021 | Cliente, mozo, lista y forma de pago |
| R06 | 005, 036 | Cantidad y balanza |
| R07 | 013 | Eliminar con autorización |
| R08 | 022 | Primera comanda |
| R09 | 023 | Rondas y reimpresión |
| R10 | 024 | Precuenta y menú de cierre |
| R11 | 025 | Impresión por comensal |
| R12 | 026 | Trasladar a mesa libre |
| R13 | 027, 028 | Cancelar/cobrar y liberar mesa |
| R14 | 029 | Cuenta corriente |
| R15 | 030 | Factura electrónica |
| R16 | 031 | Delivery |
| R17 | 032 | Autopedido impago |
| R18 | 033 | Ronda de mozo y retransmisión |
| R19 | 034 | Ronda durante el cobro |
| R20 | 035 | QR, opciones y pago |

RES-014..019 agregan la batería de recetas/ingredientes; RES-037..040 detallan histórico, descuentos globales, KDS y recuperación transaccional. No reemplazan los casos de precios ni las promociones ya documentadas.

## Trazabilidad técnica

Fuente inspeccionada: XGestion2 `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`.

- Cuenta y acciones: `src/ModuloRestobar/Vistas/formTicket.java`, `formTicketDetalle.java`, `formSalon.java`, `formCambiaMesa.java`, `formDividirTicket.java` y `formDelivery.java`.
- Opciones y receta: `src/Utilidades/Pickers/FormProductoOpcionesPicker.java`, `src/ModuloRestobar/DAO/VentaOpcionDAO.java`, `src/ModuloProductos/Vistas/FormReceta.java`, `src/ModuloProductos/Entidades/ProductoHijo.java` y `src/ModuloVentas/Entidades/TicketVenta.java`.
- RES-018 usa Escape para descartar la edición de receta: `FormReceta.java:48–53`; Guardar en 112–124 y confirmación de eliminación en 128–132. No se presupone un botón Cancelar en esa pantalla.
- Riesgos descubiertos mediante tests: `FormTicketDescuentosGlobalesTest`, `FormTicketSeleccionRenglonTest`, `FormTicketMesaLifecyclePolicyTest`, `RestobarAccesibilidadSourceGuardTest`, `SeleccionOpcionCierreMesaTest`, `KDSReglasTest`, `KDSServiceTest`, `MesaCierreProteccionTest` y `QrMesaOpcionesTest`. Cada ficha lista sus rutas completas relativas al ERP.

Esta referencia documenta las reglas y riesgos leídos, no una prueba sobre el artefacto. Cuando se implemente una ficha, actualizar estado/test, seed y perfil, grupo, controles accesibles, oráculos y matriz; registrar por separado JAR/SHA256, paquete y resultados reales. Seguir [nuevas features](../../../docs/nuevas-features.md).
