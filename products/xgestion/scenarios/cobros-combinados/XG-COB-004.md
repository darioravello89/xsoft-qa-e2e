---
{"id":"XG-COB-004","title":"Combinar pagos ARS y USD sin convertir dos veces","product":"xgestion","module":"cobros-combinados","tags":["xgestion","regression","cobros-combinados","cobros","monedas","caja"],"status":"planned"}
---

# XG-COB-004 — Combinar pagos ARS y USD sin convertir dos veces

## Objetivo

Cerrar con monedas distintas conservando cuánto se recibió realmente en cada una.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 3.**
Ver [mapa de cobros y documentos](../../docs/cobros-documentos.md).
No tiene Robot, seed propio ni ejecución real del JAR. Los resultados son criterios de aceptación; los pasos con contrato pendiente no afirman que esa funcionalidad exista ni se habilitan por observar la pantalla.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. Identificar JAR/SHA256, empresa, sucursal, puesto, operador y documentos de control.
- Datos QA-COB/QA-PRE/QA-DEV e importes de esta ficha son **propuestas sintéticas pendientes de seed y calibración**. `catalogo-comercial-v1` no acredita estos documentos, pagos o estados.
- Perfil local no fiscal; sin impresión, integraciones de pago, correo ni red. Sin ofertas, descuentos, recargos, impuestos adicionales ni financiación salvo variante explícita. Medios manuales QA separados de pasarelas reales.
- Total operativo ARS 2.000; efectivo ARS 500 más efectivo USD 1; cotización ARS 1.500/USD.
- Cobros multimoneda habilitados explícitamente; sin descuentos/recargos ni vuelto. Caja física ARS/USD inicial conocida, separada de equivalentes operativos.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Ingresar ARS 500 en el cobro múltiple. | Pago original ARS 500; faltante operativo ARS 1.500. |
| Seleccionar USD e ingresar 1. | Original USD 1, equivalente ARS 1.500; total operativo pagado ARS 2.000. |
| Alternar moneda de visualización del resumen y volver a ARS. | Los originales siguen 500 ARS y 1 USD; no se convierten nuevamente ni se modifica lo recibido. El resumen ARS vuelve a 2.000. |
| Cobrar y consultar documento y caja por moneda. | Una venta cubierta por el reparto; conserva monedas/importes originales y cotización de la operación. No se informa efectivo físico ARS 2.000 como si el dólar hubiera sido cambiado. |

## Variantes y dependencias

Variante total contable USD con importes de conversión exacta y redondeo acordado; la cifra USD visible para ARS 2.000 es una presentación redondeada, no otra entrada de dinero. La conciliación de caja multimoneda necesita definir dominios y campos del informe antes de automatizar.

Calibrar controles accesibles para el JAR antes de automatizar; los nombres/atajos leídos en fuente no sustituyen calibración. No usar coordenadas fijas ni extender permisos de doble clic de otras pantallas. Preparar oráculos independientes por identidad, importe original/operativo, medio, moneda y contexto; toda regla no confirmada se resuelve antes de habilitar su variante.

## Evidencia y límites

Contrastar documento, pagos, saldo, caja e inventario según el alcance de los pasos, con importes iniciales/finales y deltas esperados. Separar estados de preparación, persistencia de borrador/pagos y cierre definitivo. No exigir ausencia de todo registro cuando puede existir historia inactiva. Libro diario y caja pueden tener representaciones distintas: no sumar filas indiscriminadamente como dinero duplicado.

Registrar en informe privado JAR/SHA256, commit del harness, paquete, perfil, variante e identidades saneadas. INFO resume, DEBUG describe pasos y TRACE aporta diagnóstico acotado; todo fallo conserva paso, esperado, observado, categoría y evidencia. Causa no determinada si no hay prueba causal; nunca credenciales, configuración privada completa ni filas enteras.

## Recuperación

Conservar evidencia y consultar el estado antes de repetir una confirmación incierta. Cancelar por interfaz cuando el paso lo permita; no improvisar pagos compensatorios ni SQL comercial. Si no existe procedimiento aprobado para el estado parcial, mantener el bloqueo. Restaurar baseline antes de otra variante; anular una operación no reemplaza restaurar el laboratorio.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Rutas y líneas relativas a XGestion2:

- `src/ModuloVentas/Vistas/Dialogs/DialogCobroMultiple.java:363-390`.
- `src/ModuloVentas/Vistas/Dialogs/DialogCobroMultiple.java:582-600`.
- `src/ModuloVentas/Vistas/Dialogs/DialogCobroMultiple.java:672-691`.
- `test/ModuloVentas/Entidades/CobroMultipleMonedaCalculadorTest.java:14-56`.

Las referencias describen reglas o riesgos; los tests fuente no acreditan el flujo E2E del JAR. Las modalidades pendientes de contrato están delimitadas arriba, sin inventar su soporte.

