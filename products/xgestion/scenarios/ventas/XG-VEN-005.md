---
{"id":"XG-VEN-005","title":"Cobrar en efectivo con vuelto","product":"xgestion","module":"ventas","tags":["xgestion","regression","ventas","escritura","efectivo"],"status":"implemented","test":"products/xgestion/suites/ventas.robot"}
---

# XG-VEN-005 — Cobrar en efectivo con vuelto

## Objetivo

El cajero recibe un importe mayor al total y entrega el vuelto correcto.

## Estado

**Automatización implementada; ejecución real sobre el JAR pendiente.** El caso pertenece a la [etapa 1 — Venta cotidiana](../../docs/roadmap.md) y requiere la extensión privada `sales_journeys` y su mapa calibrado. Un `check`, dry-run o test del framework no acredita PASS sobre XGestion.

## Perfil, precondiciones y datos

- Windows QA exclusivo, offline, escritorio desbloqueado y ejecución serial por el runner.
- Paquete autorizado, licencia QA vigente, base aislada restaurada y selectores calibrados para el SHA-256 del JAR.
- Usuario, empresa, sucursal y computadora QA definidos en el paquete; credenciales locales privadas.
- Venta local no fiscal en ARS, producto a precio final $1.000 y stock suficiente; cantidad habitual 2 y total $2.000. Efectivo; `cartelPagoVuelto=true`; abandono sin supervisor.
- Sin ofertas, descuentos, puntos, recargos, impresión, facturación ni pagos externos.
- Perfil `ventas-etapa1`: extensión `sales_journeys` completa, columnas de la grilla observadas y defaults de cliente/lista/comprobante documentados. Ver [contrato privado](../../docs/paquete.md).
- `cartelPagoVuelto=true`. Sin diálogo y monto insuficiente requieren casos distintos.

## Pasos y resultados esperados

1. Abrir venta no fiscal y cargar 2 unidades de $1.000. **Esperado:** total $2.000 ARS.
2. Usar el cierre de venta y elegir efectivo. **Esperado:** el diálogo de cobro muestra total $2.000 y permite cargar lo recibido.
3. Ingresar $3.000 recibidos. **Esperado:** vuelto $1.000, manteniendo total de venta $2.000.
4. Confirmar. **Esperado:** termina el cobro y queda una sola venta cerrada por $2.000.
5. Revisar evidencia. **Esperado:** producto/cantidad correctos, stock −2 y entrada neta de caja +$2.000; lo recibido no aumenta el precio de la venta.

## Recuperación

Si falla, conservar el reporte privado y el paso observado. El runner cierra solo su proceso y prepara el baseline en la siguiente ejecución. No reparar resultados borrando datos ni modificar controles de seguridad. Las cancelaciones y reintentos descritos son parte del caso, no limpieza oculta. No continuar después de un fallo como si el paso hubiera aprobado.

## Evidencia para QA

INFO muestra ID, resultado y resumen; DEBUG añade pasos; TRACE diagnóstico saneado. En cualquier nivel un fallo debe incluir paso, esperado, observado, categoría y evidencia disponible. Si la causa no está demostrada, informar «causa no determinada». Capturas solo de ventanas QA autenticadas, sin credenciales. Registrar versión/hash del JAR, paquete, perfil y ruta privada del reporte.

## Anexo técnico de evidencia

La UI muestra recibido $3.000 y vuelto $1.000. `ventas` conserva `Pagado=3000`, `Vuelto=1000` y `venTotal=2000`; `ventas_cuerpo` identifica el artículo y sus 2 unidades. El efectivo simple registra el total aplicado en `movimientos_finanzas` (+2000), sin filas en `ventas_pagos`; no exigir una fila de pago múltiple. `movimientos_articulos` descuenta 2 unidades y ambos movimientos se vinculan a la venta nueva.

Lecturas acotadas a empresa/sucursal/computadora e identidad de artículo/operación. No usar `MAX(venId)` como identidad única ni escribir SQL de negocio. Las consultas son de solo lectura. Los selectores y columnas deben verificarse sobre el JAR; la implementación del oráculo no acredita ejecución real.

## Trazabilidad y límites

En el commit de referencia: `src/ModuloVentas/Vistas/Dialogs/formTicketCierre.java:306` calcula pago/vuelto, `:322` conserva recibido y `:1440` actualiza el vuelto visible; `FormVenta.java:6041` abre el diálogo y `:6051` recibe el resultado. `src/ModuloVentas/Entidades/TicketVenta.java:2029` persiste Pagado/Vuelto y `:2125` registra caja simple por venTotal. `FormVentaCierreCobroPolicyTest.java` separa el perfil automático.

La [cobertura](../../docs/cobertura.md) identifica la referencia XGestion2 `release/189-lts`, `f34238183d494259bed1279dd7d9aac0ce16a3ae`. Fuente y tests orientan expectativas; no demuestran equivalencia del JAR ni ejecución real. No cubre variantes de otras configuraciones, monedas, permisos o dispositivos.
