---
{"id":"XG-COB-005","title":"Alternar, editar y vaciar el importe recibido sin recuperar valores viejos","product":"xgestion","module":"cobros-combinados","tags":["xgestion","regression","cobros-combinados","cobros","monedas","recuperacion"],"status":"planned"}
---

# XG-COB-005 — Alternar, editar y vaciar el importe recibido sin recuperar valores viejos

## Objetivo

Mantener el importe realmente ingresado al cambiar la moneda visible antes de confirmar.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 3.**
Ver [mapa de cobros y documentos](../../docs/cobros-documentos.md).
No tiene Robot, seed propio ni ejecución real del JAR. Los resultados son criterios de aceptación; los pasos con contrato pendiente no afirman que esa funcionalidad exista ni se habilitan por observar la pantalla.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. Identificar JAR/SHA256, empresa, sucursal, puesto, operador y documentos de control.
- Datos QA-COB/QA-PRE/QA-DEV e importes de esta ficha son **propuestas sintéticas pendientes de seed y calibración**. `catalogo-comercial-v1` no acredita estos documentos, pagos o estados.
- Perfil local no fiscal; sin impresión, integraciones de pago, correo ni red. Sin ofertas, descuentos, recargos, impuestos adicionales ni financiación salvo variante explícita. Medios manuales QA separados de pasarelas reales.
- Cierre simple de control ARS 1.000, cotización 1.500 y cobros multimoneda habilitados; recibido inicial ARS 500. Esta ficha contrasta la entrada simple usada junto al acceso a Multiple, no aplica sus redondeos a cuotas.
- Sin integrar pagos externos; no cerrar por ARS 500 una venta de ARS 1.000.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Escribir ARS 500 y alternar visualización a USD y nuevamente ARS varias veces. | USD visible 0,33 y regreso ARS 500; el importe real sigue ARS 500, sin degradarse a ARS 495 por reconvertir el redondeo mostrado. |
| Volver a ARS y sustituir lo recibido por ARS 600. | El nuevo ingreso real es ARS 600; no conserva una proyección anterior de ARS 500. |
| Vaciar el campo y luego ingresar cero. | Recibido efectivo considerado cero; no reaparece el valor anterior al alternar moneda. |
| Cancelar, retomar y completar un pago válido de ARS 1.000. | Un único cobro final ARS 1.000; los valores de preparación no generaron pagos. |

## Variantes y dependencias

La entrada manual de USD, a diferencia de alternar la presentación de un importe ARS, tiene regla comercial propia de redondeo. Acordar esos ejemplos antes de ampliar. Cuotas usa conversión directa distinta; no copiar el oráculo del cierre simple a CUO-002. Complementa COB-004 sin asumir idéntico estado interno.

Calibrar controles accesibles para el JAR antes de automatizar; los nombres/atajos leídos en fuente no sustituyen calibración. No usar coordenadas fijas ni extender permisos de doble clic de otras pantallas. Preparar oráculos independientes por identidad, importe original/operativo, medio, moneda y contexto; toda regla no confirmada se resuelve antes de habilitar su variante.

## Evidencia y límites

Contrastar documento, pagos, saldo, caja e inventario según el alcance de los pasos, con importes iniciales/finales y deltas esperados. Separar estados de preparación, persistencia de borrador/pagos y cierre definitivo. No exigir ausencia de todo registro cuando puede existir historia inactiva. Libro diario y caja pueden tener representaciones distintas: no sumar filas indiscriminadamente como dinero duplicado.

Registrar en informe privado JAR/SHA256, commit del harness, paquete, perfil, variante e identidades saneadas. INFO resume, DEBUG describe pasos y TRACE aporta diagnóstico acotado; todo fallo conserva paso, esperado, observado, categoría y evidencia. Causa no determinada si no hay prueba causal; nunca credenciales, configuración privada completa ni filas enteras.

## Recuperación

Conservar evidencia y consultar el estado antes de repetir una confirmación incierta. Cancelar por interfaz cuando el paso lo permita; no improvisar pagos compensatorios ni SQL comercial. Si no existe procedimiento aprobado para el estado parcial, mantener el bloqueo. Restaurar baseline antes de otra variante; anular una operación no reemplaza restaurar el laboratorio.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Rutas y líneas relativas a XGestion2:

- `test/ModuloVentas/Vistas/Dialogs/FormTicketCierreMonedaStateTest.java:72-147`.
- `test/ModuloVentas/Vistas/Dialogs/FormTicketCierreMonedaStateTest.java:169-182`.

Las referencias describen reglas o riesgos; los tests fuente no acreditan el flujo E2E del JAR. Las modalidades pendientes de contrato están delimitadas arriba, sin inventar su soporte.

