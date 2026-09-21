# Continuación del roadmap: Venta cotidiana

## Objetivo y alcance

Implementar los siete recorridos pendientes de la etapa 1 por acciones visibles del vendedor, conservando los IDs XG-VEN-003 a XG-VEN-009: editar cantidad, código inexistente, vuelto, cancelar/retomar cobro, rechazar abandono y operación siguiente después de cobrar o abandonar.

El usuario autorizó para VEN-003/007 el doble clic sobre la celda identificada por JAB, usando su posición actual y verificando proceso/producto, sin coordenadas fijas. Esta excepción permite abrir el editor, único disparador encontrado en la grilla; las aserciones siguen siendo semánticas. Registrar en `products/xgestion/docs/backlog-accesibilidad.csv` la mejora pendiente de acceso por teclado y sus criterios de cierre.

La fuente de comportamiento es XGestion2 `f34238183d494259bed1279dd7d9aac0ce16a3ae`, consultada sin modificar el ERP. No demuestra equivalencia de un JAR ni localizadores JAB. Las fichas se marcan `implemented` cuando existe automatización completa; la validación real continúa pendiente del laboratorio.

## Contratos observados

- Venta local no fiscal 99, ARS, artículo stockeable normal a 1000, sin promociones/beneficios, cantidades 1 y 2. Diálogo de cobro habilitado y abandono sin supervisor.
- El efectivo simple conserva `Pagado`/`Vuelto` en `ventas`; genera un movimiento de caja por el total aplicado y no filas en `ventas_pagos`. Recibido 3000 y vuelto 1000 no cambian el total 2000.
- Cancelar cobro vuelve a la venta sin persistir. Rechazar abandono corresponde al botón Cancelar de la confirmación, distinto de cancelar el cobro.
- El cobro exitoso reinicia la venta en la misma ventana. Hay que observar ese reinicio antes de cargar otra operación; abrir una ventana nueva ocultaría un fallo de limpieza.
- El código inexistente tiene aviso sonoro/textual o diálogo según configuración. La calibración declara cuál y el texto observable.
- Los defaults de cliente, lista y comprobante dependen del perfil; no se presumen vacíos ni comprobante 99. Después de observarlos se selecciona explícitamente 99.
- Cantidad de grilla y diálogo de cobro usan punto decimal sin agrupación; los importes de la grilla usan formato ARS argentino. No intercambiar parsers entre controles.

## Implementación por incrementos

1. Corregir y ampliar oráculos de solo lectura: identidad completa, recibido/vuelto, pago simple y movimientos individuales; snapshots para estados intermedios y conservación de la primera venta.
2. Leer la grilla completa por JAB y verificar dimensiones. Una grilla inaccesible/incompleta bloquea; no sustituirla por comprobar solamente el total.
3. Añadir una extensión privada `sales_journeys` y aliases observados. Los paquetes anteriores conservan los siete casos iniciales; los nuevos bloquean antes de iniciar el JAR si falta la extensión/calibración.
4. Implementar recorridos y comprobaciones de UI, persistencia intermedia y recuperación. Cada caso mantiene su propio proceso; las dos operaciones de VEN-008/009 comparten ese proceso y su referencia inicial.
5. Actualizar fichas implementadas, documentación, conteos y Excel. No convertir la etapa completa en aceptada por un dry-run.

Archivos: `products/xgestion/{contracts,driver,library,oracles}.py`, ejemplos privados, `suites/ventas.robot`, fichas y documentación. Tests de contratos/adaptador/oráculos en `tests/`. No añadir dependencias, cambiar bases externas ni ejecutar SQL de negocio.

## Aceptación técnica

Tests sintéticos prueban UI incorrecta, grilla incompleta, cancelación con mutación, doble cobro, estado residual y evidencia parcial. Deben comprobar el resultado observado y rechazar discrepancias. No autorizan a marcar selectores privados como verificados.

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m robocop check products
.\.venv\Scripts\python.exe -m pytest
.\qa.cmd check
.\qa.cmd run --product xgestion --group regression --dry-run
.\qa.cmd coverage
.\qa.cmd coverage --check
```

La aceptación E2E exige Windows QA aislado/offline, paquete autorizado y controles verificados sobre el SHA-256 del JAR. Registrar por separado estos resultados y los controles técnicos. No usar producción, invocar métodos Java de negocio ni publicar datos privados.

## Comprobación de esta implementación (2026-09-21)

- 419 tests del framework aprobados; 34 omitidos (integraciones MySQL opt-in y un requisito de symlinks del sistema).
- Ruff, Robocop, catálogo y vigencia del mapa de cobertura aprobados.
- Dry-run de los 14 casos aprobado, incluidos los siete recorridos nuevos. No inicia el JAR ni acredita resultados del producto.
- Excel regenerado desde las fichas y revisado visualmente. Backlog CSV con XG-ACC-001, mejora pendiente para abrir el editor por teclado.
- No se ejecutó el paquete privado, la base real del ERP ni el JAR. La calibración y la aceptación E2E quedan pendientes.
