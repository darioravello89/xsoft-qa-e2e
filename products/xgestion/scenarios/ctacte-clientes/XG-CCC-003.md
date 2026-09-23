---
{"id":"XG-CCC-003","title":"Saldar la deuda del cliente con el importe exacto","product":"xgestion","module":"cuenta-corriente","tags":["xgestion","regression","cuenta-corriente","ctacte-clientes","cobros","caja"],"status":"planned"}
---

# XG-CCC-003 — Saldar la deuda del cliente con el importe exacto

## Objetivo

Registrar el último pago y dejar la cuenta sin deuda.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 3.**
Ver [mapa de cuentas corrientes y cuotas](../../docs/cuentas-corrientes.md).
Sin suite Robot, seed automático ni validación real del JAR. Los resultados son criterios esperados; las variantes con regla pendiente no se aprueban por observar la aplicación.

## Precondiciones y datos

- Windows QA exclusivo, offline, paquete privado saneado y escritorio visible. Operaciones locales, sin emisión fiscal, pagos externos, envío de correo ni impresión física.
- Todos los datos QA-CCC/QA-CCP/QA-CUO/QA-CTA son **propuestas sintéticas pendientes de seed/baseline**. `catalogo-comercial-v1` no certifica clientes, proveedores, saldos, cronogramas o movimientos de estas fichas.
- Declarar empresa, sucursal, puesto, operador, cliente/proveedor, moneda, medio y fecha. Sin promociones, impuestos, recargos, descuentos ni cuotas salvo indicación expresa; preservar una cuenta de control. El saldo por persona puede consolidar sucursales de una misma empresa: registrar el alcance del filtro.
- QA-CCC-A con deuda ARS 1.500 compuesta por movimientos conocidos; efectivo sin recargos; pago exacto ARS 1.500.
- Otro cliente con deuda ARS 700; baseline de caja y de ambos clientes guardado.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Consultar la cuenta antes de cobrar. | Saldo deudor ARS 1.500; el historial permite distinguir deuda y pagos previos. |
| Registrar Nuevo Pago manual por ARS 1.500. | Saldo ARS 0 y un pago por el importe recibido. |
| Cerrar y reabrir la consulta; revisar el cobro. | Sigue saldo ARS 0; ingreso financiero ARS 1.500 una sola vez y cliente de control sin cambios. |

## Variantes y dependencias

Variar deuda de una o varias ventas. Saldo cero global no significa que exista imputación individual por comprobante. No reutilizar el formulario como mecanismo de cobro de una cuota: [XG-CUO-002](../cuotas/XG-CUO-002.md).

Antes de automatizar: preparar baseline reproducible, acordar los oráculos pendientes y calibrar selectores/atajos para el SHA256 del JAR. No usar coordenadas fijas ni extender a estas pantallas la autorización de doble clic otorgada para Venta. Las variantes entre empresas/puestos y de fallo/concurrencia requieren su propio laboratorio.

## Evidencia y recuperación

Registrar saldo inicial, abono, saldo final e ingreso financiero. Un resultado ambiguo de Guardar obliga a conciliar antes de repetir.

Conservar primero evidencia y conciliar el estado ante una confirmación ambigua. Cancelar o retomar por la interfaz según el caso; no cargar otro pago ni corregir registros comerciales para forzar un aprobado. Restaurar baseline antes de otra variante. Toda escritura preparatoria pertenece al mecanismo de seed autorizado, no a los pasos E2E.

Registrar JAR/SHA256, commit del harness, paquete, perfil, variante, identidades saneadas e informe privado. INFO resume, DEBUG muestra pasos de negocio y TRACE detalle técnico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia; causa no determinada si no está demostrada. No registrar credenciales, filas completas ni configuración privada.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a XGestion2:

- `src/ModuloFinanzas/Vistas/FormCuentaCorrienteClienteIndividual.java:188-267`.
- `src/ModuloFinanzas/Entidades/CtaCteCliente.java:130-207`.

Las fuentes y tests citados orientan reglas/riesgos; no equivalen a ejecución E2E. Los criterios financieros pendientes necesitan una definición previa independiente de los importes observados.

