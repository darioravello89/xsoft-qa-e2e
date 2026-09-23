---
{"id":"XG-REC-002","title":"Reconocer un guardado fallido antes de confirmar el presupuesto","product":"xgestion","module":"recuperacion","tags":["xgestion","regression","recuperacion","ventas"],"status":"planned"}
---

# XG-REC-002 — Reconocer un guardado fallido antes de confirmar el presupuesto

## Objetivo

Evitar considerar guardado un presupuesto cuando la base rechaza su primera escritura y recuperar una forma segura de continuar.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P0.** Ver [continuidad operativa](../../docs/continuidad-operativa.md). Sin Robot, seed ni evidencia del JAR. Nuevo presupuesto sin cobro. No repite el fallo de pago manual de [FIN-004](../conciliacion/XG-FIN-004.md) ni el cierre de Restobar de [RES-040](../restobar/XG-RES-040.md).

## Precondiciones y datos

- VM QA local offline; A a ARS 1.000, stock 10; propuesta A × 2 total ARS 2.000. Sin lista, oferta, impresión ni descuento de stock al presupuestar.
- Mecanismo pendiente de fallo verificable antes de la primera escritura del presupuesto en la base exclusiva. No alcanza con cortar conexión en un instante aproximado: demostrar el punto de corte y que no se creó cabecera/detalle.
- Conservar interfaz viva y base para verificar el resultado. Si no puede recuperarse la conexión del JAR sin reinicio, el procedimiento debe definir consulta/reconstrucción tras verificar ausencia; no presuponer reconexión automática.
- Todos los fixtures mencionados son sintéticos y **NO están creados por esta entrega**. Faltan paquete, controles accesibles, perfiles y lectores por identidad. No escribir SQL comercial durante el recorrido ni debilitar las guardas del runner.

## Pasos y resultados esperados

| Acción del usuario o responsable QA | Resultado esperado |
| --- | --- |
| Cargar la propuesta y registrar los datos visibles antes de guardar. | Dos unidades, total ARS 2.000, stock 10 y ningún documento de esta ejecución. |
| Con el fallo anterior a la primera escritura preparado, elegir Guardar sin imprimir. | No se acredita guardado exitoso; no hay presupuesto persistido, pago ni movimiento de stock por el intento. |
| Restablecer el recurso y consultar si existe el documento antes de reintentar. | Ausencia comprobada por contexto y correlación del intento. Si hay persistencia o no puede determinarse, detener el reintento e investigar. |
| Retomar la propuesta que conserve la pantalla o reconstruirla según el procedimiento declarado; guardar una sola vez. | Un presupuesto completo de ARS 2.000, sin cobro y stock 10; no existe una cabecera o detalle aislado del intento anterior. |
| Reabrir el documento guardado. | Cantidad, precio y estado coinciden con la propuesta; se puede continuar sin duplicarla. |

## Variantes y dependencias

- Error durante el guardado, después de crear cabecera o algunos renglones, requiere otra preparación y oráculo. No prometer rollback total: esta ruta no contiene la transacción explícita del cierre de cobro.
- Pérdida del mensaje después de un guardado ya persistido: consultar y retomar el existente; no aplicar el esperado de ausencia del caso básico.
- Cancelar el selector o la confirmación antes de Guardar no es un fallo de base y se registra por separado.

## Evidencia y límites

Conservar contenido propuesto, instante/categoría del fallo y consulta acotada de cabecera/detalle. La ausencia del mensaje de éxito no basta para declarar que no se guardó.

Un perfil, procedimiento u oráculo faltante produce BLOQUEADO antes de la acción dependiente. Ningún resultado observado se adopta como esperado para aprobar. INFO resume y explica fallos; DEBUG muestra acciones de negocio; TRACE agrega diagnóstico saneado. Conservar paso, esperado/observado y causa no determinada si no está demostrada.

## Recuperación

Restablecer solamente el recurso de la VM propia mediante el mecanismo preparado. Si el estado es parcial o desconocido, no corregirlo con SQL ni repetir Guardar; preservar evidencia y restaurar el baseline cuando termine el diagnóstico.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: commit `daa002d597d0fa7380ace204d3727085c52d1415`. Las rutas siguientes son relativas a XGestion2; las clases/tests describen reglas y riesgos, no ejecuciones E2E.

- `src/ModuloVentas/Vistas/FormVenta.java:5234-5273`: inserción/actualización y verificación del presupuesto.
- `src/ModuloVentas/Vistas/FormVenta.java:6301-6380`: comparación con la transacción explícita del cierre, que no debe extrapolarse.
- `test/ModuloVentas/Vistas/FormVentaPreventaPresupuestoEdicionPolicyTest.java`: estado editable; no prueba atomicidad del guardado.

Registrar SHA256/build del JAR, paquete, perfil, ámbito, IDs y reporte privado. No publicar credenciales, configuración completa, copias de bases, payloads, filas completas ni logs crudos.

