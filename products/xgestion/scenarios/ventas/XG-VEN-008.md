---
{"id":"XG-VEN-008","title":"Comenzar otra venta después de cobrar","product":"xgestion","module":"ventas","tags":["xgestion","regression","ventas","escritura"],"status":"planned"}
---

# XG-VEN-008 — Comenzar otra venta después de cobrar

## Objetivo

El vendedor atiende al siguiente cliente sin arrastrar datos de la venta anterior.

## Estado

**Planificado: no hay prueba Robot de este caso.** La ficha define el recorrido a implementar y calibrar. Listarlo o validarlo con `qa.cmd check` no lo ejecuta ni acredita PASS. Pertenece a la [etapa 1 — Venta cotidiana](../../docs/roadmap.md).

## Perfil, precondiciones y datos

- Windows QA exclusivo, offline, escritorio desbloqueado y ejecución serial por el runner.
- Paquete autorizado, licencia QA vigente, base aislada restaurada y selectores calibrados para el SHA-256 del JAR.
- Usuario, empresa, sucursal y computadora QA definidos en el paquete; credenciales locales privadas.
- Venta local no fiscal en ARS, producto a precio final $1.000 y stock suficiente; cantidad habitual 2 y total $2.000. Efectivo; `cartelPagoVuelto=true`; abandono sin supervisor.
- Sin ofertas, descuentos, puntos, recargos, impresión, facturación ni pagos externos.
- Mantener la misma sesión de aplicación. Dos tests que reinician el JAR no prueban este recorrido. No exigir blancos si existe un default legítimo del perfil.

## Pasos y resultados esperados

1. Preparar venta no fiscal de 2 unidades por $2.000 y cobrar en efectivo. **Esperado:** se completa una sola venta.
2. Iniciar otra venta por el flujo habitual, sin reiniciar XGestion. **Esperado:** no contiene líneas, cantidades, cobro ni total de la anterior; usa defaults del perfil QA.
3. Cargar una unidad del mismo producto. **Esperado:** una unidad y total $1.000, sin acumulación anterior.
4. Abandonar la segunda operación confirmando. **Esperado:** solo permanece la primera venta cobrada.
5. Revisar evidencia. **Esperado:** stock/caja reflejan únicamente la primera venta de 2 unidades por $2.000.

## Recuperación

Si falla, conservar el reporte privado y el paso observado. El runner cierra solo su proceso y prepara el baseline en la siguiente ejecución. No reparar resultados borrando datos ni modificar controles de seguridad. Las cancelaciones y reintentos descritos son parte del caso, no limpieza oculta. No continuar después de un fallo como si el paso hubiera aprobado.

## Evidencia para QA

INFO muestra ID, resultado y resumen; DEBUG añade pasos; TRACE diagnóstico saneado. En cualquier nivel un fallo debe incluir paso, esperado, observado, categoría y evidencia disponible. Si la causa no está demostrada, informar «causa no determinada». Capturas solo de ventanas QA autenticadas, sin credenciales. Registrar versión/hash del JAR, paquete, perfil y ruta privada del reporte.

## Anexo técnico de evidencia

Referencia inicial y posterior al primer cobro. Tras abandonar la segunda: mismos IDs/stock/caja que después del primer cobro; una venta total y deltas globales −2/+2000. Evidencia UI del inicio de la segunda.

Lecturas acotadas a empresa/sucursal/computadora e identidad de artículo/operación. No usar `MAX(venId)` como identidad única ni escribir SQL de negocio. Los oráculos y selectores adicionales todavía deben implementarse y verificarse.

## Trazabilidad y límites

FormVenta.java:4399, preparación; :4420 reinicio y :4448 estado residual. Verificar defaults concretos al calibrar el paquete.

La [cobertura](../../docs/cobertura.md) identifica la referencia XGestion2 `release/189-lts`, `f34238183d494259bed1279dd7d9aac0ce16a3ae`. Fuente y tests orientan expectativas; no demuestran equivalencia del JAR ni ejecución real. No cubre variantes de otras configuraciones, monedas, permisos o dispositivos.
