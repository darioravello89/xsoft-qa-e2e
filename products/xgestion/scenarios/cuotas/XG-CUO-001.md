---
{"id":"XG-CUO-001","title":"Crear un plan con anticipo y redondeo exacto de las cuotas","product":"xgestion","module":"cuenta-corriente","tags":["xgestion","regression","cuenta-corriente","cuotas","ventas","cobros","monedas"],"status":"planned"}
---

# XG-CUO-001 — Crear un plan con anticipo y redondeo exacto de las cuotas

## Objetivo

Financiar sólo el saldo restante y conocer un cronograma cuya suma coincide con la venta.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 3.**
Ver [mapa de cuentas corrientes y cuotas](../../docs/cuentas-corrientes.md).
Sin suite Robot, seed automático ni validación real del JAR. Los resultados son criterios esperados; las variantes con regla pendiente no se aprueban por observar la aplicación.

## Precondiciones y datos

- Windows QA exclusivo, offline, paquete privado saneado y escritorio visible. Operaciones locales, sin emisión fiscal, pagos externos, envío de correo ni impresión física.
- Todos los datos QA-CCC/QA-CCP/QA-CUO/QA-CTA son **propuestas sintéticas pendientes de seed/baseline**. `catalogo-comercial-v1` no certifica clientes, proveedores, saldos, cronogramas o movimientos de estas fichas.
- Declarar empresa, sucursal, puesto, operador, cliente/proveedor, moneda, medio y fecha. Sin promociones, impuestos, recargos, descuentos ni cuotas salvo indicación expresa; preservar una cuenta de control. El saldo por persona puede consolidar sucursales de una misma empresa: registrar el alcance del filtro.
- QA-CUO-A; venta ARS 120, anticipo ARS 20, capital a financiar ARS 100; tres cuotas sin intereses, gastos ni mora y redondeo del plan a dos decimales.
- Plan y fechas reproducibles pendientes de seed. Financiación habilitada; para USD requiere el perfil explícito venta.cuotas.multimoneda.enabled=true.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Seleccionar el cliente, preparar la venta y calcular el plan de tres cuotas. | Anticipo ARS 20 y cuotas ARS 33,33/33,33/33,34; suma financiada ARS 100, total ARS 120. |
| Revisar vencimientos y confirmar la venta con ese plan. | Una venta y un cronograma de tres cuotas; deuda nueva ARS 100, anticipo contabilizado una sola vez. |
| Consultar Resumen Cuotas y cuenta corriente. | Las tres cuotas suman ARS 100; no queda deuda ARS 80 por volver a restar el anticipo. |
| En baseline separado, cancelar el plan antes de cerrar la venta. | No se registra un cronograma definitivo ni un cobro por sólo calcular el plan. |

## Variantes y dependencias

Sin anticipo, anticipo elevado, interés/gastos con cálculo externo acordado y USD con cotización válida. Si cambia total/moneda/anticipo después de calcular, debe recalcularse antes de cerrar; conservar venta ante rechazo. No asumir que habilitar cuotas USD está activo por defecto.

Antes de automatizar: preparar baseline reproducible, acordar los oráculos pendientes y calibrar selectores/atajos para el SHA256 del JAR. No usar coordenadas fijas ni extender a estas pantallas la autorización de doble clic otorgada para Venta. Las variantes entre empresas/puestos y de fallo/concurrencia requieren su propio laboratorio.

## Evidencia y recuperación

Conciliar venta, anticipo, cronograma, fechas y deuda. El cobro del anticipo pertenece al cierre de venta; no extrapolar el movimiento neutro de cuenta corriente como un nuevo pago físico.

Conservar primero evidencia y conciliar el estado ante una confirmación ambigua. Cancelar o retomar por la interfaz según el caso; no cargar otro pago ni corregir registros comerciales para forzar un aprobado. Restaurar baseline antes de otra variante. Toda escritura preparatoria pertenece al mecanismo de seed autorizado, no a los pasos E2E.

Registrar JAR/SHA256, commit del harness, paquete, perfil, variante, identidades saneadas e informe privado. INFO resume, DEBUG muestra pasos de negocio y TRACE detalle técnico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia; causa no determinada si no está demostrada. No registrar credenciales, filas completas ni configuración privada.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a XGestion2:

- `src/ModuloVentas/Servicios/VentaCuotasService.java:129-207`.
- `src/ModuloFinanzas/Vistas/ValidacionLimiteCtaCteDialog.java:29-42`.
- `src/ModuloVentas/Servicios/VentaCuotasService.java:42-65`.
- `test/ModuloVentas/Servicios/VentaCuotasMonedaPolicyTest.java:40-55`.

Las fuentes y tests citados orientan reglas/riesgos; no equivalen a ejecución E2E. Los criterios financieros pendientes necesitan una definición previa independiente de los importes observados.
