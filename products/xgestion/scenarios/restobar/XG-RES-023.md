---
{"id":"XG-RES-023","title":"Enviar nuevas rondas y reimprimir sin duplicar consumos","product":"xgestion","module":"restobar","tags":["xgestion","regression","restobar","mesas","preparacion","kds","impresion"],"status":"planned"}
---

# XG-RES-023 — Enviar nuevas rondas y reimprimir sin duplicar consumos

## Objetivo

Enviar nuevas rondas y reimprimir sin duplicar consumos, desde la perspectiva del mozo, cajero o supervisor que opera el pedido.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 5.**
Referencia de planificación: **R09**. Ver [mapa de Restobar](../../docs/restobar.md).
No tiene suite Robot, seed automático ni validación real del JAR. Los resultados siguientes son criterios esperados, no resultados obtenidos.

## Precondiciones y datos

- Paquete QA sintético, Windows exclusivo y escritorio visible. La preparación de carta, mesas, ingredientes, permisos y perfiles de este caso está **pendiente**; `catalogo-comercial-v1` no certifica estos datos.
- Perfil local por defecto: ARS, comprobante interno no fiscal, impuestos y cubiertos $0 salvo indicación, sin ofertas, listas ni beneficios adicionales. Las integraciones se habilitan solo en el laboratorio indicado.
- Primera comanda ya recibida de un plato $1.000; segunda ronda de dos bebidas $500 cada una; conteo por destino antes del envío.
- Se requiere evidencia de receptor/impresora, no solo contador local.
- Preparar y registrar antes de ejecutar los IDs propios de empresa, sucursal, puesto, cuenta, mesa y productos. Mantener una operación de control ajena al caso para verificar aislamiento.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Agregar la segunda ronda y elegir Nuevos. | La salida contiene las dos bebidas nuevas; no vuelve a presentarlas como un segundo consumo en la cuenta. |
| Consultar el pedido completo. | Un plato y dos bebidas, total $2.000; identidad de cuenta igual a la inicial. |
| Solicitar nuevamente cocina sin agregar y rechazar reimpresión. | No se genera otra salida ni cambian consumos. |
| Aceptar reimpresión o elegir Todos en una nueva preparación controlada. | La salida se identifica como repetición del contenido esperado; la cuenta y cobro permanecen únicos. |

## Variantes y límites

Editar cantidad antes/después del primer envío; productos con destinos diferentes; reintento tras salida fallida. Distinguir reimpresión de una nueva ronda y del estado de preparación.

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
- `src/ModuloRestobar/Controladores/VentaRestobarControlador.java`
- `src/ModuloVentas/Entidades/VentaDetalle.java`

La lectura de fuente/tests orienta el riesgo y el criterio; no acredita la ejecución del artefacto. INFO resume, DEBUG describe acciones de negocio y TRACE añade diagnóstico saneado. Un fallo conserva paso, esperado, observado, categoría y evidencia; causa no determinada si falta prueba causal. No registrar credenciales, filas completas ni configuración privada.

