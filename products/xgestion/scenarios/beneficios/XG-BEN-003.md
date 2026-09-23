---
{"id":"XG-BEN-003","title":"Consultar impuestos y conservar el total entre presentación e histórico","product":"xgestion","module":"beneficios","tags":["xgestion","regression","beneficios","impuestos","comprobantes"],"status":"planned"}
---

# XG-BEN-003 — Consultar impuestos y conservar el total entre presentación e histórico

## Objetivo

Comprobar que el vendedor conserva importes y beneficios correctos durante el recorrido y que el comprobante coincide con lo cobrado.

## Estado y alcance

**Pendiente de automatizar (`planned`), prioridad P0 por importes/saldos.**
Ver [beneficios e impuestos](../../docs/beneficios-impuestos.md). Sin Robot,
seed propio ni validación del JAR. No implica emisión fiscal.

## Precondiciones y datos

- Windows QA aislado, paquete autorizado, JAR identificado y baseline restaurable.
- ARS, venta local no fiscal, sin impresión ni servicios; stock suficiente,
  descuentos/puntos/impuestos desactivados salvo los que declara esta ficha.
- Fixture NUEVO PENDIENTE: Tres artículos QA: bases ARS 1.000 con tasa 21 %, ARS 1.000 con 10,5 % y ARS 500 con tasa 0 %. Una unidad de cada uno, sin descuentos ni otros impuestos. Total esperado ARS 2.815, bases ARS 2.500, impuesto ARS 315. Tasas sintéticas para cálculo; no certifican tratamiento fiscal.
- Confirmar perfil, controles por teclado/JAB y lecturas por identidad antes
  de implementar. El seed comercial actual no garantiza estos datos.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Cargar los tres artículos bajo el perfil de precios netos aprobado. | Importes finales ARS 1.210, ARS 1.105 y ARS 500; total ARS 2.815. |
| 2 | Abrir el desglose de impuestos y cerrarlo. | Muestra ARS 210 + ARS 105 y total de impuestos ARS 315. Consultar no modifica el total. |
| 3 | Cobrar y volver a consultar el documento. | Total e impuestos históricos conservan los valores; no se vuelve a adicionar el impuesto. |
| 4 | En un baseline independiente, usar precios finales con impuestos incluidos. | La canasta equivalente conserva total ARS 2.815 y desglose ARS 315, sin sumar dos veces el impuesto. |

## Variantes y dependencias

BLOQUEADO hasta declarar cómo representan neto/final los precios, el tipo de comprobante local que admite el desglose y las tasas en el JAR. Tasa cero no equivale a exento: el perfil exento tiene configuración propia pendiente. Extensiones: distintos conceptos/otros impuestos, cantidad fraccionada y descuento; cada una requiere cálculo esperado aprobado. No habilita emisión fiscal; ver FEL.

Las variantes requieren baseline y expectativas independientes. Si falta la
regla o el perfil, informar BLOQUEADO; no convertir lo observado en esperado.

## Evidencia y límites

Registrar cliente/producto, cantidades, base, descuentos, impuesto, puntos,
total, pago y deltas aplicables por identidad de operación. Contrastar valores
visibles y persistidos sin exportar filas completas. INFO resume; DEBUG muestra
pasos; TRACE conserva diagnóstico saneado. Cada fallo informa paso, esperado,
observado y evidencia; causa no determinada si no está demostrada.

## Recuperación

Cancelar acciones no confirmadas. Ante un resultado incierto consultar por
identidad antes de repetir; conservar informe privado y restaurar el baseline
por el procedimiento del laboratorio. No corregir saldos ni importes mediante
SQL durante el caso; cerrar únicamente procesos propios.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Las referencias descubren reglas y riesgos;
no constituyen validación E2E ni pruebas ejecutadas en esta entrega.

- `test/ModuloVentas/Vistas/FormVentaImpuestosDesglosePolicyTest.java:15-32`.
- `src/ModuloVentas/Vistas/FormVenta.java:3137-3164`.

Al validar registrar build/SHA256 del JAR, perfil, datos, fecha y reporte privado
saneado. Credenciales, configuración privada y capturas sensibles quedan fuera
del repositorio.
