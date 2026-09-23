---
{"id":"XG-PRE-005","title":"Completar una preventa editable y llevarla al cierre","product":"xgestion","module":"presupuestos","tags":["xgestion","regression","presupuestos","ventas","comprobantes","integridad-operaciones"],"status":"planned"}
---

# XG-PRE-005 — Completar una preventa editable y llevarla al cierre

## Objetivo

Continuar en escritorio una propuesta de preventa sin impedir agregar productos ni venderla dos veces.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 3.**
Ver [mapa de cobros y documentos](../../docs/cobros-documentos.md).
No tiene Robot, seed propio ni ejecución real del JAR. Los resultados son criterios de aceptación; los pasos con contrato pendiente no afirman que esa funcionalidad exista ni se habilitan por observar la pantalla.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. Identificar JAR/SHA256, empresa, sucursal, puesto, operador y documentos de control.
- Datos QA-COB/QA-PRE/QA-DEV e importes de esta ficha son **propuestas sintéticas pendientes de seed y calibración**. `catalogo-comercial-v1` no acredita estos documentos, pagos o estados.
- Perfil local no fiscal; sin impresión, integraciones de pago, correo ni red. Sin ofertas, descuentos, recargos, impuestos adicionales ni financiación salvo variante explícita. Medios manuales QA separados de pasarelas reales.
- Documento QA-PRE-PV ya disponible en el paquete como preventa en estado editable/presupuesto: A × 1 a ARS 1.000, cliente y origen identificados. Agregar B × 1 a ARS 500.
- Sin recepción de red durante el caso: origen de preventa preparado y documentado en baseline; el transporte/app externa queda fuera. Stock descuento de presupuesto OFF; cierre local no fiscal.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Abrir la preventa del cliente y revisar origen/cantidades. | Una propuesta editable por ARS 1.000, sin otra venta ni cobro creado al abrir. |
| Agregar B y guardar cambios. | Detalle A/B y total ARS 1.500 en la misma propuesta; no rechaza agregar sólo por venir de preventa. |
| Reabrir y completar el cierre autorizado con pago exacto ARS 1.500. | Una venta final por ARS 1.500 y efectos de caja/stock únicos. |
| Consultar la propuesta/origen y la venta resultante. | Trazabilidad conservada; no queda otra operación cobrable que permita duplicar la misma preventa. |

## Variantes y dependencias

Preventa cerrada/anulada se trata como histórica en PRE-006; cliente distinto requiere regla explícita. El test fuente sólo confirma habilitación de agregar en estado editable, no prueba conservación del origen ni idempotencia de conversión: esos son criterios E2E propuestos. La integración de recepción/sincronización requiere otro laboratorio.

Calibrar controles accesibles para el JAR antes de automatizar; los nombres/atajos leídos en fuente no sustituyen calibración. No usar coordenadas fijas ni extender permisos de doble clic de otras pantallas. Preparar oráculos independientes por identidad, importe original/operativo, medio, moneda y contexto; toda regla no confirmada se resuelve antes de habilitar su variante.

## Evidencia y límites

Contrastar documento, pagos, saldo, caja e inventario según el alcance de los pasos, con importes iniciales/finales y deltas esperados. Separar estados de preparación, persistencia de borrador/pagos y cierre definitivo. No exigir ausencia de todo registro cuando puede existir historia inactiva. Libro diario y caja pueden tener representaciones distintas: no sumar filas indiscriminadamente como dinero duplicado.

Registrar en informe privado JAR/SHA256, commit del harness, paquete, perfil, variante e identidades saneadas. INFO resume, DEBUG describe pasos y TRACE aporta diagnóstico acotado; todo fallo conserva paso, esperado, observado, categoría y evidencia. Causa no determinada si no hay prueba causal; nunca credenciales, configuración privada completa ni filas enteras.

## Recuperación

Conservar evidencia y consultar el estado antes de repetir una confirmación incierta. Cancelar por interfaz cuando el paso lo permita; no improvisar pagos compensatorios ni SQL comercial. Si no existe procedimiento aprobado para el estado parcial, mantener el bloqueo. Restaurar baseline antes de otra variante; anular una operación no reemplaza restaurar el laboratorio.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Rutas y líneas relativas a XGestion2:

- `src/ModuloVentas/Vistas/FormVenta.java:1941-1951`.
- `src/ModuloVentas/Vistas/FormVenta.java:6236-6238`.
- `src/ModuloVentas/Vistas/FormVenta.java:6305-6346`.
- `test/ModuloVentas/Vistas/FormVentaPreventaPresupuestoEdicionPolicyTest.java:15-21`.

Las referencias describen reglas o riesgos; los tests fuente no acreditan el flujo E2E del JAR. Las modalidades pendientes de contrato están delimitadas arriba, sin inventar su soporte.

