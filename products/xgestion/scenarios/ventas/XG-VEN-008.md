---
{"id":"XG-VEN-008","title":"Comenzar otra venta después de cobrar","product":"xgestion","module":"ventas","tags":["xgestion","regression","ventas","escritura"],"status":"implemented","test":"products/xgestion/suites/ventas.robot"}
---

# XG-VEN-008 — Comenzar otra venta después de cobrar

## Objetivo

El vendedor atiende al siguiente cliente sin arrastrar datos de la venta anterior.

## Estado

**Automatización implementada; ejecución real sobre el JAR pendiente.** El caso pertenece a la [etapa 1 — Venta cotidiana](../../docs/roadmap.md) y requiere la extensión privada `sales_journeys` y su mapa calibrado. Un `check`, dry-run o test del framework no acredita PASS sobre XGestion.

## Perfil, precondiciones y datos

- Windows QA exclusivo, offline, escritorio desbloqueado y ejecución serial por el runner.
- Paquete autorizado, licencia QA vigente, base aislada restaurada y selectores calibrados para el SHA-256 del JAR.
- Usuario, empresa, sucursal y computadora QA definidos en el paquete; credenciales locales privadas.
- Venta local no fiscal en ARS, producto a precio final $1.000 y stock suficiente; cantidad habitual 2 y total $2.000. Efectivo; `cartelPagoVuelto=true`; abandono sin supervisor.
- Sin ofertas, descuentos, puntos, recargos, impresión, facturación ni pagos externos.
- Perfil `ventas-etapa1`: extensión `sales_journeys` completa, columnas de la grilla observadas y defaults de cliente/lista/comprobante documentados. Ver [contrato privado](../../docs/paquete.md).
- Mantener la misma sesión de aplicación. Dos tests que reinician el JAR no prueban este recorrido. No exigir blancos si existe un default legítimo del perfil.

## Pasos y resultados esperados

1. Preparar venta no fiscal de 2 unidades por $2.000 y cobrar en efectivo. **Esperado:** se completa una sola venta.
2. Observar el reinicio automático de la **misma ventana de Venta**, sin abrir otra desde el menú ni reiniciar XGestion. **Esperado:** grilla vacía, cantidad inicial 1, total cero y defaults de cliente/lista/comprobante iguales al perfil QA; no arrastra la operación cobrada.
3. Cargar una unidad del mismo producto. **Esperado:** una unidad y total $1.000, sin acumulación anterior.
4. Abandonar la segunda operación confirmando. **Esperado:** solo permanece la primera venta cobrada.
5. Revisar evidencia. **Esperado:** stock/caja reflejan únicamente la primera venta de 2 unidades por $2.000.

## Recuperación

Si falla, conservar el reporte privado y el paso observado. El runner cierra solo su proceso y prepara el baseline en la siguiente ejecución. No reparar resultados borrando datos ni modificar controles de seguridad. Las cancelaciones y reintentos descritos son parte del caso, no limpieza oculta. No continuar después de un fallo como si el paso hubiera aprobado.

## Evidencia para QA

INFO muestra ID, resultado y resumen; DEBUG añade pasos; TRACE diagnóstico saneado. En cualquier nivel un fallo debe incluir paso, esperado, observado, categoría y evidencia disponible. Si la causa no está demostrada, informar «causa no determinada». Capturas solo de ventanas QA autenticadas, sin credenciales. Registrar versión/hash del JAR, paquete, perfil y ruta privada del reporte.

## Anexo técnico de evidencia

Referencia inicial y posterior al primer cobro, usando el mismo PID y la misma ventana de Venta. Tras abandonar la segunda: mismos IDs/stock/caja que después del primer cobro; una venta total y deltas globales −2/+2000. Evidencia UI del reinicio automático y de la segunda carga. El cobro inicial es efectivo simple (`Pagado=2000`, `Vuelto=0`, sin `ventas_pagos`); abandonar la segunda puede registrar auditoría, pero no otra venta ni movimientos.

Lecturas acotadas a empresa/sucursal/computadora e identidad de artículo/operación. No usar `MAX(venId)` como identidad única ni escribir SQL de negocio. Las consultas son de solo lectura. Los selectores y columnas deben verificarse sobre el JAR; la implementación del oráculo no acredita ejecución real.

## Trazabilidad y límites

En el commit de referencia: `src/ModuloVentas/Vistas/FormVenta.java:6188` llama a `reiniciarVentaNueva` después del commit; `:4399` prepara el ticket y `:4492` carga defaults, incluida cantidad 1. `:4532` elige comprobante según configuración: no asumir que 99 siempre se conserva. Verificar `sales_journeys.defaults` al calibrar el paquete.

La [cobertura](../../docs/cobertura.md) identifica la referencia XGestion2 `release/189-lts`, `f34238183d494259bed1279dd7d9aac0ce16a3ae`. Fuente y tests orientan expectativas; no demuestran equivalencia del JAR ni ejecución real. No cubre variantes de otras configuraciones, monedas, permisos o dispositivos.
