---
{"id":"XG-CCP-002","title":"Registrar pagos manuales parciales y totales al proveedor","product":"xgestion","module":"cuenta-corriente","tags":["xgestion","regression","cuenta-corriente","ctacte-proveedores","cobros"],"status":"planned"}
---

# XG-CCP-002 — Registrar pagos manuales parciales y totales al proveedor

## Objetivo

Reducir la deuda correcta cuando se registra un pago ya realizado por el circuito declarado.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 3.**
Ver [mapa de cuentas corrientes y cuotas](../../docs/cuentas-corrientes.md).
Sin suite Robot, seed automático ni validación real del JAR. Los resultados son criterios esperados; las variantes con regla pendiente no se aprueban por observar la aplicación.

## Precondiciones y datos

- Windows QA exclusivo, offline, paquete privado saneado y escritorio visible. Operaciones locales, sin emisión fiscal, pagos externos, envío de correo ni impresión física.
- Todos los datos QA-CCC/QA-CCP/QA-CUO/QA-CTA son **propuestas sintéticas pendientes de seed/baseline**. `catalogo-comercial-v1` no certifica clientes, proveedores, saldos, cronogramas o movimientos de estas fichas.
- Declarar empresa, sucursal, puesto, operador, cliente/proveedor, moneda, medio y fecha. Sin promociones, impuestos, recargos, descuentos ni cuotas salvo indicación expresa; preservar una cuenta de control. El saldo por persona puede consolidar sucursales de una misma empresa: registrar el alcance del filtro.
- QA-CCP-A con deuda ARS 2.000; pagos manuales ARS 500 y ARS 1.500; medio y fecha de cada pago conocidos.
- Perfil de registro manual en cuenta corriente. El origen del dinero se documenta aparte; no registrar el mismo pago también por Egreso de caja sin una regla explícita.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Abrir Nuevo pago de la cuenta del proveedor y registrar ARS 500. | Pago ARS 500; deuda pendiente ARS 1.500. |
| Reabrir la cuenta y registrar el pago restante ARS 1.500. | Deuda ARS 0 y dos pagos distinguibles por fecha/nota/medio. |
| Actualizar y revisar el proveedor de control. | No aparecen pagos adicionales; la cuenta de control no cambia. |

## Variantes y dependencias

Un pago exacto único de ARS 2.000 y un pago mayor ARS 2.200, que deja ARS 200 a favor de la empresa si el perfil comercial admite anticipos. Son movimientos globales; no asignar a una factura concreta sin un flujo real de imputación. La fuente de Nuevo pago manual sólo demuestra escritura en cuenta corriente, no egreso automático en Libro diario.

Antes de automatizar: preparar baseline reproducible, acordar los oráculos pendientes y calibrar selectores/atajos para el SHA256 del JAR. No usar coordenadas fijas ni extender a estas pantallas la autorización de doble clic otorgada para Venta. Las variantes entre empresas/puestos y de fallo/concurrencia requieren su propio laboratorio.

## Evidencia y recuperación

Registrar deuda inicial, pagos y saldo con su significado; documentar expresamente cómo se contabiliza el desembolso. Si esa política no está definida, la conciliación de caja permanece pendiente.

Conservar primero evidencia y conciliar el estado ante una confirmación ambigua. Cancelar o retomar por la interfaz según el caso; no cargar otro pago ni corregir registros comerciales para forzar un aprobado. Restaurar baseline antes de otra variante. Toda escritura preparatoria pertenece al mecanismo de seed autorizado, no a los pasos E2E.

Registrar JAR/SHA256, commit del harness, paquete, perfil, variante, identidades saneadas e informe privado. INFO resume, DEBUG muestra pasos de negocio y TRACE detalle técnico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia; causa no determinada si no está demostrada. No registrar credenciales, filas completas ni configuración privada.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a XGestion2:

- `src/ModuloProveedores/Vistas/FormCuentaCorrienteIndividual.java:188-254`.
- `src/ModuloProveedores/Entidades/CtaCteProveedor.java:57-94`.
- `test/ModuloFinanzas/Entidades/CuentaCorrienteSaldoServiceTest.java:23-43`.

Las fuentes y tests citados orientan reglas/riesgos; no equivalen a ejecución E2E. Los criterios financieros pendientes necesitan una definición previa independiente de los importes observados.

