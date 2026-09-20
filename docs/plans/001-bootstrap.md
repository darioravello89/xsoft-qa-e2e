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
