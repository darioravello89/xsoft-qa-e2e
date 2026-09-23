---
{"id":"XG-CCC-007","title":"Corregir una deuda manual conservando su historia monetaria","product":"xgestion","module":"cuenta-corriente","tags":["xgestion","regression","cuenta-corriente","ctacte-clientes","monedas","recuperacion"],"status":"planned"}
---

# XG-CCC-007 — Corregir una deuda manual conservando su historia monetaria

## Objetivo

Corregir un movimiento editable y recalcular el saldo sin duplicar el importe anterior.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 4.**
Ver [mapa de cuentas corrientes y cuotas](../../docs/cuentas-corrientes.md).
Sin suite Robot, seed automático ni validación real del JAR. Los resultados son criterios esperados; las variantes con regla pendiente no se aprueban por observar la aplicación.

## Precondiciones y datos

- Windows QA exclusivo, offline, paquete privado saneado y escritorio visible. Operaciones locales, sin emisión fiscal, pagos externos, envío de correo ni impresión física.
- Todos los datos QA-CCC/QA-CCP/QA-CUO/QA-CTA son **propuestas sintéticas pendientes de seed/baseline**. `catalogo-comercial-v1` no certifica clientes, proveedores, saldos, cronogramas o movimientos de estas fichas.
- Declarar empresa, sucursal, puesto, operador, cliente/proveedor, moneda, medio y fecha. Sin promociones, impuestos, recargos, descuentos ni cuotas salvo indicación expresa; preservar una cuenta de control. El saldo por persona puede consolidar sucursales de una misma empresa: registrar el alcance del filtro.
- QA-CCC-EDIT: deuda manual ARS 2.000 y pago posterior ARS 500; corregir deuda a ARS 3.000.
- Variante independiente USD: deuda manual USD 10 a cotización histórica 1.200; cotización actual 1.500; corregir a USD 12. No usar una deuda generada por venta.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Abrir la deuda manual editable y cambiar su importe de ARS 2.000 a ARS 3.000. | Guardar reemplaza el importe anterior; saldo final ARS 2.500, no ARS 4.500. |
| Reabrir el movimiento y el pago posterior. | Una deuda corregida y el pago original de ARS 500, con el saldo reencadenado. |
| En baseline USD, editar el importe a USD 12. | Conserva USD y cotización histórica 1.200; equivalente operativo ARS 14.400, sin recalcular a 1.500. |
| Cerrar sin guardar otra modificación. | Importes y saldo permanecen como en la última edición guardada. |

## Variantes y dependencias

Cambio de fecha/hora, mismo instante en dos movimientos y guardar sin cambios. Edición de pago ya recibido exige definir cómo conciliar el ingreso financiero asociado: la actualización leída modifica cuenta corriente, no demuestra actualización automática de caja. Esa variante permanece bloqueada hasta acordar el circuito.

Antes de automatizar: preparar baseline reproducible, acordar los oráculos pendientes y calibrar selectores/atajos para el SHA256 del JAR. No usar coordenadas fijas ni extender a estas pantallas la autorización de doble clic otorgada para Venta. Las variantes entre empresas/puestos y de fallo/concurrencia requieren su propio laboratorio.

## Evidencia y recuperación

Contrastar movimiento original/corregido, orden cronológico, moneda, fecha y saldo. No tomar el recálculo observado como oráculo.

Conservar primero evidencia y conciliar el estado ante una confirmación ambigua. Cancelar o retomar por la interfaz según el caso; no cargar otro pago ni corregir registros comerciales para forzar un aprobado. Restaurar baseline antes de otra variante. Toda escritura preparatoria pertenece al mecanismo de seed autorizado, no a los pasos E2E.

Registrar JAR/SHA256, commit del harness, paquete, perfil, variante, identidades saneadas e informe privado. INFO resume, DEBUG muestra pasos de negocio y TRACE detalle técnico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia; causa no determinada si no está demostrada. No registrar credenciales, filas completas ni configuración privada.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a XGestion2:

- `src/ModuloFinanzas/Vistas/FormCuentaCorrienteClienteIndividual.java:294-346`.
- `src/ModuloFinanzas/Entidades/CtaCteCliente.java:458-512`.
- `test/ModuloFinanzas/Vistas/CtaCteClienteEdicionFotoMonedaPolicyTest.java:14-52`.
- `test/ModuloFinanzas/Entidades/CuentaCorrienteSaldoServiceTest.java:12-21`.

Las fuentes y tests citados orientan reglas/riesgos; no equivalen a ejecución E2E. Los criterios financieros pendientes necesitan una definición previa independiente de los importes observados.

