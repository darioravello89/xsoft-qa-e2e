---
{"id":"XG-CCC-002","title":"Registrar un abono parcial a la cuenta del cliente","product":"xgestion","module":"cuenta-corriente","tags":["xgestion","regression","cuenta-corriente","ctacte-clientes","cobros","caja"],"status":"planned"}
---

# XG-CCC-002 — Registrar un abono parcial a la cuenta del cliente

## Objetivo

Recibir parte de una deuda y poder explicar el saldo que sigue pendiente.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 3.**
Ver [mapa de cuentas corrientes y cuotas](../../docs/cuentas-corrientes.md).
Sin suite Robot, seed automático ni validación real del JAR. Los resultados son criterios esperados; las variantes con regla pendiente no se aprueban por observar la aplicación.

## Precondiciones y datos

- Windows QA exclusivo, offline, paquete privado saneado y escritorio visible. Operaciones locales, sin emisión fiscal, pagos externos, envío de correo ni impresión física.
- Todos los datos QA-CCC/QA-CCP/QA-CUO/QA-CTA son **propuestas sintéticas pendientes de seed/baseline**. `catalogo-comercial-v1` no certifica clientes, proveedores, saldos, cronogramas o movimientos de estas fichas.
- Declarar empresa, sucursal, puesto, operador, cliente/proveedor, moneda, medio y fecha. Sin promociones, impuestos, recargos, descuentos ni cuotas salvo indicación expresa; preservar una cuenta de control. El saldo por persona puede consolidar sucursales de una misma empresa: registrar el alcance del filtro.
- QA-CCC-A con deuda ARS 2.000; efectivo sin recargos; abono ARS 500, nota Abono QA y fecha/hora conocidas.
- Usar Nuevo Pago que abre el formulario individual de cuenta corriente; hay otra entrada con el mismo texto que abre Venta y necesita una variante/calibración distinta.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Abrir la cuenta y el formulario de pago manual. | Cliente QA-CCC-A y deuda ARS 2.000; formulario de pago, no una venta nueva. |
| Completar ARS 500, efectivo, fecha y nota; guardar una vez. | Pago ARS 500 registrado; deuda restante ARS 1.500. |
| Revisar Libro diario y volver a consultar la cuenta. | Ingreso financiero ARS 500 con el medio, fecha y contexto declarados; un solo abono en la cuenta. |
| Consultar un segundo cliente de control. | Sus movimientos y su saldo permanecen iguales. |

## Variantes y dependencias

Repetir con medio manual alternativo sin integración y deuda formada por dos ventas. Este abono es global a la cuenta: no afirmar cancelación de una factura particular ni imputación FIFO. Recargos/descuentos del medio necesitan un perfil y cálculo independiente previo.

Antes de automatizar: preparar baseline reproducible, acordar los oráculos pendientes y calibrar selectores/atajos para el SHA256 del JAR. No usar coordenadas fijas ni extender a estas pantallas la autorización de doble clic otorgada para Venta. Las variantes entre empresas/puestos y de fallo/concurrencia requieren su propio laboratorio.

## Evidencia y recuperación

Contrastar el abono y el ingreso financiero, sin sumar columnas de ingreso/egreso como si fueran equivalentes entre caja y cuenta corriente.

Conservar primero evidencia y conciliar el estado ante una confirmación ambigua. Cancelar o retomar por la interfaz según el caso; no cargar otro pago ni corregir registros comerciales para forzar un aprobado. Restaurar baseline antes de otra variante. Toda escritura preparatoria pertenece al mecanismo de seed autorizado, no a los pasos E2E.

Registrar JAR/SHA256, commit del harness, paquete, perfil, variante, identidades saneadas e informe privado. INFO resume, DEBUG muestra pasos de negocio y TRACE detalle técnico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia; causa no determinada si no está demostrada. No registrar credenciales, filas completas ni configuración privada.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a XGestion2:

- `src/ModuloFinanzas/Vistas/FormCuentaCorrienteClienteIndividual.java:188-267`.
- `src/ModuloFinanzas/Entidades/CtaCteCliente.java:130-207`.
- `src/ModuloFinanzas/Vistas/FormCuentaCorrienteCliente.java:385-409`.

Las fuentes y tests citados orientan reglas/riesgos; no equivalen a ejecución E2E. Los criterios financieros pendientes necesitan una definición previa independiente de los importes observados.

