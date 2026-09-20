# Incorporar una funcionalidad al catálogo

Cada cambio funcional debe dejar claros sus escenarios, datos y evidencia. QA y la IA mantienen la documentación junto con los tests en la misma revisión.

1. Identificar producto, módulo, comportamiento esperado y criterios de aceptación de la feature. Revisar casos existentes para evitar duplicaciones.
2. Copiar `templates/scenario.md` a `products/<producto>/scenarios/<modulo>/<id>.md`. Asignar un ID único y estable. El encabezado entre `---` contiene **JSON**, no YAML libre.
3. Describir precondiciones, pasos, resultado esperado, efectos y datos concretos. Separar cobertura positiva, negativa y límites cuando tengan objetivos distintos.
4. Implementar el test en `products/<producto>/suites/` y reutilizar el adaptador del producto y recursos Robot de `resources/`. Usar el mismo ID como tag; alinear los tags de agrupación con el Markdown.
5. Si hacen falta datos, ampliar el contrato del paquete y su baseline saneado. Si cambia la UI, recalibrar selectores contra el SHA-256 del JAR. No subir fixtures privados ni reemplazar expectativas con valores obtenidos del propio resultado.
6. Ejecutar Ruff, Robocop, pytest, `qa.cmd check` y `qa.cmd run --product xgestion --group regression --dry-run`, según el producto. Después correr el caso real y el grupo afectado en el entorno QA.
7. Revisar el diff y actualizar README/guías cuando cambie la operación. Informar qué pasó técnicamente y qué se probó realmente. Mantener el ID aunque cambie el nombre descriptivo.

## Encabezado del catálogo

El campo `test` es la ruta relativa al archivo ejecutable dentro del repositorio. `status: implemented` indica que hay automatización implementada, no que ya aprobó una ejecución sobre el producto. El estado de validación real debe registrarse en el reporte y documentación de aceptación.

Usar tags sencillos para filtros: `smoke`, `regression` y el módulo, por ejemplo `ventas`. Evitar crear sinónimos como `venta`, `sales` y `ventas` para el mismo grupo.

## Activar un producto pendiente

Completar primero su onboarding: aplicación/URL real de QA, acceso local privado, datos aislados, motor instalado y primer caso comprobado. Luego registrar el producto en el runner y agregar catálogo y tests. Mientras sea `planned`, no se considera ejecutable ni cuenta como cobertura.
