# XGestion: primeras pruebas automatizadas

Los [circuitos completos](docs/circuitos-completos.md) incorporan FIN-011/013/014:
venta USD, recepción con costos/precios y cierre de caja. FIN-012 queda pendiente
por ACC-010, sin doble clic autorizado. Ver la [primera ejecución](../../docs/primera-ejecucion-circuitos.md).

Esta suite ejecuta el JAR Windows mediante Java Access Bridge y valida lo observado en pantalla. Las ventas se contrastan con consultas SQL de lectura sobre la instancia QA local. No invoca métodos internos de negocio ni usa el checkout del ERP.

**Estado: implementación inicial; ejecución GUI real pendiente.** Los ejemplos de localizadores son borradores y bloquean ejecución. Un QA responsable debe preparar el paquete privado, calibrar contra el JAR exacto y aprobar el recorrido en la VM aislada. Un `dryrun` verde sólo valida estructura Robot.

Comenzar por el [quick start general](../../README.md). Después:

```powershell
qa.cmd list --product xgestion
qa.cmd list --product xgestion --groups
qa.cmd list --product xgestion --group ventas
qa.cmd list --product xgestion --group promociones
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
| XG-VEN-003 | ventas / corregir-venta | Editar cantidad de la misma línea de 1 a 2 cambia total de 1000 a 2000; abandonar no persiste. |
| XG-VEN-004 | ventas / carga-productos | El aviso calibrado de código ausente conserva la venta; otro código válido sigue funcionando. |
| XG-VEN-005 | ventas / efectivo | Recibido 3000, vuelto 1000 y una venta por 2000; stock −2 y caja neta +2000. |
| XG-VEN-006 | ventas / efectivo / cobros | Cancelar no persiste; retomar registra un solo cobro. |
| XG-VEN-007 | ventas / corregir-venta | Rechazar el abandono conserva la venta y permite editarla y cobrarla una sola vez. |
| XG-VEN-008 | ventas / regression | Después de cobrar, la misma ventana queda limpia para la siguiente operación. |
| XG-VEN-009 | ventas / regression | Después de abandonar, otra venta en la misma sesión comienza limpia. |
| XG-PRM-001 | promociones / regression | Descuento del 10 %: cantidad 1 → 3, total 900 → 2700 ARS. |
| XG-PRM-002 | promociones / regression | Descuento de 150 ARS por unidad: cantidad 1 → 3, total 850 → 2550 ARS. |
| XG-PRM-003 | promociones / regression | 2x1: cantidad 1 → 3, total 1000 → 2000 ARS. |
| XG-PRM-004 | promociones / regression | Segunda unidad al 50 %: cantidad 1 → 3, total 1000 → 2500 ARS. |
| XG-PRM-005 | promociones / regression | Oferta vencida: cantidad 2 → 1, sin descuento; total 2000 → 1000 ARS. |
| XG-PRM-006 | promociones / regression | Oferta futura: cantidad 2 → 1, sin descuento; total 2000 → 1000 ARS. |
| XG-PRM-007 | promociones / regression | Oferta inactiva: cantidad 2 → 1, sin descuento; total 2000 → 1000 ARS. |

Cada escenario inicia un JAR propio y lo cierra al terminar. Las ventas del run quedan disponibles para inspección hasta la siguiente restauración. No se borran filas ni se anulan documentos para fabricar un resultado verde.

Los [atajos de 13 listados](docs/atajos-automatizacion.md) están codificados y seleccionables, con validación real JAB pendiente.

El catálogo tiene **315 fichas: 112 implementadas —cinco de smoke, nueve de ventas, 82 de promociones, tres circuitos y 13 de atajos— y 203 pendientes**. Consultar el [mapa de ofertas por fórmula y alcance](docs/promociones-pendientes.md): PRM-008..076 y PRM-079 tienen recorridos automatizados; PRM-077/078 esperan el paquete de varios contextos. Las 50 fichas del [complemento crítico](docs/complementos-criticos.md) amplían cobros/documentos, servicios, continuidad y beneficios. Las 58 fichas del [roadmap de circuitos críticos](docs/circuitos-criticos.md) detallan cuentas corrientes, cuotas, Libro Diario, caja, conciliación, inventario y respaldos, todas pendientes de automatizar. Las 92 fichas de [remitos de compra](docs/remitos.md), [Restobar y recetas](docs/restobar.md) y [listas de precios](docs/listas-precios.md) están planificadas, con datos/calibración y automatización pendientes. XG-VEN-003/007 usan botón, cancelación y `Ctrl+E` sólo cuando el paquete declara `ventas-teclado-v1`, verificado para su SHA256; mientras tanto conservan el doble clic legado. El [backlog de accesibilidad CSV](docs/backlog-accesibilidad.csv) deja XG-ACC-001 a XG-ACC-005 como implementados pendientes de validación JAR/JAB. Las mejoras 002–005 pertenecen a Restobar y no cuentan como escenarios ni como cobertura de Venta.

Los siete recorridos VEN-003 a VEN-009 requieren `sales_journeys` y el mapa de columnas/controles de [Venta cotidiana](docs/paquete.md), validados antes de iniciar el JAR. Un paquete con el contrato anterior conserva los siete casos iniciales, pero no habilita esos recorridos. VEN-008/009 mantienen el mismo proceso entre operaciones; VEN-008 observa el reinicio automático de la misma ventana. Ninguno tiene todavía validación real registrada.

Los siete casos iniciales de promociones requieren el [perfil y calibración de promociones](docs/promociones.md), con `promociones-v1`, `ventas-etapa1` y `ventas-teclado-v1` verificados para el SHA256 del JAR. El runner prepara automáticamente `catalogo-comercial-v1` cuando un grupo, ID o selección del menú lo requiere; también acepta `--seed catalogo-comercial-v1`. El perfil es ARS, comprobante interno 99, efectivo exacto, Ninguna Lista (ID 0), cliente/turno sin listas, otros descuentos en cero y fidelización deshabilitada. No cambiar la configuración desde el test para permitir su ejecución.

Cada promoción compara producto, cantidad, precio base, subtotal bruto, descuento y neto antes y después de editar con `Ctrl+E`; cancela el cobro sin persistencia y luego registra una sola venta con stock/caja coherentes. Los tres casos de oferta no aplicable comprueban primero una promoción válida de control y la abandonan sin efectos. Ejecutar `qa.cmd run --product xgestion --group promociones --log-level DEBUG` en el laboratorio preparado. La existencia de estos siete casos no valida las demás variantes del seed ni acredita ejecución real.

El efectivo simple se contrasta con `Pagado`/`Vuelto` en `ventas` y el ingreso por el total aplicado en caja; no exige filas en `ventas_pagos`, que corresponde a otros flujos de cobro.

El [roadmap por etapas](docs/roadmap.md) empieza por Venta y continúa con Restobar. La [cobertura](docs/cobertura.md) separa fichas, automatización y evidencia real. El análisis del código de XGestion2 y sus 420 clases de tests aporta reglas y riesgos, no acredita 420 E2E ni equivalencia del JAR.

En el menú se elige un grupo por número y nombre descriptivo, con sus conteos. INFO resume casos/resultados; `--log-level DEBUG` añade pasos y `--log-level TRACE` diagnóstico saneado. Todos muestran fallos comprensibles, sin secretos. Ver la [guía IA](../../docs/guia-ia.md).

- [Remitos de compra: mapa y variantes](docs/remitos.md)
- [Restobar: opciones, recetas y recorridos](docs/restobar.md)
- [Listas de precios: origen, prioridad y variantes](docs/listas-precios.md)
- [Roadmap de circuitos críticos e integridad](docs/circuitos-criticos.md)
- [Cuentas corrientes de clientes/proveedores y cuotas](docs/cuentas-corrientes.md)
- [Libro Diario, arqueo y cierre de caja](docs/libro-diario-caja.md)
- [Inventario y recuperación de respaldos](docs/inventario-respaldos.md)
- [50 escenarios complementarios y orden de avance](docs/complementos-criticos.md)
- [Cobros combinados, presupuestos y devoluciones](docs/cobros-documentos.md)
- [Facturación electrónica y pagos externos](docs/facturacion-pagos-externos.md)
- [Interrupciones, concurrencia y actualización](docs/continuidad-operativa.md)
- [Beneficios, puntos e impuestos](docs/beneficios-impuestos.md)
- [Contrato del paquete privado](docs/paquete.md)
- [Batería fija de productos, ofertas y listas — seed opcional](docs/seed.md)
- [Canastas de ofertas: 70 recorridos, listas, pagos y perfiles](docs/canastas-ofertas.md)
- [Calibración y aceptación JAB](docs/calibracion.md)
- [Mapa de teclado y nombres accesibles](docs/mapa-accesibilidad.md)
- [Escenarios y mantenimiento](docs/escenarios.md)
- [Referencias verificadas](docs/referencias.md)

## Ofertas USD — P0

[XG-PRM-080..084](docs/ofertas-usd.md) agregan cinco casos con trece variantes, datos USD y comprobaciones de moneda, total, cobro único y persistencia. Seleccionar `ofertas-usd`. Exigen calibración `ofertas-usd-v1`, cotización 1500 y cobro ARS; no reutilizar los importes ARS como si fueran USD. Validación real pendiente.

## Atajos de listados

[KEY-001..013](docs/atajos-listados.md): 13 escenarios documentados,
ninguno automatizado ni ejecutado todavía. Ver [artefacto/hash y evidencia
por pantalla](docs/evidencia-atajos-3f8648035.md).
`qa.cmd list --product xgestion --group atajos-listados` muestra el backlog;
`filtros-listados` reúne las ocho pantallas con modal.
