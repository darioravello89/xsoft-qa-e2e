---
{"id":"XG-BEN-002","title":"Conservar centavos al editar cantidades fraccionadas y cobrar","product":"xgestion","module":"beneficios","tags":["xgestion","regression","beneficios","descuentos","stock"],"status":"planned"}
---

# XG-BEN-002 — Conservar centavos al editar cantidades fraccionadas y cobrar

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
- Fixture NUEVO PENDIENTE: QA-BEN-KG fraccionable, precio ARS 199,90/kg, stock 10 kg. Cantidad 0,500 kg, descuento global fijo ARS 0,05; sin oferta, puntos ni impuestos. Precisión de cantidad 3 decimales y dinero 2.
- Confirmar perfil, controles por teclado/JAB y lecturas por identidad antes
  de implementar. El seed comercial actual no garantiza estos datos.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Cargar 0,500 kg y aplicar el descuento fijo. | Bruto ARS 99,95; descuento ARS 0,05; total ARS 99,90. |
| 2 | Editar a 1 kg y volver a 0,500 kg. | Primero total ARS 199,85; al regresar ARS 99,90, sin arrastrar redondeos. |
| 3 | Cancelar y retomar el cobro; ingresar ARS 100. | Vuelto ARS 0,10 y una sola operación por ARS 99,90. |
| 4 | Consultar comprobante y existencias. | Cantidad 0,500 kg, stock 9,500 kg e ingreso efectivo neto ARS 99,90. Valores visibles e históricos coinciden. |

## Variantes y dependencias

Agregar al perfil aprobado cantidades con más decimales monetarios (p. ej., 0,375 kg) y descuento porcentual. Antes de automatizar esa variante, fijar la regla de redondeo por renglón/global y sus resultados independientes; no tomar el valor observado como esperado. No usa balanza ni implica cobertura de dispositivos.

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

- `src/ModuloVentas/Vistas/FormVenta.java:3103-3155`.
- `test/ModuloVentas/Vistas/FormVentaDescuentosGlobalesTest.java`.

Al validar registrar build/SHA256 del JAR, perfil, datos, fecha y reporte privado
saneado. Credenciales, configuración privada y capturas sensibles quedan fuera
del repositorio.
