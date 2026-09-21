---
{"id":"XG-VEN-006","title":"Cancelar el cobro, retomarlo y cobrar una sola vez","product":"xgestion","module":"ventas","tags":["xgestion","regression","ventas","escritura","efectivo","cobros"],"status":"planned"}
---

# XG-VEN-006 — Cancelar el cobro, retomarlo y cobrar una sola vez

## Objetivo

El cajero vuelve desde el cobro para revisar la venta y después la cobra sin duplicarla.

## Estado

**Planificado: no hay prueba Robot de este caso.** La ficha define el recorrido a implementar y calibrar. Listarlo o validarlo con `qa.cmd check` no lo ejecuta ni acredita PASS. Pertenece a la [etapa 1 — Venta cotidiana](../../docs/roadmap.md).

## Perfil, precondiciones y datos

- Windows QA exclusivo, offline, escritorio desbloqueado y ejecución serial por el runner.
- Paquete autorizado, licencia QA vigente, base aislada restaurada y selectores calibrados para el SHA-256 del JAR.
- Usuario, empresa, sucursal y computadora QA definidos en el paquete; credenciales locales privadas.
- Venta local no fiscal en ARS, producto a precio final $1.000 y stock suficiente; cantidad habitual 2 y total $2.000. Efectivo; `cartelPagoVuelto=true`; abandono sin supervisor.
- Sin ofertas, descuentos, puntos, recargos, impresión, facturación ni pagos externos.
- cartelPagoVuelto=true. Cancelar ocurre antes de confirmar; no es anular una venta cobrada.

## Pasos y resultados esperados

1. Preparar venta no fiscal de 2 unidades por $2.000. **Esperado:** producto, cantidad y total correctos.
2. Abrir cobro en efectivo e ingresar $2.000. **Esperado:** el diálogo permite revisar antes de confirmar.
3. Cancelar el diálogo. **Esperado:** vuelve a la venta con las mismas líneas, cantidades y total, todavía sin cobrar.
4. Abrir nuevamente cobro y completar efectivo por $2.000. **Esperado:** confirma normalmente.
5. Revisar resultado. **Esperado:** una venta cerrada, stock descontado una vez y caja incrementada una vez.

## Recuperación

Si falla, conservar el reporte privado y el paso observado. El runner cierra solo su proceso y prepara el baseline en la siguiente ejecución. No reparar resultados borrando datos ni modificar controles de seguridad. Las cancelaciones y reintentos descritos son parte del caso, no limpieza oculta. No continuar después de un fallo como si el paso hubiera aprobado.

## Evidencia para QA

INFO muestra ID, resultado y resumen; DEBUG añade pasos; TRACE diagnóstico saneado. En cualquier nivel un fallo debe incluir paso, esperado, observado, categoría y evidencia disponible. Si la causa no está demostrada, informar «causa no determinada». Capturas solo de ventanas QA autenticadas, sin credenciales. Registrar versión/hash del JAR, paquete, perfil y ruta privada del reporte.

## Anexo técnico de evidencia

Evidencia intermedia después de cancelar: no nueva venta ni cambios de stock/caja. Al confirmar, una sola identidad nueva y deltas −2/+2000. No basta comprobar únicamente el total final.

Lecturas acotadas a empresa/sucursal/computadora e identidad de artículo/operación. No usar `MAX(venId)` como identidad única ni escribir SQL de negocio. Los oráculos y selectores adicionales todavía deben implementarse y verificarse.

## Trazabilidad y límites

FormVenta.java:6049, resultado del diálogo y :6072 rama cancelada; acción Cancelar en formTicketCierre.java. Las policies no ejercitan este ida y vuelta visible.

La [cobertura](../../docs/cobertura.md) identifica la referencia XGestion2 `release/189-lts`, `f34238183d494259bed1279dd7d9aac0ce16a3ae`. Fuente y tests orientan expectativas; no demuestran equivalencia del JAR ni ejecución real. No cubre variantes de otras configuraciones, monedas, permisos o dispositivos.
