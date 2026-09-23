---
{"id":"XG-CCC-005","title":"Respetar límites de crédito y permisos sin perder la venta","product":"xgestion","module":"cuenta-corriente","tags":["xgestion","regression","cuenta-corriente","ctacte-clientes","permisos","monedas","ventas","recuperacion"],"status":"planned"}
---

# XG-CCC-005 — Respetar límites de crédito y permisos sin perder la venta

## Objetivo

Permitir el crédito disponible y rechazar el exceso conservando la operación para corregirla.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 3.**
Ver [mapa de cuentas corrientes y cuotas](../../docs/cuentas-corrientes.md).
Sin suite Robot, seed automático ni validación real del JAR. Los resultados son criterios esperados; las variantes con regla pendiente no se aprueban por observar la aplicación.

## Precondiciones y datos

- Windows QA exclusivo, offline, paquete privado saneado y escritorio visible. Operaciones locales, sin emisión fiscal, pagos externos, envío de correo ni impresión física.
- Todos los datos QA-CCC/QA-CCP/QA-CUO/QA-CTA son **propuestas sintéticas pendientes de seed/baseline**. `catalogo-comercial-v1` no certifica clientes, proveedores, saldos, cronogramas o movimientos de estas fichas.
- Declarar empresa, sucursal, puesto, operador, cliente/proveedor, moneda, medio y fecha. Sin promociones, impuestos, recargos, descuentos ni cuotas salvo indicación expresa; preservar una cuenta de control. El saldo por persona puede consolidar sucursales de una misma empresa: registrar el alcance del filtro.
- QA-CCC-LIM con límite ARS 2.000 y saldo deudor ARS 1.500; venta ARS 500. Variante venta ARS 500,01.
- Perfiles independientes de operador autorizado/restringido y límites ARS/USD. Permisos concretos y acceso al circuito pendientes de acordar y calibrar; no hay excepción de supervisor demostrada para exceder el límite.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Con el operador autorizado, cerrar la venta de ARS 500 a crédito. | Alcanza ARS 2.000 exactos y se permite el cierre una sola vez. |
| Restaurar baseline y pedir crédito por ARS 500,01. | Se informa exceso ARS 0,01; venta abierta, deuda ARS 1.500, sin cobro ni cierre definitivo. |
| Corregir la operación hasta ARS 500 y reintentar. | Cierre permitido con deuda final ARS 2.000; no quedan movimientos del intento rechazado. |
| Repetir con el perfil restringido definido. | No consigue la operación que su permiso prohíbe; no cambia venta/deuda por intentar acceder. Variante bloqueada hasta identificar permiso y expectativa concretos. |

## Variantes y dependencias

Límite cero sin techo; límite propio frente a predeterminado; saldo a favor reduce deuda proyectada; anticipo reduce nueva deuda; límites independientes ARS/USD. Configuración inválida o error al consultar saldo conserva venta. No usar rol supervisor como bypass de límite sin una regla documentada.

Antes de automatizar: preparar baseline reproducible, acordar los oráculos pendientes y calibrar selectores/atajos para el SHA256 del JAR. No usar coordenadas fijas ni extender a estas pantallas la autorización de doble clic otorgada para Venta. Las variantes entre empresas/puestos y de fallo/concurrencia requieren su propio laboratorio.

## Evidencia y recuperación

Separar rechazo comercial del bloqueo de entorno. Para fallos de consulta hace falta laboratorio reproducible autorizado; comparar datos antes/después y conservar el mensaje.

Conservar primero evidencia y conciliar el estado ante una confirmación ambigua. Cancelar o retomar por la interfaz según el caso; no cargar otro pago ni corregir registros comerciales para forzar un aprobado. Restaurar baseline antes de otra variante. Toda escritura preparatoria pertenece al mecanismo de seed autorizado, no a los pasos E2E.

Registrar JAR/SHA256, commit del harness, paquete, perfil, variante, identidades saneadas e informe privado. INFO resume, DEBUG muestra pasos de negocio y TRACE detalle técnico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia; causa no determinada si no está demostrada. No registrar credenciales, filas completas ni configuración privada.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a XGestion2:

- `src/ModuloFinanzas/Entidades/LimiteCuentaCorrientePolicy.java:11-56`.
- `src/ModuloFinanzas/Vistas/ValidacionLimiteCtaCteDialog.java:25-77`.
- `test/ModuloFinanzas/Entidades/LimiteCuentaCorrientePolicyTest.java:10-37`.

Las fuentes y tests citados orientan reglas/riesgos; no equivalen a ejecución E2E. Los criterios financieros pendientes necesitan una definición previa independiente de los importes observados.
