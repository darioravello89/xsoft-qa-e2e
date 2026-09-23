# Inventario y respaldos: circuitos críticos pendientes

Este mapa reúne **seis fichas planned**, cuatro de inventario y dos de respaldos. Todas tienen prioridad **P0 por integridad o recuperación**; los controles secundarios de presentación/listados son P1. No agrega automatización, seed ni validación sobre el JAR.

Consultar el [roadmap](roadmap.md), la [cobertura](cobertura.md) y los mapas de [remitos](remitos.md) y [Restobar](restobar.md). Las fichas usan datos sintéticos nuevos **NO creados**, cuyo perfil y preparación deben completarse antes de ejecutar.

## Recorridos y criterios de avance

| Ficha | Trabajo del usuario | Comprobación principal | Dependencia |
| --- | --- | --- | --- |
| [XG-INV-001](../scenarios/inventario/XG-INV-001.md) | Corregir stock con ingreso, egreso y motivo. | S1/A 10 → 13 → 11; materia prima 2,500 → 2,375 kg; cancelaciones sin movimiento. | Sucursales, permisos, controles y oráculo de ajustes. |
| [XG-INV-002](../scenarios/inventario/XG-INV-002.md) | Transferir A × 3 de S1 a S2. | Saldos 10/4 → 7/7; dos movimientos enlazados y total 14 conservado. | Transferencia directa local, estado y conciliación por ambos ámbitos. |
| [XG-INV-003](../scenarios/inventario/XG-INV-003.md) | Comenzar el año con existencias fiables. | Arrastrar 10 unidades y 2,500 kg una sola vez; reconocer cierre pendiente/inconsistente. | Baselines por año/protocolo, perfil local y lectura de aperturas. |
| [XG-INV-004](../scenarios/inventario/XG-INV-004.md) | Conciliar recepción, venta, receta y anulaciones. | Cada entrada/salida corresponde a su documento; saldos finales iguales al inicio sin errores compensados. | REM-001/003/024 y RES-014; receta fija y ruta autorizada de anulación. |
| [XG-BKP-001](../scenarios/respaldos/XG-BKP-001.md) | Crear una copia o cancelar/reintentar ante fallo. | Archivo .xbd verificable; copia anterior intacta; sin éxito falso por tamaño o mensaje. | Destino privado, manifest y verificador de integridad. |
| [XG-BKP-002](../scenarios/respaldos/XG-BKP-002.md) | Recuperar la copia y volver a vender. | Estado exacto esperado, datos posteriores ausentes y una venta nueva sin duplicación. | Procedimiento de restauración completa pendiente; VM descartable obligatoria. |

Para consultar el backlog:

```powershell
qa.cmd list --product xgestion --group inventario
qa.cmd list --product xgestion --group respaldos
```

Los grupos `stock`, `recuperacion` y `permisos` permiten cruzar riesgos. Estos IDs todavía no se ofrecen como ejecutables; una ficha pendiente no se aprueba por estar listada.

## Orden de preparación

1. Definir roles, identidades y saldos del laboratorio, cierre anual íntegro y consultas de lectura por producto/sucursal/documento. Preparar INV-001/002.
2. Habilitar recepción y receta por separado; luego unirlas en INV-004. Verificar cada delta intermedio, no solo el saldo final.
3. Preparar baselines temporales de INV-003 antes del arranque del JAR. El reloj de año no se cambia durante la ejecución y los protocolos nube quedan para un laboratorio propio.
4. Preparar manifest de datos, destino privado y verificador para BKP-001; después acordar recuperación completa para BKP-002. La generación de un archivo no autoriza ni demuestra su restauración.

No hace falta automatizar todos los reportes para comprobar estos recorridos. Sí es necesario que los controles accesibles, los datos y el oráculo del resultado estén disponibles. Un requisito faltante se informa como bloqueo y no como defecto confirmado.

## Reglas verificadas y límites

**Ajustes.** La pantalla exige producto, cantidad y motivo, confirma antes de guardar y acepta hasta tres decimales. Su rango es 0 a 9.999.999,999 para la cantidad y ±9.999.999,999 para el stock final. Cero y saldo negativo dentro del rango no están rechazados por la validación revisada. El criterio de registrar un ajuste de cero queda pendiente; no trasladar las restricciones de una venta a esta pantalla.

**Transferencias.** El origen y destino deben ser válidos y diferentes. La confirmación marca el documento cerrado y llama a salida y entrada; la fuente inspeccionada corresponde a transferencia directa. No se inventan estados «en tránsito» o «recibido por otra PC». Deben conciliarse ambos lados incluso si la ventana se cierra, y la atomicidad ante un fallo requiere comprobarse.

**Cierre anual.** La ruta local verifica aperturas y marcador; al repetir un cierre íntegro no debe duplicar existencias. Si falta un cierre previo reconocido, la recuperación exige soporte. Las funciones de stock pueden quedar temporalmente indisponibles, mientras ventas/recepciones continúan según el comportamiento declarado por el ERP: no afirmar un bloqueo general ni stock conocido. El protocolo de nube tiene sincronización y dependencias distintas del laboratorio offline.

**Recetas y anulaciones.** Separar producto padre, ingredientes y extras. El circuito básico usa receta fija sin extras; una devolución de receta no acredita extras ni una receta modificada después de vender. Conservar los riesgos de [RES-015](../scenarios/restobar/XG-RES-015.md) y comprobar que un padre no stockeable no recibe un ingreso indebido. Anular una compra no se utiliza como sustituto de restaurar el baseline.

**Respaldo e importación.** Existen Backup Datos, Exportar BD y COMENZAR para exportar .xbd, y **Importar BD** para ingresar esos datos. El importador hace upserts por tabla/lotes: no elimina por ese mecanismo los registros posteriores a la copia ni demuestra rollback completo al cancelar. **Importar sobre una base existente no acredita restaurarla exactamente.** BKP-002 exige un procedimiento aún pendiente para preparar/verificar el destino, sin inventar un botón Restaurar ni comandos destructivos.

Además, el exportador puede capturar errores de lectura por tabla y continuar. El mensaje de exportación o la fecha del último backup son evidencia insuficiente; verificar cobertura del manifest y recuperación posterior. Los errores del importador pueden incluir filas de datos: conservar logs crudos privados y sanear el diagnóstico antes de mostrarlo.

## Datos y evidencia

Los códigos QA-INV, documentos, ingredientes, sucursales y copias descritos son especificaciones de fixtures nuevos. Esta entrega no reserva IDs ni crea upserts. No asumir que los 387 productos del seed comercial ya cubren inventario, receta o restauración.

Cada ejecución futura registrará JAR/SHA256, paquete, perfil, ámbito, baseline, pasos, esperado/observado y reporte local. En inventario, verificar movimientos por identidad y unidad; en recuperación, comparar manifest, vínculos y la siguiente operación. Nunca publicar dumps, .xbd, contenido descifrado, credenciales, capturas de autenticación o filas completas.

INFO resume casos y explica fallos; DEBUG muestra acciones de negocio; TRACE aporta diagnóstico saneado. La validación del catálogo y los tests unitarios fuente no equivalen a E2E real. Una variante con procedimiento/oráculo pendiente no se contabiliza como aprobada.

## Trazabilidad

Fuente ERP inspeccionada: commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Cada ficha incluye rangos específicos. Referencias principales:

- `src/ModuloStocks/Vistas/FormStockAjuste.java:89-108,210-253` y `test/ModuloStocks/Vistas/FormStockAjusteValidationTest.java`.
- `src/ModuloStocks/Vistas/FormNuevaTransferencia.java:440-480`; `src/ModuloProductos/Entidades/Compra.java:539-595`; `CompraDetalle.java:277-365`.
- `src/ModuloProductos/Entidades/CierreAnualStocks.java:36-74,155-192`; `src/ModuloProductos/Servicios/CierreAnualStockService.java:157-255,470-489` y tests de cierre local/previo.
- `src/ModuloVentas/Entidades/TicketVenta.java:526-562,3285-3312`; `src/ModuloProductos/Entidades/ProductoHijo.java:28-45,83-101`.
- `src/ModuloConfiguracion/Entidades/DatabaseBackup.java:28-69`; `src/ModuloConfiguracion/Vistas/FormMiSucursal.java:541-626`.
- `src/Integraciones/SincronizacionManual/SincronizacionManualService.java:87-171,173-213,238-305`.

Este mapa documenta alcance y riesgos comprobados por lectura; no modifica el ERP, bases, permisos del equipo, snapshots ni las guardas de ejecución.

