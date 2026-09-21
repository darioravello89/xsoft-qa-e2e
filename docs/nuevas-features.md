# Incorporar una funcionalidad al catálogo

Cada cambio funcional debe dejar claros sus escenarios, datos y evidencia. QA y la IA mantienen la documentación junto con los tests en la misma revisión.

1. Identificar producto, familia, etapa, comportamiento de usuario y criterios de aceptación. En XGestion leer roadmap y cobertura; revisar casos existentes y backlog para evitar duplicaciones. Elegir una variante con configuración y datos explícitos, sin intentar cubrir un producto cartesiano de opciones.
2. Copiar `templates/scenario.md` a `products/<producto>/scenarios/<modulo>/<id>.md`. Asignar un ID único y estable. El encabezado entre `---` contiene **JSON**, no YAML libre.
3. Describir objetivo, perfil, datos, pasos con resultados visibles, recuperación, evidencia y límites. Dejar SQL y selectores en el anexo técnico. Si solo se está planificando, usar `status: planned`, omitir `test` y no crear `.robot`; terminar la ficha no acredita ejecución.
4. Al implementar, crear el test en `products/<producto>/suites/`, usar `status: implemented` y enlazarlo en `test`. Reutilizar el adaptador y recursos Robot; usar el mismo ID como tag y alinear todos los tags del Markdown. Añadir acciones y comprobaciones que sigan los pasos de la ficha, con logs DEBUG; dejar diagnóstico saneado para TRACE.
5. Si hacen falta datos comerciales de XGestion, revisar primero el [catálogo fijo](../products/xgestion/docs/seed.md). Para ampliarlo, mantener códigos/IDs existentes, agregar datos y expectativas con fuente, actualizar esa guía y probar aplicación repetida y colisiones. Si requiere contexto nuevo, ampliar el contrato del paquete y su baseline saneado. Si cambia la UI, recalibrar selectores contra el SHA-256 del JAR. No subir fixtures privados ni reemplazar expectativas con valores obtenidos del propio resultado.
6. Ejecutar Ruff, Robocop, pytest, `qa.cmd check` y `qa.cmd run --product xgestion --group regression --dry-run`, según el producto. Después correr el caso real y el grupo afectado en el entorno QA.
7. Revisar el diff, actualizar cobertura/roadmap y README/guías cuando cambie la operación. Verificar conteos por estado y `list --groups`, `list --group`, selección por ID y menú. Regenerar el [mapa público](cobertura.md) con `qa.cmd coverage` y exigir `qa.cmd coverage --check` antes de publicar; incluir los tres archivos de `docs/coverage/` —JSON, XLSX y manifiesto con hashes/fecha UTC— con el cambio de fuentes. El control funciona sin Node y corre también en CI. Informar qué pasó técnicamente y qué se probó realmente. Mantener el ID aunque cambie el nombre descriptivo.

## Encabezado del catálogo

El campo `test` es la ruta relativa al archivo ejecutable dentro del repositorio. `status: implemented` indica que hay automatización implementada, no que ya aprobó una ejecución sobre el producto. El estado de validación real debe registrarse en el reporte y documentación de aceptación.

Registrar grupos en `products/<producto>/groups.json`: ID igual al tag, nombre legible, descripción y etapa. Reutilizar `smoke`, `regression`, `ventas`, `efectivo`, etc. Evitar sinónimos como `venta`, `sales` y `ventas`. El módulo debe existir como grupo y el caso debe tener una etiqueta registrada; etiquetas técnicas como `xgestion` y `escritura` no necesitan convertirse en opciones del menú.

El estado `manual` permite documentar un procedimiento que no se ejecuta con Robot. Igual que `planned`, no genera PASS ni cuenta como automatización. Las filas de backlog del roadmap no son fichas del catálogo. Los grupos sin fichas implementadas se muestran pendientes, con ejecución bloqueada y motivo.

El Excel es generado y no se edita a mano. Sus grupos pueden repetir escenarios; los recorridos Restobar por detallar y los ejemplos del seed se cuentan separados. No llenar estados de validación real a partir de un test de infraestructura o de la existencia de una ficha. Regenerarlo requiere Node con `@oai/artifact-tool` en el runtime del mantenedor/IA, sin agregar Node como requisito para ejecutar E2E o leer el archivo publicado.

## Evidencia y diagnóstico al ampliar

Cada nuevo caso debe explicar qué observa en UI y qué contrasta en persistencia u otro sistema. INFO conserva caso/resultado/resumen; DEBUG añade pasos; TRACE diagnóstico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia sin depender del nivel. Redactar secretos antes de emitir o guardar texto; usar canarios sintéticos para verificarlo.

Para la extensión Venta cotidiana, mantener `sales_journeys` y las columnas de `sale.lines` alineados con las fichas. Los índices pertenecen al modelo observado por JAB; no son posiciones de controles para elegir la primera coincidencia. La configuración de aviso ausente, la consolidación y los defaults se declaran en el paquete y se comprueban en pantalla. Un paquete anterior debe seguir sirviendo para los siete casos iniciales; la falta de la extensión bloquea los nuevos antes del JAR.

Registrar la fuente de la regla sin confundirla con prueba del JAR: commit del producto, hash del artefacto y ejecución son evidencias distintas. Si falta comprobar soporte de una variante, mantenerla pendiente. No redefinir el esperado para que coincida con el observado ni inventar una causa raíz.

## Activar un producto pendiente

Completar primero su onboarding: aplicación/URL real de QA, acceso local privado, datos aislados, motor instalado y primer caso comprobado. Luego registrar el producto en el runner y agregar catálogo y tests. Mientras sea `planned`, no se considera ejecutable ni cuenta como cobertura.
