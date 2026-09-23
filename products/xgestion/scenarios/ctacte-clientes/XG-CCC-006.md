---
{"id":"XG-CCC-006","title":"Mantener separadas las deudas y los pagos en ARS y USD","product":"xgestion","module":"cuenta-corriente","tags":["xgestion","regression","cuenta-corriente","ctacte-clientes","monedas","cobros"],"status":"planned"}
---

# XG-CCC-006 — Mantener separadas las deudas y los pagos en ARS y USD

## Objetivo

Saber cuánto debe el cliente en cada moneda sin sumar importes incompatibles.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 3.**
Ver [mapa de cuentas corrientes y cuotas](../../docs/cuentas-corrientes.md).
Sin suite Robot, seed automático ni validación real del JAR. Los resultados son criterios esperados; las variantes con regla pendiente no se aprueban por observar la aplicación.

## Precondiciones y datos

- Windows QA exclusivo, offline, paquete privado saneado y escritorio visible. Operaciones locales, sin emisión fiscal, pagos externos, envío de correo ni impresión física.
- Todos los datos QA-CCC/QA-CCP/QA-CUO/QA-CTA son **propuestas sintéticas pendientes de seed/baseline**. `catalogo-comercial-v1` no certifica clientes, proveedores, saldos, cronogramas o movimientos de estas fichas.
- Declarar empresa, sucursal, puesto, operador, cliente/proveedor, moneda, medio y fecha. Sin promociones, impuestos, recargos, descuentos ni cuotas salvo indicación expresa; preservar una cuenta de control. El saldo por persona puede consolidar sucursales de una misma empresa: registrar el alcance del filtro.
- QA-CCC-M con deuda ARS 15.000 y deuda USD 25, sin cuotas; pago manual USD 10, cotización del perfil ARS 1.200/USD.
- Movimientos históricos USD con cotización guardada distinta de la actual y otro cliente de control. Preparación por origen y moneda pendiente.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Consultar los movimientos y el resumen del cliente. | Se muestran ARS 15.000 y USD 25 separados; no un total nominal de 15.025. |
| Registrar pago USD 10 con la cotización declarada. | Quedan ARS 15.000 y USD 15; el pago conserva USD 10 y su equivalente operativo ARS 12.000. |
| Consultar el ingreso financiero del pago y el historial. | Ingreso con foto monetaria del cobro; la cotización nueva no reescribe los importes originales de las deudas históricas. |
| Reabrir la consulta. | Saldos por moneda iguales y movimientos del cliente de control intactos. |

## Variantes y dependencias

ARS solamente, USD solamente, combinación y registros antiguos sin moneda (tratamiento ARS). No generalizar este pago USD a cancelación cruzada de deuda ARS; la conversión explícita entre deuda y cobro se cubre para cuotas en CUO-002.

Antes de automatizar: preparar baseline reproducible, acordar los oráculos pendientes y calibrar selectores/atajos para el SHA256 del JAR. No usar coordenadas fijas ni extender a estas pantallas la autorización de doble clic otorgada para Venta. Las variantes entre empresas/puestos y de fallo/concurrencia requieren su propio laboratorio.

## Evidencia y recuperación

Comprobar importes originales y equivalentes por separado, moneda, cotización y contexto. No aprobar una pantalla que muestre un único total mixto sin definición.

Conservar primero evidencia y conciliar el estado ante una confirmación ambigua. Cancelar o retomar por la interfaz según el caso; no cargar otro pago ni corregir registros comerciales para forzar un aprobado. Restaurar baseline antes de otra variante. Toda escritura preparatoria pertenece al mecanismo de seed autorizado, no a los pasos E2E.

Registrar JAR/SHA256, commit del harness, paquete, perfil, variante, identidades saneadas e informe privado. INFO resume, DEBUG muestra pasos de negocio y TRACE detalle técnico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia; causa no determinada si no está demostrada. No registrar credenciales, filas completas ni configuración privada.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a XGestion2:

- `src/ModuloFinanzas/Vistas/FormCuentaCorrienteClienteIndividual.java:188-267`.
- `src/ModuloFinanzas/Entidades/CtaCteCliente.java:130-207`.
- `src/ModuloFinanzas/Entidades/CuentaCorrienteMonedaResumen.java:16-55`.
- `src/ModuloFinanzas/Vistas/FormCuentaCorrienteCliente.java:1302-1338`.
- `test/ModuloFinanzas/Vistas/FormCuentaCorrienteClienteMonedaPolicyTest.java:18-72`.

Las fuentes y tests citados orientan reglas/riesgos; no equivalen a ejecución E2E. Los criterios financieros pendientes necesitan una definición previa independiente de los importes observados.

