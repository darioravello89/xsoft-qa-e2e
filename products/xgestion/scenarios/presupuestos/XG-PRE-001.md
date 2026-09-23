---
{"id":"XG-PRE-001","title":"Guardar un presupuesto nuevo sin registrar un cobro","product":"xgestion","module":"presupuestos","tags":["xgestion","regression","presupuestos","comprobantes","stock"],"status":"planned"}
---

# XG-PRE-001 — Guardar un presupuesto nuevo sin registrar un cobro

## Objetivo

Conservar una propuesta de venta y sus cantidades sin tratarla como dinero recibido.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 3.**
Ver [mapa de cobros y documentos](../../docs/cobros-documentos.md).
No tiene Robot, seed propio ni ejecución real del JAR. Los resultados son criterios de aceptación; los pasos con contrato pendiente no afirman que esa funcionalidad exista ni se habilitan por observar la pantalla.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. Identificar JAR/SHA256, empresa, sucursal, puesto, operador y documentos de control.
- Datos QA-COB/QA-PRE/QA-DEV e importes de esta ficha son **propuestas sintéticas pendientes de seed y calibración**. `catalogo-comercial-v1` no acredita estos documentos, pagos o estados.
- Perfil local no fiscal; sin impresión, integraciones de pago, correo ni red. Sin ofertas, descuentos, recargos, impuestos adicionales ni financiación salvo variante explícita. Medios manuales QA separados de pasarelas reales.
- QA-PRE-A: producto ARS 1.000, cantidad 2, total ARS 2.000; cliente identificado, notas y lista conocidas; stock inicial 10.
- Perfil principal venta.presupuestoDescontarStock=false, cobros multimoneda OFF y acción Sólo Guardar, sin impresión. Baseline independiente con descuento de stock ON para la variante.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Preparar los productos e iniciar Guardar presupuesto. | Se ofrece guardar/imprimir según la UI; no es un diálogo de cobro. |
| Elegir Guardar sin impresión. | Un presupuesto por ARS 2.000, con cliente/notas y dos unidades; no se registra cobro ni ingreso de caja. |
| Consultar el documento y el inventario. | En el perfil OFF, stock 10; no hay venta cobrada por guardar el presupuesto. |
| Reabrir el presupuesto y consultar sin modificar. | Misma identidad y total; no crea una segunda propuesta ni un pago. |

## Variantes y dependencias

Perfil ON: preparar y acordar el momento de descuento de stock y su conservación al convertir; no afirmar que todo presupuesto carece de efectos de inventario. Variantes sin productos y total inválido deben rechazar sin un documento definitivo. La reapertura detallada de moneda/lista se mantiene en [LPR-022](../listas-precios/XG-LPR-022.md).

Calibrar controles accesibles para el JAR antes de automatizar; los nombres/atajos leídos en fuente no sustituyen calibración. No usar coordenadas fijas ni extender permisos de doble clic de otras pantallas. Preparar oráculos independientes por identidad, importe original/operativo, medio, moneda y contexto; toda regla no confirmada se resuelve antes de habilitar su variante.

## Evidencia y límites

Contrastar documento, pagos, saldo, caja e inventario según el alcance de los pasos, con importes iniciales/finales y deltas esperados. Separar estados de preparación, persistencia de borrador/pagos y cierre definitivo. No exigir ausencia de todo registro cuando puede existir historia inactiva. Libro diario y caja pueden tener representaciones distintas: no sumar filas indiscriminadamente como dinero duplicado.

Registrar en informe privado JAR/SHA256, commit del harness, paquete, perfil, variante e identidades saneadas. INFO resume, DEBUG describe pasos y TRACE aporta diagnóstico acotado; todo fallo conserva paso, esperado, observado, categoría y evidencia. Causa no determinada si no hay prueba causal; nunca credenciales, configuración privada completa ni filas enteras.

## Recuperación

Conservar evidencia y consultar el estado antes de repetir una confirmación incierta. Cancelar por interfaz cuando el paso lo permita; no improvisar pagos compensatorios ni SQL comercial. Si no existe procedimiento aprobado para el estado parcial, mantener el bloqueo. Restaurar baseline antes de otra variante; anular una operación no reemplaza restaurar el laboratorio.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Rutas y líneas relativas a XGestion2:

- `src/ModuloVentas/Vistas/FormVenta.java:5183-5195`.
- `src/ModuloVentas/Vistas/FormVenta.java:5217-5251`.
- `test/ModuloVentas/Vistas/FormVentaPresupuestoMonedaPolicyTest.java:15-56`.

Las referencias describen reglas o riesgos; los tests fuente no acreditan el flujo E2E del JAR. Las modalidades pendientes de contrato están delimitadas arriba, sin inventar su soporte.

