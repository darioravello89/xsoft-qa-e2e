---
{"id":"XG-COB-001","title":"Cobrar una venta repartiendo el total entre dos medios","product":"xgestion","module":"cobros-combinados","tags":["xgestion","regression","cobros-combinados","cobros","caja","stock"],"status":"planned"}
---

# XG-COB-001 — Cobrar una venta repartiendo el total entre dos medios

## Objetivo

Completar el total correcto usando efectivo y un segundo medio manual, sin duplicar caja ni venta.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 3.**
Ver [mapa de cobros y documentos](../../docs/cobros-documentos.md).
No tiene Robot, seed propio ni ejecución real del JAR. Los resultados son criterios de aceptación; los pasos con contrato pendiente no afirman que esa funcionalidad exista ni se habilitan por observar la pantalla.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. Identificar JAR/SHA256, empresa, sucursal, puesto, operador y documentos de control.
- Datos QA-COB/QA-PRE/QA-DEV e importes de esta ficha son **propuestas sintéticas pendientes de seed y calibración**. `catalogo-comercial-v1` no acredita estos documentos, pagos o estados.
- Perfil local no fiscal; sin impresión, integraciones de pago, correo ni red. Sin ofertas, descuentos, recargos, impuestos adicionales ni financiación salvo variante explícita. Medios manuales QA separados de pasarelas reales.
- Venta QA-COB-A: 2 unidades a ARS 1.000, total ARS 2.000; efectivo ARS 500 y tarjeta manual QA ARS 1.500, sin integración ni ajustes del medio.
- Moneda operativa ARS; cobros multimoneda deshabilitados. Stock inicial 10; caja y otro documento de control conocidos.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Abrir Multiple e ingresar efectivo ARS 500. | Pagado ARS 500, falta ARS 1.500; la venta todavía no está cerrada. |
| Intentar Cobrar sin completar el total. | Se informa que el dinero debe cubrir el total; no cierra ni descuenta stock definitivamente. |
| Ingresar tarjeta manual ARS 1.500 y elegir Cobrar. | Pagado ARS 2.000, faltante/vuelto ARS 0; termina un solo cierre válido, incluido el cierre automático del diálogo principal cuando corresponda. |
| Consultar comprobante, pagos y caja por medio. | Una venta ARS 2.000, cobros efectivo 500/tarjeta 1.500 y stock 8; ninguna alteración en el documento de control. |

## Variantes y dependencias

Ingresar el mismo reparto en orden inverso desde baseline. La carga de un pago puede persistir antes del cierre: comprobar ausencia de efectos definitivos y pagos activos ajenos, no exigir cero filas en toda tabla. No confundir varios medios habilitados para una oferta con un cobro dividido.

Calibrar controles accesibles para el JAR antes de automatizar; los nombres/atajos leídos en fuente no sustituyen calibración. No usar coordenadas fijas ni extender permisos de doble clic de otras pantallas. Preparar oráculos independientes por identidad, importe original/operativo, medio, moneda y contexto; toda regla no confirmada se resuelve antes de habilitar su variante.

## Evidencia y límites

Contrastar documento, pagos, saldo, caja e inventario según el alcance de los pasos, con importes iniciales/finales y deltas esperados. Separar estados de preparación, persistencia de borrador/pagos y cierre definitivo. No exigir ausencia de todo registro cuando puede existir historia inactiva. Libro diario y caja pueden tener representaciones distintas: no sumar filas indiscriminadamente como dinero duplicado.

Registrar en informe privado JAR/SHA256, commit del harness, paquete, perfil, variante e identidades saneadas. INFO resume, DEBUG describe pasos y TRACE aporta diagnóstico acotado; todo fallo conserva paso, esperado, observado, categoría y evidencia. Causa no determinada si no hay prueba causal; nunca credenciales, configuración privada completa ni filas enteras.

## Recuperación

Conservar evidencia y consultar el estado antes de repetir una confirmación incierta. Cancelar por interfaz cuando el paso lo permita; no improvisar pagos compensatorios ni SQL comercial. Si no existe procedimiento aprobado para el estado parcial, mantener el bloqueo. Restaurar baseline antes de otra variante; anular una operación no reemplaza restaurar el laboratorio.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Rutas y líneas relativas a XGestion2:

- `src/ModuloVentas/Vistas/Dialogs/DialogCobroMultiple.java:309-415`.
- `src/ModuloVentas/Vistas/Dialogs/DialogCobroMultiple.java:438-447`.
- `src/ModuloVentas/Vistas/Dialogs/formTicketCierre.java:572-625`.
- `test/ModuloVentas/Vistas/Dialogs/FormTicketCierreCobroMultiplePolicyTest.java:15-41`.

Las referencias describen reglas o riesgos; los tests fuente no acreditan el flujo E2E del JAR. Las modalidades pendientes de contrato están delimitadas arriba, sin inventar su soporte.

