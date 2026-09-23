---
{"id":"XG-ACT-001","title":"Abrir una versión nueva sobre una copia de la base anterior","product":"xgestion","module":"actualizacion","tags":["xgestion","regression","actualizacion","recuperacion"],"status":"planned"}
---

# XG-ACT-001 — Abrir una versión nueva sobre una copia de la base anterior

## Objetivo

Actualizar una instalación QA con datos existentes y comprobar que puede consultar su negocio y realizar una operación nueva.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P0.** Ver [continuidad operativa](../../docs/continuidad-operativa.md). Sin Robot, seed ni evidencia del JAR. Actualización de versión sobre copia anterior, no instalación limpia. [BKP-001](../respaldos/XG-BKP-001.md) y [BKP-002](../respaldos/XG-BKP-002.md) cubren creación/recuperación de copias; este caso comienza con una copia restaurada y comprobada.

## Precondiciones y datos

- VM Windows QA descartable offline. Par de versiones origen V0/destino V1, FAT JARs, hashes, motor y schema compatibles pendientes de identificar; no usar «última versión» como requisito móvil.
- Copia sintética de V0 con A a ARS 1.000, stock 10, venta histórica H por ARS 2.000, cliente con deuda ARS 600 y proveedor con deuda ARS 400. Manifest de identidades, saldos y documentos previo a actualizar.
- Lista aprobada de cambios de schema/datos esperados para V0→V1 y procedimiento de sustitución del paquete en la copia, conservando licencia/configuración QA compatibles. Sin escritores ni sincronización durante actualización.
- Snapshot completo anterior recuperable y verificado; no basta el archivo .xbd para asumir recuperación de paquete/configuración.
- Todos los fixtures mencionados son sintéticos y **NO están creados por esta entrega**. Faltan paquete, controles accesibles, perfiles y lectores por identidad. No escribir SQL comercial durante el recorrido ni debilitar las guardas del runner.

## Pasos y resultados esperados

| Acción del usuario o responsable QA | Resultado esperado |
| --- | --- |
| Antes de actualizar, abrir V0 y contrastar el manifest; cerrar el producto. | Documentos y saldos de referencia conocidos, sin operaciones pendientes de guardar. |
| Aplicar el paquete V1 por el procedimiento preparado e iniciar el JAR en la copia. | Se ejecutan/verifican los cambios previstos para esa base; no se considera lista solo porque abrió la pantalla principal. |
| Esperar resultado íntegro del verificador antes de operar y consultar históricos/saldos. | Sin migración fallida ni pendiente requerida; A = 10, H = ARS 2.000, deudas cliente 600/proveedor 400. Los cambios técnicos autorizados no alteran esos valores comerciales. |
| Crear una venta nueva de A × 1 y cobrar ARS 1.000. | Una venta/cobro nuevos, stock 9; identidades sin conflicto con el histórico H. Las deudas previas no cambian. |
| Cerrar y volver a abrir la instalación V1. | Se conserva la operación nueva y continúa consultable H; no se vuelven a crear datos por abrir el programa. |

## Variantes y dependencias

- Base sin registro previo de migraciones y base con migraciones registradas requieren perfiles propios; no elegir manualmente estados APPLIED para saltar pasos.
- Actualización de una base con varias empresas exige manifest y verificación por todas las incluidas; no inferir cobertura del caso E1.
- Cambio de JAR con la misma versión declarada y cambio de versión son estímulos distintos: registrar huella y ruta de verificación.
- Instalación limpia, actualización automática por red y versiones no compatibles quedan fuera.

## Evidencia y límites

Versiones/hashes de ambos paquetes, snapshot previo, resultado del verificador, migraciones requeridas y manifest comercial antes/después. Revisar efectos autorizados en schema por separado de los saldos; no exigir igualdad binaria de la base.

Un perfil, procedimiento u oráculo faltante produce BLOQUEADO antes de la acción dependiente. Ningún resultado observado se adopta como esperado para aprobar. INFO resume y explica fallos; DEBUG muestra acciones de negocio; TRACE agrega diagnóstico saneado. Conservar paso, esperado/observado y causa no determinada si no está demostrada.

## Recuperación

Si el verificador falla o quedan requisitos pendientes, QA detiene las operaciones. Preservar copia fallida y diagnóstico; recuperar snapshot completo según el procedimiento demostrado en ACT-003, sin ejecutar V0 contra una base parcialmente migrada.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: commit `daa002d597d0fa7380ace204d3727085c52d1415`. Las rutas siguientes son relativas a XGestion2; las clases/tests describen reglas y riesgos, no ejecuciones E2E.

- `src/ModuloPrincipal/Vistas/AppXGestion.java:778-809` del commit citado, leído con `git show`: esquema mínimo, versión y resultado completo antes de persistir ultimaVersion.
- `src/ModuloPrincipal/Entidades/VerificadorDeBaseDeDatos.java:198-260`: ejecución y resultado.
- `src/ModuloPrincipal/Entidades/DBVerifyScheduler.java:153-188`: cambio de versión y verificación pendiente.
- `test/ModuloPrincipal/Entidades/VerificadorDeBaseDeDatosArranqueTest.java`, `DatabaseMigrationRunnerTest.java` y `DBVerifySchedulerPolicyTest.java`.

Registrar SHA256/build del JAR, paquete, perfil, ámbito, IDs y reporte privado. No publicar credenciales, configuración completa, copias de bases, payloads, filas completas ni logs crudos.

