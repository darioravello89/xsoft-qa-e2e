---
{"id":"XG-FIN-004","title":"Recuperar un fallo de cobro manual sin deuda o dinero parciales","product":"xgestion","module":"conciliacion","tags":["xgestion","regression","conciliacion","integridad-operaciones","cuenta-corriente","cobros","recuperacion"],"status":"planned"}
---

# XG-FIN-004 — Recuperar un fallo de cobro manual sin deuda o dinero parciales

## Objetivo

Poder volver a cobrar después de un error sin que una parte del pago quede registrada sola.

## Estado y alcance

**Pendiente de automatizar (`planned`), prioridad P0.** Etapas 3–4, integridad entre circuitos.
Ver [roadmap de circuitos críticos](../../docs/circuitos-criticos.md). No tiene Robot, seed propio ni evidencia del JAR.

## Precondiciones y datos

- Windows QA aislado, JAR identificado, baseline recuperable y paquete autorizado. Sin fiscal, correo, servicios externos ni impresoras salvo laboratorio expresamente preparado.
- Cliente QA-FIN-C1 con deuda ARS 1.000 y pago propuesto ARS 400. Preparación pendiente: mecanismo de laboratorio reproducible desde el JAR para fallar la escritura financiera después de iniciar el registro del pago; baseline privado restaurable.
- Nombres QA e importes son requisitos públicos de fixtures futuros; no están creados por esta ficha ni garantizados por el seed comercial. Calibración de controles y lecturas por identidad pendientes.
- Definir moneda, concepto, medio, empresa, sucursal, puesto, operador y período antes de ejecutar. No cambiar datos mediante SQL para corregir una operación en curso.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Registrar saldos e identidades antes del pago. | Deuda ARS 1.000; ningún pago ni ingreso financiero de esta ejecución. |
| 2 | Con el fallo preparado por el mantenedor, confirmar un cobro manual de ARS 400. | La operación no se presenta como completada: deuda ARS 1.000, ningún pago de ARS 400 aislado ni ingreso financiero parcial. |
| 3 | Desactivar el fallo por el procedimiento entregado y comprobar primero si hubo persistencia. | Sólo se permite reintentar tras determinar el estado. Si no puede determinarse, caso bloqueado y evidencia conservada. |
| 4 | Reintentar una vez y volver a consultar. | Deuda ARS 600; un solo pago de ARS 400 y su ingreso financiero de ARS 400. Se puede continuar operando. |

## Variantes y dependencias

Fallo anterior a guardar, error durante escritura y pérdida de confirmación posterior al commit son estados diferentes. En el último, preservar el pago ya registrado y no repetirlo. Sin un mecanismo seguro para producir cada variante, sigue pendiente: un mock no acredita recuperación del JAR.

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
- `src/ModuloFinanzas/Entidades/MovimientoFinanzas.java:190-237`.
- `test/ModuloFinanzas/Entidades/CtaCteClienteMovimientoFinanzasMonedaPolicyTest.java`.

Registrar build/SHA256 del JAR, perfil, paquete, fecha, responsable, IDs y reporte privado al validar. Cambios posteriores de fuente obligan a revisar el contrato antes de ejecutar.
