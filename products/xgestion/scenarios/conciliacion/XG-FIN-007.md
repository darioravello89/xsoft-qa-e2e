---
{"id":"XG-FIN-007","title":"Conservar la moneda histórica entre venta, deuda y consultas","product":"xgestion","module":"conciliacion","tags":["xgestion","regression","conciliacion","integridad-operaciones","monedas","cuenta-corriente","comprobantes"],"status":"planned"}
---

# XG-FIN-007 — Conservar la moneda histórica entre venta, deuda y consultas

## Objetivo

Mantener la deuda original y la cotización del documento al cambiar condiciones para operaciones nuevas.

## Estado y alcance

**Pendiente de automatizar (`planned`), prioridad P0.** Etapas 3–4, integridad entre circuitos.
Ver [roadmap de circuitos críticos](../../docs/circuitos-criticos.md). No tiene Robot, seed propio ni evidencia del JAR.

## Precondiciones y datos

- Windows QA aislado, JAR identificado, baseline recuperable y paquete autorizado. Sin fiscal, correo, servicios externos ni impresoras salvo laboratorio expresamente preparado.
- Documento cerrado QA-FIN-USD por USD 100, cotización histórica ARS 1.000/USD y equivalente guardado ARS 100.000; sin pago. Otro movimiento ARS 2.000. Preparar segunda condición vigente de ARS 1.500/USD sin reescribir el histórico; mecanismo de cambio y baseline autorizados pendientes.
- Nombres QA e importes son requisitos públicos de fixtures futuros; no están creados por esta ficha ni garantizados por el seed comercial. Calibración de controles y lecturas por identidad pendientes.
- Definir moneda, concepto, medio, empresa, sucursal, puesto, operador y período antes de ejecutar. No cambiar datos mediante SQL para corregir una operación en curso.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Consultar documento, cuenta del cliente y resumen por moneda. | Documento USD 100, deuda USD 100 y deuda ARS 2.000 separadas; nunca saldo nominal 2.100. |
| 2 | Con la nueva cotización vigente, volver a consultar el documento histórico. | Se conservan USD 100 y la fotografía histórica de ARS 100.000. No sustituirla por ARS 150.000. |
| 3 | Consultar el resumen exportado localmente con el mismo filtro. | Moneda, importe original y saldo coinciden con la pantalla. Un equivalente a cotización actual, si el informe lo ofrece, debe identificarse como valoración actual separada. |
| 4 | Abrir una operación nueva sin confirmar y luego cancelarla. | Puede usar las condiciones vigentes según su perfil; no modifica el documento ni las deudas anteriores. |

## Variantes y dependencias

ARS legado sin ID de moneda, precisión/redondeo y pago posterior requieren sus perfiles. No inferir conversión automática ni compensación entre saldos ARS/USD. No enviar correos ni enlaces públicos durante este caso.

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
- `src/ModuloFinanzas/Entidades/CuentaCorrienteMonedaResumen.java`.
- `test/ModuloFinanzas/Vistas/CtaCteClienteEdicionFotoMonedaPolicyTest.java`.
- `test/ModuloVentas/Entidades/TicketVentaPresupuestoCotizacionTest.java`.

Registrar build/SHA256 del JAR, perfil, paquete, fecha, responsable, IDs y reporte privado al validar. Cambios posteriores de fuente obligan a revisar el contrato antes de ejecutar.
