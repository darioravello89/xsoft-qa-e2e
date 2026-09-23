---
{"id":"XG-BEN-001","title":"Combinar descuento por artículo y descuento global sin repetirlos","product":"xgestion","module":"beneficios","tags":["xgestion","regression","beneficios","descuentos"],"status":"planned"}
---

# XG-BEN-001 — Combinar descuento por artículo y descuento global sin repetirlos

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
- Fixture NUEVO PENDIENTE: Vender dos unidades de QA-BEN-A a ARS 1.000; stock inicial 10 unidades; descuento por artículo 10 %, global 10 %, sin oferta ni puntos. Operador autorizado.
- Confirmar perfil, controles por teclado/JAB y lecturas por identidad antes
  de implementar. El seed comercial actual no garantiza estos datos.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Cargar las dos unidades y aplicar 10 % al artículo. | Bruto ARS 2.000, descuento por artículo ARS 200, base restante ARS 1.800. |
| 2 | Aplicar 10 % global y abrir/cancelar el cobro. | Descuento global ARS 180; total ARS 1.620. Cancelar conserva una venta sin cobrar. |
| 3 | Volver al renglón, guardar sin cambios y retomar el cobro. | Total ARS 1.620; no se aplican nuevamente los descuentos. |
| 4 | Cobrar ARS 1.620 y consultar el comprobante. | Una venta por ARS 1.620, dos unidades, stock −2 e ingreso efectivo neto ARS 1.620. |

## Variantes y dependencias

Repetir global por importe ARS 180. Límite: solicitar un importe global mayor que la base; el descuento aplicable no supera ARS 1.800 ni deja total negativo. Fijar la interacción de rechazo/ajuste en calibración. Perfil con oferta + descuento global + descuento por pago requiere importes independientes aprobados antes de ejecutarlo; PRM-079 cubre otra ruta (descuento manual por artículo sobre oferta).

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

- `test/ModuloVentas/Vistas/FormVentaDescuentosGlobalesTest.java:12-24`.
- `src/ModuloVentas/Vistas/FormVenta.java:3103-3155`.

Al validar registrar build/SHA256 del JAR, perfil, datos, fecha y reporte privado
saneado. Credenciales, configuración privada y capturas sensibles quedan fuera
del repositorio.
