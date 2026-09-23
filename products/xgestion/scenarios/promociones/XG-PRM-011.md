---
{"id":"XG-PRM-011","title":"Aplicar el 10 % por familia","product":"xgestion","module":"promociones","tags":["xgestion","regression","promociones","promociones-alcances","ofertas-familia","escritura"],"status":"implemented","test":"products/xgestion/suites/ofertas/familia.robot","seed":"catalogo-comercial-v1"}
---

# XG-PRM-011 — Aplicar el 10 % por familia

## Objetivo

El vendedor comprueba 10 % de descuento por familia, distingue los productos incluidos de los ajenos y conserva el importe correcto al corregir cantidades y retomar un cobro.

<!-- BEGIN GENERATED OFFER JOURNEY -->

## Recorrido de automatización

Estado del catálogo: **implemented**. Automatización catalogada en [`familia.robot`](../../suites/ofertas/familia.robot). Validación real: **pendiente**; requiere ejecutar el JAR exacto en el laboratorio calibrado.

Las tablas siguientes son los datos y pasos actuales del recorrido. Los importes son expectativas fijas, no resultados medidos. El diseño anterior queda al final como referencia histórica para conservar reglas, variantes y límites; sus estados y códigos no describen la implementación actual.

```powershell
.\qa.cmd run --product xgestion --scenario XG-PRM-011 --seed catalogo-comercial-v1 --log-level DEBUG
```

## Perfil y preparación

Windows QA exclusivo y offline, escritorio desbloqueado, paquete autorizado y baseline restaurable. ARS, IVA 0 %, comprobante interno 99, stock suficiente, sin impresión ni fiscalización. Cliente y turno sin listas automáticas; otros descuentos, recargos y fidelización deshabilitados, salvo lo indicado en cada variante.

Preparar mediante el runner y `catalogo-comercial-v1` antes de abrir el JAR. Los códigos públicos de abajo pertenecen a este recorrido y reemplazan los ejemplos genéricos del diseño original. No cambiar reglas mediante SQL durante la venta. La falta de perfil, seed o calibración accesible se informa como bloqueo.

Cada variante inicia el JAR de forma independiente. Los perfiles de configuración de 070 y 079 además requieren su preparación y restauración por fase. Una misma ficha conserva un solo ID lógico; solo queda aprobada si todas las variantes requeridas producen evidencia completa.

**Lectura de importes:** automático y manual son descuentos totales del renglón. La grilla muestra ambos sumados en Descuentos; el informe y la evidencia de persistencia los distinguen. El neto de todos los renglones debe sumar el total de la venta.

## Variante 1: principal

### Productos preparados

| Referencia | Código | Precio base | Unidad | Familia / subfamilia / sector | Marca |
| --- | --- | ---: | --- | --- | --- |
| A | `QA-PRM-011-A` | $1.000,00 | unidad | 982100 / 982101 / 980001 | QA-SEED |
| B | `QA-PRM-011-B` | $1.000,00 | unidad | 982100 / 982102 / 980001 | QA-SEED |
| E | `QA-PRM-011-E` | $1.000,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |

### Ofertas preparadas

| Oferta | Incluye | Regla | Agrupación | Estado / vigencia inclusiva | Medios habilitados |
| --- | --- | --- | --- | --- | --- |
| `QA-PRM-011` | Familia `982100` | 10 % sobre el importe | OFF | Activa; hoy -365 días a hoy +365 días | Todos |

Las fechas se refieren a la fecha local usada al preparar el seed; Windows y MySQL deben coincidir. No se modifica el reloj durante el recorrido.

### Pasos y resultados esperados

| Paso | Acción del usuario | Canasta completa después del paso | Resultado |
| ---: | --- | --- | --- |
| 1 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 2 | Cargar 1 u de `QA-PRM-011-E` por código. | `QA-PRM-011-E` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal | Total **$1.000,00**. |
| 3 | Cargar 1 u de `QA-PRM-011-A` por código. | `QA-PRM-011-E` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal<br>`QA-PRM-011-A` × 1 u: precio $1.000,00; automático $100,00; manual $0,00; neto $900,00; lista aplicada: precio normal | Total **$1.900,00**. |
| 4 | Seleccionar `QA-PRM-011-A`, abrir Ctrl+E, dejar 2 u y guardar. | `QA-PRM-011-E` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal<br>`QA-PRM-011-A` × 2 u: precio $1.000,00; automático $200,00; manual $0,00; neto $1.800,00; lista aplicada: precio normal | Total **$2.800,00**. |
| 5 | Seleccionar `QA-PRM-011-A`, abrir Ctrl+E, dejar 3 u y guardar. | `QA-PRM-011-E` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal<br>`QA-PRM-011-A` × 3 u: precio $1.000,00; automático $300,00; manual $0,00; neto $2.700,00; lista aplicada: precio normal | Total **$3.700,00**. |
| 6 | Seleccionar `QA-PRM-011-A`, abrir Ctrl+E, dejar 1 u y guardar. | `QA-PRM-011-E` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal<br>`QA-PRM-011-A` × 1 u: precio $1.000,00; automático $100,00; manual $0,00; neto $900,00; lista aplicada: precio normal | Total **$1.900,00**. |
| 7 | Cargar 1 u de `QA-PRM-011-B` por código. | `QA-PRM-011-E` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal<br>`QA-PRM-011-A` × 1 u: precio $1.000,00; automático $100,00; manual $0,00; neto $900,00; lista aplicada: precio normal<br>`QA-PRM-011-B` × 1 u: precio $1.000,00; automático $100,00; manual $0,00; neto $900,00; lista aplicada: precio normal | Total **$2.800,00**. |
| 8 | Seleccionar `QA-PRM-011-A`, abrir Ctrl+E, dejar 2 u y guardar. | `QA-PRM-011-E` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal<br>`QA-PRM-011-A` × 2 u: precio $1.000,00; automático $200,00; manual $0,00; neto $1.800,00; lista aplicada: precio normal<br>`QA-PRM-011-B` × 1 u: precio $1.000,00; automático $100,00; manual $0,00; neto $900,00; lista aplicada: precio normal | Total **$3.700,00**. |
| 9 | Abrir cobro en efectivo del perfil QA, ingresar $3.700,00 y cancelar antes de confirmar. | `QA-PRM-011-E` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal<br>`QA-PRM-011-A` × 2 u: precio $1.000,00; automático $200,00; manual $0,00; neto $1.800,00; lista aplicada: precio normal<br>`QA-PRM-011-B` × 1 u: precio $1.000,00; automático $100,00; manual $0,00; neto $900,00; lista aplicada: precio normal | Total **$3.700,00**. Conserva toda la canasta; sin venta cobrada, pago ni movimientos. |
| 10 | Retomar el cobro en efectivo del perfil QA, ingresar $3.700,00 y confirmar una sola vez. | `QA-PRM-011-E` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal<br>`QA-PRM-011-A` × 2 u: precio $1.000,00; automático $200,00; manual $0,00; neto $1.800,00; lista aplicada: precio normal<br>`QA-PRM-011-B` × 1 u: precio $1.000,00; automático $100,00; manual $0,00; neto $900,00; lista aplicada: precio normal | Total **$3.700,00**. Una venta y un cobro en efectivo del perfil QA; vuelto cero. Stock: `QA-PRM-011-E` −1 u; `QA-PRM-011-A` −2 u; `QA-PRM-011-B` −1 u. |

## Notas del recorrido

- ARS, precio base 1000, stock suficiente y agrupación OFF.
- El producto E conserva su precio sin oferta.
- Cancelar cobro conserva la venta; confirmar cobra una sola vez.

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

**Pendiente de automatización (`planned`), sin ejecución real registrada.** Etapa 2, grupo `promociones-alcances` / `ofertas-familia`; prioridad **P1**. Consultar el [índice de pendientes](../../docs/promociones-pendientes.md). Esta ficha no tiene Robot ni se ofrece como caso ejecutable.

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete privado compatible, baseline restaurable y contexto propio de empresa/sucursal/puesto/operador.
- Todos los productos del caso: ARS, unidad entera, precio base $1.000, IVA 0 % y stock suficiente (100 unidades al preparar). Comprobante interno 99; sin fiscalización ni impresión.
- Lista **Ninguna Lista**; cliente y turno sin lista; descuentos manuales/globales/de pago en cero, fidelización y recargos desactivados. Oferta activa, vigente y habilitada para la sucursal y efectivo, sin ofertas superpuestas.
- Regla: **10 % sobre el subtotal de cada producto, sin cantidad mínima.** Agrupación **desactivada**: cada producto se evalúa por separado.
- Datos disponibles en `catalogo-comercial-v1`: A = `QA-SEED-FAMILIA`, con oferta del 10 % por familia `QA-SEED-OFERTA-FAMILIA` (980113); E = `QA-SEED-NORMAL`, sin ofertas.
- **Dato nuevo pendiente de preparar:** B = `QA-PEND-PRM-011-B`, otro producto del mismo alcance que A. Es un identificador propuesto; aún no existe en el seed. Preparar la ampliación del catálogo y sus controles de aislamiento antes de automatizar, sin insertar filas ad hoc sobre el seed protegido.
- A y B pertenecen a la misma familia, pero a subfamilias distintas; E pertenece a otra familia. Así se comprueba que la oferta alcanza toda la familia y no solo la subfamilia de A.
- Dependencias para implementar: paquete y JAR identificados, preparación reproducible de todos los datos anteriores, perfil comercial validado y calibración accesible de grilla, Ctrl+E, oferta, total y cobro. No ejecutar si falta alguna; informar bloqueo sin inventar un resultado.

## Pasos y resultados esperados

Una unidad descuenta $100; tres descuentan $300. Al cambiar cantidad se recalcula el subtotal completo.

| Paso | Acción visible | Resultado esperado |
| --- | --- | --- |
| 1 | Abrir una venta nueva y comprobar el contexto QA. | Operación vacía, moneda ARS y sin lista comercial. |
| 2 | Cargar E (`QA-SEED-NORMAL`), cantidad 1. | Precio base $1.000,00, oferta $0,00 y total $1.000,00. |
| 3 | Cargar A (`QA-SEED-FAMILIA`), cantidad 1. | A: bruto $1.000,00, descuento $100,00, neto $900,00. E continúa en $1.000,00; total de venta $1.900,00. |
| 4 | Editar la misma línea A mediante Ctrl+E y dejar cantidad 2. | A: bruto $2.000,00, descuento $200,00, neto $1.800,00; total $2.800,00. |
| 5 | Editar A a cantidad 3. | A: bruto $3.000,00, descuento $300,00, neto $2.700,00; total $3.700,00. E conserva precio normal. |
| 6 | Reducir A a cantidad 1. | A vuelve a neto $900,00 y la venta a $1.900,00; no conserva descuentos de la cantidad anterior. |
| 7 | Cargar B (`QA-PEND-PRM-011-B`), cantidad 1, sin modificar A. | A y B se calculan por separado: cada uno queda en $900,00; E sigue en $1.000,00; total $2.800,00. Ambos productos incluidos reciben el beneficio y E queda excluido. |
| 8 | Editar A nuevamente a cantidad 2. | A queda en $1.800,00, B en $900,00 y E en $1.000,00; total $3.700,00. Se mantienen identidades y una línea por producto. |
| 9 | Abrir el cobro y cancelarlo antes de confirmar. | La venta vuelve con el mismo total $3.700,00 y las mismas líneas. No queda venta confirmada, cobro ni movimiento de stock/caja. |
| 10 | Retomar el cobro, entregar $3.700,00 en efectivo y confirmar una sola vez. | Venta cerrada por $3.700,00, vuelto cero; no cobra otra vez el intento cancelado. |
| 11 | Consultar el comprobante interno y contrastar los efectos de la operación. | Una venta y un cobro; bruto $4.000,00, oferta $300,00, neto $3.700,00. Stock A −2, B −1, E −1; caja +$3.700,00. |

## Evidencia y límites

Guardar importes visibles y cantidades antes/después de cada edición, al cancelar y al confirmar. Contrastar comprobante, cobro único y deltas de stock/caja de esta operación. Registrar JAR/build y SHA256, paquete, perfil, fecha y contexto en evidencia privada; los importes de esta ficha son expectativas, no resultados medidos.

No cubre fracciones, listas, otros medios de pago, ofertas agrupadas, superposiciones, fiscalización ni impresión. El recorrido exige distinguir familia de las demás clasificaciones; que A y B sean distintos evita confundir alcance amplio con oferta por producto.

## Recuperación

Cancelar el cobro conserva la operación; retomarlo debe cerrar una sola vez. Ante una discrepancia, conservar el informe privado y detener el caso antes de seguir cobrando. Finalizar solamente el JAR del runner y restaurar el baseline en la próxima ejecución; no corregir ventas, caja o stock con escrituras manuales ni ocultar evidencia mediante limpieza.

## Anexo técnico y trazabilidad

Fuente inspeccionada: XGestion2 commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Alcance `ofeTipo=2`; fórmula `TipoDescuento=%`, `ofeDescuentoPorcentaje=10`, `Lleva=0`; agrupación OFF. `src/ModuloFinanzas/Entidades/Oferta.java`, método `seleccionarOfertaAplicable`, selecciona por identidad/clasificación, vigencia, sucursal y pago. `src/ModuloFinanzas/Entidades/OfertaCalculador.java` y `test/ModuloFinanzas/Entidades/OfertaPorcentajeTest.java` sustentan la aritmética; `OfertaAplicacionCalculador.java` distingue cálculo individual y agrupado. Revisar integración en `src/ModuloVentas/Vistas/FormVenta.java` sobre el JAR al implementar.

Los oráculos futuros serán lecturas acotadas por identidad y contexto: `vecTotal` es bruto, `vecOferta` descuento automático y `venTotal` neto. No asumir una fila en `ventas_pagos` para cobro simple ni usar el cálculo del ERP como único esperado. INFO resume; DEBUG muestra acciones; TRACE aporta diagnóstico saneado. Todo fallo conserva paso, esperado, observado, categoría y evidencia; causa no determinada si no está demostrada.
<!-- END ORIGINAL OFFER DESIGN -->

</details>
