# Ofertas: mapa de escenarios y pendientes

De las 72 fichas del backlog inicial, **70 están automatizadas**: XG-PRM-008..076 y XG-PRM-079.
XG-PRM-077/078 siguen pendientes: todavía no existe el paquete de varias sucursales/empresas.
La [cobertura general](cobertura.md) cuenta 315 fichas: 112 implementadas y 203 pendientes, incluidas las nuevas familias de remitos, Restobar y listas.
La evidencia real sigue pendiente. Preparar los [contratos de canastas](canastas-ofertas.md) antes de ejecutar.

## Cómo consultar y priorizar

```powershell
.\qa.cmd list --product xgestion --groups
.\qa.cmd list --product xgestion --group promociones-alcances
.\qa.cmd list --product xgestion --group ofertas-familia
.\qa.cmd list --product xgestion --group promociones-agrupadas
.\qa.cmd list --product xgestion --group promociones-combos
.\qa.cmd list --product xgestion --group promociones-condiciones
```

Los subgrupos ejecutan únicamente los casos implementados. `promociones` selecciona 77 y
`regression`, 96, sin duplicaciones por etiquetas. El menú identifica los dos pendientes.
Comenzar por un caso y luego un grupo pequeño; cada ficha incluye datos y perfiles necesarios.

## Fórmula y alcance sin agrupación

Cada celda identifica un escenario. **I** significa implementado, con validación
real pendiente; **P** significa pendiente de automatizar. Los demás alcances están
sin agrupación: dos productos diferentes no suman cantidades para alcanzar el mínimo.

| Fórmula | Producto | Familia | Subfamilia | Marca | Sector |
| --- | --- | --- | --- | --- | --- |
| Porcentaje | [001 I](../scenarios/promociones/XG-PRM-001.md) | [011 I](../scenarios/promociones/XG-PRM-011.md) | [018 I](../scenarios/promociones/XG-PRM-018.md) | [025 I](../scenarios/promociones/XG-PRM-025.md) | [032 I](../scenarios/promociones/XG-PRM-032.md) |
| Importe por unidad | [002 I](../scenarios/promociones/XG-PRM-002.md) | [012 I](../scenarios/promociones/XG-PRM-012.md) | [019 I](../scenarios/promociones/XG-PRM-019.md) | [026 I](../scenarios/promociones/XG-PRM-026.md) | [033 I](../scenarios/promociones/XG-PRM-033.md) |
| Lleva X y paga Y | [003 I](../scenarios/promociones/XG-PRM-003.md) | [013 I](../scenarios/promociones/XG-PRM-013.md) | [020 I](../scenarios/promociones/XG-PRM-020.md) | [027 I](../scenarios/promociones/XG-PRM-027.md) | [034 I](../scenarios/promociones/XG-PRM-034.md) |
| Descuento cada N unidades | [004 I](../scenarios/promociones/XG-PRM-004.md) | [014 I](../scenarios/promociones/XG-PRM-014.md) | [021 I](../scenarios/promociones/XG-PRM-021.md) | [028 I](../scenarios/promociones/XG-PRM-028.md) | [035 I](../scenarios/promociones/XG-PRM-035.md) |
| Porcentaje desde mínimo | [008 I](../scenarios/promociones/XG-PRM-008.md) | [015 I](../scenarios/promociones/XG-PRM-015.md) | [022 I](../scenarios/promociones/XG-PRM-022.md) | [029 I](../scenarios/promociones/XG-PRM-029.md) | [036 I](../scenarios/promociones/XG-PRM-036.md) |
| Importe desde mínimo | [009 I](../scenarios/promociones/XG-PRM-009.md) | [016 I](../scenarios/promociones/XG-PRM-016.md) | [023 I](../scenarios/promociones/XG-PRM-023.md) | [030 I](../scenarios/promociones/XG-PRM-030.md) | [037 I](../scenarios/promociones/XG-PRM-037.md) |
| Precio unitario desde mínimo | [010 I](../scenarios/promociones/XG-PRM-010.md) | [017 I](../scenarios/promociones/XG-PRM-017.md) | [024 I](../scenarios/promociones/XG-PRM-024.md) | [031 I](../scenarios/promociones/XG-PRM-031.md) | [038 I](../scenarios/promociones/XG-PRM-038.md) |

Las fichas incluyen aplicación y exclusión del producto ajeno, cantidad por debajo,
igual y superior al umbral cuando existe, reducción posterior y cancelación/retoma.
Los casos simples no acreditan todos los valores posibles de cada parámetro.

## Fórmulas combinando productos distintos

Los 21 casos son **I**, con variantes ON/OFF. Solo familia, subfamilia y marca admiten esta agrupación.
Producto y sector no tienen una celda equivalente. Los combos se definen por sus
componentes y tienen recorridos separados, no por esta matriz de alcances.

| Fórmula | Familia | Subfamilia | Marca |
| --- | --- | --- | --- |
| Porcentaje | [039](../scenarios/promociones/XG-PRM-039.md) | [046](../scenarios/promociones/XG-PRM-046.md) | [053](../scenarios/promociones/XG-PRM-053.md) |
| Importe por unidad | [040](../scenarios/promociones/XG-PRM-040.md) | [047](../scenarios/promociones/XG-PRM-047.md) | [054](../scenarios/promociones/XG-PRM-054.md) |
| Lleva tres y paga dos | [041](../scenarios/promociones/XG-PRM-041.md) | [048](../scenarios/promociones/XG-PRM-048.md) | [055](../scenarios/promociones/XG-PRM-055.md) |
| Descuento cada N unidades | [042](../scenarios/promociones/XG-PRM-042.md) | [049](../scenarios/promociones/XG-PRM-049.md) | [056](../scenarios/promociones/XG-PRM-056.md) |
| Porcentaje desde mínimo | [043](../scenarios/promociones/XG-PRM-043.md) | [050](../scenarios/promociones/XG-PRM-050.md) | [057](../scenarios/promociones/XG-PRM-057.md) |
| Importe desde mínimo | [044](../scenarios/promociones/XG-PRM-044.md) | [051](../scenarios/promociones/XG-PRM-051.md) | [058](../scenarios/promociones/XG-PRM-058.md) |
| Precio unitario desde mínimo | [045](../scenarios/promociones/XG-PRM-045.md) | [052](../scenarios/promociones/XG-PRM-052.md) | [059](../scenarios/promociones/XG-PRM-059.md) |

Comparar agrupación ON/OFF desde perfiles separados; incluir producto ajeno,
productos de distinto precio, umbral incompleto/completo/sobrante y recálculo.
No activar la agrupación de todas las fórmulas simultáneamente en los mismos datos.

## Combos y condiciones comerciales

Todos están implementados salvo 077/078; la validación real de todos sigue pendiente.

| ID | Recorrido | Dependencia principal |
| --- | --- | --- |
| [060](../scenarios/promociones/XG-PRM-060.md) | Completar un combo y quitar un componente. | Combo seed y edición de varias líneas. |
| [061](../scenarios/promociones/XG-PRM-061.md) | Repetir combos y aplicar oferta al sobrante. | Cantidades y descuento por producto restante. |
| [062](../scenarios/promociones/XG-PRM-062.md) | Elegir entre combos que compiten. | Datos nuevos de mayor ahorro y empate. |
| [063](../scenarios/promociones/XG-PRM-063.md) | Distribuir descuentos de combo sin perder centavos. | Precios nuevos y oráculos de redondeo. |
| [064](../scenarios/promociones/XG-PRM-064.md) | Respetar cantidades fraccionarias del combo. | Cantidades y componentes calibrados. |
| [065](../scenarios/promociones/XG-PRM-065.md) | Fracciones sin mínimo, con precio, porcentaje e importe. | Seed KG-MIN0 y ampliaciones. |
| [066](../scenarios/promociones/XG-PRM-066.md) | Alcanzar/perder el mínimo de un kilo. | Seed KG-MIN1 y ampliaciones. |
| [067](../scenarios/promociones/XG-PRM-067.md) | Prioridad producto → marca → subfamilia → familia → sector. | Pertenencias y ofertas superpuestas nuevas. |
| [068](../scenarios/promociones/XG-PRM-068.md) | Prioridad por mínimo y fecha dentro del mismo alcance. | Ofertas elegibles/ineligibles simultáneas. |
| [069](../scenarios/promociones/XG-PRM-069.md) | Primer y último día de vigencia. | Fecha QA consistente, sin cambiar reloj. |
| [070](../scenarios/promociones/XG-PRM-070.md) | Activa/desactivada en nuevas corridas. | Baselines independientes. |
| [071](../scenarios/promociones/XG-PRM-071.md) | Oferta sobre el precio efectivo de una lista. | Cruce producto/oferta/listas nuevo. |
| [072](../scenarios/promociones/XG-PRM-072.md) | Cambiar lista y recuperar precio de producto ausente. | Selector, precios y recálculo. |
| [073](../scenarios/promociones/XG-PRM-073.md) | Oferta para Todos los medios. | Medios manuales offline. |
| [074](../scenarios/promociones/XG-PRM-074.md) | Oferta para un único medio. | Medio admitido y excluido. |
| [075](../scenarios/promociones/XG-PRM-075.md) | Oferta para varios medios elegidos. | Selección múltiple de aplicabilidad; cobro simple. |
| [076](../scenarios/promociones/XG-PRM-076.md) | Cambiar medio y cancelar/retomar cobro. | Extender el contrato de cobro. |
| [077](../scenarios/promociones/XG-PRM-077.md) | Sucursal admitida, excluida y Todas. | Laboratorio multi-sucursal aislado. |
| [078](../scenarios/promociones/XG-PRM-078.md) | Aislar empresas con IDs coincidentes. | Laboratorio multiempresa aislado. |
| [079](../scenarios/promociones/XG-PRM-079.md) | Permitir/rechazar descuento manual sobre oferta. | Permisos, aviso y base de cálculo. |

## Datos, evidencia y mantenimiento

El [seed actual](seed.md) aporta ejemplos, no todos los perfiles de estas fichas.
Los datos nuevos se identifican como pendientes de preparar. Los vínculos entre
ejemplos y fichas indican el escenario que los utiliza; no garantizan que el seed
por sí solo satisfaga todos sus prerrequisitos. El runner no aplica datos para un
caso `planned`, porque rechaza su ejecución antes de preparar el laboratorio.

El [Excel](../../../docs/coverage/xgestion-cobertura.xlsx) muestra cada ficha en
**Escenarios**, los subgrupos en **Grupos** y sus ejemplos en **Ejemplos seed**.
**Por detallar** conserva familias más amplias; no se suma a las fichas para
inventar un total de casos. Hay otras variantes del roadmap todavía sin ficha.

Antes de automatizar: completar fixtures, selectores accesibles, oráculos y logs;
actualizar el mismo ID a `implemented`, enlazar Robot y regenerar el mapa. La
validación real exige JAR, perfil y evidencia registrados. Las condiciones comunes
son ARS, comprobante interno 99, datos QA aislados y sin fiscalización/impresión.
Los medios de pago nuevos son manuales offline, sin integración con proveedores.

Fuente de reglas: XGestion2 `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`, enums
`TipoOferta`/`TipoOfertaDescuento`, `OfertaCalculador`, `OfertaAplicacionCalculador`,
`OfertaLineaService`, `OfertaComboService`, `OfertaTiposCobro` y tests referidos en
cada ficha. Especificación de esta entrega: [006-backlog-promociones](../../../docs/specs/006-backlog-promociones.md).

## Incidente de precio final USD

[PRM-080..084](ofertas-usd.md) agregan cinco casos P0 automatizados con trece variantes por producto, familia, subfamilia, marca y sector. Validación real pendiente. PRM-077/078 continúan planificados. No se consideran cubiertas otras fórmulas en USD, canastas de monedas mezcladas, listas, impuestos, cotizaciones adicionales ni reaperturas.
