---
{"id":"XG-PRO-001","title":"Buscar producto conocido","product":"xgestion","module":"productos","tags":["xgestion","smoke","regression","productos","lectura"],"status":"implemented","test":"products/xgestion/suites/smoke.robot"}
---

# XG-PRO-001 — Buscar producto conocido

## Objetivo

El usuario encuentra un producto por su código en el listado.

## Estado y perfil

Automatización implementada; **ejecución real pendiente** de paquete privado, calibración y aceptación. Lint y dry-run no acreditan este recorrido en el producto.

- Windows QA exclusivo, offline, escritorio desbloqueado y ejecución serial por el runner.
- Paquete autorizado, licencia QA vigente, base aislada restaurada y selectores calibrados para el SHA-256 del JAR.
- Usuario, empresa, sucursal y computadora QA definidos en el paquete; credenciales locales privadas.
- Datos de consulta y código ausente conocidos, preparados en el paquete saneado.

## Pasos y resultados esperados

1. Ingresar como QA y abrir Productos → Listado de Productos. **Esperado:** está disponible la búsqueda.
2. Buscar el código conocido del entorno. **Esperado:** aparece el producto con el nombre exacto definido para ese código.

## Recuperación y límites

Si falla, conservar el reporte privado y el paso observado. El runner cierra solo su proceso y prepara el baseline en la siguiente ejecución. No reparar resultados borrando datos ni modificar controles de seguridad. La consulta no agrega un producto a una venta, no edita su ficha ni valida precio/stock.

## Evidencia para QA

INFO muestra ID, resultado y resumen; DEBUG añade pasos; TRACE diagnóstico saneado. En cualquier nivel un fallo debe incluir paso, esperado, observado, categoría y evidencia disponible. Si la causa no está demostrada, informar «causa no determinada». Capturas solo de ventanas QA autenticadas, sin credenciales. Registrar versión/hash del JAR, paquete, perfil y ruta privada del reporte.

## Anexo técnico y trazabilidad

Se contrasta código/nombre con fixtures.product y un control de resultado calibrado. La carga en venta se planifica por separado en XG-VEN-003.

La [cobertura](../../docs/cobertura.md) identifica la referencia XGestion2 `release/189-lts`, `f34238183d494259bed1279dd7d9aac0ce16a3ae`. Fuente y tests orientan expectativas; no demuestran equivalencia del JAR ni ejecución real. Se mantienen IDs, tags y archivo Robot existentes.
