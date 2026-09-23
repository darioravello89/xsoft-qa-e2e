---
{"id":"XG-BKP-001","title":"Generar un respaldo y distinguir cancelación, fallo y copia verificable","product":"xgestion","module":"respaldos","tags":["xgestion","regression","respaldos","recuperacion","permisos"],"status":"planned"}
---

# XG-BKP-001 — Generar un respaldo y distinguir cancelación, fallo y copia verificable

## Objetivo

Guardar una copia de los datos del laboratorio, conocer cuándo terminó o falló y conservar una copia anterior utilizable sin confundir un mensaje de éxito con recuperación probada.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P0; recuperación, etapa 6.** Ver [mapa](../../docs/inventario-respaldos.md). Exportación local de archivo .xbd; no subir copias a servicios externos. El indicador «Último backup» y la claridad del resultado son comprobaciones P1, insuficientes para acreditar integridad.

## Precondiciones y datos

- VM Windows QA descartable, offline, JAR/paquete identificados; base exclusivamente sintética y sin escritores concurrentes durante la captura.
- **Fixtures nuevos, NO creados:** A con stock 10, una venta interna cerrada por ARS 2.000, un cliente QA y un remito QA. Manifest de evidencia pendiente con identidades, estados, conteos y saldos conocidos; no copiar filas completas al reporte público.
- Carpeta de salida QA privada dentro de la VM, inicialmente sin el archivo nuevo; copia anterior de control con hash conocido. Nombre propuesto `qa-respaldo-001`, normalizado a .xbd.
- Último respaldo registrado en una fecha previa del laboratorio. Preparar usuario autorizado y permiso de rol restringido; no se ha verificado un permiso independiente del botón.
- Perfil de carpeta no escribible e inyección de error de lectura pendientes, limitados a carpetas/base propias de esta VM. No modificar ACL ni servicios del host habitual.

## Pasos y resultados esperados

| Acción del usuario | Resultado esperado |
| --- | --- |
| Abrir Backup Datos y cancelar el selector de destino. | Informa que no se realizará el respaldo en esta ruta; no crea el archivo nuevo ni modifica la fecha del último backup. |
| Reabrir, elegir un nombre nuevo sin extensión y guardar en la carpeta autorizada. | Crea `qa-respaldo-001.xbd`; informa exportación finalizada con ese destino. No altera la copia anterior. |
| Consultar el último backup después de reabrir su pantalla. | Corresponde al día de la exportación terminada; este dato no acredita por sí solo que la copia sea recuperable. |
| Registrar tamaño/hash del archivo y contrastar su contenido con el manifest mediante el verificador privado que se prepare. | Archivo no vacío y conjunto de datos esperado completo. Si falta el verificador, esta comprobación queda bloqueada; no aprobar por tamaño, extensión o mensaje. |
| Desde baseline, repetir con un destino nuevo no escribible. | Informa error, no éxito; conserva la fecha previa y la copia anterior. Un archivo parcial, si queda, no se considera respaldo válido. |
| Corregir solo el destino y reintentar con otro nombre nuevo. | Genera una copia verificable; el fallo previo conserva su evidencia y no produce datos comerciales nuevos. |

## Variantes y dependencias

- Nombre ya terminado en .xbd: no duplicar extensión. La sobrescritura de un archivo existente necesita política confirmada; el caso base siempre usa nombre nuevo.
- Repetir por Exportar BD de Mi Sucursal y COMENZAR de la pantalla BackUp una vez calibradas: comparten exportador, pero cancelar el selector no necesariamente muestra el mismo mensaje.
- Error al leer una tabla: preparar fallo controlado en el laboratorio; **no aceptar una copia incompleta como recuperación válida**, aunque la pantalla anuncie exportación. La fuente captura errores de lectura por tabla y puede continuar; es un riesgo identificado, no un fallo ejecutado.
- Cierre/cancelación durante la exportación: no se verificó un control de cancelación de trabajo en curso. No inventar ese botón ni matar procesos para simular una cancelación exitosa.
- Rol restringido, volumen grande, espacio insuficiente y bases con varias empresas necesitan perfiles/oráculos propios. La exportación revisada recorre tablas de la base, no solo la empresa visible.

## Evidencia y límites

Conservar acción, mensaje, destino relativo QA, tamaño, hash y resultado de la verificación; fecha anterior/posterior. El .xbd, cualquier contenido descifrado y los logs del ERP permanecen privados. La recuperación completa se acredita en [BKP-002](XG-BKP-002.md), no con una exportación terminada.

## Recuperación

Preservar el respaldo anterior y el archivo fallido para diagnóstico privado; no reemplazar la única copia conocida. Ante error, corregir el requisito del laboratorio y usar otro destino. La limpieza solo elimina archivos propios según el procedimiento QA, después de conservar evidencia.

## Anexo técnico y trazabilidad

Fuente ERP: commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`.

- `src/ModuloConfiguracion/Vistas/FormOpciones.java:2325-2332`: botón Backup Datos.
- `src/ModuloConfiguracion/Entidades/DatabaseBackup.java:28-69`: cancelar, normalización .xbd, error y registro de fecha posterior a exportar.
- `src/ModuloPrincipal/Vistas/Dialogs/FormBackUp.java:55-74,89-98,116-126`: COMENZAR y resultado.
- `src/ModuloConfiguracion/Vistas/FormMiSucursal.java:522-538`: Exportar BD.
- `src/Integraciones/SincronizacionManual/SincronizacionManualService.java:87-99,173-213`: contenido, cifrado, escritura y lectura por tabla.

Selectores y verificador de integridad pendientes. Registrar SHA256 del JAR, paquete/perfil y reporte saneado. INFO/DEBUG/TRACE nunca publican contenido de copias, credenciales ni filas de datos.

