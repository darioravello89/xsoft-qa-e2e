---
{"id":"XG-CUO-004","title":"Evitar cobrar dos veces la misma cuota","product":"xgestion","module":"cuenta-corriente","tags":["xgestion","regression","cuenta-corriente","cuotas","cobros","recuperacion"],"status":"planned"}
---

# XG-CUO-004 — Evitar cobrar dos veces la misma cuota

## Objetivo

Mantener un solo pago aunque se repita la acción o se vuelva a abrir el cobro.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 3.**
Ver [mapa de cuentas corrientes y cuotas](../../docs/cuentas-corrientes.md).
Sin suite Robot, seed automático ni validación real del JAR. Los resultados son criterios esperados; las variantes con regla pendiente no se aprueban por observar la aplicación.

## Precondiciones y datos

- Windows QA exclusivo, offline, paquete privado saneado y escritorio visible. Operaciones locales, sin emisión fiscal, pagos externos, envío de correo ni impresión física.
- Todos los datos QA-CCC/QA-CCP/QA-CUO/QA-CTA son **propuestas sintéticas pendientes de seed/baseline**. `catalogo-comercial-v1` no certifica clientes, proveedores, saldos, cronogramas o movimientos de estas fichas.
- Declarar empresa, sucursal, puesto, operador, cliente/proveedor, moneda, medio y fecha. Sin promociones, impuestos, recargos, descuentos ni cuotas salvo indicación expresa; preservar una cuenta de control. El saldo por persona puede consolidar sucursales de una misma empresa: registrar el alcance del filtro.
- QA-CUO-D con una cuota ARS 1.000 pendiente; un puesto y una misma base QA.
- Variante de dos ventanas/sesiones sólo con laboratorio compartido aislado y autorizado. No extrapolar bloqueo de una base a sincronización entre bases offline.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Abrir el cobro y confirmar el total; repetir la acción mientras procesa. | La interfaz protege el registro en curso; no permite iniciar un segundo cobro del mismo formulario. |
| Esperar confirmación y consultar la cuota. | Estado pagada, saldo ARS 0 y una sola cancelación de deuda ARS 1.000. |
| Volver a abrir la consulta e intentar cobrar la misma cuota pagada. | No admite otro pago; historial y saldo permanecen iguales. |
| En variante de concurrencia preparada, intentar confirmar desde una vista desactualizada. | Sólo una confirmación produce el pago; la otra informa que ya no es cobrable. Variante bloqueada hasta disponer de ese laboratorio. |

## Variantes y dependencias

Reintento después de resultado ambiguo y misma cuota visible en dos consultas. Concurrencia real no se acredita con repetir clics en una sola ventana. No asumir que existe un recibo o ingreso financiero adicional por intento rechazado.

Antes de automatizar: preparar baseline reproducible, acordar los oráculos pendientes y calibrar selectores/atajos para el SHA256 del JAR. No usar coordenadas fijas ni extender a estas pantallas la autorización de doble clic otorgada para Venta. Las variantes entre empresas/puestos y de fallo/concurrencia requieren su propio laboratorio.

## Evidencia y recuperación

Identificar cuota por venta, número y contexto; contar cancelaciones efectivas por identidad. Si el resultado se pierde, consultar antes de reintentar y no realizar otro abono manual.

Conservar primero evidencia y conciliar el estado ante una confirmación ambigua. Cancelar o retomar por la interfaz según el caso; no cargar otro pago ni corregir registros comerciales para forzar un aprobado. Restaurar baseline antes de otra variante. Toda escritura preparatoria pertenece al mecanismo de seed autorizado, no a los pasos E2E.

Registrar JAR/SHA256, commit del harness, paquete, perfil, variante, identidades saneadas e informe privado. INFO resume, DEBUG muestra pasos de negocio y TRACE detalle técnico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia; causa no determinada si no está demostrada. No registrar credenciales, filas completas ni configuración privada.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a XGestion2:

- `src/ModuloFinanzas/Vistas/FormCobroCuotaVenta.java:234-319`.
- `src/ModuloVentas/Servicios/VentaCuotasService.java:488-542`.
- `src/ModuloVentas/Servicios/VentaCuotasRepository.java:33-59`.
- `test/ModuloVentas/Servicios/VentaCuotasPersistenciaTest.java:28-43`.
- `test/ModuloFinanzas/Vistas/CobroCuotaVentaWorkerTest.java:17-78`.

Las fuentes y tests citados orientan reglas/riesgos; no equivalen a ejecución E2E. Los criterios financieros pendientes necesitan una definición previa independiente de los importes observados.
