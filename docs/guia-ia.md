# Trabajar con la IA local

Abrí este repositorio en la herramienta de IA que use tu equipo. Pedile que lea `AGENTS.md` antes de operar. Si XGestion corre en una VM sin red, podés conversar con la IA desde el host y copiar solamente comandos y diagnósticos saneados hacia/desde la VM.

## Ejecutar casos existentes

1. Pedí que lea el [roadmap](../products/xgestion/docs/roadmap.md) y la [cobertura](../products/xgestion/docs/cobertura.md). Primero debe distinguir los casos implementados de los planificados.
2. Consultá `qa.cmd list --product xgestion --groups`. Para ver los casos de una familia, usá `qa.cmd list --product xgestion --group ventas`. Los grupos tienen nombre descriptivo, propósito y conteos; un caso en varios grupos sigue siendo un solo caso.
3. Elegí un grupo o ID. La IA lee sus fichas y explica objetivo, perfil, pasos, resultados y efectos en lenguaje de usuario; el SQL queda en el anexo. Un caso `planned` todavía no se ejecuta.
4. Ejecutá `qa.cmd doctor --product xgestion` y luego `qa.cmd run --product xgestion --group ventas --log-level INFO` en la máquina aislada. También podés abrir `qa.cmd`, elegir Ejecutar grupo, su número y el nivel de detalle. Dejá el escritorio disponible.
5. Abrí `qa.cmd report --latest`. La IA puede interpretar los mensajes saneados; no necesita tus contraseñas.

Para el primer lote de promociones, usá `qa.cmd list --product xgestion --group promociones` y leé las fichas XG-PRM-001 a XG-PRM-007 junto con el [perfil de promociones](../products/xgestion/docs/promociones.md). Ejecutá `qa.cmd run --product xgestion --group promociones --log-level DEBUG` o elegí su grupo en el menú. El runner anuncia y prepara automáticamente `catalogo-comercial-v1` cuando una selección lo requiere, incluida la regresión completa o un ID PRM; `--seed catalogo-comercial-v1` sigue disponible como opción explícita. El dry-run no aplica datos ni abre el producto.

Antes de esos casos, la IA debe verificar perfil ARS, comprobante interno 99, Ninguna Lista (ID 0), cliente/turno sin listas, otros descuentos en cero y fidelización deshabilitada; calibración `promociones-v1`, `ventas-etapa1` y `ventas-teclado-v1` para el SHA256 del JAR. Si falta un requisito, informar el bloqueo: no cambiar datos comerciales desde un keyword, suprimir controles ni adivinar columnas. En pantalla se distinguen subtotal bruto, oferta y neto; en persistencia `vecTotal` conserva el bruto y `venTotal` el neto. Los negativos comprueban primero una oferta válida y la abandonan sin efectos; no interpretar «nunca aplica ofertas» como un resultado correcto.

No es necesario que entiendas Python o Robot para ejecutar un caso. Para crear pruebas nuevas, la IA sí debe implementar las acciones y aserciones y verificar el resultado sobre el producto; escribir un Markdown no automatiza por sí solo una prueba.

## Elegir cuánto detalle ver

| Nivel | Cuándo usarlo | Contenido |
| --- | --- | --- |
| INFO, predeterminado | Ejecución habitual | Cada caso, resultado y resumen final. |
| DEBUG | Comprender dónde avanza o falla | Pasos de usuario y comprobaciones además del resumen. |
| TRACE | Investigar con una persona responsable | Diagnóstico técnico saneado además de los pasos. |

Ejemplo: `qa.cmd run --product xgestion --scenario XG-VEN-001 --log-level DEBUG`. Los tres niveles mantienen las mismas pruebas. Un error siempre debe mostrar paso, esperado, observado, categoría y evidencia disponible, incluso con INFO. No volver a ejecutar una operación solo para conseguir más logs sin considerar que el runner restaurará el entorno y que se perderá el estado anterior; conservar primero la evidencia privada.

## Qué puede compartir QA

Compartí ID del caso, versión de XGestion, etapa que falló y mensaje sin datos sensibles. No pegues el contenido de `.env.local`, `config.properties`, licencias, dumps o tokens. Los reportes y árboles de accesibilidad pueden contener nombres de usuarios y artículos; mantenelos en el entorno privado.

## Cómo informar un resultado

Usá una frase como: «XG-VEN-001, build y hash JAR registrados, paquete QA identificado: FAIL en verificar stock; esperado −2, observado sin cambio; categoría de comprobación, causa no determinada; reporte local disponible». La categoría orienta el diagnóstico, no prueba la causa. No atribuir automáticamente un fallo al ERP, al selector o a los datos. Si solo se ejecutó `check` o `dry-run`, indicá «validación técnica, E2E real pendiente».

El resultado global está en `report.html`, resumen oficial del runner abierto por `qa.cmd report --latest`. Incluye grupos y fallos de preparación/cierre. `robot-report.html` y `log.html` sirven como detalle parcial de Robot y pasos, generados desde XML saneado; no reemplazan el resultado global cuando falla el entorno fuera de un caso.

Ante un bloqueo no pidas a la IA que quite el control. Primero debe identificar si falta el paquete, la licencia offline, la calibración, el escritorio o el aislamiento de red. Los pasos habituales están en [solución de problemas](solucion-de-problemas.md).

## Planificar y ampliar con IA

Elegir una familia del roadmap y una variante concreta. Para Venta cotidiana ya existen XG-VEN-003 a XG-VEN-009: reutilizar sus IDs y criterios. Los siete casos de esa ampliación están implementados y requieren `sales_journeys`. VEN-003/007 usan botón y `Ctrl+E` únicamente con `ventas-teclado-v1` verificado para el SHA256 del JAR; los paquetes anteriores conservan el doble clic autorizado sobre una celda identificada por JAB. Verificar el editor y el resultado, sin coordenadas fijas ni sustituir la edición por cargar otro producto. El estado de accesibilidad se registra en el [CSV del producto](../products/xgestion/docs/backlog-accesibilidad.csv), separado del catálogo E2E. Para Restobar consultar el [mapa y sus 40 fichas](../products/xgestion/docs/restobar.md). R01–R20 se conservan como referencias del roadmap, vinculadas a XG-RES; no se pasan a `run --scenario` ni suman casos adicionales.

Pedir primero la ficha del recorrido, perfil y evidencia. Al implementar, actualizar grupos, ficha, adaptador, oráculos y Robot según [nuevas features](nuevas-features.md). Los tests fuente del ERP son insumo para reglas y riesgos; no sustituir acciones de usuario por llamadas internas de negocio ni declarar QA real por revisar esos tests.

El catálogo actual contiene 298 fichas: 96 implementadas y 202 planificadas, todas con ejecución real pendiente. Para ampliar promociones, leer el [mapa de pendientes](../products/xgestion/docs/promociones-pendientes.md) y reutilizar los IDs XG-PRM-008..079. Los subgrupos `promociones-alcances`, `promociones-agrupadas`, `promociones-combos` y `promociones-condiciones` permiten consultar y ejecutar sus fichas implementadas. Para los 70 nuevos recorridos, completar la [calibración de canastas](../products/xgestion/docs/canastas-ofertas.md); PRM-077/078 no se ejecutan. Los filtros `ofertas-familia`, `ofertas-subfamilia`, `ofertas-marca`, `ofertas-sector` y `ofertas-producto` cruzan alcances sin duplicar casos.

Los 26 ejemplos seed siguen siendo expectativas públicas: veinte están vinculados a fichas implementadas y seis a fichas LPR pendientes (016/017/019/020). Un vínculo no acredita el JAR ni garantiza todos los datos de un escenario. Revisar `docs/specs/005-promociones.md` y `006-backlog-promociones.md`, preparar los fixtures nuevos declarados y conservar los IDs al automatizar. Mantener el marcador `seed` de las fichas implementadas que lo requieren y regenerar el mapa después de actualizar sus fuentes.

Los grupos `remitos`, `restobar` y `listas-precios` son backlog documentado: leer sus mapas y fichas antes de implementar. No generar PASS ni usar el seed de ofertas como si contuviera todos sus datos. Priorizar recepción/stock, recetas con varios renglones y precedencia cliente/turno/base; las divergencias de reglas entre Venta y Restobar deben resolverse, no copiarse de un circuito al otro.

Para cuentas corrientes, Libro Diario, caja e integridad, comenzar por el
[roadmap de circuitos críticos](../products/xgestion/docs/circuitos-criticos.md)
y sus 58 fichas planned. No equiparar cobro manual, cuota y pago a proveedor,
ni sumar todas las filas de finanzas como efectivo. Las dependencias sin
procedimiento y los criterios pendientes bloquean la variante. Importar una
base mediante upserts no demuestra recuperar una fotografía anterior.

## Complemento de escenarios críticos

El [mapa complementario](../products/xgestion/docs/complementos-criticos.md) añade 50 fichas
planned de cobros/documentos, servicios, continuidad y beneficios. Revisar
los filtros del catálogo y del Excel; deben conservar 96 implementados,
202 pendientes y ninguna validación real inferida. Los casos nuevos no se
ejecutan. Datos, accesibilidad y laboratorios propios siguen pendientes.

## Ofertas USD P0

Para PRM-080..084 leer [ofertas-usd-v1](../products/xgestion/docs/ofertas-usd.md). No convertir Paga=50 a ARS en el seed, no relajar selectores ni aceptar ARS 50 como esperado. Se requieren las trece variantes y moneda visible/persistida consistente; un fallo o bloqueo mantiene pendiente la aceptación del circuito.
