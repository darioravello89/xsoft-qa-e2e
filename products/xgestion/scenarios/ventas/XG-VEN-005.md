---
{"id":"XG-VEN-005","title":"Cobrar en efectivo con vuelto","product":"xgestion","module":"ventas","tags":["xgestion","regression","ventas","escritura","efectivo"],"status":"planned"}
---

# XG-VEN-005 — Cobrar en efectivo con vuelto

## Objetivo

El cajero recibe un importe mayor al total y entrega el vuelto correcto.

## Estado

**Planificado: no hay prueba Robot de este caso.** La ficha define el recorrido a implementar y calibrar. Listarlo o validarlo con `qa.cmd check` no lo ejecuta ni acredita PASS. Pertenece a la [etapa 1 — Venta cotidiana](../../docs/roadmap.md).

## Perfil, precondiciones y datos

- Windows QA exclusivo, offline, escritorio desbloqueado y ejecución serial por el runner.
- Paquete autorizado, licencia QA vigente, base aislada restaurada y selectores calibrados para el SHA-256 del JAR.
- Usuario, empresa, sucursal y computadora QA definidos en el paquete; credenciales locales privadas.
- Venta local no fiscal en ARS, producto a precio final $1.000 y stock suficiente; cantidad habitual 2 y total $2.000. Efectivo; `cartelPagoVuelto=true`; abandono sin supervisor.
- Sin ofertas, descuentos, puntos, recargos, impresión, facturación ni pagos externos.
- cartelPagoVuelto=true. Sin diálogo y monto insuficiente requieren casos distintos.

## Pasos y resultados esperados

1. Abrir venta no fiscal y cargar 2 unidades de $1.000. **Esperado:** total $2.000 ARS.
2. Cerrar y elegir efectivo. **Esperado:** el diálogo muestra el importe a cobrar.
3. Ingresar $3.000 recibidos. **Esperado:** vuelto $1.000, manteniendo total de venta $2.000.
4. Confirmar. **Esperado:** termina el cobro y queda una sola venta cerrada por $2.000.
5. Revisar evidencia. **Esperado:** producto/cantidad correctos, stock −2 y entrada neta de caja +$2.000; lo recibido no aumenta el precio de la venta.

## Recuperación

Si falla, conservar el reporte privado y el paso observado. El runner cierra solo su proceso y prepara el baseline en la siguiente ejecución. No reparar resultados borrando datos ni modificar controles de seguridad. Las cancelaciones y reintentos descritos son parte del caso, no limpieza oculta. No continuar después de un fallo como si el paso hubiera aprobado.

## Evidencia para QA

INFO muestra ID, resultado y resumen; DEBUG añade pasos; TRACE diagnóstico saneado. En cualquier nivel un fallo debe incluir paso, esperado, observado, categoría y evidencia disponible. Si la causa no está demostrada, informar «causa no determinada». Capturas solo de ventanas QA autenticadas, sin credenciales. Registrar versión/hash del JAR, paquete, perfil y ruta privada del reporte.

## Anexo técnico de evidencia

Reutilizar identidad/deltas de XG-VEN-001 y ampliar recibido/vuelto mediante UI y persistencia con semántica confirmada. No exigir que todos los registros de pago guarden 3000: distinguir total aplicado de dinero entregado.

Lecturas acotadas a empresa/sucursal/computadora e identidad de artículo/operación. No usar `MAX(venId)` como identidad única ni escribir SQL de negocio. Los oráculos y selectores adicionales todavía deben implementarse y verificarse.

## Trazabilidad y límites

formTicketCierre.java:296, cálculo de pago/vuelto; FormVenta.java:6041 diálogo y :6051 resultado. FormVentaCierreCobroPolicyTest.java separa el perfil automático.

La [cobertura](../../docs/cobertura.md) identifica la referencia XGestion2 `release/189-lts`, `f34238183d494259bed1279dd7d9aac0ce16a3ae`. Fuente y tests orientan expectativas; no demuestran equivalencia del JAR ni ejecución real. No cubre variantes de otras configuraciones, monedas, permisos o dispositivos.
