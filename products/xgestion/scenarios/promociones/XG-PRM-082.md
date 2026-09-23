---
{"id":"XG-PRM-082","title":"Cobrar precio final USD 50 por subfamilia","product":"xgestion","module":"promociones","priority":"P0","tags":["xgestion","regression","promociones","promociones-alcances","ofertas-subfamilia","ofertas-usd","p0","escritura"],"status":"implemented","test":"products/xgestion/suites/ofertas/usd.robot","seed":"catalogo-comercial-v1"}
---

# XG-PRM-082 — Precio final USD 50 por subfamilia

## Objetivo

Como vendedor, cobrar el precio promocional en la moneda del producto y su equivalente correcto en pesos.

<!-- BEGIN GENERATED OFFER JOURNEY -->

## Recorrido de automatización

Estado del catálogo: **implemented**. Automatización catalogada en [`usd.robot`](../../suites/ofertas/usd.robot). Validación real: **pendiente**; requiere ejecutar el JAR exacto en el laboratorio calibrado.

Las tablas siguientes son los datos y pasos actuales del recorrido. Los importes son expectativas fijas, no resultados medidos. El diseño anterior queda al final como referencia histórica para conservar reglas, variantes y límites; sus estados y códigos no describen la implementación actual.

```powershell
.\qa.cmd run --product xgestion --scenario XG-PRM-082 --seed catalogo-comercial-v1 --log-level DEBUG
```

## Perfil y preparación

Windows QA exclusivo y offline, escritorio desbloqueado, paquete autorizado y baseline restaurable. Productos y renglones USD; comprobante y cobro ARS; cotización 1500 ARS/USD. IVA 0 %, comprobante interno 99, stock suficiente, sin impresión ni fiscalización. Cliente y turno sin listas automáticas; otros descuentos, recargos y fidelización deshabilitados, salvo lo indicado en cada variante.

Preparar mediante el runner y `catalogo-comercial-v1` antes de abrir el JAR. Los códigos públicos de abajo pertenecen a este recorrido y reemplazan los ejemplos genéricos del diseño original. No cambiar reglas mediante SQL durante la venta. La falta de perfil, seed o calibración accesible se informa como bloqueo.

Cada variante inicia el JAR de forma independiente. Los perfiles de configuración de 070 y 079 además requieren su preparación y restauración por fase. Una misma ficha conserva un solo ID lógico; solo queda aprobada si todas las variantes requeridas producen evidencia completa.

**Lectura de importes:** automático y manual son descuentos totales del renglón. La grilla muestra ambos sumados en Descuentos; el informe y la evidencia de persistencia los distinguen. El neto de todos los renglones debe sumar el total de la venta.

**P0.** Requiere [calibración ofertas-usd-v1](../../docs/ofertas-usd.md). En la canasta de abajo, $ indica ARS operativos; la grilla muestra los originales USD. No convertir el precio promocional 50 a pesos en el seed. Fallo o bloqueo impide acreditar aceptación de ofertas.

## Variante 1: desde-una-unidad

### Productos preparados

| Referencia | Código | Precio base | Unidad | Familia / subfamilia / sector | Marca |
| --- | --- | ---: | --- | --- | --- |
| A | `QA-PRM-082-V0-A` | USD 100,00 | unidad | 989200 / 989200 / 989201 | QA-PRM-082-V0-MARCA-1 |
| B | `QA-PRM-082-V0-B` | USD 100,00 | unidad | 989200 / 989200 / 989202 | QA-PRM-082-V0-MARCA-2 |
| E | `QA-PRM-082-V0-E` | USD 100,00 | unidad | 989200 / 989209 / 989201 | QA-PRM-082-V0-MARCA-1 |

### Ofertas preparadas

| Oferta | Incluye | Regla | Agrupación | Estado / vigencia inclusiva | Medios habilitados |
| --- | --- | --- | --- | --- | --- |
| `QA-PRM-082-V0` | Subfamilia `989200` | Desde 1: precio final USD 50,00 por unidad | OFF | Activa; hoy -365 días a hoy +365 días | Todos |

Las fechas se refieren a la fecha local usada al preparar el seed; Windows y MySQL deben coincidir. No se modifica el reloj durante el recorrido.

### Pasos y resultados esperados

| Paso | Acción del usuario | Canasta completa después del paso | Resultado |
| ---: | --- | --- | --- |
| 1 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 2 | Cargar 1 u de `QA-PRM-082-V0-A` por código. | `QA-PRM-082-V0-A` × 1 u: precio $150.000,00; automático $75.000,00; manual $0,00; neto $75.000,00; original USD: precio USD 100,00, descuento USD 50,00; lista aplicada: precio normal | Total **$75.000,00**. |
| 3 | Seleccionar `QA-PRM-082-V0-A`, abrir Ctrl+E, dejar 2 u y guardar. | `QA-PRM-082-V0-A` × 2 u: precio $150.000,00; automático $150.000,00; manual $0,00; neto $150.000,00; original USD: precio USD 100,00, descuento USD 100,00; lista aplicada: precio normal | Total **$150.000,00**. |
| 4 | Seleccionar `QA-PRM-082-V0-A`, abrir Ctrl+E, dejar 1 u y guardar. | `QA-PRM-082-V0-A` × 1 u: precio $150.000,00; automático $75.000,00; manual $0,00; neto $75.000,00; original USD: precio USD 100,00, descuento USD 50,00; lista aplicada: precio normal | Total **$75.000,00**. |
| 5 | Cargar 1 u de `QA-PRM-082-V0-E` por código. | `QA-PRM-082-V0-A` × 1 u: precio $150.000,00; automático $75.000,00; manual $0,00; neto $75.000,00; original USD: precio USD 100,00, descuento USD 50,00; lista aplicada: precio normal<br>`QA-PRM-082-V0-E` × 1 u: precio $150.000,00; automático $0,00; manual $0,00; neto $150.000,00; original USD: precio USD 100,00, descuento USD 0,00; lista aplicada: precio normal | Total **$225.000,00**. |
| 6 | Seleccionar `QA-PRM-082-V0-E`, abrir Ctrl+E y elegir Eliminar. | `QA-PRM-082-V0-A` × 1 u: precio $150.000,00; automático $75.000,00; manual $0,00; neto $75.000,00; original USD: precio USD 100,00, descuento USD 50,00; lista aplicada: precio normal | Total **$75.000,00**. |
| 7 | Cargar 1 u de `QA-PRM-082-V0-B` por código. | `QA-PRM-082-V0-A` × 1 u: precio $150.000,00; automático $75.000,00; manual $0,00; neto $75.000,00; original USD: precio USD 100,00, descuento USD 50,00; lista aplicada: precio normal<br>`QA-PRM-082-V0-B` × 1 u: precio $150.000,00; automático $75.000,00; manual $0,00; neto $75.000,00; original USD: precio USD 100,00, descuento USD 50,00; lista aplicada: precio normal | Total **$150.000,00**. |
| 8 | Seleccionar `QA-PRM-082-V0-B`, abrir Ctrl+E y elegir Eliminar. | `QA-PRM-082-V0-A` × 1 u: precio $150.000,00; automático $75.000,00; manual $0,00; neto $75.000,00; original USD: precio USD 100,00, descuento USD 50,00; lista aplicada: precio normal | Total **$75.000,00**. |
| 9 | Abrir cobro en efectivo del perfil QA, ingresar $75.000,00 y cancelar antes de confirmar. | `QA-PRM-082-V0-A` × 1 u: precio $150.000,00; automático $75.000,00; manual $0,00; neto $75.000,00; original USD: precio USD 100,00, descuento USD 50,00; lista aplicada: precio normal | Total **$75.000,00**. Conserva toda la canasta; sin venta cobrada, pago ni movimientos. |
| 10 | Retomar el cobro en efectivo del perfil QA, ingresar $75.000,00 y confirmar una sola vez. | `QA-PRM-082-V0-A` × 1 u: precio $150.000,00; automático $75.000,00; manual $0,00; neto $75.000,00; original USD: precio USD 100,00, descuento USD 50,00; lista aplicada: precio normal | Total **$75.000,00**. Una venta y un cobro en efectivo del perfil QA; vuelto cero. Stock: `QA-PRM-082-V0-A` −1 u. |

## Variante 2: desde-dos-sin-agrupar

### Productos preparados

| Referencia | Código | Precio base | Unidad | Familia / subfamilia / sector | Marca |
| --- | --- | ---: | --- | --- | --- |
| A | `QA-PRM-082-V1-A` | USD 100,00 | unidad | 989210 / 989210 / 989211 | QA-PRM-082-V1-MARCA-1 |
| B | `QA-PRM-082-V1-B` | USD 100,00 | unidad | 989210 / 989210 / 989212 | QA-PRM-082-V1-MARCA-2 |
| E | `QA-PRM-082-V1-E` | USD 100,00 | unidad | 989210 / 989219 / 989211 | QA-PRM-082-V1-MARCA-1 |

### Ofertas preparadas

| Oferta | Incluye | Regla | Agrupación | Estado / vigencia inclusiva | Medios habilitados |
| --- | --- | --- | --- | --- | --- |
| `QA-PRM-082-V1` | Subfamilia `989210` | Desde 2: precio final USD 50,00 por unidad | OFF | Activa; hoy -365 días a hoy +365 días | Todos |

Las fechas se refieren a la fecha local usada al preparar el seed; Windows y MySQL deben coincidir. No se modifica el reloj durante el recorrido.

### Pasos y resultados esperados

| Paso | Acción del usuario | Canasta completa después del paso | Resultado |
| ---: | --- | --- | --- |
| 1 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 2 | Cargar 1 u de `QA-PRM-082-V1-A` por código. | `QA-PRM-082-V1-A` × 1 u: precio $150.000,00; automático $0,00; manual $0,00; neto $150.000,00; original USD: precio USD 100,00, descuento USD 0,00; lista aplicada: precio normal | Total **$150.000,00**. |
| 3 | Seleccionar `QA-PRM-082-V1-A`, abrir Ctrl+E, dejar 2 u y guardar. | `QA-PRM-082-V1-A` × 2 u: precio $150.000,00; automático $150.000,00; manual $0,00; neto $150.000,00; original USD: precio USD 100,00, descuento USD 100,00; lista aplicada: precio normal | Total **$150.000,00**. |
| 4 | Seleccionar `QA-PRM-082-V1-A`, abrir Ctrl+E, dejar 1 u y guardar. | `QA-PRM-082-V1-A` × 1 u: precio $150.000,00; automático $0,00; manual $0,00; neto $150.000,00; original USD: precio USD 100,00, descuento USD 0,00; lista aplicada: precio normal | Total **$150.000,00**. |
| 5 | Cargar 1 u de `QA-PRM-082-V1-E` por código. | `QA-PRM-082-V1-A` × 1 u: precio $150.000,00; automático $0,00; manual $0,00; neto $150.000,00; original USD: precio USD 100,00, descuento USD 0,00; lista aplicada: precio normal<br>`QA-PRM-082-V1-E` × 1 u: precio $150.000,00; automático $0,00; manual $0,00; neto $150.000,00; original USD: precio USD 100,00, descuento USD 0,00; lista aplicada: precio normal | Total **$300.000,00**. |
| 6 | Seleccionar `QA-PRM-082-V1-E`, abrir Ctrl+E y elegir Eliminar. | `QA-PRM-082-V1-A` × 1 u: precio $150.000,00; automático $0,00; manual $0,00; neto $150.000,00; original USD: precio USD 100,00, descuento USD 0,00; lista aplicada: precio normal | Total **$150.000,00**. |
| 7 | Cargar 1 u de `QA-PRM-082-V1-B` por código. | `QA-PRM-082-V1-A` × 1 u: precio $150.000,00; automático $0,00; manual $0,00; neto $150.000,00; original USD: precio USD 100,00, descuento USD 0,00; lista aplicada: precio normal<br>`QA-PRM-082-V1-B` × 1 u: precio $150.000,00; automático $0,00; manual $0,00; neto $150.000,00; original USD: precio USD 100,00, descuento USD 0,00; lista aplicada: precio normal | Total **$300.000,00**. |
| 8 | Seleccionar `QA-PRM-082-V1-A`, abrir Ctrl+E, dejar 2 u y guardar. | `QA-PRM-082-V1-A` × 2 u: precio $150.000,00; automático $150.000,00; manual $0,00; neto $150.000,00; original USD: precio USD 100,00, descuento USD 100,00; lista aplicada: precio normal<br>`QA-PRM-082-V1-B` × 1 u: precio $150.000,00; automático $0,00; manual $0,00; neto $150.000,00; original USD: precio USD 100,00, descuento USD 0,00; lista aplicada: precio normal | Total **$300.000,00**. |
| 9 | Seleccionar `QA-PRM-082-V1-A`, abrir Ctrl+E, dejar 1 u y guardar. | `QA-PRM-082-V1-A` × 1 u: precio $150.000,00; automático $0,00; manual $0,00; neto $150.000,00; original USD: precio USD 100,00, descuento USD 0,00; lista aplicada: precio normal<br>`QA-PRM-082-V1-B` × 1 u: precio $150.000,00; automático $0,00; manual $0,00; neto $150.000,00; original USD: precio USD 100,00, descuento USD 0,00; lista aplicada: precio normal | Total **$300.000,00**. |
| 10 | Seleccionar `QA-PRM-082-V1-B`, abrir Ctrl+E y elegir Eliminar. | `QA-PRM-082-V1-A` × 1 u: precio $150.000,00; automático $0,00; manual $0,00; neto $150.000,00; original USD: precio USD 100,00, descuento USD 0,00; lista aplicada: precio normal | Total **$150.000,00**. |
| 11 | Seleccionar `QA-PRM-082-V1-A`, abrir Ctrl+E, dejar 2 u y guardar. | `QA-PRM-082-V1-A` × 2 u: precio $150.000,00; automático $150.000,00; manual $0,00; neto $150.000,00; original USD: precio USD 100,00, descuento USD 100,00; lista aplicada: precio normal | Total **$150.000,00**. |
| 12 | Abrir cobro en efectivo del perfil QA, ingresar $150.000,00 y cancelar antes de confirmar. | `QA-PRM-082-V1-A` × 2 u: precio $150.000,00; automático $150.000,00; manual $0,00; neto $150.000,00; original USD: precio USD 100,00, descuento USD 100,00; lista aplicada: precio normal | Total **$150.000,00**. Conserva toda la canasta; sin venta cobrada, pago ni movimientos. |
| 13 | Retomar el cobro en efectivo del perfil QA, ingresar $150.000,00 y confirmar una sola vez. | `QA-PRM-082-V1-A` × 2 u: precio $150.000,00; automático $150.000,00; manual $0,00; neto $150.000,00; original USD: precio USD 100,00, descuento USD 100,00; lista aplicada: precio normal | Total **$150.000,00**. Una venta y un cobro en efectivo del perfil QA; vuelto cero. Stock: `QA-PRM-082-V1-A` −2 u. |

## Variante 3: desde-dos-agrupadas

### Productos preparados

| Referencia | Código | Precio base | Unidad | Familia / subfamilia / sector | Marca |
| --- | --- | ---: | --- | --- | --- |
| A | `QA-PRM-082-V2-A` | USD 100,00 | unidad | 989220 / 989220 / 989221 | QA-PRM-082-V2-MARCA-1 |
| B | `QA-PRM-082-V2-B` | USD 100,00 | unidad | 989220 / 989220 / 989222 | QA-PRM-082-V2-MARCA-2 |
| E | `QA-PRM-082-V2-E` | USD 100,00 | unidad | 989220 / 989229 / 989221 | QA-PRM-082-V2-MARCA-1 |

### Ofertas preparadas

| Oferta | Incluye | Regla | Agrupación | Estado / vigencia inclusiva | Medios habilitados |
| --- | --- | --- | --- | --- | --- |
| `QA-PRM-082-V2` | Subfamilia `989220` | Desde 2: precio final USD 50,00 por unidad | ON | Activa; hoy -365 días a hoy +365 días | Todos |

Las fechas se refieren a la fecha local usada al preparar el seed; Windows y MySQL deben coincidir. No se modifica el reloj durante el recorrido.

### Pasos y resultados esperados

| Paso | Acción del usuario | Canasta completa después del paso | Resultado |
| ---: | --- | --- | --- |
| 1 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 2 | Cargar 1 u de `QA-PRM-082-V2-A` por código. | `QA-PRM-082-V2-A` × 1 u: precio $150.000,00; automático $0,00; manual $0,00; neto $150.000,00; original USD: precio USD 100,00, descuento USD 0,00; lista aplicada: precio normal | Total **$150.000,00**. |
| 3 | Seleccionar `QA-PRM-082-V2-A`, abrir Ctrl+E, dejar 2 u y guardar. | `QA-PRM-082-V2-A` × 2 u: precio $150.000,00; automático $150.000,00; manual $0,00; neto $150.000,00; original USD: precio USD 100,00, descuento USD 100,00; lista aplicada: precio normal | Total **$150.000,00**. |
| 4 | Seleccionar `QA-PRM-082-V2-A`, abrir Ctrl+E, dejar 1 u y guardar. | `QA-PRM-082-V2-A` × 1 u: precio $150.000,00; automático $0,00; manual $0,00; neto $150.000,00; original USD: precio USD 100,00, descuento USD 0,00; lista aplicada: precio normal | Total **$150.000,00**. |
| 5 | Cargar 1 u de `QA-PRM-082-V2-E` por código. | `QA-PRM-082-V2-A` × 1 u: precio $150.000,00; automático $0,00; manual $0,00; neto $150.000,00; original USD: precio USD 100,00, descuento USD 0,00; lista aplicada: precio normal<br>`QA-PRM-082-V2-E` × 1 u: precio $150.000,00; automático $0,00; manual $0,00; neto $150.000,00; original USD: precio USD 100,00, descuento USD 0,00; lista aplicada: precio normal | Total **$300.000,00**. |
| 6 | Seleccionar `QA-PRM-082-V2-E`, abrir Ctrl+E y elegir Eliminar. | `QA-PRM-082-V2-A` × 1 u: precio $150.000,00; automático $0,00; manual $0,00; neto $150.000,00; original USD: precio USD 100,00, descuento USD 0,00; lista aplicada: precio normal | Total **$150.000,00**. |
| 7 | Cargar 1 u de `QA-PRM-082-V2-B` por código. | `QA-PRM-082-V2-A` × 1 u: precio $150.000,00; automático $75.000,00; manual $0,00; neto $75.000,00; original USD: precio USD 100,00, descuento USD 50,00; lista aplicada: precio normal<br>`QA-PRM-082-V2-B` × 1 u: precio $150.000,00; automático $75.000,00; manual $0,00; neto $75.000,00; original USD: precio USD 100,00, descuento USD 50,00; lista aplicada: precio normal | Total **$150.000,00**. |
| 8 | Seleccionar `QA-PRM-082-V2-A`, abrir Ctrl+E, dejar 2 u y guardar. | `QA-PRM-082-V2-A` × 2 u: precio $150.000,00; automático $150.000,00; manual $0,00; neto $150.000,00; original USD: precio USD 100,00, descuento USD 100,00; lista aplicada: precio normal<br>`QA-PRM-082-V2-B` × 1 u: precio $150.000,00; automático $75.000,00; manual $0,00; neto $75.000,00; original USD: precio USD 100,00, descuento USD 50,00; lista aplicada: precio normal | Total **$225.000,00**. |
| 9 | Seleccionar `QA-PRM-082-V2-A`, abrir Ctrl+E, dejar 1 u y guardar. | `QA-PRM-082-V2-A` × 1 u: precio $150.000,00; automático $75.000,00; manual $0,00; neto $75.000,00; original USD: precio USD 100,00, descuento USD 50,00; lista aplicada: precio normal<br>`QA-PRM-082-V2-B` × 1 u: precio $150.000,00; automático $75.000,00; manual $0,00; neto $75.000,00; original USD: precio USD 100,00, descuento USD 50,00; lista aplicada: precio normal | Total **$150.000,00**. |
| 10 | Seleccionar `QA-PRM-082-V2-B`, abrir Ctrl+E y elegir Eliminar. | `QA-PRM-082-V2-A` × 1 u: precio $150.000,00; automático $0,00; manual $0,00; neto $150.000,00; original USD: precio USD 100,00, descuento USD 0,00; lista aplicada: precio normal | Total **$150.000,00**. |
| 11 | Seleccionar `QA-PRM-082-V2-A`, abrir Ctrl+E, dejar 2 u y guardar. | `QA-PRM-082-V2-A` × 2 u: precio $150.000,00; automático $150.000,00; manual $0,00; neto $150.000,00; original USD: precio USD 100,00, descuento USD 100,00; lista aplicada: precio normal | Total **$150.000,00**. |
| 12 | Abrir cobro en efectivo del perfil QA, ingresar $150.000,00 y cancelar antes de confirmar. | `QA-PRM-082-V2-A` × 2 u: precio $150.000,00; automático $150.000,00; manual $0,00; neto $150.000,00; original USD: precio USD 100,00, descuento USD 100,00; lista aplicada: precio normal | Total **$150.000,00**. Conserva toda la canasta; sin venta cobrada, pago ni movimientos. |
| 13 | Retomar el cobro en efectivo del perfil QA, ingresar $150.000,00 y confirmar una sola vez. | `QA-PRM-082-V2-A` × 2 u: precio $150.000,00; automático $150.000,00; manual $0,00; neto $150.000,00; original USD: precio USD 100,00, descuento USD 100,00; lista aplicada: precio normal | Total **$150.000,00**. Una venta y un cobro en efectivo del perfil QA; vuelto cero. Stock: `QA-PRM-082-V2-A` −2 u. |

## Notas del recorrido

- P0: USD 100 con precio final USD 50; no reemplazar Paga=50 por 75000 en el seed.
- Cotización 1500 ARS/USD. Renglones USD, documento interno y cobro ARS, IVA 0 %.
- Un fallo o bloqueo mantiene pendiente la aceptación del circuito de ofertas.

## Evidencia, recuperación y límites

Registrar cada variante y paso con esperado, observado, resultado y ubicación del informe privado. Conservar cantidades, precios, descuentos y netos visibles; comprobar por identidad de la operación venta, detalle, oferta, lista aplicada, medio, stock y destino de cobro. Cancelar o abandonar no debe crear esos efectos; confirmar produce una sola operación. No se deduce el número de filas de pago sin el contrato de cobro simple del perfil.

Ante una discrepancia, conservar evidencia y detener la confirmación. Finalizar únicamente el JAR del runner; restaurar el baseline antes de repetir. No corregir importes o movimientos en la base para conseguir un resultado aprobado. INFO resume; DEBUG muestra los pasos; TRACE añade diagnóstico saneado. Un fallo informa paso, esperado, observado, categoría y evidencia; causa no determinada si no está demostrada.

La automatización y su dry-run no acreditan ejecución real. No cubre producción, emisión fiscal, impresoras, balanzas, pasarelas de pago, red ni concurrencia. Las variantes descritas solamente en el diseño original deben contrastarse antes de acreditarlas como cubiertas.

## Trazabilidad de la automatización

- Fuente ERP del contrato técnico: commit `39d6b6d64b12205fbabe29222f72679e875f7031`; la regla USD 50 proviene del incidente y del plan aprobado. Las rutas y tests están preservados en el anexo original; no son evidencia de ejecución sobre el JAR.
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

P0 del incidente USD 100, precio final USD 50 y cotización 1500: el total debe ser ARS 75000, no ARS 50. Automatizar según el plan aprobado; validación real pendiente.

## Variantes

Desde una y desde dos unidades; cargar y editar cantidades, agregar/quitar producto ajeno, cancelar y retomar cobro. Dos productos de la categoría; agrupación ON y OFF desde dos unidades.

## Trazabilidad técnica

Contrato fuente ERP `39d6b6d64b12205fbabe29222f72679e875f7031`: `src/ModuloVentas/Vistas/FormVenta.java`, `src/ModuloVentas/Entidades/TicketVenta.java`, `src/ModuloVentas/Entidades/VentaDetalle.java`, `src/ModuloFinanzas/Entidades/Oferta.java`, `src/ModuloFinanzas/Entidades/OfertaLineaService.java`.

Tests de referencia: `test/ModuloFinanzas/Entidades/OfertaCantidadMayorPrecioUnitarioTest.java` y `test/ModuloVentas/Entidades/TicketVentaPresupuestoCotizacionTest.java`. Sus comprobaciones previas no acreditan este incidente; la expectativa monetaria proviene del plan aprobado.

Ver [perfil, evidencia y recuperación](../../docs/ofertas-usd.md).
<!-- END ORIGINAL OFFER DESIGN -->

</details>
