---
{"id":"XG-CCP-008","title":"Consultar deuda, saldo a favor y resumen del proveedor","product":"xgestion","module":"cuenta-corriente","tags":["xgestion","regression","cuenta-corriente","ctacte-proveedores"],"status":"planned"}
---

# XG-CCP-008 — Consultar deuda, saldo a favor y resumen del proveedor

## Objetivo

Entender si queda dinero por pagar al proveedor o a favor de la empresa.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P1; etapa 4.**
Ver [mapa de cuentas corrientes y cuotas](../../docs/cuentas-corrientes.md).
Sin suite Robot, seed automático ni validación real del JAR. Los resultados son criterios esperados; las variantes con regla pendiente no se aprueban por observar la aplicación.

## Precondiciones y datos

- Windows QA exclusivo, offline, paquete privado saneado y escritorio visible. Operaciones locales, sin emisión fiscal, pagos externos, envío de correo ni impresión física.
- Todos los datos QA-CCC/QA-CCP/QA-CUO/QA-CTA son **propuestas sintéticas pendientes de seed/baseline**. `catalogo-comercial-v1` no certifica clientes, proveedores, saldos, cronogramas o movimientos de estas fichas.
- Declarar empresa, sucursal, puesto, operador, cliente/proveedor, moneda, medio y fecha. Sin promociones, impuestos, recargos, descuentos ni cuotas salvo indicación expresa; preservar una cuenta de control. El saldo por persona puede consolidar sucursales de una misma empresa: registrar el alcance del filtro.
- Tres baselines ARS: deuda ARS 2.000/pago ARS 500; deuda ARS 2.000/pago ARS 2.000; deuda ARS 2.000/pago ARS 2.200.
- Rango de fechas conocido con una deuda anterior y pago dentro; otro proveedor y contexto de control.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Consultar el primer baseline. | Saldo ARS 1.500 con significado Pendiente de pago al proveedor. |
| Consultar los baselines de pago exacto y mayor. | Saldo ARS 0 sin deuda; saldo ARS -200 equivalente a ARS 200 a favor de la empresa, no nueva deuda al proveedor. |
| Filtrar por fechas y tipo de movimiento; quitar el filtro. | Se distinguen importe filtrado y saldo actual/total, sin ocultar deudas anteriores como si estuvieran pagadas; al quitar filtro vuelve el historial esperado. |
| Abrir Ver resumen y volver a la cuenta. | Informe del mismo proveedor y alcance declarado; consultar no registra pagos. Variante bloqueada si falta plantilla o regla del informe. |

## Variantes y dependencias

Resumen/exportación local, sin enviar correo ni imprimir; validar el artefacto real cuando se habilite esa variante. Multimoneda tiene contrato pendiente en [XG-CCP-006](XG-CCP-006.md); esta ficha fija el oráculo ARS. Aislamiento por empresa y proveedor, sin confundir saldo consolidado con filtro por sucursal.

Antes de automatizar: preparar baseline reproducible, acordar los oráculos pendientes y calibrar selectores/atajos para el SHA256 del JAR. No usar coordenadas fijas ni extender a estas pantallas la autorización de doble clic otorgada para Venta. Las variantes entre empresas/puestos y de fallo/concurrencia requieren su propio laboratorio.

## Evidencia y recuperación

Capturas del significado del saldo, filtros y detalle; para informes guardar artefacto privado y comparar filas/importes con el baseline.

Conservar primero evidencia y conciliar el estado ante una confirmación ambigua. Cancelar o retomar por la interfaz según el caso; no cargar otro pago ni corregir registros comerciales para forzar un aprobado. Restaurar baseline antes de otra variante. Toda escritura preparatoria pertenece al mecanismo de seed autorizado, no a los pasos E2E.

Registrar JAR/SHA256, commit del harness, paquete, perfil, variante, identidades saneadas e informe privado. INFO resume, DEBUG muestra pasos de negocio y TRACE detalle técnico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia; causa no determinada si no está demostrada. No registrar credenciales, filas completas ni configuración privada.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a XGestion2:

- `src/ModuloProveedores/Vistas/FormCuentaCorriente.java:175-202`.
- `src/ModuloProveedores/Vistas/FormCuentaCorriente.java:371-402`.
- `src/ModuloProveedores/Vistas/FormCuentaCorriente.java:761-805`.
- `test/ModuloProveedores/Vistas/FormCuentaCorrienteProveedorBalanceStatusTest.java:11-30`.

Las fuentes y tests citados orientan reglas/riesgos; no equivalen a ejecución E2E. Los criterios financieros pendientes necesitan una definición previa independiente de los importes observados.
