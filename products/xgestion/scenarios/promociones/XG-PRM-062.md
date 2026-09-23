---
{"id":"XG-PRM-062","title":"Elegir entre combos que comparten productos y resolver un empate","product":"xgestion","module":"promociones","tags":["xgestion","regression","promociones","promociones-combos","escritura"],"status":"implemented","test":"products/xgestion/suites/ofertas/combos.robot","seed":"catalogo-comercial-v1"}
---

# XG-PRM-062 — Elegir entre combos que comparten productos y resolver un empate

## Objetivo

El vendedor recibe el combo de mayor ahorro disponible sin que un mismo producto complete dos combos competidores; ante un empate, el resultado y su identificación permanecen estables.

<!-- BEGIN GENERATED OFFER JOURNEY -->

## Recorrido de automatización

Estado del catálogo: **implemented**. Automatización catalogada en [`combos.robot`](../../suites/ofertas/combos.robot). Validación real: **pendiente**; requiere ejecutar el JAR exacto en el laboratorio calibrado.

Las tablas siguientes son los datos y pasos actuales del recorrido. Los importes son expectativas fijas, no resultados medidos. El diseño anterior queda al final como referencia histórica para conservar reglas, variantes y límites; sus estados y códigos no describen la implementación actual.

```powershell
.\qa.cmd run --product xgestion --scenario XG-PRM-062 --seed catalogo-comercial-v1 --log-level DEBUG
```

## Perfil y preparación

Windows QA exclusivo y offline, escritorio desbloqueado, paquete autorizado y baseline restaurable. ARS, IVA 0 %, comprobante interno 99, stock suficiente, sin impresión ni fiscalización. Cliente y turno sin listas automáticas; otros descuentos, recargos y fidelización deshabilitados, salvo lo indicado en cada variante.

Preparar mediante el runner y `catalogo-comercial-v1` antes de abrir el JAR. Los códigos públicos de abajo pertenecen a este recorrido y reemplazan los ejemplos genéricos del diseño original. No cambiar reglas mediante SQL durante la venta. La falta de perfil, seed o calibración accesible se informa como bloqueo.

Cada variante inicia el JAR de forma independiente. Los perfiles de configuración de 070 y 079 además requieren su preparación y restauración por fase. Una misma ficha conserva un solo ID lógico; solo queda aprobada si todas las variantes requeridas producen evidencia completa.

**Lectura de importes:** automático y manual son descuentos totales del renglón. La grilla muestra ambos sumados en Descuentos; el informe y la evidencia de persistencia los distinguen. El neto de todos los renglones debe sumar el total de la venta.

## Variante 1: mayor-ahorro

### Productos preparados

| Referencia | Código | Precio base | Unidad | Familia / subfamilia / sector | Marca |
| --- | --- | ---: | --- | --- | --- |
| A | `QA-PRM-062-V0-A` | $100,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |
| B | `QA-PRM-062-V0-B` | $50,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |
| C | `QA-PRM-062-V0-C` | $60,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |
| E | `QA-PRM-062-V0-E` | $100,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |

### Ofertas preparadas

| Oferta | Incluye | Regla | Agrupación | Estado / vigencia inclusiva | Medios habilitados |
| --- | --- | --- | --- | --- | --- |
| `QA-COMBO-987200` | 1 × `QA-PRM-062-V0-A` + 1 × `QA-PRM-062-V0-B` | Precio final del combo completo: $130,00 | No aplica: combo por componentes | Activa; hoy -365 días a hoy +365 días | Todos |
| `QA-COMBO-987201` | 1 × `QA-PRM-062-V0-A` + 1 × `QA-PRM-062-V0-C` | Precio final del combo completo: $120,00 | No aplica: combo por componentes | Activa; hoy -365 días a hoy +365 días | Todos |

Las fechas se refieren a la fecha local usada al preparar el seed; Windows y MySQL deben coincidir. No se modifica el reloj durante el recorrido.

### Pasos y resultados esperados

| Paso | Acción del usuario | Canasta completa después del paso | Resultado |
| ---: | --- | --- | --- |
| 1 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 2 | Cargar 1 u de `QA-PRM-062-V0-A` por código. | `QA-PRM-062-V0-A` × 1 u: precio $100,00; automático $0,00; manual $0,00; neto $100,00; lista aplicada: precio normal | Total **$100,00**. |
| 3 | Cargar 1 u de `QA-PRM-062-V0-E` por código. | `QA-PRM-062-V0-A` × 1 u: precio $100,00; automático $0,00; manual $0,00; neto $100,00; lista aplicada: precio normal<br>`QA-PRM-062-V0-E` × 1 u: precio $100,00; automático $0,00; manual $0,00; neto $100,00; lista aplicada: precio normal | Total **$200,00**. |
| 4 | Seleccionar `QA-PRM-062-V0-E`, abrir Ctrl+E y elegir Eliminar. | `QA-PRM-062-V0-A` × 1 u: precio $100,00; automático $0,00; manual $0,00; neto $100,00; lista aplicada: precio normal | Total **$100,00**. |
| 5 | Cargar 1 u de `QA-PRM-062-V0-B` por código. | `QA-PRM-062-V0-A` × 1 u: precio $100,00; automático $13,33; manual $0,00; neto $86,67; lista aplicada: precio normal<br>`QA-PRM-062-V0-B` × 1 u: precio $50,00; automático $6,67; manual $0,00; neto $43,33; lista aplicada: precio normal | Total **$130,00**. |
| 6 | Cargar 1 u de `QA-PRM-062-V0-C` por código. | `QA-PRM-062-V0-A` × 1 u: precio $100,00; automático $25,00; manual $0,00; neto $75,00; lista aplicada: precio normal<br>`QA-PRM-062-V0-B` × 1 u: precio $50,00; automático $0,00; manual $0,00; neto $50,00; lista aplicada: precio normal<br>`QA-PRM-062-V0-C` × 1 u: precio $60,00; automático $15,00; manual $0,00; neto $45,00; lista aplicada: precio normal | Total **$170,00**. |
| 7 | Seleccionar `QA-PRM-062-V0-C`, abrir Ctrl+E y elegir Eliminar. | `QA-PRM-062-V0-A` × 1 u: precio $100,00; automático $13,33; manual $0,00; neto $86,67; lista aplicada: precio normal<br>`QA-PRM-062-V0-B` × 1 u: precio $50,00; automático $6,67; manual $0,00; neto $43,33; lista aplicada: precio normal | Total **$130,00**. |
| 8 | Cargar 1 u de `QA-PRM-062-V0-C` por código. | `QA-PRM-062-V0-A` × 1 u: precio $100,00; automático $25,00; manual $0,00; neto $75,00; lista aplicada: precio normal<br>`QA-PRM-062-V0-B` × 1 u: precio $50,00; automático $0,00; manual $0,00; neto $50,00; lista aplicada: precio normal<br>`QA-PRM-062-V0-C` × 1 u: precio $60,00; automático $15,00; manual $0,00; neto $45,00; lista aplicada: precio normal | Total **$170,00**. |
| 9 | Abandonar la venta y confirmar la salida sin cobrar. | Sin renglones en la operación. | Sin venta cobrada, pago ni cambios de stock o destino de cobro. |
| 10 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 11 | Cargar 1 u de `QA-PRM-062-V0-A` por código. | `QA-PRM-062-V0-A` × 1 u: precio $100,00; automático $0,00; manual $0,00; neto $100,00; lista aplicada: precio normal | Total **$100,00**. |
| 12 | Cargar 1 u de `QA-PRM-062-V0-B` por código. | `QA-PRM-062-V0-A` × 1 u: precio $100,00; automático $13,33; manual $0,00; neto $86,67; lista aplicada: precio normal<br>`QA-PRM-062-V0-B` × 1 u: precio $50,00; automático $6,67; manual $0,00; neto $43,33; lista aplicada: precio normal | Total **$130,00**. |
| 13 | Cargar 1 u de `QA-PRM-062-V0-C` por código. | `QA-PRM-062-V0-A` × 1 u: precio $100,00; automático $25,00; manual $0,00; neto $75,00; lista aplicada: precio normal<br>`QA-PRM-062-V0-B` × 1 u: precio $50,00; automático $0,00; manual $0,00; neto $50,00; lista aplicada: precio normal<br>`QA-PRM-062-V0-C` × 1 u: precio $60,00; automático $15,00; manual $0,00; neto $45,00; lista aplicada: precio normal | Total **$170,00**. |
| 14 | Abrir cobro en efectivo del perfil QA, ingresar $170,00 y cancelar antes de confirmar. | `QA-PRM-062-V0-A` × 1 u: precio $100,00; automático $25,00; manual $0,00; neto $75,00; lista aplicada: precio normal<br>`QA-PRM-062-V0-B` × 1 u: precio $50,00; automático $0,00; manual $0,00; neto $50,00; lista aplicada: precio normal<br>`QA-PRM-062-V0-C` × 1 u: precio $60,00; automático $15,00; manual $0,00; neto $45,00; lista aplicada: precio normal | Total **$170,00**. Conserva toda la canasta; sin venta cobrada, pago ni movimientos. |
| 15 | Retomar el cobro en efectivo del perfil QA, ingresar $170,00 y confirmar una sola vez. | `QA-PRM-062-V0-A` × 1 u: precio $100,00; automático $25,00; manual $0,00; neto $75,00; lista aplicada: precio normal<br>`QA-PRM-062-V0-B` × 1 u: precio $50,00; automático $0,00; manual $0,00; neto $50,00; lista aplicada: precio normal<br>`QA-PRM-062-V0-C` × 1 u: precio $60,00; automático $15,00; manual $0,00; neto $45,00; lista aplicada: precio normal | Total **$170,00**. Una venta y un cobro en efectivo del perfil QA; vuelto cero. Stock: `QA-PRM-062-V0-A` −1 u; `QA-PRM-062-V0-B` −1 u; `QA-PRM-062-V0-C` −1 u. |

## Variante 2: empate-menor-id

### Productos preparados

| Referencia | Código | Precio base | Unidad | Familia / subfamilia / sector | Marca |
| --- | --- | ---: | --- | --- | --- |
| A | `QA-PRM-062-V1-A` | $100,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |
| B | `QA-PRM-062-V1-B` | $50,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |

### Ofertas preparadas

| Oferta | Incluye | Regla | Agrupación | Estado / vigencia inclusiva | Medios habilitados |
| --- | --- | --- | --- | --- | --- |
| `QA-COMBO-987211` | 1 × `QA-PRM-062-V1-A` + 1 × `QA-PRM-062-V1-B` | Precio final del combo completo: $130,00 | No aplica: combo por componentes | Activa; hoy -365 días a hoy +365 días | Todos |
| `QA-COMBO-987210` | 1 × `QA-PRM-062-V1-A` + 1 × `QA-PRM-062-V1-B` | Precio final del combo completo: $130,00 | No aplica: combo por componentes | Activa; hoy -365 días a hoy +365 días | Todos |

Las fechas se refieren a la fecha local usada al preparar el seed; Windows y MySQL deben coincidir. No se modifica el reloj durante el recorrido.

### Pasos y resultados esperados

| Paso | Acción del usuario | Canasta completa después del paso | Resultado |
| ---: | --- | --- | --- |
| 1 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 2 | Cargar 1 u de `QA-PRM-062-V1-A` por código. | `QA-PRM-062-V1-A` × 1 u: precio $100,00; automático $0,00; manual $0,00; neto $100,00; lista aplicada: precio normal | Total **$100,00**. |
| 3 | Cargar 1 u de `QA-PRM-062-V1-B` por código. | `QA-PRM-062-V1-A` × 1 u: precio $100,00; automático $13,33; manual $0,00; neto $86,67; lista aplicada: precio normal<br>`QA-PRM-062-V1-B` × 1 u: precio $50,00; automático $6,67; manual $0,00; neto $43,33; lista aplicada: precio normal | Total **$130,00**. |
| 4 | Abrir cobro en efectivo del perfil QA, ingresar $130,00 y cancelar antes de confirmar. | `QA-PRM-062-V1-A` × 1 u: precio $100,00; automático $13,33; manual $0,00; neto $86,67; lista aplicada: precio normal<br>`QA-PRM-062-V1-B` × 1 u: precio $50,00; automático $6,67; manual $0,00; neto $43,33; lista aplicada: precio normal | Total **$130,00**. Conserva toda la canasta; sin venta cobrada, pago ni movimientos. |
| 5 | Retomar el cobro en efectivo del perfil QA, ingresar $130,00 y confirmar una sola vez. | `QA-PRM-062-V1-A` × 1 u: precio $100,00; automático $13,33; manual $0,00; neto $86,67; lista aplicada: precio normal<br>`QA-PRM-062-V1-B` × 1 u: precio $50,00; automático $6,67; manual $0,00; neto $43,33; lista aplicada: precio normal | Total **$130,00**. Una venta y un cobro en efectivo del perfil QA; vuelto cero. Stock: `QA-PRM-062-V1-A` −1 u; `QA-PRM-062-V1-B` −1 u. |
| 6 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 7 | Cargar 1 u de `QA-PRM-062-V1-B` por código. | `QA-PRM-062-V1-B` × 1 u: precio $50,00; automático $0,00; manual $0,00; neto $50,00; lista aplicada: precio normal | Total **$50,00**. |
| 8 | Cargar 1 u de `QA-PRM-062-V1-A` por código. | `QA-PRM-062-V1-B` × 1 u: precio $50,00; automático $6,67; manual $0,00; neto $43,33; lista aplicada: precio normal<br>`QA-PRM-062-V1-A` × 1 u: precio $100,00; automático $13,33; manual $0,00; neto $86,67; lista aplicada: precio normal | Total **$130,00**. |
| 9 | Abrir cobro en efectivo del perfil QA, ingresar $130,00 y cancelar antes de confirmar. | `QA-PRM-062-V1-B` × 1 u: precio $50,00; automático $6,67; manual $0,00; neto $43,33; lista aplicada: precio normal<br>`QA-PRM-062-V1-A` × 1 u: precio $100,00; automático $13,33; manual $0,00; neto $86,67; lista aplicada: precio normal | Total **$130,00**. Conserva toda la canasta; sin venta cobrada, pago ni movimientos. |
| 10 | Retomar el cobro en efectivo del perfil QA, ingresar $130,00 y confirmar una sola vez. | `QA-PRM-062-V1-B` × 1 u: precio $50,00; automático $6,67; manual $0,00; neto $43,33; lista aplicada: precio normal<br>`QA-PRM-062-V1-A` × 1 u: precio $100,00; automático $13,33; manual $0,00; neto $86,67; lista aplicada: precio normal | Total **$130,00**. Una venta y un cobro en efectivo del perfil QA; vuelto cero. Stock: `QA-PRM-062-V1-B` −1 u; `QA-PRM-062-V1-A` −1 u. |

## Notas del recorrido

- AB ahorra 20; AC ahorra 40 y deja total 170 con B sin descuento.
- El empate se verifica cobrando las dos ventas AB y BA a 130 cada una: ambas deben guardar el ID menor.
- La variante de empate termina con stock A -2, B -2 y dos cobros independientes por un total de 260.
- La leyenda visual del combo queda pendiente de accesibilidad y calibración; se verifican importes e ID persistido.
- Estos datos no acreditan optimización global de cualquier canasta.

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
- **NUEVO PENDIENTE DE PREPARAR:** productos exclusivos A=$100, B=$50, C=$60 y Ajeno=$100, una unidad base cada uno; combo «AB» = A+B por $130 (ahorro $20), combo «AC» = A+C por $120 (ahorro $40). Sin promociones individuales.
- **NUEVO PENDIENTE DE PREPARAR:** perfil de empate independiente con dos combos A+B a $130, nombres distinguibles «Empate menor ID» y «Empate mayor ID» y orden de identidad conocido al preparar los datos. Reservar IDs propios sin asumir que los números del test Java están disponibles.
- Los combos corresponden a productos concretos; Ajeno no es componente. La agrupación por familia/subfamilia/marca es otra regla y permanece fuera de estos perfiles.

## Pasos y resultados esperados

1. Cargar A ×1 y Ajeno ×1. **Esperado:** total $200, sin combo. Quitar Ajeno y cargar B ×1. **Esperado:** bruto $150, descuento $20 y total $130, identificando el combo AB.

2. Agregar C ×1. **Esperado:** bruto $210; gana AC, ahorro $40 y total $170 ($120 de AC + $50 de B). AB deja de aplicarse: A no se consume dos veces y el total no baja a $150 acumulando ambos ahorros.

3. Quitar C. **Esperado:** vuelve al combo AB, bruto $150, descuento $20 y neto $130. Volver a cargar C. **Esperado:** reaparece AC y el total $170. Abandonar sin venta cobrada ni cambios de stock/caja.

4. En el perfil independiente de empate, cargar A ×1 + B ×1. **Esperado:** bruto $150, descuento $20 y neto $130; la leyenda corresponde a «Empate menor ID», sin acumular dos descuentos iguales. Abandonar; repetir desde venta nueva cargando B antes que A. **Esperado:** el mismo combo y el mismo neto $130. Abandonar sin efectos.

5. Restaurar el primer perfil y cargar A ×1 + B ×1 + C ×1. Abrir y cancelar el cobro. **Esperado:** mantiene AC y $170 sin registrar venta cobrada ni mover stock/caja. Retomar y cobrar $170 una sola vez. **Esperado:** una venta y un cobro, caja +$170, stock A −1, B −1 y C −1; Ajeno sin cambios.

## Evidencia y límites

La cifra y el nombre del combo ganador deben quedar registrados en cada recálculo; en el empate, completar con su identidad en la evidencia acotada. No confundir «mayor ahorro del candidato» con una garantía matemática de optimización global de cualquier canasta.

La asignación actual puede reservar un renglón a un combo. No se define aquí cómo repartir sobrantes de ese renglón entre otros combos ni se promete resolver todas las combinaciones globales; esa política requiere una ficha y verificación propias. Datos, contratos de perfil, localizadores de grilla/leyenda/edición y automatización deben prepararse antes de ejecutar. Escribir esta ficha o aplicar un seed parecido no acredita que el caso haya pasado.

## Recuperación

La cancelación del cobro debe devolver las mismas cantidades e importe sin cerrar la operación. Para las variantes abandonadas, confirmar salida y verificar ausencia de venta cobrada y movimientos de stock/caja. Si una comprobación falla, conservar evidencia privada antes de restaurar el baseline; no borrar filas ni modificar descuentos para conseguir el resultado. Cada perfil independiente comienza con datos controlados y no reutiliza operaciones anteriores.

## Anexo técnico y trazabilidad

Fuente ERP verificada: commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; `src/ModuloFinanzas/Entidades/OfertaComboCalculador.java`, `src/ModuloVentas/Servicios/OfertaComboService.java` y `test/ModuloFinanzas/Entidades/OfertaComboCalculadorTest.java`. `OfertaComboCalculadorTest.eligeMayorAhorroYDesempataPorIdAscendente`; `OfertaComboCalculador.Candidato.esMejorQue` compara ahorro y luego ID. `obtenerDisponibles` excluye líneas ya asignadas. Los importes $100/$50/$60 y $130/$120 coinciden con el ejemplo fuente.

Comprobar UI y persistencia mediante lecturas acotadas por operación/contexto: bruto `vecTotal`, automático `vecOferta`, manual `vecOfertaManual` cuando corresponda, neto `venTotal`, identidad/leyenda del combo, un cobro y deltas declarados. El número de filas de pago no se deduce sin revisar el contrato del cobro simple. Selectores y oráculos para estas variantes permanecen pendientes de calibración; no usar coordenadas fijas. Registrar SHA256/build JAR, paquete, perfil y versión de datos. INFO resume, DEBUG muestra pasos y TRACE agrega diagnóstico saneado; un fallo informa paso, esperado, observado, categoría y evidencia, con causa no determinada si no está demostrada. No exponer filas completas, credenciales ni árboles privados.
<!-- END ORIGINAL OFFER DESIGN -->

</details>
