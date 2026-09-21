---
{"id":"XG-VEN-002","title":"Cancelar venta sin persistir","product":"xgestion","module":"ventas","tags":["xgestion","regression","ventas","escritura"],"status":"implemented","test":"products/xgestion/suites/ventas.robot"}
---

# XG-VEN-002 — Cancelar venta sin persistir

## Objetivo

El vendedor abandona una operación todavía no cobrada sin registrarla como venta.

## Estado y perfil

Automatización implementada; **ejecución real pendiente** de paquete privado, calibración y aceptación. Lint y dry-run no acreditan este recorrido en el producto.

- Windows QA exclusivo, offline, escritorio desbloqueado y ejecución serial por el runner.
- Paquete autorizado, licencia QA vigente, base aislada restaurada y selectores calibrados para el SHA-256 del JAR.
- Usuario, empresa, sucursal y computadora QA definidos en el paquete; credenciales locales privadas.
- Venta local no fiscal en ARS, producto a precio final $1.000 y stock suficiente; cantidad habitual 2 y total $2.000. Efectivo; `cartelPagoVuelto=true`; abandono sin supervisor.
- Sin ofertas, descuentos, puntos, recargos, impresión, facturación ni pagos externos.

## Pasos y resultados esperados

1. Ingresar como QA y abrir Nueva venta. **Esperado:** el formulario está disponible.
2. Cargar 2 unidades del producto de $1.000. **Esperado:** total visible de $2.000 ARS.
3. Cancelar la venta y confirmar el descarte. **Esperado:** se cierra el formulario y se vuelve a la pantalla prevista.
4. Revisar el resultado automático. **Esperado:** no se creó una venta ni cambiaron stock o caja por esta operación.

## Recuperación y límites

Si falla, conservar el reporte privado y el paso observado. El runner cierra solo su proceso y prepara el baseline en la siguiente ejecución. No reparar resultados borrando datos ni modificar controles de seguridad. Abandonar una venta nueva no equivale a anular una cobrada. Puede existir auditoría de abandono sin venta. Rechazar el descarte se planifica en XG-VEN-007.

## Evidencia para QA

INFO muestra ID, resultado y resumen; DEBUG añade pasos; TRACE diagnóstico saneado. En cualquier nivel un fallo debe incluir paso, esperado, observado, categoría y evidencia disponible. Si la causa no está demostrada, informar «causa no determinada». Capturas solo de ventanas QA autenticadas, sin credenciales. Registrar versión/hash del JAR, paquete, perfil y ruta privada del reporte.

## Anexo técnico y trazabilidad

Se comparan los IDs de ventas y los valores de stock/caja anteriores y posteriores dentro del contexto fixture: deben permanecer iguales. No borrar filas ni anular documentos. Fuente: FormVenta.java:648 confirmación, :681 supervisor y :709 auditoría; contrato: assert_cancelled en products/xgestion/oracles.py.

La [cobertura](../../docs/cobertura.md) identifica la referencia XGestion2 `release/189-lts`, `f34238183d494259bed1279dd7d9aac0ce16a3ae`. Fuente y tests orientan expectativas; no demuestran equivalencia del JAR ni ejecución real. Se mantienen IDs, tags y archivo Robot existentes.
