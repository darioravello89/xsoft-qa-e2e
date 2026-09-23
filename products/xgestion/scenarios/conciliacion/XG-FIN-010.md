---
{"id":"XG-FIN-010","title":"Conciliar una jornada con ventas nuevas y cobros de deudas anteriores","product":"xgestion","module":"conciliacion","tags":["xgestion","regression","conciliacion","integridad-operaciones","caja","cuenta-corriente","cobros"],"status":"planned"}
---

# XG-FIN-010 — Conciliar una jornada con ventas nuevas y cobros de deudas anteriores

## Objetivo

Cerrar el día diferenciando venta, cobro y pago, aunque correspondan a documentos de fechas distintas.

## Estado y alcance

**Pendiente de automatizar (`planned`), prioridad P0.** Etapas 3–4, integridad entre circuitos.
Ver [roadmap de circuitos críticos](../../docs/circuitos-criticos.md). No tiene Robot, seed propio ni evidencia del JAR.

## Precondiciones y datos

- Windows QA aislado, JAR identificado, baseline recuperable y paquete autorizado. Sin fiscal, correo, servicios externos ni impresoras salvo laboratorio expresamente preparado.
- Caja abierta ARS 1.000; cliente adeuda ARS 1.000 de un día anterior y proveedor ARS 600. En el turno actual: cobro manual cliente ARS 300, venta de contado ARS 500 y pago a proveedor desde Egreso de caja ARS 200. Todo efectivo ARS, sin impuestos, cuotas ni otros movimientos.
- Nombres QA e importes son requisitos públicos de fixtures futuros; no están creados por esta ficha ni garantizados por el seed comercial. Calibración de controles y lecturas por identidad pendientes.
- Definir moneda, concepto, medio, empresa, sucursal, puesto, operador y período antes de ejecutar. No cambiar datos mediante SQL para corregir una operación en curso.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Cobrar ARS 300 de la deuda anterior y vender de contado ARS 500. | Deuda cliente ARS 700; venta del turno ARS 500, cobro de cuenta corriente ARS 300. No presentar ARS 800 como nuevas ventas. |
| 2 | Pagar ARS 200 al proveedor desde Egreso de caja con la opción de cuenta proveedor. | Deuda proveedor ARS 400; un egreso real ARS 200. El concepto financiero y movimiento de caja no suman dos pagos. |
| 3 | Revisar arqueo y rubros del turno antes de cerrar. | Efectivo conciliado ARS 1.600 = 1.000 + 300 + 500 - 200. Registrar por separado ventas, cobros anteriores, ingresos y egresos; acordar las columnas exactas de cada modalidad de cierre antes de automatizar. |
| 4 | Cerrar una vez y consultar sus resultados históricos. | Se conservan los importes conciliados, las deudas y la referencia al turno; reabrir la consulta no genera movimientos. El perfil de cierre normal/ciego se fija antes del caso. |

## Variantes y dependencias

Cobro en otro medio, otro operador, turno que cruza medianoche y anulación anterior al cierre requieren deltas propios. La comparación abarca las mismas fechas/contextos; no exigir igualdad del total genérico de Libro Diario con el efectivo físico. Una diferencia de clasificación debe investigarse, no compensarse manualmente para cerrar.

Las dependencias sin procedimiento reproducible bloquean la variante. Un resultado observado no se convierte automáticamente en el resultado esperado. La aprobación exige todos los pasos y variantes habilitadas del perfil, identificando cuáles siguen pendientes.

## Evidencia y límites

Registrar importes antes/después, identidad de documentos y deltas de deuda, caja, stock y movimientos relevantes. Cada dominio tiene su alcance: dos representaciones técnicas no acreditan dos movimientos de dinero. Conservar lectura acotada y saneada, sin filas completas, credenciales ni datos privados en el repositorio.

INFO muestra caso y resultado; DEBUG acciones de negocio; TRACE controles, esperas y diagnóstico saneado. Todo fallo incluye paso, esperado, observado y evidencia; causa no determinada si no está demostrada. Un dry-run no acredita estos resultados.

## Recuperación

Cancelar las acciones no confirmadas. Ante persistencia incierta, consultar antes de reintentar y no ejecutar compensaciones improvisadas. Conservar evidencia privada, cerrar sólo procesos propios y restaurar el baseline mediante el procedimiento del laboratorio. La anulación de negocio no reemplaza la restauración técnica de datos.

## Anexo técnico y trazabilidad

Fuente inspeccionada: XGestion2 `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`.
Los tests fuente son insumos de reglas/riesgos, no evidencia de ejecución del JAR.

- `src/ModuloVentas/Entidades/CajaValores.java:203-283`.
- `src/ModuloVentas/Vistas/FormCierreDeCaja.java:739-806`.
- `src/ModuloVentas/Vistas/FormEgresoDeCaja.java:299-351`.
- `src/ModuloFinanzas/Entidades/CtaCteCliente.java:130-200`.

Registrar build/SHA256 del JAR, perfil, paquete, fecha, responsable, IDs y reporte privado al validar. Cambios posteriores de fuente obligan a revisar el contrato antes de ejecutar.
