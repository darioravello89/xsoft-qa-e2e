---
{"id":"XG-PRM-063","title":"Conservar los centavos al distribuir el descuento de un combo","product":"xgestion","module":"promociones","tags":["xgestion","regression","promociones","promociones-combos","escritura"],"status":"implemented","test":"products/xgestion/suites/ofertas/combos.robot","seed":"catalogo-comercial-v1"}
---

# XG-PRM-063 — Conservar los centavos al distribuir el descuento de un combo

## Objetivo

El vendedor ve un importe de combo exacto aunque su descuento deba repartirse en tres líneas con centavos, y el cobro coincide con la suma de la venta.

<!-- BEGIN GENERATED OFFER JOURNEY -->

## Recorrido de automatización

Estado del catálogo: **implemented**. Automatización catalogada en [`combos.robot`](../../suites/ofertas/combos.robot). Validación real: **pendiente**; requiere ejecutar el JAR exacto en el laboratorio calibrado.

Las tablas siguientes son los datos y pasos actuales del recorrido. Los importes son expectativas fijas, no resultados medidos. El diseño anterior queda al final como referencia histórica para conservar reglas, variantes y límites; sus estados y códigos no describen la implementación actual.

```powershell
.\qa.cmd run --product xgestion --scenario XG-PRM-063 --seed catalogo-comercial-v1 --log-level DEBUG
```

## Perfil y preparación

Windows QA exclusivo y offline, escritorio desbloqueado, paquete autorizado y baseline restaurable. ARS, IVA 0 %, comprobante interno 99, stock suficiente, sin impresión ni fiscalización. Cliente y turno sin listas automáticas; otros descuentos, recargos y fidelización deshabilitados, salvo lo indicado en cada variante.

Preparar mediante el runner y `catalogo-comercial-v1` antes de abrir el JAR. Los códigos públicos de abajo pertenecen a este recorrido y reemplazan los ejemplos genéricos del diseño original. No cambiar reglas mediante SQL durante la venta. La falta de perfil, seed o calibración accesible se informa como bloqueo.

Cada variante inicia el JAR de forma independiente. Los perfiles de configuración de 070 y 079 además requieren su preparación y restauración por fase. Una misma ficha conserva un solo ID lógico; solo queda aprobada si todas las variantes requeridas producen evidencia completa.

**Lectura de importes:** automático y manual son descuentos totales del renglón. La grilla muestra ambos sumados en Descuentos; el informe y la evidencia de persistencia los distinguen. El neto de todos los renglones debe sumar el total de la venta.

## Variante 1: centavos-exactos

### Productos preparados

| Referencia | Código | Precio base | Unidad | Familia / subfamilia / sector | Marca |
| --- | --- | ---: | --- | --- | --- |
| A | `QA-PRM-063-V0-A` | $10,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |
| B | `QA-PRM-063-V0-B` | $10,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |
| C | `QA-PRM-063-V0-C` | $10,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |
| E | `QA-PRM-063-V0-E` | $10,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |

### Ofertas preparadas

| Oferta | Incluye | Regla | Agrupación | Estado / vigencia inclusiva | Medios habilitados |
| --- | --- | --- | --- | --- | --- |
| `QA-COMBO-987300` | 1 × `QA-PRM-063-V0-A` + 1 × `QA-PRM-063-V0-B` + 1 × `QA-PRM-063-V0-C` | Precio final del combo completo: $20,00 | No aplica: combo por componentes | Activa; hoy -365 días a hoy +365 días | Todos |

Las fechas se refieren a la fecha local usada al preparar el seed; Windows y MySQL deben coincidir. No se modifica el reloj durante el recorrido.

### Pasos y resultados esperados

| Paso | Acción del usuario | Canasta completa después del paso | Resultado |
| ---: | --- | --- | --- |
| 1 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 2 | Cargar 1 u de `QA-PRM-063-V0-A` por código. | `QA-PRM-063-V0-A` × 1 u: precio $10,00; automático $0,00; manual $0,00; neto $10,00; lista aplicada: precio normal | Total **$10,00**. |
| 3 | Cargar 1 u de `QA-PRM-063-V0-B` por código. | `QA-PRM-063-V0-A` × 1 u: precio $10,00; automático $0,00; manual $0,00; neto $10,00; lista aplicada: precio normal<br>`QA-PRM-063-V0-B` × 1 u: precio $10,00; automático $0,00; manual $0,00; neto $10,00; lista aplicada: precio normal | Total **$20,00**. |
| 4 | Cargar 1 u de `QA-PRM-063-V0-C` por código. | `QA-PRM-063-V0-A` × 1 u: precio $10,00; automático $3,33; manual $0,00; neto $6,67; lista aplicada: precio normal<br>`QA-PRM-063-V0-B` × 1 u: precio $10,00; automático $3,33; manual $0,00; neto $6,67; lista aplicada: precio normal<br>`QA-PRM-063-V0-C` × 1 u: precio $10,00; automático $3,34; manual $0,00; neto $6,66; lista aplicada: precio normal | Total **$20,00**. |
| 5 | Cargar 1 u de `QA-PRM-063-V0-E` por código. | `QA-PRM-063-V0-A` × 1 u: precio $10,00; automático $3,33; manual $0,00; neto $6,67; lista aplicada: precio normal<br>`QA-PRM-063-V0-B` × 1 u: precio $10,00; automático $3,33; manual $0,00; neto $6,67; lista aplicada: precio normal<br>`QA-PRM-063-V0-C` × 1 u: precio $10,00; automático $3,34; manual $0,00; neto $6,66; lista aplicada: precio normal<br>`QA-PRM-063-V0-E` × 1 u: precio $10,00; automático $0,00; manual $0,00; neto $10,00; lista aplicada: precio normal | Total **$30,00**. |
| 6 | Seleccionar `QA-PRM-063-V0-E`, abrir Ctrl+E y elegir Eliminar. | `QA-PRM-063-V0-A` × 1 u: precio $10,00; automático $3,33; manual $0,00; neto $6,67; lista aplicada: precio normal<br>`QA-PRM-063-V0-B` × 1 u: precio $10,00; automático $3,33; manual $0,00; neto $6,67; lista aplicada: precio normal<br>`QA-PRM-063-V0-C` × 1 u: precio $10,00; automático $3,34; manual $0,00; neto $6,66; lista aplicada: precio normal | Total **$20,00**. |
| 7 | Seleccionar `QA-PRM-063-V0-C`, abrir Ctrl+E y elegir Eliminar. | `QA-PRM-063-V0-A` × 1 u: precio $10,00; automático $0,00; manual $0,00; neto $10,00; lista aplicada: precio normal<br>`QA-PRM-063-V0-B` × 1 u: precio $10,00; automático $0,00; manual $0,00; neto $10,00; lista aplicada: precio normal | Total **$20,00**. |
| 8 | Cargar 1 u de `QA-PRM-063-V0-C` por código. | `QA-PRM-063-V0-A` × 1 u: precio $10,00; automático $3,33; manual $0,00; neto $6,67; lista aplicada: precio normal<br>`QA-PRM-063-V0-B` × 1 u: precio $10,00; automático $3,33; manual $0,00; neto $6,67; lista aplicada: precio normal<br>`QA-PRM-063-V0-C` × 1 u: precio $10,00; automático $3,34; manual $0,00; neto $6,66; lista aplicada: precio normal | Total **$20,00**. |
| 9 | Abandonar la venta y confirmar la salida sin cobrar. | Sin renglones en la operación. | Sin venta cobrada, pago ni cambios de stock o destino de cobro. |
| 10 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 11 | Cargar 1 u de `QA-PRM-063-V0-A` por código. | `QA-PRM-063-V0-A` × 1 u: precio $10,00; automático $0,00; manual $0,00; neto $10,00; lista aplicada: precio normal | Total **$10,00**. |
| 12 | Cargar 1 u de `QA-PRM-063-V0-B` por código. | `QA-PRM-063-V0-A` × 1 u: precio $10,00; automático $0,00; manual $0,00; neto $10,00; lista aplicada: precio normal<br>`QA-PRM-063-V0-B` × 1 u: precio $10,00; automático $0,00; manual $0,00; neto $10,00; lista aplicada: precio normal | Total **$20,00**. |
| 13 | Cargar 1 u de `QA-PRM-063-V0-C` por código. | `QA-PRM-063-V0-A` × 1 u: precio $10,00; automático $3,33; manual $0,00; neto $6,67; lista aplicada: precio normal<br>`QA-PRM-063-V0-B` × 1 u: precio $10,00; automático $3,33; manual $0,00; neto $6,67; lista aplicada: precio normal<br>`QA-PRM-063-V0-C` × 1 u: precio $10,00; automático $3,34; manual $0,00; neto $6,66; lista aplicada: precio normal | Total **$20,00**. |
| 14 | Abrir cobro en efectivo del perfil QA, ingresar $20,00 y cancelar antes de confirmar. | `QA-PRM-063-V0-A` × 1 u: precio $10,00; automático $3,33; manual $0,00; neto $6,67; lista aplicada: precio normal<br>`QA-PRM-063-V0-B` × 1 u: precio $10,00; automático $3,33; manual $0,00; neto $6,67; lista aplicada: precio normal<br>`QA-PRM-063-V0-C` × 1 u: precio $10,00; automático $3,34; manual $0,00; neto $6,66; lista aplicada: precio normal | Total **$20,00**. Conserva toda la canasta; sin venta cobrada, pago ni movimientos. |
| 15 | Retomar el cobro en efectivo del perfil QA, ingresar $20,00 y confirmar una sola vez. | `QA-PRM-063-V0-A` × 1 u: precio $10,00; automático $3,33; manual $0,00; neto $6,67; lista aplicada: precio normal<br>`QA-PRM-063-V0-B` × 1 u: precio $10,00; automático $3,33; manual $0,00; neto $6,67; lista aplicada: precio normal<br>`QA-PRM-063-V0-C` × 1 u: precio $10,00; automático $3,34; manual $0,00; neto $6,66; lista aplicada: precio normal | Total **$20,00**. Una venta y un cobro en efectivo del perfil QA; vuelto cero. Stock: `QA-PRM-063-V0-A` −1 u; `QA-PRM-063-V0-B` −1 u; `QA-PRM-063-V0-C` −1 u. |

## Variante 2: base-neta-manual

- Permisos general y sobre ofertas habilitados; descuento manual por importe total de línea.

### Productos preparados

| Referencia | Código | Precio base | Unidad | Familia / subfamilia / sector | Marca |
| --- | --- | ---: | --- | --- | --- |
| A | `QA-PRM-063-V1-A` | $10,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |
| B | `QA-PRM-063-V1-B` | $10,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |
| C | `QA-PRM-063-V1-C` | $10,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |
| E | `QA-PRM-063-V1-E` | $10,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |

### Ofertas preparadas

| Oferta | Incluye | Regla | Agrupación | Estado / vigencia inclusiva | Medios habilitados |
| --- | --- | --- | --- | --- | --- |
| `QA-COMBO-987310` | 1 × `QA-PRM-063-V1-A` + 1 × `QA-PRM-063-V1-B` + 1 × `QA-PRM-063-V1-C` | Precio final del combo completo: $20,00 | No aplica: combo por componentes | Activa; hoy -365 días a hoy +365 días | Todos |

Las fechas se refieren a la fecha local usada al preparar el seed; Windows y MySQL deben coincidir. No se modifica el reloj durante el recorrido.

### Pasos y resultados esperados

| Paso | Acción del usuario | Canasta completa después del paso | Resultado |
| ---: | --- | --- | --- |
| 1 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 2 | Cargar 1 u de `QA-PRM-063-V1-A` por código. | `QA-PRM-063-V1-A` × 1 u: precio $10,00; automático $0,00; manual $0,00; neto $10,00; lista aplicada: precio normal | Total **$10,00**. |
| 3 | Cargar 1 u de `QA-PRM-063-V1-B` por código. | `QA-PRM-063-V1-A` × 1 u: precio $10,00; automático $0,00; manual $0,00; neto $10,00; lista aplicada: precio normal<br>`QA-PRM-063-V1-B` × 1 u: precio $10,00; automático $0,00; manual $0,00; neto $10,00; lista aplicada: precio normal | Total **$20,00**. |
| 4 | Cargar 1 u de `QA-PRM-063-V1-C` por código. | `QA-PRM-063-V1-A` × 1 u: precio $10,00; automático $3,33; manual $0,00; neto $6,67; lista aplicada: precio normal<br>`QA-PRM-063-V1-B` × 1 u: precio $10,00; automático $3,33; manual $0,00; neto $6,67; lista aplicada: precio normal<br>`QA-PRM-063-V1-C` × 1 u: precio $10,00; automático $3,34; manual $0,00; neto $6,66; lista aplicada: precio normal | Total **$20,00**. |
| 5 | Abrir Ctrl+E en `QA-PRM-063-V1-A`, guardar $1,00 de descuento manual total. | `QA-PRM-063-V1-A` × 1 u: precio $10,00; automático $2,79; manual $1,00; neto $6,21; lista aplicada: precio normal<br>`QA-PRM-063-V1-B` × 1 u: precio $10,00; automático $3,10; manual $0,00; neto $6,90; lista aplicada: precio normal<br>`QA-PRM-063-V1-C` × 1 u: precio $10,00; automático $3,11; manual $0,00; neto $6,89; lista aplicada: precio normal | Total **$20,00**. |
| 6 | Abrir Ctrl+E en `QA-PRM-063-V1-A`, guardar $0,00 de descuento manual total. | `QA-PRM-063-V1-A` × 1 u: precio $10,00; automático $3,33; manual $0,00; neto $6,67; lista aplicada: precio normal<br>`QA-PRM-063-V1-B` × 1 u: precio $10,00; automático $3,33; manual $0,00; neto $6,67; lista aplicada: precio normal<br>`QA-PRM-063-V1-C` × 1 u: precio $10,00; automático $3,34; manual $0,00; neto $6,66; lista aplicada: precio normal | Total **$20,00**. |
| 7 | Abandonar la venta y confirmar la salida sin cobrar. | Sin renglones en la operación. | Sin venta cobrada, pago ni cambios de stock o destino de cobro. |

## Notas del recorrido

- Orden ABC: automático 3.33+3.33+3.34=10, neto 20.
- Manual A=1: base 29, automático 2.79+3.10+3.11=9, neto 20.
- La variante manual exige permisos general y sobre ofertas ON; no comprueba el aviso.

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

**Pendiente de automatizar (`planned`), prioridad P1, etapa 2.** Esta ficha no tiene test Robot ni validación real sobre el JAR. Forma parte del [backlog de promociones](../../docs/promociones-pendientes.md). Los combos se definen por sus componentes; no son la opción «agrupar productos» de una oferta tradicional.

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete autorizado y baseline restaurable. Registrar JAR y contexto propio de empresa/sucursal/puesto; vendedor con permiso de carga, edición, eliminación, cobro y abandono sin supervisor.
- ARS, IVA 0 %, sin otros impuestos; stock suficiente, comprobante interno 99, efectivo exacto, diálogo de cobro habilitado, sin impresión ni fiscalización. Lista Ninguna Lista (ID 0), cliente/turno sin lista automática y fidelización deshabilitada.
- Ofertas activas y vigentes para la sucursal QA, aplicables a todos los medios de pago. Otros descuentos, recargos y condiciones comerciales en cero salvo las excepciones explícitas. Preparar cada variante antes de abrir la venta; no modificar reglas mediante escrituras directas en la base durante el recorrido.
- **NUEVO PENDIENTE DE PREPARAR:** A, B y C exclusivos, precio $10 por unidad, combo A+B+C por $20; Ajeno=$10 sin ofertas. Sin promociones individuales. Cargar en orden A, B, C para hacer determinista el reparto de centavos.
- **NUEVO PENDIENTE DE PREPARAR:** variante independiente que permite al vendedor descuento manual de $1 en la línea A. Es la única excepción a otros descuentos en cero; debe registrarse por separado del descuento automático.
- Usar cantidades enteras. La regla de combo tiene ahorro $10 sobre bruto $30 en el perfil base; no introducir tolerancias que acepten $19,99 o $20,01 como si fueran $20.

## Pasos y resultados esperados

1. Cargar A ×1 + B ×1. **Esperado:** bruto/neto $20, sin combo completo. Agregar C ×1. **Esperado:** bruto $30, descuento automático $10 y neto $20.

2. Con orden A, B, C, comprobar las líneas. **Esperado:** descuentos $3,33 + $3,33 + $3,34 = $10; netos $6,67 + $6,67 + $6,66 = $20. No se pierden ni duplican centavos al cerrar el reparto.

3. Agregar Ajeno ×1. **Esperado:** bruto $40, oferta $10 y total $30; Ajeno conserva sus $10. Quitar Ajeno y luego C. **Esperado:** A+B vuelven a total $20 sin oferta. Volver a cargar C. **Esperado:** restaura descuento $10 y neto $20. Abandonar sin efectos.

4. En una ejecución independiente, cargar A+B+C y aplicar descuento manual de $1 a A. **Esperado:** bruto $30, manual $1, base posterior $29, automático $9, neto $20. Con orden A, B, C, el automático es $2,79 + $3,10 + $3,11 = $9; netos $6,21 + $6,90 + $6,89 = $20. El descuento manual no se resta dos veces. Quitar el descuento manual. **Esperado:** automático $10 y neto $20. Abandonar sin efectos.

5. Restaurar el perfil base, cargar A+B+C, abrir y cancelar el cobro. **Esperado:** total exacto $20, sin venta cobrada ni movimientos de stock/caja. Retomar y cobrar $20 una sola vez. **Esperado:** una venta y un cobro por $20, vuelto cero, caja +$20, stock A −1, B −1 y C −1; Ajeno sin cambios.

## Evidencia y límites

Guardar importes por línea y totales con dos decimales, distinguiendo descuento manual del automático. La lectura acotada de la venta debe sumar exactamente los centavos cobrados. La variante manual puede requerir un diálogo y autorización accesibles todavía pendientes de calibrar.

El residuo corresponde a la última línea participante en el orden observado. No exigir que C reciba siempre el centavo si se cambia el orden de carga. Otras monedas, impuestos y redondeo de caja quedan fuera. Datos, contratos de perfil, localizadores de grilla/leyenda/edición y automatización deben prepararse antes de ejecutar. Escribir esta ficha o aplicar un seed parecido no acredita que el caso haya pasado.

## Recuperación

La cancelación del cobro debe devolver las mismas cantidades e importe sin cerrar la operación. Para las variantes abandonadas, confirmar salida y verificar ausencia de venta cobrada y movimientos de stock/caja. Si una comprobación falla, conservar evidencia privada antes de restaurar el baseline; no borrar filas ni modificar descuentos para conseguir el resultado. Cada perfil independiente comienza con datos controlados y no reutiliza operaciones anteriores.

## Anexo técnico y trazabilidad

Fuente ERP verificada: commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; `src/ModuloFinanzas/Entidades/OfertaComboCalculador.java`, `src/ModuloVentas/Servicios/OfertaComboService.java` y `test/ModuloFinanzas/Entidades/OfertaComboCalculadorTest.java`. `OfertaComboCalculadorTest.descuentaSobreBaseNetaManualYConservaCentavosExactos`; `OfertaComboCalculador.aplicarCandidato` prorratea y asigna el residuo al último participante, con redondeo HALF_UP. El ejemplo manual conserva los $10/$10/$10 y $1 del test; la distribución numérica se deriva de esa regla.

Comprobar UI y persistencia mediante lecturas acotadas por operación/contexto: bruto `vecTotal`, automático `vecOferta`, manual `vecOfertaManual` cuando corresponda, neto `venTotal`, identidad/leyenda del combo, un cobro y deltas declarados. El número de filas de pago no se deduce sin revisar el contrato del cobro simple. Selectores y oráculos para estas variantes permanecen pendientes de calibración; no usar coordenadas fijas. Registrar SHA256/build JAR, paquete, perfil y versión de datos. INFO resume, DEBUG muestra pasos y TRACE agrega diagnóstico saneado; un fallo informa paso, esperado, observado, categoría y evidencia, con causa no determinada si no está demostrada. No exponer filas completas, credenciales ni árboles privados.
<!-- END ORIGINAL OFFER DESIGN -->

</details>
