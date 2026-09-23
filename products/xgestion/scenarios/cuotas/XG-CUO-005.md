---
{"id":"XG-CUO-005","title":"Rechazar un cobro inválido o fallido sin perder la cuota","product":"xgestion","module":"cuenta-corriente","tags":["xgestion","regression","cuenta-corriente","cuotas","recuperacion","monedas","cobros"],"status":"planned"}
---

# XG-CUO-005 — Rechazar un cobro inválido o fallido sin perder la cuota

## Objetivo

Corregir importe o cotización y recuperar un fallo conservando la deuda hasta un pago válido.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 3.**
Ver [mapa de cuentas corrientes y cuotas](../../docs/cuentas-corrientes.md).
Sin suite Robot, seed automático ni validación real del JAR. Los resultados son criterios esperados; las variantes con regla pendiente no se aprueban por observar la aplicación.

## Precondiciones y datos

- Windows QA exclusivo, offline, paquete privado saneado y escritorio visible. Operaciones locales, sin emisión fiscal, pagos externos, envío de correo ni impresión física.
- Todos los datos QA-CCC/QA-CCP/QA-CUO/QA-CTA son **propuestas sintéticas pendientes de seed/baseline**. `catalogo-comercial-v1` no certifica clientes, proveedores, saldos, cronogramas o movimientos de estas fichas.
- Declarar empresa, sucursal, puesto, operador, cliente/proveedor, moneda, medio y fecha. Sin promociones, impuestos, recargos, descuentos ni cuotas salvo indicación expresa; preservar una cuenta de control. El saldo por persona puede consolidar sucursales de una misma empresa: registrar el alcance del filtro.
- QA-CUO-R con cuota USD 10 pendiente; cotización mostrada 1.500 y cobro esperado ARS 15.000.
- Baselines independientes de importe insuficiente, cotización cambiada a 1.800, cotización inválida y fallo controlado de persistencia. Fallos y cambio de cotización requieren mecanismo de laboratorio autorizado; no improvisar escrituras en producción.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Intentar cobrar ARS 14.999. | Se rechaza por no ser pago completo; cuota pendiente USD 10 y sin cancelación parcial. |
| En perfil de cambio de cotización, confirmar con el valor anterior. | Informa cotización actualizada a 1.800 y nuevo total ARS 18.000; no registra el pago sin reconfirmación. |
| Cancelar y consultar la cuota. | Permanece pendiente USD 10; no se registró dinero por cancelar. |
| En perfil de fallo controlado, provocar error al registrar el movimiento. | No quedan cuota pagada y deuda sin cancelar como estados contradictorios; conserva la deuda y ofrece diagnóstico. Conciliar antes de repetir. |
| Restaurar condición válida, reabrir, confirmar ARS 18.000 a 1.800. | Un pago válido cancela USD 10; los intentos rechazados/fallidos no generan cobros adicionales. |

## Variantes y dependencias

Cotización cero/ausente se rechaza; cuota ARS con cobro USD se rechaza; cliente/empresa ajenos no cambian. Timeout o pérdida de respuesta requieren consulta de estado y evidencia antes de reintentar. La variante de fallo necesita un punto reproducible y conocido, no simular aprobación con dry-run.

Antes de automatizar: preparar baseline reproducible, acordar los oráculos pendientes y calibrar selectores/atajos para el SHA256 del JAR. No usar coordenadas fijas ni extender a estas pantallas la autorización de doble clic otorgada para Venta. Las variantes entre empresas/puestos y de fallo/concurrencia requieren su propio laboratorio.

## Evidencia y recuperación

Conservar mensaje, monto/cotización, estado antes/después y evidencia transaccional saneada. La fuente prueba transacción de cuota/cuenta corriente; no afirmar rollback de sistemas financieros externos no conectados por esta ruta.

Conservar primero evidencia y conciliar el estado ante una confirmación ambigua. Cancelar o retomar por la interfaz según el caso; no cargar otro pago ni corregir registros comerciales para forzar un aprobado. Restaurar baseline antes de otra variante. Toda escritura preparatoria pertenece al mecanismo de seed autorizado, no a los pasos E2E.

Registrar JAR/SHA256, commit del harness, paquete, perfil, variante, identidades saneadas e informe privado. INFO resume, DEBUG muestra pasos de negocio y TRACE detalle técnico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia; causa no determinada si no está demostrada. No registrar credenciales, filas completas ni configuración privada.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a XGestion2:

- `src/ModuloFinanzas/Vistas/FormCobroCuotaVenta.java:234-319`.
- `src/ModuloVentas/Servicios/VentaCuotasService.java:488-542`.
- `src/ModuloVentas/Servicios/VentaCuotasRepository.java:33-59`.
- `test/ModuloVentas/Servicios/VentaCuotasPersistenciaTest.java:35-51`.
- `test/ModuloVentas/Servicios/VentaCuotasPersistenciaTest.java:83-104`.
- `test/ModuloFinanzas/Vistas/CobroCuotaVentaWorkerTest.java:17-78`.

Las fuentes y tests citados orientan reglas/riesgos; no equivalen a ejecución E2E. Los criterios financieros pendientes necesitan una definición previa independiente de los importes observados.
