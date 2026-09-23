---
{"id":"XG-BEN-006","title":"Cambiar de cliente o condición sin trasladar puntos ajenos","product":"xgestion","module":"beneficios","tags":["xgestion","regression","beneficios","fidelizacion","descuentos","cuenta-corriente"],"status":"planned"}
---

# XG-BEN-006 — Cambiar de cliente o condición sin trasladar puntos ajenos

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
- Fixture NUEVO PENDIENTE: C1 tiene 100 puntos; C2 tiene 0; consumidor final sin fidelización. Artículo elegible ARS 1.000, valor ARS 10/punto. C1 habilitado para cuenta corriente con límite suficiente. Sin descuentos por cliente ni listas distintas.
- Confirmar perfil, controles por teclado/JAB y lecturas por identidad antes
  de implementar. El seed comercial actual no garantiza estos datos.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Elegir C1 y solicitar 20 puntos. | Cliente C1, descuento ARS 200, total ARS 800 antes de confirmar. |
| 2 | Cambiar a C2 y después a consumidor final. | No se usan los puntos de C1 en otra identidad; importe ARS 1.000 sin ese beneficio. Ningún saldo se altera. |
| 3 | Cancelar la venta y comenzar otra con C1 para cuenta corriente. | Fidelización omitida: no canjea ni acumula puntos en esa ruta; total/deuda ARS 1.000 al confirmar, sin ingreso efectivo por crédito. |
| 4 | Comenzar otra venta al contado con C1. | La omisión del crédito no contamina la nueva operación; saldo original 100 disponible y cliente correcto. |

## Variantes y dependencias

Repetir con programa desactivado, cierre/reapertura y cambio de cliente rechazado/cancelado. El cambio de cliente con canje ya escrito requiere revisar el comportamiento visible y la regla de reinicio antes de automatizar: nunca reutilizar un saldo ajeno. No aplicar esta expectativa de crédito a cuotas u otras rutas sin contrato propio.

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

- `src/ModuloVentas/Vistas/FormVenta.java:7059-7075`.
- `src/ModuloVentas/Vistas/FormVenta.java:7329-7351`.
- `src/ModuloVentas/Vistas/FormVenta.java:7077-7082`.

Al validar registrar build/SHA256 del JAR, perfil, datos, fecha y reporte privado
saneado. Credenciales, configuración privada y capturas sensibles quedan fuera
del repositorio.
