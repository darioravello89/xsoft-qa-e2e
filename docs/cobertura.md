# Consultar y actualizar el mapa de cobertura

Abrí o descargá el [Excel de cobertura de XGestion](coverage/xgestion-cobertura.xlsx). En GitHub, usá la descarga del archivo si no aparece una vista previa. Para consultarlo no necesitás el paquete privado, Node, Java ni una instalación del ERP; basta una aplicación compatible con `.xlsx`.

El archivo responde qué está implementado, qué está planificado y qué falta detallar. Es una foto pública del repositorio, no el resultado de una corrida. El [mapa funcional](../products/xgestion/docs/cobertura.md) y el [roadmap](../products/xgestion/docs/roadmap.md) conservan el contexto y los límites de cada familia.

## Leer las hojas

| Hoja | Qué consultar | Cómo interpretarla |
| --- | --- | --- |
| Resumen | Conteos y alcance de la foto. | Implementación y validación real son medidas distintas. |
| Grupos | Familias, etapas y cantidades por estado. | Un caso puede aparecer en varios grupos; no sumar las filas como E2E únicos. |
| Escenarios | Fichas por ID, objetivo, estado y referencias. | `implemented` significa que hay automatización; `planned` significa que falta implementarla. |
| Por detallar | Familias y recorridos pendientes de convertirse en escenarios completos. | Incluye el backlog de Restobar, sin hacerlo pasar por casos ejecutables. |
| Ejemplos seed | Ejemplos comerciales y expectativas de la batería pública. | Son ejemplos pendientes de validar con el perfil y el JAR, no resultados observados. |

La foto inicial distingue **14 fichas: 7 implementadas y 7 planificadas**, con **0 validaciones reales registradas en este mapa público**. Ese cero no afirma que nadie haya ejecutado pruebas en privado: el generador no lee reportes de QA. Los 20 recorridos R01–R20 de Restobar y los 26 ejemplos de cálculo del seed tienen su propio espacio; no se suman a las 14 fichas ni a los 7 casos implementados.

Un grupo sin casos implementados muestra una oportunidad de ampliación. Un caso planificado no equivale a una prueba fallida. Una familia con alguna automatización tampoco implica que todas sus variantes estén cubiertas. Para elegir qué desarrollar después, revisar sus dependencias, datos, configuración y criterios en el roadmap.

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
