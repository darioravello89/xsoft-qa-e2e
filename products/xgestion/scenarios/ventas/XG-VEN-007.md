---
{"id":"XG-VEN-007","title":"Rechazar el abandono y continuar vendiendo","product":"xgestion","module":"ventas","tags":["xgestion","regression","ventas","escritura","corregir-venta"],"status":"implemented","test":"products/xgestion/suites/ventas.robot"}
---

# XG-VEN-007 — Rechazar el abandono y continuar vendiendo

## Objetivo

El vendedor evita descartar por error una venta y continúa hasta cobrarla.

## Estado

**Automatización implementada; ejecución real sobre el JAR pendiente.** El caso pertenece a la [etapa 1 — Venta cotidiana](../../docs/roadmap.md) y requiere `sales_journeys`, grilla y editor calibrados. Un `check`, dry-run o test del framework no acredita PASS sobre XGestion.

La apertura del editor usa el doble clic autorizado sobre la celda identificada por JAB, con su posición actual verificada; no usa coordenadas fijas. En la fuente fijada, `FormVenta.java:1748` dispara ese editor y no define un botón Editar ni un atajo propio. La mejora de accesibilidad sigue en el [backlog CSV](../../docs/backlog-accesibilidad.csv); implementarla en el ERP es una tarea distinta. No sustituir la edición por precargar cantidad antes de agregar.

## Perfil, precondiciones y datos

- Windows QA exclusivo, offline, escritorio desbloqueado y ejecución serial por el runner.
- Paquete autorizado, licencia QA vigente, base aislada restaurada y selectores calibrados para el SHA-256 del JAR.
- Usuario, empresa, sucursal y computadora QA definidos en el paquete; credenciales locales privadas.
- Venta local no fiscal en ARS, producto a precio final $1.000 y stock suficiente; cantidad habitual 2 y total $2.000. Efectivo; `cartelPagoVuelto=true`; abandono sin supervisor.
- Sin ofertas, descuentos, puntos, recargos, impresión, facturación ni pagos externos.
- Extensión `sales_journeys` y `calibration.verified_features` con `ventas-etapa1`; comprobar editor, grilla y confirmaciones del [contrato privado](../../docs/paquete.md).
- Sin supervisor para abandonar. Autorizaciones de otros roles pertenecen a permisos.

## Pasos y resultados esperados

1. Preparar venta no fiscal con una unidad de $1.000. **Esperado:** cantidad 1 y total $1.000.
2. Solicitar salir de la venta con Escape o el cierre del formulario. **Esperado:** confirmación de abandono. El botón “Cerrar” del cuerpo de Venta inicia el cobro y no sirve para este paso.
3. Rechazar el abandono con “Cancelar” en la confirmación observada. **Esperado:** formulario abierto, mismo producto, cantidad y total; no se registra un cobro.
4. Abrir la línea mediante doble clic en su celda JAB, comprobar el producto del editor, editar cantidad a 2 y guardar. **Esperado:** se puede seguir operando y el total pasa a $2.000.
5. Cobrar $2.000 en efectivo. **Esperado:** una sola venta cerrada, cantidad 2 y efectos de stock/caja correspondientes.

## Recuperación

Si falla, conservar el reporte privado y el paso observado. El runner cierra solo su proceso y prepara el baseline en la siguiente ejecución. No reparar resultados borrando datos ni modificar controles de seguridad. Las cancelaciones y reintentos descritos son parte del caso, no limpieza oculta. No continuar después de un fallo como si el paso hubiera aprobado.

## Evidencia para QA

INFO muestra ID, resultado y resumen; DEBUG añade pasos; TRACE diagnóstico saneado. En cualquier nivel un fallo debe incluir paso, esperado, observado, categoría y evidencia disponible. Si la causa no está demostrada, informar «causa no determinada». Capturas solo de ventanas QA autenticadas, sin credenciales. Registrar versión/hash del JAR, paquete, perfil y ruta privada del reporte.

## Anexo técnico de evidencia

Comparar estado antes/después del rechazo, incluida ausencia de venta y movimientos nuevos; cobro final con una sola venta y deltas −2/+2000. Efectivo simple: `ventas.Pagado=2000`, `Vuelto=0`, sin filas en `ventas_pagos`. Cerrar el aviso solo no demuestra que se pudo continuar.

Lecturas acotadas a empresa/sucursal/computadora e identidad de artículo/operación. No usar `MAX(venId)` como identidad única ni escribir SQL de negocio. Las consultas son de solo lectura. Los selectores y el doble clic sobre la celda deben calibrarse sobre el JAR; la implementación no acredita ejecución real.

## Trazabilidad y límites

En el commit de referencia: `FormVenta.java:648` confirma, `:681` exige supervisor según configuración y `:1748` abre edición por doble clic. `src/Utilidades/Componentes/DialogConfirmacion.java:44` titula la ventana “Confirmar”; “Confirmar salida” es el texto del encabezado y los botones son “Aceptar”/“Cancelar”. Calibrar rechazo y confirmación como acciones distintas.

La [cobertura](../../docs/cobertura.md) identifica la referencia XGestion2 `release/189-lts`, `f34238183d494259bed1279dd7d9aac0ce16a3ae`. Fuente y tests orientan expectativas; no demuestran equivalencia del JAR ni ejecución real. No cubre variantes de otras configuraciones, monedas, permisos o dispositivos.
