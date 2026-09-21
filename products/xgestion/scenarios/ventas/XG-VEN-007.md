---
{"id":"XG-VEN-007","title":"Rechazar el abandono y continuar vendiendo","product":"xgestion","module":"ventas","tags":["xgestion","regression","ventas","escritura","corregir-venta"],"status":"implemented","test":"products/xgestion/suites/ventas.robot"}
---

# XG-VEN-007 — Rechazar el abandono y continuar vendiendo

## Objetivo

El vendedor evita descartar por error una venta y continúa hasta cobrarla.

## Estado

**Automatización implementada; ejecución real sobre el JAR pendiente.** El caso pertenece a la [etapa 1 — Venta cotidiana](../../docs/roadmap.md) y requiere `sales_journeys`, grilla y editor calibrados. Un `check`, dry-run o test del framework no acredita PASS sobre XGestion.

El checkout ERP incorpora una acción única de edición compartida por botón, `Ctrl+E` y doble clic. La ruta automatizada nueva sólo se activa con `ventas-teclado-v1`, después de observarla y recalibrarla para el SHA256 del JAR; los paquetes anteriores conservan temporalmente el doble clic legado. XG-ACC-001 continúa como `implementado_pendiente_validacion_jar` en el [backlog CSV](../../docs/backlog-accesibilidad.csv). No sustituir la edición por precargar cantidad antes de agregar.

## Perfil, precondiciones y datos

- Windows QA exclusivo, offline, escritorio desbloqueado y ejecución serial por el runner.
- Paquete autorizado, licencia QA vigente, base aislada restaurada y selectores calibrados para el SHA-256 del JAR.
- Usuario, empresa, sucursal y computadora QA definidos en el paquete; credenciales locales privadas.
- Venta local no fiscal en ARS, producto a precio final $1.000 y stock suficiente; cantidad habitual 2 y total $2.000. Efectivo; `cartelPagoVuelto=true`; abandono sin supervisor.
- Sin ofertas, descuentos, puntos, recargos, impresión, facturación ni pagos externos.
- Extensión `sales_journeys` y `calibration.verified_features` con `ventas-etapa1`; para la ruta nueva, sumar `ventas-teclado-v1` y comprobar editor, grilla, selección, foco y confirmaciones del [contrato privado](../../docs/paquete.md).
- Sin supervisor para abandonar. Autorizaciones de otros roles pertenecen a permisos.

## Pasos y resultados esperados

1. Preparar venta no fiscal con una unidad de $1.000. **Esperado:** cantidad 1 y total $1.000.
2. Solicitar salir de la venta con Escape o el cierre del formulario. **Esperado:** confirmación de abandono. El botón “Cerrar” del cuerpo de Venta inicia el cobro y no sirve para este paso.
3. Rechazar el abandono con “Cancelar” en la confirmación observada. **Esperado:** formulario abierto, mismo producto, cantidad y total; no se registra un cobro.
4. Con `ventas-teclado-v1`, seleccionar la línea, abrir con Editar, cancelar sin cambios y verificar el retorno; reabrir con `Ctrl+E`, editar cantidad a 2 y guardar. Sin esa feature, usar la ruta legada por doble clic. **Esperado:** se puede seguir operando, la misma línea queda seleccionada y el total pasa a $2.000.
5. Cobrar $2.000 en efectivo. **Esperado:** una sola venta cerrada, cantidad 2 y efectos de stock/caja correspondientes.

## Recuperación

Si falla, conservar el reporte privado y el paso observado. El runner cierra solo su proceso y prepara el baseline en la siguiente ejecución. No reparar resultados borrando datos ni modificar controles de seguridad. Las cancelaciones y reintentos descritos son parte del caso, no limpieza oculta. No continuar después de un fallo como si el paso hubiera aprobado.

## Evidencia para QA

INFO muestra ID, resultado y resumen; DEBUG añade pasos; TRACE diagnóstico saneado. En cualquier nivel un fallo debe incluir paso, esperado, observado, categoría y evidencia disponible. Si la causa no está demostrada, informar «causa no determinada». Capturas solo de ventanas QA autenticadas, sin credenciales. Registrar versión/hash del JAR, paquete, perfil y ruta privada del reporte.

## Anexo técnico de evidencia

Comparar estado antes/después del rechazo, incluida ausencia de venta y movimientos nuevos; cobro final con una sola venta y deltas −2/+2000. Efectivo simple: `ventas.Pagado=2000`, `Vuelto=0`, sin filas en `ventas_pagos`. Cerrar el aviso solo no demuestra que se pudo continuar.

Lecturas acotadas a empresa/sucursal/computadora e identidad de artículo/operación. No usar `MAX(venId)` como identidad única ni escribir SQL de negocio. Las consultas son de solo lectura. `sale.edit`, `editor.cancel`, la selección y el foco deben calibrarse sobre el JAR exacto antes de habilitar `ventas-teclado-v1`; la implementación no acredita ejecución real.

## Trazabilidad y límites

En el working tree sobre `d7f1946ba9520622ea7743722dc6b894b2c12eba`, `FormVenta` conserva las reglas de abandono y abre la edición mediante una acción común; `DialogConfirmacion` separa Aceptar de Cancelar/Rechazar. Calibrar rechazo y confirmación como acciones distintas.

La [cobertura](../../docs/cobertura.md) identifica la referencia XGestion2 `release/189-lts`, `f34238183d494259bed1279dd7d9aac0ce16a3ae`. Fuente y tests orientan expectativas; no demuestran equivalencia del JAR ni ejecución real. No cubre variantes de otras configuraciones, monedas, permisos o dispositivos.
