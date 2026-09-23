---
{"id":"XG-CCP-003","title":"Pagar desde caja y elegir si afecta la cuenta del proveedor","product":"xgestion","module":"cuenta-corriente","tags":["xgestion","regression","cuenta-corriente","ctacte-proveedores","caja","recuperacion"],"status":"planned"}
---

# XG-CCP-003 — Pagar desde caja y elegir si afecta la cuenta del proveedor

## Objetivo

Relacionar una salida de dinero con la deuda del proveedor sin duplicar el pago.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 3.**
Ver [mapa de cuentas corrientes y cuotas](../../docs/cuentas-corrientes.md).
Sin suite Robot, seed automático ni validación real del JAR. Los resultados son criterios esperados; las variantes con regla pendiente no se aprueban por observar la aplicación.

## Precondiciones y datos

- Windows QA exclusivo, offline, paquete privado saneado y escritorio visible. Operaciones locales, sin emisión fiscal, pagos externos, envío de correo ni impresión física.
- Todos los datos QA-CCC/QA-CCP/QA-CUO/QA-CTA son **propuestas sintéticas pendientes de seed/baseline**. `catalogo-comercial-v1` no certifica clientes, proveedores, saldos, cronogramas o movimientos de estas fichas.
- Declarar empresa, sucursal, puesto, operador, cliente/proveedor, moneda, medio y fecha. Sin promociones, impuestos, recargos, descuentos ni cuotas salvo indicación expresa; preservar una cuenta de control. El saldo por persona puede consolidar sucursales de una misma empresa: registrar el alcance del filtro.
- Caja QA con ARS 5.000 disponibles; QA-CCP-A con deuda ARS 2.000; egreso ARS 500, efectivo y concepto de pago a proveedor declarado.
- Dos baselines: opción de enviar a cuenta del proveedor activada/desactivada. Conceptos y dominio del informe de caja deben quedar definidos antes de automatizar.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Preparar un Egreso de caja por ARS 500 y rechazar confirmación. | Caja ARS 5.000 y deuda ARS 2.000; sin pago registrado. |
| Confirmar con envío a cuenta del proveedor activado; rechazar impresión. | Caja operativa ARS 4.500; deuda ARS 1.500 y pago al proveedor ARS 500 una sola vez. |
| Restaurar baseline y confirmar con envío a cuenta desactivado. | Caja operativa ARS 4.500; la deuda del proveedor sigue ARS 2.000. |
| Consultar ambos dominios y sus conceptos. | Se puede explicar el egreso y, cuando corresponde, su pago relacionado; no se cuentan dos salidas físicas por existir registros en dominios diferentes. |

## Variantes y dependencias

Saldo disponible suficiente/insuficiente según configuración; operador permitido/restringido sólo con permiso identificado. La fuente registra concepto movimientoCaja y concepto elegido: **pendiente acordar el oráculo por dominio** del Libro diario, evitando sumar todo indiscriminadamente. No afirmar atomicidad ante fallo entre ambas escrituras; esa recuperación requiere laboratorio controlado.

Antes de automatizar: preparar baseline reproducible, acordar los oráculos pendientes y calibrar selectores/atajos para el SHA256 del JAR. No usar coordenadas fijas ni extender a estas pantallas la autorización de doble clic otorgada para Venta. Las variantes entre empresas/puestos y de fallo/concurrencia requieren su propio laboratorio.

## Evidencia y recuperación

Conciliar caja por medio/contexto, cuenta del proveedor y conceptos. Bloquear automatización hasta definir dominio, ubicación de los controles y datos de saldo; no declarar que dos filas implican dos pagos.

Conservar primero evidencia y conciliar el estado ante una confirmación ambigua. Cancelar o retomar por la interfaz según el caso; no cargar otro pago ni corregir registros comerciales para forzar un aprobado. Restaurar baseline antes de otra variante. Toda escritura preparatoria pertenece al mecanismo de seed autorizado, no a los pasos E2E.

Registrar JAR/SHA256, commit del harness, paquete, perfil, variante, identidades saneadas e informe privado. INFO resume, DEBUG muestra pasos de negocio y TRACE detalle técnico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia; causa no determinada si no está demostrada. No registrar credenciales, filas completas ni configuración privada.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a XGestion2:

- `src/ModuloVentas/Vistas/FormEgresoDeCaja.java:299-370`.
- `src/ModuloProveedores/Entidades/CtaCteProveedor.java:155-198`.

Las fuentes y tests citados orientan reglas/riesgos; no equivalen a ejecución E2E. Los criterios financieros pendientes necesitan una definición previa independiente de los importes observados.

