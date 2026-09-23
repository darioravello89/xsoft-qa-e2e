---
{"id":"XG-BKP-002","title":"Recuperar una copia en una VM descartable y volver a operar","product":"xgestion","module":"respaldos","tags":["xgestion","regression","respaldos","recuperacion","permisos"],"status":"planned"}
---

# XG-BKP-002 — Recuperar una copia en una VM descartable y volver a operar

## Objetivo

Comprobar que una copia permite recuperar el estado acordado del negocio y realizar la siguiente operación sin duplicar documentos ni arrastrar datos posteriores.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P0; recuperación, etapa 6.** Ver [mapa](../../docs/inventario-respaldos.md). **El procedimiento de restauración completa está pendiente de definir y verificar.** La UI existente se llama Importar BD: combina registros por identidad y no demuestra una restauración exacta. No se inventa un botón «Restaurar».

## Precondiciones y datos

- Dos VMs QA descartables o snapshots equivalentes, con identidades/rutas propias verificadas, completamente offline. Ninguna base cotidiana, de producción o compartida puede ser destino.
- Copia .xbd obtenida y verificada en [BKP-001](XG-BKP-001.md), hash y manifest privados. Versiones compatibles del JAR, schema y motor; cierre anual consistente.
- **Fixtures sintéticos nuevos, NO creados:** en la copia, A stockeable a ARS 1.000 con stock 10, venta V1 cerrada por ARS 2.000 y recibo asociado; B = 20 como control. Después de la copia, preparar en el destino una venta V2 por una unidad de A, de modo que A = 9. V2 es el control de datos posteriores.
- Procedimiento reproducible pendiente que defina preparación del destino, archivos/configuración requeridos, orden de importación, reinicio y verificación. El archivo de datos no se presume copia de licencia, JAR o configuración local.
- Identificar rol autorizado, controles accesibles y oráculo de comparación por identidad. La documentación actual no habilita una restauración ni permite omitir las guardas del runner.

## Pasos y resultados esperados

| Acción del usuario/responsable QA | Resultado esperado |
| --- | --- |
| Revisar destino, hash, manifest y procedimiento aprobado para recuperación completa. | Si falta cualquiera, informar BLOQUEADO antes de importar. No sustituirlo por una importación sobre la base que contiene V2. |
| En la VM descartable preparada, ejecutar el procedimiento de recuperación acordado, usando Importar BD solo si ese procedimiento lo requiere. | El estado recuperado coincide con la copia: V1 y recibo presentes, A = 10, B = 20 y V2 ausente. Si V2 permanece, no se logró una restauración exacta. |
| Reiniciar XGestión y acceder con el perfil QA del destino. | Empresa/sucursal/puesto correctos; los documentos y saldos se pueden consultar sin repetir movimientos. |
| Abrir una venta nueva de A × 1, cancelar cobro, retomarlo y cobrar ARS 1.000. | Una nueva venta/cobro con identidad no conflictiva; A = 9, B = 20. V1 no cambia ni se cobra otra vez. |
| Reiniciar y consultar la nueva venta y existencias. | Persisten los mismos documentos, saldos y vínculos; no aparecen duplicados tras volver a operar. |

## Variantes y dependencias

- **Caracterización de Importar BD, en otra VM descartable:** importar la copia sobre el destino con V2 conserva registros posteriores que no comparten identidad. Ese resultado confirma la combinación de datos, pero no aprueba el objetivo de restauración exacta. No convertirlo en «restauración exitosa».
- Cancelar el selector antes de iniciar: ningún cambio. Archivo corrupto o formato inválido: error, sin mensaje de importación completada; verificar estado antes de reintentar.
- Cancelar durante la importación o fallar después de un lote: puede haber cambios parciales. La fuente muestra lotes/upserts y no acredita rollback de toda la importación; descartar la VM afectada y repetir desde destino limpio, nunca continuar ventas en estado ambiguo.
- Copia de otra empresa/versión o manifest incompleto: la comprobación del procedimiento QA debe detener el intento. No asumir que el producto ya valida estos casos.
- Comparar todos los registros comerciales del fixture, no solo stock y V1. El verificador completo y el tratamiento de secuencias/identidades son requisitos pendientes; hasta implementarlos la ficha no puede aprobarse.

## Evidencia y límites

Registrar hash de la copia, perfil/schema/build del destino, manifest esperado/observado, ausencia de V2 y la operación nueva con sus deltas. Mensaje «Importación completada» o progreso 100 % no demuestra recuperación íntegra. No publicar copias, filas, credenciales ni logs crudos: el importador puede incluir datos de filas al fallar.

## Recuperación

Al cancelar o fallar, conservar diagnóstico saneado y descartar/revertir únicamente la VM QA afectada mediante el procedimiento autorizado. Mantener intacta la copia fuente. No reparar la base parcialmente importada a mano ni reimportar en bucle hasta que el mensaje cambie a éxito.

## Anexo técnico y trazabilidad

Fuente ERP: commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`.

- `src/ModuloConfiguracion/Vistas/FormMiSucursal.java:165-175,541-626`: botón Importar BD, progreso, cancelación y resultado.
- `src/Integraciones/SincronizacionManual/SincronizacionManualService.java:101-171,238-305`: lectura, importación por tabla, upserts/lotes y cancelación.
- `SincronizacionManualService.java:285-293`: riesgo de datos de filas en mensajes de error; saneamiento antes del reporte QA.
- `src/ModuloConfiguracion/Entidades/DatabaseBackup.java:48-69`: generación y fecha del respaldo, sin procedimiento de recuperación completa.

La ficha documenta un objetivo de recuperación y sus dependencias. No agrega comandos destructivos, importaciones automáticas ni lógica de restauración al framework.

