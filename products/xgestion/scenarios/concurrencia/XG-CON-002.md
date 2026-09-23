---
{"id":"XG-CON-002","title":"Reabrir un presupuesto en dos puestos sin perder cambios ni cobrarlo dos veces","product":"xgestion","module":"concurrencia","tags":["xgestion","regression","concurrencia","varios-puestos","ventas"],"status":"planned"}
---

# XG-CON-002 — Reabrir un presupuesto en dos puestos sin perder cambios ni cobrarlo dos veces

## Objetivo

Coordinar dos operadores sobre el mismo presupuesto, diferenciando recarga de datos, edición desactualizada y cierre de una operación ya cobrada.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P0.** Ver [continuidad operativa](../../docs/continuidad-operativa.md). Sin Robot, seed ni evidencia del JAR. Documento compartido, distinto de repetir la confirmación en [FIN-009](../conciliacion/XG-FIN-009.md) y de la reapertura en un solo puesto de [REC-001](../recuperacion/XG-REC-001.md).

## Precondiciones y datos

- E1/S1, puestos P1/P2, presupuesto Q guardado por P1 con A × 2 a ARS 1.000: total ARS 2.000. Stock A = 10, presupuesto no descuenta stock; sin ofertas, listas, impresión ni fiscal.
- Acceso de P2 al documento exacto de P1 permitido por el perfil y calibrado; si la instalación lo restringe, registrar ese comportamiento y bloquear la variante de edición simultánea.
- Contrato de concurrencia de presupuesto pendiente: definir bloqueo, aviso de dato obsoleto o regla explícita de resolución antes de mutar desde una pantalla desactualizada. No atribuir al ERP un lock o versionado optimista no verificado.
- Todos los fixtures mencionados son sintéticos y **NO están creados por esta entrega**. Faltan paquete, controles accesibles, perfiles y lectores por identidad. No escribir SQL comercial durante el recorrido ni debilitar las guardas del runner.

## Pasos y resultados esperados

| Acción del usuario o responsable QA | Resultado esperado |
| --- | --- |
| Abrir Q desde ambos puestos por su contexto completo. | Ambos identifican el mismo documento y dos unidades, sin crear una copia con otro ID. |
| P1 cambia a 3 unidades y guarda; P2 cierra su consulta sin guardar y vuelve a cargar Q. | P2 recupera 3 unidades y ARS 3.000; stock 10, sin cobro. Se verifica recarga explícita, no refresco automático de una ventana abierta. |
| Desde baseline, P1 guarda 3 mientras P2 conserva una propuesta de 4; aplicar el contrato de conflicto acordado. | Oráculo pendiente antes de ejecutar: documentar si se rechaza, bloquea o resuelve la segunda edición y cuál total queda (ARS 3.000 o ARS 4.000 según la regla). Nunca aprobar una mezcla de renglones ni elegir el ganador después de observarlo. |
| Con un único estado resuelto, cobrar Q desde el puesto autorizado; recargarlo desde el otro. | Un cierre y un pago por la cantidad resuelta; stock 7 o 6 según esa cantidad. En la nueva consulta el documento cerrado es histórico y no se cobra otra vez. |

## Variantes y dependencias

- Intento de cerrar desde una ventana que quedó obsoleta tras el cierre del otro puesto: preparación/resultado de rechazo pendientes; no equipararlo con abrir de nuevo el histórico.
- Misma numeración local en documentos diferentes de P1/P2: conservar identidades completas y no fusionar ambos presupuestos.
- Sincronización entre bases separadas, política de cotización/lista al reabrir y receta quedan fuera del perfil básico.

## Evidencia y límites

Documento, puesto de origen, cantidades/precios de cada propuesta, orden de guardados, regla aprobada y efectos únicos del cierre. Conservar el conflicto aun si la recarga posterior muestra un documento coherente.

Un perfil, procedimiento u oráculo faltante produce BLOQUEADO antes de la acción dependiente. Ningún resultado observado se adopta como esperado para aprobar. INFO resume y explica fallos; DEBUG muestra acciones de negocio; TRACE agrega diagnóstico saneado. Conservar paso, esperado/observado y causa no determinada si no está demostrada.

## Recuperación

Ante una edición obsoleta, no insistir en Guardar para imponerla. Recargar según el procedimiento acordado o detener la operación si el estado no es confiable; preservar evidencia antes de restaurar ambos puestos.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: commit `daa002d597d0fa7380ace204d3727085c52d1415`. Las rutas siguientes son relativas a XGestion2; las clases/tests describen reglas y riesgos, no ejecuciones E2E.

- `src/ModuloVentas/Vistas/FormVenta.java:1916-1962`: lectura del documento y modo histórico de cerrados/anulados.
- `src/ModuloVentas/Vistas/FormVenta.java:5252-5273`: actualización del presupuesto guardado.
- `src/ModuloVentas/Vistas/FormVenta.java:6315-6347`: cierre de un documento existente.
- `test/ModuloVentas/Vistas/FormVentaPreventaPresupuestoEdicionPolicyTest.java`: edición habilitada; no acredita exclusión entre puestos.

Registrar SHA256/build del JAR, paquete, perfil, ámbito, IDs y reporte privado. No publicar credenciales, configuración completa, copias de bases, payloads, filas completas ni logs crudos.

