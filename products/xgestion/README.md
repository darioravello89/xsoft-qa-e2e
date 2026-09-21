# XGestion: primeras pruebas automatizadas

Esta suite ejecuta el JAR Windows mediante Java Access Bridge y valida lo observado en pantalla. Las ventas se contrastan con consultas SQL de lectura sobre la instancia QA local. No invoca métodos internos de negocio ni usa el checkout del ERP.

**Estado: implementación inicial; ejecución GUI real pendiente.** Los ejemplos de localizadores son borradores y bloquean ejecución. Un QA responsable debe preparar el paquete privado, calibrar contra el JAR exacto y aprobar el recorrido en la VM aislada. Un `dryrun` verde sólo valida estructura Robot.

Comenzar por el [quick start general](../../README.md). Después:

```powershell
qa.cmd list --product xgestion
qa.cmd list --product xgestion --groups
qa.cmd list --product xgestion --group ventas
qa.cmd doctor
qa.cmd run --product xgestion --group smoke
```

Consultar `qa.cmd --help` para los filtros disponibles del runner. No ejecutar Robot directamente contra una instalación real: el runner prepara entorno, aislamiento, restauración y exclusión de ejecuciones simultáneas.

| ID | Grupo | Resultado exigido |
|---|---|---|
| XG-INI-001 | inicio / smoke | Login accesible del PID iniciado por el test. |
| XG-AUT-001 | autenticación / smoke | Acceso inválido, mensaje y campos vaciados. |
| XG-AUT-002 | autenticación / smoke | Usuario, empresa y sucursal QA exactos. |
| XG-PRO-001 | productos / smoke | Búsqueda del código fixture devuelve su nombre. |
| XG-PRO-002 | productos / smoke | Código ausente devuelve indicador vacío calibrado. |
| XG-VEN-001 | ventas / regression | 2 unidades de 1000 ARS: total 2000, efectivo, venta cerrada, stock −2 y caja +2000. |
| XG-VEN-002 | ventas / regression | Cancelar no agrega venta ni altera stock/caja. |

Cada escenario inicia un JAR propio y lo cierra al terminar. Las ventas del run quedan disponibles para inspección hasta la siguiente restauración. No se borran filas ni se anulan documentos para fabricar un resultado verde.

Además de estos siete casos implementados, **XG-VEN-003 a XG-VEN-009 están planificados**: editar cantidad, código inexistente dentro de venta, vuelto, cancelar/retomar cobro, rechazar abandono y comenzar otra venta después de cobrar o abandonar. Tienen fichas detalladas, sin `.robot`; el runner no los ejecuta. Los dos recorridos consecutivos deberán mantener el mismo proceso dentro de su caso para comprobar datos residuales.

El [roadmap por etapas](docs/roadmap.md) empieza por Venta y continúa con Restobar. La [cobertura](docs/cobertura.md) separa fichas, automatización y evidencia real. El análisis del código de XGestion2 y sus 420 clases de tests aporta reglas y riesgos, no acredita 420 E2E ni equivalencia del JAR.

En el menú se elige un grupo por número y nombre descriptivo, con sus conteos. INFO resume casos/resultados; `--log-level DEBUG` añade pasos y `--log-level TRACE` diagnóstico saneado. Todos muestran fallos comprensibles, sin secretos. Ver la [guía IA](../../docs/guia-ia.md).

- [Contrato del paquete privado](docs/paquete.md)
- [Batería fija de productos, ofertas y listas — seed opcional](docs/seed.md)
- [Calibración y aceptación JAB](docs/calibracion.md)
- [Escenarios y mantenimiento](docs/escenarios.md)
- [Referencias verificadas](docs/referencias.md)
