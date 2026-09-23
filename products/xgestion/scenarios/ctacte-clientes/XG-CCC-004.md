---
{"id":"XG-CCC-004","title":"Conservar un pago mayor a la deuda como saldo a favor","product":"xgestion","module":"cuenta-corriente","tags":["xgestion","regression","cuenta-corriente","ctacte-clientes","cobros","caja"],"status":"planned"}
---

# XG-CCC-004 — Conservar un pago mayor a la deuda como saldo a favor

## Objetivo

Distinguir una cuenta saldada de dinero del cliente disponible a su favor.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 3.**
Ver [mapa de cuentas corrientes y cuotas](../../docs/cuentas-corrientes.md).
Sin suite Robot, seed automático ni validación real del JAR. Los resultados son criterios esperados; las variantes con regla pendiente no se aprueban por observar la aplicación.

## Precondiciones y datos

- Windows QA exclusivo, offline, paquete privado saneado y escritorio visible. Operaciones locales, sin emisión fiscal, pagos externos, envío de correo ni impresión física.
- Todos los datos QA-CCC/QA-CCP/QA-CUO/QA-CTA son **propuestas sintéticas pendientes de seed/baseline**. `catalogo-comercial-v1` no certifica clientes, proveedores, saldos, cronogramas o movimientos de estas fichas.
- Declarar empresa, sucursal, puesto, operador, cliente/proveedor, moneda, medio y fecha. Sin promociones, impuestos, recargos, descuentos ni cuotas salvo indicación expresa; preservar una cuenta de control. El saldo por persona puede consolidar sucursales de una misma empresa: registrar el alcance del filtro.
- QA-CCC-A con deuda ARS 1.000; pago manual ARS 1.200. Segunda operación a crédito ARS 500 sin anticipo.
- Límite declarado suficiente, sin cuotas ni devoluciones; medios sin recargos.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Registrar el pago de ARS 1.200. | La cuenta queda con saldo ARS -200, equivalente a ARS 200 a favor del cliente; ingreso financiero por ARS 1.200. |
| Consultar la cuenta antes de iniciar otra venta. | El crédito no se presenta como nueva deuda de ARS 200 ni desaparece al actualizar. |
| Cerrar una nueva venta a crédito de ARS 500. | Deuda neta ARS 300; la nueva venta no registra otros ARS 200 como dinero recibido. |
| Reabrir el historial. | Se distinguen pago ARS 1.200 y nuevo cargo ARS 500, sin consumir el crédito dos veces. |

## Variantes y dependencias

Perfil alternativo: anticipo con deuda inicial cero. El saldo a favor se aplica en el balance global; no asumir un botón de aplicar crédito a factura. Si la política comercial del paquete limita sobrepagos, acordar ese perfil antes de automatizar esta variante.

Antes de automatizar: preparar baseline reproducible, acordar los oráculos pendientes y calibrar selectores/atajos para el SHA256 del JAR. No usar coordenadas fijas ni extender a estas pantallas la autorización de doble clic otorgada para Venta. Las variantes entre empresas/puestos y de fallo/concurrencia requieren su propio laboratorio.

## Evidencia y recuperación

Contrastar signo y significado mostrado, saldo y caja. La aceptación comercial de anticipos debe quedar declarada; no inferirla de que una entrada numérica lo permita.

Conservar primero evidencia y conciliar el estado ante una confirmación ambigua. Cancelar o retomar por la interfaz según el caso; no cargar otro pago ni corregir registros comerciales para forzar un aprobado. Restaurar baseline antes de otra variante. Toda escritura preparatoria pertenece al mecanismo de seed autorizado, no a los pasos E2E.

Registrar JAR/SHA256, commit del harness, paquete, perfil, variante, identidades saneadas e informe privado. INFO resume, DEBUG muestra pasos de negocio y TRACE detalle técnico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia; causa no determinada si no está demostrada. No registrar credenciales, filas completas ni configuración privada.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a XGestion2:

- `src/ModuloFinanzas/Vistas/FormCuentaCorrienteClienteIndividual.java:188-267`.
- `src/ModuloFinanzas/Entidades/CtaCteCliente.java:130-207`.
- `src/ModuloFinanzas/Entidades/CuentaCorrienteSaldoService.java:41-70`.
- `test/ModuloFinanzas/Entidades/LimiteCuentaCorrientePolicyTest.java:22-31`.

Las fuentes y tests citados orientan reglas/riesgos; no equivalen a ejecución E2E. Los criterios financieros pendientes necesitan una definición previa independiente de los importes observados.

