---
{"id":"XG-PRE-006","title":"Distinguir propuestas editables de documentos cerrados o anulados","product":"xgestion","module":"presupuestos","tags":["xgestion","regression","presupuestos","permisos","comprobantes","integridad-operaciones"],"status":"planned"}
---

# XG-PRE-006 — Distinguir propuestas editables de documentos cerrados o anulados

## Objetivo

Consultar históricos sin volver a habilitar cambios y cobros de una operación terminada.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P1; etapa 3.**
Ver [mapa de cobros y documentos](../../docs/cobros-documentos.md).
No tiene Robot, seed propio ni ejecución real del JAR. Los resultados son criterios de aceptación; los pasos con contrato pendiente no afirman que esa funcionalidad exista ni se habilitan por observar la pantalla.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. Identificar JAR/SHA256, empresa, sucursal, puesto, operador y documentos de control.
- Datos QA-COB/QA-PRE/QA-DEV e importes de esta ficha son **propuestas sintéticas pendientes de seed y calibración**. `catalogo-comercial-v1` no acredita estos documentos, pagos o estados.
- Perfil local no fiscal; sin impresión, integraciones de pago, correo ni red. Sin ofertas, descuentos, recargos, impuestos adicionales ni financiación salvo variante explícita. Medios manuales QA separados de pasarelas reales.
- Tres documentos QA-PRE-EST con productos conocidos: presupuesto editable 2.000, venta cerrada 2.000 y venta anulada 2.000; identidades distintas.
- Operador con acceso de consulta; perfil restringido con permisos concretos pendiente. Sin modificar los originales durante preparación del caso.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Abrir el presupuesto editable. | Permite continuar la carga según PRE-003; consultar no lo cierra. |
| Abrir el documento cerrado e intentar agregar un producto por la acción normal. | La acción de agregar está deshabilitada; conserva detalle/total y cobro original. |
| Repetir con el anulado. | No habilita agregar productos como si fuera una venta nueva; historial y anulación conservados. |
| Volver a consultar pagos, stock y documentos. | Sin nuevo cobro, reversión o venta por las consultas e intentos rechazados. |

## Variantes y dependencias

Guardar/cobrar de nuevo, cambiar tipo y operador restringido requieren ubicar cada control y permiso, sin asumir que deshabilitar Agregar protege toda la pantalla. Abrir una copia como venta nueva, si existe, debe ser una acción explícita con otra identidad, no una reapertura accidental. La fuente sólo confirma la protección de Agregar y el chequeo de venta ya cerrada.

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
- `test/ModuloVentas/Vistas/FormVentaPreventaPresupuestoEdicionPolicyTest.java:15-21`.

Las referencias describen reglas o riesgos; los tests fuente no acreditan el flujo E2E del JAR. Las modalidades pendientes de contrato están delimitadas arriba, sin inventar su soporte.

