---
{"id":"XG-INV-004","title":"Conciliar recepción, venta, receta y anulación en el mismo inventario","product":"xgestion","module":"inventario","tags":["xgestion","regression","inventario","stock","recuperacion"],"status":"planned"}
---

# XG-INV-004 — Conciliar recepción, venta, receta y anulación en el mismo inventario

## Objetivo

Seguir las existencias desde que se recibe mercadería hasta que se vende o consume en una receta y luego se anula, identificando cada entrada y salida sin compensaciones duplicadas.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P0; inventario, etapas 5 y 6.** Ver [mapa](../../docs/inventario-respaldos.md). Es una conciliación entre módulos; depende de los recorridos individuales de [recepción REM-001](../remitos/XG-REM-001.md), [materia prima REM-003](../remitos/XG-REM-003.md), [receta RES-014](../restobar/XG-RES-014.md) y [anulación de recepción REM-024](../remitos/XG-REM-024.md). Estas fichas también están pendientes; enlazarlas no acredita su ejecución.

## Precondiciones y datos

- VM Windows QA exclusiva y offline; cierre anual completo; empresa E1/S1, puesto y operador identificados. Comprobantes internos, ARS, efectivo, IVA 0; sin impresión, ofertas, listas ni pagos externos.
- **Fixtures sintéticos nuevos, NO creados:** A stockeable por unidad, inicial 10, venta ARS 1.000; harina y queso stockeables en kg, inicial 10,000 cada uno. Plato QA-INV-REC no stockeable, ARS 1.000, receta fija de 0,200 kg harina y 0,050 kg queso por plato, sin extras.
- Recepción R: A × 5, harina 1,000 kg y queso 0,500 kg; Recibido y Suma stock ON, actualización de precios OFF, sin cuenta corriente. Receta no se modifica durante el circuito.
- Otra sucursal y empresa mantienen saldos de control. Carta, remito, autorización de anulación y oráculos por producto/documento pendientes; el seed comercial no garantiza esta preparación.

## Pasos y resultados esperados

| Acción del usuario | Resultado esperado |
| --- | --- |
| Confirmar R una sola vez y consultar existencias. | A = 15; harina = 11,000 kg; queso = 10,500 kg. Una recepción enlazada, controles ajenos sin cambios. |
| En Venta, cargar A × 2; cancelar el cobro y retomarlo para cobrar ARS 2.000. | A = 13 tras el cobro; un solo egreso de 2. Harina/queso conservan sus saldos. |
| En Restobar, cargar dos platos; salir/reabrir la cuenta y cobrar ARS 2.000. | Consume harina 0,400 y queso 0,100 kg; quedan 10,600 y 10,400. Reabrir/consultar no duplica consumos. A sigue en 13. |
| Anular la venta de A mediante la ruta autorizada y consultar su comprobante. | A vuelve a 15; reversión de 2 vinculada a esa venta. Los platos y sus ingredientes no cambian. |
| Anular el comprobante de los dos platos por la ruta autorizada. | Harina vuelve a 11,000 y queso a 10,500; se devuelve una vez la receta de dos platos, sin sumar stock al padre no stockeable. |
| Anular R y volver a consultar los tres productos. | A = 10, harina = 10,000 y queso = 10,000: coincide con el inicio. No resta ingredientes dos veces ni revierte precios comerciales. |
| Consultar otra vez los documentos anulados y el historial. | Estados y motivos permanecen; consultar no crea nuevas entradas/salidas. Cada delta se explica por un único documento del circuito. |

## Variantes y dependencias

- En un baseline independiente, rechazar cada confirmación de anulación antes de aceptarla: saldos sin cambios por el rechazo. Repetir una consulta no equivale a intentar anular otra vez.
- Registrar antes de automatizar la política de devolución de dinero y su movimiento esperado. Esta ficha concilia stock; la compensación financiera requiere el caso específico correspondiente.
- El plato no stockeable es deliberado: una entrada indebida al padre debe detectarse aunque los ingredientes terminen bien. La fuente de anulación merece verificar ese riesgo en el JAR; no se afirma defecto ya reproducido.
- Extras/ingredientes compartidos remiten a [RES-015](../restobar/XG-RES-015.md). La devolución de extras no queda acreditada por devolver la receta: preparar su oráculo y ruta antes de sumar esa variante.
- Una receta modificada entre venta y anulación requiere criterio de histórico pendiente. No cambiar el esperado tomando la receta actual por conveniencia.
- Sucursales destino, unidades/bultos y recepción parcial necesitan perfiles independientes; no inferir su resultado del circuito básico.

## Evidencia y límites

Conciliar para cada producto **saldo inicial + recepciones - ventas/consumos + anulaciones de venta - anulaciones de recepción = saldo final**. Guardar unidades, ámbitos y vínculos de todos los documentos; no basta que la suma global termine igual, pues dos errores podrían compensarse. Diferenciar cuenta, mesa y cocina; cocina/impresión quedan fuera.

## Recuperación

Ante cierre o anulación ambiguos, consultar por identidad antes de reintentar. Conservar los deltas parciales y el fallo; no completar el circuito para disimular una discrepancia. La anulación funcional forma parte de la prueba y no reemplaza la restauración del baseline posterior.

## Anexo técnico y trazabilidad

Fuente ERP: commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`.

- `src/ModuloVentas/Entidades/TicketVenta.java:526-562,3285-3312`: cierre, producto stockeable, receta y anulación.
- `src/ModuloProductos/Entidades/ProductoHijo.java:28-45,83-101,115-139`: cantidades de receta consumidas/devueltas.
- `src/ModuloProductos/Entidades/Compra.java:652-660` y `CompraDetalle.java:214-275`: reversión de recepción.
- `test/ModuloProductos/Entidades/ProductoHijoStockPolicyTest.java`; trazabilidad de UI de recepción y recetas en REM-001/003/024 y RES-014/015.

Acciones de anulación, localizadores y lectura de movimientos aún pendientes. Registrar JAR/paquete/perfil y esperado/observado por paso; INFO breve, DEBUG de negocio y TRACE saneado, sin filas completas.

