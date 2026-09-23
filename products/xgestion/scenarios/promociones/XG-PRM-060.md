---
{"id":"XG-PRM-060","title":"Completar un combo, quitar un componente y recuperar el beneficio","product":"xgestion","module":"promociones","tags":["xgestion","regression","promociones","promociones-combos","escritura"],"status":"implemented","test":"products/xgestion/suites/ofertas/combos.robot","seed":"catalogo-comercial-v1"}
---

# XG-PRM-060 — Completar un combo, quitar un componente y recuperar el beneficio

## Objetivo

El vendedor ve cuándo un conjunto de productos forma un combo y recupera el precio correcto al quitar y volver a agregar un componente.

<!-- BEGIN GENERATED OFFER JOURNEY -->

## Recorrido de automatización

Estado del catálogo: **implemented**. Automatización catalogada en [`combos.robot`](../../suites/ofertas/combos.robot). Validación real: **pendiente**; requiere ejecutar el JAR exacto en el laboratorio calibrado.

Las tablas siguientes son los datos y pasos actuales del recorrido. Los importes son expectativas fijas, no resultados medidos. El diseño anterior queda al final como referencia histórica para conservar reglas, variantes y límites; sus estados y códigos no describen la implementación actual.

```powershell
.\qa.cmd run --product xgestion --scenario XG-PRM-060 --seed catalogo-comercial-v1 --log-level DEBUG
```

## Perfil y preparación

Windows QA exclusivo y offline, escritorio desbloqueado, paquete autorizado y baseline restaurable. ARS, IVA 0 %, comprobante interno 99, stock suficiente, sin impresión ni fiscalización. Cliente y turno sin listas automáticas; otros descuentos, recargos y fidelización deshabilitados, salvo lo indicado en cada variante.

Preparar mediante el runner y `catalogo-comercial-v1` antes de abrir el JAR. Los códigos públicos de abajo pertenecen a este recorrido y reemplazan los ejemplos genéricos del diseño original. No cambiar reglas mediante SQL durante la venta. La falta de perfil, seed o calibración accesible se informa como bloqueo.

Cada variante inicia el JAR de forma independiente. Los perfiles de configuración de 070 y 079 además requieren su preparación y restauración por fase. Una misma ficha conserva un solo ID lógico; solo queda aprobada si todas las variantes requeridas producen evidencia completa.

**Lectura de importes:** automático y manual son descuentos totales del renglón. La grilla muestra ambos sumados en Descuentos; el informe y la evidencia de persistencia los distinguen. El neto de todos los renglones debe sumar el total de la venta.

## Variante 1: completar-quitar-retomar

### Productos preparados

| Referencia | Código | Precio base | Unidad | Familia / subfamilia / sector | Marca |
| --- | --- | ---: | --- | --- | --- |
| A | `QA-PRM-060-V0-A` | $1.000,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |
| B | `QA-PRM-060-V0-B` | $1.000,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |
| E | `QA-PRM-060-V0-E` | $1.000,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |

### Ofertas preparadas

| Oferta | Incluye | Regla | Agrupación | Estado / vigencia inclusiva | Medios habilitados |
| --- | --- | --- | --- | --- | --- |
| `QA-COMBO-987000` | 1 × `QA-PRM-060-V0-A` + 1 × `QA-PRM-060-V0-B` | Precio final del combo completo: $1.500,00 | No aplica: combo por componentes | Activa; hoy -365 días a hoy +365 días | Todos |
| `QA-SOBRANTE-987001` | Producto `QA-PRM-060-V0-A` | 10 % sobre el importe | OFF | Activa; hoy -365 días a hoy +365 días | Todos |

Las fechas se refieren a la fecha local usada al preparar el seed; Windows y MySQL deben coincidir. No se modifica el reloj durante el recorrido.

### Pasos y resultados esperados

| Paso | Acción del usuario | Canasta completa después del paso | Resultado |
| ---: | --- | --- | --- |
| 1 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 2 | Cargar 1 u de `QA-PRM-060-V0-A` por código. | `QA-PRM-060-V0-A` × 1 u: precio $1.000,00; automático $100,00; manual $0,00; neto $900,00; lista aplicada: precio normal | Total **$900,00**. |
| 3 | Cargar 1 u de `QA-PRM-060-V0-E` por código. | `QA-PRM-060-V0-A` × 1 u: precio $1.000,00; automático $100,00; manual $0,00; neto $900,00; lista aplicada: precio normal<br>`QA-PRM-060-V0-E` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal | Total **$1.900,00**. |
| 4 | Cargar 1 u de `QA-PRM-060-V0-B` por código. | `QA-PRM-060-V0-A` × 1 u: precio $1.000,00; automático $250,00; manual $0,00; neto $750,00; lista aplicada: precio normal<br>`QA-PRM-060-V0-E` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal<br>`QA-PRM-060-V0-B` × 1 u: precio $1.000,00; automático $250,00; manual $0,00; neto $750,00; lista aplicada: precio normal | Total **$2.500,00**. |
| 5 | Seleccionar `QA-PRM-060-V0-E`, abrir Ctrl+E y elegir Eliminar. | `QA-PRM-060-V0-A` × 1 u: precio $1.000,00; automático $250,00; manual $0,00; neto $750,00; lista aplicada: precio normal<br>`QA-PRM-060-V0-B` × 1 u: precio $1.000,00; automático $250,00; manual $0,00; neto $750,00; lista aplicada: precio normal | Total **$1.500,00**. |
| 6 | Seleccionar `QA-PRM-060-V0-B`, abrir Ctrl+E y elegir Eliminar. | `QA-PRM-060-V0-A` × 1 u: precio $1.000,00; automático $100,00; manual $0,00; neto $900,00; lista aplicada: precio normal | Total **$900,00**. |
| 7 | Cargar 1 u de `QA-PRM-060-V0-B` por código. | `QA-PRM-060-V0-A` × 1 u: precio $1.000,00; automático $250,00; manual $0,00; neto $750,00; lista aplicada: precio normal<br>`QA-PRM-060-V0-B` × 1 u: precio $1.000,00; automático $250,00; manual $0,00; neto $750,00; lista aplicada: precio normal | Total **$1.500,00**. |
| 8 | Abandonar la venta y confirmar la salida sin cobrar. | Sin renglones en la operación. | Sin venta cobrada, pago ni cambios de stock o destino de cobro. |
| 9 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 10 | Cargar 1 u de `QA-PRM-060-V0-A` por código. | `QA-PRM-060-V0-A` × 1 u: precio $1.000,00; automático $100,00; manual $0,00; neto $900,00; lista aplicada: precio normal | Total **$900,00**. |
| 11 | Cargar 1 u de `QA-PRM-060-V0-B` por código. | `QA-PRM-060-V0-A` × 1 u: precio $1.000,00; automático $250,00; manual $0,00; neto $750,00; lista aplicada: precio normal<br>`QA-PRM-060-V0-B` × 1 u: precio $1.000,00; automático $250,00; manual $0,00; neto $750,00; lista aplicada: precio normal | Total **$1.500,00**. |
| 12 | Abrir cobro en efectivo del perfil QA, ingresar $1.500,00 y cancelar antes de confirmar. | `QA-PRM-060-V0-A` × 1 u: precio $1.000,00; automático $250,00; manual $0,00; neto $750,00; lista aplicada: precio normal<br>`QA-PRM-060-V0-B` × 1 u: precio $1.000,00; automático $250,00; manual $0,00; neto $750,00; lista aplicada: precio normal | Total **$1.500,00**. Conserva toda la canasta; sin venta cobrada, pago ni movimientos. |
| 13 | Retomar el cobro en efectivo del perfil QA, ingresar $1.500,00 y confirmar una sola vez. | `QA-PRM-060-V0-A` × 1 u: precio $1.000,00; automático $250,00; manual $0,00; neto $750,00; lista aplicada: precio normal<br>`QA-PRM-060-V0-B` × 1 u: precio $1.000,00; automático $250,00; manual $0,00; neto $750,00; lista aplicada: precio normal | Total **$1.500,00**. Una venta y un cobro en efectivo del perfil QA; vuelto cero. Stock: `QA-PRM-060-V0-A` −1 u; `QA-PRM-060-V0-B` −1 u. |

## Variante 2: combo-sin-ahorro

### Productos preparados

| Referencia | Código | Precio base | Unidad | Familia / subfamilia / sector | Marca |
| --- | --- | ---: | --- | --- | --- |
| A | `QA-PRM-060-V1-A` | $1.000,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |
| B | `QA-PRM-060-V1-B` | $1.000,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |
| E | `QA-PRM-060-V1-E` | $1.000,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |

### Ofertas preparadas

| Oferta | Incluye | Regla | Agrupación | Estado / vigencia inclusiva | Medios habilitados |
| --- | --- | --- | --- | --- | --- |
| `QA-COMBO-987010` | 1 × `QA-PRM-060-V1-A` + 1 × `QA-PRM-060-V1-B` | Precio final del combo completo: $2.000,00 | No aplica: combo por componentes | Activa; hoy -365 días a hoy +365 días | Todos |
| `QA-SOBRANTE-987011` | Producto `QA-PRM-060-V1-A` | 10 % sobre el importe | OFF | Activa; hoy -365 días a hoy +365 días | Todos |

Las fechas se refieren a la fecha local usada al preparar el seed; Windows y MySQL deben coincidir. No se modifica el reloj durante el recorrido.

### Pasos y resultados esperados

| Paso | Acción del usuario | Canasta completa después del paso | Resultado |
| ---: | --- | --- | --- |
| 1 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 2 | Cargar 1 u de `QA-PRM-060-V1-A` por código. | `QA-PRM-060-V1-A` × 1 u: precio $1.000,00; automático $100,00; manual $0,00; neto $900,00; lista aplicada: precio normal | Total **$900,00**. |
| 3 | Cargar 1 u de `QA-PRM-060-V1-B` por código. | `QA-PRM-060-V1-A` × 1 u: precio $1.000,00; automático $100,00; manual $0,00; neto $900,00; lista aplicada: precio normal<br>`QA-PRM-060-V1-B` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal | Total **$1.900,00**. |
| 4 | Abandonar la venta y confirmar la salida sin cobrar. | Sin renglones en la operación. | Sin venta cobrada, pago ni cambios de stock o destino de cobro. |

## Variante 3: combo-mas-caro

### Productos preparados

| Referencia | Código | Precio base | Unidad | Familia / subfamilia / sector | Marca |
| --- | --- | ---: | --- | --- | --- |
| A | `QA-PRM-060-V2-A` | $1.000,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |
| B | `QA-PRM-060-V2-B` | $1.000,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |
| E | `QA-PRM-060-V2-E` | $1.000,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |

### Ofertas preparadas

| Oferta | Incluye | Regla | Agrupación | Estado / vigencia inclusiva | Medios habilitados |
| --- | --- | --- | --- | --- | --- |
| `QA-COMBO-987020` | 1 × `QA-PRM-060-V2-A` + 1 × `QA-PRM-060-V2-B` | Precio final del combo completo: $2.100,00 | No aplica: combo por componentes | Activa; hoy -365 días a hoy +365 días | Todos |
| `QA-SOBRANTE-987021` | Producto `QA-PRM-060-V2-A` | 10 % sobre el importe | OFF | Activa; hoy -365 días a hoy +365 días | Todos |

Las fechas se refieren a la fecha local usada al preparar el seed; Windows y MySQL deben coincidir. No se modifica el reloj durante el recorrido.

### Pasos y resultados esperados

| Paso | Acción del usuario | Canasta completa después del paso | Resultado |
| ---: | --- | --- | --- |
| 1 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 2 | Cargar 1 u de `QA-PRM-060-V2-A` por código. | `QA-PRM-060-V2-A` × 1 u: precio $1.000,00; automático $100,00; manual $0,00; neto $900,00; lista aplicada: precio normal | Total **$900,00**. |
| 3 | Cargar 1 u de `QA-PRM-060-V2-B` por código. | `QA-PRM-060-V2-A` × 1 u: precio $1.000,00; automático $100,00; manual $0,00; neto $900,00; lista aplicada: precio normal<br>`QA-PRM-060-V2-B` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal | Total **$1.900,00**. |
| 4 | Abandonar la venta y confirmar la salida sin cobrar. | Sin renglones en la operación. | Sin venta cobrada, pago ni cambios de stock o destino de cobro. |

## Notas del recorrido

- A incompleto cuesta 900 por su oferta individual; completo, 1500 sin duplicar beneficio.
- Los combos sin ahorro dejan total 1900 por la oferta individual de A.
- La leyenda visual del combo queda pendiente de accesibilidad y calibración; se verifican importes e ID persistido.

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
- Datos existentes: `catalogo-comercial-v1`, ejemplo `COMBO`. A = `QA-SEED-COMBO-A`, B = `QA-SEED-COMBO-B`, ambos $1.000 por unidad; un A + un B por $1.500. Ajeno = `QA-SEED-NORMAL`, $1.000.
- El seed contiene además 10 % individual para A: cuando A no entra en el combo, su unidad cuesta $900. No suponer que el combo incompleto deja A a $1.000.
- Variante de combo sin ahorro: **NUEVO PENDIENTE DE PREPARAR**, copia independiente del perfil con precio de combo $2.000 y otra con $2.100, conservando la oferta individual de A. No cambiar el seed existente ni sus reglas durante la prueba.

## Pasos y resultados esperados

1. Cargar A ×1. **Esperado:** bruto $1.000, oferta individual $100, neto $900; no aparece un combo completo.

2. Agregar Ajeno ×1. **Esperado:** bruto $2.000, oferta $100, neto $1.900; Ajeno no reemplaza a B. Agregar B ×1. **Esperado:** bruto $3.000, descuento total $500 y neto $2.500: combo $1.500 + Ajeno $1.000, sin sumar otro 10 % sobre el A consumido.

3. Quitar Ajeno. **Esperado:** A ×1 + B ×1, bruto $2.000, descuento $500, neto $1.500. Quitar B. **Esperado:** A ×1 vuelve a bruto $1.000, descuento individual $100 y neto $900; no conserva un descuento o una leyenda de combo completo.

4. Volver a agregar B. **Esperado:** un combo por $1.500, sin duplicación de descuento. Abandonar y confirmar. **Esperado:** no registra venta cobrada ni movimientos de stock/caja.

5. En perfiles independientes restaurados con precio de combo $2.000 y luego $2.100, cargar A ×1 + B ×1. **Esperado en ambos:** el combo sin ahorro no se aplica; bruto $2.000, descuento individual de A $100, neto $1.900. Abandonar sin efectos. No confundir este límite con la selección entre combos beneficiosos.

6. Restaurar el perfil seed original y cargar A ×1 + B ×1. Abrir el cobro y cancelarlo. **Esperado:** se conserva neto $1.500, sin venta cobrada ni cambios en stock/caja. Retomar y confirmar una sola vez $1.500. **Esperado:** una venta, un cobro, caja +$1.500, stock A −1 y B −1; Ajeno sin cambios.

## Evidencia y límites

Capturar los estados incompleto/completo/incompleto, la leyenda del combo y bruto/oferta/neto de cada línea. El descuento del combo se distribuye entre A y B; el 10 % de A solo reaparece cuando queda fuera. Comparar los perfiles de combo sin ahorro por separado.

No cubre combos competidores, redondeos, fracciones, listas ni reparto entre comensales. Datos, contratos de perfil, localizadores de grilla/leyenda/edición y automatización deben prepararse antes de ejecutar. Escribir esta ficha o aplicar un seed parecido no acredita que el caso haya pasado.

## Recuperación

La cancelación del cobro debe devolver las mismas cantidades e importe sin cerrar la operación. Para las variantes abandonadas, confirmar salida y verificar ausencia de venta cobrada y movimientos de stock/caja. Si una comprobación falla, conservar evidencia privada antes de restaurar el baseline; no borrar filas ni modificar descuentos para conseguir el resultado. Cada perfil independiente comienza con datos controlados y no reutiliza operaciones anteriores.

## Anexo técnico y trazabilidad

Fuente ERP verificada: commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; `src/ModuloFinanzas/Entidades/OfertaComboCalculador.java`, `src/ModuloVentas/Servicios/OfertaComboService.java` y `test/ModuloFinanzas/Entidades/OfertaComboCalculadorTest.java`. `OfertaComboCalculadorTest.aplicaComboExactoYProrrateaElDescuento` y `noAplicaComboIncompletoONoBeneficioso`; `OfertaComboService.calcularTradicional` aplica la oferta individual únicamente a la cantidad sobrante. Ejemplo seed `COMBO`, enlazado desde `seeds/pricing.py`.

Comprobar UI y persistencia mediante lecturas acotadas por operación/contexto: bruto `vecTotal`, automático `vecOferta`, manual `vecOfertaManual` cuando corresponda, neto `venTotal`, identidad/leyenda del combo, un cobro y deltas declarados. El número de filas de pago no se deduce sin revisar el contrato del cobro simple. Selectores y oráculos para estas variantes permanecen pendientes de calibración; no usar coordenadas fijas. Registrar SHA256/build JAR, paquete, perfil y versión de datos. INFO resume, DEBUG muestra pasos y TRACE agrega diagnóstico saneado; un fallo informa paso, esperado, observado, categoría y evidencia, con causa no determinada si no está demostrada. No exponer filas completas, credenciales ni árboles privados.
<!-- END ORIGINAL OFFER DESIGN -->

</details>
