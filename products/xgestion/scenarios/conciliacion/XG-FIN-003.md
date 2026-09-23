---
{"id":"XG-FIN-003","title":"Anular una venta a crédito sin cobros y conciliar sus efectos","product":"xgestion","module":"conciliacion","tags":["xgestion","regression","conciliacion","integridad-operaciones","cuenta-corriente","devoluciones","stock","permisos"],"status":"planned"}
---

# XG-FIN-003 — Anular una venta a crédito sin cobros y conciliar sus efectos

## Objetivo

Revertir una venta simple conservando la relación con el documento y sin devolver dinero que nunca se recibió.

## Estado y alcance

**Pendiente de automatizar (`planned`), prioridad P0.** Etapas 3–4, integridad entre circuitos.
Ver [roadmap de circuitos críticos](../../docs/circuitos-criticos.md). No tiene Robot, seed propio ni evidencia del JAR.

## Precondiciones y datos

- Windows QA aislado, JAR identificado, baseline recuperable y paquete autorizado. Sin fiscal, correo, servicios externos ni impresoras salvo laboratorio expresamente preparado.
- Venta cerrada QA-FIN-V1 por ARS 1.000 a crédito, sin anticipo, cuotas ni cobros posteriores; stock anterior 10 y actual 9; cliente sin otra deuda; caja ARS 5.000. Operador autorizado, motivo de anulación requerido por el flujo calibrado.
- Nombres QA e importes son requisitos públicos de fixtures futuros; no están creados por esta ficha ni garantizados por el seed comercial. Calibración de controles y lecturas por identidad pendientes.
- Definir moneda, concepto, medio, empresa, sucursal, puesto, operador y período antes de ejecutar. No cambiar datos mediante SQL para corregir una operación en curso.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Consultar venta, deuda, stock y caja antes de anular. | Venta activa, deuda ARS 1.000, stock 9 y caja ARS 5.000 identificados por contexto completo. |
| 2 | Solicitar anulación y rechazar su confirmación. | Se conserva exactamente el estado inicial. |
| 3 | Repetir y confirmar la anulación por el procedimiento autorizado. | Venta anulada, deuda neta ARS 0 mediante su contramovimiento, stock 10; caja sigue ARS 5.000. Conservar motivo y operador. |
| 4 | Volver a consultar y probar el intento de anular nuevamente según el acceso que permita la UI. | No hay otra devolución de stock, pago o contramovimiento; no se elimina la historia. La ausencia de un botón de segundo intento también se registra. |

## Variantes y dependencias

Anticipo, pagos posteriores, cuotas y devolución parcial no se deducen de este caso: requieren decidir cómo devolver/imputar dinero y preparar sus estados. La anulación de compras tiene reglas distintas. Una falla de reversión conserva evidencia; no limpiar con SQL.

Las dependencias sin procedimiento reproducible bloquean la variante. Un resultado observado no se convierte automáticamente en el resultado esperado. La aprobación exige todos los pasos y variantes habilitadas del perfil, identificando cuáles siguen pendientes.

## Evidencia y límites

Registrar importes antes/después, identidad de documentos y deltas de deuda, caja, stock y movimientos relevantes. Cada dominio tiene su alcance: dos representaciones técnicas no acreditan dos movimientos de dinero. Conservar lectura acotada y saneada, sin filas completas, credenciales ni datos privados en el repositorio.

INFO muestra caso y resultado; DEBUG acciones de negocio; TRACE controles, esperas y diagnóstico saneado. Todo fallo incluye paso, esperado, observado y evidencia; causa no determinada si no está demostrada. Un dry-run no acredita estos resultados.

## Recuperación

Cancelar las acciones no confirmadas. Ante persistencia incierta, consultar antes de reintentar y no ejecutar compensaciones improvisadas. Conservar evidencia privada, cerrar sólo procesos propios y restaurar el baseline mediante el procedimiento del laboratorio. La anulación de negocio no reemplaza la restauración técnica de datos.

## Anexo técnico y trazabilidad

Fuente inspeccionada: XGestion2 `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`.
Los tests fuente son insumos de reglas/riesgos, no evidencia de ejecución del JAR.

- `src/ModuloVentas/Entidades/TicketVenta.java:3285-3347`.
- `src/ModuloVentas/Servicios/AuditoriaVentasService.java`.
- `test/ModuloVentas/Entidades/TicketVentaAnulacionCuentaCorrienteTest.java`.

Registrar build/SHA256 del JAR, perfil, paquete, fecha, responsable, IDs y reporte privado al validar. Cambios posteriores de fuente obligan a revisar el contrato antes de ejecutar.
