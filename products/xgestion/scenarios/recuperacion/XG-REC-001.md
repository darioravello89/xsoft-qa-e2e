---
{"id":"XG-REC-001","title":"Retomar una venta guardada después de interrumpir la interfaz","product":"xgestion","module":"recuperacion","tags":["xgestion","regression","recuperacion","ventas"],"status":"planned"}
---

# XG-REC-001 — Retomar una venta guardada después de interrumpir la interfaz

## Objetivo

Recuperar los productos de una operación guardada tras perder la interfaz y continuar trabajando sin crear otro documento.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P0.** Ver [continuidad operativa](../../docs/continuidad-operativa.md). Sin Robot, seed ni evidencia del JAR. Venta local guardada como presupuesto, sin cobro. Se diferencia de [BKP-002](../respaldos/XG-BKP-002.md): se recupera el documento persistido, no se restaura una base. [LPR-022](../listas-precios/XG-LPR-022.md) cubre condiciones monetarias de reapertura; aquí se comprueba la interrupción y la identidad.

## Precondiciones y datos

- Windows QA exclusivo, offline y descartable, JAR conocido. Procedimiento pendiente para interrumpir exclusivamente el proceso propio después de comprobar que terminó Guardar, conservando la base para la consulta posterior.
- A stockeable, ARS 1.000, stock 10; cliente QA-REC-C1; presupuesto A × 2, total ARS 2.000, nota «Retomar QA». IVA 0, sin ofertas/listas, impresión ni integración; presupuesto no descuenta stock.
- Empresa/sucursal/puesto y número del documento se registran después del guardado. El harness debe poder observar el estado posterior sin restaurar automáticamente el baseline entre la interrupción y la consulta; ese flujo de laboratorio aún no existe.
- Todos los fixtures mencionados son sintéticos y **NO están creados por esta entrega**. Faltan paquete, controles accesibles, perfiles y lectores por identidad. No escribir SQL comercial durante el recorrido ni debilitar las guardas del runner.

## Pasos y resultados esperados

| Acción del usuario o responsable QA | Resultado esperado |
| --- | --- |
| Cargar A × 2 y la nota; elegir guardar presupuesto sin imprimir. | Presupuesto identificable por contexto completo, cantidad 2, ARS 2.000 y nota. No hay cobro ni egreso de stock; A sigue en 10. |
| Cuando la persistencia esté verificada, ejecutar el corte de interfaz previsto y reiniciar el mismo JAR con la misma base QA. | No se crea ni se cobra otro documento por reiniciar; la operación guardada sigue consultable. |
| Buscar y abrir el presupuesto registrado. | Misma identidad, cliente, cantidad 2, total ARS 2.000 y nota; editable según su estado. No exigir reapertura automática de la ventana. |
| Cerrar y volver a consultar sin modificar. | Un presupuesto, sin movimientos de pago/stock; la consulta repetida no cambia lo guardado. |

## Variantes y dependencias

- Cerrar normalmente y repetir con interrupción controlada; las evidencias se conservan por separado.
- Una venta nueva nunca guardada no tiene recuperación automática verificada. No exigir que reaparezca después de terminar el proceso ni confundir memoria de la UI con persistencia.
- Si se necesita editar antes del corte, verificar primero cuándo persiste cada cambio: la edición de un presupuesto existente puede escribir antes de pulsar Guardar. Esa variante requiere su propio punto de corte.

## Evidencia y límites

Comparar cabecera, detalle, nota, estado e identidad antes/después; contrastar ausencia de pagos y deltas de stock. El éxito no se deduce de que vuelva a abrir el programa.

Un perfil, procedimiento u oráculo faltante produce BLOQUEADO antes de la acción dependiente. Ningún resultado observado se adopta como esperado para aprobar. INFO resume y explica fallos; DEBUG muestra acciones de negocio; TRACE agrega diagnóstico saneado. Conservar paso, esperado/observado y causa no determinada si no está demostrada.

## Recuperación

Si el documento no aparece, detener nuevos guardados y conservar la evidencia. Consultar por identidad antes de reconstruirlo; no crear uno igual para ocultar la pérdida. Restaurar el baseline únicamente al terminar la investigación de esta variante.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: commit `daa002d597d0fa7380ace204d3727085c52d1415`. Las rutas siguientes son relativas a XGestion2; las clases/tests describen reglas y riesgos, no ejecuciones E2E.

- `src/ModuloVentas/Vistas/FormVenta.java:5217-5273`: Guardar presupuesto y validación de persistencia.
- `src/ModuloVentas/Vistas/FormVenta.java:1916-1962`: reapertura por identidad y estado.
- `src/ModuloVentas/Vistas/FormVenta.java:653-679`: aviso de pérdida de cambios sin guardar.
- `test/ModuloVentas/Vistas/FormVentaPreventaPresupuestoEdicionPolicyTest.java` y `test/ModuloVentas/Entidades/TicketVentaPresupuestoCotizacionTest.java`.

Registrar SHA256/build del JAR, paquete, perfil, ámbito, IDs y reporte privado. No publicar credenciales, configuración completa, copias de bases, payloads, filas completas ni logs crudos.

