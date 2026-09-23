---
{"id":"XG-CCC-010","title":"Consultar y exportar una cuenta de cliente sin mezclar monedas","product":"xgestion","module":"cuenta-corriente","tags":["xgestion","regression","cuenta-corriente","ctacte-clientes","monedas"],"status":"planned"}
---

# XG-CCC-010 — Consultar y exportar una cuenta de cliente sin mezclar monedas

## Objetivo

Entregar un resumen comprensible del período y de la deuda total.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P1; etapa 3.**
Ver [mapa de cuentas corrientes y cuotas](../../docs/cuentas-corrientes.md).
Sin suite Robot, seed automático ni validación real del JAR. Los resultados son criterios esperados; las variantes con regla pendiente no se aprueban por observar la aplicación.

## Precondiciones y datos

- Windows QA exclusivo, offline, paquete privado saneado y escritorio visible. Operaciones locales, sin emisión fiscal, pagos externos, envío de correo ni impresión física.
- Todos los datos QA-CCC/QA-CCP/QA-CUO/QA-CTA son **propuestas sintéticas pendientes de seed/baseline**. `catalogo-comercial-v1` no certifica clientes, proveedores, saldos, cronogramas o movimientos de estas fichas.
- Declarar empresa, sucursal, puesto, operador, cliente/proveedor, moneda, medio y fecha. Sin promociones, impuestos, recargos, descuentos ni cuotas salvo indicación expresa; preservar una cuenta de control. El saldo por persona puede consolidar sucursales de una misma empresa: registrar el alcance del filtro.
- QA-CCC-RES: deuda ARS 2.000 anterior al período; pago ARS 500 dentro; deuda USD 25 dentro. Otro cliente con movimientos propios.
- Fechas fijas del paquete y exportación local a carpeta privada permitida. No enviar email ni imprimir.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Abrir la cuenta del cliente y consultar todo el historial. | Saldo ARS 1.500 y USD 25, con deudas y pagos identificables. |
| Filtrar el período que sólo incluye el pago y la deuda USD. | Aparecen esos movimientos; el efecto del período es ARS -500 y USD 25. El saldo acumulado incluye la deuda previa y continúa ARS 1.500/USD 25. |
| Exportar la consulta localmente y abrir el archivo generado. | Coinciden cliente, alcance del filtro, importes y prefijos de moneda; no se exponen identificadores internos como columnas para el cliente. |
| Quitar filtros y cambiar al cliente de control. | Se recupera el historial completo; no se mezclan movimientos de clientes ni se generan pagos por consultar. |

## Variantes y dependencias

Resumen normal/extendido requiere sus plantillas Jasper en el paquete; comparar el alcance declarado de cada informe. Sin filas, moneda única, mismo instante y notas vacías. PDF e impresión tienen validación propia; exportación no acredita entrega por correo.

Antes de automatizar: preparar baseline reproducible, acordar los oráculos pendientes y calibrar selectores/atajos para el SHA256 del JAR. No usar coordenadas fijas ni extender a estas pantallas la autorización de doble clic otorgada para Venta. Las variantes entre empresas/puestos y de fallo/concurrencia requieren su propio laboratorio.

## Evidencia y recuperación

Leer el archivo real exportado y compararlo con los datos esperados; captura de la grilla sola no valida Excel. Si falta plantilla o contrato del resumen, bloquear esa variante.

Conservar primero evidencia y conciliar el estado ante una confirmación ambigua. Cancelar o retomar por la interfaz según el caso; no cargar otro pago ni corregir registros comerciales para forzar un aprobado. Restaurar baseline antes de otra variante. Toda escritura preparatoria pertenece al mecanismo de seed autorizado, no a los pasos E2E.

Registrar JAR/SHA256, commit del harness, paquete, perfil, variante, identidades saneadas e informe privado. INFO resume, DEBUG muestra pasos de negocio y TRACE detalle técnico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia; causa no determinada si no está demostrada. No registrar credenciales, filas completas ni configuración privada.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas relativas a XGestion2:

- `src/ModuloFinanzas/Vistas/FormCuentaCorrienteCliente.java:194-225`.
- `src/ModuloFinanzas/Vistas/FormCuentaCorrienteCliente.java:1302-1338`.
- `test/ModuloFinanzas/Vistas/FormCuentaCorrienteClienteExcelPolicyTest.java:14-68`.
- `test/ModuloFinanzas/Vistas/FormCuentaCorrienteClienteMonedaPolicyTest.java:18-72`.

Las fuentes y tests citados orientan reglas/riesgos; no equivalen a ejecución E2E. Los criterios financieros pendientes necesitan una definición previa independiente de los importes observados.

