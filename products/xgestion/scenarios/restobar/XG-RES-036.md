---
{"id":"XG-RES-036","title":"Cargar un producto pesable y recuperarse de una lectura fallida","product":"xgestion","module":"restobar","tags":["xgestion","regression","restobar","dispositivos","mesas","recuperacion"],"status":"planned"}
---

# XG-RES-036 — Cargar un producto pesable y recuperarse de una lectura fallida

## Objetivo

Cargar un producto pesable y recuperarse de una lectura fallida, desde la perspectiva del mozo, cajero o supervisor que opera el pedido.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P1; etapa 5 con dependencia de laboratorio de etapa 6.**
Referencia de planificación: **R06**. Ver [mapa de Restobar](../../docs/restobar.md).
No tiene suite Robot, seed automático ni validación real del JAR. Los resultados siguientes son criterios esperados, no resultados obtenidos.

## Precondiciones y datos

- Paquete QA sintético, Windows exclusivo y escritorio visible. La preparación de carta, mesas, ingredientes, permisos y perfiles de este caso está **pendiente**; `catalogo-comercial-v1` no certifica estos datos.
- Perfil local por defecto: ARS, comprobante interno no fiscal, impuestos y cubiertos $0 salvo indicación, sin ofertas, listas ni beneficios adicionales. Las integraciones se habilitan solo en el laboratorio indicado.
- Producto QA-PESO a $4.000/kg, balanza QA calibrada con 0,250 kg; producto de control $500. Perfil y unidad declarados.
- Balanza física y protocolo de lectura; ingreso decimal manual no acredita el dispositivo.
- Preparar y registrar antes de ejecutar los IDs propios de empresa, sucursal, puesto, cuenta, mesa y productos. Mantener una operación de control ajena al caso para verificar aislamiento.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Leer 0,250 kg y cargar el producto. | Se agrega 0,250 kg por $1.000. |
| Interrumpir la balanza antes de la siguiente carga. | Se informa falta de lectura; no se agrega cantidad vieja, cero inventado ni un kilogramo por defecto. |
| Recuperar el dispositivo y leer 0,500 kg. | La nueva carga corresponde a 0,500 kg y $2.000, sin repetir la fallida. |
| Revisar los renglones y cancelar una edición de cantidad. | Se conserva el peso confirmado y el total esperado. |

## Variantes y límites

Lectura nula/inestable, desconexión, etiqueta por peso e importe solo si se habilitan como variantes separadas. Registrar valor observado por el dispositivo además del visible en la aplicación.

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
- `test/ModuloProductos/Entidades/ArticuloSelectPlatoBalanzaPolicyTest.java`

La lectura de fuente/tests orienta el riesgo y el criterio; no acredita la ejecución del artefacto. INFO resume, DEBUG describe acciones de negocio y TRACE añade diagnóstico saneado. Un fallo conserva paso, esperado, observado, categoría y evidencia; causa no determinada si falta prueba causal. No registrar credenciales, filas completas ni configuración privada.

