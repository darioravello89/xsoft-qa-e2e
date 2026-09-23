---
{"id":"XG-CCP-004","title":"Cancelar un pago y retirar una deuda manual errónea","product":"xgestion","module":"cuenta-corriente","tags":["xgestion","regression","cuenta-corriente","ctacte-proveedores","recuperacion"],"status":"planned"}
---

# XG-CCP-004 — Cancelar un pago y retirar una deuda manual errónea

## Objetivo

Evitar salidas o reducciones de deuda al abandonar una carga, y corregir sólo el movimiento manual elegido.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 3.**
Ver [mapa de cuentas corrientes y cuotas](../../docs/cuentas-corrientes.md).
Sin suite Robot, seed automático ni validación real del JAR. Los resultados son criterios esperados; las variantes con regla pendiente no se aprueban por observar la aplicación.

## Precondiciones y datos

- Windows QA exclusivo, offline, paquete privado saneado y escritorio visible. Operaciones locales, sin emisión fiscal, pagos externos, envío de correo ni impresión física.
- Todos los datos QA-CCC/QA-CCP/QA-CUO/QA-CTA son **propuestas sintéticas pendientes de seed/baseline**. `catalogo-comercial-v1` no certifica clientes, proveedores, saldos, cronogramas o movimientos de estas fichas.
- Declarar empresa, sucursal, puesto, operador, cliente/proveedor, moneda, medio y fecha. Sin promociones, impuestos, recargos, descuentos ni cuotas salvo indicación expresa; preservar una cuenta de control. El saldo por persona puede consolidar sucursales de una misma empresa: registrar el alcance del filtro.
- QA-CCP-CAN con deuda ARS 2.000; pago nuevo en preparación ARS 500.
- Variante separada: deuda manual errónea ARS 400 agregada a la cuenta, saldo ARS 2.400. No es una deuda generada por compra ni Dar baja de la cuenta completa.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Abrir Nuevo pago, completar ARS 500 y cerrar sin Guardar. | Deuda ARS 2.000; no queda pago por ARS 500. |
| En la variante con deuda errónea, abrirla y rechazar Eliminar. | La deuda errónea sigue activa; saldo ARS 2.400. |
| Eliminar esa deuda manual con confirmación. | Saldo ARS 2.000; permanecen los restantes movimientos del proveedor. |
| Actualizar y consultar otro proveedor. | Sin reducción adicional de deuda ni modificación del proveedor de control. |

## Variantes y dependencias

Cancelar antes/después de cambiar fecha o medio. Baja de un pago ya efectuado requiere definir reversión del desembolso; no suponer devolución automática de dinero. Pagos programados/vencimientos tienen estado y acciones distintos: quedan como variante dependiente de un perfil y oráculo propio, no equivalen a guardar este pago manual.

Antes de automatizar: preparar baseline reproducible, acordar los oráculos pendientes y calibrar selectores/atajos para el SHA256 del JAR. No usar coordenadas fijas ni extender a estas pantallas la autorización de doble clic otorgada para Venta. Las variantes entre empresas/puestos y de fallo/concurrencia requieren su propio laboratorio.

## Evidencia y recuperación

Conservar identificación del movimiento, confirmaciones y deltas de cuenta/finanzas. La baja leída desactiva cuenta corriente; no usarla como reparación genérica de caja.

Conservar primero evidencia y conciliar el estado ante una confirmación ambigua. Cancelar o retomar por la interfaz según el caso; no cargar otro pago ni corregir registros comerciales para forzar un aprobado. Restaurar baseline antes de otra variante. Toda escritura preparatoria pertenece al mecanismo de seed autorizado, no a los pasos E2E.

Registrar JAR/SHA256, commit del harness, paquete, perfil, variante, identidades saneadas e informe privado. INFO resume, DEBUG muestra pasos de negocio y TRACE detalle técnico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia; causa no determinada si no está demostrada. No registrar credenciales, filas completas ni configuración privada.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a XGestion2:

- `src/ModuloProveedores/Vistas/FormCuentaCorrienteIndividual.java:164-185`.
- `src/ModuloProveedores/Entidades/CtaCteProveedor.java:343-359`.
- `src/ModuloProveedores/Vistas/FormCuentaCorriente.java:731-758`.
- `src/ModuloProveedores/Vistas/FormCuentaCorrienteIndividual.java:288-316`.
- `src/ModuloProveedores/Entidades/CtaCteProveedor.java:253-359`.
- `test/ModuloProveedores/Entidades/CtaCteProveedorEdicionFotoMonedaPolicyTest.java:14-51`.

Las fuentes y tests citados orientan reglas/riesgos; no equivalen a ejecución E2E. Los criterios financieros pendientes necesitan una definición previa independiente de los importes observados.

