---
{"id":"XG-FIN-008","title":"Conciliar movimientos del período, saldo acumulado y exportación","product":"xgestion","module":"conciliacion","tags":["xgestion","regression","conciliacion","integridad-operaciones","cuenta-corriente","comprobantes"],"status":"planned"}
---

# XG-FIN-008 — Conciliar movimientos del período, saldo acumulado y exportación

## Objetivo

Distinguir lo ocurrido dentro del filtro de la deuda acumulada, sin perder saldos previos ni mezclar monedas.

## Estado y alcance

**Pendiente de automatizar (`planned`), prioridad P0.** Etapas 3–4, integridad entre circuitos.
Ver [roadmap de circuitos críticos](../../docs/circuitos-criticos.md). No tiene Robot, seed propio ni evidencia del JAR.

## Precondiciones y datos

- Windows QA aislado, JAR identificado, baseline recuperable y paquete autorizado. Sin fiscal, correo, servicios externos ni impresoras salvo laboratorio expresamente preparado.
- Cliente QA-FIN-C1: deuda ARS 1.000 el 31/08/2026; deuda ARS 2.000 el 01/09/2026 y pago ARS 500 el 02/09/2026, sin movimientos posteriores. Cliente control con deuda ARS 9.000. Filtrar septiembre de 2026; preparar fechas en fixtures, sin cambiar el reloj del host.
- Nombres QA e importes son requisitos públicos de fixtures futuros; no están creados por esta ficha ni garantizados por el seed comercial. Calibración de controles y lecturas por identidad pendientes.
- Definir moneda, concepto, medio, empresa, sucursal, puesto, operador y período antes de ejecutar. No cambiar datos mediante SQL para corregir una operación en curso.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Consultar el cliente desde 01/09/2026 hasta 30/09/2026. | Movimientos del período: deuda ARS 2.000 y pago ARS 500; neto ARS 1.500. Los resúmenes visibles, incluido el denominado acumulado en esta pantalla, están sujetos al rango y muestran ARS 1.500. No interpretarlo como toda la deuda histórica. |
| 2 | Ampliar el filtro para incluir agosto y volver a septiembre. | Al incluir el historial completo, deuda neta y resúmenes ARS 2.500; al volver a septiembre, resúmenes ARS 1.500. La deuda del cliente sigue siendo ARS 2.500 aunque la consulta muestre sólo una parte. No exigir que la última celda de la grilla filtrada incluya el saldo anterior. |
| 3 | Exportar localmente el resumen con el mismo cliente y rango. | Moneda, importes, orden y alcance coinciden con la consulta que ese informe declara. Diferenciar exportar la grilla de emitir un resumen completo; una modalidad sin contrato verificado permanece pendiente. |
| 4 | Consultar un período sin movimientos; volver al historial completo y luego al cliente control. | El período vacío muestra cero movimientos y resúmenes filtrados en cero. Volver al historial recupera ARS 2.500: no se borró deuda. Con un rango que incluya su deuda, el control muestra ARS 9.000 sin sumarlo al primer cliente. |

## Variantes y dependencias

Fechas límite, misma fecha/hora en varios puestos, USD separado, filas anuladas y orden estable. La etiqueta acumulado no implica que el campo ignore los filtros: la fuente aplica rango y búsqueda también a ese resumen. Si se requiere mostrar siempre toda la deuda, acordar esa mejora aparte. Repetir la lógica de alcance en proveedores con sus signos y filtros propios, sin copiar los de clientes. PDF e impresión física requieren sus verificadores; no se acreditan por validar Excel.

Las dependencias sin procedimiento reproducible bloquean la variante. Un resultado observado no se convierte automáticamente en el resultado esperado. La aprobación exige todos los pasos y variantes habilitadas del perfil, identificando cuáles siguen pendientes.

## Evidencia y límites

Registrar importes antes/después, identidad de documentos y deltas de deuda, caja, stock y movimientos relevantes. Cada dominio tiene su alcance: dos representaciones técnicas no acreditan dos movimientos de dinero. Conservar lectura acotada y saneada, sin filas completas, credenciales ni datos privados en el repositorio.

INFO muestra caso y resultado; DEBUG acciones de negocio; TRACE controles, esperas y diagnóstico saneado. Todo fallo incluye paso, esperado, observado y evidencia; causa no determinada si no está demostrada. Un dry-run no acredita estos resultados.

## Recuperación

Cancelar las acciones no confirmadas. Ante persistencia incierta, consultar antes de reintentar y no ejecutar compensaciones improvisadas. Conservar evidencia privada, cerrar sólo procesos propios y restaurar el baseline mediante el procedimiento del laboratorio. La anulación de negocio no reemplaza la restauración técnica de datos.

## Anexo técnico y trazabilidad

Fuente inspeccionada: XGestion2 `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`.
Los tests fuente son insumos de reglas/riesgos, no evidencia de ejecución del JAR.

- `src/ModuloFinanzas/Vistas/FormCuentaCorrienteCliente.java:1170-1337`.
- `src/ModuloFinanzas/Entidades/CuentaCorrienteSaldoService.java:42-92`.
- `src/ModuloProveedores/Vistas/FormCuentaCorriente.java:782-817`.
- `test/ModuloFinanzas/Vistas/FormCuentaCorrienteClienteExcelPolicyTest.java`.

Registrar build/SHA256 del JAR, perfil, paquete, fecha, responsable, IDs y reporte privado al validar. Cambios posteriores de fuente obligan a revisar el contrato antes de ejecutar.
