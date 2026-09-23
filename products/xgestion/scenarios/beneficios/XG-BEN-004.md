---
{"id":"XG-BEN-004","title":"Canjear puntos, cancelar y cobrar una sola vez","product":"xgestion","module":"beneficios","tags":["xgestion","regression","beneficios","fidelizacion","descuentos","cobros"],"status":"planned"}
---

# XG-BEN-004 — Canjear puntos, cancelar y cobrar una sola vez

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
- Fixture NUEVO PENDIENTE: Cliente QA-BEN-C1 con 100 puntos vigentes y ningún consumo anterior; valor ARS 10/punto, acumulación 1 punto cada ARS 100 netos. Artículo elegible ARS 1.000; canje 20 puntos; venta al contado, sin otros beneficios.
- Confirmar perfil, controles por teclado/JAB y lecturas por identidad antes
  de implementar. El seed comercial actual no garantiza estos datos.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Elegir el cliente, cargar el artículo y solicitar 20 puntos. | Descuento ARS 200; total ARS 800; la intención de uso no es todavía un consumo definitivo. |
| 2 | Abrir el cobro y cancelarlo. | La venta sigue editable; no hay venta cerrada, ingreso ni consumo definitivo de puntos. |
| 3 | Retomar y cobrar ARS 800. | Una venta, un cobro y uso de 20 puntos; acumula 8 nuevos bajo este perfil. |
| 4 | Iniciar otra venta y consultar el saldo. | Saldo vigente 88 puntos (100 − 20 + 8), sin duplicación por reapertura. |

## Variantes y dependencias

Baseline independiente para abandonar antes de cobrar: conservar 100 puntos y ningún consumo. Probar canje que cubre el total con contrato de cierre en cero calibrado. Fallo de persistencia o lectura de saldo no permite declarar éxito; no ajustar los puntos por SQL para repetir.

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

- `src/ModuloVentas/Vistas/FormVenta.java:7077-7129`.
- `src/ModuloVentas/Vistas/FormVenta.java:7155-7206`.
- `src/ModuloVentas/Vistas/FormVenta.java:7342-7441`.

Al validar registrar build/SHA256 del JAR, perfil, datos, fecha y reporte privado
saneado. Credenciales, configuración privada y capturas sensibles quedan fuera
del repositorio.
