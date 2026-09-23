---
{"id":"XG-INV-003","title":"Comenzar el año conservando el stock previo sin duplicar la apertura","product":"xgestion","module":"inventario","tags":["xgestion","regression","inventario","stock","recuperacion"],"status":"planned"}
---

# XG-INV-003 — Comenzar el año conservando el stock previo sin duplicar la apertura

## Objetivo

Consultar y usar existencias al comenzar un año, reconociendo un cierre pendiente o inconsistente sin presentar cantidades desconocidas como disponibilidad comprobada.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P0; inventario, etapa 6.** Ver [mapa](../../docs/inventario-respaldos.md). Primera variante local offline; los protocolos de nube/sincronización requieren otro laboratorio antes de habilitarse.

## Precondiciones y datos

- **Fixtures sintéticos nuevos, NO creados:** año QA Y, empresa E1/S1, movimientos activos de Y-1 con saldo A = 10,000 unidades y MP = 2,500 kg; sin apertura de Y. Sin movimientos anteriores a Y-1 en el perfil básico.
- Perfil local sin nube, cierre automático habilitado. Control E1/S2 con A = 40,000 y otra empresa con A = 30,000; no deben participar en el cierre de E1/S1.
- Año/reloj y fecha de baseline coherentes en VM temporal antes de iniciar el JAR. El año de la regla usa Buenos Aires; no cambiar el reloj durante la ejecución.
- Preparar aparte perfiles ya cerrado, apertura incompleta y stock previo no reconocido. No simularlos alterando SQL mientras el usuario opera.

## Pasos y resultados esperados

| Acción del usuario | Resultado esperado |
| --- | --- |
| Iniciar XGestión con el perfil básico y esperar a que finalice la coordinación del cierre. | Al abrir el listado de stock, A = 10,000 y MP = 2,500; existe una sola apertura del año Y para ese ámbito. No exigir un popup de éxito en la ruta de inicio en segundo plano. |
| Cerrar/reabrir el programa y consultar nuevamente. | Mantiene A = 10,000 y MP = 2,500; no duplica aperturas ni existencias. |
| Vender y cobrar A × 1 con comprobante interno ARS 1.000. | A queda en 9,000; una venta y un egreso posterior a la apertura. MP y controles ajenos no cambian. |
| Desde otro baseline, iniciar con apertura incompleta e intentar abrir ajuste o transferencias. | Informa cierre pendiente/inconsistente y no presenta la función de stock como lista para operar. Expone una opción de reintento o detalle sin declarar cierre íntegro. |
| Elegir Ver detalle y continuar. | No duplica ni completa silenciosamente la apertura inválida. La fuente permite continuar ventas/recepciones: no exigir bloqueo general del sistema ni afirmar stock disponible mientras sea desconocido. |
| Tras recuperar un baseline íntegro por el procedimiento QA, reiniciar y repetir la consulta. | Acceso normal y saldos previstos; el caso conserva la evidencia del intento fallido. |

## Variantes y dependencias

- Sin movimientos del año anterior ni anteriores: no crear un cierre ficticio. La evidencia debe distinguir «no requerido» de «creado».
- Movimientos en Y-2 y cierre previo de Y-1 ausente/inconsistente: informar intervención de soporte, no inventar arrastre desde un saldo incompleto. Con cierre previo reconocido, conservar correctamente su saldo y los movimientos de Y-1.
- Marcador existente con aperturas faltantes, duplicado o checksum discrepante: rechazo sin nueva apertura. Protocolos legacy y nuevo se preparan en baselines separados; no mezclar evidencia.
- Interrupción/fallo local: inyección y recuperación pendientes de implementar. Exigir ausencia de un cierre parcial aceptado y reintento sin duplicación; las pruebas de transacción de fuente no acreditan el JAR.
- Nube sin endpoint o sincronización incompleta queda fuera del perfil offline. No aceptar automáticamente el cierre manual compatible ni conectarse a un backend real.

## Evidencia y límites

Registrar año, ámbito, saldos previos, aperturas y movimiento siguiente por identidad/delta; estado visible y diagnóstico saneado. La integridad requiere el conjunto completo de productos del fixture, no solo un total. Nunca validar por el mero mensaje de cierre. La consulta/reporte es P1; integridad, rechazo y recuperación son P0.

## Recuperación

Si el cierre queda inconsistente, preservar la evidencia y detener las acciones que dependan de stock fiable. Restaurar la VM/baseline preparado; no reparar marcadores ni aperturas a mano. Reintentar únicamente cuando el estado del laboratorio esté conocido y documentado.

## Anexo técnico y trazabilidad

Fuente ERP: commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`.

- `src/ModuloProductos/Entidades/CierreAnualStocks.java:36-74,155-192,230-243`: coordinación, funciones de stock, continuación y reintento.
- `src/ModuloProductos/Servicios/CierreAnualStockService.java:47-86,157-255,470-489`: local/nube, verificación, transacción y cierre previo.
- `src/ModuloProductos/Servicios/CierreAnualStockPolicy.java:11-38`: año/zona, marcador y necesidad de cierre.
- `test/ModuloProductos/Servicios/CierreAnualStockPrevioPolicyTest.java`, `CierreAnualStockLocalTransactionPolicyTest.java`, `CierreAnualStockProtocolosJdbcTest.java` y `test/ModuloProductos/Entidades/CierreAnualStocksUiPolicyTest.java`.

Pendientes: perfiles temporales, navegación y oráculo de aperturas. Registrar SHA256 del JAR, paquete, fecha y reporte privado sin filas completas.

