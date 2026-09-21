# Mapa público de cobertura en Excel

## Objetivo y límites

Dar a QA una vista descargable de lo implementado y lo que falta, sin exigirle leer código ni instalar herramientas para consultar el archivo. El Excel representa una foto del contenido público del repositorio; no es un reporte de ejecución ni acredita validación del JAR.

Las fuentes son las fichas del catálogo, `groups.json`, el roadmap y los ejemplos públicos del seed de XGestion. No leer `reports/`, `.local/`, `.env.local`, paquetes, dumps o credenciales. La foto inicial tiene 14 fichas —7 implementadas y 7 planificadas— y 0 validaciones reales registradas en el mapa público. No inferir resultados privados ni marcar casos como PASS.

Los grupos se superponen; no sumar sus conteos como casos distintos. Los 20 recorridos R01–R20 de Restobar y los 26 ejemplos comerciales del seed se presentan separados de las fichas y no incrementan la cantidad de E2E disponibles. El mapa no afirma cubrir todas las combinaciones del producto.

## Entregables y contrato

- `docs/coverage/xgestion-cobertura.json`: foto pública generada, utilizada para trazabilidad y control de actualización.
- `docs/coverage/xgestion-cobertura.xlsx`: libro generado con hojas **Resumen**, **Grupos**, **Escenarios**, **Por detallar** y **Ejemplos seed**.
- `docs/coverage/xgestion-cobertura.manifest.json`: hashes de los datos, archivos del generador y XLSX, con fecha de generación UTC.
- `docs/cobertura.md`: guía de lectura y regeneración, enlazada desde el README.
- Fuente y tests del generador junto a las herramientas del repositorio; sin cambiar dependencias necesarias para ejecutar E2E.

El libro usa nombres comprensibles, estados explícitos, filtros y referencias a las fuentes. Debe permitir distinguir «automatización implementada», «planificada», «por detallar» y «ejemplo pendiente de validar». Ejemplo de lectura: `XG-VEN-001 | Implementado | Validación real pendiente`; nunca convertir `implemented` en «probado». Resumen identifica la revisión por hash de los datos públicos; el timestamp UTC se conserva únicamente en el manifiesto, sin confundirse con una ejecución del producto.

## Generación y mantenimiento

```powershell
.\qa.cmd coverage
.\qa.cmd coverage --check
```

La generación actualiza JSON, XLSX y manifiesto. El control funciona sin Node, compara la foto pública con sus fuentes y verifica los hashes de datos, generador y libro; falla si falta alguno de los tres archivos, fue alterado o quedó desactualizado. No regenera silenciosamente. Incluir los tres archivos generados con el cambio de catálogo, grupos, roadmap o seed que los modifica. No editarlos a mano. El CI incorpora este control sin requerir herramientas de generación.

El mantenedor o su IA genera el libro con Node y `@oai/artifact-tool` del runtime local de Codex. La autodetección es portable, sin rutas personales incrustadas; `QA_COVERAGE_NODE` y `QA_COVERAGE_MODULES` permiten indicar herramientas ya disponibles en esa máquina. Consultar el XLSX y ejecutar E2E no requieren que cada QA instale Node.

## Secuencia y aceptación

1. Recoger y validar fuentes públicas; producir datos con IDs estables y separar los cuatro niveles de evidencia.
2. Generar el libro y la foto JSON con los mismos datos, y su manifiesto de hashes/fecha UTC; mantener conteos y referencias coherentes.
3. Agregar el comando de regeneración y el control de actualización; documentar operación y límites.
4. Verificar conteos, estados, omisión de datos privados, fuentes, desactualización detectable y apertura/legibilidad del libro. Los tests del generador no sustituyen pruebas del producto.

La aceptación exige las cinco hojas, 14 fichas sin duplicaciones, backlog y ejemplos separados, enlaces visibles desde README y un `coverage --check` correcto para los archivos entregados. Un cambio de fuente sin regenerar debe hacer fallar ese control. No agregar estados de validación real a partir de grupos, unit tests, seed o reportes privados.
