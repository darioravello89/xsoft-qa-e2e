---
{"id":"XG-CCP-005","title":"Conciliar la anulación de compra cuando hubo un anticipo","product":"xgestion","module":"cuenta-corriente","tags":["xgestion","regression","cuenta-corriente","ctacte-proveedores","compras","devoluciones","caja"],"status":"planned"}
---

# XG-CCP-005 — Conciliar la anulación de compra cuando hubo un anticipo

## Objetivo

Anular una compra y distinguir la compensación de su deuda de una devolución real del proveedor.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 4.**
Ver [mapa de cuentas corrientes y cuotas](../../docs/cuentas-corrientes.md).
Sin suite Robot, seed automático ni validación real del JAR. Los resultados son criterios esperados; las variantes con regla pendiente no se aprueban por observar la aplicación.

## Precondiciones y datos

- Windows QA exclusivo, offline, paquete privado saneado y escritorio visible. Operaciones locales, sin emisión fiscal, pagos externos, envío de correo ni impresión física.
- Todos los datos QA-CCC/QA-CCP/QA-CUO/QA-CTA son **propuestas sintéticas pendientes de seed/baseline**. `catalogo-comercial-v1` no certifica clientes, proveedores, saldos, cronogramas o movimientos de estas fichas.
- Declarar empresa, sucursal, puesto, operador, cliente/proveedor, moneda, medio y fecha. Sin promociones, impuestos, recargos, descuentos ni cuotas salvo indicación expresa; preservar una cuenta de control. El saldo por persona puede consolidar sucursales de una misma empresa: registrar el alcance del filtro.
- QA-CCP-AN: compra ARS 2.000 con pagado ARS 500, deuda ARS 1.500; otra deuda independiente ARS 700.
- Usar el documento, permisos y stock de [XG-REM-024](../remitos/XG-REM-024.md). Esta ficha añade lectura financiera; no duplica su procedimiento de anulación.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Consultar ambas deudas y rechazar la primera confirmación de anulación del remito. | Saldo ARS 2.200 y compra vigente; sin compensación. |
| Ejecutar la anulación confirmada del recorrido REM-024. | La deuda neta ARS 1.500 queda compensada; saldo ARS 700 por la otra operación. |
| Consultar compra original y movimiento compensatorio. | Se identifican total/pagado y motivo; no se compensan ARS 2.000 adicionales sobre el saldo neto. |
| Revisar el anticipo y la caja sin cargar una devolución adicional. | La compensación de deuda no se presenta como prueba de reintegro de ARS 500. El destino de ese anticipo debe tener un circuito comercial definido antes de cerrar la conciliación completa. |

## Variantes y dependencias

Sin anticipo, pagado total y moneda extranjera con foto histórica. El saldo esperado de cuenta proviene de invertir los importes de la compra; la devolución de dinero o conservación del anticipo como crédito es un **oráculo pendiente de definición**, no se elige mirando el saldo obtenido. No extrapolar a pagos posteriores independientes.

Antes de automatizar: preparar baseline reproducible, acordar los oráculos pendientes y calibrar selectores/atajos para el SHA256 del JAR. No usar coordenadas fijas ni extender a estas pantallas la autorización de doble clic otorgada para Venta. Las variantes entre empresas/puestos y de fallo/concurrencia requieren su propio laboratorio.

## Evidencia y recuperación

Conservar documento, compensación y pago inicial. Reutilizar evidencia de stock/precios de REM-024: anular no restaura automáticamente los precios anteriores.

Conservar primero evidencia y conciliar el estado ante una confirmación ambigua. Cancelar o retomar por la interfaz según el caso; no cargar otro pago ni corregir registros comerciales para forzar un aprobado. Restaurar baseline antes de otra variante. Toda escritura preparatoria pertenece al mecanismo de seed autorizado, no a los pasos E2E.

Registrar JAR/SHA256, commit del harness, paquete, perfil, variante, identidades saneadas e informe privado. INFO resume, DEBUG muestra pasos de negocio y TRACE detalle técnico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia; causa no determinada si no está demostrada. No registrar credenciales, filas completas ni configuración privada.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a XGestion2:

- `src/ModuloProductos/Entidades/Compra.java:652-700`.
- `src/ModuloStocks/Vistas/FormListadoOrdenesCompras.java:538-561`.
- `test/ModuloFinanzas/Entidades/CuentaCorrienteSaldoServiceTest.java:23-43`.

Las fuentes y tests citados orientan reglas/riesgos; no equivalen a ejecución E2E. Los criterios financieros pendientes necesitan una definición previa independiente de los importes observados.

