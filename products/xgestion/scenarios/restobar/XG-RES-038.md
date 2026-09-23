---
{"id":"XG-RES-038","title":"Calcular descuentos globales sobre los consumos ya descontados","product":"xgestion","module":"restobar","tags":["xgestion","regression","restobar","descuentos","precios","cobros"],"status":"planned"}
---

# XG-RES-038 — Calcular descuentos globales sobre los consumos ya descontados

## Objetivo

Calcular descuentos globales sobre los consumos ya descontados, desde la perspectiva del mozo, cajero o supervisor que opera el pedido.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P1; etapa 5.**
Referencia de planificación: **Importes**. Ver [mapa de Restobar](../../docs/restobar.md).
No tiene suite Robot, seed automático ni validación real del JAR. Los resultados siguientes son criterios esperados, no resultados obtenidos.

## Precondiciones y datos

- Paquete QA sintético, Windows exclusivo y escritorio visible. La preparación de carta, mesas, ingredientes, permisos y perfiles de este caso está **pendiente**; `catalogo-comercial-v1` no certifica estos datos.
- Perfil local por defecto: ARS, comprobante interno no fiscal, impuestos y cubiertos $0 salvo indicación, sin ofertas, listas ni beneficios adicionales. Las integraciones se habilitan solo en el laboratorio indicado.
- Canasta bruta $1.500, descuento de artículos $1.000, base restante $500. Perfil A cliente 10% y pago sin descuento; B pago 10% y cliente sin descuento. Sin promociones superpuestas.
- Seed para descuento de artículos y globales pendiente; no reciclar expectativas del mismo motor.
- Preparar y registrar antes de ejecutar los IDs propios de empresa, sucursal, puesto, cuenta, mesa y productos. Mantener una operación de control ajena al caso para verificar aislamiento.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Cargar la canasta y verificar descuentos de sus artículos. | Bruto $1.500, descuento de artículos $1.000, base $500. |
| En perfil A elegir el cliente del 10%. | Descuento global $50 y total $450; no se aplica 10% al bruto ya descontado. |
| Restaurar perfil B y elegir el medio manual del 10%. | Mismo descuento por pago $50 y total $450, sin duplicar el del cliente. |
| Cancelar el cobro, retomarlo y confirmar. | Total $450 estable y una sola operación; guardar/reabrir no acumula otro $50. |

## Variantes y límites

Quitar/cambiar cliente o pago y comparar recálculo; combinación simultánea cliente+pago requiere fórmula acordada y no se infiere de las dos variantes aisladas. Promociones exhaustivas siguen en PRM.

## Dependencias para automatizar

Preparar el baseline privado reproducible y sus datos, declarar el perfil, calibrar acciones accesibles sobre el SHA256 del JAR y construir comprobaciones por identidad. Utilizar atajos/acciones accesibles verificados; no tomar una posición de pantalla como identidad. Si el control o laboratorio no está disponible, mantener el caso pendiente y explicar el bloqueo.

## Evidencia y límites

Conservar UI y valores esperados/observados de cada transición. En una cuenta abierta distinguir lo guardado de lo cobrado: salir de la pantalla no es abandonar la venta. Registrar por separado **estado de cuenta, ocupación de mesa y estado de cocina** cuando apliquen.

Comparar operaciones, consumos, opciones, importes y efectos de stock/pagos por identidad y deltas según el caso, con lecturas autorizadas y saneadas. Las salidas de cocina, fiscalización y dispositivos requieren evidencia del extremo receptor; un log o test unitario no la sustituye. Registrar versión/SHA256 del JAR, commit del harness, paquete, perfil, IDs y reporte privado.

## Recuperación

Ante una discrepancia conservar primero la evidencia y cancelar o retomar por la interfaz según los pasos del caso. No borrar ni corregir registros comerciales para obtener un resultado aprobado. Restaurar el baseline QA antes de otra variante; para un cierre de resultado ambiguo conciliar la operación antes de reintentar, evitando cobrar o consumir ingredientes dos veces.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas relativas a XGestion2:

- `src/ModuloRestobar/Vistas/formTicket.java`
- `test/ModuloRestobar/Vistas/FormTicketDescuentosGlobalesTest.java`
- `src/ModuloVentas/Entidades/VentaTotalesCalculador.java`

La lectura de fuente/tests orienta el riesgo y el criterio; no acredita la ejecución del artefacto. INFO resume, DEBUG describe acciones de negocio y TRACE añade diagnóstico saneado. Un fallo conserva paso, esperado, observado, categoría y evidencia; causa no determinada si falta prueba causal. No registrar credenciales, filas completas ni configuración privada.

