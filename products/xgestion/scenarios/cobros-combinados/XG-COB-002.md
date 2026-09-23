---
{"id":"XG-COB-002","title":"Corregir un pago cargado antes de completar el cobro combinado","product":"xgestion","module":"cobros-combinados","tags":["xgestion","regression","cobros-combinados","cobros","recuperacion"],"status":"planned"}
---

# XG-COB-002 — Corregir un pago cargado antes de completar el cobro combinado

## Objetivo

Quitar un importe equivocado y sustituirlo sin conservar el pago anterior en el total.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 3.**
Ver [mapa de cobros y documentos](../../docs/cobros-documentos.md).
No tiene Robot, seed propio ni ejecución real del JAR. Los resultados son criterios de aceptación; los pasos con contrato pendiente no afirman que esa funcionalidad exista ni se habilitan por observar la pantalla.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. Identificar JAR/SHA256, empresa, sucursal, puesto, operador y documentos de control.
- Datos QA-COB/QA-PRE/QA-DEV e importes de esta ficha son **propuestas sintéticas pendientes de seed y calibración**. `catalogo-comercial-v1` no acredita estos documentos, pagos o estados.
- Perfil local no fiscal; sin impresión, integraciones de pago, correo ni red. Sin ofertas, descuentos, recargos, impuestos adicionales ni financiación salvo variante explícita. Medios manuales QA separados de pasarelas reales.
- Venta ARS 2.000; pagos iniciales efectivo 500 y tarjeta manual 1.000. Corregir tarjeta a 800 y agregar transferencia manual 700.
- Ruta de eliminación por teclado/JAB pendiente. La fuente sólo muestra doble clic en fila; no está autorizado automáticamente por el permiso concedido para el editor de cantidades de Venta.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Cargar efectivo 500 y tarjeta 1.000. | Pagado 1.500, faltan 500; ambas líneas pertenecen a esta venta. |
| Quitar la línea de tarjeta mediante la acción accesible autorizada para esta pantalla. | Permanece efectivo 500 y faltan 1.500. Paso bloqueado hasta contar con esa acción o autorización específica; no inventar botón Eliminar. |
| Ingresar tarjeta 800 y transferencia manual 700. | Pagado 2.000 y faltante 0; el pago retirado de 1.000 no participa. |
| Completar el cierre y consultar el reparto. | Efectivo 500, tarjeta 800 y transferencia 700; un solo cierre ARS 2.000. |

## Variantes y dependencias

Repetir dos pagos del mismo medio con notas distintas para seleccionar por identidad, y variar orden de las filas. Corrección significa quitar/reingresar; no se verificó editor directo de una línea. Con documento cerrado, la fuente deshabilita ingreso/cobro y la eliminación; conservar el histórico.

Calibrar controles accesibles para el JAR antes de automatizar; los nombres/atajos leídos en fuente no sustituyen calibración. No usar coordenadas fijas ni extender permisos de doble clic de otras pantallas. Preparar oráculos independientes por identidad, importe original/operativo, medio, moneda y contexto; toda regla no confirmada se resuelve antes de habilitar su variante.

## Evidencia y límites

Contrastar documento, pagos, saldo, caja e inventario según el alcance de los pasos, con importes iniciales/finales y deltas esperados. Separar estados de preparación, persistencia de borrador/pagos y cierre definitivo. No exigir ausencia de todo registro cuando puede existir historia inactiva. Libro diario y caja pueden tener representaciones distintas: no sumar filas indiscriminadamente como dinero duplicado.

Registrar en informe privado JAR/SHA256, commit del harness, paquete, perfil, variante e identidades saneadas. INFO resume, DEBUG describe pasos y TRACE aporta diagnóstico acotado; todo fallo conserva paso, esperado, observado, categoría y evidencia. Causa no determinada si no hay prueba causal; nunca credenciales, configuración privada completa ni filas enteras.

## Recuperación

Conservar evidencia y consultar el estado antes de repetir una confirmación incierta. Cancelar por interfaz cuando el paso lo permita; no improvisar pagos compensatorios ni SQL comercial. Si no existe procedimiento aprobado para el estado parcial, mantener el bloqueo. Restaurar baseline antes de otra variante; anular una operación no reemplaza restaurar el laboratorio.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Rutas y líneas relativas a XGestion2:

- `src/ModuloVentas/Vistas/Dialogs/DialogCobroMultiple.java:551-570`.
- `src/ModuloVentas/Vistas/Dialogs/DialogCobroMultiple.java:611-625`.
- `src/ModuloVentas/Entidades/VentaPago.java:545-570`.

Las referencias describen reglas o riesgos; los tests fuente no acreditan el flujo E2E del JAR. Las modalidades pendientes de contrato están delimitadas arriba, sin inventar su soporte.

