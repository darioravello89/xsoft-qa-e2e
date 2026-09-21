# Cobertura y evidencia de XGestion

La cobertura se expresa por recorridos de usuario y por evidencia obtenida. Un grupo puede mostrar capacidades futuras aunque todavía no tenga automatización. Consultar el [roadmap por etapas](roadmap.md) para el alcance y las dependencias.

## Estado actual

| Capa | Disponible | Qué demuestra |
| --- | --- | --- |
| Catálogo | 14 fichas: 7 `implemented` y 7 `planned`; 0 `manual`. | Objetivos, datos y resultados documentados. |
| Automatización | 7 casos Robot implementados. | Existe código ejecutable y comprobaciones definidas. |
| Datos comerciales | [Seed opcional](seed.md): 48 artículos, 19 ofertas, 5 listas y 26 ejemplos de cálculo pendientes de validar. | Datos reproducibles para ampliar los escenarios; no suma casos automatizados. |
| Casos nuevos de Venta | XG-VEN-003 a XG-VEN-009, sin `.robot`. | Plan detallado; no se ejecutan ni se reportan como PASS. |
| Controles del repositorio | Lint, tests del framework, catálogo y dry-run. | Coherencia técnica; registrar el resultado de cada ejecución. |
| Producto real | Pendiente de paquete privado, calibración y ejecución. | Todavía no acredita acceso, venta ni recuperación en el JAR. |

`implemented` no significa validado en el producto; `planned` no significa fallado. Un caso `manual` describe un procedimiento sin automatización ejecutable y necesita su propia evidencia. Ninguno cambia a aprobado por pertenecer a un grupo.

## Casos y grupos

| Caso | Qué comprueba para QA | Implementación | E2E real |
| --- | --- | --- | --- |
| [XG-INI-001](../scenarios/inicio/XG-INI-001.md) | Aparece la pantalla de acceso. | Disponible | Pendiente |
| [XG-AUT-001](../scenarios/autenticacion/XG-AUT-001.md) | Se rechaza un acceso inválido y se limpian los campos. | Disponible | Pendiente |
| [XG-AUT-002](../scenarios/autenticacion/XG-AUT-002.md) | El usuario accede al contexto QA correcto. | Disponible | Pendiente |
| [XG-PRO-001](../scenarios/productos/XG-PRO-001.md) | Un código conocido devuelve el producto esperado. | Disponible | Pendiente |
| [XG-PRO-002](../scenarios/productos/XG-PRO-002.md) | Un código ausente no devuelve productos. | Disponible | Pendiente |
| [XG-VEN-001](../scenarios/ventas/XG-VEN-001.md) | Se cobra una venta no fiscal en efectivo. | Disponible | Pendiente |
| [XG-VEN-002](../scenarios/ventas/XG-VEN-002.md) | Abandonar no registra una venta ni modifica stock/caja. | Disponible | Pendiente |
| [XG-VEN-003](../scenarios/ventas/XG-VEN-003.md) | Se modifica la cantidad cargada. | Planificada | Pendiente |
| [XG-VEN-004](../scenarios/ventas/XG-VEN-004.md) | Un código inexistente no altera la venta. | Planificada | Pendiente |
| [XG-VEN-005](../scenarios/ventas/XG-VEN-005.md) | Se cobra con vuelto. | Planificada | Pendiente |
| [XG-VEN-006](../scenarios/ventas/XG-VEN-006.md) | Se cancela y retoma el cobro sin duplicarlo. | Planificada | Pendiente |
| [XG-VEN-007](../scenarios/ventas/XG-VEN-007.md) | Se rechaza el abandono y se continúa. | Planificada | Pendiente |
| [XG-VEN-008](../scenarios/ventas/XG-VEN-008.md) | La siguiente venta después de cobrar comienza limpia. | Planificada | Pendiente |
| [XG-VEN-009](../scenarios/ventas/XG-VEN-009.md) | La siguiente venta después de abandonar comienza limpia. | Planificada | Pendiente |

Los conteos vivos salen del catálogo: `qa.cmd list --product xgestion --groups`. Hoy `smoke` tiene cinco casos implementados y `regression` siete; `ventas` contiene dos implementados y siete planificados. Un escenario puede pertenecer a varios grupos: no sumar sus conteos como si fueran casos diferentes. Los tags iniciales se conservan para no alterar selecciones existentes.

XG-VEN-001 agrega `efectivo` y `cobros` a sus tags previos: ambas familias muestran una automatización disponible. El backlog R01–R20 de Restobar es una matriz de planificación fuera del catálogo; no se suma a las 14 fichas ni al denominador de automatización.

## Matriz funcional y variantes

La matriz funcional permite decidir la próxima ampliación. **Parcial** significa que existe alguna automatización de esa familia, no que estén verificadas sus variantes. Todos los recorridos de producto de esta matriz mantienen E2E real pendiente.

| Familia | Variantes incluidas en el mapa | Estado de automatización / siguiente paso |
| --- | --- | --- |
| Preparación/acceso | Inicio, credenciales inválidas/válidas, empresa/sucursal/usuario. | Parcial: XG-INI-001, XG-AUT-001/002. Aceptación real y perfiles pendientes. |
| Consultar productos | Conocido/ausente en listado. | Parcial: XG-PRO-001/002; no cubre carga en venta. |
| Cargar/corregir venta | Cantidad, código ausente, conservar líneas y continuar. | Carga básica incluida en VEN-001/002; variantes VEN-003/004/007 planificadas. |
| Efectivo/cancelación | Exacto, vuelto, cancelar/retomar, abandono y operación siguiente. | VEN-001/002 disponibles; VEN-005/006/008/009 planificados. |
| Cantidades/stock | Decimales, bultos, importe, repetidos, variantes padre/hijo, suficiente/insuficiente, bloqueo on/off. | Variantes pendientes; la venta básica solo comprueba su delta de stock. |
| Precios/promociones | Listas por cliente/sucursal/turno/cantidad, porcentaje/importe/cantidad/combos, vigencia y aplicabilidad. | Pendiente de fichas y perfiles. |
| Descuentos/impuestos | Ítem/global/pago, redondeos/desglose, notas, puntos y combinaciones. | Pendiente; el perfil inicial evita estos efectos. |
| Monedas | ARS/USD, cotización válida/inválida, moneda contable, cambio de importe/moneda y redondeos. | ARS simple disponible; variantes pendientes. |
| Cobros/crédito | Simple/múltiple, parcial permitido, insuficiente, cuenta corriente/límite, cuotas y anticipo. | Efectivo simple disponible; demás variantes pendientes. |
| Presupuestos/documentos | Guardar/cancelar, moneda, nueva/reabierta/histórica, conversión y tipo de comprobante. | No fiscal inicial disponible; familias adicionales pendientes. |
| Después de vender | Consulta, devolución/anulación, caja/arqueo/cierre, autorizaciones y auditoría. | Pendiente; separar empresa/sucursal/puesto/operador. |
| Restobar salón/mostrador | Cuenta, cubiertos, platos, personalización, mozo, comanda/rondas, precuenta/comensal y traslado/cierre. | Backlog R01–R13; sin fichas ejecutables. |
| Restobar canales | Crédito/FE, delivery/cadete, autopedido/KDS, mozo/QR, retransmisión y concurrencia. | Backlog R14–R20; servicios y laboratorio pendientes. |
| Servicios/dispositivos | Pagos externos, fiscal, impresión, balanza/lector y fallas de conexión. | Pendiente de entornos/equipos autorizados. |
| Ampliación operativa | Varios puestos y compras/abastecimiento. | Mapa pendiente de fichas específicas y datos. |
| Recuperación transversal | Rechazar, cancelar, corregir/reintentar, límites y fallas sin datos parciales/duplicados. | Abandono simple disponible; recuperación restante pendiente por familia. |

Cada ampliación selecciona combinaciones de alto riesgo de promoción/descuento/pago, moneda/presupuesto/reapertura, cantidad/stock y mesa/ronda/cobro. Incluir camino exitoso, rechazo, cancelación, límites y recuperación, con config on/off y roles que correspondan. Esta matriz no afirma cobertura cartesiana exhaustiva.

## Acreditar un caso real

1. Preparar el paquete legítimo y el perfil exacto de configuración/datos de la ficha.
2. Calibrar controles sobre el SHA-256 del JAR, sin inferir selectores desde nombres Java.
3. Ejecutar acciones de usuario y comprobar resultados visibles, incluidos los pasos de recuperación.
4. En ventas, contrastar los efectos con el anexo de evidencia de la ficha; no corregir datos mediante SQL.
5. Registrar resultado, versión/hash JAR, manifest del paquete, perfil, ID, paso, esperado/observado y ruta privada de evidencia.
6. Repetir de forma independiente y dentro del grupo para detectar dependencias entre casos. La aceptación inicial requiere tres regresiones reales consecutivas.

No afirmar causa de un fallo solo por su categoría. Por ejemplo, un control no encontrado puede ser un selector desactualizado, una pantalla distinta o un bloqueo previo del producto. Si la evidencia no permite decidir, informar **causa no determinada**.

## Fuente examinada como insumo

Referencia del análisis: repositorio XGestion2, rama `release/189-lts`, commit `f34238183d494259bed1279dd7d9aac0ce16a3ae`. Las rutas siguientes son relativas a ese repositorio; las líneas son ayudas de navegación de la inspección y pueden cambiar. La fuente ayuda a diseñar expectativas y perfiles, pero no acredita que el JAR tenga ese código ni que los recorridos se hayan ejecutado.

| Familia | Fuente de comportamiento | Tests relevantes como insumo |
| --- | --- | --- |
| Carga/cantidad/variantes | `src/ModuloVentas/Vistas/FormVenta.java`: carga, `setProducto`, selección de variante; `FormVentaDetalle.java`. | `test/ModuloVentas/Vistas/FormVentaProductoCantidadPolicyTest.java`, `FormVentaCantidadPreviaTecladoTest.java`, `PrecioBultoVentaPolicyTest.java`, `FormVentaSeleccionVarianteWiringTest.java`. |
| Notas/listas/ofertas | `FormVenta.java`: consolidación, selección y recálculo de lista/ofertas. | `FormVentaNotasConsolidacionWiringTest.java`, `FormVentaListaPrecioPrioridadPolicyTest.java`, `FormVentaReaperturaOfertasPolicyTest.java`. |
| Descuentos/precio | `FormVentaDetalle.java`, cálculo de totales. | `FormVentaDescuentosGlobalesTest.java`, `FormVentaDetalleDescuentoOfertaPolicyTest.java`, `FormVentaDetallePrecioUnitarioTest.java`. |
| Cotización/presupuestos | `FormVenta.java:3061` carga protegida de cotización; `:4978` moneda del presupuesto; `:6370` validación antes de guardar. | `FormVentaCotizacionCargaTest.java`, `FormVentaCotizacionQa3Test.java`, `FormVentaDetalleCotizacionQa3Test.java`, `FormVentaPresupuestoMonedaPolicyTest.java`. |
| Cobro simple | `FormVenta.java:6041` diálogo según `cartelPagoVuelto`; `:6532` pago automático; `:6541` validación de cobro. | `FormVentaCierreCobroPolicyTest.java`. |
| Cobro multimoneda/múltiple | `src/ModuloVentas/Vistas/Dialogs/formTicketCierre.java`: importe recibido, vuelto, moneda y pagos. | `test/ModuloVentas/Vistas/Dialogs/FormTicketCierreMonedaStateTest.java`, `FormTicketCierreCobroMultiplePolicyTest.java`. |
| Crédito/cuotas | `FormVenta.java:5910` cliente de cuenta corriente y `:6083` límite; `Dialogs/DialogVentaCuotas.java`. | `FormVentaCierreCuentaCorrientePolicyTest.java`, `Dialogs/CuotasDialogMonedaTest.java`, tests de persistencia y moneda de cuotas. |
| Stock/recuperación | `FormVenta.java:5930` acumulación de stock al cerrar existente; `:6391` rollback; `:6422` restauración; `:6568` verificación de persistencia. | Tests de cierre, persistencia y rollback del producto. Exigen además un escenario real con falla controlada. |
| Abandono/nueva venta | `FormVenta.java:648` confirmación; `:681` supervisor; `:709` auditoría; `:4399` y `:4448` inicio limpio. | Tests de auditoría y políticas de venta; completar evidencia del recorrido visible. |
| Fidelización | `FormVenta.java:6781` visibilidad/cliente; `:6867` uso de puntos y límites. | Requiere fixtures de saldo/vencimiento y fichas propias; no cubierto por venta básica. |
| Restobar | `formTicket.java` y diálogos de mesa/cuenta/preparación. | Tests de políticas, estados y wiring relacionados; seleccionar por recorrido, no convertir cada clase en un E2E. |
| Servicios/dispositivos | `Dialogs/formTicketCierre.java` para MP; FormVenta para FE/balanza; impresión y cocina. | `MercadoPagoCobroConfirmadoPolicyTest.java`, `MercadoPagoQrFlowPolicyTest.java`, `FormVentaBalanzaLifecyclePolicyTest.java`. |

El inventario de **420 clases de tests** inspeccionado es una fuente de reglas y riesgos, no 420 E2E. Hay pruebas de políticas, inspección de texto fuente y ejecución de métodos/listeners sin ventana ni base; por ejemplo `FormTicketCierreMonedaStateTest` explicita esa limitación. No se ejecutaron esos tests ni la aplicación como parte del análisis del roadmap.

### Insumos concretos para crédito, caja y stock

Los nombres siguientes son rutas existentes en XGestion2. Ayudan a seleccionar variantes al escribir las fichas; no se atribuye cobertura E2E a su sola existencia.

| Familia | Tests fuente / documentación de negocio |
| --- | --- |
| Límite y saldo de cuenta corriente | `test/ModuloFinanzas/Entidades/LimiteCuentaCorrientePolicyTest.java`, `LimiteCuentaCorrienteServiceTest.java`, `CuentaCorrienteSaldoServiceTest.java`, `CuentaCorrienteMontoFinalCalculadorTest.java`, `CuentaCorrienteMonedaResumenTest.java`. |
| Anulación con cuenta corriente | `test/ModuloVentas/Entidades/TicketVentaAnulacionCuentaCorrienteTest.java`; compila fragmentos de producción y simula JDBC, no prueba el JAR con MySQL. |
| Caja/turno/medios | `test/ModuloVentas/Entidades/CajaSaldoDisponibleServiceTest.java`, `CajaValoresEsperadoPorPagoTest.java`, `TurnoCajaSqlBuilderTest.java`. |
| Cierre y reimpresión | `test/ModuloVentas/Servicios/CierreCajaCategoriasServiceTest.java`, `CierreCajaCiegoReimpresionServiceTest.java`, `CierreCajaCiegoTicketPrinterTest.java`; `docs/cierre-caja-ciego.md`. El test de categorías usa H2 embebido, no la instancia MySQL ni una impresora real. |
| Ajustes, bultos y variantes de stock | `test/ModuloStocks/Vistas/StockBultosEdicionPolicyTest.java`, `FormStockAjusteValidationTest.java`, `FormListadoStockCantidadPorBultoPolicyTest.java`; `test/ModuloProductos/Entidades/ProductoHijoStockPolicyTest.java`; `docs/stock-por-bulto.md`. Estas variantes amplían gestión de existencias y no quedan cubiertas por descontar dos unidades al vender. |

### Insumos concretos para Restobar

Relacionar cada nuevo caso con una fila R01–R20 del [backlog](roadmap.md) y leer el cuerpo del test pertinente antes de transformar una condición interna en expectativa de usuario.

| Recorridos / foco | Fuente | Tests candidatos |
| --- | --- | --- |
| R01–R07: cargar y editar cuenta | `src/ModuloRestobar/Vistas/formTicket.java`, `formSalon.java`. | `test/ModuloRestobar/Vistas/FormTicketMesaLifecyclePolicyTest.java`, `FormTicketOfertaComboPresentacionTest.java`, `FormTicketDescuentosGlobalesTest.java`; `test/ModuloVentas/Entidades/TicketVentaRecalculoRestobarPersistenciaTest.java`, `RestobarRondaCotizacionTest.java`. |
| R08–R10: cocina, rondas y precuenta | `src/ModuloRestobar/Entidades/KDSEstado.java`, `KDSReglas.java`; `formTicket.java`. | `test/ModuloRestobar/Entidades/KDSReglasTest.java`, `KDSServiceTest.java`; `test/ModuloRestobar/Vistas/FormKDSCajaTest.java`. |
| R11–R13: comensales, traslado y cierre | `src/ModuloRestobar/Vistas/formDividirTicket.java`, `formCambiaMesa.java`; `src/ModuloRestobar/AppMozo/MesaCierreProteccion.java`. | `test/ModuloRestobar/AppMozo/MesaCuentaAperturaTest.java`, `MesaCierreProteccionTest.java`; `FormTicketMesaLifecyclePolicyTest.java`. |
| R14–R16: crédito, factura y delivery | `formTicket.java`, `src/ModuloRestobar/Vistas/formDelivery.java`; validación de límite de cuenta corriente. | `test/ModuloRestobar/Vistas/FormTicketFacturaElectronicaPedidoPolicyTest.java` y tests de crédito de la tabla anterior; precisar cobertura de delivery al escribir la ficha. |
| R17–R20: canales y concurrencia | `src/ModuloRestobar/AppMozo/AppMozoRoundProcessor.java`, `QrMesaRoundProcessor.java`, `MesaCierreProteccion.java`. | `test/ModuloRestobar/AppMozo/AppMozoRoundPolicyTest.java`, `AppMozoIntegrationPolicyTest.java`, `AppMozoSnapshotServiceTest.java`, `AppMozoSnapshotPresentationTest.java`, `QrMesaPolicyTest.java`, `QrMesaOpcionesTest.java`, `QrMesaDespachoTest.java`, `QrMesaCocinaReportTest.java`. |

Tres distinciones deben permanecer en toda ficha: cuenta/ocupación de mesa/preparación son estados diferentes; dividir impresión por comensal no demuestra cobros separados; trasladar a mesa libre no demuestra fusión con una ocupada. El estado de reparto tampoco demuestra que el pedido esté cobrado.

## Cómo actualizar esta página

Al agregar una ficha, actualizar su familia/etapa y grupos. Al implementar, enlazar el `.robot` y mantener ID/tags coherentes. Al ejecutar realmente, registrar evidencia privada por build y el alcance probado; no publicar reportes, SQL con datos, capturas o secretos. Si cambia JAR, configuración o fixture, no trasladar automáticamente el resultado anterior a la nueva combinación.
