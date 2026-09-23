---
{"id":"XG-COB-008","title":"Recuperar un fallo de cobro combinado sin repetir pagos","product":"xgestion","module":"cobros-combinados","tags":["xgestion","regression","cobros-combinados","cobros","recuperacion","integridad-operaciones"],"status":"planned"}
---

# XG-COB-008 — Recuperar un fallo de cobro combinado sin repetir pagos

## Objetivo

Conocer qué se registró antes de reintentar una carga o cierre con resultado incierto.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 3.**
Ver [mapa de cobros y documentos](../../docs/cobros-documentos.md).
No tiene Robot, seed propio ni ejecución real del JAR. Los resultados son criterios de aceptación; los pasos con contrato pendiente no afirman que esa funcionalidad exista ni se habilitan por observar la pantalla.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. Identificar JAR/SHA256, empresa, sucursal, puesto, operador y documentos de control.
- Datos QA-COB/QA-PRE/QA-DEV e importes de esta ficha son **propuestas sintéticas pendientes de seed y calibración**. `catalogo-comercial-v1` no acredita estos documentos, pagos o estados.
- Perfil local no fiscal; sin impresión, integraciones de pago, correo ni red. Sin ofertas, descuentos, recargos, impuestos adicionales ni financiación salvo variante explícita. Medios manuales QA separados de pasarelas reales.
- Venta ARS 2.000 y reparto 500/1.500; dos puntos de fallo separados: al ingresar la segunda línea y al confirmar cierre.
- Laboratorio local autorizado pendiente, capaz de producir error/timeout reproducible y distinguir fallo previo a persistir de respuesta perdida después. No cortar una base compartida.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Preparar el primer pago y activar el fallo al registrar el segundo. | Se informa el error; no se acredita éxito por cerrar un diálogo. Se conserva evidencia de qué pagos quedaron activos/inactivos. |
| Consultar la operación por identidad antes de repetir. | Determina si sigue abierta o ya cerró, y sus pagos/stock/caja. Si no puede determinarlo, reintento bloqueado. |
| Recuperar mediante el procedimiento aprobado para el estado comprobado. | Termina con un cierre válido por 2.000 y reparto efectivo 500/1.500; no vuelve a cobrar una venta ya cerrada. |
| Intentar confirmar desde una vista desactualizada del mismo documento. | No se duplica venta, cobro ni stock; mantener evidencia del rechazo o de la acción deshabilitada. |

## Variantes y dependencias

Error al reservar identidad, al guardar pago y al cerrar son fallos distintos. No presumir una transacción única desde la primera línea de Multiple hasta el cierre: la fuente inserta pagos durante la preparación. Procedimiento de reconciliación/restauración pendiente antes de habilitar cada variante.

Calibrar controles accesibles para el JAR antes de automatizar; los nombres/atajos leídos en fuente no sustituyen calibración. No usar coordenadas fijas ni extender permisos de doble clic de otras pantallas. Preparar oráculos independientes por identidad, importe original/operativo, medio, moneda y contexto; toda regla no confirmada se resuelve antes de habilitar su variante.

## Evidencia y límites

Contrastar documento, pagos, saldo, caja e inventario según el alcance de los pasos, con importes iniciales/finales y deltas esperados. Separar estados de preparación, persistencia de borrador/pagos y cierre definitivo. No exigir ausencia de todo registro cuando puede existir historia inactiva. Libro diario y caja pueden tener representaciones distintas: no sumar filas indiscriminadamente como dinero duplicado.

Registrar en informe privado JAR/SHA256, commit del harness, paquete, perfil, variante e identidades saneadas. INFO resume, DEBUG describe pasos y TRACE aporta diagnóstico acotado; todo fallo conserva paso, esperado, observado, categoría y evidencia. Causa no determinada si no hay prueba causal; nunca credenciales, configuración privada completa ni filas enteras.

## Recuperación

Conservar evidencia y consultar el estado antes de repetir una confirmación incierta. Cancelar por interfaz cuando el paso lo permita; no improvisar pagos compensatorios ni SQL comercial. Si no existe procedimiento aprobado para el estado parcial, mantener el bloqueo. Restaurar baseline antes de otra variante; anular una operación no reemplaza restaurar el laboratorio.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Rutas y líneas relativas a XGestion2:

- `src/ModuloVentas/Vistas/Dialogs/DialogCobroMultiple.java:391-400`.
- `src/ModuloVentas/Vistas/Dialogs/formTicketCierre.java:1916-1929`.
- `src/ModuloVentas/Vistas/FormVenta.java:6236-6238`.
- `src/ModuloVentas/Vistas/FormVenta.java:6305-6346`.

Las referencias describen reglas o riesgos; los tests fuente no acreditan el flujo E2E del JAR. Las modalidades pendientes de contrato están delimitadas arriba, sin inventar su soporte.

