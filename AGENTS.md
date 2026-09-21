# Instrucciones para IA de QA y mantenimiento

## Objetivo y fuentes

Ayudar a QA a ejecutar y ampliar pruebas reproducibles. Leer primero `README.md`, `docs/guia-ia.md` y el README del producto. En XGestion consultar `products/xgestion/docs/roadmap.md` y `cobertura.md` antes de proponer casos. Los contratos técnicos están en `docs/specs/`, `docs/decisions/` y el código de `framework/`; los criterios de cada caso, en `products/<producto>/scenarios/`.

## Operación

- Usar `qa.cmd` y sus comandos documentados. No ejecutar Robot directamente para evitar preflight, aislamiento o restauración.
- XGestion requiere Windows exclusivo, consola local o de hipervisor, escritorio visible y desbloqueado y red desconectada durante su ejecución. El host de la VM puede seguir conectado para usar IA. No usar RDP.
- Nunca apuntar las pruebas a producción, a una instalación cotidiana de XGestion ni a una base compartida. No modificar productos o servicios externos desde este repositorio.
- Las credenciales se importan desde un paquete privado autorizado. No inventarlas, pegarlas en prompts, imprimir `.env.local` ni leerlas en voz alta. Para diagnosticar, comprobar nombres/presencia, no valores.
- No subir `.local/`, `.env.local`, JAR, dump, licencia, ZIP, reportes, logs ni capturas. Tratar también los árboles de accesibilidad como información privada.
- Para datos comerciales de XGestion, leer `products/xgestion/docs/seed.md` y reutilizar `catalogo-comercial-v1`. Aplicar únicamente mediante `seed --apply` o `run --seed`; no pegar el SQL de revisión en una DB. La única excepción SQL pública es `tests/fixtures/xgestion_seed_schema.sql`: estructura sintética para tests, sin datos privados.
- No modificar el aislamiento, los límites de rutas ni el marcador de propiedad para conseguir que pase una prueba. Un bloqueo se informa con causa y paso de resolución.
- No crear ni usar worktrees sin pedido explícito para la tarea actual. Preservar trabajo concurrente; staging solamente por rutas propias. No hacer commit o push salvo pedido del usuario.

## Nuevos casos

- Una ficha de backlog usa `status: planned`, sin archivo Robot ni resultado simulado. Al implementarla, actualizar Markdown y automatización juntos usando `templates/scenario.md`; mantener ID estable y tags coherentes entre catálogo y Robot.
- Redactar fichas desde la perspectiva del usuario, con resultados por paso, datos, configuración, recuperación y límites. SQL, selectores y referencias de código van en anexos técnicos. No convertir cada test unitario en un supuesto E2E.
- Registrar grupos en `products/<producto>/groups.json` con ID igual al tag. Reutilizar nombres existentes, mantener descripciones comprensibles y revisar conteos por estado. Una familia del roadmap puede no tener fichas todavía.
- Preferir esperas por estado observable, selectores accesibles verificados y oráculos por identidad/deltas. No sustituir aserciones por esperas fijas, coordenadas o tests que solo comprueban su propia implementación.
- No introducir casos falsos aprobados en productos `planned`. Un caso escrito pero no ejecutado sobre el producto conserva evidencia real pendiente.
- No ampliar automáticamente el alcance fiscal, impresión, integraciones o mutaciones externas. La v1 es venta local no fiscal sin impresión.
- Cada feature debe actualizar el catálogo, documentación de datos/prerrequisitos y resultado esperado. Ver `docs/nuevas-features.md`.

## Verificación y reporte

- Revisar scripts disponibles. Si en el futuro hay `package.json`, revisar y ejecutar `lint` y `stylelint` cuando existan y correspondan al cambio.
- Ejecutar Ruff, Robocop, pytest, `qa.cmd check` y `qa.cmd run --product xgestion --group regression --dry-run` para cambios de infraestructura/casos; registrar errores sin ocultarlos.
- Diferenciar controles del framework, dry-run y E2E real. No declarar producto validado porque el CI o el parser estén verdes.
- Usar INFO por defecto; DEBUG añade pasos y TRACE diagnóstico saneado. Ningún nivel permite secretos, configuración privada completa ni capturas de autenticación. Todo fallo debe conservar paso, esperado, observado, categoría y evidencia; decir «causa no determinada» si no está demostrada.
- `qa.cmd list --product xgestion --groups` y `--group ventas` ayudan a seleccionar; `run` ejecuta únicamente casos implementados. No contar backlog Restobar o las 420 clases de tests fuente como casos E2E disponibles.
- Entregar archivos cambiados, comprobaciones ejecutadas, bloqueos y riesgos. Para ejecución real informar producto/build, paquete, escenarios, resultados y reporte local sin secretos.
