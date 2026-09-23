---
{"id":"XG-COB-007","title":"Calcular el vuelto de un cobro combinado sin duplicar dinero","product":"xgestion","module":"cobros-combinados","tags":["xgestion","regression","cobros-combinados","cobros","efectivo","caja"],"status":"planned"}
---

# XG-COB-007 — Calcular el vuelto de un cobro combinado sin duplicar dinero

## Objetivo

Distinguir importe recibido, aplicado y vuelto cuando el reparto excede el total.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 3.**
Ver [mapa de cobros y documentos](../../docs/cobros-documentos.md).
No tiene Robot, seed propio ni ejecución real del JAR. Los resultados son criterios de aceptación; los pasos con contrato pendiente no afirman que esa funcionalidad exista ni se habilitan por observar la pantalla.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. Identificar JAR/SHA256, empresa, sucursal, puesto, operador y documentos de control.
- Datos QA-COB/QA-PRE/QA-DEV e importes de esta ficha son **propuestas sintéticas pendientes de seed y calibración**. `catalogo-comercial-v1` no acredita estos documentos, pagos o estados.
- Perfil local no fiscal; sin impresión, integraciones de pago, correo ni red. Sin ofertas, descuentos, recargos, impuestos adicionales ni financiación salvo variante explícita. Medios manuales QA separados de pasarelas reales.
- Venta ARS 2.000; tarjeta manual ARS 1.000 y efectivo ARS 1.500; total recibido ARS 2.500, vuelto ARS 500.
- Perfil comercial de vuelto exclusivamente en efectivo, sin ajustes del medio. **Pendiente confirmar cómo el JAR atribuye el vuelto en caja por medio**; no convertir el reparto observado en regla.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Ingresar el reparto 1.000/1.500. | Resumen recibido ARS 2.500, total ARS 2.000 y vuelto ARS 500. |
| Revisar y confirmar el cierre una vez. | Venta ARS 2.000 y vuelto ARS 500; no registra una venta por 2.500. |
| Conciliar caja según el contrato de vuelto declarado. | Objetivo comercial: tarjeta aplicada 1.000 y efectivo neto 1.000, suma 2.000. Paso bloqueado hasta validar el contrato por medio y su representación. |
| Consultar otra vez los pagos y el comprobante. | Originales recibidos y vuelto explican el neto; no se devuelve nuevamente por consultar. |

## Variantes y dependencias

Sin vuelto, vuelto con centavos, orden de ingreso invertido y vuelto mostrado en USD. USD y descuentos/recargos del medio requieren ejemplos independientes. La fuente calcula agregado y vuelto, pero eso no acredita distribución física por medio. No aprobar por comparar únicamente total de venta.

Calibrar controles accesibles para el JAR antes de automatizar; los nombres/atajos leídos en fuente no sustituyen calibración. No usar coordenadas fijas ni extender permisos de doble clic de otras pantallas. Preparar oráculos independientes por identidad, importe original/operativo, medio, moneda y contexto; toda regla no confirmada se resuelve antes de habilitar su variante.

## Evidencia y límites

Contrastar documento, pagos, saldo, caja e inventario según el alcance de los pasos, con importes iniciales/finales y deltas esperados. Separar estados de preparación, persistencia de borrador/pagos y cierre definitivo. No exigir ausencia de todo registro cuando puede existir historia inactiva. Libro diario y caja pueden tener representaciones distintas: no sumar filas indiscriminadamente como dinero duplicado.

Registrar en informe privado JAR/SHA256, commit del harness, paquete, perfil, variante e identidades saneadas. INFO resume, DEBUG describe pasos y TRACE aporta diagnóstico acotado; todo fallo conserva paso, esperado, observado, categoría y evidencia. Causa no determinada si no hay prueba causal; nunca credenciales, configuración privada completa ni filas enteras.

## Recuperación

Conservar evidencia y consultar el estado antes de repetir una confirmación incierta. Cancelar por interfaz cuando el paso lo permita; no improvisar pagos compensatorios ni SQL comercial. Si no existe procedimiento aprobado para el estado parcial, mantener el bloqueo. Restaurar baseline antes de otra variante; anular una operación no reemplaza restaurar el laboratorio.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Rutas y líneas relativas a XGestion2:

- `src/ModuloVentas/Vistas/Dialogs/formTicketCierre.java:582-610`.
- `src/ModuloVentas/Vistas/Dialogs/DialogCobroMultiple.java:672-691`.
- `test/ModuloVentas/Entidades/CobroMultipleMonedaCalculadorTest.java:41-68`.

Las referencias describen reglas o riesgos; los tests fuente no acreditan el flujo E2E del JAR. Las modalidades pendientes de contrato están delimitadas arriba, sin inventar su soporte.

