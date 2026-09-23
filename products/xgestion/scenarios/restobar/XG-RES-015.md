---
{"id":"XG-RES-015","title":"Consumir extras una sola vez con varios platos y distinto orden","product":"xgestion","module":"restobar","tags":["xgestion","regression","restobar","restobar-recetas","restobar-opciones","stock"],"status":"planned"}
---

# XG-RES-015 — Consumir extras una sola vez con varios platos y distinto orden

## Objetivo

Consumir extras una sola vez con varios platos y distinto orden, desde la perspectiva del mozo, cajero o supervisor que opera el pedido.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 5.**
Referencia de planificación: **Recetas**. Ver [mapa de Restobar](../../docs/restobar.md).
No tiene suite Robot, seed automático ni validación real del JAR. Los resultados siguientes son criterios esperados, no resultados obtenidos.

## Precondiciones y datos

- Paquete QA sintético, Windows exclusivo y escritorio visible. La preparación de carta, mesas, ingredientes, permisos y perfiles de este caso está **pendiente**; `catalogo-comercial-v1` no certifica estos datos.
- Perfil local por defecto: ARS, comprobante interno no fiscal, impuestos y cubiertos $0 salvo indicación, sin ofertas, listas ni beneficios adicionales. Las integraciones se habilitan solo en el laboratorio indicado.
- Receta actual de PLATO-A: queso 0,05 kg/plato. Extra queso 0,02 kg por plato; PLATO-B sin receta a $500. Queso inicial 10 kg. A $1.000, extra $80; sin consolidación ambigua.
- Riesgo de consumo repetido identificado en lectura de fuente; no es un fallo demostrado sobre JAR. Prioridad de automatización P0.
- Preparar y registrar antes de ejecutar los IDs propios de empresa, sucursal, puesto, cuenta, mesa y productos. Mantener una operación de control ajena al caso para verificar aislamiento.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Cargar A cantidad 2 con un extra y luego B cantidad 1. | A $2.160 más B $500, total $2.660; dos platos A conservan la selección de extra. |
| Cobrar y consultar el consumo de queso. | Consumo comercial esperado: receta 0,10 kg más extra 0,04 kg = 0,14 kg; stock final 9,86 kg. |
| Restaurar el baseline y repetir cargando B antes que A. | Mismos importes y mismo consumo 0,14 kg; el orden y número de filas no multiplican el extra. |
| Repetir A sin B y con dos consumos A personalizados por separado. | La suma de ingredientes coincide con los platos y extras comprados, sin omisiones ni doble descuento. |

## Variantes y límites

Ingredientes compartidos por receta y extra; extra en un solo renglón y dos renglones; cancelar antes de pagar. El esperado se calcula desde unidades vendidas y receta, nunca copiando iteraciones internas.

## Dependencias para automatizar

Preparar el baseline privado reproducible y sus datos, declarar el perfil, calibrar acciones accesibles sobre el SHA256 del JAR y construir comprobaciones por identidad. Utilizar atajos/acciones accesibles verificados; no tomar una posición de pantalla como identidad. Si el control o laboratorio no está disponible, mantener el caso pendiente y explicar el bloqueo.

## Evidencia y límites

Conservar UI y valores esperados/observados de cada transición. En una cuenta abierta distinguir lo guardado de lo cobrado: salir de la pantalla no es abandonar la venta. Registrar por separado **estado de cuenta, ocupación de mesa y estado de cocina** cuando apliquen.

Comparar operaciones, consumos, opciones, importes y efectos de stock/pagos por identidad y deltas según el caso, con lecturas autorizadas y saneadas. Las salidas de cocina, fiscalización y dispositivos requieren evidencia del extremo receptor; un log o test unitario no la sustituye. Registrar versión/SHA256 del JAR, commit del harness, paquete, perfil, IDs y reporte privado.

## Recuperación

Ante una discrepancia conservar primero la evidencia y cancelar o retomar por la interfaz según los pasos del caso. No borrar ni corregir registros comerciales para obtener un resultado aprobado. Restaurar el baseline QA antes de otra variante; para un cierre de resultado ambiguo conciliar la operación antes de reintentar, evitando cobrar o consumir ingredientes dos veces.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas relativas a XGestion2:

- `src/ModuloVentas/Entidades/TicketVenta.java`
- `src/Utilidades/Pickers/FormProductoOpcionesPicker.java`
- `src/ModuloProductos/Entidades/ProductoHijo.java`
- `src/ModuloRestobar/DAO/VentaOpcionDAO.java`

La lectura de fuente/tests orienta el riesgo y el criterio; no acredita la ejecución del artefacto. INFO resume, DEBUG describe acciones de negocio y TRACE añade diagnóstico saneado. Un fallo conserva paso, esperado, observado, categoría y evidencia; causa no determinada si falta prueba causal. No registrar credenciales, filas completas ni configuración privada.

