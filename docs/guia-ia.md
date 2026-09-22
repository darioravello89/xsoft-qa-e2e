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

Elegir una familia del roadmap y una variante concreta. Para Venta cotidiana ya existen XG-VEN-003 a XG-VEN-009: reutilizar sus IDs y criterios. Los siete casos de esa ampliación están implementados y requieren `sales_journeys`. VEN-003/007 usan botón y `Ctrl+E` únicamente con `ventas-teclado-v1` verificado para el SHA256 del JAR; los paquetes anteriores conservan el doble clic autorizado sobre una celda identificada por JAB. Verificar el editor y el resultado, sin coordenadas fijas ni sustituir la edición por cargar otro producto. El estado de accesibilidad se registra en el [CSV del producto](../products/xgestion/docs/backlog-accesibilidad.csv), separado del catálogo E2E. Para Restobar consultar el backlog R01–R20 antes de inventar cobertura. Esos identificadores de planificación no son IDs del catálogo ni se pueden pasar a `run --scenario`.

Pedir primero la ficha del recorrido, perfil y evidencia. Al implementar, actualizar grupos, ficha, adaptador, oráculos y Robot según [nuevas features](nuevas-features.md). Los tests fuente del ERP son insumo para reglas y riesgos; no sustituir acciones de usuario por llamadas internas de negocio ni declarar QA real por revisar esos tests.

El catálogo actual contiene 21 fichas implementadas y ninguna planificada: cinco smoke, nueve ventas y siete promociones, todas con ejecución real pendiente. Para ampliar promociones, reutilizar XG-PRM-001 a XG-PRM-007 sin duplicarlos y diseñar nuevos IDs para listas, combos, alcances o combinaciones aún no cubiertos. Los 26 ejemplos seed siguen siendo expectativas públicas: siete están vinculados a esas fichas; escribir el vínculo no acredita el JAR. Revisar `docs/specs/005-promociones.md`, mantener el marcador `seed` de las fichas que lo requieren y regenerar el mapa de cobertura después de actualizar sus fuentes.
