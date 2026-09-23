---
{"id":"XG-ACT-004","title":"Conservar documentos y monedas históricas después de actualizar","product":"xgestion","module":"actualizacion","tags":["xgestion","regression","actualizacion","recuperacion","comprobantes","monedas"],"status":"planned"}
---

# XG-ACT-004 — Conservar documentos y monedas históricas después de actualizar

## Objetivo

Consultar operaciones anteriores a la actualización con sus importes, estados y relaciones originales, aunque el catálogo y la cotización actuales sean distintos.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P0.** Ver [continuidad operativa](../../docs/continuidad-operativa.md). Sin Robot, seed ni evidencia del JAR. Preservación semántica de históricos V0→V1. Complementa [FIN-007](../conciliacion/XG-FIN-007.md) y [LPR-023](../listas-precios/XG-LPR-023.md): el estímulo aquí es una migración de versión, no cambiar una condición comercial en la misma instalación.

## Precondiciones y datos

- Par V0/V1 y copia recuperable de ACT-001, sin nube ni nuevos movimientos durante la actualización. Schema exacto, migraciones y campos legacy pendientes de preparar.
- H-ARS cerrado: A × 2 a ARS 1.000, total/cobro ARS 2.000. H-USD cerrado a crédito: B × 2 a USD 2,50, total/deuda USD 5,00, cotización histórica ARS 1.000/USD y equivalente ARS 5.000. Ambos sin impuestos ni descuentos.
- Control anulado y presupuesto editable con identidades propias; receta/stock y saldos referenciados en el manifest. Catálogo vigente A = ARS 1.200 y cotización ARS 1.500/USD, preparados antes de consultar.
- Variante legacy ARS sin ID de moneda/foto original solo si existe en la versión origen; su interpretación y backfill autorizados deben acordarse, no crearse mediante corrupción de datos durante el caso.
- Todos los fixtures mencionados son sintéticos y **NO están creados por esta entrega**. Faltan paquete, controles accesibles, perfiles y lectores por identidad. No escribir SQL comercial durante el recorrido ni debilitar las guardas del runner.

## Pasos y resultados esperados

| Acción del usuario o responsable QA | Resultado esperado |
| --- | --- |
| En V0, consultar H-ARS/H-USD y registrar su manifest comercial. | Estados, cantidades, precios, cobros/deuda, cotización y vínculos conocidos, independientes de los precios actuales. |
| Actualizar la copia con resultado completo y abrir ambos históricos en V1. | H-ARS sigue total ARS 2.000; H-USD sigue USD 5,00 y equivalente histórico ARS 5.000, sin convertirlo en ARS 7.500 por la cotización actual. |
| Consultar cuenta del cliente, pagos y movimientos asociados. | Deuda USD 5,00 separada de ARS, un solo conjunto de efectos por cada documento; no recalcular ni duplicar movimientos al abrir. |
| Consultar el anulado y luego el presupuesto editable. | El anulado conserva su estado y vínculos; el presupuesto conserva identidad y estado editable. Sus reglas de recálculo son las del perfil explícito, no las del histórico cerrado. |
| Exportar por una modalidad local previamente calibrada y repetir las consultas. | Importes/monedas/alcance coinciden con el contrato de ese informe. Si no existe verificador, la variante de exportación queda pendiente; no usarla para declarar preservación total. |

## Variantes y dependencias

- Esquemas legacy con moneda nula, fotografía de precios faltante y backfill de netos requieren manifest de valores comerciales antes/después. Un campo técnico puede completarse sin que el total cambie.
- Estados cerrado/anulado/editable se verifican por separado; no congelar todo presupuesto como si fuera histórico inmutable.
- No afirmar que conservar históricos impide cambios autorizados de estructura o metadatos. La equivalencia se evalúa por negocio y relaciones, no por hash binario de la base.

## Evidencia y límites

Comparación del manifest de cada documento y de sus pagos/deudas/movimientos, monedas e identidades completas. Consultas/exportaciones saneadas; no usar solo sumas globales que oculten intercambios entre documentos.

Un perfil, procedimiento u oráculo faltante produce BLOQUEADO antes de la acción dependiente. Ningún resultado observado se adopta como esperado para aprobar. INFO resume y explica fallos; DEBUG muestra acciones de negocio; TRACE agrega diagnóstico saneado. Conservar paso, esperado/observado y causa no determinada si no está demostrada.

## Recuperación

Ante divergencia, detener nuevas operaciones en V1 y preservar la copia migrada. Recuperar snapshot completo si corresponde; no editar importes históricos para que el test pase ni hacer downgrade sobre el schema nuevo.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: commit `daa002d597d0fa7380ace204d3727085c52d1415`. Las rutas siguientes son relativas a XGestion2; las clases/tests describen reglas y riesgos, no ejecuciones E2E.

- `src/ModuloPrincipal/Entidades/VerificadorDeBaseDeDatos.java:5375-5403`: columnas de fotografía monetaria en documentos y finanzas.
- `src/ModuloVentas/Vistas/FormVenta.java:1916-1962`: presentación y modo de históricos.
- `test/ModuloPrincipal/Entidades/VerificadorPrecioNetoLegacyTest.java` y `CuentaCorrienteClienteImporteSchemaPolicyTest.java`: riesgos de migración de importes.
- `test/ModuloVentas/Entidades/TicketVentaPresupuestoCotizacionTest.java` y `TicketVentaAnulacionCuentaCorrienteTest.java`: fotografía y reversión; no acreditan por sí solos la actualización E2E.

Registrar SHA256/build del JAR, paquete, perfil, ámbito, IDs y reporte privado. No publicar credenciales, configuración completa, copias de bases, payloads, filas completas ni logs crudos.

