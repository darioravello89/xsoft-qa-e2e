---
{"id":"XG-ACT-003","title":"Recuperar una actualización interrumpida sin asumir rollback ni downgrade","product":"xgestion","module":"actualizacion","tags":["xgestion","regression","actualizacion","recuperacion"],"status":"planned"}
---

# XG-ACT-003 — Recuperar una actualización interrumpida sin asumir rollback ni downgrade

## Objetivo

Reconocer que una actualización no terminó y demostrar una recuperación verificable antes de volver a usar la instalación.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P0.** Ver [continuidad operativa](../../docs/continuidad-operativa.md). Sin Robot, seed ni evidencia del JAR. Fallo de migración y recuperación del paquete completo. [BKP-002](../respaldos/XG-BKP-002.md) verifica recuperación de copia y siguiente venta; aquí se agrega el estado de schema/versiones y el reintento de migración.

## Precondiciones y datos

- Dos copias descartables de la misma VM V0 previa a ACT-001: una para fallo/reintento y otra para demostrar recuperación del snapshot. JARs V0/V1 y hashes fijos.
- Manifest V0: A = 10, H = ARS 2.000, deudas cliente 600/proveedor 400. Mecanismo de fallo limitado al schema QA: permiso faltante o interrupción en un paso identificado, preparado antes del arranque; no modificar permisos del host cotidiano.
- Lista de pasos que pueden quedar aplicados y procedimiento aprobado de reintento o recuperación completa. Inyección/observación pendientes; el DDL y el registro de migraciones no se presumen transacción reversible.
- Todos los fixtures mencionados son sintéticos y **NO están creados por esta entrega**. Faltan paquete, controles accesibles, perfiles y lectores por identidad. No escribir SQL comercial durante el recorrido ni debilitar las guardas del runner.

## Pasos y resultados esperados

| Acción del usuario o responsable QA | Resultado esperado |
| --- | --- |
| Iniciar V1 sobre la copia con el fallo controlado preparado. | Resultado fallido/incompleto reconocible, sin aceptar la base como actualizada. Registrar último paso y si hubo cambios antes del fallo. |
| Antes de vender, consultar el diagnóstico por el procedimiento QA. | QA detiene la operación hasta conocer schema y estado; no exigir que toda pantalla del ERP quede bloqueada si esa política no está verificada. |
| En la copia destinada a reintento, corregir la causa por el procedimiento aprobado y reiniciar V1. | Los pasos pendientes/fallidos convergen al estado esperado solo si la migración admite ese reintento; verificar manifest y estado completo. Sin contrato, variante bloqueada. |
| En la copia destinada a recuperación, recuperar el snapshot completo V0 sin reutilizar la base parcialmente migrada. | Paquete, configuración y base coinciden con V0; A = 10, H y deudas conservados. No basta sustituir el JAR V1 por V0. |
| Sobre la V0 recuperada, registrar una operación nueva de prueba y verificarla; después repetir actualización limpia en otra copia. | Se demuestra que V0 recuperada puede operar y que V1 puede completar desde el snapshot original. Las pruebas no comparten cambios posteriores por accidente. |

## Variantes y dependencias

- Fallo antes del primer cambio y después de un DDL requieren evidencia distinta; no declarar rollback del schema por capturar una excepción.
- Registro RUNNING abandonado, FAILED, checksum inválido y lock ocupado se preparan aparte. No marcar manualmente APPLIED para habilitar el producto.
- Sin snapshot completo comprobado, no existe ruta de recuperación demostrable y no se ejecuta la inyección.
- Downgrade in situ no está verificado ni forma parte del procedimiento; versiones antiguas nunca se prueban sobre la copia parcialmente migrada.

## Evidencia y límites

Punto del fallo, schema/estado alcanzado, versión/huella persistida y manifest antes/después. Conservar cambios parciales como evidencia; una pantalla que abre no demuestra recuperación.

Un perfil, procedimiento u oráculo faltante produce BLOQUEADO antes de la acción dependiente. Ningún resultado observado se adopta como esperado para aprobar. INFO resume y explica fallos; DEBUG muestra acciones de negocio; TRACE agrega diagnóstico saneado. Conservar paso, esperado/observado y causa no determinada si no está demostrada.

## Recuperación

Elegir la ruta previamente aprobada según el estado conocido: reintento compatible o snapshot completo en VM descartable. Si no puede verificarse, mantener la instalación fuera de operación y preservar evidencia; no borrar tablas ni estados para forzar arranque.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: commit `daa002d597d0fa7380ace204d3727085c52d1415`. Las rutas siguientes son relativas a XGestion2; las clases/tests describen reglas y riesgos, no ejecuciones E2E.

- `src/ModuloPrincipal/Entidades/DatabaseMigrationRunner.java:193-262`: intentos, estados APPLIED/FAILED y detención.
- `src/ModuloPrincipal/Entidades/JdbcDatabaseMigrationStore.java:34-41,82-131`: lock y persistencia de estado.
- `src/ModuloPrincipal/Entidades/VerificadorDeBaseDeDatos.java:234-260`: captura de fallo y resultado.
- `src/ModuloPrincipal/Vistas/AppXGestion.java:801-806` del commit citado: no actualiza ultimaVersion sin resultado completo.
- `test/ModuloPrincipal/Entidades/DatabaseMigrationRunnerTest.java`: fallo/reintento; no demuestra recuperación de VM.

Registrar SHA256/build del JAR, paquete, perfil, ámbito, IDs y reporte privado. No publicar credenciales, configuración completa, copias de bases, payloads, filas completas ni logs crudos.

