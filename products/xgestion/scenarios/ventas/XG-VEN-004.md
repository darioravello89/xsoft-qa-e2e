---
{"id":"XG-VEN-004","title":"Buscar un código inexistente sin alterar la venta","product":"xgestion","module":"ventas","tags":["xgestion","regression","ventas","escritura","carga-productos"],"status":"implemented","test":"products/xgestion/suites/ventas.robot"}
---

# XG-VEN-004 — Buscar un código inexistente sin alterar la venta

## Objetivo

El vendedor recibe un aviso por un código incorrecto y continúa sin perder lo ya cargado.

## Estado

**Automatización implementada; ejecución real sobre el JAR pendiente.** El caso pertenece a la [etapa 1 — Venta cotidiana](../../docs/roadmap.md) y requiere la extensión privada `sales_journeys` y su mapa calibrado. Un `check`, dry-run o test del framework no acredita PASS sobre XGestion.

## Perfil, precondiciones y datos

- Windows QA exclusivo, offline, escritorio desbloqueado y ejecución serial por el runner.
- Paquete autorizado, licencia QA vigente, base aislada restaurada y selectores calibrados para el SHA-256 del JAR.
- Usuario, empresa, sucursal y computadora QA definidos en el paquete; credenciales locales privadas.
- Venta local no fiscal en ARS, producto a precio final $1.000 y stock suficiente; cantidad habitual 2 y total $2.000. Efectivo; `cartelPagoVuelto=true`; abandono sin supervisor.
- Sin ofertas, descuentos, puntos, recargos, impresión, facturación ni pagos externos.
- Perfil `ventas-etapa1`: extensión `sales_journeys` completa, columnas de la grilla observadas y defaults de cliente/lista/comprobante documentados. Ver [contrato privado](../../docs/paquete.md).
- El código ausente está garantizado por el baseline. Esta búsqueda sucede dentro de la venta, no en el listado de XG-PRO-002.

## Pasos y resultados esperados

1. Abrir venta no fiscal y cargar una unidad del producto de $1.000. **Esperado:** una línea, cantidad 1 y total $1.000.
2. Ingresar el código inexistente en la entrada de productos de la venta. **Esperado:** aparece el texto exacto calibrado en `unknown_notice_text`, como estado (`unknown_notice: status`) o diálogo (`dialog`); no se agrega una línea. El sonido por sí solo no acredita el aviso.
3. Cerrar el aviso solamente si el perfil declara diálogo, y revisar la venta. **Esperado:** mismo producto, cantidad 1 y total $1.000.
4. Ingresar de nuevo el código válido con cantidad 1. **Esperado:** dos unidades en total, sin línea del código ausente, y total $2.000. La grilla tiene exactamente las 1 o 2 líneas declaradas en `repeated_product_rows`, con dos unidades válidas en total.
5. Abandonar confirmando descarte. **Esperado:** ninguna venta registrada ni cambios de stock/caja.

## Recuperación

Si falla, conservar el reporte privado y el paso observado. El runner cierra solo su proceso y prepara el baseline en la siguiente ejecución. No reparar resultados borrando datos ni modificar controles de seguridad. Las cancelaciones y reintentos descritos son parte del caso, no limpieza oculta. No continuar después de un fallo como si el paso hubiera aprobado.

## Evidencia para QA

INFO muestra ID, resultado y resumen; DEBUG añade pasos; TRACE diagnóstico saneado. En cualquier nivel un fallo debe incluir paso, esperado, observado, categoría y evidencia disponible. Si la causa no está demostrada, informar «causa no determinada». Capturas solo de ventanas QA autenticadas, sin credenciales. Registrar versión/hash del JAR, paquete, perfil y ruta privada del reporte.

## Anexo técnico de evidencia

Mismos IDs de ventas, stock y caja al finalizar; la auditoría de abandono puede existir. Verificar en UI ausencia del código fallido y cantidad total del artículo válido; no inferir un mensaje desde nombres Java.

Lecturas acotadas a empresa/sucursal/computadora e identidad de artículo/operación. No usar `MAX(venId)` como identidad única ni escribir SQL de negocio. Las consultas son de solo lectura. Los selectores y columnas deben verificarse sobre el JAR; la implementación del oráculo no acredita ejecución real.

## Trazabilidad y límites

En el commit de referencia: `src/ModuloVentas/Vistas/FormVenta.java:3430` centraliza sonido/diálogo; `:3640` rechaza el código, limpia su entrada y muestra `Codigo inexistente.` sin agregar producto. `src/ModuloPrincipal/Entidades/Config.java:85` declara `venta.avisarProductoInexistentePorSonido`, cuyo default es true. Texto, acceso y recuperación de foco se confirman en el JAR.

La [cobertura](../../docs/cobertura.md) identifica la referencia XGestion2 `release/189-lts`, `f34238183d494259bed1279dd7d9aac0ce16a3ae`. Fuente y tests orientan expectativas; no demuestran equivalencia del JAR ni ejecución real. No cubre variantes de otras configuraciones, monedas, permisos o dispositivos.
