---
{"id":"XG-VEN-007","title":"Rechazar el abandono y continuar vendiendo","product":"xgestion","module":"ventas","tags":["xgestion","regression","ventas","escritura","corregir-venta"],"status":"planned"}
---

# XG-VEN-007 — Rechazar el abandono y continuar vendiendo

## Objetivo

El vendedor evita descartar por error una venta y continúa hasta cobrarla.

## Estado

**Planificado: no hay prueba Robot de este caso.** La ficha define el recorrido a implementar y calibrar. Listarlo o validarlo con `qa.cmd check` no lo ejecuta ni acredita PASS. Pertenece a la [etapa 1 — Venta cotidiana](../../docs/roadmap.md).

## Perfil, precondiciones y datos

- Windows QA exclusivo, offline, escritorio desbloqueado y ejecución serial por el runner.
- Paquete autorizado, licencia QA vigente, base aislada restaurada y selectores calibrados para el SHA-256 del JAR.
- Usuario, empresa, sucursal y computadora QA definidos en el paquete; credenciales locales privadas.
- Venta local no fiscal en ARS, producto a precio final $1.000 y stock suficiente; cantidad habitual 2 y total $2.000. Efectivo; `cartelPagoVuelto=true`; abandono sin supervisor.
- Sin ofertas, descuentos, puntos, recargos, impresión, facturación ni pagos externos.
- Sin supervisor para abandonar. Autorizaciones de otros roles pertenecen a permisos.

## Pasos y resultados esperados

1. Preparar venta no fiscal con una unidad de $1.000. **Esperado:** cantidad 1 y total $1.000.
2. Intentar cerrar o cancelar la venta. **Esperado:** confirmación de abandono.
3. Elegir no abandonar. **Esperado:** formulario abierto, mismo producto, cantidad y total; no se registra un cobro.
4. Editar cantidad a 2. **Esperado:** se puede seguir operando y el total pasa a $2.000.
5. Cobrar $2.000 en efectivo. **Esperado:** una sola venta cerrada, cantidad 2 y efectos de stock/caja correspondientes.

## Recuperación

Si falla, conservar el reporte privado y el paso observado. El runner cierra solo su proceso y prepara el baseline en la siguiente ejecución. No reparar resultados borrando datos ni modificar controles de seguridad. Las cancelaciones y reintentos descritos son parte del caso, no limpieza oculta. No continuar después de un fallo como si el paso hubiera aprobado.

## Evidencia para QA

INFO muestra ID, resultado y resumen; DEBUG añade pasos; TRACE diagnóstico saneado. En cualquier nivel un fallo debe incluir paso, esperado, observado, categoría y evidencia disponible. Si la causa no está demostrada, informar «causa no determinada». Capturas solo de ventanas QA autenticadas, sin credenciales. Registrar versión/hash del JAR, paquete, perfil y ruta privada del reporte.

## Anexo técnico de evidencia

Comparar estado antes/después del rechazo; cobro final con una sola venta y deltas −2/+2000. Cerrar el aviso solo no demuestra que se pudo continuar.

Lecturas acotadas a empresa/sucursal/computadora e identidad de artículo/operación. No usar `MAX(venId)` como identidad única ni escribir SQL de negocio. Los oráculos y selectores adicionales todavía deben implementarse y verificarse.

## Trazabilidad y límites

FormVenta.java:648, confirmación y :681 supervisor; edición y cierre. Calibrar rechazo y confirmación del aviso como acciones distintas.

La [cobertura](../../docs/cobertura.md) identifica la referencia XGestion2 `release/189-lts`, `f34238183d494259bed1279dd7d9aac0ce16a3ae`. Fuente y tests orientan expectativas; no demuestran equivalencia del JAR ni ejecución real. No cubre variantes de otras configuraciones, monedas, permisos o dispositivos.
