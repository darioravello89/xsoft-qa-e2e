---
{"id":"XG-COB-006","title":"Respetar la habilitación de monedas y rechazar cotizaciones inválidas","product":"xgestion","module":"cobros-combinados","tags":["xgestion","regression","cobros-combinados","cobros","monedas","recuperacion"],"status":"planned"}
---

# XG-COB-006 — Respetar la habilitación de monedas y rechazar cotizaciones inválidas

## Objetivo

Evitar un cobro convertido parcialmente o una moneda no habilitada por el perfil.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 3.**
Ver [mapa de cobros y documentos](../../docs/cobros-documentos.md).
No tiene Robot, seed propio ni ejecución real del JAR. Los resultados son criterios de aceptación; los pasos con contrato pendiente no afirman que esa funcionalidad exista ni se habilitan por observar la pantalla.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. Identificar JAR/SHA256, empresa, sucursal, puesto, operador y documentos de control.
- Datos QA-COB/QA-PRE/QA-DEV e importes de esta ficha son **propuestas sintéticas pendientes de seed y calibración**. `catalogo-comercial-v1` no acredita estos documentos, pagos o estados.
- Perfil local no fiscal; sin impresión, integraciones de pago, correo ni red. Sin ofertas, descuentos, recargos, impuestos adicionales ni financiación salvo variante explícita. Medios manuales QA separados de pasarelas reales.
- Tres baselines: cobros multimoneda OFF; ON con cotización 1.500; ON con cotización cero/ausente preparada por laboratorio.
- Venta ARS 2.000 y pago en preparación ARS 500; perfil sin promociones ni cuotas. La cotización inválida no se provoca editando datos productivos.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Con multimoneda OFF, abrir cierre y Multiple. | No permite elegir cobro USD sólo porque el artículo/documento use USD; conserva el circuito ARS definido. |
| Con multimoneda ON y cotización válida, seleccionar USD y preparar el pago. | La opción está disponible y los equivalentes corresponden a 1.500. |
| Desde el baseline inválido, intentar la conversión del pago preparado. | Se rechaza sin modificar parcialmente moneda/importe original ni cerrar venta; el ingreso ARS 500 se conserva si ya estaba preparado. |
| Cancelar y reabrir desde condición válida declarada. | Puede preparar el cobro correcto, sin pagos activos del intento inválido. |

## Variantes y dependencias

Cotización cambiada mientras un diálogo está abierto requiere definir si usa foto de venta o valor vigente y qué aviso debe mostrar; no inferirlo del flujo de cuotas. Esa variante permanece pendiente de contrato. Registrar por separado monto visible, original y operativo.

Calibrar controles accesibles para el JAR antes de automatizar; los nombres/atajos leídos en fuente no sustituyen calibración. No usar coordenadas fijas ni extender permisos de doble clic de otras pantallas. Preparar oráculos independientes por identidad, importe original/operativo, medio, moneda y contexto; toda regla no confirmada se resuelve antes de habilitar su variante.

## Evidencia y límites

Contrastar documento, pagos, saldo, caja e inventario según el alcance de los pasos, con importes iniciales/finales y deltas esperados. Separar estados de preparación, persistencia de borrador/pagos y cierre definitivo. No exigir ausencia de todo registro cuando puede existir historia inactiva. Libro diario y caja pueden tener representaciones distintas: no sumar filas indiscriminadamente como dinero duplicado.

Registrar en informe privado JAR/SHA256, commit del harness, paquete, perfil, variante e identidades saneadas. INFO resume, DEBUG describe pasos y TRACE aporta diagnóstico acotado; todo fallo conserva paso, esperado, observado, categoría y evidencia. Causa no determinada si no hay prueba causal; nunca credenciales, configuración privada completa ni filas enteras.

## Recuperación

Conservar evidencia y consultar el estado antes de repetir una confirmación incierta. Cancelar por interfaz cuando el paso lo permita; no improvisar pagos compensatorios ni SQL comercial. Si no existe procedimiento aprobado para el estado parcial, mantener el bloqueo. Restaurar baseline antes de otra variante; anular una operación no reemplaza restaurar el laboratorio.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Rutas y líneas relativas a XGestion2:

- `src/ModuloVentas/Vistas/Dialogs/DialogCobroMultiple.java:582-600`.
- `test/ModuloVentas/Vistas/Dialogs/FormTicketCierreCobroMultiplePolicyTest.java:57-80`.
- `test/ModuloVentas/Vistas/Dialogs/FormTicketCierreMonedaStateTest.java:150-166`.
- `test/ModuloVentas/Entidades/CobroMultipleMonedaCalculadorTest.java:71-81`.

Las referencias describen reglas o riesgos; los tests fuente no acreditan el flujo E2E del JAR. Las modalidades pendientes de contrato están delimitadas arriba, sin inventar su soporte.

