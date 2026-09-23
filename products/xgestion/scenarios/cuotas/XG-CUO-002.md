---
{"id":"XG-CUO-002","title":"Cobrar una cuota completa conservando moneda de deuda y de cobro","product":"xgestion","module":"cuenta-corriente","tags":["xgestion","regression","cuenta-corriente","cuotas","cobros","monedas"],"status":"planned"}
---

# XG-CUO-002 — Cobrar una cuota completa conservando moneda de deuda y de cobro

## Objetivo

Cancelar la cuota por su importe exacto aunque una deuda en dólares se cobre en pesos.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 3.**
Ver [mapa de cuentas corrientes y cuotas](../../docs/cuentas-corrientes.md).
Sin suite Robot, seed automático ni validación real del JAR. Los resultados son criterios esperados; las variantes con regla pendiente no se aprueban por observar la aplicación.

## Precondiciones y datos

- Windows QA exclusivo, offline, paquete privado saneado y escritorio visible. Operaciones locales, sin emisión fiscal, pagos externos, envío de correo ni impresión física.
- Todos los datos QA-CCC/QA-CCP/QA-CUO/QA-CTA son **propuestas sintéticas pendientes de seed/baseline**. `catalogo-comercial-v1` no certifica clientes, proveedores, saldos, cronogramas o movimientos de estas fichas.
- Declarar empresa, sucursal, puesto, operador, cliente/proveedor, moneda, medio y fecha. Sin promociones, impuestos, recargos, descuentos ni cuotas salvo indicación expresa; preservar una cuenta de control. El saldo por persona puede consolidar sucursales de una misma empresa: registrar el alcance del filtro.
- QA-CUO-A con cuota USD 10 pendiente; cotización confirmada 1.500; efectivo ARS 15.000. Cotización de origen de la deuda 1.200.
- Baselines separados: cuota ARS 1.000 cobrada ARS 1.000 y cuota USD 10 cobrada USD 10. Sin mora ni recargos del medio.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Abrir el cobro de la cuota USD y elegir ARS. | Muestra deuda USD 10 y cobro ARS 15.000 a cotización 1.500; exige confirmar la cotización. |
| Confirmar el importe completo y registrar una vez. | Cuota pagada, saldo USD 0; pago conserva ARS 15.000/cotización 1.500 y monto cancelado USD 10. |
| Reabrir cuota e historial del cliente. | Se mantiene la deuda original USD y su cancelación USD 10; no cambia a una deuda nominal ARS 15.000. |
| Repetir desde los baselines ARS/ARS y USD/USD. | Cada cuota queda pagada por el total exacto en su moneda, conservando la foto del cobro. |

## Variantes y dependencias

Centavos USD 3,33 a cotización 1.500: pago ARS 4.995. La UI exige pago completo: no presentar abonos parciales como implementados. Cuota ARS no se cobra en USD en la ruta leída. La cuenta corriente y el recibo de cuota no acreditan ingreso automático en Libro diario; la integración de caja está **pendiente de definición/verificación**.

Antes de automatizar: preparar baseline reproducible, acordar los oráculos pendientes y calibrar selectores/atajos para el SHA256 del JAR. No usar coordenadas fijas ni extender a estas pantallas la autorización de doble clic otorgada para Venta. Las variantes entre empresas/puestos y de fallo/concurrencia requieren su propio laboratorio.

## Evidencia y recuperación

Conservar los dos importes y las dos cotizaciones (origen/cobro), estado y saldo. No reconvertir el monto cancelado desde un importe ya redondeado. Conciliar caja sólo con un contrato previo, sin registrar un Nuevo pago adicional para hacer coincidir resultados.

Conservar primero evidencia y conciliar el estado ante una confirmación ambigua. Cancelar o retomar por la interfaz según el caso; no cargar otro pago ni corregir registros comerciales para forzar un aprobado. Restaurar baseline antes de otra variante. Toda escritura preparatoria pertenece al mecanismo de seed autorizado, no a los pasos E2E.

Registrar JAR/SHA256, commit del harness, paquete, perfil, variante, identidades saneadas e informe privado. INFO resume, DEBUG muestra pasos de negocio y TRACE detalle técnico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia; causa no determinada si no está demostrada. No registrar credenciales, filas completas ni configuración privada.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a XGestion2:

- `src/ModuloFinanzas/Vistas/FormCobroCuotaVenta.java:234-319`.
- `src/ModuloVentas/Servicios/VentaCuotasService.java:488-542`.
- `src/ModuloVentas/Servicios/VentaCuotasRepository.java:33-59`.
- `test/ModuloVentas/Servicios/VentaCuotasPersistenciaTest.java:14-27`.
- `test/ModuloVentas/Servicios/VentaCuotasMonedaPolicyTest.java:11-37`.

Las fuentes y tests citados orientan reglas/riesgos; no equivalen a ejecución E2E. Los criterios financieros pendientes necesitan una definición previa independiente de los importes observados.
