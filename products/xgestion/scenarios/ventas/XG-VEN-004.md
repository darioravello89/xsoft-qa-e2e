---
{"id":"XG-VEN-004","title":"Buscar un código inexistente sin alterar la venta","product":"xgestion","module":"ventas","tags":["xgestion","regression","ventas","escritura","carga-productos"],"status":"planned"}
---

# XG-VEN-004 — Buscar un código inexistente sin alterar la venta

## Objetivo

El vendedor recibe un aviso por un código incorrecto y continúa sin perder lo ya cargado.

## Estado

**Planificado: no hay prueba Robot de este caso.** La ficha define el recorrido a implementar y calibrar. Listarlo o validarlo con `qa.cmd check` no lo ejecuta ni acredita PASS. Pertenece a la [etapa 1 — Venta cotidiana](../../docs/roadmap.md).

## Perfil, precondiciones y datos

- Windows QA exclusivo, offline, escritorio desbloqueado y ejecución serial por el runner.
- Paquete autorizado, licencia QA vigente, base aislada restaurada y selectores calibrados para el SHA-256 del JAR.
- Usuario, empresa, sucursal y computadora QA definidos en el paquete; credenciales locales privadas.
- Venta local no fiscal en ARS, producto a precio final $1.000 y stock suficiente; cantidad habitual 2 y total $2.000. Efectivo; `cartelPagoVuelto=true`; abandono sin supervisor.
- Sin ofertas, descuentos, puntos, recargos, impresión, facturación ni pagos externos.
- El código ausente está garantizado por el baseline. Esta búsqueda sucede dentro de la venta, no en el listado de XG-PRO-002.

## Pasos y resultados esperados

1. Abrir venta no fiscal y cargar una unidad del producto de $1.000. **Esperado:** una línea, cantidad 1 y total $1.000.
2. Ingresar el código inexistente en la entrada de productos de la venta. **Esperado:** aviso de producto no encontrado; no se agrega una línea.
3. Cerrar el aviso, si corresponde, y revisar la venta. **Esperado:** mismo producto, cantidad 1 y total $1.000.
4. Ingresar de nuevo el código válido con cantidad 1. **Esperado:** dos unidades en total, sin línea del código ausente, y total $2.000. La presentación de líneas debe respetar la consolidación configurada y documentada al calibrar.
5. Abandonar confirmando descarte. **Esperado:** ninguna venta registrada ni cambios de stock/caja.

## Recuperación

Si falla, conservar el reporte privado y el paso observado. El runner cierra solo su proceso y prepara el baseline en la siguiente ejecución. No reparar resultados borrando datos ni modificar controles de seguridad. Las cancelaciones y reintentos descritos son parte del caso, no limpieza oculta. No continuar después de un fallo como si el paso hubiera aprobado.

## Evidencia para QA

INFO muestra ID, resultado y resumen; DEBUG añade pasos; TRACE diagnóstico saneado. En cualquier nivel un fallo debe incluir paso, esperado, observado, categoría y evidencia disponible. Si la causa no está demostrada, informar «causa no determinada». Capturas solo de ventanas QA autenticadas, sin credenciales. Registrar versión/hash del JAR, paquete, perfil y ruta privada del reporte.

## Anexo técnico de evidencia

Mismos IDs de ventas, stock y caja al finalizar. Verificar en UI ausencia del código fallido y cantidad total del artículo válido; no inferir un mensaje desde nombres Java.

Lecturas acotadas a empresa/sucursal/computadora e identidad de artículo/operación. No usar `MAX(venId)` como identidad única ni escribir SQL de negocio. Los oráculos y selectores adicionales todavía deben implementarse y verificarse.

## Trazabilidad y límites

FormVenta.java:3430, aviso de producto inexistente y carga posterior; políticas de cantidad previa y consolidación. Texto y recuperación de foco se confirman en el JAR.

La [cobertura](../../docs/cobertura.md) identifica la referencia XGestion2 `release/189-lts`, `f34238183d494259bed1279dd7d9aac0ce16a3ae`. Fuente y tests orientan expectativas; no demuestran equivalencia del JAR ni ejecución real. No cubre variantes de otras configuraciones, monedas, permisos o dispositivos.
