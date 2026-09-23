---
{"id":"XG-CON-001","title":"Disputar la última unidad desde dos puestos sin ocultar una sobreventa","product":"xgestion","module":"concurrencia","tags":["xgestion","regression","concurrencia","varios-puestos","stock","ventas"],"status":"planned"}
---

# XG-CON-001 — Disputar la última unidad desde dos puestos sin ocultar una sobreventa

## Objetivo

Comprobar el resultado de dos vendedores que intentan vender la misma última unidad con el perfil comercial de stock declarado.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P0.** Ver [continuidad operativa](../../docs/continuidad-operativa.md). Sin Robot, seed ni evidencia del JAR. Concurrencia de inventario entre puestos; no es doble confirmación de un mismo botón de [FIN-009](../conciliacion/XG-FIN-009.md). Etapa 6, laboratorio multicontexto pendiente.

## Precondiciones y datos

- Dos puestos QA P1/P2 de E1/S1, operadores distintos, misma existencia autoritativa de A = 1 unidad a ARS 1.000. Otra sucursal B conserva A = 5. Efectivo, comprobante interno, IVA 0, sin red externa, ofertas ni stock de presupuesto.
- Laboratorio multisesión pendiente con coordinación de ambos JAR y topología explícita. No asumir que dos bases locales sincronizadas equivalen a una base compartida con reserva global.
- Perfil bloqueo de venta sin stock ON, cierre anual íntegro. Acordar antes de automatizar si ese perfil garantiza exclusión concurrente, qué acción rechaza al segundo y cómo conserva su canasta; la lectura de fuente no demuestra bloqueo atómico de stock.
- Todos los fixtures mencionados son sintéticos y **NO están creados por esta entrega**. Faltan paquete, controles accesibles, perfiles y lectores por identidad. No escribir SQL comercial durante el recorrido ni debilitar las guardas del runner.

## Pasos y resultados esperados

| Acción del usuario o responsable QA | Resultado esperado |
| --- | --- |
| Abrir en ambos puestos una venta de A × 1 antes de confirmar cualquiera. | Cada propuesta muestra ARS 1.000; todavía no hay dos ventas cobradas por mostrar dos canastas. |
| Con el contrato de exclusión acordado, confirmar P1 y luego liberar la confirmación pendiente de P2. | Criterio del perfil estricto: una venta/cobro por ARS 1.000, stock final 0; el segundo intento no genera cobro ni stock -1. Si la regla concurrente no está acordada, bloquear antes de ejecutar este paso. |
| Atender el rechazo/actualización que corresponda en P2 y consultar ambas operaciones. | P2 conoce que no dispone de la unidad y puede cancelar/corregir; no aparece una venta cerrada adicional. A en la sucursal de control sigue en 5. |
| Desde baseline, invertir el puesto que confirma primero. | Mismo criterio de una unidad vendida; no privilegiar un puesto por su número ni fijar cuál gana un empate simultáneo. |

## Variantes y dependencias

- Preparar una barrera simultánea real además del orden P1→P2; la repetición secuencial no acredita carrera concurrente.
- Con bloqueo OFF y negocio que admite negativo, dos ventas legítimas pueden llevar stock a -1 y cobros a ARS 2.000. Ese perfil se acuerda y verifica aparte; no clasificarlo automáticamente como duplicación.
- Una base por puesto con cola pendiente necesita política de sobreventa/reconciliación distinta. No afirmar reserva global offline ni relajar el aislamiento actual para probarla.

## Evidencia y límites

Cronología de ambos puestos, stock observado al cargar y al cerrar, identidades distintas, pagos y saldo final por sucursal. El rechazo de selección de producto no demuestra exclusión atómica al cobrar.

Un perfil, procedimiento u oráculo faltante produce BLOQUEADO antes de la acción dependiente. Ningún resultado observado se adopta como esperado para aprobar. INFO resume y explica fallos; DEBUG muestra acciones de negocio; TRACE agrega diagnóstico saneado. Conservar paso, esperado/observado y causa no determinada si no está demostrada.

## Recuperación

Ante dos cierres inesperados, detener las ventas y conservar ambos documentos/movimientos. No anular automáticamente uno ni sumar stock para fabricar el resultado; conciliar y restaurar el laboratorio completo al terminar.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: commit `daa002d597d0fa7380ace204d3727085c52d1415`. Las rutas siguientes son relativas a XGestion2; las clases/tests describen reglas y riesgos, no ejecuciones E2E.

- `src/ModuloVentas/Vistas/FormVenta.java:6140-6193`: validación de stock condicionada por configuración, cierre anual y venta existente.
- `src/ModuloVentas/Vistas/FormVenta.java:6309-6347`: transacción de cierre posterior a las validaciones.
- `src/ModuloVentas/Entidades/TicketVenta.java:526-562`: movimientos de stock del cierre; no prueba una reserva concurrente global.
- `test/ModuloProductos/Servicios/CierreAnualStockPrevioPolicyTest.java`: disponibilidad de stock previo, distinta de concurrencia de ventas.

Registrar SHA256/build del JAR, paquete, perfil, ámbito, IDs y reporte privado. No publicar credenciales, configuración completa, copias de bases, payloads, filas completas ni logs crudos.

