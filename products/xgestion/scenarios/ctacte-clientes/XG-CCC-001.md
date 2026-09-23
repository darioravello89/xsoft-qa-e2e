---
{"id":"XG-CCC-001","title":"Vender a crédito con y sin anticipo","product":"xgestion","module":"cuenta-corriente","tags":["xgestion","regression","cuenta-corriente","ctacte-clientes","ventas","cobros","caja"],"status":"planned"}
---

# XG-CCC-001 — Vender a crédito con y sin anticipo

## Objetivo

Cerrar una venta conservando exactamente la parte que el cliente queda debiendo.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 3.**
Ver [mapa de cuentas corrientes y cuotas](../../docs/cuentas-corrientes.md).
Sin suite Robot, seed automático ni validación real del JAR. Los resultados son criterios esperados; las variantes con regla pendiente no se aprueban por observar la aplicación.

## Precondiciones y datos

- Windows QA exclusivo, offline, paquete privado saneado y escritorio visible. Operaciones locales, sin emisión fiscal, pagos externos, envío de correo ni impresión física.
- Todos los datos QA-CCC/QA-CCP/QA-CUO/QA-CTA son **propuestas sintéticas pendientes de seed/baseline**. `catalogo-comercial-v1` no certifica clientes, proveedores, saldos, cronogramas o movimientos de estas fichas.
- Declarar empresa, sucursal, puesto, operador, cliente/proveedor, moneda, medio y fecha. Sin promociones, impuestos, recargos, descuentos ni cuotas salvo indicación expresa; preservar una cuenta de control. El saldo por persona puede consolidar sucursales de una misma empresa: registrar el alcance del filtro.
- Cliente QA-CCC-A sin deuda; producto QA-CTA-1000 a ARS 1.000; venta de 2 unidades, total ARS 2.000. Sin financiación en cuotas.
- Dos baselines independientes: sin anticipo y anticipo efectivo ARS 500. Medio Cuenta corriente y cliente habilitados; caja inicial conocida.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Identificar al cliente y cargar las dos unidades. | Venta ARS 2.000 con el cliente correcto; todavía no hay nueva deuda ni cobro definitivo. |
| Cerrar a cuenta corriente sin anticipo. | Comprobante cerrado una vez; deuda adicional ARS 2.000 y sin entrada efectiva de dinero. |
| Restaurar el segundo baseline y cerrar con anticipo ARS 500. | Documento por ARS 2.000, pago inicial ARS 500 y saldo deudor ARS 1.500; el anticipo no se resta dos veces. |
| Consultar nuevamente el documento, la cuenta y el movimiento de cobro. | Se conserva la identidad de la venta y sus importes; consultar no genera otro cargo o cobro. La caja refleja únicamente los ARS 500 recibidos en el perfil con anticipo. |

## Variantes y dependencias

Variar cliente con saldo previo y producto con stock controlado. Restobar conserva su propio recorrido [XG-RES-029](../restobar/XG-RES-029.md); las cuotas se prueban en [XG-CUO-001](../cuotas/XG-CUO-001.md). No equiparar Cuenta corriente con efectivo ni volver a registrar el anticipo como Nuevo pago.

Antes de automatizar: preparar baseline reproducible, acordar los oráculos pendientes y calibrar selectores/atajos para el SHA256 del JAR. No usar coordenadas fijas ni extender a estas pantallas la autorización de doble clic otorgada para Venta. Las variantes entre empresas/puestos y de fallo/concurrencia requieren su propio laboratorio.

## Evidencia y recuperación

Conciliar total, pagado, deuda neta, documento e ingreso financiero por identidad; verificar otro cliente sin cambios.

Conservar primero evidencia y conciliar el estado ante una confirmación ambigua. Cancelar o retomar por la interfaz según el caso; no cargar otro pago ni corregir registros comerciales para forzar un aprobado. Restaurar baseline antes de otra variante. Toda escritura preparatoria pertenece al mecanismo de seed autorizado, no a los pasos E2E.

Registrar JAR/SHA256, commit del harness, paquete, perfil, variante, identidades saneadas e informe privado. INFO resume, DEBUG muestra pasos de negocio y TRACE detalle técnico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia; causa no determinada si no está demostrada. No registrar credenciales, filas completas ni configuración privada.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a XGestion2:

- `src/ModuloVentas/Entidades/TicketVenta.java:2314-2343`.
- `src/ModuloVentas/Entidades/TicketVenta.java:2563-2587`.
- `test/ModuloVentas/Vistas/FormVentaCierreCuentaCorrientePolicyTest.java:13-23`.

Las fuentes y tests citados orientan reglas/riesgos; no equivalen a ejecución E2E. Los criterios financieros pendientes necesitan una definición previa independiente de los importes observados.
