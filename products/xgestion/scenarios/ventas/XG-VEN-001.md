---
{"id":"XG-VEN-001","title":"Venta no fiscal en efectivo","product":"xgestion","module":"ventas","tags":["xgestion","regression","ventas","escritura","efectivo","cobros"],"status":"implemented","test":"products/xgestion/suites/ventas.robot"}
---

# XG-VEN-001 — Venta no fiscal en efectivo

## Objetivo

El vendedor cobra dos unidades de un producto y la operación queda registrada una sola vez.

## Estado y perfil

Automatización implementada; **ejecución real pendiente** de paquete privado, calibración y aceptación. Lint y dry-run no acreditan este recorrido en el producto.

- Windows QA exclusivo, offline, escritorio desbloqueado y ejecución serial por el runner.
- Paquete autorizado, licencia QA vigente, base aislada restaurada y selectores calibrados para el SHA-256 del JAR.
- Usuario, empresa, sucursal y computadora QA definidos en el paquete; credenciales locales privadas.
- Venta local no fiscal en ARS, producto a precio final $1.000 y stock suficiente; cantidad habitual 2 y total $2.000. Efectivo; `cartelPagoVuelto=true`; abandono sin supervisor.
- Sin ofertas, descuentos, puntos, recargos, impresión, facturación ni pagos externos.

## Pasos y resultados esperados

1. Ingresar como QA y abrir Nueva venta. **Esperado:** se trabaja en el contexto QA.
2. Elegir el comprobante interno no fiscal y cargar 2 unidades del producto de $1.000. **Esperado:** total visible de $2.000 ARS.
3. Cerrar la venta, elegir efectivo e ingresar $2.000 recibidos. **Esperado:** se puede confirmar el cobro.
4. Confirmar. **Esperado:** finaliza el diálogo y queda una única venta cerrada del producto y total previstos; el control automático de evidencia confirma stock y caja.

## Recuperación y límites

Si falla, conservar el reporte privado y el paso observado. El runner cierra solo su proceso y prepara el baseline en la siguiente ejecución. No reparar resultados borrando datos ni modificar controles de seguridad. Cobra el importe exacto. El vuelto se planifica en XG-VEN-005. No emitir F9, imprimir ni usar pagos externos.

## Evidencia para QA

INFO muestra ID, resultado y resumen; DEBUG añade pasos; TRACE diagnóstico saneado. En cualquier nivel un fallo debe incluir paso, esperado, observado, categoría y evidencia disponible. Si la causa no está demostrada, informar «causa no determinada». Capturas solo de ventanas QA autenticadas, sin credenciales. Registrar versión/hash del JAR, paquete, perfil y ruta privada del reporte.

## Anexo técnico y trazabilidad

Se toma una referencia de lectura antes de operar. El oráculo exige una venta nueva por empresa/sucursal/computadora/ID, activa y cerrada, del usuario QA; comprobante 99 sin CAE; un detalle del artículo fixture, cantidad 2, precio 1000 y total 2000; efectivo inmediato por 2000; stock −2 y caja +2000 vinculados a esa venta. Lee ventas, ventas_cuerpo, ventas_pagos, movimientos_articulos y movimientos_finanzas. No escribe SQL. Fuente: FormVenta.java, formTicketCierre.java y TicketVenta.java; contrato actual: products/xgestion/oracles.py.

La [cobertura](../../docs/cobertura.md) identifica la referencia XGestion2 `release/189-lts`, `f34238183d494259bed1279dd7d9aac0ce16a3ae`. Fuente y tests orientan expectativas; no demuestran equivalencia del JAR ni ejecución real. Se mantienen IDs, tags y archivo Robot existentes.
