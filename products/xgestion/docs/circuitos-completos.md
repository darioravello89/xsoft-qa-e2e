# Circuitos completos: productos, stock, dinero y deuda

Tres recorridos P0 tienen automatización: **FIN-011, FIN-013 y FIN-014**.
**FIN-012 sigue pendiente y bloqueado por accesibilidad**, por decisión del
usuario: no usar doble clic para abrir la cuenta del cliente. El commit
`3f8648035` incorpora Enter; falta validarlo con [KEY-001](atajos-listados.md)
antes de habilitar FIN-012. Ver ACC-010 en
[backlog](backlog-accesibilidad.csv). Ninguno tiene todavía validación real del
JAR; faltan la VM, el paquete privado y la calibración.

## Ejecutar por circuito

```powershell
.\qa.cmd list --product xgestion --group circuitos-completos
.\qa.cmd run --product xgestion --group circuitos-completos --seed catalogo-comercial-v1 --log-level INFO
```

Para una primera ejecución, usar `--scenario XG-FIN-011`, luego FIN-013 y FIN-014,
en lugar de `--group`. Cada invocación restaura el baseline. INFO resume,
DEBUG muestra acciones, TRACE conserva diagnóstico saneado. Un fallo o bloqueo
P0 impide aceptar el circuito. El dry-run sólo valida el armado de la suite.

## Recorridos y cifras de control

| Caso | Recorrido del usuario | Aprobación obligatoria |
| --- | --- | --- |
| [FIN-011](../scenarios/conciliacion/XG-FIN-011.md) | Vender dos unidades USD 100, cancelar cobro, retomarlo; recibir ARS 350.000 | Bruto/neto ARS 300.000; vuelto ARS 50.000; una venta, stock −2, Libro Diario +300.000; cuentas corrientes intactas |
| [FIN-012](../scenarios/conciliacion/XG-FIN-012.md) | Venta de dos unidades USD 100 a cuenta corriente ARS con anticipo 50.000; abonos 100.000 y 150.000 | Deuda 250.000→150.000→0; caja 50.000→150.000→300.000; stock −2 sólo al vender. **Pendiente por ACC-010** |
| [FIN-013](../scenarios/conciliacion/XG-FIN-013.md) | Cargar cuatro productos ARS/USD; rechazar recepción; confirmar a cuenta del proveedor; vender una unidad USD calculada | Compra ARS 362.400, stock +2 por producto, cuatro costos actualizados, sólo dos precios de venta calculados cambian; una deuda proveedor sin egreso. Venta posterior USD 120 = ARS 180.000, stock −1 |
| [FIN-014](../scenarios/conciliacion/XG-FIN-014.md) | Abrir turno, cancelar ingreso inicial, vender USD 100 por ARS 150.000, cerrar y consultar nuevamente | Fondo 0, efectivo/total 150.000; otros medios y egresos 0; un cierre asociado a su apertura; volver a consultar no cambia dinero, stock, deuda ni venta |

Los importes originales y operativos se comprueban por separado. **Producto
USD con documento y cobro ARS no prueba deuda ni efectivo en USD.** Libro Diario
se comprueba por persistencia; su pantalla de consulta sigue en las fichas LDI.
El balance del cierre sí se lee en pantalla. No se imprime ni se genera PDF.

## Batería fija de productos

El seed `catalogo-comercial-v1` agrega estos ocho productos a los anteriores.
IDs 990101..990108; clasificaciones reservadas 990100; proveedor 980001
`QA-SEED-PROVEEDOR`. No agrega monedas globales, clientes ni movimientos reales.

| Código QA-CIR- | Moneda | Venta / costo inicial | Stock | Uso |
| --- | --- | --- | --- | --- |
| ARS-FIJO | ARS | 1000 / 500 | 20 | Recibir a costo 600; venta sigue 1000 |
| USD-FIJO | USD | 100 / 50 | 20 | Recibir a costo 60; venta sigue 100; venta y cierre |
| ARS-CALCULADO | ARS | 1000 / 500 | 20 | Margen 100%; recibir a 600; venta pasa a 1200 |
| USD-CALCULADO | USD | 100 / 50 | 20 | Margen 100%; recibir a 60; venta pasa a 120 |
| USD-KG | USD | 10,01 / 5 | 10,5 | Fracción y redondeo: datos listos, recorrido pendiente |
| USD-BULTO | USD | 100 / 50 | 24 | Bulto 12, precio bulto 1200; recorrido pendiente |
| USD-SERVICIO | USD | 50 / 0 | No stockeable | Control de no movimiento; venta específica pendiente |
| CONTROL | ARS | 900 / 450 | 7 | No debe cambiar en ningún recorrido |

Cada remito recibe **dos unidades de los primeros cuatro productos**: costos
originales 600 ARS, 60 USD, 600 ARS y 60 USD. Total fijo 362.400 ARS. Los casos
comparan deltas para poder agruparse; el saldo absoluto depende de ventas
anteriores de la misma corrida. Un producto no usado no debe alterar su saldo.

## Perfil privado y calibración

Usar Windows QA exclusivo, local y offline, el [paquete](../../../docs/paquete-privado.md)
y la [calibración](calibracion.md). Monedas existentes PES=1/DOL=2, IVA 0%, tasa
1500, sin ofertas, listas, fidelización, recargos ni impresión. Comprobante 99,
efectivo ARS ID 1, sin supervisión al cancelar. Usuario administrador del
laboratorio. Baseline sin remitos abiertos ni turnos de hoy/abiertos ni mesas
abiertas para FIN-014. La fecha de Windows y MySQL debe coincidir.

Preparar en el paquete (el recorrido no reescribe configuración):

```properties
venta.convertirProductosUsdAPesos=false
pedirPagoAlCerrarTicket=true
venta.habilitarCierreAperturaTurno=true
venta.habilitarCierreCiego=false
ventas.cerrarSistemaConCierreDeTurno=false
```

Conservar `offer_usd` y `sales_journeys` de los ejemplos. Agregar `circuits`
versión 1, `operator_role: administrator` y el nombre accesible real del puesto
en `cash_computer_label`. Confirmar los efectos del perfil en el JAR: no basta
editar JSON. Los controles deben ser únicos, visibles y del proceso administrado.

| Capacidad verificada | Controles que hay que observar en el JAR |
| --- | --- |
| `circuitos-comerciales-v1` y `ofertas-usd-v1` | Venta, renglones USD, total ARS, tasa y monedas del diálogo de cobro |
| `remitos-circuito-v1` | Menú de compras, Cargar Remito, proveedor 980001, comprobante, producto, cantidad, costo, bonificación, grilla, Suma stock/Actualiza precio, confirmaciones de carga y deuda |
| `caja-circuito-v1` | Abrir/Cerrar Turno, autenticación, Cancelar ingreso inicial, balance, puesto/turno elegidos, rubros y salida Escape |

Los aliases exactos están en `examples/locators.example.json` y
`circuits/contracts.py`. La grilla de remito usa importes `USD 120.00`/`$ 1,200.00`;
Venta usa `USD 120,00`/`$ 1.200,00`. El total del remito usa el formato monetario
de Venta. Un control o formato incompatible bloquea calibración; no se normaliza
la moneda ni se cambia el esperado para hacer aprobar el producto.

No habilitar capacidades con `CALIBRAR` ni con hashes ficticios. La
autenticación del turno queda fuera de capturas aunque haya una ventana modal
encima. FIN-012 no tiene Robot: ninguna calibración habilita el doble clic.

## Variantes que aún faltan

| Riesgo | Datos/recorridos que faltan | Fichas relacionadas |
| --- | --- | --- |
| Cuenta corriente cliente | Atajo ACC-010; dos clientes identificados, deuda previa, sin anticipo/anticipo, abonos parciales/totales, cancelación, límite, deuda USD y otra cotización | FIN-012; FIN-001; CCC-001..010 |
| Remito | Recepción parcial; flags OFF; bonificación e impuestos; variantes/insumos/recetas; costo universal/lista proveedor; anulación; rechazo por variante de otra PC; reintento y rollback | REM-001..018; FIN-002..010 |
| Caja | Fondo/ingreso/egreso, tarjeta/transferencia, abonos de deuda anterior, monedas, arqueo con diferencia, cierre ciego, turno cruzando fecha, otras sucursales y puestos | CAJ-001..010; FIN-001 |
| USD y precios | Otras cotizaciones, USD como documento/pago/deuda, presupuesto/reapertura, listas por cliente/sucursal/horario, impuestos, ofertas y redondeos | LPR-001..028; COB; PRE; PRM-080..084 |
| Tipo de producto | Ejecutar fraccionable, bulto, servicio; stock mínimo/agotado; variantes padre/hijo, recetas, notas/agregados, devolución | BEN; INV; RES; DEV |
| Laboratorio ampliado | Varios puestos/empresas, procesos concurrentes, red/reintentos, impresoras/fiscal | CON; REC; FEL; PEX |

El seed previo ya contiene familias, subfamilias, marcas, sectores, variantes,
promociones y listas. No alcanza para probar estas combinaciones sin un perfil,
acciones y evidencia específicos. Nuevos clientes, roles, saldos, varias
sucursales/empresas y recetas requieren paquete preparado; no están inventados
ni importados a la instalación habitual.

## Evidencia y recuperación

Por paso conservar estado antes/después, identidades y deltas. Las lecturas
usan columnas acotadas de venta, detalle, pagos, stock, finanzas, compra,
cuentas corrientes, precios y turnos. Deuda del proveedor usa egresos para el
cargo de compra; deuda del cliente usa ingresos para el cargo de venta.
No volcar filas completas ni credenciales. Una evidencia incompleta falla.

Ante resultado incierto, conservar el informe local, cerrar sólo el proceso
administrado y repetir mediante el runner desde el baseline. No compensar ni
arreglar stock/deuda con SQL. Registrar SHA256 del JAR, paquete, perfil, fecha y
reporte al aceptar realmente. Fuente revisada: XGestion2
`0adea394095e4ceff54344bf38cbf21b7c01a5e8` (FormVenta, FormCargaDeRemito,
Compra/CompraDetalle, Articulo, MovimientoFinanzas, Turno y FormCierreDeCaja).
