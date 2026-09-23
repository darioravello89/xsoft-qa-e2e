---
{"id":"XG-CCP-006","title":"Distinguir saldos del proveedor por moneda","product":"xgestion","module":"cuenta-corriente","tags":["xgestion","regression","cuenta-corriente","ctacte-proveedores","monedas"],"status":"planned"}
---

# XG-CCP-006 — Distinguir saldos del proveedor por moneda

## Objetivo

Consultar deuda y saldo a favor del proveedor sin mezclar pesos y dólares.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 3.**
Ver [mapa de cuentas corrientes y cuotas](../../docs/cuentas-corrientes.md).
Sin suite Robot, seed automático ni validación real del JAR. Los resultados son criterios esperados; las variantes con regla pendiente no se aprueban por observar la aplicación.

## Precondiciones y datos

- Windows QA exclusivo, offline, paquete privado saneado y escritorio visible. Operaciones locales, sin emisión fiscal, pagos externos, envío de correo ni impresión física.
- Todos los datos QA-CCC/QA-CCP/QA-CUO/QA-CTA son **propuestas sintéticas pendientes de seed/baseline**. `catalogo-comercial-v1` no certifica clientes, proveedores, saldos, cronogramas o movimientos de estas fichas.
- Declarar empresa, sucursal, puesto, operador, cliente/proveedor, moneda, medio y fecha. Sin promociones, impuestos, recargos, descuentos ni cuotas salvo indicación expresa; preservar una cuenta de control. El saldo por persona puede consolidar sucursales de una misma empresa: registrar el alcance del filtro.
- QA-CCP-M con deuda manual ARS 15.000 y deuda manual USD 25; pago USD 10, cotización del perfil 1.200.
- Cotización actual distinta de la de movimientos antiguos; proveedor de control. Desactivar Convertir productos USD a pesos para habilitar USD en movimientos nuevos del proveedor. Datos y contrato de resumen por moneda pendientes de preparar.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Abrir detalle de cuenta y reconocer la moneda de cada movimiento. | Deuda ARS 15.000 y USD 25 identificables; los importes originales no se suman nominalmente como 15.025. |
| Registrar pago manual USD 10 con el perfil declarado. | Deuda USD 15 y ARS 15.000 sin cambios; foto del pago USD 10 a 1.200, equivalente ARS 12.000. |
| Reabrir el detalle y revisar los movimientos antiguos. | Conservan moneda y cotización originales; no se recotizan por abrir la consulta. |
| Contrastar el resumen del proveedor con el detalle. | Debe distinguir los saldos por moneda o explicitar la conversión y cotización; no aprobar un total sin significado. **Presentación exacta del resumen pendiente de contrato previo.** |

## Variantes y dependencias

Moneda única, saldo a favor, registros antiguos sin foto (ARS) y cotización inválida. La fuente del editor conserva foto y el renderer distingue moneda; eso no prueba que todas las tarjetas o informes totalicen por moneda. El pago cruzado ARS/USD fuera de cuotas requiere otra regla y no se infiere aquí.

Antes de automatizar: preparar baseline reproducible, acordar los oráculos pendientes y calibrar selectores/atajos para el SHA256 del JAR. No usar coordenadas fijas ni extender a estas pantallas la autorización de doble clic otorgada para Venta. Las variantes entre empresas/puestos y de fallo/concurrencia requieren su propio laboratorio.

## Evidencia y recuperación

Comparar montos originales/equivalentes, signos y resumen. No aprobar un resumen por copiar su fórmula de agregación; la regla del negocio debe fijarse antes.

Conservar primero evidencia y conciliar el estado ante una confirmación ambigua. Cancelar o retomar por la interfaz según el caso; no cargar otro pago ni corregir registros comerciales para forzar un aprobado. Restaurar baseline antes de otra variante. Toda escritura preparatoria pertenece al mecanismo de seed autorizado, no a los pasos E2E.

Registrar JAR/SHA256, commit del harness, paquete, perfil, variante, identidades saneadas e informe privado. INFO resume, DEBUG muestra pasos de negocio y TRACE detalle técnico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia; causa no determinada si no está demostrada. No registrar credenciales, filas completas ni configuración privada.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a XGestion2:

- `src/ModuloProveedores/Vistas/FormCuentaCorrienteIndividual.java:157-162`.
- `src/ModuloProveedores/Vistas/FormCuentaCorrienteIndividual.java:206-248`.
- `src/ModuloProveedores/Vistas/FormCuentaCorriente.java:1195-1258`.
- `test/ModuloProveedores/Entidades/CtaCteProveedorEdicionFotoMonedaPolicyTest.java:14-35`.

Las fuentes y tests citados orientan reglas/riesgos; no equivalen a ejecución E2E. Los criterios financieros pendientes necesitan una definición previa independiente de los importes observados.
