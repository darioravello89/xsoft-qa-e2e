# Ejecutar promociones simples

El grupo `promociones` contiene XG-PRM-001 a XG-PRM-007. Cada caso carga un
artículo, cambia su cantidad por teclado, cancela el cobro y lo retoma para cobrar
una sola vez. La automatización está implementada; falta validarla sobre el FAT JAR.

```powershell
.\qa.cmd list --product xgestion --group promociones
.\qa.cmd run --product xgestion --group promociones --log-level DEBUG
.\qa.cmd report --latest
```

El menú **Ejecutar grupo → Promociones** selecciona los mismos siete casos.
Sus fichas declaran `seed: catalogo-comercial-v1`: el runner lo informa, restaura
el baseline QA y aplica/verifica los upserts antes de iniciar XGestion. Esto también
ocurre al elegir un solo ID o `regression`. Se puede escribir `--seed
catalogo-comercial-v1` explícitamente. El dry-run sólo describe el catálogo, sin DB.

## Perfil necesario

Conservar el Windows QA exclusivo, offline, con consola visible, paquete privado
autorizado y controles de [preparación](../../../docs/paquete-privado.md).
No se ejecutan estas pruebas sobre una instalación habitual o una DB compartida.

- ARS, precio base 1000, IVA 0%, stock suficiente y artículos seed sin listas ni
  condiciones ajenas. La fecha del seed debe coincidir con Windows y MySQL.
- Comprobante interno 99, cobro simple en efectivo y diálogo de cobro habilitado.
  Sin impresión ni fiscalización. Abandonar no requiere supervisor.
- Selector de lista visible (`venta.listadeprecio.elegir=true`), **Ninguna Lista**
  (ID 0) como valor inicial. `venta.listaPrecio.fija.id=0`, cliente y turno sin lista.
- Sin descuentos manuales de línea, globales, por cliente o por medio de pago.
  Efectivo con `pagPorcentajeDescuento=0` y `fidelizacion.activo=false`.
- El seed no configura cliente, turno ni aplicación. El responsable prepara esas
  condiciones en el paquete y las comprueba durante la calibración.

`fixtures.json` añade este bloque opcional para el lote:

```json
"promotions": {
  "schema_version": 1,
  "currency": "ARS",
  "price_list_id": 0,
  "price_list_text": "Ninguna Lista",
  "other_discounts": false,
  "loyalty": false,
  "customer_and_shift_lists": false
}
```

`sales_journeys.defaults.price_list` debe ser también `Ninguna Lista`. Los demás
defaults conservan los textos observados del cliente y comprobante. Los productos
de los casos se eligen del catálogo público por ID/código; no se reemplaza el
fixture de Venta cotidiana en el archivo privado.

## Calibración para el responsable

Se necesitan `ventas-etapa1`, `ventas-teclado-v1` y `promociones-v1` en
`locators.calibration.verified_features`, verificadas sobre el mismo SHA256 del JAR.
Agregar el nombre de la feature por sí solo no calibra ni aprueba un caso.

1. Identificar el botón Editar, el editor, Cantidad, Guardar y Cancelar. Comprobar
   selección por identidad de producto, Ctrl+E y regreso del foco a la misma fila.
2. En `sale.lines.columns`, observar siete columnas distintas: `code`, `name`,
   `quantity`, `unit_price`, `gross_total`, `offer_discount` y `total`.
   **`total` representa el neto final del renglón**, `gross_total` su bruto y
   `offer_discount` el descuento expresado como importe positivo. No mapear una
   columna porcentual como importe. Registrar `column_count` real e índices JAB
   observados; no copiar coordenadas ni inventar posiciones de columnas.
3. Verificar formato ARS con coma decimal en grilla y total de venta; cantidad con
   punto decimal; en el diálogo de cobro, importe decimal con punto sin agrupación.
4. Observar carga y recálculo de PCT, IMP, 2×1 y segunda al 50%. Para cantidades sin
   beneficio, la columna de oferta debe mostrar cero legible. Confirmar la lectura
   real antes de habilitar esta versión del contrato.
5. Verificar cancelar cobro y volver a abrirlo con el mismo neto. Registrar persona,
   fecha, versión JAB y hash del JAR mediante el flujo normal de calibración.

Si la grilla o el formato no coinciden, el caso bloquea o falla con evidencia del
paso; adaptar y verificar el contrato para ese JAR antes de repetir. No relajar las
aserciones para aceptar un total aparentemente correcto.

## Resultados que se comprueban

| Caso | Producto seed | Cantidad / neto inicial ARS | Cantidad / neto final ARS |
| --- | --- | --- | --- |
| XG-PRM-001 | PCT | 1 / 900 | 3 / 2700 |
| XG-PRM-002 | IMP | 1 / 850 | 3 / 2550 |
| XG-PRM-003 | 2X1 | 1 / 1000 | 3 / 2000 |
| XG-PRM-004 | 2DA50 | 1 / 1000 | 3 / 2500 |
| XG-PRM-005 | EXPIRADA | 2 / 2000 | 1 / 1000 |
| XG-PRM-006 | FUTURA | 2 / 2000 | 1 / 1000 |
| XG-PRM-007 | INACTIVA | 2 / 2000 | 1 / 1000 |

En los tres últimos casos se comprueba antes PCT × 1 = 900 y se abandona esa venta
sin movimientos. Si ese control positivo falla, el caso no continúa. Así, no aplicar
una oferta inválida no se aprueba simplemente porque todas las ofertas dejaron de funcionar.

Al editar se exige una sola línea del mismo producto, cantidades correctas y
componentes bruto/oferta/neto. Al cancelar cobro, se conserva la grilla y no cambia
la evidencia de ventas, detalles, pagos, stock ni caja. Al retomar: efectivo exacto,
vuelto cero, una venta, un movimiento de stock y un ingreso de caja por el neto.

Los SELECT de evidencia verifican `vecPrecio=1000`, `vecTotal` bruto, `vecOferta`
automático e `ID_Oferta`; `vecOfertaManual`, otros descuentos y puntos deben ser cero.
La cabecera conserva neto y descuentos correspondientes. Las comprobaciones se
acotan a empresa/sucursal/puesto y a la identidad de la operación; no imprimen filas.

## Recuperación y alcance pendiente

Ante un fallo, conservar el informe local. Repetir desde `qa.cmd run` restaura el
baseline y prepara de nuevo el catálogo. No corregir importes o movimientos con SQL
para aprobar un caso. INFO resume, DEBUG muestra pasos y TRACE añade diagnóstico
saneado; ningún nivel implica registrar credenciales o configuración completa.

Quedan pendientes combos, umbrales, fracciones, ofertas por alcance o pago,
descuentos combinados y listas. Ver [roadmap](roadmap.md), [seed](seed.md) y
[especificación del lote](../../../docs/specs/005-promociones.md).

Fuente inspeccionada: XGestion2 `925589278503f2d339beeb0a79f773c605512dd8`,
`OfertaCalculador`, `OfertaLineaService`, `FormVenta`, `FormVentaDetalle`,
`TicketVenta` y `VentaListaPrecioPrioridadPolicy`. Esa referencia acredita reglas
observadas en fuente, no ejecución E2E del artefacto distribuido.
