# Especificación 001 — Plataforma local de QA E2E

Fecha: 2026-09-19. Estado: alcance acordado; aceptación sobre aplicaciones reales pendiente.

## Objetivo

Un QA debe poder instalar requisitos, importar su entorno privado y ejecutar pruebas por producto, grupo o escenario sin programar. La IA local ayuda a operar y ampliar casos a partir de documentación versionada. El repositorio mantiene automatización y documentación juntas, con evidencia que distinga validación técnica de QA real.

## Primera entrega

- Plataforma operativa inicial: Windows exclusivo de QA, Python 3.12 x64, Java 17 x64 y XGestion JAR `2.02.189-lts`.
- Casos iniciales: login inválido/válido, consulta de producto conocido/no encontrado, cancelación sin persistencia y venta en efectivo de dos unidades de un producto a ARS 1000.00 cada una, total ARS 2000.00, sin fiscal ni impresión. El catálogo ejecutable es la fuente de IDs y agrupación.
- Aserciones de venta: total esperado y persistencia de venta, stock y caja mediante lecturas acotadas a los identificadores del fixture. Los datos se preparan mediante baseline privado.
- Ejecución serial con entorno exclusivo. XGestion corre con la red de Windows desconectada; la IA puede estar online en el host de la VM. No RDP ni escritorio bloqueado.
- MySQL portable `5.7.44` en instancia privada, `127.0.0.1:13317`, base `xsoft_qa`. El aislamiento debe abarcar la instancia porque el ERP puede ejecutar `SET GLOBAL`.

## Interfaces y estructura

`qa.cmd` ofrece menú y comandos `setup`, `doctor`, `list`, `run`, `report`, `check`, `inspect` y `calibrate`. `run` filtra por `--product`, `--group` o `--scenario`; `--dry-run` valida sin lanzar aplicaciones ni conectarse a servicios. `calibrate` importa selectores verificados para el hash del JAR actual y conserva un respaldo local.

`products/<producto>/{scenarios,suites,resources,docs}` encapsula cada producto. Los adaptadores y oráculos Python pertenecen al directorio del producto. Los casos Markdown llevan frontmatter JSON con ID, título, producto, módulo, tags, estado y archivo de test; el validador verifica coherencia. Robot conserva los IDs y grupos como tags.

El archivo `test` se exige para `implemented`; `planned` y `manual` documentan casos no ejecutables. `groups.json` registra ID/tag, nombre descriptivo, propósito y etapa por producto. El catálogo calcula conteos separados de implementados/planificados/manuales, sin sumar dos veces un caso por pertenecer a distintos grupos.

El paquete privado tiene manifiesto con hashes del JAR, dump saneado, MySQL portable, configuración legítima de QA, credenciales, fixtures y selectores calibrados. `.env.local` y `.local/xgestion/` son locales e ignorados. La restauración solo puede operar sobre el perfil propio cuya ubicación y propiedad valida el runner.

## Productos siguientes

XPORTAL y Consultador web quedan `planned`, con URLs locales `XPORTAL_BASE_URL` y `CONSULTADOR_BASE_URL`. Su motor previsto es Robot Framework Browser sobre Playwright. Mozos es una app Flutter separada, con Maestro Android previsto. No se presume que el repositorio Angular XMozo sea esa app ni se agrega cobertura ficticia.

## Aceptación

El framework debe pasar lint Python/Robot, tests propios, validación del catálogo y dry-run sin datos privados. Para acreditar QA del producto se exige paquete real, prueba técnica del bridge/controles, onboarding en Windows limpio y tres ejecuciones consecutivas de los escenarios iniciales con resultados y estado final verificados.

No están incluidos facturación fiscal, impresoras/comandas, integraciones externas, producción, CI de escritorio ni cambios en código de los productos. Cada ampliación debe explicitar sus datos, efectos y criterios de aceptación.

## Evolución aprobada — cobertura y ejecución comprensible

El alcance de esta ampliación es documentación, grupos, menú y logs de los **siete casos existentes**. No implementa nuevos recorridos GUI ni modifica XGestion. Se agregan siete fichas `planned`, XG-VEN-003 a XG-VEN-009, en el orden de la [etapa 1](../../products/xgestion/docs/roadmap.md); las siete originales conservan identidad y automatización. VEN-001 suma tags `efectivo` y `cobros` sin quitar los previos.

El roadmap completo tiene etapas 0 Preparación y ejecución comprensible, 1 Venta cotidiana, 2 Productos y condiciones comerciales, 3 Cobros y documentos, 4 Después de vender, 5 Restobar y 6 Integraciones y laboratorio ampliado. Solo la primera ampliación de Venta se detalla paso a paso. Restobar R01–R20 es backlog fuera del catálogo; los tests del ERP son insumo, no E2E.

Contratos de operación:

- `qa.cmd list --product xgestion --groups`: grupos descriptivos, etapa y conteos por estado.
- `qa.cmd list --product xgestion --group ventas`: casos de una familia, incluidos los pendientes. `--groups` y `--group` son alternativas.
- Menú numérico con nombres legibles y conteos; selección de grupo y nivel de detalle. Grupos pendientes visibles sin ofrecer ejecución.
- `qa.cmd run --product xgestion --group ventas --log-level INFO|DEBUG|TRACE`: INFO predeterminado, sin cambiar las aserciones por el nivel. Elegir un único valor al ejecutar, por ejemplo `--log-level DEBUG`.
- INFO: caso/resultado/resumen; DEBUG: pasos/comprobaciones; TRACE: diagnóstico saneado. En todos los niveles, fallos con paso, esperado, observado, categoría y evidencia; causa no determinada cuando no pueda demostrarse.
- `report.html` es el resumen oficial del runner con estado global, grupos y fallos; `robot-report.html` y `log.html` son detalle parcial de Robot y pasos, generados desde XML saneado. Un éxito parcial de Robot no oculta fallos de preparación o cierre.

Aceptación técnica de la ampliación: catálogo 7 implementados + 7 planificados, ninguna suite Robot nueva, filtros/conteos/menú correctos, casos actuales y nivel INFO compatibles, sanitización validada con canarios, errores visibles y controles técnicos aprobados. La aceptación real del JAR permanece separada y pendiente hasta completar el protocolo privado.
