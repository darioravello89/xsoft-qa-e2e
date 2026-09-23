---
{"id":"XG-RES-018","title":"Crear y corregir una receta y utilizarla en el próximo pedido","product":"xgestion","module":"restobar","tags":["xgestion","regression","restobar","restobar-recetas","stock","permisos"],"status":"planned"}
---

# XG-RES-018 — Crear y corregir una receta y utilizarla en el próximo pedido

## Objetivo

Crear y corregir una receta y utilizarla en el próximo pedido, desde la perspectiva del mozo, cajero o supervisor que opera el pedido.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P1; etapa 5.**
Referencia de planificación: **Recetas**. Ver [mapa de Restobar](../../docs/restobar.md).
No tiene suite Robot, seed automático ni validación real del JAR. Los resultados siguientes son criterios esperados, no resultados obtenidos.

## Precondiciones y datos

- Paquete QA sintético, Windows exclusivo y escritorio visible. La preparación de carta, mesas, ingredientes, permisos y perfiles de este caso está **pendiente**; `catalogo-comercial-v1` no certifica estos datos.
- Perfil local por defecto: ARS, comprobante interno no fiscal, impuestos y cubiertos $0 salvo indicación, sin ofertas, listas ni beneficios adicionales. Las integraciones se habilitan solo en el laboratorio indicado.
- Supervisor QA con edición de productos permitida; PLATO-NUEVO $1.000 sin receta, harina y queso identificados. Receta actual mediante pantalla Productos/Receta, sin precios por sumatoria.
- Acceso accesible al mantenimiento de receta y guardado/rollback pendientes de calibrar.
- Preparar y registrar antes de ejecutar los IDs propios de empresa, sucursal, puesto, cuenta, mesa y productos. Mantener una operación de control ajena al caso para verificar aislamiento.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Agregar harina 0,20 kg y queso 0,05 kg a la receta y guardar. | Al reabrir se ven ambos ingredientes y sus cantidades, asociados al plato correcto. |
| Editar harina a 0,25 kg y presionar Escape sin Guardar; volver a consultar. | Permanece 0,20 kg, sin guardar el cambio descartado. |
| Editar harina a 0,25 kg y guardar; cancelar primero y luego aceptar eliminar queso. | La receta final conserva solo harina 0,25 kg; la confirmación rechazada no elimina antes de tiempo. |
| Abrir un pedido nuevo y cobrar dos platos. | Se consumen 0,50 kg de harina según la receta final; queso no se consume. |

## Variantes y límites

Operador sin permiso; cantidad vacía/no positiva debe tener criterio de validación acordado antes de habilitar la variante. Registrar como brecha si la pantalla admite un valor inválido; no aceptar silencio como validación. Cambios sobre pedidos ya abiertos requieren decisión de snapshot adicional.

## Dependencias para automatizar

Preparar el baseline privado reproducible y sus datos, declarar el perfil, calibrar acciones accesibles sobre el SHA256 del JAR y construir comprobaciones por identidad. Utilizar atajos/acciones accesibles verificados; no tomar una posición de pantalla como identidad. Si el control o laboratorio no está disponible, mantener el caso pendiente y explicar el bloqueo.

## Evidencia y límites

Conservar UI y valores esperados/observados de cada transición. En una cuenta abierta distinguir lo guardado de lo cobrado: salir de la pantalla no es abandonar la venta. Registrar por separado **estado de cuenta, ocupación de mesa y estado de cocina** cuando apliquen.

Comparar operaciones, consumos, opciones, importes y efectos de stock/pagos por identidad y deltas según el caso, con lecturas autorizadas y saneadas. Las salidas de cocina, fiscalización y dispositivos requieren evidencia del extremo receptor; un log o test unitario no la sustituye. Registrar versión/SHA256 del JAR, commit del harness, paquete, perfil, IDs y reporte privado.

## Recuperación

Ante una discrepancia conservar primero la evidencia y cancelar o retomar por la interfaz según los pasos del caso. No borrar ni corregir registros comerciales para obtener un resultado aprobado. Restaurar el baseline QA antes de otra variante; para un cierre de resultado ambiguo conciliar la operación antes de reintentar, evitando cobrar o consumir ingredientes dos veces.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas relativas a XGestion2:

- `src/ModuloProductos/Vistas/FormReceta.java`
- `src/ModuloProductos/Entidades/ProductoHijo.java`
- `src/ModuloVentas/Entidades/TicketVenta.java`

En `FormReceta.java`, líneas 48–53 vinculan Escape con cerrar sin guardar; líneas 112–124 guardan la receta y 128–132 confirman su eliminación. Esta pantalla no ofrece un botón Cancelar: la variante de descarte utiliza Escape.

La lectura de fuente/tests orienta el riesgo y el criterio; no acredita la ejecución del artefacto. INFO resume, DEBUG describe acciones de negocio y TRACE añade diagnóstico saneado. Un fallo conserva paso, esperado, observado, categoría y evidencia; causa no determinada si falta prueba causal. No registrar credenciales, filas completas ni configuración privada.
