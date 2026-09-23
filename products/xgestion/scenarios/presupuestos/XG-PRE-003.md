---
{"id":"XG-PRE-003","title":"Agregar productos a un presupuesto reabierto y conservar una sola propuesta","product":"xgestion","module":"presupuestos","tags":["xgestion","regression","presupuestos","comprobantes","precios","recuperacion"],"status":"planned"}
---

# XG-PRE-003 — Agregar productos a un presupuesto reabierto y conservar una sola propuesta

## Objetivo

Ampliar una cotización editable sin crear una copia ni duplicar cantidades.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P1; etapa 3.**
Ver [mapa de cobros y documentos](../../docs/cobros-documentos.md).
No tiene Robot, seed propio ni ejecución real del JAR. Los resultados son criterios de aceptación; los pasos con contrato pendiente no afirman que esa funcionalidad exista ni se habilitan por observar la pantalla.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. Identificar JAR/SHA256, empresa, sucursal, puesto, operador y documentos de control.
- Datos QA-COB/QA-PRE/QA-DEV e importes de esta ficha son **propuestas sintéticas pendientes de seed y calibración**. `catalogo-comercial-v1` no acredita estos documentos, pagos o estados.
- Perfil local no fiscal; sin impresión, integraciones de pago, correo ni red. Sin ofertas, descuentos, recargos, impuestos adicionales ni financiación salvo variante explícita. Medios manuales QA separados de pasarelas reales.
- Baseline de [LPR-022](../listas-precios/XG-LPR-022.md), variante ARS: A × 2 a ARS 750, total ARS 1.500. Agregar B × 1 a ARS 500; lista y precios sin cambios.
- Documento editable, stock de presupuesto OFF. La reproducción de moneda/lista de LPR-022 se usa como prerrequisito, no se cuenta otra vez como objetivo.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Reabrir la propuesta verificada y agregar B. | Detalle A × 2 y B × 1; total ARS 2.000. |
| Guardar los cambios sin imprimir y consultar la misma propuesta. | Una identidad de documento, cantidades 2/1 y total ARS 2.000. |
| Reabrir y guardar sin nuevas modificaciones. | Conserva total y cantidades, sin volver a agregar B ni registrar cobro. |
| Consultar cliente, stock y caja de control. | Sin cobro ni deuda por una venta definitiva; stock sin cambios en perfil OFF. |

## Variantes y dependencias

Modificar/eliminar un renglón exige editor accesible calibrado. Si cambia el precio de catálogo entre guardar y editar, acordar previamente qué precio corresponde a artículos existentes/nuevos; LPR-022 ya señala ese contrato pendiente. No afirmar que cerrar sin Guardar revierte todas las ediciones de un documento existente.

Calibrar controles accesibles para el JAR antes de automatizar; los nombres/atajos leídos en fuente no sustituyen calibración. No usar coordenadas fijas ni extender permisos de doble clic de otras pantallas. Preparar oráculos independientes por identidad, importe original/operativo, medio, moneda y contexto; toda regla no confirmada se resuelve antes de habilitar su variante.

## Evidencia y límites

Contrastar documento, pagos, saldo, caja e inventario según el alcance de los pasos, con importes iniciales/finales y deltas esperados. Separar estados de preparación, persistencia de borrador/pagos y cierre definitivo. No exigir ausencia de todo registro cuando puede existir historia inactiva. Libro diario y caja pueden tener representaciones distintas: no sumar filas indiscriminadamente como dinero duplicado.

Registrar en informe privado JAR/SHA256, commit del harness, paquete, perfil, variante e identidades saneadas. INFO resume, DEBUG describe pasos y TRACE aporta diagnóstico acotado; todo fallo conserva paso, esperado, observado, categoría y evidencia. Causa no determinada si no hay prueba causal; nunca credenciales, configuración privada completa ni filas enteras.

## Recuperación

Conservar evidencia y consultar el estado antes de repetir una confirmación incierta. Cancelar por interfaz cuando el paso lo permita; no improvisar pagos compensatorios ni SQL comercial. Si no existe procedimiento aprobado para el estado parcial, mantener el bloqueo. Restaurar baseline antes de otra variante; anular una operación no reemplaza restaurar el laboratorio.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Rutas y líneas relativas a XGestion2:

- `src/ModuloVentas/Vistas/FormVenta.java:1941-1951`.
- `src/ModuloVentas/Vistas/FormVenta.java:5252-5273`.
- `test/ModuloVentas/Vistas/FormVentaPreventaPresupuestoEdicionPolicyTest.java:15-21`.

Las referencias describen reglas o riesgos; los tests fuente no acreditan el flujo E2E del JAR. Las modalidades pendientes de contrato están delimitadas arriba, sin inventar su soporte.

