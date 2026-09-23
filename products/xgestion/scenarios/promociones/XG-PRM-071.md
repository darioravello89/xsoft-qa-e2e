---
{"id":"XG-PRM-071","title":"Calcular la oferta sobre el precio de la lista seleccionada","product":"xgestion","module":"promociones","tags":["xgestion","regression","promociones","promociones-condiciones","precios","escritura"],"status":"implemented","test":"products/xgestion/suites/ofertas/condiciones.robot","seed":"catalogo-comercial-v1"}
---

# XG-PRM-071 — Calcular la oferta sobre el precio de la lista seleccionada

## Objetivo

Calcular la oferta sobre el precio de la lista seleccionada durante una venta, con importes y efectos observables por el vendedor o cajero.

<!-- BEGIN GENERATED OFFER JOURNEY -->

## Recorrido de automatización

Estado del catálogo: **implemented**. Automatización catalogada en [`condiciones.robot`](../../suites/ofertas/condiciones.robot). Validación real: **pendiente**; requiere ejecutar el JAR exacto en el laboratorio calibrado.

Las tablas siguientes son los datos y pasos actuales del recorrido. Los importes son expectativas fijas, no resultados medidos. El diseño anterior queda al final como referencia histórica para conservar reglas, variantes y límites; sus estados y códigos no describen la implementación actual.

```powershell
.\qa.cmd run --product xgestion --scenario XG-PRM-071 --seed catalogo-comercial-v1 --log-level DEBUG
```

## Perfil y preparación

Windows QA exclusivo y offline, escritorio desbloqueado, paquete autorizado y baseline restaurable. ARS, IVA 0 %, comprobante interno 99, stock suficiente, sin impresión ni fiscalización. Cliente y turno sin listas automáticas; otros descuentos, recargos y fidelización deshabilitados, salvo lo indicado en cada variante.

Preparar mediante el runner y `catalogo-comercial-v1` antes de abrir el JAR. Los códigos públicos de abajo pertenecen a este recorrido y reemplazan los ejemplos genéricos del diseño original. No cambiar reglas mediante SQL durante la venta. La falta de perfil, seed o calibración accesible se informa como bloqueo.

Cada variante inicia el JAR de forma independiente. Los perfiles de configuración de 070 y 079 además requieren su preparación y restauración por fase. Una misma ficha conserva un solo ID lógico; solo queda aprobada si todas las variantes requeridas producen evidencia completa.

**Lectura de importes:** automático y manual son descuentos totales del renglón. La grilla muestra ambos sumados en Descuentos; el informe y la evidencia de persistencia los distinguen. El neto de todos los renglones debe sumar el total de la venta.

## Variante 1: precio-segun-lista

- Elección manual de listas habilitada; cliente y turno sin lista automática.

### Productos preparados

| Referencia | Código | Precio base | Unidad | Familia / subfamilia / sector | Marca |
| --- | --- | ---: | --- | --- | --- |
| A | `QA-PRM-071-PRODUCTO` | $1.000,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |

### Ofertas preparadas

| Oferta | Incluye | Regla | Agrupación | Estado / vigencia inclusiva | Medios habilitados |
| --- | --- | --- | --- | --- | --- |
| `QA-PRM-071-OFERTA` | Producto `QA-PRM-071-PRODUCTO` | 10 % sobre el importe | OFF | Activa; hoy -365 días a hoy +365 días | Todos |

Las fechas se refieren a la fecha local usada al preparar el seed; Windows y MySQL deben coincidir. No se modifica el reloj durante el recorrido.

### Listas preparadas

| Lista | Entradas de precio |
| --- | --- |
| `QA-PRM-071-LISTA-A` | `QA-PRM-071-PRODUCTO`: $750,00 |
| `QA-PRM-071-LISTA-B` | `QA-PRM-071-PRODUCTO`: $1.200,00 |

### Pasos y resultados esperados

| Paso | Acción del usuario | Canasta completa después del paso | Resultado |
| ---: | --- | --- | --- |
| 1 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 2 | Cargar 1 u de `QA-PRM-071-PRODUCTO` por código. | `QA-PRM-071-PRODUCTO` × 1 u: precio $1.000,00; automático $100,00; manual $0,00; neto $900,00; lista aplicada: precio normal | Total **$900,00**. |
| 3 | Abandonar la venta y confirmar la salida sin cobrar. | Sin renglones en la operación. | Sin venta cobrada, pago ni cambios de stock o destino de cobro. |
| 4 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 5 | Elegir la lista `QA-PRM-071-LISTA-A` y comprobar el precio aplicado. | Sin renglones en la operación. | Total **$0,00**. |
| 6 | Cargar 1 u de `QA-PRM-071-PRODUCTO` por código. | `QA-PRM-071-PRODUCTO` × 1 u: precio $750,00; automático $75,00; manual $0,00; neto $675,00; lista aplicada: QA-PRM-071-LISTA-A | Total **$675,00**. |
| 7 | Abandonar la venta y confirmar la salida sin cobrar. | Sin renglones en la operación. | Sin venta cobrada, pago ni cambios de stock o destino de cobro. |
| 8 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 9 | Elegir la lista `QA-PRM-071-LISTA-B` y comprobar el precio aplicado. | Sin renglones en la operación. | Total **$0,00**. |
| 10 | Cargar 2 u de `QA-PRM-071-PRODUCTO` por código. | `QA-PRM-071-PRODUCTO` × 2 u: precio $1.200,00; automático $240,00; manual $0,00; neto $2.160,00; lista aplicada: QA-PRM-071-LISTA-B | Total **$2.160,00**. |
| 11 | Abrir cobro en efectivo del perfil QA, ingresar $2.160,00 y cancelar antes de confirmar. | `QA-PRM-071-PRODUCTO` × 2 u: precio $1.200,00; automático $240,00; manual $0,00; neto $2.160,00; lista aplicada: QA-PRM-071-LISTA-B | Total **$2.160,00**. Conserva toda la canasta; sin venta cobrada, pago ni movimientos. |
| 12 | Retomar el cobro en efectivo del perfil QA, ingresar $2.160,00 y confirmar una sola vez. | `QA-PRM-071-PRODUCTO` × 2 u: precio $1.200,00; automático $240,00; manual $0,00; neto $2.160,00; lista aplicada: QA-PRM-071-LISTA-B | Total **$2.160,00**. Una venta y un cobro en efectivo del perfil QA; vuelto cero. Stock: `QA-PRM-071-PRODUCTO` −2 u. |

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

**Pendiente de automatizar — `planned`. Prioridad P1, etapa 2.**
Ficha para [el backlog de promociones](../../docs/promociones-pendientes.md).
Validación real pendiente. No tiene suite Robot ni resultado aprobado.

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete privado autorizado, escritorio visible.
- ARS, comprobante interno 99, IVA 0%, stock suficiente y sin impresión ni fiscalización.
- Perfil por defecto sin listas, descuentos adicionales, fidelización ni ofertas superpuestas,
  salvo las condiciones expresamente indicadas a continuación.
- Producto nuevo de precio normal $1.000 con oferta 10%, lista QA-A a $750 y lista QA-B a $1.200. Listas activas en ARS, sin asignación automática por cliente/turno y sin descuentos adicionales. El seed tiene ejemplos de listas, pero este cruce producto/oferta/listas está pendiente de preparar.
- Preparar cada variante de perfil desde su baseline antes de abrir XGestión;
  no cambiar datos comerciales con SQL durante el recorrido.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Elegir Ninguna Lista y cargar una unidad. | Precio $1.000, oferta $100 y neto $900. |
| En una nueva operación, elegir QA-A antes de cargar el mismo producto. | Precio $750, oferta $75, neto $675; no se calcula el descuento sobre $1.000. |
| En otra operación independiente, elegir QA-B y cargar dos unidades. | Bruto $2.400, oferta $240 y neto $2.160. |
| Cancelar el cobro de QA-B y retomarlo. | Mantiene lista, cantidad, bruto y neto; una venta por $2.160 al confirmar. |

## Dependencias para automatizar

Calibrar selector y nombre de lista y comprobar precio efectivo en cada renglón. Las ofertas tradicionales inspeccionadas calculan sobre el precio aplicado; no suponer un selector de listas permitidas dentro de la oferta.
El autor del caso debe comprobar datos y selectores en el JAR correspondiente;
si falta una precondición, informar bloqueo sin sustituir el esperado por lo observado.

## Evidencia y límites

Registrar producto, cantidad, precio, descuento y neto visibles en cada transición.
Conservar evidencia de cancelación sin efectos y de confirmación única cuando
corresponda. Contrastar venta, detalle, identidad de oferta, medio, stock y destino
del pago por operación y contexto; no imprimir filas completas. Los importes de
esta ficha son expectativas del perfil, no resultados medidos. El cobro de variantes
con otros medios o empresas requiere un contrato de laboratorio específico.

## Recuperación

Ante una discrepancia, conservar el reporte privado y abandonar por la interfaz
si está disponible. No corregir importes ni movimientos en la base para hacer pasar
el caso. Restaurar el baseline correspondiente antes de repetir o cambiar de perfil.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`.
Rutas relativas a XGestion2: `src/ModuloFinanzas/Entidades/Oferta.java`; `test/ModuloVentas/Vistas/FormVentaOfertaPerformancePolicyTest.java`.
Esta referencia acredita reglas de fuente, no ejecución del artefacto.

Selectores accesibles y oráculos por identidad pendientes de implementar/calibrar;
registrar SHA256 del JAR, paquete, perfil y persona responsable en evidencia privada.
INFO resume; DEBUG muestra pasos; TRACE aporta diagnóstico saneado. Todo fallo
informa paso, esperado, observado, categoría y evidencia; causa no determinada
cuando no existe prueba causal. No incluir credenciales ni configuración privada.
<!-- END ORIGINAL OFFER DESIGN -->

</details>
