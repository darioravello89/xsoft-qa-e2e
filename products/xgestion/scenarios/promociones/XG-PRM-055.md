---
{"id":"XG-PRM-055","title":"Agrupar por marca: 3x2 entre productos","product":"xgestion","module":"promociones","tags":["xgestion","regression","promociones","promociones-agrupadas","ofertas-marca","escritura"],"status":"implemented","test":"products/xgestion/suites/ofertas/agrupadas.robot","seed":"catalogo-comercial-v1"}
---

# XG-PRM-055 — Agrupar por marca: 3x2 entre productos

## Objetivo

El vendedor combina artículos de una misma marca, comprueba qué beneficio corresponde y corrige la venta sin conservar descuentos que ya no corresponden.

<!-- BEGIN GENERATED OFFER JOURNEY -->

## Recorrido de automatización

Estado del catálogo: **implemented**. Automatización catalogada en [`agrupadas.robot`](../../suites/ofertas/agrupadas.robot). Validación real: **pendiente**; requiere ejecutar el JAR exacto en el laboratorio calibrado.

Las tablas siguientes son los datos y pasos actuales del recorrido. Los importes son expectativas fijas, no resultados medidos. El diseño anterior queda al final como referencia histórica para conservar reglas, variantes y límites; sus estados y códigos no describen la implementación actual.

```powershell
.\qa.cmd run --product xgestion --scenario XG-PRM-055 --seed catalogo-comercial-v1 --log-level DEBUG
```

## Perfil y preparación

Windows QA exclusivo y offline, escritorio desbloqueado, paquete autorizado y baseline restaurable. ARS, IVA 0 %, comprobante interno 99, stock suficiente, sin impresión ni fiscalización. Cliente y turno sin listas automáticas; otros descuentos, recargos y fidelización deshabilitados, salvo lo indicado en cada variante.

Preparar mediante el runner y `catalogo-comercial-v1` antes de abrir el JAR. Los códigos públicos de abajo pertenecen a este recorrido y reemplazan los ejemplos genéricos del diseño original. No cambiar reglas mediante SQL durante la venta. La falta de perfil, seed o calibración accesible se informa como bloqueo.

Cada variante inicia el JAR de forma independiente. Los perfiles de configuración de 070 y 079 además requieren su preparación y restauración por fase. Una misma ficha conserva un solo ID lógico; solo queda aprobada si todas las variantes requeridas producen evidencia completa.

**Lectura de importes:** automático y manual son descuentos totales del renglón. La grilla muestra ambos sumados en Descuentos; el informe y la evidencia de persistencia los distinguen. El neto de todos los renglones debe sumar el total de la venta.

## Variante 1: agrupacion-on

### Productos preparados

| Referencia | Código | Precio base | Unidad | Familia / subfamilia / sector | Marca |
| --- | --- | ---: | --- | --- | --- |
| A | `QA-PRM-055-V0-A` | $1.000,00 | unidad | 986501 / 986501 / 986500 | QA-PRM-055-V0-MARCA |
| B | `QA-PRM-055-V0-B` | $1.000,00 | unidad | 986502 / 986502 / 986500 | QA-PRM-055-V0-MARCA |
| C | `QA-PRM-055-V0-C` | $1.000,00 | unidad | 986503 / 986503 / 986500 | QA-PRM-055-V0-MARCA |
| E | `QA-PRM-055-V0-E` | $1.000,00 | unidad | 986501 / 986501 / 986500 | QA-PRM-055-V0-MARCA-AJENA |

### Ofertas preparadas

| Oferta | Incluye | Regla | Agrupación | Estado / vigencia inclusiva | Medios habilitados |
| --- | --- | --- | --- | --- | --- |
| `QA-PRM-055-V0` | Marca `QA-PRM-055-V0-MARCA` | Llevar 3 y pagar 2 | ON | Activa; hoy -365 días a hoy +365 días | Todos |

Las fechas se refieren a la fecha local usada al preparar el seed; Windows y MySQL deben coincidir. No se modifica el reloj durante el recorrido.

### Pasos y resultados esperados

| Paso | Acción del usuario | Canasta completa después del paso | Resultado |
| ---: | --- | --- | --- |
| 1 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 2 | Cargar 1 u de `QA-PRM-055-V0-A` por código. | `QA-PRM-055-V0-A` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal | Total **$1.000,00**. |
| 3 | Cargar 1 u de `QA-PRM-055-V0-E` por código. | `QA-PRM-055-V0-A` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal<br>`QA-PRM-055-V0-E` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal | Total **$2.000,00**. |
| 4 | Cargar 1 u de `QA-PRM-055-V0-B` por código. | `QA-PRM-055-V0-A` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal<br>`QA-PRM-055-V0-E` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal<br>`QA-PRM-055-V0-B` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal | Total **$3.000,00**. |
| 5 | Seleccionar `QA-PRM-055-V0-E`, abrir Ctrl+E y elegir Eliminar. | `QA-PRM-055-V0-A` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal<br>`QA-PRM-055-V0-B` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal | Total **$2.000,00**. |
| 6 | Cargar 1 u de `QA-PRM-055-V0-C` por código. | `QA-PRM-055-V0-A` × 1 u: precio $1.000,00; automático $333,33; manual $0,00; neto $666,67; lista aplicada: precio normal<br>`QA-PRM-055-V0-B` × 1 u: precio $1.000,00; automático $333,33; manual $0,00; neto $666,67; lista aplicada: precio normal<br>`QA-PRM-055-V0-C` × 1 u: precio $1.000,00; automático $333,34; manual $0,00; neto $666,66; lista aplicada: precio normal | Total **$2.000,00**. |
| 7 | Seleccionar `QA-PRM-055-V0-A`, abrir Ctrl+E, dejar 2 u y guardar. | `QA-PRM-055-V0-A` × 2 u: precio $1.000,00; automático $500,00; manual $0,00; neto $1.500,00; lista aplicada: precio normal<br>`QA-PRM-055-V0-B` × 1 u: precio $1.000,00; automático $250,00; manual $0,00; neto $750,00; lista aplicada: precio normal<br>`QA-PRM-055-V0-C` × 1 u: precio $1.000,00; automático $250,00; manual $0,00; neto $750,00; lista aplicada: precio normal | Total **$3.000,00**. |
| 8 | Seleccionar `QA-PRM-055-V0-C`, abrir Ctrl+E y elegir Eliminar. | `QA-PRM-055-V0-A` × 2 u: precio $1.000,00; automático $666,67; manual $0,00; neto $1.333,33; lista aplicada: precio normal<br>`QA-PRM-055-V0-B` × 1 u: precio $1.000,00; automático $333,33; manual $0,00; neto $666,67; lista aplicada: precio normal | Total **$2.000,00**. |
| 9 | Seleccionar `QA-PRM-055-V0-A`, abrir Ctrl+E, dejar 1 u y guardar. | `QA-PRM-055-V0-A` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal<br>`QA-PRM-055-V0-B` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal | Total **$2.000,00**. |
| 10 | Abandonar la venta y confirmar la salida sin cobrar. | Sin renglones en la operación. | Sin venta cobrada, pago ni cambios de stock o destino de cobro. |
| 11 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 12 | Cargar 1 u de `QA-PRM-055-V0-A` por código. | `QA-PRM-055-V0-A` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal | Total **$1.000,00**. |
| 13 | Cargar 1 u de `QA-PRM-055-V0-B` por código. | `QA-PRM-055-V0-A` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal<br>`QA-PRM-055-V0-B` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal | Total **$2.000,00**. |
| 14 | Cargar 1 u de `QA-PRM-055-V0-C` por código. | `QA-PRM-055-V0-A` × 1 u: precio $1.000,00; automático $333,33; manual $0,00; neto $666,67; lista aplicada: precio normal<br>`QA-PRM-055-V0-B` × 1 u: precio $1.000,00; automático $333,33; manual $0,00; neto $666,67; lista aplicada: precio normal<br>`QA-PRM-055-V0-C` × 1 u: precio $1.000,00; automático $333,34; manual $0,00; neto $666,66; lista aplicada: precio normal | Total **$2.000,00**. |
| 15 | Abrir cobro en efectivo del perfil QA, ingresar $2.000,00 y cancelar antes de confirmar. | `QA-PRM-055-V0-A` × 1 u: precio $1.000,00; automático $333,33; manual $0,00; neto $666,67; lista aplicada: precio normal<br>`QA-PRM-055-V0-B` × 1 u: precio $1.000,00; automático $333,33; manual $0,00; neto $666,67; lista aplicada: precio normal<br>`QA-PRM-055-V0-C` × 1 u: precio $1.000,00; automático $333,34; manual $0,00; neto $666,66; lista aplicada: precio normal | Total **$2.000,00**. Conserva toda la canasta; sin venta cobrada, pago ni movimientos. |
| 16 | Retomar el cobro en efectivo del perfil QA, ingresar $2.000,00 y confirmar una sola vez. | `QA-PRM-055-V0-A` × 1 u: precio $1.000,00; automático $333,33; manual $0,00; neto $666,67; lista aplicada: precio normal<br>`QA-PRM-055-V0-B` × 1 u: precio $1.000,00; automático $333,33; manual $0,00; neto $666,67; lista aplicada: precio normal<br>`QA-PRM-055-V0-C` × 1 u: precio $1.000,00; automático $333,34; manual $0,00; neto $666,66; lista aplicada: precio normal | Total **$2.000,00**. Una venta y un cobro en efectivo del perfil QA; vuelto cero. Stock: `QA-PRM-055-V0-A` −1 u; `QA-PRM-055-V0-B` −1 u; `QA-PRM-055-V0-C` −1 u. |

## Variante 2: agrupacion-off

### Productos preparados

| Referencia | Código | Precio base | Unidad | Familia / subfamilia / sector | Marca |
| --- | --- | ---: | --- | --- | --- |
| A | `QA-PRM-055-V1-A` | $1.000,00 | unidad | 986511 / 986511 / 986510 | QA-PRM-055-V1-MARCA |
| B | `QA-PRM-055-V1-B` | $1.000,00 | unidad | 986512 / 986512 / 986510 | QA-PRM-055-V1-MARCA |
| C | `QA-PRM-055-V1-C` | $1.000,00 | unidad | 986513 / 986513 / 986510 | QA-PRM-055-V1-MARCA |
| E | `QA-PRM-055-V1-E` | $1.000,00 | unidad | 986511 / 986511 / 986510 | QA-PRM-055-V1-MARCA-AJENA |

### Ofertas preparadas

| Oferta | Incluye | Regla | Agrupación | Estado / vigencia inclusiva | Medios habilitados |
| --- | --- | --- | --- | --- | --- |
| `QA-PRM-055-V1` | Marca `QA-PRM-055-V1-MARCA` | Llevar 3 y pagar 2 | OFF | Activa; hoy -365 días a hoy +365 días | Todos |

Las fechas se refieren a la fecha local usada al preparar el seed; Windows y MySQL deben coincidir. No se modifica el reloj durante el recorrido.

### Pasos y resultados esperados

| Paso | Acción del usuario | Canasta completa después del paso | Resultado |
| ---: | --- | --- | --- |
| 1 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 2 | Cargar 1 u de `QA-PRM-055-V1-A` por código. | `QA-PRM-055-V1-A` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal | Total **$1.000,00**. |
| 3 | Cargar 1 u de `QA-PRM-055-V1-B` por código. | `QA-PRM-055-V1-A` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal<br>`QA-PRM-055-V1-B` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal | Total **$2.000,00**. |
| 4 | Cargar 1 u de `QA-PRM-055-V1-C` por código. | `QA-PRM-055-V1-A` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal<br>`QA-PRM-055-V1-B` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal<br>`QA-PRM-055-V1-C` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal | Total **$3.000,00**. |
| 5 | Seleccionar `QA-PRM-055-V1-A`, abrir Ctrl+E, dejar 3 u y guardar. | `QA-PRM-055-V1-A` × 3 u: precio $1.000,00; automático $1.000,00; manual $0,00; neto $2.000,00; lista aplicada: precio normal<br>`QA-PRM-055-V1-B` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal<br>`QA-PRM-055-V1-C` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal | Total **$4.000,00**. |
| 6 | Abandonar la venta y confirmar la salida sin cobrar. | Sin renglones en la operación. | Sin venta cobrada, pago ni cambios de stock o destino de cobro. |

## Variante 3: precios-distintos

### Productos preparados

| Referencia | Código | Precio base | Unidad | Familia / subfamilia / sector | Marca |
| --- | --- | ---: | --- | --- | --- |
| A | `QA-PRM-055-V2-A` | $1.000,00 | unidad | 986521 / 986521 / 986520 | QA-PRM-055-V2-MARCA |
| B | `QA-PRM-055-V2-B` | $2.000,00 | unidad | 986522 / 986522 / 986520 | QA-PRM-055-V2-MARCA |
| C | `QA-PRM-055-V2-C` | $3.000,00 | unidad | 986523 / 986523 / 986520 | QA-PRM-055-V2-MARCA |
| E | `QA-PRM-055-V2-E` | $1.000,00 | unidad | 986521 / 986521 / 986520 | QA-PRM-055-V2-MARCA-AJENA |

### Ofertas preparadas

| Oferta | Incluye | Regla | Agrupación | Estado / vigencia inclusiva | Medios habilitados |
| --- | --- | --- | --- | --- | --- |
| `QA-PRM-055-V2` | Marca `QA-PRM-055-V2-MARCA` | Llevar 3 y pagar 2 | ON | Activa; hoy -365 días a hoy +365 días | Todos |

Las fechas se refieren a la fecha local usada al preparar el seed; Windows y MySQL deben coincidir. No se modifica el reloj durante el recorrido.

### Pasos y resultados esperados

| Paso | Acción del usuario | Canasta completa después del paso | Resultado |
| ---: | --- | --- | --- |
| 1 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 2 | Cargar 1 u de `QA-PRM-055-V2-A` por código. | `QA-PRM-055-V2-A` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal | Total **$1.000,00**. |
| 3 | Cargar 1 u de `QA-PRM-055-V2-B` por código. | `QA-PRM-055-V2-A` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal<br>`QA-PRM-055-V2-B` × 1 u: precio $2.000,00; automático $0,00; manual $0,00; neto $2.000,00; lista aplicada: precio normal | Total **$3.000,00**. |
| 4 | Cargar 1 u de `QA-PRM-055-V2-C` por código. | `QA-PRM-055-V2-A` × 1 u: precio $1.000,00; automático $333,33; manual $0,00; neto $666,67; lista aplicada: precio normal<br>`QA-PRM-055-V2-B` × 1 u: precio $2.000,00; automático $666,67; manual $0,00; neto $1.333,33; lista aplicada: precio normal<br>`QA-PRM-055-V2-C` × 1 u: precio $3.000,00; automático $1.000,00; manual $0,00; neto $2.000,00; lista aplicada: precio normal | Total **$4.000,00**. |
| 5 | Seleccionar `QA-PRM-055-V2-C`, abrir Ctrl+E y elegir Eliminar. | `QA-PRM-055-V2-A` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal<br>`QA-PRM-055-V2-B` × 1 u: precio $2.000,00; automático $0,00; manual $0,00; neto $2.000,00; lista aplicada: precio normal | Total **$3.000,00**. |
| 6 | Cargar 1 u de `QA-PRM-055-V2-C` por código. | `QA-PRM-055-V2-A` × 1 u: precio $1.000,00; automático $333,33; manual $0,00; neto $666,67; lista aplicada: precio normal<br>`QA-PRM-055-V2-B` × 1 u: precio $2.000,00; automático $666,67; manual $0,00; neto $1.333,33; lista aplicada: precio normal<br>`QA-PRM-055-V2-C` × 1 u: precio $3.000,00; automático $1.000,00; manual $0,00; neto $2.000,00; lista aplicada: precio normal | Total **$4.000,00**. |
| 7 | Abandonar la venta y confirmar la salida sin cobrar. | Sin renglones en la operación. | Sin venta cobrada, pago ni cambios de stock o destino de cobro. |

## Notas del recorrido

- Reparto manual con ajuste de centavos en la última línea.
- Los productos comparten o separan clasificaciones alternativas para detectar un alcance incorrecto.
- Validación sobre el JAR pendiente.

## Evidencia, recuperación y límites

Registrar cada variante y paso con esperado, observado, resultado y ubicación del informe privado. Conservar cantidades, precios, descuentos y netos visibles; comprobar por identidad de la operación venta, detalle, oferta, lista aplicada, medio, stock y destino de cobro. Cancelar o abandonar no debe crear esos efectos; confirmar produce una sola operación. No se deduce el número de filas de pago sin el contrato de cobro simple del perfil.

Ante una discrepancia, conservar evidencia y detener la confirmación. Finalizar únicamente el JAR del runner; restaurar el baseline antes de repetir. No corregir importes o movimientos en la base para conseguir un resultado aprobado. INFO resume; DEBUG muestra los pasos; TRACE añade diagnóstico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia; causa no determinada si no está demostrada.

La automatización y su dry-run no acreditan ejecución real. No cubre producción, emisión fiscal, impresoras, balanzas, pasarelas de pago, red ni concurrencia. Las variantes descritas solamente en el diseño original deben contrastarse antes de acreditarlas como cubiertas.

## Trazabilidad de la automatización

- Fuente ERP de las expectativas: commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Las rutas y tests de reglas están preservados en el anexo original; no son evidencia de ejecución sobre el JAR.
- Contrato de datos y pasos: [catálogo de recorridos](../../offer_journeys/catalog.py).
- Identidad de ofertas, precios y deltas: [oráculos de lectura](../../offer_journeys/oracles.py).
- Mantener SHA256/build del JAR, paquete, perfil, versión de datos, fecha y responsable en evidencia privada; no publicar credenciales, filas completas, capturas de autenticación ni árboles privados.
- Regenerar desde la raíz: `python scripts/update-offer-journey-docs.py`; comprobar sincronización con `python scripts/update-offer-journey-docs.py --check`.

<!-- END GENERATED OFFER JOURNEY -->

<details>
<summary>Diseño funcional original: referencia histórica y variantes a contrastar</summary>

Este bloque conserva el diseño previo completo. Sus menciones de estado, seed pendiente o ausencia de Robot son históricas; el contrato actual está en las tablas anteriores. Una variante adicional de este bloque no se considera ejecutada por aparecer documentada.

<!-- BEGIN ORIGINAL OFFER DESIGN -->
## Estado y alcance

**Pendiente de automatizar (`planned`), prioridad P1, etapa 2.** No hay test Robot asociado ni validación real del JAR. Fórmula `C`: lleva 3 unidades y paga 2, sumando los productos incluidos. Consultar el [índice de pendientes](../../docs/promociones-pendientes.md). Agrupación de productos distintos solo se contempla para familia, subfamilia y marca.

## Precondiciones y datos

- Windows QA exclusivo y offline; paquete autorizado, baseline restaurable y JAR identificado. Usuario vendedor con permiso de carga/edición/cobro y abandono sin supervisor. Empresa, sucursal y puesto propios, stock suficiente.
- ARS, precio base $1.000,00 por unidad para A, B, C y Ajeno; unidades enteras, IVA 0 %, sin otros impuestos. Comprobante interno 99, efectivo exacto, diálogo de cobro habilitado, sin impresión ni fiscalización.
- Lista **Ninguna Lista** (ID 0); cliente/turno sin lista automática, otros descuentos/recargos en cero y fidelización deshabilitada. Oferta activa y vigente para la sucursal QA y todos los medios de pago. No hay combos ni ofertas superpuestas.
- **NUEVO PENDIENTE DE PREPARAR:** perfil QA-XG-PRM-055, productos A y B y C exclusivos de una misma marca, un producto Ajeno de otra marca y la oferta indicada. Son nombres funcionales propuestos, sin IDs asignados ni filas disponibles en el seed actual. Preparar dos copias del perfil: agrupación activada y desactivada, con idénticos datos y una sola regla comercial.
- A y B tienen exactamente la misma marca no vacía. Ajeno tiene otra marca aunque comparta familia/subfamilia; no usar una diferencia de precio para explicar su exclusión. C también pertenece al grupo elegido.
- La agrupación se cambia en la preparación de cada perfil independiente, nunca mientras una venta está abierta ni mediante una escritura para forzar el esperado. Requiere preparación/calibración de perfiles y controles accesibles; aún pendientes. Los datos propuestos no se aplican en esta entrega.

## Pasos y resultados esperados

1. Abrir una venta vacía con el perfil de agrupación **activada** y cargar A ×1. **Esperado:** bruto $1.000,00, oferta $0,00, neto $1.000,00: una unidad no completa el 3x2.

2. Agregar Ajeno ×1. **Esperado:** total $2.000,00, oferta $0,00; Ajeno no suma unidades al grupo. Agregar B ×1 manteniendo Ajeno. **Esperado:** bruto $3.000,00, oferta $0,00, neto $3.000,00: hay solo dos unidades elegibles aunque la venta tenga tres.

3. Quitar Ajeno y agregar C ×1. **Esperado:** A ×1 + B ×1 + C ×1, bruto $3.000,00, descuento total $1.000,00, neto $2.000,00. La suma de descuentos por línea es exactamente $1.000,00; no se exige repartir un tercio de centavo ni regalar arbitrariamente una fila.

4. Editar A a ×2. **Esperado:** cuatro unidades elegibles, bruto $4.000,00, descuento $1.000,00 y neto $3.000,00; la unidad sobrante no crea un segundo bloque. Quitar C. **Esperado:** A ×2 + B ×1, bruto $3.000,00, descuento $1.000,00, neto $2.000,00.

5. Reducir A a ×1. **Esperado:** A ×1 + B ×1, bruto/neto $2.000,00, descuento $0,00; el beneficio anterior desaparece. Abandonar y confirmar. **Esperado:** ninguna venta cobrada ni cambios de stock/caja.

6. En una ejecución independiente restaurada, usar la copia con agrupación **desactivada**. Cargar A ×1 + B ×1 + C ×1. **Esperado:** bruto/neto $3.000,00, descuento $0,00. Cambiar A a ×3. **Esperado:** bruto $5.000,00, descuento $1.000,00, neto $4.000,00: A alcanza por sí solo el 3x2; B y C siguen sin descuento. Abandonar sin efectos.

7. Variante independiente con agrupación activada y precios A=$1.000,00, B=$2.000,00, C=$3.000,00, todos ×1, datos **NUEVO PENDIENTE DE PREPARAR**. **Esperado:** bruto $6.000,00, ahorro $2.000,00, neto $4.000,00; descuentos A=$333,33, B=$666,67, C=$1.000,00. Es descuento proporcional al importe, no «se regala el más barato». Quitar C deja bruto/neto $3.000,00 sin oferta; volver a cargarlo recupera $4.000,00. Abandonar sin efectos.

8. Restaurar el perfil inicial agrupado con los tres precios de $1.000,00 y cargar A ×1 + B ×1 + C ×1. Abrir y cancelar el cobro. **Esperado:** conserva neto $2.000,00, no registra venta cobrada ni mueve stock/caja. Retomar y cobrar una vez $2.000,00 en efectivo. **Esperado:** una sola venta y cobro, caja +$2.000,00, stock A −1, B −1, C −1; Ajeno sin cambios.

## Evidencia y límites

Guardar identidad visible de los artículos, condición de agrupación del perfil, cantidades y bruto/oferta/neto en cada transición, incluyendo Ajeno, cancelación y cobro final. Los importes anteriores son expectativas calculadas manualmente desde la regla, no resultados de ejecución. Verificar la suma del descuento y del neto de las filas contra el total; una etiqueta porcentual aislada no prueba el importe. Esta ficha no cubre fracciones, listas, otros medios de pago, cruces de ofertas ni Restobar.

## Recuperación

Cancelar el cobro debe volver al mismo contenido e importe. Abandonar las variantes previas no debe producir una venta cobrada ni movimientos de stock/caja. Conservar evidencia privada ante un fallo antes de restaurar el perfil; no borrar ni corregir operaciones en la base. La siguiente variante comienza desde su baseline controlado y no reutiliza la venta anterior.

## Anexo técnico y trazabilidad

Fuente ERP verificada: commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; `src/ModuloFinanzas/Entidades/OfertaAplicacionCalculador.java`, `test/ModuloFinanzas/Entidades/OfertaAplicacionCalculadorAgrupacionTest.java` (siete tipos por familia/subfamilia/marca y agrupación desactivada), `test/ModuloFinanzas/Entidades/OfertaLlevaXPagaXTest.java`. La configuración agrupada está en `Configuracion.agrupada`; no habilitarla por sector o para combinar productos ajenos. El caso de precios diferentes deriva de `llevaTresPagaDosUsaBaseProporcionalConPreciosDistintos`, escalado por diez.

Selectores para edición por teclado, eliminación y comprobación de oferta pendientes de verificar en el JAR recibido. Contrastar operación e identidad con lecturas acotadas: `vecTotal` bruto, `vecOferta` descuento automático, `venTotal` neto; sin descuentos adicionales, un cobro final y deltas de stock/caja declarados. No imprimir filas completas ni datos privados. Registrar SHA256/build del JAR, paquete, perfil, versión de datos y fecha. INFO resume, DEBUG muestra pasos y TRACE diagnóstico saneado. Un fallo siempre informa paso, esperado, observado, categoría y evidencia; causa no determinada si no está demostrada.
<!-- END ORIGINAL OFFER DESIGN -->

</details>
