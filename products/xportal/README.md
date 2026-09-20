# XPORTAL

Estado: **`planned`**. Carpeta reservada; todavía no hay casos E2E ejecutables ni cobertura acreditada.

Producto web CodeIgniter 3. El motor previsto es Robot Framework Browser sobre Playwright. Al incorporarlo, cada QA configurará `XPORTAL_BASE_URL` en su `.env.local` con una URL de pruebas autorizada. No usar una URL de producción ni copiar el `.env` interno del servidor.

La ejecución contra una URL QA no requiere instalar PHP, Apache o el repositorio del producto en cada estación. El onboarding debe definir autenticación, roles, tenant y datos aislados antes de activar casos. Ver [preparación](docs/onboarding.md).

La estructura mantiene `scenarios/`, `suites/`, `resources/` y `docs/`. Las carpetas vacías expresan trabajo futuro, no tests omitidos o aprobados.
