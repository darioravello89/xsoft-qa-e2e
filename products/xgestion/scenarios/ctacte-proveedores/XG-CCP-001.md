---
{"id":"XG-CCP-001","title":"Reconocer la deuda de una compra recibida y su pago inicial","product":"xgestion","module":"cuenta-corriente","tags":["xgestion","regression","cuenta-corriente","ctacte-proveedores","compras"],"status":"planned"}
---

# XG-CCP-001 — Reconocer la deuda de una compra recibida y su pago inicial

## Objetivo

Saber cuánto queda por pagar al proveedor después de confirmar una recepción.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 3.**
Ver [mapa de cuentas corrientes y cuotas](../../docs/cuentas-corrientes.md).
Sin suite Robot, seed automático ni validación real del JAR. Los resultados son criterios esperados; las variantes con regla pendiente no se aprueban por observar la aplicación.

## Precondiciones y datos

- Windows QA exclusivo, offline, paquete privado saneado y escritorio visible. Operaciones locales, sin emisión fiscal, pagos externos, envío de correo ni impresión física.
- Todos los datos QA-CCC/QA-CCP/QA-CUO/QA-CTA son **propuestas sintéticas pendientes de seed/baseline**. `catalogo-comercial-v1` no certifica clientes, proveedores, saldos, cronogramas o movimientos de estas fichas.
- Declarar empresa, sucursal, puesto, operador, cliente/proveedor, moneda, medio y fecha. Sin promociones, impuestos, recargos, descuentos ni cuotas salvo indicación expresa; preservar una cuenta de control. El saldo por persona puede consolidar sucursales de una misma empresa: registrar el alcance del filtro.
- QA-CCP-A sin saldo inicial; remito interno ARS 2.000 y pago inicial ARS 500; producto y stock del perfil REM ya preparado.
- Reutilizar la carga/recepción de [XG-REM-001](../remitos/XG-REM-001.md) y la confirmación de [XG-REM-021](../remitos/XG-REM-021.md); esta ficha añade conciliación de cuenta corriente, no otro recorrido de carga.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Consultar proveedor y remito antes de confirmar la recepción. | Proveedor sin deuda nueva; remito todavía no recibido. |
| Completar la recepción con total ARS 2.000 y pagado ARS 500. | Deuda neta ARS 1.500; se distingue la compra de su pago inicial. |
| Consultar nuevamente proveedor y documento. | Una sola deuda originada por la compra; actualizar no agrega otros ARS 2.000. |
| Abrir otro proveedor de control. | Saldo e historial sin cambios. |

## Variantes y dependencias

Perfil sin pago inicial: deuda ARS 2.000; perfil totalmente pagado: ARS 0. El pago informado en el documento no acredita por sí solo una salida automática de caja: definir el origen efectivo del pago y conciliarlo en el circuito correspondiente antes de aprobar esa variante.

Antes de automatizar: preparar baseline reproducible, acordar los oráculos pendientes y calibrar selectores/atajos para el SHA256 del JAR. No usar coordenadas fijas ni extender a estas pantallas la autorización de doble clic otorgada para Venta. Las variantes entre empresas/puestos y de fallo/concurrencia requieren su propio laboratorio.

## Evidencia y recuperación

Comprobar compra, importe pagado, saldo del proveedor y vínculo del documento por identidad. No usar recepción como método de preparar baselines de todas las variantes durante un mismo caso.

Conservar primero evidencia y conciliar el estado ante una confirmación ambigua. Cancelar o retomar por la interfaz según el caso; no cargar otro pago ni corregir registros comerciales para forzar un aprobado. Restaurar baseline antes de otra variante. Toda escritura preparatoria pertenece al mecanismo de seed autorizado, no a los pasos E2E.

Registrar JAR/SHA256, commit del harness, paquete, perfil, variante, identidades saneadas e informe privado. INFO resume, DEBUG muestra pasos de negocio y TRACE detalle técnico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia; causa no determinada si no está demostrada. No registrar credenciales, filas completas ni configuración privada.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a XGestion2:

- `src/ModuloProductos/Entidades/Compra.java:405-416`.
- `src/ModuloProductos/Entidades/Compra.java:508-537`.
- `src/ModuloProveedores/Entidades/CtaCteProveedor.java:238-251`.
- `test/ModuloFinanzas/Entidades/CuentaCorrienteSaldoServiceTest.java:23-43`.

Las fuentes y tests citados orientan reglas/riesgos; no equivalen a ejecución E2E. Los criterios financieros pendientes necesitan una definición previa independiente de los importes observados.

