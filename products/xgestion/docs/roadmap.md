# Roadmap de QA de XGestion

Este mapa organiza la cobertura por lo que hace una persona en XGestion: primero vender, luego administrar lo vendido y después trabajar en Restobar. Describe las familias observadas y sus variantes; no promete probar todas las combinaciones posibles del ERP.

La [cobertura actual](cobertura.md) distingue automatización disponible, escenarios planificados y evidencia real. Hoy hay catorce casos implementados, incluidos los nueve de Venta cotidiana, y ninguna ficha `planned` en el catálogo actual de XGestion. El backlog funcional de las siguientes etapas permanece pendiente. La ejecución real sobre el JAR sigue pendiente. XPORTAL, Mozos Flutter y Consultador conservan su onboarding independiente.

## Cómo leer y mantener el mapa

- **P0:** recorrido cotidiano o riesgo de perder/duplicar una venta, un cobro o datos. **P1:** regla comercial o variante frecuente. **P2:** integración, dispositivo o configuración especializada. La prioridad no reemplaza sus dependencias.
- Cada variante que se incorpore debe declarar configuración, datos, resultado y evidencia propios. No extrapolar una prueba en efectivo a todas las formas de pago ni una configuración a todas las instalaciones.
- Antes de ampliar automatización se necesitan grupos comprensibles, logs útiles y un paquete QA reproducible. Las etapas se aceptan con evidencia del producto, no con el número de fichas o tests unitarios.
- Recuperación es transversal: en cada etapa incluir cancelar, corregir, reintentar y volver a operar cuando correspondan. No esperar a la última etapa para comprobar esos recorridos.
- Para cada familia considerar camino exitoso, rechazo, cancelación, límites y recuperación; configuración habilitada/deshabilitada; roles; operación nueva, reabierta e histórica. Seleccionar combinaciones por riesgo: promoción/descuento/pago, moneda/presupuesto/reapertura, cantidad/stock y mesa/ronda/cobro. Documentar cuáles se eligieron y cuáles quedan pendientes, sin prometer todas las combinaciones.
- Los grupos se registran en `products/xgestion/groups.json`. Un caso puede estar en varios grupos y se cuenta una sola vez en el catálogo general. La numeración del menú es una ayuda temporal; el ID estable es el nombre del grupo o escenario.

## Etapa 0 — Preparación y ejecución comprensible

**Prioridad P0.** QA instala el entorno, reconoce qué puede ejecutar, elige un grupo y entiende el resultado.

Alcance: Windows y escritorio exclusivos, paquete privado, licencia QA válida offline, base aislada, restauración, acceso, consultas de productos y selectores calibrados para el JAR. Grupos iniciales: `smoke`, `regression`, `inicio`, `autenticacion`, `productos`.

El menú debe mostrar nombre, descripción y cantidades de casos implementados, planificados y manuales. `qa.cmd list --product xgestion --groups` resume grupos; `qa.cmd list --product xgestion --group ventas` muestra sus casos. Un grupo sin automatización es visible y explica por qué todavía no puede ejecutarse.

`qa.cmd run --product xgestion --group ventas --log-level INFO` es la salida habitual. INFO muestra cada caso y el resumen; DEBUG añade pasos y comprobaciones; TRACE añade diagnóstico técnico saneado. Los fallos siempre informan caso, paso, esperado, observado, categoría y evidencia disponible. Si no hay prueba de la causa, se declara **causa no determinada**.

**Dependencias:** paquete autorizado y calibración para aceptación real. **Aceptación:** instalación reproducible; catálogo actual identificado, incluidos los siete casos iniciales; filtros coherentes; logs revisados con datos sintéticos sensibles; controles técnicos aprobados y tres regresiones reales consecutivas en el laboratorio. Los controles técnicos pueden completarse antes del paquete, pero no acreditan esta aceptación real.

## Etapa 1 — Venta cotidiana

**Prioridad P0.** El vendedor carga, corrige, cobra o abandona una venta y puede continuar con la siguiente.

Perfil inicial: venta local no fiscal en ARS, producto a $1.000 por unidad, cantidad 2 y total $2.000; efectivo exacto o recibido $3.000 con vuelto $1.000; `cartelPagoVuelto=true`, sin autorización de supervisor para abandonar. Sin promociones, descuentos, fidelización, integración de pagos ni impresión. Stock suficiente y datos saneados conocidos.

| ID | Recorrido | Estado |
| --- | --- | --- |
| [XG-VEN-001](../scenarios/ventas/XG-VEN-001.md) | Cobrar en efectivo el importe exacto. | Implementado; E2E real pendiente |
| [XG-VEN-002](../scenarios/ventas/XG-VEN-002.md) | Abandonar una venta sin cobrarla. | Implementado; E2E real pendiente |
| [XG-VEN-003](../scenarios/ventas/XG-VEN-003.md) | Cargar un producto y modificar su cantidad. | Implementado; E2E real pendiente |
| [XG-VEN-004](../scenarios/ventas/XG-VEN-004.md) | Buscar un código inexistente sin alterar la venta. | Implementado; E2E real pendiente |
| [XG-VEN-005](../scenarios/ventas/XG-VEN-005.md) | Cobrar en efectivo con vuelto. | Implementado; E2E real pendiente |
| [XG-VEN-006](../scenarios/ventas/XG-VEN-006.md) | Cancelar el cobro, retomarlo y cobrar una sola vez. | Implementado; E2E real pendiente |
| [XG-VEN-007](../scenarios/ventas/XG-VEN-007.md) | Rechazar el abandono y continuar vendiendo. | Implementado; E2E real pendiente |
| [XG-VEN-008](../scenarios/ventas/XG-VEN-008.md) | Comenzar otra venta después de cobrar. | Implementado; E2E real pendiente |
| [XG-VEN-009](../scenarios/ventas/XG-VEN-009.md) | Comenzar otra venta después de abandonar. | Implementado; E2E real pendiente |

Grupos: `ventas`, `carga-productos`, `corregir-venta`, `efectivo`; los recorridos de cobro también pueden pertenecer a `cobros`. Las fichas detallan pasos y resultados; su campo `test` identifica la automatización disponible. Los casos planificados conservan su criterio sin generar un resultado Robot.

Los casos XG-VEN-003 a XG-VEN-009 requieren el contrato privado `sales_journeys`: aviso de código ausente, grilla y defaults observados, diálogo de efectivo y controles de recuperación. VEN-008 observa el reinicio automático de la misma ventana; VEN-009 reabre desde la misma sesión. Los casos 003/007 abren el editor mediante doble clic autorizado sobre la celda localizada por JAB. La mejora de un atajo accesible sigue pendiente en el [backlog CSV](backlog-accesibilidad.csv), separado de los escenarios.

**Dependencias:** etapa 0; calibrar los controles adicionales antes de ejecutar cada caso nuevo. **Aceptación:** nueve casos de venta implementados y ejecutados individualmente y en su grupo, repetibles desde baseline; importes y efectos correctos, sin duplicados ni datos residuales. Hasta entonces se informa por caso lo disponible y lo pendiente.

## Etapa 2 — Productos y condiciones comerciales

**Prioridad P1; stock y coherencia de importes P0.** El vendedor selecciona el artículo correcto y aplica las condiciones del cliente y la operación.

| Familia / grupos | Variantes a desglosar | Riesgo / resultado a observar |
| --- | --- | --- |
| Carga: `carga-productos`, `corregir-venta` | Código y búsqueda; repetido; variantes padre/hijo; cancelar selección; cantidades previas, decimales, bultos e ingreso por importe. | Artículo, cantidad y unidad correctos; no vender el padre ni conservar entradas anteriores. |
| Existencias: `stock` | Disponible, insuficiente, repetido en varias líneas, sucursal; bloqueo habilitado/deshabilitado y reglas del cierre anual. | Aplicar la regla del perfil, sin presumir que siempre se bloquea stock negativo. |
| Precios: `precios` | Lista seleccionada, cliente, sucursal, turno y cantidad; cambio de lista; edición manual, vacío/cero y precisión. | Prioridad correcta, importe visible consistente y ausencia de cambios parciales al cancelar. |
| Ofertas: `promociones`, `descuentos` | Porcentaje, importe, cantidad y combos; vigencia/aplicabilidad; descuento de ítem/global, cambio de cliente y líneas con notas diferentes. | Recalcular una vez; no perder notas, duplicar beneficios ni superar la base permitida. |
| Impuestos e importes: `precios`, `comprobantes` | Inclusión/desglose según producto y documento; combinación con descuentos; precisión y redondeos en línea/total. | Explicar la composición del importe y conservarla al cobrar/reabrir; fiscalización real en etapa 6. |
| Fidelización: `descuentos` | Cliente identificado/consumidor final, saldo/vencimiento, uso parcial/total, límites y cambio de cliente. | Beneficio limitado al saldo/total; sin arrastre entre clientes o ventas. |

**Dependencias:** venta básica estable; fixtures y perfiles por configuración. **Aceptación:** matriz revisada de las reglas seleccionadas, datos independientes, totales y stock coherentes; cancelar/reintentar conserva el estado previsto. La lectura física de balanza se acepta en laboratorio de dispositivos, aunque la cantidad decimal pueda probarse antes.

## Etapa 3 — Cobros y documentos

**Prioridad P0 para dinero y duplicados; P1 para variantes.** El cajero cobra con la forma elegida o deja documentada la operación para después.

| Familia / grupos | Variantes a desglosar | Resultado / dependencia |
| --- | --- | --- |
| Cobro: `cobros`, `efectivo` | Diálogo habilitado/deshabilitado, exacto, vuelto, insuficiente, cancelar; pago simple/múltiple, parcial cuando el flujo lo permita, descuentos por pago. | Cierre y pagos una sola vez. No confundir pago parcial permitido con cerrar en efectivo por un importe insuficiente. Insuficiente se prueba con un perfil que permita ingresarlo; sin diálogo el cobro simple puede completarse automáticamente. |
| Monedas: `monedas` | ARS/USD en artículos, listas y moneda contable; cotización de empresa/venta válida, nula o no positiva; cambio autorizado, redondeos; alternar/editar/borrar importe pagado. | Mantener importe recibido y cotización de la operación; bloquear cambios inválidos sin mutación parcial. |
| Retomar: `presupuestos` | Guardar ARS/USD o cancelar; abrir venta/preventa/presupuesto; convertir a venta; abierta frente a cerrada/anulada. | No convertir dos veces ni recalcular snapshots históricos donde no corresponda. |
| Crédito: `cuenta-corriente` | Cliente, saldo/límite, autorización, anticipo, cuotas y recálculo del plan. | Cuenta correcta, sin financiar recargos dos veces; cancelar no deja efectos parciales. |
| Documentos: `comprobantes` | Tipo permitido, datos del cliente, consulta y relación con la operación original. | Coherencia entre documento, venta y pago. Emisión fiscal e impresión requieren etapa 6. |

**Dependencias:** etapas 1–2, perfiles de moneda/crédito y datos de clientes; no necesita habilitar servicios externos para los casos locales. **Aceptación:** reglas documentadas, importes y saldos contrastados y recuperación de cancelaciones; cierre fallido no deja venta/cobro/stock parciales. La simulación de fallas debe ser controlada, reproducible y exclusiva del laboratorio.

## Etapa 4 — Después de vender

**Prioridad P0 para saldos y permisos; P1 para consultas.** El usuario encuentra lo vendido, corrige mediante el procedimiento autorizado y reconcilia su caja.

Familias: consulta y reapertura permitida, devolución/anulación y vínculo con la venta original (`devoluciones`, `comprobantes`); movimientos, retiros/ingresos, arqueo y cierre de caja (`caja`); autorizaciones, rechazo y auditoría para eliminar/abandonar/modificar (`permisos`). Distinguir una devolución o anulación de borrar datos del sistema.

Variantes: parcial/total cuando la fuente y la UI confirmen soporte; comprobante/cobro previo; usuario autorizado/no autorizado; operación ya cerrada; repetición; caja/puesto/sucursal correctos. Las modalidades no confirmadas se mantienen como preguntas de diseño de la ficha, no como resultados inventados.

Comprobar explícitamente separación por **empresa, sucursal, puesto y operador**: consultar/corregir/cerrar debe afectar la operación y caja del contexto esperado. Preparar fixtures con identidades diferenciadas; no asumir aislamiento por probar solo una empresa con un usuario.

**Dependencias:** ventas y cobros aceptados, fixtures de operaciones previas y perfiles de permisos. **Aceptación:** trazabilidad al origen, saldos/stock/caja esperados, una sola corrección por acción y auditoría conservada; ninguna limpieza SQL para fabricar resultados.

## Etapa 5 — Restobar

**Prioridad P0 en cuenta y cobro; P1 en operación del salón.** Después de Venta se cubre el recorrido del mozo, cocina y cajero.

| Familia / grupos | Variantes observadas o por detallar | Límite de interpretación |
| --- | --- | --- |
| Mostrador y mesas: `mostrador`, `mesas` | Crear/retomar cuenta, mesa libre/ocupada, varios consumos y comensales; mover una cuenta a una mesa libre; cambio de sector. | Estado de la cuenta, estado de ocupación de la mesa y estado de cocina son dimensiones distintas. No inferir fusión con mesa ocupada. |
| Preparación: `preparacion`, `kds` | Agregar/corregir pedido, observaciones, envío y avance de preparación; repetir/cancelar según permiso. | Confirmar transiciones de cocina en su UI y en el dispositivo/sistema correspondiente. |
| Precuenta y cierre: `precuenta`, `cobros` | Revisar consumos, precuenta, comensales, cobrar y liberar la mesa. | Dividir la impresión por comensal no demuestra cobros independientes; diseñar ese caso solo tras verificar soporte. |
| Reparto: `delivery` | Pedido, cliente/dirección, preparación, entrega y cobro según flujo confirmado. | Precisar quién cobra, cuándo y cómo se recupera una cancelación. |
| Canales: `mozos-qr` | Origen mozo/QR, recepción en caja/cocina, modificación y duplicados. | La app Flutter tiene su propio producto y onboarding; no asumir que XMozo Angular es esa app. |

**Dependencias:** flujo de Venta aceptado, datos de salón/mesas/usuarios, selectores específicos de `formTicket.java`, y entorno de cocina/canales si se usan. **Aceptación:** recorridos completos desde pedido hasta cobro, estados diferenciados y consistentes, sin consumos duplicados; cualquier impresora o servicio externo se acepta con el laboratorio de etapa 6.

### Backlog de recorridos de Restobar

Los códigos **R01–R20 son referencias de planificación**, no escenarios del catálogo, tests implementados ni comandos ejecutables. Antes de crear cada ficha se deben precisar perfil, variantes y resultados con la UI de QA; por ahora solo Venta cotidiana tiene detalle paso a paso. R01–R13 priorizan salón/mostrador; R14–R20 agregan dependencias de crédito, servicios y concurrencia.

| Ref. | Recorrido de usuario y variantes que hay que cubrir | Prioridad / dependencia |
| --- | --- | --- |
| R01 | Abrir mostrador vacío, cargar productos y cobrar; revisar el tratamiento de intentar cerrar sin consumos. | P0; Venta cotidiana |
| R02 | Abrir mesa indicando cubiertos, salir y reabrir la misma cuenta; distinguir mesa ocupada de cuenta cerrada. | P0; datos de salón |
| R03 | Buscar platos por código, nombre o familia; elegir uno, buscar uno ausente y continuar. | P1; catálogo de carta |
| R04 | Personalizar un plato con agregados y notas; revisar precio y conservación de personalizaciones al editar/reabrir. | P1; carta con opciones |
| R05 | Cambiar cliente, mozo, lista y forma de pago; verificar condiciones aplicadas y contexto de la cuenta. | P1; perfiles comerciales |
| R06 | Agregar un producto pesable y corregir cantidad; una lectura fallida no debe convertirse en una venta de peso anterior o inventado. | P1; dispositivo real en etapa 6 |
| R07 | Eliminar un consumo con autorización requerida: aceptar, rechazar o cancelar; conservar el pedido cuando no se autoriza. | P0; roles QA |
| R08 | Enviar la primera comanda y revisar qué consumos llegan a preparación. | P0; cocina/KDS y salida de impresión si aplica |
| R09 | Agregar otra ronda y emitir Nuevos/Todos; verificar cantidades ya enviadas y nuevas sin duplicar consumos. | P0; primera comanda |
| R10 | Obtener una precuenta y continuar agregando consumos: la consulta/impresión no equivale a cobrar ni cerrar la cuenta. | P0; impresión en etapa 6 |
| R11 | Dividir la impresión por comensal y revisar distribución/importes. No acreditar cobros independientes con esta prueba. | P1; comensales e impresión |
| R12 | Trasladar una cuenta a una mesa libre y retomar allí los consumos; revisar origen/destino. Mesa ocupada requiere regla y caso propios, no inferir fusión. | P0; dos mesas |
| R13 | Cobrar una mesa y comprobar su liberación; cancelar antes de confirmar y continuar con la cuenta abierta. | P0; cobro simple |
| R14 | Enviar a cuenta corriente con cliente y límite; revisar rechazo/autorización y recuperación sin cierres parciales. | P0; etapa 3 |
| R15 | Solicitar factura electrónica del pedido y revisar aceptación/rechazo/reintento sin duplicar. | P0; laboratorio fiscal etapa 6 |
| R16 | Crear delivery, asignar cadete y pasar En proceso/En camino; comprobar entrega y cobro por separado. Estado de reparto no equivale a pagado. | P1; datos de reparto |
| R17 | Recibir un autopedido impago, cobrarlo y comprobar su habilitación/recepción en KDS según el flujo de QA. | P0; canal y KDS |
| R18 | Recibir una ronda desde mozo, retransmitir la misma y verificar que no duplica consumos ni comanda. | P0; canal mozo y etapa 6 para red |
| R19 | Recibir otra operación/ronda mientras se está cobrando; verificar protección del cierre y resultado consistente para ambos participantes. | P0; varios puestos, etapa 6 |
| R20 | Pedir por QR con prepago o pago al cierre; probar otra ronda/uso de una mesa ya ocupada y distinguir ronda, cuenta, pago y cocina. | P0; políticas QR, canal y pagos de QA |

Fuentes de diseño: `src/ModuloRestobar/Vistas/formTicket.java`, `formSalon.java`, `formDividirTicket.java`, `formCambiaMesa.java` y `formDelivery.java`; estados/reglas de preparación en `src/ModuloRestobar/Entidades/KDSEstado.java` y `KDSReglas.java`; coordinación de canales/cierre en `src/ModuloRestobar/AppMozo/MesaCierreProteccion.java`, `AppMozoRoundProcessor.java` y `QrMesaRoundProcessor.java`. La [matriz de fuentes](cobertura.md) identifica tests candidatos; su existencia no prueba estos recorridos de extremo a extremo.

## Etapa 6 — Integraciones y laboratorio ampliado

**Prioridad por impacto y disponibilidad del entorno; normalmente P2.** El usuario opera con sistemas y equipos reales de pruebas.

Grupos: `pagos-externos` (cuenta activa/inactiva, transferencia confirmada, QR/Point, cancelación, timeout, respuesta repetida); `fiscal` (datos del comprador, emisión/rechazo/reintento y documentos relacionados); `impresion` (vista previa y salida real por impresora/formato); `dispositivos` (balanza, lector, desconexión y lectura inválida); `varios-puestos` (operación concurrente, stock y caja por puesto); `compras` (abastecimiento y sus efectos cuando se amplíe el alcance). `recuperacion` atraviesa todas las etapas y aquí añade fallas de red/dispositivo y concurrencia.

**Dependencias:** entornos de prueba autorizados, dispositivos, fixtures y permisos propios. Requiere un diseño de aislamiento distinto del perfil inicial offline; no basta con reconectar esa VM. **Aceptación:** evidencia de extremo a extremo del servicio/dispositivo real de QA, idempotencia y recuperación verificadas. Un mock o un test unitario no acredita entrega a cocina, impresión física, pago confirmado ni emisión fiscal.

## Evidencia y trazabilidad

La fuente examinada corresponde a XGestion2 `release/189-lts`, referencia de inspección `f34238183d494259bed1279dd7d9aac0ce16a3ae`. Es trazabilidad del análisis, **no prueba de equivalencia con el JAR distribuido**. Registrar por separado commit del harness, versión y SHA-256 del JAR, paquete, perfil, IDs y reporte de cada ejecución. Los cambios posteriores de fuente requieren revisar las expectativas.

El inventario observado de **420 clases de tests** del producto es insumo para descubrir reglas, errores históricos y combinaciones. No significa 420 escenarios E2E ni cobertura de 420 recorridos de usuario. Ver [mapa de fuentes y evidencia](cobertura.md) y [referencias](referencias.md).

Cada ampliación sigue [nuevas features](../../../docs/nuevas-features.md): decidir la variante, escribir la ficha, preparar datos, implementar/calibrar, ejecutar y actualizar cobertura. No se fijan fechas ni se marca una etapa completa por haber escrito su documentación.
