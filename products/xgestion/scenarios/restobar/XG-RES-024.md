---
{"id":"XG-RES-024","title":"Pedir precuenta, cancelar el menú y continuar consumiendo","product":"xgestion","module":"restobar","tags":["xgestion","regression","restobar","precuenta","mesas","impresion"],"status":"planned"}
---

# XG-RES-024 — Pedir precuenta, cancelar el menú y continuar consumiendo

## Objetivo

Pedir precuenta, cancelar el menú y continuar consumiendo, desde la perspectiva del mozo, cajero o supervisor que opera el pedido.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 5.**
Referencia de planificación: **R10**. Ver [mapa de Restobar](../../docs/restobar.md).
No tiene suite Robot, seed automático ni validación real del JAR. Los resultados siguientes son criterios esperados, no resultados obtenidos.

## Precondiciones y datos

- Paquete QA sintético, Windows exclusivo y escritorio visible. La preparación de carta, mesas, ingredientes, permisos y perfiles de este caso está **pendiente**; `catalogo-comercial-v1` no certifica estos datos.
- Perfil local por defecto: ARS, comprobante interno no fiscal, impuestos y cubiertos $0 salvo indicación, sin ofertas, listas ni beneficios adicionales. Las integraciones se habilitan solo en el laboratorio indicado.
- Mesa con dos platos $1.000 cada uno, cubiertos $0; salida de precuenta QA preparada.
- Impresión física pendiente de laboratorio. Consultar precuenta no prueba un cierre.
- Preparar y registrar antes de ejecutar los IDs propios de empresa, sucursal, puesto, cuenta, mesa y productos. Mantener una operación de control ajena al caso para verificar aislamiento.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Abrir Cerrar e imprimir y cancelar el menú. | La cuenta sigue abierta por $2.000, sin cobro ni impresión. |
| Volver a abrir, elegir precuenta y confirmar su diálogo de revisión sin cobrar. | Se imprime la precuenta por $2.000 y la mesa queda lista para cobro según el perfil, con la cuenta abierta; no se cierra ni se libera. |
| Agregar una bebida $500 y emitir otra precuenta. | La nueva salida totaliza $2.500; la cuenta conserva todos los consumos. |
| Abrir de nuevo el menú y cancelarlo. | No se repite automáticamente la acción elegida en la apertura anterior. |

## Variantes y límites

Cancelar por Escape/cierre de ventana; impresora no disponible; precuenta ya emitida y eliminación con autorización RES-013. Cancelar también el diálogo de revisión de la precuenta debe evitar su salida y conservar el estado previo.

## Dependencias para automatizar

Preparar el baseline privado reproducible y sus datos, declarar el perfil, calibrar acciones accesibles sobre el SHA256 del JAR y construir comprobaciones por identidad. Utilizar atajos/acciones accesibles verificados; no tomar una posición de pantalla como identidad. Si el control o laboratorio no está disponible, mantener el caso pendiente y explicar el bloqueo.

## Evidencia y límites

Conservar UI y valores esperados/observados de cada transición. En una cuenta abierta distinguir lo guardado de lo cobrado: salir de la pantalla no es abandonar la venta. Registrar por separado **estado de cuenta, ocupación de mesa y estado de cocina** cuando apliquen.

Comparar operaciones, consumos, opciones, importes y efectos de stock/pagos por identidad y deltas según el caso, con lecturas autorizadas y saneadas. Las salidas de cocina, fiscalización y dispositivos requieren evidencia del extremo receptor; un log o test unitario no la sustituye. Registrar versión/SHA256 del JAR, commit del harness, paquete, perfil, IDs y reporte privado.

## Recuperación

Ante una discrepancia conservar primero la evidencia y cancelar o retomar por la interfaz según los pasos del caso. No borrar ni corregir registros comerciales para obtener un resultado aprobado. Restaurar el baseline QA antes de otra variante; para un cierre de resultado ambiguo conciliar la operación antes de reintentar, evitando cobrar o consumir ingredientes dos veces.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas relativas a XGestion2:

- `src/ModuloRestobar/Vistas/formTicket.java`
- `src/ModuloRestobar/Vistas/Modales/FormOpcionesCierreMesa.java`
- `test/ModuloRestobar/Vistas/Modales/SeleccionOpcionCierreMesaTest.java`

La lectura de fuente/tests orienta el riesgo y el criterio; no acredita la ejecución del artefacto. INFO resume, DEBUG describe acciones de negocio y TRACE añade diagnóstico saneado. Un fallo conserva paso, esperado, observado, categoría y evidencia; causa no determinada si falta prueba causal. No registrar credenciales, filas completas ni configuración privada.
