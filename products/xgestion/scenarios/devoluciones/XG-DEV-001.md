---
{"id":"XG-DEV-001","title":"Anular una venta pagada devolviendo el neto recibido","product":"xgestion","module":"devoluciones","tags":["xgestion","regression","devoluciones","cobros","efectivo","caja","stock"],"status":"planned"}
---

# XG-DEV-001 — Anular una venta pagada devolviendo el neto recibido

## Objetivo

Devolver el dinero aplicado a una venta y reponer sus productos sin devolver también el vuelto ya entregado.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 4.**
Ver [mapa de cobros y documentos](../../docs/cobros-documentos.md).
No tiene Robot, seed propio ni ejecución real del JAR. Los resultados son criterios de aceptación; los pasos con contrato pendiente no afirman que esa funcionalidad exista ni se habilitan por observar la pantalla.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. Identificar JAR/SHA256, empresa, sucursal, puesto, operador y documentos de control.
- Datos QA-COB/QA-PRE/QA-DEV e importes de esta ficha son **propuestas sintéticas pendientes de seed y calibración**. `catalogo-comercial-v1` no acredita estos documentos, pagos o estados.
- Perfil local no fiscal; sin impresión, integraciones de pago, correo ni red. Sin ofertas, descuentos, recargos, impuestos adicionales ni financiación salvo variante explícita. Medios manuales QA separados de pasarelas reales.
- Venta local cerrada ARS 2.000: 2 unidades a 1.000; recibido efectivo ARS 3.000 y vuelto entregado ARS 1.000. Stock antes/después de venta 10/8.
- venta.devolucionDeDinero=true, comprobante sin emisión fiscal ni número fiscal, operador del mismo puesto/sucursal y motivo QA-DEV-001; caja posterior a venta conocida.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Seleccionar la venta, iniciar Anular Venta y cancelar el diálogo de motivo. | Venta vigente, stock 8 y caja sin nuevo egreso. |
| Repetir, completar motivo y elegir Devolver en el diálogo de dinero. | Venta anulada; devolución ARS 2.000, no 3.000; stock vuelve a 10 una sola vez. |
| Consultar venta, motivo y caja. | Ingreso neto original 2.000 compensado por egreso 2.000; conserva historia y operador. |
| Actualizar y revisar el mismo documento. | No se registra otra devolución ni reposición por consultar. |

## Variantes y dependencias

Venta con recibido exacto, centavos y opción No Devolver en baseline separado: anula sin acreditar egreso de dinero. No Devolver no significa cancelar la anulación. La disponibilidad del diálogo depende de configuración; no inferir devolución si está deshabilitado. Fiscal/nota de crédito quedan fuera de esta ficha.

Calibrar controles accesibles para el JAR antes de automatizar; los nombres/atajos leídos en fuente no sustituyen calibración. No usar coordenadas fijas ni extender permisos de doble clic de otras pantallas. Preparar oráculos independientes por identidad, importe original/operativo, medio, moneda y contexto; toda regla no confirmada se resuelve antes de habilitar su variante.

## Evidencia y límites

Contrastar documento, pagos, saldo, caja e inventario según el alcance de los pasos, con importes iniciales/finales y deltas esperados. Separar estados de preparación, persistencia de borrador/pagos y cierre definitivo. No exigir ausencia de todo registro cuando puede existir historia inactiva. Libro diario y caja pueden tener representaciones distintas: no sumar filas indiscriminadamente como dinero duplicado.

Registrar en informe privado JAR/SHA256, commit del harness, paquete, perfil, variante e identidades saneadas. INFO resume, DEBUG describe pasos y TRACE aporta diagnóstico acotado; todo fallo conserva paso, esperado, observado, categoría y evidencia. Causa no determinada si no hay prueba causal; nunca credenciales, configuración privada completa ni filas enteras.

## Recuperación

Conservar evidencia y consultar el estado antes de repetir una confirmación incierta. Cancelar por interfaz cuando el paso lo permita; no improvisar pagos compensatorios ni SQL comercial. Si no existe procedimiento aprobado para el estado parcial, mantener el bloqueo. Restaurar baseline antes de otra variante; anular una operación no reemplaza restaurar el laboratorio.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Rutas y líneas relativas a XGestion2:

- `src/ModuloVentas/Vistas/FormVentas.java:1323-1359`.
- `src/ModuloVentas/Vistas/FormVentas.java:1426-1442`.
- `src/ModuloVentas/Vistas/Dialogs/FormVentaAnulacionMotivo.java:70-92`.
- `src/ModuloVentas/Entidades/TicketVenta.java:3302-3346`.
- `test/ModuloVentas/Entidades/VentaTotalesCalculadorTest.java:87-105`.

Las referencias describen reglas o riesgos; los tests fuente no acreditan el flujo E2E del JAR. Las modalidades pendientes de contrato están delimitadas arriba, sin inventar su soporte.

