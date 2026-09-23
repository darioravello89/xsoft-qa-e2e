---
{"id":"XG-PRE-002","title":"Cancelar la elección de moneda del presupuesto y corregir un rechazo","product":"xgestion","module":"presupuestos","tags":["xgestion","regression","presupuestos","monedas","recuperacion"],"status":"planned"}
---

# XG-PRE-002 — Cancelar la elección de moneda del presupuesto y corregir un rechazo

## Objetivo

Salir de la preparación sin guardar por accidente y volver a guardar correctamente.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 3.**
Ver [mapa de cobros y documentos](../../docs/cobros-documentos.md).
No tiene Robot, seed propio ni ejecución real del JAR. Los resultados son criterios de aceptación; los pasos con contrato pendiente no afirman que esa funcionalidad exista ni se habilitan por observar la pantalla.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. Identificar JAR/SHA256, empresa, sucursal, puesto, operador y documentos de control.
- Datos QA-COB/QA-PRE/QA-DEV e importes de esta ficha son **propuestas sintéticas pendientes de seed y calibración**. `catalogo-comercial-v1` no acredita estos documentos, pagos o estados.
- Perfil local no fiscal; sin impresión, integraciones de pago, correo ni red. Sin ofertas, descuentos, recargos, impuestos adicionales ni financiación salvo variante explícita. Medios manuales QA separados de pasarelas reales.
- Documento nuevo sin ID persistido; dos unidades ARS 1.000, total ARS 2.000; cobros multimoneda ON y cotización 1.000.
- Stock de presupuesto OFF. Variante de cotización cero/ausente preparada en baseline separado; no editar DB durante la operación.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Iniciar Guardar presupuesto y elegir Cancelar en Moneda del presupuesto. | Permanece la propuesta editable; no guarda presupuesto ni cobro por cancelar la elección. |
| Repetir, elegir ARS y guardar sin imprimir. | Un presupuesto ARS 2.000; sin caja ni stock definitivo en este perfil. |
| En baseline inválido, elegir USD para guardar. | La cotización inválida rechaza antes de guardar; productos e importes de preparación siguen disponibles para corregir. |
| Reiniciar desde perfil válido y guardar la variante USD con total previamente calculado. | Se conserva la moneda elegida y un solo presupuesto; el intento rechazado no aparece como documento guardado. |

## Variantes y dependencias

Cerrar el selector equivale a no elegir moneda; probar sin filas por separado. La cancelación aquí corresponde a documento nuevo: no prometer que cerrar una venta ya existente deshace ediciones que se hubieran persistido antes. Presupuesto USD esperado: ARS 2.000 / 1.000 = USD 2 en el perfil definido.

Calibrar controles accesibles para el JAR antes de automatizar; los nombres/atajos leídos en fuente no sustituyen calibración. No usar coordenadas fijas ni extender permisos de doble clic de otras pantallas. Preparar oráculos independientes por identidad, importe original/operativo, medio, moneda y contexto; toda regla no confirmada se resuelve antes de habilitar su variante.

## Evidencia y límites

Contrastar documento, pagos, saldo, caja e inventario según el alcance de los pasos, con importes iniciales/finales y deltas esperados. Separar estados de preparación, persistencia de borrador/pagos y cierre definitivo. No exigir ausencia de todo registro cuando puede existir historia inactiva. Libro diario y caja pueden tener representaciones distintas: no sumar filas indiscriminadamente como dinero duplicado.

Registrar en informe privado JAR/SHA256, commit del harness, paquete, perfil, variante e identidades saneadas. INFO resume, DEBUG describe pasos y TRACE aporta diagnóstico acotado; todo fallo conserva paso, esperado, observado, categoría y evidencia. Causa no determinada si no hay prueba causal; nunca credenciales, configuración privada completa ni filas enteras.

## Recuperación

Conservar evidencia y consultar el estado antes de repetir una confirmación incierta. Cancelar por interfaz cuando el paso lo permita; no improvisar pagos compensatorios ni SQL comercial. Si no existe procedimiento aprobado para el estado parcial, mantener el bloqueo. Restaurar baseline antes de otra variante; anular una operación no reemplaza restaurar el laboratorio.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Rutas y líneas relativas a XGestion2:

- `src/ModuloVentas/Vistas/FormVenta.java:5188-5231`.
- `test/ModuloVentas/Vistas/FormVentaPresupuestoMonedaPolicyTest.java:31-83`.

Las referencias describen reglas o riesgos; los tests fuente no acreditan el flujo E2E del JAR. Las modalidades pendientes de contrato están delimitadas arriba, sin inventar su soporte.

