---
{"id":"XG-CCP-007","title":"Editar movimientos manuales y proteger los originados por compra","product":"xgestion","module":"cuenta-corriente","tags":["xgestion","regression","cuenta-corriente","ctacte-proveedores","monedas","compras"],"status":"planned"}
---

# XG-CCP-007 — Editar movimientos manuales y proteger los originados por compra

## Objetivo

Corregir un dato permitido sin duplicar saldo ni perder su moneda histórica.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 4.**
Ver [mapa de cuentas corrientes y cuotas](../../docs/cuentas-corrientes.md).
Sin suite Robot, seed automático ni validación real del JAR. Los resultados son criterios esperados; las variantes con regla pendiente no se aprueban por observar la aplicación.

## Precondiciones y datos

- Windows QA exclusivo, offline, paquete privado saneado y escritorio visible. Operaciones locales, sin emisión fiscal, pagos externos, envío de correo ni impresión física.
- Todos los datos QA-CCC/QA-CCP/QA-CUO/QA-CTA son **propuestas sintéticas pendientes de seed/baseline**. `catalogo-comercial-v1` no certifica clientes, proveedores, saldos, cronogramas o movimientos de estas fichas.
- Declarar empresa, sucursal, puesto, operador, cliente/proveedor, moneda, medio y fecha. Sin promociones, impuestos, recargos, descuentos ni cuotas salvo indicación expresa; preservar una cuenta de control. El saldo por persona puede consolidar sucursales de una misma empresa: registrar el alcance del filtro.
- QA-CCP-EDIT: deuda manual ARS 2.000 y pago ARS 750; corregir deuda a ARS 3.000.
- Variante USD: deuda manual USD 10 a cotización histórica 1.200, actual 1.500; corregir a USD 12. Documento de compra asociado separado para intentar edición.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Editar la deuda manual ARS y guardar ARS 3.000. | Saldo ARS 2.250; el importe anterior se reemplaza, no se vuelve a sumar. |
| En baseline USD, cambiar importe a USD 12 y guardar. | Conserva moneda USD y cotización 1.200; equivalente ARS 14.400. |
| Intentar editar en cuenta corriente el movimiento generado por la compra. | Se informa que los registros ingresados por remitos/facturas no se modifican por este editor; documento y saldo conservados. |
| Reabrir el movimiento manual y salir sin guardar cambios. | Quedan la última versión guardada y el medio/fecha correspondientes. |

## Variantes y dependencias

Edición de fecha, medio de pago y nota; historial ordenado con dos movimientos del mismo instante. Edición de pagos con efectos en otros circuitos requiere conciliación acordada; el editor no demuestra ajuste del egreso de caja relacionado.

Antes de automatizar: preparar baseline reproducible, acordar los oráculos pendientes y calibrar selectores/atajos para el SHA256 del JAR. No usar coordenadas fijas ni extender a estas pantallas la autorización de doble clic otorgada para Venta. Las variantes entre empresas/puestos y de fallo/concurrencia requieren su propio laboratorio.

## Evidencia y recuperación

Verificar fecha/medio/importe, clave del proveedor y foto histórica. Calibrar acción accesible del editor; no aplicar automáticamente permiso de doble clic de otra pantalla.

Conservar primero evidencia y conciliar el estado ante una confirmación ambigua. Cancelar o retomar por la interfaz según el caso; no cargar otro pago ni corregir registros comerciales para forzar un aprobado. Restaurar baseline antes de otra variante. Toda escritura preparatoria pertenece al mecanismo de seed autorizado, no a los pasos E2E.

Registrar JAR/SHA256, commit del harness, paquete, perfil, variante, identidades saneadas e informe privado. INFO resume, DEBUG muestra pasos de negocio y TRACE detalle técnico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia; causa no determinada si no está demostrada. No registrar credenciales, filas completas ni configuración privada.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a XGestion2:

- `src/ModuloProveedores/Vistas/FormCuentaCorriente.java:731-758`.
- `src/ModuloProveedores/Vistas/FormCuentaCorrienteIndividual.java:288-316`.
- `src/ModuloProveedores/Entidades/CtaCteProveedor.java:253-359`.
- `test/ModuloProveedores/Entidades/CtaCteProveedorEdicionFotoMonedaPolicyTest.java:14-51`.

Las fuentes y tests citados orientan reglas/riesgos; no equivalen a ejecución E2E. Los criterios financieros pendientes necesitan una definición previa independiente de los importes observados.

