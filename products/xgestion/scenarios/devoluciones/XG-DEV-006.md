---
{"id":"XG-DEV-006","title":"Recuperar una anulación incierta sin duplicar reembolsos","product":"xgestion","module":"devoluciones","tags":["xgestion","regression","devoluciones","recuperacion","integridad-operaciones","caja","stock"],"status":"planned"}
---

# XG-DEV-006 — Recuperar una anulación incierta sin duplicar reembolsos

## Objetivo

Conservar evidencia y verificar los efectos antes de repetir una anulación fallida.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 4.**
Ver [mapa de cobros y documentos](../../docs/cobros-documentos.md).
No tiene Robot, seed propio ni ejecución real del JAR. Los resultados son criterios de aceptación; los pasos con contrato pendiente no afirman que esa funcionalidad exista ni se habilitan por observar la pantalla.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. Identificar JAR/SHA256, empresa, sucursal, puesto, operador y documentos de control.
- Datos QA-COB/QA-PRE/QA-DEV e importes de esta ficha son **propuestas sintéticas pendientes de seed y calibración**. `catalogo-comercial-v1` no acredita estos documentos, pagos o estados.
- Perfil local no fiscal; sin impresión, integraciones de pago, correo ni red. Sin ofertas, descuentos, recargos, impuestos adicionales ni financiación salvo variante explícita. Medios manuales QA separados de pasarelas reales.
- Venta pagada ARS 2.000, efectivo exacto, stock antes/después 10/8; devolución habilitada, sin fiscal.
- Laboratorio autorizado pendiente para fallo antes de anular, fallo entre efectos y respuesta perdida después de completar. Cada punto tiene baseline y procedimiento distinto.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Iniciar anulación y provocar el fallo controlado en el punto declarado. | No acreditar éxito por un cierre de ventana; conservar estado observado y diagnóstico. |
| Consultar venta, stock y devolución por identidad antes de reintentar. | Determina si no hubo efectos, si se completó o si quedaron efectos parciales. No afirmar rollback total sin evidencia. |
| Recuperar sólo con el procedimiento aprobado para ese estado. | Criterio final: una anulación, reposición total de dos unidades y devolución neta ARS 2.000 una sola vez; si no existe procedimiento, mantener bloqueo. |
| Consultar nuevamente e intentar repetir sobre el documento anulado según lo que permita la UI. | Sin segundo reembolso ni reposición; rechazo por estado o acción no disponible registrado. |

## Variantes y dependencias

La fuente de anulación no prueba una transacción atómica de todos sus efectos. No usar SQL correctivo ni repetir ciegamente como recuperación. Reimpresión o fallo de comunicación no equivalen a que la devolución no exista. Se enlaza con la integridad de confirmación [FIN-009](../conciliacion/XG-FIN-009.md) sin sustituir su caso de cierre.

Calibrar controles accesibles para el JAR antes de automatizar; los nombres/atajos leídos en fuente no sustituyen calibración. No usar coordenadas fijas ni extender permisos de doble clic de otras pantallas. Preparar oráculos independientes por identidad, importe original/operativo, medio, moneda y contexto; toda regla no confirmada se resuelve antes de habilitar su variante.

## Evidencia y límites

Contrastar documento, pagos, saldo, caja e inventario según el alcance de los pasos, con importes iniciales/finales y deltas esperados. Separar estados de preparación, persistencia de borrador/pagos y cierre definitivo. No exigir ausencia de todo registro cuando puede existir historia inactiva. Libro diario y caja pueden tener representaciones distintas: no sumar filas indiscriminadamente como dinero duplicado.

Registrar en informe privado JAR/SHA256, commit del harness, paquete, perfil, variante e identidades saneadas. INFO resume, DEBUG describe pasos y TRACE aporta diagnóstico acotado; todo fallo conserva paso, esperado, observado, categoría y evidencia. Causa no determinada si no hay prueba causal; nunca credenciales, configuración privada completa ni filas enteras.

## Recuperación

Conservar evidencia y consultar el estado antes de repetir una confirmación incierta. Cancelar por interfaz cuando el paso lo permita; no improvisar pagos compensatorios ni SQL comercial. Si no existe procedimiento aprobado para el estado parcial, mantener el bloqueo. Restaurar baseline antes de otra variante; anular una operación no reemplaza restaurar el laboratorio.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Rutas y líneas relativas a XGestion2:

- `src/ModuloVentas/Entidades/TicketVenta.java:3285-3385`.
- `src/ModuloVentas/Vistas/FormVentas.java:1438-1442`.

Las referencias describen reglas o riesgos; los tests fuente no acreditan el flujo E2E del JAR. Las modalidades pendientes de contrato están delimitadas arriba, sin inventar su soporte.

