---
{"id":"XG-CUO-003","title":"Aplicar mora una sola vez y respetar gracia y tolerancia","product":"xgestion","module":"cuenta-corriente","tags":["xgestion","regression","cuenta-corriente","cuotas","recuperacion","monedas"],"status":"planned"}
---

# XG-CUO-003 — Aplicar mora una sola vez y respetar gracia y tolerancia

## Objetivo

Actualizar una deuda vencida sin duplicar intereses por repetir la consulta o el cálculo.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 3.**
Ver [mapa de cuentas corrientes y cuotas](../../docs/cuentas-corrientes.md).
Sin suite Robot, seed automático ni validación real del JAR. Los resultados son criterios esperados; las variantes con regla pendiente no se aprueban por observar la aplicación.

## Precondiciones y datos

- Windows QA exclusivo, offline, paquete privado saneado y escritorio visible. Operaciones locales, sin emisión fiscal, pagos externos, envío de correo ni impresión física.
- Todos los datos QA-CCC/QA-CCP/QA-CUO/QA-CTA son **propuestas sintéticas pendientes de seed/baseline**. `catalogo-comercial-v1` no certifica clientes, proveedores, saldos, cronogramas o movimientos de estas fichas.
- Declarar empresa, sucursal, puesto, operador, cliente/proveedor, moneda, medio y fecha. Sin promociones, impuestos, recargos, descuentos ni cuotas salvo indicación expresa; preservar una cuenta de control. El saldo por persona puede consolidar sucursales de una misma empresa: registrar el alcance del filtro.
- QA-CUO-M: cuota ARS 1.000, vencimiento 10/01/2026; gracia 1 día, tolerancia 1 día; punitorio diario 1%, compensatorio 0%, cargo fijo ARS 5.
- Fecha de evaluación controlada en laboratorio QA: 14/01/2026; dos días de mora después del inicio 12/01/2026. Sin mora anterior. No modificar el reloj de una PC de uso cotidiano.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Evaluar en la fecha límite 12/01/2026 desde su baseline. | Sin mora aplicada todavía; saldo ARS 1.000. |
| Actualizar mora al 14/01/2026. | Interés/cargo acumulado ARS 25; saldo ARS 1.025. |
| Repetir actualización en la misma fecha. | Saldo sigue ARS 1.025; no se agregan otros ARS 25. |
| Evaluar al 15/01/2026 en continuidad controlada. | Mora acumulada ARS 35 y saldo ARS 1.035: sólo ARS 10 adicionales, sin capitalizar la mora anterior. |

## Variantes y dependencias

Cuota pagada no genera nueva mora; moneda USD conserva importe en USD; otro cliente/empresa no cambia. Tasas/gracia/tolerancia y fecha efectiva deben estar declaradas, con oráculo firmado antes de automatizar. La disponibilidad de un mecanismo de fecha controlada para la UI es dependencia pendiente.

Antes de automatizar: preparar baseline reproducible, acordar los oráculos pendientes y calibrar selectores/atajos para el SHA256 del JAR. No usar coordenadas fijas ni extender a estas pantallas la autorización de doble clic otorgada para Venta. Las variantes entre empresas/puestos y de fallo/concurrencia requieren su propio laboratorio.

## Evidencia y recuperación

Registrar fecha de evaluación, fecha de inicio efectiva, base, tasas/cargo, mora previa/nueva y delta. Comparar la repetición con el mismo baseline conocido, no usar la fórmula de la aplicación como calculadora de resultados.

Conservar primero evidencia y conciliar el estado ante una confirmación ambigua. Cancelar o retomar por la interfaz según el caso; no cargar otro pago ni corregir registros comerciales para forzar un aprobado. Restaurar baseline antes de otra variante. Toda escritura preparatoria pertenece al mecanismo de seed autorizado, no a los pasos E2E.

Registrar JAR/SHA256, commit del harness, paquete, perfil, variante, identidades saneadas e informe privado. INFO resume, DEBUG muestra pasos de negocio y TRACE detalle técnico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia; causa no determinada si no está demostrada. No registrar credenciales, filas completas ni configuración privada.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a XGestion2:

- `src/ModuloVentas/Servicios/VentaCuotasService.java:208-273`.
- `src/ModuloFinanzas/Vistas/ActualizacionMoraCuotasDialog.java:24-65`.
- `test/ModuloVentas/Servicios/VentaCuotasPersistenciaTest.java:53-64`.

Las fuentes y tests citados orientan reglas/riesgos; no equivalen a ejecución E2E. Los criterios financieros pendientes necesitan una definición previa independiente de los importes observados.
