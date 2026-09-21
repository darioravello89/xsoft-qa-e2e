# Plan 001 — Implementación y habilitación inicial

## 1. Base del repositorio

Implementar CLI y menú, instalación idempotente, dependencias fijadas, paquete privado verificado por hash, configuración local ignorada, catálogo validado y reportes locales. Mantener cada producto encapsulado y documentar los futuros como `planned`.

## 2. Entorno XGestion

Preparar perfil exclusivo con JAR `2.02.189-lts`, licencia QA offline vigente y MySQL portable propio. Validar red desconectada, escritorio utilizable, configuración, rutas y propiedad del runtime antes de ejecutar. Restaurar únicamente la instancia propia y evitar ejecuciones concurrentes.

## 3. Casos y documentación

Implementar acceso, consulta de producto y venta básica no fiscal; describir cada escenario en Markdown con ID y tags coherentes. Comprobar persistencia por identidad y deltas. Añadir quickstart, guía IA, preparación de paquete, calibración, troubleshooting y protocolo de aceptación.

## 4. Controles técnicos

Ejecutar Ruff, Robocop, pytest, validación de catálogo y dry-run. El CI repite esos controles en Windows y Ubuntu sin aplicación ni secretos. Revisar que fallos de entorno y falta de selectores no aparezcan como escenarios aprobados.

## 5. Habilitación con paquete privado

Pendiente de material real: validar el paquete legítimo, calibrar el bridge y selectores, completar onboarding en VM limpia y ejecutar el conjunto inicial tres veces en serie. Registrar resultados privados y corregir cualquier diferencia de producto/datos antes de recomendar uso rutinario.

La entrega de infraestructura no sustituye el quinto paso. Los bloqueos se documentan con el requisito faltante y su responsable; no se inventan credenciales, licencias ni resultados.

## Ampliación aprobada — mapa funcional, grupos y logs

1. **Documentación revisable:** redactar roadmap de siete etapas y matriz de cobertura; reformular las siete fichas disponibles en lenguaje de usuario con anexos técnicos; agregar VEN-003 a VEN-009 como `planned` sin `.robot`. Aceptación: perfiles explícitos, resultado por paso, recuperación y límites; backlog Restobar separado de los conteos.
2. **Grupos coherentes:** registrar grupos por producto con ID/tag estable, nombre, propósito y etapa. Incorporar `list --groups`, filtro `list --group`, conteos por estado y menú numérico descriptivo. Aceptación: grupos vacíos/pendientes visibles sin ejecución; filtros e IDs previos compatibles; VEN-001 suma efectivo/cobros sin perder tags.
3. **Resultados comprensibles:** INFO predeterminado para cada caso/resumen, DEBUG para pasos, TRACE para diagnóstico saneado. Aceptación: mismos escenarios y aserciones; fallos informan paso, esperado/observado, categoría y evidencia; secretos ausentes incluso en TRACE; no inventar causa raíz.
4. **Verificación de la ampliación:** revisar scripts; Ruff, Robocop, pytest, `qa.cmd check` y dry-run. Contrastar conteos 7/7, selección por ID/grupo, menú y nivel INFO. Registrar estos controles como técnicos, sin abrir JAR ni DB ni afirmar QA real.
5. **Ampliar Venta después:** implementar cada ficha planeada cuando existan paquete, selectores y datos comprobados; ejecutar sola/en grupo y actualizar cobertura. Continuar condiciones comerciales, cobros/documentos, después de vender y Restobar según dependencias del [roadmap](../../products/xgestion/docs/roadmap.md). Integraciones requieren laboratorio propio.

Dependencias: 1 fija el vocabulario y alcance; 2 y 3 comparten catálogo y reporte, por lo que sus contratos se coordinan; 4 valida el conjunto. El paso 5 y la aceptación GUI son trabajo posterior, no resultados de escribir el roadmap. No se comprometen fechas ni cobertura de todas las combinaciones.
