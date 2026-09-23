# Facturación electrónica y pagos externos: mapa de escenarios críticos

**12 fichas nuevas, todas P0 y `planned`: 6 de facturación y 6 de pagos externos.**
Documentan recorridos y riesgos; no agregan Robot, seed, credenciales, adaptadores ni autorización para ejecutar servicios.
La prioridad refleja el riesgo de duplicar documentos o dinero, no la disponibilidad del laboratorio.

## Grupos y alcance para QA

| Grupo existente | Fichas de esta ampliación | Alcance |
| --- | --- | --- |
| `fiscal` | FEL-001..006 | Validación, aprobación, rechazo, incertidumbre, persistencia y nota de crédito. |
| `pagos-externos` | PEX-001..006 | Frontera manual/integrado, transferencia, QR, Point y recuperación. |

Consultar con `qa.cmd list --product xgestion --group fiscal` o
`qa.cmd list --product xgestion --group pagos-externos`.
Los grupos también pueden incluir fichas de otros mapas; **12 es el número de esta batería**, no la suma de todos los tags.
Los casos pendientes no se ejecutan ni producen PASS por estar documentados.

Las fichas usan los módulos y filtros existentes `fiscal` y `pagos-externos`; las FEL se organizan en la carpeta `scenarios/facturacion/`.
Se reutilizan los grupos transversales `comprobantes`, `cobros`, `recuperacion`, `integridad-operaciones`,
`permisos`, `devoluciones` y `dispositivos` cuando corresponden.

## Facturación

| ID | Recorrido | Prioridad |
| --- | --- | --- |
| [XG-FEL-001](../scenarios/facturacion/XG-FEL-001.md) | Corregir datos fiscales y cancelar antes de solicitar la emisión | P0 |
| [XG-FEL-002](../scenarios/facturacion/XG-FEL-002.md) | Autorizar una factura y conservar una sola emisión al volver a consultarla | P0 |
| [XG-FEL-003](../scenarios/facturacion/XG-FEL-003.md) | Resolver un rechazo fiscal explícito y reintentar sobre la misma venta | P0 |
| [XG-FEL-004](../scenarios/facturacion/XG-FEL-004.md) | Conciliar un resultado fiscal incierto antes de repetir la emisión | P0 |
| [XG-FEL-005](../scenarios/facturacion/XG-FEL-005.md) | Recuperar una factura autorizada que no pudo guardarse localmente | P0 |
| [XG-FEL-006](../scenarios/facturacion/XG-FEL-006.md) | Vincular una nota de crédito con la factura y sus importes originales | P0 |

## Pagos externos

| ID | Recorrido | Prioridad |
| --- | --- | --- |
| [XG-PEX-001](../scenarios/pagos-externos/XG-PEX-001.md) | Distinguir un cobro manual de la confirmación integrada de Mercado Pago | P0 |
| [XG-PEX-002](../scenarios/pagos-externos/XG-PEX-002.md) | Confirmar transferencias de la venta sin contar canceladas o repetidas | P0 |
| [XG-PEX-003](../scenarios/pagos-externos/XG-PEX-003.md) | Cobrar por QR sólo después de confirmar el pago de esa operación | P0 |
| [XG-PEX-004](../scenarios/pagos-externos/XG-PEX-004.md) | Resolver cancelación, vencimiento y confirmación tardía de un QR | P0 |
| [XG-PEX-005](../scenarios/pagos-externos/XG-PEX-005.md) | Confirmar un cobro Point con pago e importe correspondientes a la venta | P0 |
| [XG-PEX-006](../scenarios/pagos-externos/XG-PEX-006.md) | Recuperar rechazo o espera agotada de Point sin duplicar el cobro | P0 |

## Orden y criterios de avance

1. **Contrato del laboratorio:** paquete sintético, versiones, identidades de prueba, endpoints de homologación/sandbox, observación independiente y recuperación en ambos extremos. Adaptar el runner con una política explícita de aislamiento y red. Sin esto, ninguna integración se habilita.
2. **Estados simples:** FEL-001/002/003 y PEX-001/002/003/005. Hito: una solicitud se distingue de una autorización/pago; cada resultado tiene importe, moneda, contexto e identidad verificables, con un único efecto comercial.
3. **Incertidumbre y recuperación:** FEL-004/005 y PEX-004/006. Hito: se resuelve el estado remoto antes de repetir; respuestas tardías/repetidas no duplican cobro, venta ni emisión. Un éxito final no borra un intento anterior incierto.
4. **Documento relacionado:** FEL-006. Hito: una nota de crédito conserva origen e importes históricos, con efectos comerciales/financieros acordados por separado.
5. **Cruces de mayor riesgo:** sólo después de aceptar los recorridos individuales, preparar venta con pago externo + factura, Restobar + cobro + emisión y reinicio/concurrencia. No se declaran cubiertos por las doce fichas aisladas.

No hay fechas comprometidas. Cada hito requiere evidencia sobre JAR, paquete y servicio de pruebas concreto.
Mocks y tests unitarios son útiles para el framework, pero no acreditan homologación, pago confirmado ni terminal Point.

## Perfiles y datos todavía pendientes

| Perfil propuesto | Datos sintéticos | Requisito antes de ejecutar |
| --- | --- | --- |
| Fiscal simple | Venta ARS 2.420; neto 2.000 e IVA 420; receptor y emisor de prueba compatibles. | Datos fiscales válidos aportados por el paquete privado, tipo/punto/certificado de homologación y consulta de estado. |
| Fiscal incierto | Misma venta; autorización sin respuesta o autorización sin persistencia local. | Mecanismo controlado y observable de fallo; procedimiento de conciliación, sin reemisión a ciegas. |
| Nota de crédito | Factura ARS 1.000; neto 826,45 e IVA 173,55; precio actual distinto 1.200. | Contrato del vínculo fiscal y efectos de anulación; consulta independiente del original y la nota. |
| Transferencias | Venta ARS 2.000; T1=800, T2=1.200 y operación de control T3=2.000. | Cuenta sandbox y política verificable de pertenencia/uso único de cada ID. |
| QR | Orden ARS 2.000, control ARS 500; pendiente, confirmada, vencida y tardía. | Consulta orden/pago, control de tiempos y conciliación después de cerrar el diálogo. |
| Point | Venta ARS 2.000; aprobado, rechazado, cancelado, discrepancia 1.999 y monto ausente. | Dispositivo/cuenta compatibles de prueba, contrato de importe/identidad y reintentos. |

Estos alias **no existen como fixtures instalados** y no reservan IDs, cuentas ni documentos fiscales.
`catalogo-comercial-v1` no prepara esta batería.
La disponibilidad actual de homologación/sandbox y sus contratos debe verificarse durante la preparación;
leer la fuente del ERP no demuestra que cada proveedor ofrezca todos los estados o dispositivos de prueba.

La v1 ejecutable sigue siendo Windows QA exclusivo **offline, sin fiscalización ni pagos integrados**.
No basta reconectar esa VM: faltan perfiles, adaptación del runner, destinos permitidos y protección de salidas.
Estas fichas no autorizan pagos, devoluciones, emisiones, altas de cuentas, cambios de credenciales ni mutaciones externas.
No incluyen secretos ni comandos para omitir guardas.

## Reglas observadas y riesgos que deben probarse

| Tema | Observado en la fuente | Límite de lo que puede afirmarse |
| --- | --- | --- |
| Venta frente a factura | Una operación puede estar guardada/cobrada antes del resultado fiscal. | Un rechazo fiscal no implica venta abierta ni reversión de cobro/stock; declarar estado previo por ruta. |
| Rechazo fiscal | Rechazo explícito y error de datos son terminales; no habilitan fallback en ese intento. | Timeout/respuesta incompleta no son rechazo demostrado. |
| Estado remoto incierto | El orquestador permite fallback técnico y conserva el indicador de ambigüedad. | No existe una garantía acreditada de emisión única entre proveedores; FEL-004 concilia todos los intentos. |
| Autorizada sin guardar | Hay resultado y aviso específico que detiene el fallback. | No demuestra reconciliación automática ni bloqueo persistente de reemisión tras reiniciar. |
| Nota de crédito | La fuente usa importes fiscales guardados y datos del comprobante asociado. | Vínculo remoto, moneda, recuperación parcial y devolución de dinero requieren sus contratos; no inferirlos de una nota creada. |
| Manual frente a integrado | Sin cuenta activa, ciertos medios Mercado Pago usan importe manual; transferencia activa usa total confirmado. | Escribir un importe o elegir un medio no prueba pago remoto; promociones offline tampoco. |
| Transferencias | Se acumulan selecciones confirmadas y se limpian al cancelar ciertos diálogos. | El acumulador no acredita uso único global por ID ni conciliación entre puestos. |
| QR | Creación de orden, consulta de pago y asignación de ID son pasos distintos; cancelar puede fallar. | Cerrar/expirar el diálogo no demuestra que la orden sea impagable ni resuelve una confirmación tardía. |
| Point | Intención y pago aprobado son distintos; controla monto cuando está disponible. | Algunas respuestas sin monto pueden continuar; falta oráculo independiente. Cancelar el worker local no cancela por sí mismo el intento remoto. |

Los riesgos provienen de lectura de fuente; **no son defectos reproducidos ni resultados E2E**.
Si falta evidencia del estado remoto, se informa BLOQUEADO, con causa y requisito pendiente, sin inventar aprobación.
Si una ejecución preparada contradice el criterio acordado, se conserva el fallo aunque el mensaje final sea exitoso.

## Relación con los demás mapas

- [RES-030](../scenarios/restobar/XG-RES-030.md) conserva el recorrido fiscal propio de un pedido. FEL profundiza estados del servicio y recuperación; no agrega otra copia de ese cierre.
- [RES-035](../scenarios/restobar/XG-RES-035.md) conserva pedido QR, cuenta, mesa y cocina. PEX trata el cobro; pagar por QR no acredita toda la recepción del pedido.
- [PRM-074](../scenarios/promociones/XG-PRM-074.md), [PRM-075](../scenarios/promociones/XG-PRM-075.md) y [PRM-076](../scenarios/promociones/XG-PRM-076.md) prueban condiciones de oferta con medios manuales; no son evidencia de una integración activa.
- [Libro Diario y caja](libro-diario-caja.md) y [circuitos críticos](circuitos-criticos.md) definen conciliación por dominio. No exigir igualdad de filas o sumar todo el Libro Diario para probar un pago.
- [Respaldos](inventario-respaldos.md) recupera el laboratorio local; restaurarlo no borra pagos ni comprobantes remotos.
- [Roadmap general](roadmap.md) y [cobertura](cobertura.md) mantienen el estado agregado y el orden de implementación.

## Evidencia, mantenimiento y fuentes

Registrar identidades completas saneadas, eventos de solicitud/confirmación, estado remoto y local,
importes por moneda y deltas comerciales. INFO debe ser breve; cualquier fallo conserva esperado/observado
y evidencia aun en INFO. Los tokens, certificados, documentos personales, payloads, QR y logs crudos permanecen privados.
No convertir datos técnicos recibidos del proveedor en texto confiable sin saneamiento.

Fuente ERP inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Referencias con líneas en las fichas:
`EmisionFacturaElectronicaService`, `ResultadoEmisionFacturaElectronica`, `FormVenta`,
`FormVentas`, `NotaCreditoFiscalSnapshot`, `formTicketCierre`, `DialogMercadoPagoQR`
y `DialogMercadoPagoPointSmart`, con sus tests de política disponibles.
Este SHA describe el análisis y no demuestra equivalencia con el JAR instalado.

Al implementar una ficha: resolver sus dependencias, mantener ID/tags, agregar automatización y datos autorizados,
actualizar este mapa y el catálogo y conservar la evidencia del servicio de prueba utilizado.
No declarar cobertura fiscal o de pagos por un dry-run.
