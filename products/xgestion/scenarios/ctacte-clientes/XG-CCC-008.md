---
{"id":"XG-CCC-008","title":"Cancelar un pago en preparación y dar de baja una deuda manual","product":"xgestion","module":"cuenta-corriente","tags":["xgestion","regression","cuenta-corriente","ctacte-clientes","cobros","recuperacion"],"status":"planned"}
---

# XG-CCC-008 — Cancelar un pago en preparación y dar de baja una deuda manual

## Objetivo

Abandonar una carga sin registrar dinero y retirar una deuda manual errónea con confirmación.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 4.**
Ver [mapa de cuentas corrientes y cuotas](../../docs/cuentas-corrientes.md).
Sin suite Robot, seed automático ni validación real del JAR. Los resultados son criterios esperados; las variantes con regla pendiente no se aprueban por observar la aplicación.

## Precondiciones y datos

- Windows QA exclusivo, offline, paquete privado saneado y escritorio visible. Operaciones locales, sin emisión fiscal, pagos externos, envío de correo ni impresión física.
- Todos los datos QA-CCC/QA-CCP/QA-CUO/QA-CTA son **propuestas sintéticas pendientes de seed/baseline**. `catalogo-comercial-v1` no certifica clientes, proveedores, saldos, cronogramas o movimientos de estas fichas.
- Declarar empresa, sucursal, puesto, operador, cliente/proveedor, moneda, medio y fecha. Sin promociones, impuestos, recargos, descuentos ni cuotas salvo indicación expresa; preservar una cuenta de control. El saldo por persona puede consolidar sucursales de una misma empresa: registrar el alcance del filtro.
- QA-CCC-CAN con deuda manual ARS 2.000 y pago histórico ARS 500; saldo ARS 1.500.
- Nuevo pago en preparación por ARS 300; deuda manual errónea adicional ARS 400 para la variante de baja. No usar Dar baja de toda la cuenta ni registros originados por venta.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Abrir un pago ARS 300 y salir sin Guardar. | Saldo ARS 1.500 y ningún ingreso financiero por ARS 300. |
| Con baseline de deuda errónea adicional, abrir ese movimiento y rechazar Eliminar. | La deuda adicional ARS 400 sigue vigente; saldo ARS 1.900. |
| Repetir Eliminar y aceptar sobre la deuda manual elegida. | La deuda errónea deja de participar; saldo ARS 1.500 y pago histórico ARS 500 conservado. |
| Actualizar y revisar el cliente de control. | Sin nuevos cobros ni alteraciones en otras cuentas. |

## Variantes y dependencias

La baja de un pago ya cobrado no equivale a devolver dinero: el método de baja leído sólo desactiva cuenta corriente. Documentar y acordar su reversión de caja antes de habilitar esa variante; no darla por aprobada porque el saldo del cliente cambió. Cancelar un diálogo no es cancelar una venta.

Antes de automatizar: preparar baseline reproducible, acordar los oráculos pendientes y calibrar selectores/atajos para el SHA256 del JAR. No usar coordenadas fijas ni extender a estas pantallas la autorización de doble clic otorgada para Venta. Las variantes entre empresas/puestos y de fallo/concurrencia requieren su propio laboratorio.

## Evidencia y recuperación

Conservar confirmaciones y antes/después de deuda/pagos/finanzas. Confirmación y acceso accesible del editor pendientes de calibrar; no extender autorizaciones previas de doble clic a esta pantalla.

Conservar primero evidencia y conciliar el estado ante una confirmación ambigua. Cancelar o retomar por la interfaz según el caso; no cargar otro pago ni corregir registros comerciales para forzar un aprobado. Restaurar baseline antes de otra variante. Toda escritura preparatoria pertenece al mecanismo de seed autorizado, no a los pasos E2E.

Registrar JAR/SHA256, commit del harness, paquete, perfil, variante, identidades saneadas e informe privado. INFO resume, DEBUG muestra pasos de negocio y TRACE detalle técnico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia; causa no determinada si no está demostrada. No registrar credenciales, filas completas ni configuración privada.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a XGestion2:

- `src/ModuloFinanzas/Vistas/FormCuentaCorrienteClienteIndividual.java:172-184`.
- `src/ModuloFinanzas/Entidades/CtaCteCliente.java:496-512`.
- `src/ModuloFinanzas/Vistas/FormCuentaCorrienteClienteIndividual.java:294-346`.
- `src/ModuloFinanzas/Entidades/CtaCteCliente.java:458-512`.
- `test/ModuloFinanzas/Vistas/CtaCteClienteEdicionFotoMonedaPolicyTest.java:14-52`.
- `test/ModuloFinanzas/Entidades/CuentaCorrienteSaldoServiceTest.java:12-21`.

Las fuentes y tests citados orientan reglas/riesgos; no equivalen a ejecución E2E. Los criterios financieros pendientes necesitan una definición previa independiente de los importes observados.

