---
{"id":"XG-BEN-005","title":"Limitar puntos por vigencia, saldo y elegibilidad","product":"xgestion","module":"beneficios","tags":["xgestion","regression","beneficios","fidelizacion","descuentos"],"status":"planned"}
---

# XG-BEN-005 — Limitar puntos por vigencia, saldo y elegibilidad

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
- Fixture NUEVO PENDIENTE: Fecha/reloj de aplicación y DB coordinados en laboratorio; vigencia 30 días. Cliente con 40 puntos ganados hace 10 días y 60 hace 40 días, sin usos. Valor ARS 10/punto; artículo elegible QA-BEN-E a ARS 100 por unidad (10 unidades iniciales) y artículo QA-BEN-X a ARS 1.000 excluido de acumulación, ambos con stock 20. Acumulación normal 1 punto cada ARS 100 netos. No cambiar el reloj del equipo cotidiano.
- Confirmar perfil, controles por teclado/JAB y lecturas por identidad antes
  de implementar. El seed comercial actual no garantiza estos datos.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Consultar el resumen del cliente y cargar 10 unidades de QA-BEN-E. | 100 acumulados, 60 vencidos y 40 disponibles; venta de ARS 1.000 antes del canje. |
| 2 | Solicitar 80 puntos en la venta de ARS 1.000. | Aplica como máximo 40 puntos/ARS 400; total ARS 600. El campo y el resumen explican el valor aplicado. |
| 3 | Editar QA-BEN-E de 10 a 1 unidad conservando la solicitud. | Canje limitado a 10 puntos/ARS 100; nunca total negativo ni uso superior al saldo. |
| 4 | Abandonar; iniciar otra venta del mismo cliente con una unidad de QA-BEN-X y canje en cero. | Abandono no consume puntos ni stock. La nueva venta totaliza ARS 1.000 y muestra cero puntos a acumular. |
| 5 | Cobrar ARS 1.000 y consultar nuevamente el resumen del cliente. | Una venta, stock de QA-BEN-X 19 e ingreso neto ARS 1.000; saldo disponible 40 sin nuevos puntos acumulados ni usados. |

## Variantes y dependencias

Vigencia 0 (sin vencimiento), límite exacto día 30 y día 31, saldo cero, valor de punto inválido y puntos negativos. La fuente usa días calendario; fijar zona/fecha y frontera antes de probar. Canasta mixta elegible/excluida exige decidir la base de acumulación: no asumir proporcionalidad por línea. Excluir acumulación no prueba prohibición de canje sobre ese artículo.

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
- `src/ModuloVentas/Vistas/FormVenta.java:7175-7222`.
- `src/ModuloVentas/Vistas/FormVenta.java:7359-7399`.

Al validar registrar build/SHA256 del JAR, perfil, datos, fecha y reporte privado
saneado. Credenciales, configuración privada y capturas sensibles quedan fuera
del repositorio.
