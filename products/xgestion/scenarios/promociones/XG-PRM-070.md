---
{"id":"XG-PRM-070","title":"Revisar una oferta activa y desactivada entre ventas nuevas","product":"xgestion","module":"promociones","tags":["xgestion","regression","promociones","promociones-condiciones","escritura"],"status":"implemented","test":"products/xgestion/suites/ofertas/condiciones.robot","seed":"catalogo-comercial-v1"}
---

# XG-PRM-070 — Revisar una oferta activa y desactivada entre ventas nuevas

## Objetivo

Revisar una oferta activa y desactivada entre ventas nuevas durante una venta, con importes y efectos observables por el vendedor o cajero.

<!-- BEGIN GENERATED OFFER JOURNEY -->

## Recorrido de automatización

Estado del catálogo: **implemented**. Automatización catalogada en [`condiciones.robot`](../../suites/ofertas/condiciones.robot). Validación real: **pendiente**; requiere ejecutar el JAR exacto en el laboratorio calibrado.

Las tablas siguientes son los datos y pasos actuales del recorrido. Los importes son expectativas fijas, no resultados medidos. El diseño anterior queda al final como referencia histórica para conservar reglas, variantes y límites; sus estados y códigos no describen la implementación actual.

```powershell
.\qa.cmd run --product xgestion --scenario XG-PRM-070 --seed catalogo-comercial-v1 --log-level DEBUG
```

## Perfil y preparación

Windows QA exclusivo y offline, escritorio desbloqueado, paquete autorizado y baseline restaurable. ARS, IVA 0 %, comprobante interno 99, stock suficiente, sin impresión ni fiscalización. Cliente y turno sin listas automáticas; otros descuentos, recargos y fidelización deshabilitados, salvo lo indicado en cada variante.

Preparar mediante el runner y `catalogo-comercial-v1` antes de abrir el JAR. Los códigos públicos de abajo pertenecen a este recorrido y reemplazan los ejemplos genéricos del diseño original. No cambiar reglas mediante SQL durante la venta. La falta de perfil, seed o calibración accesible se informa como bloqueo.

Cada variante inicia el JAR de forma independiente. Los perfiles de configuración de 070 y 079 además requieren su preparación y restauración por fase. Una misma ficha conserva un solo ID lógico; solo queda aprobada si todas las variantes requeridas producen evidencia completa.

**Lectura de importes:** automático y manual son descuentos totales del renglón. La grilla muestra ambos sumados en Descuentos; el informe y la evidencia de persistencia los distinguen. El neto de todos los renglones debe sumar el total de la venta.

## Variante 1: active

### Productos preparados

| Referencia | Código | Precio base | Unidad | Familia / subfamilia / sector | Marca |
| --- | --- | ---: | --- | --- | --- |
| A | `QA-PRM-070-A` | $1.000,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |
| B | `QA-PRM-070-CONTROL` | $1.000,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |

### Ofertas preparadas

| Oferta | Incluye | Regla | Agrupación | Estado / vigencia inclusiva | Medios habilitados |
| --- | --- | --- | --- | --- | --- |
| `QA-PRM-070` | Producto `QA-PRM-070-A` | 10 % sobre el importe | OFF | Activa; hoy -365 días a hoy +365 días | Todos |
| `QA-PRM-070-CONTROL` | Producto `QA-PRM-070-CONTROL` | 10 % sobre el importe | OFF | Activa; hoy -365 días a hoy +365 días | Todos |

Las fechas se refieren a la fecha local usada al preparar el seed; Windows y MySQL deben coincidir. No se modifica el reloj durante el recorrido.

### Pasos y resultados esperados

| Paso | Acción del usuario | Canasta completa después del paso | Resultado |
| ---: | --- | --- | --- |
| 1 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 2 | Cargar 1 u de `QA-PRM-070-CONTROL` por código. | `QA-PRM-070-CONTROL` × 1 u: precio $1.000,00; automático $100,00; manual $0,00; neto $900,00; lista aplicada: precio normal | Total **$900,00**. |
| 3 | Abandonar la venta y confirmar la salida sin cobrar. | Sin renglones en la operación. | Sin venta cobrada, pago ni cambios de stock o destino de cobro. |
| 4 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 5 | Cargar 1 u de `QA-PRM-070-A` por código. | `QA-PRM-070-A` × 1 u: precio $1.000,00; automático $100,00; manual $0,00; neto $900,00; lista aplicada: precio normal | Total **$900,00**. |
| 6 | Abandonar la venta y confirmar la salida sin cobrar. | Sin renglones en la operación. | Sin venta cobrada, pago ni cambios de stock o destino de cobro. |

## Variante 2: inactive

### Productos preparados

| Referencia | Código | Precio base | Unidad | Familia / subfamilia / sector | Marca |
| --- | --- | ---: | --- | --- | --- |
| A | `QA-PRM-070-A` | $1.000,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |
| B | `QA-PRM-070-CONTROL` | $1.000,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |

### Ofertas preparadas

| Oferta | Incluye | Regla | Agrupación | Estado / vigencia inclusiva | Medios habilitados |
| --- | --- | --- | --- | --- | --- |
| `QA-PRM-070` | Producto `QA-PRM-070-A` | 10 % sobre el importe | OFF | Inactiva; hoy -365 días a hoy +365 días | Todos |
| `QA-PRM-070-CONTROL` | Producto `QA-PRM-070-CONTROL` | 10 % sobre el importe | OFF | Activa; hoy -365 días a hoy +365 días | Todos |

Las fechas se refieren a la fecha local usada al preparar el seed; Windows y MySQL deben coincidir. No se modifica el reloj durante el recorrido.

### Pasos y resultados esperados

| Paso | Acción del usuario | Canasta completa después del paso | Resultado |
| ---: | --- | --- | --- |
| 1 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 2 | Cargar 1 u de `QA-PRM-070-CONTROL` por código. | `QA-PRM-070-CONTROL` × 1 u: precio $1.000,00; automático $100,00; manual $0,00; neto $900,00; lista aplicada: precio normal | Total **$900,00**. |
| 3 | Abandonar la venta y confirmar la salida sin cobrar. | Sin renglones en la operación. | Sin venta cobrada, pago ni cambios de stock o destino de cobro. |
| 4 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 5 | Cargar 1 u de `QA-PRM-070-A` por código. | `QA-PRM-070-A` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal | Total **$1.000,00**. |
| 6 | Abandonar la venta y confirmar la salida sin cobrar. | Sin renglones en la operación. | Sin venta cobrada, pago ni cambios de stock o destino de cobro. |

## Variante 3: active-again

### Productos preparados

| Referencia | Código | Precio base | Unidad | Familia / subfamilia / sector | Marca |
| --- | --- | ---: | --- | --- | --- |
| A | `QA-PRM-070-A` | $1.000,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |
| B | `QA-PRM-070-CONTROL` | $1.000,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |

### Ofertas preparadas

| Oferta | Incluye | Regla | Agrupación | Estado / vigencia inclusiva | Medios habilitados |
| --- | --- | --- | --- | --- | --- |
| `QA-PRM-070` | Producto `QA-PRM-070-A` | 10 % sobre el importe | OFF | Activa; hoy -365 días a hoy +365 días | Todos |
| `QA-PRM-070-CONTROL` | Producto `QA-PRM-070-CONTROL` | 10 % sobre el importe | OFF | Activa; hoy -365 días a hoy +365 días | Todos |

Las fechas se refieren a la fecha local usada al preparar el seed; Windows y MySQL deben coincidir. No se modifica el reloj durante el recorrido.

### Pasos y resultados esperados

| Paso | Acción del usuario | Canasta completa después del paso | Resultado |
| ---: | --- | --- | --- |
| 1 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 2 | Cargar 1 u de `QA-PRM-070-CONTROL` por código. | `QA-PRM-070-CONTROL` × 1 u: precio $1.000,00; automático $100,00; manual $0,00; neto $900,00; lista aplicada: precio normal | Total **$900,00**. |
| 3 | Abandonar la venta y confirmar la salida sin cobrar. | Sin renglones en la operación. | Sin venta cobrada, pago ni cambios de stock o destino de cobro. |
| 4 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 5 | Cargar 1 u de `QA-PRM-070-A` por código. | `QA-PRM-070-A` × 1 u: precio $1.000,00; automático $100,00; manual $0,00; neto $900,00; lista aplicada: precio normal | Total **$900,00**. |
| 6 | Cargar 1 u de `QA-PRM-070-A` por código. | `QA-PRM-070-A` × 2 u: precio $1.000,00; automático $200,00; manual $0,00; neto $1.800,00; lista aplicada: precio normal | Total **$1.800,00**. |
| 7 | Abrir cobro en efectivo del perfil QA, ingresar $1.800,00 y cancelar antes de confirmar. | `QA-PRM-070-A` × 2 u: precio $1.000,00; automático $200,00; manual $0,00; neto $1.800,00; lista aplicada: precio normal | Total **$1.800,00**. Conserva toda la canasta; sin venta cobrada, pago ni movimientos. |
| 8 | Retomar el cobro en efectivo del perfil QA, ingresar $1.800,00 y confirmar una sola vez. | `QA-PRM-070-A` × 2 u: precio $1.000,00; automático $200,00; manual $0,00; neto $1.800,00; lista aplicada: precio normal | Total **$1.800,00**. Una venta y un cobro en efectivo del perfil QA; vuelto cero. Stock: `QA-PRM-070-A` −2 u. |

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
- Producto nuevo de $1.000 y oferta 10%, con tres perfiles independientes ACTIVE, INACTIVE y ACTIVE-AGAIN. Son estados iniciales preparados, no cambios durante una venta ni reapertura histórica. Control adicional de oferta vigente en cada perfil.
- Preparar cada variante de perfil desde su baseline antes de abrir XGestión;
  no cambiar datos comerciales con SQL durante el recorrido.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| En ACTIVE, iniciar sesión nueva y cargar una unidad. | Neto $900. |
| Cerrar la operación sin cobrar y comenzar la corrida INACTIVE desde su baseline. | La misma identidad de producto muestra $1.000, oferta $0; el control positivo separado sigue descontando. |
| Comenzar ACTIVE-AGAIN desde su baseline y cargar dos unidades. | Neto $1.800, sin reutilizar estado de la corrida anterior. |
| Cancelar y retomar el cobro de esta última venta. | Conserva $1.800; al confirmar se registra un solo cobro. |

## Dependencias para automatizar

Preparar variantes del paquete y restauración por corrida. La edición de ofertas en su pantalla administrativa y la invalidación de caché en una sesión abierta quedan como ampliación distinta.
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
Rutas relativas a XGestion2: `src/ModuloFinanzas/Entidades/Oferta.java`; `test/ModuloFinanzas/Entidades/OfertaAplicabilidadTest.java`.
Esta referencia acredita reglas de fuente, no ejecución del artefacto.

Selectores accesibles y oráculos por identidad pendientes de implementar/calibrar;
registrar SHA256 del JAR, paquete, perfil y persona responsable en evidencia privada.
INFO resume; DEBUG muestra pasos; TRACE aporta diagnóstico saneado. Todo fallo
informa paso, esperado, observado, categoría y evidencia; causa no determinada
cuando no existe prueba causal. No incluir credenciales ni configuración privada.
<!-- END ORIGINAL OFFER DESIGN -->

</details>
