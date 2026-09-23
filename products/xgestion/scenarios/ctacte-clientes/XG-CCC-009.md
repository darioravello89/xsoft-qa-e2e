---
{"id":"XG-CCC-009","title":"Anular una venta a crédito revirtiendo sólo su deuda y su cobro","product":"xgestion","module":"cuenta-corriente","tags":["xgestion","regression","cuenta-corriente","ctacte-clientes","devoluciones","monedas","caja"],"status":"planned"}
---

# XG-CCC-009 — Anular una venta a crédito revirtiendo sólo su deuda y su cobro

## Objetivo

Deshacer una venta simple a crédito sin alterar deudas de otras operaciones.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 4.**
Ver [mapa de cuentas corrientes y cuotas](../../docs/cuentas-corrientes.md).
Sin suite Robot, seed automático ni validación real del JAR. Los resultados son criterios esperados; las variantes con regla pendiente no se aprueban por observar la aplicación.

## Precondiciones y datos

- Windows QA exclusivo, offline, paquete privado saneado y escritorio visible. Operaciones locales, sin emisión fiscal, pagos externos, envío de correo ni impresión física.
- Todos los datos QA-CCC/QA-CCP/QA-CUO/QA-CTA son **propuestas sintéticas pendientes de seed/baseline**. `catalogo-comercial-v1` no certifica clientes, proveedores, saldos, cronogramas o movimientos de estas fichas.
- Declarar empresa, sucursal, puesto, operador, cliente/proveedor, moneda, medio y fecha. Sin promociones, impuestos, recargos, descuentos ni cuotas salvo indicación expresa; preservar una cuenta de control. El saldo por persona puede consolidar sucursales de una misma empresa: registrar el alcance del filtro.
- Venta QA-CCC-AN de ARS 1.000, anticipo ARS 300 y deuda ARS 700; cliente sin otros abonos posteriores sobre este circuito.
- Otra deuda de control ARS 200 del mismo cliente; stock inicial/con venta conocidos. Sin cuotas, emisión fiscal ni pagos múltiples.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Solicitar anulación y rechazar la confirmación. | Venta vigente y saldo ARS 900; sin devolución de dinero ni reversión de existencias. |
| Anular con motivo y perfil sin devolución de dinero. | Se compensa deuda neta ARS 700 de la venta; saldo ARS 200. No se infiere devolución del anticipo por compensar deuda. |
| Restaurar baseline y anular con devolución de dinero explícita. | Deuda final ARS 200 y devolución ARS 300 por el medio original, una sola vez; no devuelve ARS 1.000. |
| Consultar originales y compensaciones. | Importes y motivo permiten explicar la anulación; la deuda de control no cambia. |

## Variantes y dependencias

Variante USD: total USD 100/anticipo USD 25 a cotización histórica 1.200; compensación USD 75 sin recotizar al valor actual. Preparar como perfil separado; caja multimoneda requiere oráculo propio. Excluir de esta ficha financiación en cuotas y pagos posteriores: la búsqueda del movimiento asociado no prueba que revierta todo un cronograma.

Antes de automatizar: preparar baseline reproducible, acordar los oráculos pendientes y calibrar selectores/atajos para el SHA256 del JAR. No usar coordenadas fijas ni extender a estas pantallas la autorización de doble clic otorgada para Venta. Las variantes entre empresas/puestos y de fallo/concurrencia requieren su propio laboratorio.

## Evidencia y recuperación

Conservar venta, pagos, movimiento compensatorio, motivo y efectos de stock/caja. Vincular por identidad y nota de anulación sin exigir una FK inexistente en el contramovimiento.

Conservar primero evidencia y conciliar el estado ante una confirmación ambigua. Cancelar o retomar por la interfaz según el caso; no cargar otro pago ni corregir registros comerciales para forzar un aprobado. Restaurar baseline antes de otra variante. Toda escritura preparatoria pertenece al mecanismo de seed autorizado, no a los pasos E2E.

Registrar JAR/SHA256, commit del harness, paquete, perfil, variante, identidades saneadas e informe privado. INFO resume, DEBUG muestra pasos de negocio y TRACE detalle técnico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia; causa no determinada si no está demostrada. No registrar credenciales, filas completas ni configuración privada.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a XGestion2:

- `src/ModuloVentas/Entidades/TicketVenta.java:3285-3360`.
- `test/ModuloVentas/Entidades/TicketVentaAnulacionCuentaCorrienteTest.java:1-170`.

Las fuentes y tests citados orientan reglas/riesgos; no equivalen a ejecución E2E. Los criterios financieros pendientes necesitan una definición previa independiente de los importes observados.

