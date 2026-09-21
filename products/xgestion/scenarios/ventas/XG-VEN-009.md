---
{"id":"XG-VEN-009","title":"Comenzar otra venta después de abandonar","product":"xgestion","module":"ventas","tags":["xgestion","regression","ventas","escritura"],"status":"implemented","test":"products/xgestion/suites/ventas.robot"}
---

# XG-VEN-009 — Comenzar otra venta después de abandonar

## Objetivo

El vendedor descarta una operación y empieza otra sin recuperar productos o importes abandonados.

## Estado

**Automatización implementada; ejecución real sobre el JAR pendiente.** El caso pertenece a la [etapa 1 — Venta cotidiana](../../docs/roadmap.md) y requiere la extensión privada `sales_journeys` y su mapa calibrado. Un `check`, dry-run o test del framework no acredita PASS sobre XGestion.

## Perfil, precondiciones y datos

- Windows QA exclusivo, offline, escritorio desbloqueado y ejecución serial por el runner.
- Paquete autorizado, licencia QA vigente, base aislada restaurada y selectores calibrados para el SHA-256 del JAR.
- Usuario, empresa, sucursal y computadora QA definidos en el paquete; credenciales locales privadas.
- Venta local no fiscal en ARS, producto a precio final $1.000 y stock suficiente; cantidad habitual 2 y total $2.000. Efectivo; `cartelPagoVuelto=true`; abandono sin supervisor.
- Sin ofertas, descuentos, puntos, recargos, impresión, facturación ni pagos externos.
- Perfil `ventas-etapa1`: extensión `sales_journeys` completa, columnas de la grilla observadas y defaults de cliente/lista/comprobante documentados. Ver [contrato privado](../../docs/paquete.md).
- Recorrido continuo en el mismo proceso. Puede haber auditoría de abandono; no equivale a venta persistida y no debe eliminarse.

## Pasos y resultados esperados

1. Preparar venta no fiscal de 2 unidades por $2.000. **Esperado:** líneas y total correctos, sin cobrar.
2. Solicitar salir de la venta y aceptar el descarte. **Esperado:** cierra el formulario sin registrar una venta. La confirmación observada distingue “Aceptar” de “Cancelar”.
3. Abrir otra venta sin reiniciar XGestion. **Esperado:** grilla vacía, cantidad inicial 1, total cero y defaults exactos de cliente/lista/comprobante; no arrastra datos de la abandonada.
4. Cargar una unidad del producto. **Esperado:** una unidad y total $1.000; no reaparece la cantidad 2.
5. Abandonar también la segunda. **Esperado:** ninguna venta creada ni cambios de stock/caja.

## Recuperación

Si falla, conservar el reporte privado y el paso observado. El runner cierra solo su proceso y prepara el baseline en la siguiente ejecución. No reparar resultados borrando datos ni modificar controles de seguridad. Las cancelaciones y reintentos descritos son parte del caso, no limpieza oculta. No continuar después de un fallo como si el paso hubiera aprobado.

## Evidencia para QA

INFO muestra ID, resultado y resumen; DEBUG añade pasos; TRACE diagnóstico saneado. En cualquier nivel un fallo debe incluir paso, esperado, observado, categoría y evidencia disponible. Si la causa no está demostrada, informar «causa no determinada». Capturas solo de ventanas QA autenticadas, sin credenciales. Registrar versión/hash del JAR, paquete, perfil y ruta privada del reporte.

## Anexo técnico de evidencia

Comparar ambas cancelaciones con referencia inicial: mismos IDs de ventas, stock y caja. La auditoría de abandono puede registrar las operaciones; no se exige ausencia de cualquier escritura en la base. Evidencia UI de la segunda operación para demostrar limpieza del formulario.

Lecturas acotadas a empresa/sucursal/computadora e identidad de artículo/operación. No usar `MAX(venId)` como identidad única ni escribir SQL de negocio. Las consultas son de solo lectura. Los selectores y columnas deben verificarse sobre el JAR; la implementación del oráculo no acredita ejecución real.

## Trazabilidad y límites

En el commit de referencia: `src/ModuloVentas/Vistas/FormVenta.java:648` confirma abandono, `:709` registra auditoría y `:4492` prepara defaults. `src/Utilidades/Componentes/DialogConfirmacion.java:44` usa título “Confirmar” y botones “Aceptar”/“Cancelar” (`:68`/`:82`). `src/ModuloPrincipal/Vistas/AppXGestion.java:4565` exige turno abierto al abrir “Nueva venta”.

La [cobertura](../../docs/cobertura.md) identifica la referencia XGestion2 `release/189-lts`, `f34238183d494259bed1279dd7d9aac0ce16a3ae`. Fuente y tests orientan expectativas; no demuestran equivalencia del JAR ni ejecución real. No cubre variantes de otras configuraciones, monedas, permisos o dispositivos.
