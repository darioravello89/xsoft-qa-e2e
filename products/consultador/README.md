# Consultador web

Estado: **`planned`**. Se probará la aplicación web indicada por `CONSULTADOR_BASE_URL` en `.env.local`. Todavía no hay escenarios ejecutables ni se declara cobertura.

El motor previsto es Robot Framework Browser sobre Playwright. La URL QA define el producto desplegado que se debe probar; no se asume equivalencia entre los repositorios existentes `XConsultador` Angular y `Consultador` Next.js.

La estructura reserva `scenarios/`, `suites/`, `resources/` y `docs/`. Ver [onboarding](docs/onboarding.md) antes de agregar la primera suite.
