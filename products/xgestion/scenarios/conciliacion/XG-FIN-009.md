---
{"id":"XG-FIN-009","title":"Confirmar y reabrir sin duplicar una operación monetaria","product":"xgestion","module":"conciliacion","tags":["xgestion","regression","conciliacion","integridad-operaciones","recuperacion","cobros","varios-puestos"],"status":"planned"}
---

# XG-FIN-009 — Confirmar y reabrir sin duplicar una operación monetaria

## Objetivo

Detectar doble registro por confirmación repetida o lectura tardía del resultado.

## Estado y alcance

**Pendiente de automatizar (`planned`), prioridad P0.** Etapas 3–4, integridad entre circuitos.
Ver [roadmap de circuitos críticos](../../docs/circuitos-criticos.md). No tiene Robot, seed propio ni evidencia del JAR.

## Precondiciones y datos

- Windows QA aislado, JAR identificado, baseline recuperable y paquete autorizado. Sin fiscal, correo, servicios externos ni impresoras salvo laboratorio expresamente preparado.
- Baseline por variante: cliente con deuda ARS 1.000 para cobrar ARS 400, o venta simple ARS 1.000 aún no cobrada. Controles accesibles y mecanismo de demora de respuesta pendientes; sólo ventanas/procesos propios. Repetición de confirmación no es autorización para usar coordenadas.
- Nombres QA e importes son requisitos públicos de fixtures futuros; no están creados por esta ficha ni garantizados por el seed comercial. Calibración de controles y lecturas por identidad pendientes.
- Definir moneda, concepto, medio, empresa, sucursal, puesto, operador y período antes de ejecutar. No cambiar datos mediante SQL para corregir una operación en curso.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Confirmar el pago y repetir la activación del control mientras la primera sigue en curso. | Se produce una sola operación: en cobro manual, deuda ARS 600 y un ingreso de ARS 400; en venta, un documento y un cobro de ARS 1.000. |
| 2 | Esperar el resultado con límite y volver a abrir la consulta. | Identidad y efectos persisten una sola vez. Si el resultado es indeterminado, detener los reintentos y conservar evidencia. |
| 3 | Volver a entrar al flujo de la operación ya completada. | No ejecutar de nuevo automáticamente. Un nuevo pago manual legítimo es otra intención: la prueba no exige bloquear todos los cobros del mismo importe. |
| 4 | En el laboratorio específico, repetir con dos ventanas sobre la misma cuota pendiente. | Una cuota sólo se cancela una vez; el segundo intento no agrega deuda/pago. Esta variante queda bloqueada sin preparación de concurrencia y contrato CUO. |

## Variantes y dependencias

Confirmación por teclado, demora antes/después de commit y ventana cerrada tras confirmar. Un pago distinto por el mismo importe no es un duplicado por sí solo. No automatizar la concurrencia sobre una base cotidiana ni dar por validada la variante con el test secuencial.

Las dependencias sin procedimiento reproducible bloquean la variante. Un resultado observado no se convierte automáticamente en el resultado esperado. La aprobación exige todos los pasos y variantes habilitadas del perfil, identificando cuáles siguen pendientes.

## Evidencia y límites

Registrar importes antes/después, identidad de documentos y deltas de deuda, caja, stock y movimientos relevantes. Cada dominio tiene su alcance: dos representaciones técnicas no acreditan dos movimientos de dinero. Conservar lectura acotada y saneada, sin filas completas, credenciales ni datos privados en el repositorio.

INFO muestra caso y resultado; DEBUG acciones de negocio; TRACE controles, esperas y diagnóstico saneado. Todo fallo incluye paso, esperado, observado y evidencia; causa no determinada si no está demostrada. Un dry-run no acredita estos resultados.

## Recuperación

Cancelar las acciones no confirmadas. Ante persistencia incierta, consultar antes de reintentar y no ejecutar compensaciones improvisadas. Conservar evidencia privada, cerrar sólo procesos propios y restaurar el baseline mediante el procedimiento del laboratorio. La anulación de negocio no reemplaza la restauración técnica de datos.

## Anexo técnico y trazabilidad

Fuente inspeccionada: XGestion2 `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`.
Los tests fuente son insumos de reglas/riesgos, no evidencia de ejecución del JAR.

- `src/ModuloFinanzas/Entidades/CtaCteCliente.java:130-200`.
- `src/ModuloVentas/Servicios/VentaCuotasService.java`.
- `test/ModuloVentas/Servicios/VentaCuotasPersistenciaTest.java`.

Registrar build/SHA256 del JAR, perfil, paquete, fecha, responsable, IDs y reporte privado al validar. Cambios posteriores de fuente obligan a revisar el contrato antes de ejecutar.
