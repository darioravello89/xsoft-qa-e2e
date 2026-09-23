# Cobertura y evidencia de XGestion

La cobertura se expresa por recorridos de usuario y por evidencia obtenida. Un grupo puede mostrar capacidades futuras aunque todavía no tenga automatización. Consultar el [roadmap por etapas](roadmap.md) para el alcance y las dependencias.

Consultar el **[Excel de cobertura](../../../docs/coverage/xgestion-cobertura.xlsx)** para filtrar grupos, escenarios, pendientes y ejemplos del seed. Es una foto pública generada desde las fuentes, sin reportes privados ni validación real inferida. La [guía de uso y regeneración](../../../docs/cobertura.md) explica los estados y cómo mantenerla al día.

## Estado actual

| Capa | Disponible | Qué demuestra |
| --- | --- | --- |
| Catálogo | 298 fichas: 96 `implemented` y 202 `planned`; 0 `manual`. | Objetivos, datos y resultados documentados. |
| Automatización | 96 casos Robot implementados: 5 smoke, 9 ventas y 82 promociones. | Existe código ejecutable y comprobaciones definidas. |
| Datos comerciales | [Seed opcional](seed.md): 387 artículos, 163 ofertas, 9 listas y 3 medios manuales QA y 26 ejemplos de cálculo pendientes de validar. | Datos reproducibles para ampliar los escenarios; no suma casos automatizados. |
| Extensión de Venta | VEN-003 a VEN-009 implementados. | Siete recorridos requieren `sales_journeys`, grilla y editor calibrados; no acreditan E2E real por existir. |
| Promociones simples | PRM-001 a PRM-007 implementados y vinculados a siete ejemplos seed. | Recalcular, cancelar/retomar y cobrar; perfil y calibración propios, E2E real pendiente. |
| Canastas de ofertas | [PRM-008..076 y PRM-079](canastas-ofertas.md): 70 recorridos nuevos implementados. | Fórmulas/alcances, agrupadas, combos, fechas, listas, pagos y permisos. E2E real pendiente. |
| Nuevos circuitos | [24 remitos](remitos.md), [40 Restobar](restobar.md) y [28 listas](listas-precios.md), todos `planned`. | Fichas y variantes disponibles; faltan datos, adaptadores, calibración y automatización. |
| Circuitos críticos | [58 fichas CCC/CCP/CUO/LDI/CAJ/FIN/INV/BKP](circuitos-criticos.md), todas `planned`. | Prioridades, variantes y datos declarados; sin Robot ni seed financiero todavía. |
| Complemento crítico | [50 fichas COB/PRE/DEV/FEL/PEX/REC/CON/ACT/BEN](complementos-criticos.md), todas `planned`. | Datos, pasos, riesgos y dependencias; no añade pruebas ejecutables. |
| Contextos pendientes | PRM-077/078. | Falta el paquete QA de varias sucursales/empresas; sin suite ejecutable. |
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
| [XG-VEN-003](../scenarios/ventas/XG-VEN-003.md) | Se modifica la cantidad cargada. | Disponible | Pendiente |
| [XG-VEN-004](../scenarios/ventas/XG-VEN-004.md) | Un código inexistente no altera la venta. | Disponible | Pendiente |
| [XG-VEN-005](../scenarios/ventas/XG-VEN-005.md) | Se cobra con vuelto. | Disponible | Pendiente |
| [XG-VEN-006](../scenarios/ventas/XG-VEN-006.md) | Se cancela y retoma el cobro sin duplicarlo. | Disponible | Pendiente |
| [XG-VEN-007](../scenarios/ventas/XG-VEN-007.md) | Se rechaza el abandono y se continúa. | Disponible | Pendiente |
| [XG-VEN-008](../scenarios/ventas/XG-VEN-008.md) | La siguiente venta después de cobrar comienza limpia. | Disponible | Pendiente |
| [XG-VEN-009](../scenarios/ventas/XG-VEN-009.md) | La siguiente venta después de abandonar comienza limpia. | Disponible | Pendiente |
| [XG-PRM-001](../scenarios/promociones/XG-PRM-001.md) | Aplicar una promoción porcentual y recalcular la cantidad. | Disponible | Pendiente |
| [XG-PRM-002](../scenarios/promociones/XG-PRM-002.md) | Aplicar un descuento de importe fijo y recalcular la cantidad. | Disponible | Pendiente |
| [XG-PRM-003](../scenarios/promociones/XG-PRM-003.md) | Recalcular una promoción 2x1 al pasar de una a tres unidades. | Disponible | Pendiente |
| [XG-PRM-004](../scenarios/promociones/XG-PRM-004.md) | Recalcular el descuento del 50 % en la segunda unidad. | Disponible | Pendiente |
| [XG-PRM-005](../scenarios/promociones/XG-PRM-005.md) | Conservar el precio normal cuando la promoción está vencida. | Disponible | Pendiente |
| [XG-PRM-006](../scenarios/promociones/XG-PRM-006.md) | Conservar el precio normal antes del inicio de una promoción. | Disponible | Pendiente |
| [XG-PRM-007](../scenarios/promociones/XG-PRM-007.md) | Conservar el precio normal cuando la promoción está desactivada. | Disponible | Pendiente |

Los conteos vivos salen del catálogo: `qa.cmd list --product xgestion --groups`. Hoy `smoke` tiene cinco implementados; `regression`, 96 implementados y 202 pendientes; `ventas`, nueve implementados; y `promociones`, 77 implementados y 2 pendientes. Los subgrupos de alcances, agrupadas, combos y condiciones tienen 31, 21, 5 y 13 implementados; condiciones conserva 2 pendientes. Un escenario puede pertenecer a varios grupos: no sumar sus conteos como si fueran casos diferentes. Los tags iniciales se conservan para no alterar selecciones existentes.

El efectivo exacto, el vuelto y el reintento pertenecen a sus grupos según los tags del catálogo; los conteos de esas familias no implican cobertura de pagos múltiples, crédito ni otras monedas. R01–R20 son referencias del roadmap vinculadas a las fichas XG-RES; no agregan casos a las 298 fichas ni al denominador de automatización.

Los siete casos PRM iniciales requieren el [perfil de promociones](promociones.md); los 70 nuevos añaden [canastas, listas, pagos y perfiles](canastas-ofertas.md) y la preparación automática del seed al seleccionarlos; también se puede indicar `--seed catalogo-comercial-v1`. Los 26 ejemplos comerciales continúan separados del catálogo: veinte enlazan fichas implementadas y seis enlazan fichas LPR pendientes (016/017/019/020). Los vínculos no acreditan automatización ni garantizan todos los datos requeridos por la ficha. En UI se distingue subtotal bruto, descuento y neto; en persistencia `vecTotal` es bruto, `vecOferta` el descuento automático y `venTotal` el neto. Los negativos implementados prueban antes una oferta válida de control y la abandonan sin efectos.

## Matriz funcional y variantes

La matriz funcional permite decidir la próxima ampliación. **Parcial** significa que existe alguna automatización de esa familia, no que estén verificadas sus variantes. Todos los recorridos de producto de esta matriz mantienen E2E real pendiente.

| Familia | Variantes incluidas en el mapa | Estado de automatización / siguiente paso |
| --- | --- | --- |
| Preparación/acceso | Inicio, credenciales inválidas/válidas, empresa/sucursal/usuario. | Parcial: XG-INI-001, XG-AUT-001/002. Aceptación real y perfiles pendientes. |
| Consultar productos | Conocido/ausente en listado. | Parcial: XG-PRO-001/002; no cubre carga en venta. |
| Cargar/corregir venta | Cantidad, código ausente, conservar líneas y continuar. | Carga, código ausente y edición incluidos en VEN-001/002/003/004/007; calibración y E2E real pendientes. |
| Efectivo/cancelación | Exacto, vuelto, cancelar/retomar, abandono y operación siguiente. | VEN-001/002/005/006/008/009 disponibles; requieren calibración y ejecución real. |
| Cantidades/stock | Decimales, bultos, importe, repetidos, variantes padre/hijo, suficiente/insuficiente, bloqueo on/off. | INV-001..004 documentan ajustes, traslados, cierre anual y conciliación. Automatización pendiente; la venta básica solo comprueba su delta de stock. |
| Precios/promociones | Listas por cliente/sucursal/turno/cantidad, porcentaje/importe/cantidad/combos, vigencia y aplicabilidad. | PRM-001..076 y PRM-079 implementados; PRM-077/078 pendientes. LPR-001..028 documentan origen/prioridad/moneda y diferencias Venta/Restobar, pendientes de automatizar. Ver mapas de ofertas y listas. |
| Descuentos/impuestos | Ítem/global/pago, redondeos/desglose, notas, puntos y combinaciones. | PRM-079 implementa permiso y descuento manual sobre oferta; REM-017..022 y RES-038 documentan circuitos relacionados. BEN-001..006 documentan globales/fracciones, desglose y puntos; otras variantes, calibración y ejecución real pendientes. |
| Monedas | ARS/USD, cotización válida/inválida, moneda contable, cambio de importe/moneda y redondeos. | ARS simple disponible; LPR, CCC/CCP/CUO y FIN-007/008 documentan variantes por ruta, moneda original, cotización e histórico, pendientes de automatizar. |
| Cobros/crédito | Simple/múltiple, parcial permitido, insuficiente, cuenta corriente/límite, cuotas y anticipo. | Efectivo simple disponible; COB-001..008 detallan cobro combinado/multimoneda, pendiente. CCC-001..010, CCP-001..008 y CUO-001..006 documentan cuentas, pagos y cuotas. Preparar datos/perfiles y resolver efectos distintos según origen del cobro. |
| Presupuestos/documentos | Guardar/cancelar, moneda, nueva/reabierta/histórica, conversión y tipo de comprobante. | No fiscal inicial disponible; PRE-001..006 documentan ciclo guardar/convertir, enlazando LPR-022; FEL-001..006 cubren emisión/reintentos en homologación futura. Todo el complemento pendiente. |
| Después de vender | Consulta, devolución/anulación, caja/arqueo/cierre, autorizaciones y auditoría. | LDI-001..008, CAJ-001..010 y FIN-001..010 documentados, pendientes de automatizar; DEV-001..006 amplían devolución/nota de crédito, con contratos por resolver. Separar origen, medio, moneda, empresa/sucursal/puesto/operador. |
| Restobar salón/mostrador | Cuenta, cubiertos, platos, opciones, agregados, recetas, ingredientes, mozo, comanda/rondas, precuenta y traslado/cierre. | 40 fichas RES-001..040 planificadas, con mapa a R01–R20. Recetas con varios renglones y cantidades son riesgo prioritario. Ninguna suite Restobar disponible todavía. |
| Restobar canales | Crédito/FE, delivery/cadete, autopedido/KDS, mozo/QR, retransmisión y concurrencia. | RES-029..036 y RES-039/040 documentan límites y dependencias; servicios, dispositivos y laboratorio pendientes. |
| Servicios/dispositivos | Pagos externos, fiscal, impresión, balanza/lector y fallas de conexión. | FEL-001..006 y PEX-001..006 documentan servicios. Entornos/equipos autorizados, runner específico y automatización pendientes. |
| Ampliación operativa | Recepción de remitos de compra, borrador/confirmación, unidades/bultos, costos/listas, moneda, destino y anulación. Varios puestos. | REM-001..024 documentados; preparar datos, permisos y accesibilidad de recepción. Borrador no recibe stock; anular no restaura costos/precios. Concurrencia con laboratorio propio. |
| Recuperación transversal | Rechazar, cancelar, corregir/reintentar, límites y fallas sin datos parciales/duplicados. | Abandono, rechazo con continuación, edición, cancelar/retomar cobro (también en promociones) y siguiente operación disponibles; FIN-004/005/006/009 y BKP-001/002 documentan integridad, permisos y recuperación, pendientes de automatizar. REC-001..004 separan interrupciones al guardar/cerrar; CON-001..004, dos puestos y sincronización; ACT-001..004, cambio de versión e históricos. Todos pendientes. Importación no acredita restauración exacta. |

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

Referencia del análisis inicial y de la tabla de fuentes siguiente: repositorio XGestion2, rama `release/189-lts`, commit `f34238183d494259bed1279dd7d9aac0ce16a3ae`. Las rutas son relativas a ese repositorio; las líneas corresponden a ese commit fijado y pueden cambiar en el checkout actual. La fuente ayuda a diseñar expectativas y perfiles, pero no acredita que el JAR tenga ese código ni que los recorridos se hayan ejecutado.

Las ampliaciones REM/RES/LPR y de [circuitos críticos](circuitos-criticos.md) se inspeccionaron en `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Sus referencias específicas están en los mapas de [remitos](remitos.md), [Restobar](restobar.md) y [listas de precios](listas-precios.md), y en los anexos de cada ficha.

El lote PRM-001..007 usa además la referencia ERP `925589278503f2d339beeb0a79f773c605512dd8`, documentada en la [especificación de promociones](../../../docs/specs/005-promociones.md) y en los anexos de las fichas: `FormVenta`, `TicketVenta`, reglas de oferta y sus expectativas públicas del seed. El commit fuente no sustituye la calibración del JAR ni su evidencia de ejecución.

| Familia | Fuente de comportamiento | Tests relevantes como insumo |
| --- | --- | --- |
| Carga/cantidad/variantes | `src/ModuloVentas/Vistas/FormVenta.java`: carga, `setProducto`, selección de variante; `FormVentaDetalle.java`. | `test/ModuloVentas/Vistas/FormVentaProductoCantidadPolicyTest.java`, `FormVentaCantidadPreviaTecladoTest.java`, `PrecioBultoVentaPolicyTest.java`, `FormVentaSeleccionVarianteWiringTest.java`. |
| Notas/listas/ofertas | `FormVenta.java`: consolidación, selección y recálculo de lista/ofertas. | `FormVentaNotasConsolidacionWiringTest.java`, `FormVentaListaPrecioPrioridadPolicyTest.java`, `FormVentaReaperturaOfertasPolicyTest.java`. |
| Descuentos/precio | `FormVentaDetalle.java`, cálculo de totales. | `FormVentaDescuentosGlobalesTest.java`, `FormVentaDetalleDescuentoOfertaPolicyTest.java`, `FormVentaDetallePrecioUnitarioTest.java`. |
| Cotización/presupuestos | `FormVenta.java:3061` carga protegida de cotización; `:4978` moneda del presupuesto; `:6370` validación antes de guardar. | `FormVentaCotizacionCargaTest.java`, `FormVentaCotizacionQa3Test.java`, `FormVentaDetalleCotizacionQa3Test.java`, `FormVentaPresupuestoMonedaPolicyTest.java`. |
| Cobro simple | `FormVenta.java:6041` diálogo, `:6078` persistencia sólo al confirmar; `Dialogs/formTicketCierre.java:322` recibido/vuelto; `TicketVenta.java:2029` encabezado y `:2125` caja por total aplicado, sin pago múltiple. | `FormVentaCierreCobroPolicyTest.java`; helpers y wiring, no E2E. |
| Cobro multimoneda/múltiple | `src/ModuloVentas/Vistas/Dialogs/formTicketCierre.java`: importe recibido, vuelto, moneda y pagos. | `test/ModuloVentas/Vistas/Dialogs/FormTicketCierreMonedaStateTest.java`, `FormTicketCierreCobroMultiplePolicyTest.java`. |
| Crédito/cuotas | `FormVenta.java:5910` cliente de cuenta corriente y `:6083` límite; `Dialogs/DialogVentaCuotas.java`. | `FormVentaCierreCuentaCorrientePolicyTest.java`, `Dialogs/CuotasDialogMonedaTest.java`, tests de persistencia y moneda de cuotas. |
| Stock/recuperación | `FormVenta.java:5930` acumulación de stock al cerrar existente; `:6391` rollback; `:6422` restauración; `:6568` verificación de persistencia. | Tests de cierre, persistencia y rollback del producto. Exigen además un escenario real con falla controlada. |
| Abandono/nueva venta | `FormVenta.java:648` confirmación; `:681` supervisor; `:709` auditoría; `:4492` defaults y `:6188` reinicio de la misma ventana. `DialogConfirmacion.java:68`/`:82`: Aceptar/Cancelar. | Tests de auditoría y políticas de venta; completar evidencia del recorrido visible. |
| Fidelización | `FormVenta.java:6781` visibilidad/cliente; `:6867` uso de puntos y límites. | BEN-004..006 documentan canje, vigencia y cambio de cliente/condición; requieren fixtures de saldo/vencimiento y automatización. No cubierto por venta básica. |
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

Relacionar cada nuevo caso con R01–R20 cuando corresponda o con la familia nueva del [mapa Restobar](restobar.md), como recetas o recuperación y leer el cuerpo del test pertinente antes de transformar una condición interna en expectativa de usuario.

| Recorridos / foco | Fuente | Tests candidatos |
| --- | --- | --- |
| R01–R07: cargar y editar cuenta | `src/ModuloRestobar/Vistas/formTicket.java`, `formSalon.java`. | `test/ModuloRestobar/Vistas/FormTicketMesaLifecyclePolicyTest.java`, `FormTicketOfertaComboPresentacionTest.java`, `FormTicketDescuentosGlobalesTest.java`; `test/ModuloVentas/Entidades/TicketVentaRecalculoRestobarPersistenciaTest.java`, `RestobarRondaCotizacionTest.java`. |
| R08–R10: cocina, rondas y precuenta | `src/ModuloRestobar/Entidades/KDSEstado.java`, `KDSReglas.java`; `formTicket.java`. | `test/ModuloRestobar/Entidades/KDSReglasTest.java`, `KDSServiceTest.java`; `test/ModuloRestobar/Vistas/FormKDSCajaTest.java`. |
| R11–R13: comensales, traslado y cierre | `src/ModuloRestobar/Vistas/formDividirTicket.java`, `formCambiaMesa.java`; `src/ModuloRestobar/AppMozo/MesaCierreProteccion.java`. | `test/ModuloRestobar/AppMozo/MesaCuentaAperturaTest.java`, `MesaCierreProteccionTest.java`; `FormTicketMesaLifecyclePolicyTest.java`. |
| R14–R16: crédito, factura y delivery | `formTicket.java`, `src/ModuloRestobar/Vistas/formDelivery.java`; validación de límite de cuenta corriente. | `test/ModuloRestobar/Vistas/FormTicketFacturaElectronicaPedidoPolicyTest.java` y tests de crédito de la tabla anterior; RES-031 documenta delivery; precisar variantes adicionales y calibración al automatizar. |
| R17–R20: canales y concurrencia | `src/ModuloRestobar/AppMozo/AppMozoRoundProcessor.java`, `QrMesaRoundProcessor.java`, `MesaCierreProteccion.java`. | `test/ModuloRestobar/AppMozo/AppMozoRoundPolicyTest.java`, `AppMozoIntegrationPolicyTest.java`, `AppMozoSnapshotServiceTest.java`, `AppMozoSnapshotPresentationTest.java`, `QrMesaPolicyTest.java`, `QrMesaOpcionesTest.java`, `QrMesaDespachoTest.java`, `QrMesaCocinaReportTest.java`. |

Tres distinciones deben permanecer en toda ficha: cuenta/ocupación de mesa/preparación son estados diferentes; dividir impresión por comensal no demuestra cobros separados; trasladar a mesa libre no demuestra fusión con una ocupada. El estado de reparto tampoco demuestra que el pedido esté cobrado.

## Cómo actualizar esta página

Al agregar una ficha, actualizar su familia/etapa y grupos. Al implementar, enlazar el `.robot` y mantener ID/tags coherentes. Al ejecutar realmente, registrar evidencia privada por build y el alcance probado; no publicar reportes, SQL con datos, capturas o secretos. Si cambia JAR, configuración o fixture, no trasladar automáticamente el resultado anterior a la nueva combinación.

Después de cambiar estas fuentes, ejecutar `qa.cmd coverage` y `qa.cmd coverage --check`. Revisar e incluir los tres archivos de `docs/coverage/` en la misma revisión: `xgestion-cobertura.json`, `xgestion-cobertura.xlsx` y `xgestion-cobertura.manifest.json`. El control no necesita Node; el manifiesto registra hashes y fecha de generación UTC. No editar directamente los archivos generados para cambiar estados o conteos.

## Ofertas USD críticas

[PRM-080..084](ofertas-usd.md): cinco casos P0 implementados, trece variantes obligatorias, grupo `ofertas-usd`. Un caso aprueba sólo al completar todas sus variantes. Validación real pendiente; el Excel muestra prioridad específica P0. Se comprueban originales USD, equivalencia ARS, caja, stock y persistencia. Las combinaciones monetarias adicionales siguen pendientes.
