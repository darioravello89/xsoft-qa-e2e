---
{"id":"XG-FIN-001","title":"Conciliar una venta a crédito y su cobro manual parcial","product":"xgestion","module":"conciliacion","tags":["xgestion","regression","conciliacion","integridad-operaciones","cuenta-corriente","cobros","caja","stock"],"status":"planned"}
---

# XG-FIN-001 — Conciliar una venta a crédito y su cobro manual parcial

## Objetivo

Seguir la deuda y el dinero desde la venta hasta el cobro, sin registrar dos ventas ni dos ingresos.

## Estado y alcance

**Pendiente de automatizar (`planned`), prioridad P0.** Etapas 3–4, integridad entre circuitos.
Ver [roadmap de circuitos críticos](../../docs/circuitos-criticos.md). No tiene Robot, seed propio ni evidencia del JAR.

## Precondiciones y datos

- Windows QA aislado, JAR identificado, baseline recuperable y paquete autorizado. Sin fiscal, correo, servicios externos ni impresoras salvo laboratorio expresamente preparado.
- Cliente QA-FIN-C1 sin deuda; artículo QA-FIN-A a ARS 1.000, stock 10; sin anticipo. Caja abierta con fondo ARS 5.000, efectivo, mismo puesto y turno. Se requiere cobro manual de cliente; no cuotas.
- Nombres QA e importes son requisitos públicos de fixtures futuros; no están creados por esta ficha ni garantizados por el seed comercial. Calibración de controles y lecturas por identidad pendientes.
- Definir moneda, concepto, medio, empresa, sucursal, puesto, operador y período antes de ejecutar. No cambiar datos mediante SQL para corregir una operación en curso.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Vender una unidad a cuenta corriente, sin anticipo. | Venta ARS 1.000, stock 9 y deuda del cliente ARS 1.000; no se recibe efectivo por esta venta. |
| 2 | Registrar desde la cuenta del cliente un cobro manual de ARS 400 en efectivo. | Deuda ARS 600; un pago de ARS 400 y un ingreso financiero Cobro a clientes de ARS 400, con el cliente y contexto correctos. |
| 3 | Consultar Libro Diario y el resumen del turno. | Se identifica el cobro de ARS 400 por su origen y medio. El rubro de cobros de cuenta corriente refleja ARS 400; la venta a crédito no se convierte en venta de contado ni se cuenta otra vez el cobro. |
| 4 | Cerrar y volver a abrir las consultas. | Permanecen una venta, un cobro y deuda ARS 600. El fondo más efectivo efectivamente recibido es ARS 5.400; antes de automatizar se calibra cómo lo presenta cada rubro del cierre. |

## Variantes y dependencias

Repetir con deuda previa y cobro total; transferencia manual usa su medio y no aumenta efectivo. Cancelar el diálogo de pago deja deuda ARS 1.000. Las cuotas tienen otro contrato: no heredan este ingreso financiero.

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
- `src/ModuloVentas/Entidades/CajaValores.java:203-283`.
- `src/ModuloFinanzas/Vistas/FormLibroDiario.java:355-404`.
- `test/ModuloFinanzas/Entidades/CtaCteClienteMovimientoFinanzasMonedaPolicyTest.java`.

Registrar build/SHA256 del JAR, perfil, paquete, fecha, responsable, IDs y reporte privado al validar. Cambios posteriores de fuente obligan a revisar el contrato antes de ejecutar.
