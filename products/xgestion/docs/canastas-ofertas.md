# Canastas de ofertas: preparación y ejecución

Este lote agrega **70 escenarios automatizados**, PRM-008 a PRM-076 y PRM-079.
PRM-077/078 siguen pendientes: el usuario confirmó que todavía no existe el paquete
de varias sucursales/empresas. La validación real de todos los casos requiere el
JAR y el paquete privado calibrados. Un dry-run verifica estructura y keywords.

## Comenzar por un grupo pequeño

Seguir primero el [quick start del README](../../../README.md). En Windows QA
exclusivo, offline, con escritorio visible y desbloqueado:

```powershell
.\qa.cmd doctor
.\qa.cmd list --product xgestion --groups
.\qa.cmd list --product xgestion --group ofertas-familia
.\qa.cmd run --product xgestion --scenario XG-PRM-011 --dry-run
.\qa.cmd run --product xgestion --scenario XG-PRM-011 --log-level DEBUG
.\qa.cmd report --latest
```

Luego ejecutar `--group ofertas-familia`, `ofertas-subfamilia`, `ofertas-marca`,
`ofertas-sector`, `promociones-agrupadas`, `promociones-combos` o
`promociones-condiciones`. El runner prepara automáticamente el seed cuando el
caso lo requiere. INFO resume resultados; DEBUG muestra acciones de negocio;
TRACE conserva diagnóstico saneado. Todas las variantes pertenecen al mismo ID.

Consultar el [Excel de cobertura](../../../docs/coverage/xgestion-cobertura.xlsx)
y las [fichas](../scenarios/promociones/). Las tablas de cada ficha muestran el
código público, cantidades, descuentos automáticos/manuales y netos esperados.
Las expectativas son constantes revisadas; nunca se copian desde la respuesta del ERP.

## Datos fijos y aislamiento

El [seed](seed.md) contiene 395 artículos, 163 ofertas y 9 listas en total,
más tres medios **manuales internos QA**:

| Referencia | ID reservado | Nombre visible |
| --- | --- | --- |
| Efectivo QA | 989901 | QA-PRM-EFECTIVO |
| Transferencia QA | 989902 | QA-PRM-TRANSFERENCIA |
| Tarjeta QA | 989903 | QA-PRM-TARJETA |

Los tres son de tipo **Cobrado**, sin comisiones, recargos, descuentos propios,
proveedor ni integración. Comprueban aplicabilidad y destino del cobro simple;
no acreditan terminal, banco, tarjeta física ni servicio externo. El efectivo
habitual del paquete se conserva para los casos anteriores y las otras canastas.
La selección múltiple de medios habilitados en una oferta no divide el cobro.

Cada recorrido/variante dispone de productos y ofertas propios. El precio usual
es ARS 1.000; combos de centavos y fracciones declaran otros precios. El stock
inicial es 100 por producto nuevo y los impuestos adicionales son cero.
Se conservan los 48 artículos del catálogo original.

El seed comprueba identidades, referencias, esquema, triggers, colisiones y
readback en una transacción. Rechaza una instalación incompatible. No aplicar
los upserts con un cliente SQL ni modificar la base durante un recorrido.

## Calibración adicional del paquete

Mantener las comprobaciones existentes `ventas-etapa1`, `ventas-teclado-v1` y
`promociones-v1`. Agregar `promociones-canastas-v1` a las features verificadas
**solo después de observarla en el SHA256 exacto del JAR**.
Los [ejemplos públicos](../examples/) contienen placeholders, no una calibración aprobada.

En `fixtures.offer_journeys`, verificar:

- `schema_version: 1`, `item_removal_requires_supervisor: false`.
- Para todo recorrido que cobra, `choose_payment_on_close: true`: `pedirPagoAlCerrarTicket=true` abre el selector; se elige por ID mediante JAB y se confirma con Enter. Calibrar sus tres columnas nativas y `payment.method`, también para el efectivo habitual.
- Productos repetidos consolidados en una fila: `sales_journeys.repeated_product_rows: 1`.
- Para 071/072, `manual_price_list_enabled: true` y `recalculate_price_list: true`.
- Para 063/079, `manual_amount_mode: true`: el descuento es un importe **total del renglón**.
- Para 073–076, `manual_payments_offline: true`, con los tres medios y el cobro simple observados.

Calibrar por JAB, sin coordenadas:

| Controles | Comprobación |
| --- | --- |
| `editor.remove` | Ctrl+E abre el producto seleccionado; Eliminar quita ese renglón. |
| `editor.manual`, `editor.manual_percent` | Editable/focusable según permiso; importe seleccionado, no porcentaje. |
| `sale.choose_price_list`, `list_picker.lines/search` | Tabla de 2 columnas: ID y nombre, incluidos los ocultos. Enter en el buscador confirma la fila sin volver a escribir el filtro. |
| `sale.choose_payment`, `sale.payment_method` | Medio visible de venta y recálculo. |
| `payment_picker.lines/search` | Tabla de 3 columnas: ID, nombre y descuento; selección exacta por nombre e ID. |
| `payment.method` | Combo de cobro: hijo accesible seleccionado, no solo su etiqueta. |
| `editor.manual_warning` | Aviso exacto “Es peligroso hacer descuentos manuales a ofertas”, en la ventana y proceso propios observados. |

Para 079, `manual_warning_observation` exige `verified: true`, una ventana de
observación de 4 a 10 segundos, visibilidad mínima observada de 1 a 3 segundos y
un intervalo máximo de muestra menor que esa visibilidad (ejemplo 4 / 2 / 1).
Un aviso previo, una ambigüedad JAB o una pausa que podría ocultarlo bloquea la
evidencia. No acreditar ausencia con una única captura. El ejemplo deja
`verified: false` hasta medirlo en el laboratorio.

## Perfiles preparados por el runner

070 ejecuta **active → inactive → active-again** con la misma identidad de oferta
y un control positivo. Antes de cada fase restaura el baseline, aplica/verifica
el seed y abre una instancia nueva; no edita ofertas en una venta en curso.

079 ejecuta **general-off → offers-off → allowed-warning-on → allowed-warning-off**.
Cada fase restaura datos y prepara una copia local de configuración. En perfiles
restringidos verifica que el editor no permita escribir ni enfocar el descuento;
en los permitidos guarda 100 en A y exige oferta automática 90, neto A 810,
B 900 y total 1.710. El aviso no cambia los importes.

La configuración base de estas canastas habilita elegir/recalcular listas y
descuento manual sobre ofertas, con el aviso desactivado. Solo se cambian las
claves públicas acotadas de la copia runtime; el paquete original queda intacto.
El runner vuelve a preparar la configuración original al cerrar la ejecución.
No configurar manualmente variables de fase para ejecutar solo una parte del caso.

El selector de medios al cerrar se habilita en la copia runtime de canastas. Los botones usan acciones JAB; un control sin acción accesible bloquea el caso. Las leyendas dibujadas de combos mantienen su revisión pendiente en [XG-ACC-006](backlog-accesibilidad.csv); los casos 060/062 verifican el ID de oferta persistido.

El informe principal conserva **un resultado por ID** y muestra sus fases con
enlaces a los informes locales. Un fallo funcional permite completar las otras
fases; un bloqueo o cancelación deja las fases omitidas explícitas. Una fase sin
evidencia nunca cuenta como aprobada.

## Qué comprueba la confirmación

Cada transición compara todos los productos por código, cantidad, precio bruto,
descuentos visibles y neto. La grilla muestra automático más manual; la evidencia
de persistencia los distingue.

Cancelar o abandonar exige que no cambien ventas, detalles, pagos, movimientos
de stock, movimientos financieros ni existencias. Confirmar exige exactamente una
venta, sus líneas y ofertas, stock de todos los productos (también los excluidos)
y un ingreso por el medio seleccionado; detecta modificaciones a registros previos.

Fuente funcional: XGestion2 `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`.
No acredita fiscalización, impresión, red, dispositivos, concurrencia ni todos
los cruces posibles de configuración. Para ampliar un caso, actualizar datos,
pasos, ficha y mapa; conservar el resultado real vinculado al JAR y entorno usados.

## Ampliación crítica USD

[PRM-080..084](ofertas-usd.md) añaden cinco recorridos y trece variantes al lote ARS original de 70. Requieren ofertas-usd-v1 y expectativas originales USD separadas de importes operativos ARS. No quedan acreditados por validar el perfil ARS original.
