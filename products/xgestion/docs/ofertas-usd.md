# Ofertas USD — regresión crítica P0

La oferta debe dejar un producto de **USD 100 en USD 50**. A cotización
1500 ARS/USD se cobran **ARS 75.000**, no ARS 50. Este contrato comercial
proviene del incidente reportado; el cálculo actual del ERP no define el esperado.

## Ejecutar y consultar

```powershell
.\qa.cmd list --product xgestion --group ofertas-usd
.\qa.cmd run --product xgestion --group ofertas-usd --seed catalogo-comercial-v1 --log-level INFO
```

En el menú elegir **Ofertas en USD — P0**. DEBUG muestra pasos; TRACE añade
diagnóstico saneado. Para ejecutar una ficha usar `--scenario XG-PRM-080`
en lugar de `--group ofertas-usd`. El grupo también pertenece a promociones
y regression; cada selección ejecuta cada ID una sola vez.

| Caso | Alcance | Variantes obligatorias |
| --- | --- | --- |
| [XG-PRM-080](../scenarios/promociones/XG-PRM-080.md) | Producto | Desde 1; desde 2, sin agrupar |
| [XG-PRM-081](../scenarios/promociones/XG-PRM-081.md) | Familia | Desde 1; desde 2 con agrupación OFF y ON |
| [XG-PRM-082](../scenarios/promociones/XG-PRM-082.md) | Subfamilia | Desde 1; desde 2 con agrupación OFF y ON |
| [XG-PRM-083](../scenarios/promociones/XG-PRM-083.md) | Marca | Desde 1; desde 2 con agrupación OFF y ON |
| [XG-PRM-084](../scenarios/promociones/XG-PRM-084.md) | Sector | Desde 1; desde 2, sin agrupar |

Son **cinco casos y trece variantes**, no trece casos adicionales. Si una
variante falla, el caso no aprueba; las variantes posteriores no se consideran
ejecutadas. Un fallo o bloqueo P0 mantiene pendiente la aceptación de ofertas.

## Perfil y datos reproducibles

Windows QA exclusivo y offline, escritorio local desbloqueado, paquete privado
autorizado y JAR identificado por SHA256. Usar el [quick start](../../../README.md)
y completar la [calibración](calibracion.md) y [canastas](canastas-ofertas.md).

- Productos A/B/E a USD 100, IVA 0 %, stock inicial 100 unidades, precio normal.
- Documento interno 99, moneda contable ARS, efectivo ARS, vuelto ARS, diálogo
  de cobro habilitado; cobro multimoneda habilitado para observar los selectores.
- Cotización visible **1500.00**; prepararla en el paquete QA. El recorrido la
  lee y bloquea si no coincide; no cambia la cotización para hacer pasar el caso.
- Sin listas, otros descuentos, recargos, fidelización, impuestos adicionales,
  impresión ni fiscalización. Edición Ctrl+E y eliminación sin supervisor.
- Seed `catalogo-comercial-v1`, prefijos `QA-PRM-080..084-V0/V1/V2`.
  Reservas 989000..989429 según variante. Los productos y categorías son
  independientes, sin afectar los medios QA 989901..989903.
- Moneda del artículo ID 2 (DOL), comprobante y cobro ID 1 (PES), validadas
  contra catálogos existentes. Oferta `LXO+$CU`, **Paga=50.00**; mínimo 1 o 2.
  No reemplazar 50 por 75000 en el seed ni interpretar la regla como descuento `$`.

El seed aplica upserts mediante los controles habituales y deja las monedas
globales intactas. Su aplicación no demuestra que el JAR aplique bien la oferta.

## Calibración privada ofertas-usd-v1

En fixtures copiar la sección `offer_usd` del ejemplo: versión 1, producto y
renglones USD, documento/cobro ARS y cotización `1500.00`. Conservar `currency: ARS`
en promociones y sales_journeys: indica el documento, no la moneda original de
cada artículo. La sección adicional es obligatoria sólo para estos cinco casos.

Observar en el JAR real y completar estos aliases semánticos, sin coordenadas:

| Alias | Control y contrato observable |
| --- | --- |
| `sale.usd_rate` | Cotización USD/ARS visible al cargar un producto USD, decimal con punto `1500.00` |
| `sale.lines` | Columnas existentes: código, nombre, cantidad, precio, bruto, descuento y neto; importes originales con prefijo `USD` |
| `sale.total` | Total contable con prefijo `$` o `ARS`; formato `75.000,00` |
| `payment.total_currency` | Texto del selector visible de moneda del total: `ARS` |
| `payment.amount_currency` | Texto del selector visible de moneda recibida: `ARS` |
| `payment.change_currency` | Texto del selector visible de moneda del vuelto: `ARS` |

Los campos de total/recibido/vuelto del cobro mantienen el formato decimal con
punto del perfil actual. Los selectores aportan su moneda; no se infiere del
número. Agregar `ofertas-usd-v1` a `verified_features` solamente tras verificar
los controles y el SHA256. Los ejemplos permanecen `draft` y con `CALIBRAR`.
Si los controles no son accesibles, registrar el bloqueo para ese JAR; no usar
coordenadas ni marcar la calibración como verificada por inspeccionar fuentes.

## Resultados esperados

Con mínimo uno, A pasa 1→2→1: netos USD 50→100→50 y totales ARS
75000→150000→75000. E conserva USD 100 sin oferta. En categorías, B también
recibe USD 50 de precio final; al quitarlo se conserva A.

Con mínimo dos, A1 no tiene oferta; A2 termina en USD 100; volver a A1 retira
el descuento. A1+B1 termina en USD 200 con agrupación OFF y USD 100 con ON.
Retirar B vuelve a dejar A1 sin oferta. Finalmente A2 se cobra a ARS 150000.

Cada variante cancela el diálogo después de ingresar el total y vuelve a
cobrar. La cancelación mantiene toda la canasta y no crea venta/caja/stock.
La confirmación crea una venta y un movimiento de caja por el neto, con salida
de stock sólo de A (1 o 2 unidades); B/E fueron retirados.

En cualquier nivel de log, un importe erróneo debe mostrar paso, moneda,
esperado y observado. El caso reportado debe fallar antes de confirmar ARS 50;
no se acepta como un resultado esperado por ser un defecto conocido.

## Evidencia y recuperación

Guardar reporte local con variante/pasos, captura posterior al login, versión
y SHA256 del JAR, paquete, perfil, fecha y responsable. No publicar credenciales
ni filas completas. Ante fallo, detener la confirmación, finalizar sólo el
proceso administrado y restaurar baseline mediante el runner antes de repetir.

Anexo técnico: las lecturas de ventas incluyen ID_Moneda, Cotizacion_USD y
snapshots originales de pago/vuelto. Las de ventas_cuerpo incluyen ID_Moneda,
vecPrecioOriginal, vecTotalOriginal, vecOfertaOriginal, manual e impuestos
originales, además de importes ARS, identidad de oferta y deltas existentes.
La ausencia de evidencia nunca produce OK.

## Cobertura y límites

En el [Excel](../../../docs/coverage/xgestion-cobertura.xlsx), filtrar grupo
**Ofertas en USD — P0**. Los cinco casos llevan prioridad P0 explícita; la
validación real sigue **pendiente** hasta ejecutar el JAR correspondiente.

Continúan pendientes los cruces con presupuestos/reaperturas, otras
cotizaciones, IVA/impuestos, listas, documentos/cobros USD, canastas con monedas
mezcladas dentro de una misma oferta y otras fórmulas de promociones.
Los casos ARS existentes siguen siendo necesarios; este grupo no los sustituye.
