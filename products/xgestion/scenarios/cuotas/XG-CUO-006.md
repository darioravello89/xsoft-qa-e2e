---
{"id":"XG-CUO-006","title":"Reabrir el historial de cuotas y conservar el plan original","product":"xgestion","module":"cuenta-corriente","tags":["xgestion","regression","cuenta-corriente","cuotas","monedas"],"status":"planned"}
---

# XG-CUO-006 — Reabrir el historial de cuotas y conservar el plan original

## Objetivo

Consultar cuotas pagadas y pendientes sin que una cotización o configuración nueva reescriba su historia.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P1; etapa 3.**
Ver [mapa de cuentas corrientes y cuotas](../../docs/cuentas-corrientes.md).
Sin suite Robot, seed automático ni validación real del JAR. Los resultados son criterios esperados; las variantes con regla pendiente no se aprueban por observar la aplicación.

## Precondiciones y datos

- Windows QA exclusivo, offline, paquete privado saneado y escritorio visible. Operaciones locales, sin emisión fiscal, pagos externos, envío de correo ni impresión física.
- Todos los datos QA-CCC/QA-CCP/QA-CUO/QA-CTA son **propuestas sintéticas pendientes de seed/baseline**. `catalogo-comercial-v1` no certifica clientes, proveedores, saldos, cronogramas o movimientos de estas fichas.
- Declarar empresa, sucursal, puesto, operador, cliente/proveedor, moneda, medio y fecha. Sin promociones, impuestos, recargos, descuentos ni cuotas salvo indicación expresa; preservar una cuenta de control. El saldo por persona puede consolidar sucursales de una misma empresa: registrar el alcance del filtro.
- QA-CUO-H: plan de tres cuotas conocidas, primera pagada y dos pendientes; monedas/importes, vencimientos y estado preparados en baseline.
- Variante USD con cotización de origen 1.200 y pago en ARS a 1.500; cotización actual 1.800. Variante antigua sin moneda declarada tratada como ARS.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Abrir Resumen Cuotas del cliente y su venta. | Aparecen las tres cuotas con número, vencimiento, importe, estado y saldo esperados. |
| Consultar la cuota pagada y las pendientes. | La pagada conserva saldo cero y sus datos de pago; las otras mantienen su deuda original. |
| Cerrar y volver a consultar con la configuración/cotización actual del perfil. | No cambia el cronograma ni se recotiza el pago histórico; consultar no vuelve a cobrar ni genera otro plan. |
| Filtrar el estado y luego quitar el filtro. | Se recuperan las cuotas esperadas del cliente y contexto, sin mezclar otra empresa. |

## Variantes y dependencias

Vencidas, pagadas, legado ARS, plan sin anticipo/con anticipo y centavos finales. Editar un plan ya cerrado, refinanciar o anular una venta con cuotas no se presume soportado: necesita circuito/oráculo propio antes de automatizar. No aplicar la anulación de venta simple CCC-009 a todo un cronograma.

Antes de automatizar: preparar baseline reproducible, acordar los oráculos pendientes y calibrar selectores/atajos para el SHA256 del JAR. No usar coordenadas fijas ni extender a estas pantallas la autorización de doble clic otorgada para Venta. Las variantes entre empresas/puestos y de fallo/concurrencia requieren su propio laboratorio.

## Evidencia y recuperación

Comparar calendario, moneda, cotización de origen, foto del pago y estados del baseline. Si el informe no expone un dato, complementar lectura privada autorizada por identidad; no inventar un control en pantalla.

Conservar primero evidencia y conciliar el estado ante una confirmación ambigua. Cancelar o retomar por la interfaz según el caso; no cargar otro pago ni corregir registros comerciales para forzar un aprobado. Restaurar baseline antes de otra variante. Toda escritura preparatoria pertenece al mecanismo de seed autorizado, no a los pasos E2E.

Registrar JAR/SHA256, commit del harness, paquete, perfil, variante, identidades saneadas e informe privado. INFO resume, DEBUG muestra pasos de negocio y TRACE detalle técnico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia; causa no determinada si no está demostrada. No registrar credenciales, filas completas ni configuración privada.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a XGestion2:

- `src/ModuloFinanzas/Vistas/FormCuentaCorrienteCliente.java:412-421`.
- `src/ModuloVentas/Servicios/VentaCuotasService.java:275-337`.
- `src/ModuloVentas/Servicios/VentaCuotasService.java:365-410`.
- `test/ModuloVentas/Servicios/VentaCuotasPersistenciaTest.java:14-27`.
- `test/ModuloVentas/Servicios/VentaCuotasPersistenciaTest.java:65-81`.

Las fuentes y tests citados orientan reglas/riesgos; no equivalen a ejecución E2E. Los criterios financieros pendientes necesitan una definición previa independiente de los importes observados.

