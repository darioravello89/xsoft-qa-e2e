---
{"id":"XG-DEV-005","title":"Cancelar o rechazar una anulación sin afectar otra venta","product":"xgestion","module":"devoluciones","tags":["xgestion","regression","devoluciones","permisos","integridad-operaciones","recuperacion"],"status":"planned"}
---

# XG-DEV-005 — Cancelar o rechazar una anulación sin afectar otra venta

## Objetivo

Proteger el documento correcto cuando el operador cancela, omite el motivo o actúa desde otro contexto.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 4.**
Ver [mapa de cobros y documentos](../../docs/cobros-documentos.md).
No tiene Robot, seed propio ni ejecución real del JAR. Los resultados son criterios de aceptación; los pasos con contrato pendiente no afirman que esa funcionalidad exista ni se habilitan por observar la pantalla.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. Identificar JAR/SHA256, empresa, sucursal, puesto, operador y documentos de control.
- Datos QA-COB/QA-PRE/QA-DEV e importes de esta ficha son **propuestas sintéticas pendientes de seed y calibración**. `catalogo-comercial-v1` no acredita estos documentos, pagos o estados.
- Perfil local no fiscal; sin impresión, integraciones de pago, correo ni red. Sin ofertas, descuentos, recargos, impuestos adicionales ni financiación salvo variante explícita. Medios manuales QA separados de pasarelas reales.
- Ventas locales QA-DEV-A por ARS 1.000 y QA-DEV-B por ARS 3.000, con identidades completas distintas; listado ordenable y saldos/stock conocidos.
- Variantes de otra sucursal/puesto sólo con paquete multicontexto pendiente. Perfil de operador restringido requiere permiso concreto identificado; no se inventa un bypass de supervisor.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Ordenar/filtrar el listado, seleccionar A y abrir Anular Venta. | La acción corresponde a A por identidad, no a B por posición visual o número de fila. |
| Intentar confirmar sin motivo y luego cancelar. | Solicita motivo; tras cancelar ambas ventas, caja y stock siguen iguales. |
| En baseline autorizado de otro puesto/sucursal, intentar anular el documento ajeno. | Se rechaza indicando que debe hacerse desde su puesto/sucursal; ninguna venta se modifica. |
| Volver al contexto permitido y consultar ambas operaciones. | Se conservan importes y estado de A/B; no hubo devolución ni reversión por los intentos. |

## Variantes y dependencias

Rol sin permiso, documento ya anulado y dos documentos con el mismo número local requieren perfiles separados. El criterio de seleccionar la identidad correcta sigue vigente con orden/filtro del listado. No afirmar aislamiento empresarial sólo por pasar el bloqueo de sucursal/puesto.

Calibrar controles accesibles para el JAR antes de automatizar; los nombres/atajos leídos en fuente no sustituyen calibración. No usar coordenadas fijas ni extender permisos de doble clic de otras pantallas. Preparar oráculos independientes por identidad, importe original/operativo, medio, moneda y contexto; toda regla no confirmada se resuelve antes de habilitar su variante.

## Evidencia y límites

Contrastar documento, pagos, saldo, caja e inventario según el alcance de los pasos, con importes iniciales/finales y deltas esperados. Separar estados de preparación, persistencia de borrador/pagos y cierre definitivo. No exigir ausencia de todo registro cuando puede existir historia inactiva. Libro diario y caja pueden tener representaciones distintas: no sumar filas indiscriminadamente como dinero duplicado.

Registrar en informe privado JAR/SHA256, commit del harness, paquete, perfil, variante e identidades saneadas. INFO resume, DEBUG describe pasos y TRACE aporta diagnóstico acotado; todo fallo conserva paso, esperado, observado, categoría y evidencia. Causa no determinada si no hay prueba causal; nunca credenciales, configuración privada completa ni filas enteras.

## Recuperación

Conservar evidencia y consultar el estado antes de repetir una confirmación incierta. Cancelar por interfaz cuando el paso lo permita; no improvisar pagos compensatorios ni SQL comercial. Si no existe procedimiento aprobado para el estado parcial, mantener el bloqueo. Restaurar baseline antes de otra variante; anular una operación no reemplaza restaurar el laboratorio.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Rutas y líneas relativas a XGestion2:

- `src/ModuloVentas/Vistas/FormVentas.java:1323-1359`.
- `src/ModuloVentas/Vistas/FormVentas.java:1441-1442`.
- `src/ModuloVentas/Vistas/Dialogs/FormVentaAnulacionMotivo.java:70-92`.

Las referencias describen reglas o riesgos; los tests fuente no acreditan el flujo E2E del JAR. Las modalidades pendientes de contrato están delimitadas arriba, sin inventar su soporte.

