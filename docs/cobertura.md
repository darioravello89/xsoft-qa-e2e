# Consultar y actualizar el mapa de cobertura

Abrí o descargá el [Excel de cobertura de XGestion](coverage/xgestion-cobertura.xlsx). En GitHub, usá la descarga del archivo si no aparece una vista previa. Para consultarlo no necesitás el paquete privado, Node, Java ni una instalación del ERP; basta una aplicación compatible con `.xlsx`.

El archivo responde qué está implementado, qué está planificado y qué falta detallar. Es una foto pública del repositorio, no el resultado de una corrida. El [mapa funcional](../products/xgestion/docs/cobertura.md) y el [roadmap](../products/xgestion/docs/roadmap.md) conservan el contexto y los límites de cada familia.

## Leer las hojas

| Hoja | Qué consultar | Cómo interpretarla |
| --- | --- | --- |
| Resumen | Conteos y alcance de la foto. | Implementación y validación real son medidas distintas. |
| Grupos | Familias, etapas y cantidades por estado. | Un caso puede aparecer en varios grupos; no sumar las filas como E2E únicos. |
| Escenarios | Fichas por ID, objetivo, estado y referencias. | `implemented` significa que hay automatización; `planned` significa que falta implementarla. |
| Por detallar | Familias y referencias del roadmap, incluidas las que ya tienen fichas. | R01–R20 apuntan a fichas Restobar pendientes de automatizar; las referencias no suman casos. |
| Ejemplos seed | Ejemplos comerciales y expectativas de la batería pública. | Son ejemplos pendientes de validar con el perfil y el JAR, no resultados observados. |

La foto actual distingue **298 fichas: 96 implementadas y 202 planificadas**, con **0 validaciones reales registradas en este mapa público**. Las implementadas son cinco de smoke, nueve de ventas y 82 de promociones; las pendientes son PRM-077/078 (paquete de varios contextos), 24 remitos de compra, 40 Restobar, 28 listas de precios y 58 de circuitos críticos (clientes/proveedores/cuotas, Libro Diario/caja, conciliación, inventario y respaldos), más 50 del complemento crítico. Ese cero no afirma que nadie haya ejecutado pruebas en privado: el generador no lee reportes de QA. Las 20 referencias R01–R20 de Restobar y los 26 ejemplos de cálculo del seed tienen su propio espacio; no se suman a las 298 fichas ni a los 96 casos implementados. Cada R enlaza los IDs XG-RES relacionados en el roadmap. Veinte ejemplos seed enlazan fichas implementadas y seis enlazan fichas de listas pendientes; los 26 tienen referencia, sin acreditar el JAR. Ningún vínculo otorga PASS ni garantiza todos los datos de la ficha. La mejora de accesibilidad del editor se registra en un backlog independiente; la especificación inicial del mapa conserva sus conteos históricos y las fuentes actuales determinan cada regeneración.

El grupo `promociones` conserva un primer lote implementado: porcentaje, importe fijo, 2x1, segunda unidad al 50 % y ofertas vencidas, futuras o inactivas. Las fichas incluyen editar cantidad, cancelar/retomar y un único cobro, bajo el [perfil de promociones](../products/xgestion/docs/promociones.md). El [mapa de pendientes](../products/xgestion/docs/promociones-pendientes.md) agrega 31 casos de alcances, 21 de agrupadas, 5 de combos y 15 de condiciones. De esa ampliación, 70 casos están implementados y PRM-077/078 siguen pendientes. En **Escenarios**, filtrar Automatización por Pendiente y Grupos para QA por Promociones para localizar esos dos; filtrar Grupos para QA por `ofertas-familia` o uno de los subgrupos para consultar cada familia. **Grupos** muestra sus conteos; **Ejemplos seed** distingue vínculos implementados de pendientes. Una familia parcialmente implementada no acredita todas sus variantes.

Un grupo sin casos implementados muestra una oportunidad de ampliación. Un caso planificado no equivale a una prueba fallida. Una familia con alguna automatización tampoco implica que todas sus variantes estén cubiertas. Para elegir qué desarrollar después, revisar sus dependencias, datos, configuración y criterios en el roadmap.

## Controlar remitos, Restobar y listas

- [Remitos de compra](../products/xgestion/docs/remitos.md): XG-REM-001..024.
- [Restobar, opciones y recetas](../products/xgestion/docs/restobar.md): XG-RES-001..040.
- [Listas por origen, horario y prioridad](../products/xgestion/docs/listas-precios.md): XG-LPR-001..028.

En **Escenarios**, filtrar **Grupos para QA** por `remitos`, `restobar` o
`listas-precios`; filtrar **Automatización** por Pendiente. Abrir la ficha para
ver datos, pasos, variantes y bloqueos. La columna **Prioridad** usa la prioridad explícita de la ficha cuando existe;
en los demás casos se hereda de la etapa.
La hoja **Grupos** muestra los subgrupos para planificar el siguiente lote.

## Controlar los circuitos críticos

El [roadmap financiero y operativo](../products/xgestion/docs/circuitos-criticos.md)
ordena 58 fichas nuevas y enlaza sus mapas. Filtrar **Grupos para QA** por
`ctacte-clientes`, `ctacte-proveedores`, `cuotas`, `libro-diario`, `caja`,
`conciliacion`, `inventario` o `respaldos`, y **Automatización** por Pendiente.
Los subgrupos de cierre e integridad también permiten revisar sus variantes.
La cantidad del grupo puede incluir fichas transversales: los IDs únicos de
Escenarios son la unidad de conteo. No hay nuevas pruebas Robot ni aceptación real.

## Controlar el complemento crítico

El [mapa de las 50 fichas adicionales](../products/xgestion/docs/complementos-criticos.md)
enlaza nueve circuitos. Filtrar Grupos para QA por `cobros-combinados`,
`presupuestos`, `devoluciones`, `fiscal`, `pagos-externos`, `recuperacion`,
`concurrencia`, `actualizacion` o `beneficios`. `sincronizacion`, `impuestos`
y `fidelizacion` permiten afinar la selección. Filtrar Automatización por
Pendiente; cada ficha aclara los contratos, datos y laboratorio que faltan.

## Regenerar desde las fuentes

Esto corresponde al mantenedor o a su IA local. Después de modificar fichas, grupos, roadmap o ejemplos del seed:

```powershell
.\qa.cmd coverage
.\qa.cmd coverage --check
```

El primer comando genera tres archivos en `docs/coverage/`: [la foto JSON](coverage/xgestion-cobertura.json), el Excel y [el manifiesto](coverage/xgestion-cobertura.manifest.json). Este último registra hashes de los datos, el generador y el XLSX, junto con la fecha de generación en UTC. El segundo comando comprueba los tres archivos contra las fuentes y el generador actuales, sin regenerarlos y **sin necesitar Node**. Debe terminar correctamente antes de publicar. Si informa que faltan archivos, fueron alterados o están desactualizados, revisar las fuentes, regenerar y repetir el control. Revisar también el Excel resultante y añadir los tres archivos a la misma revisión que sus fuentes.

La hoja Resumen identifica la revisión mediante un hash de los datos públicos. La fecha UTC queda en el manifiesto; no se inserta un timestamp de generación en el Excel ni se presenta como fecha de ejecución del producto.

**No editar las celdas, el JSON ni el manifiesto generado a mano.** Corregir la ficha, el grupo, el roadmap o el ejemplo comercial de origen y volver a generar. No completar un «PASS» en el Excel: la evidencia de ejecución real conserva su flujo privado por producto, build y entorno.

La generación usa Node y `@oai/artifact-tool` disponibles en el runtime local de Codex del mantenedor. El comando busca ese runtime sin depender de una ruta personal fija. Si hace falta indicar una instalación compatible existente, usar estas variables locales:

| Variable | Valor esperado |
| --- | --- |
| `QA_COVERAGE_NODE` | Ruta del ejecutable Node que generará el libro. |
| `QA_COVERAGE_MODULES` | Directorio de módulos que contiene `@oai/artifact-tool`. |

No copiar rutas personales al repositorio ni agregar estas herramientas al setup de E2E de cada QA. Si falta el runtime, la IA o el mantenedor debe resolverlo en su equipo de generación; el QA puede seguir consultando el Excel publicado y ejecutando las pruebas con el setup habitual.

El generador utiliza únicamente información pública del catálogo, grupos, roadmap y seed. No necesita abrir `.env.local`, paquetes, dumps, `.local/` ni `reports/`. La [especificación](specs/003-mapa-cobertura.md) detalla los criterios del mapa.

## Control crítico de ofertas USD

Filtrar **Grupos para QA** por **Ofertas en USD — P0**: PRM-080..084, cinco casos automatizados y trece variantes obligatorias. La prioridad explícita de una ficha prevalece sobre la heredada de su etapa; estos cinco muestran P0. La columna Validación real permanece Pendiente. Ver [perfil y alcance](../products/xgestion/docs/ofertas-usd.md).
