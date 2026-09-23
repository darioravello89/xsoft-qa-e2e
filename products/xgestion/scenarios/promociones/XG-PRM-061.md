---
{"id":"XG-PRM-061","title":"Repetir combos y descontar solo los productos sobrantes","product":"xgestion","module":"promociones","tags":["xgestion","regression","promociones","promociones-combos","escritura"],"status":"implemented","test":"products/xgestion/suites/ofertas/combos.robot","seed":"catalogo-comercial-v1"}
---

# XG-PRM-061 — Repetir combos y descontar solo los productos sobrantes

## Objetivo

El vendedor distingue cuántos combos completos compra el cliente y comprueba que la promoción individual se aplica únicamente a las unidades sobrantes.

<!-- BEGIN GENERATED OFFER JOURNEY -->

## Recorrido de automatización

Estado del catálogo: **implemented**. Automatización catalogada en [`combos.robot`](../../suites/ofertas/combos.robot). Validación real: **pendiente**; requiere ejecutar el JAR exacto en el laboratorio calibrado.

Las tablas siguientes son los datos y pasos actuales del recorrido. Los importes son expectativas fijas, no resultados medidos. El diseño anterior queda al final como referencia histórica para conservar reglas, variantes y límites; sus estados y códigos no describen la implementación actual.

```powershell
.\qa.cmd run --product xgestion --scenario XG-PRM-061 --seed catalogo-comercial-v1 --log-level DEBUG
```

## Perfil y preparación

Windows QA exclusivo y offline, escritorio desbloqueado, paquete autorizado y baseline restaurable. ARS, IVA 0 %, comprobante interno 99, stock suficiente, sin impresión ni fiscalización. Cliente y turno sin listas automáticas; otros descuentos, recargos y fidelización deshabilitados, salvo lo indicado en cada variante.

Preparar mediante el runner y `catalogo-comercial-v1` antes de abrir el JAR. Los códigos públicos de abajo pertenecen a este recorrido y reemplazan los ejemplos genéricos del diseño original. No cambiar reglas mediante SQL durante la venta. La falta de perfil, seed o calibración accesible se informa como bloqueo.

Cada variante inicia el JAR de forma independiente. Los perfiles de configuración de 070 y 079 además requieren su preparación y restauración por fase. Una misma ficha conserva un solo ID lógico; solo queda aprobada si todas las variantes requeridas producen evidencia completa.

**Lectura de importes:** automático y manual son descuentos totales del renglón. La grilla muestra ambos sumados en Descuentos; el informe y la evidencia de persistencia los distinguen. El neto de todos los renglones debe sumar el total de la venta.

## Variante 1: repeticiones-y-sobrantes

### Productos preparados

| Referencia | Código | Precio base | Unidad | Familia / subfamilia / sector | Marca |
| --- | --- | ---: | --- | --- | --- |
| A | `QA-PRM-061-V0-A` | $1.000,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |
| B | `QA-PRM-061-V0-B` | $1.000,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |
| E | `QA-PRM-061-V0-E` | $1.000,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |

### Ofertas preparadas

| Oferta | Incluye | Regla | Agrupación | Estado / vigencia inclusiva | Medios habilitados |
| --- | --- | --- | --- | --- | --- |
| `QA-COMBO-987100` | 1 × `QA-PRM-061-V0-A` + 1 × `QA-PRM-061-V0-B` | Precio final del combo completo: $1.500,00 | No aplica: combo por componentes | Activa; hoy -365 días a hoy +365 días | Todos |
| `QA-SOBRANTE-987101` | Producto `QA-PRM-061-V0-A` | 10 % sobre el importe | OFF | Activa; hoy -365 días a hoy +365 días | Todos |

Las fechas se refieren a la fecha local usada al preparar el seed; Windows y MySQL deben coincidir. No se modifica el reloj durante el recorrido.

### Pasos y resultados esperados

| Paso | Acción del usuario | Canasta completa después del paso | Resultado |
| ---: | --- | --- | --- |
| 1 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 2 | Cargar 2 u de `QA-PRM-061-V0-A` por código. | `QA-PRM-061-V0-A` × 2 u: precio $1.000,00; automático $200,00; manual $0,00; neto $1.800,00; lista aplicada: precio normal | Total **$1.800,00**. |
| 3 | Cargar 1 u de `QA-PRM-061-V0-B` por código. | `QA-PRM-061-V0-A` × 2 u: precio $1.000,00; automático $350,00; manual $0,00; neto $1.650,00; lista aplicada: precio normal<br>`QA-PRM-061-V0-B` × 1 u: precio $1.000,00; automático $250,00; manual $0,00; neto $750,00; lista aplicada: precio normal | Total **$2.400,00**. |
| 4 | Cargar 1 u de `QA-PRM-061-V0-E` por código. | `QA-PRM-061-V0-A` × 2 u: precio $1.000,00; automático $350,00; manual $0,00; neto $1.650,00; lista aplicada: precio normal<br>`QA-PRM-061-V0-B` × 1 u: precio $1.000,00; automático $250,00; manual $0,00; neto $750,00; lista aplicada: precio normal<br>`QA-PRM-061-V0-E` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal | Total **$3.400,00**. |
| 5 | Seleccionar `QA-PRM-061-V0-E`, abrir Ctrl+E y elegir Eliminar. | `QA-PRM-061-V0-A` × 2 u: precio $1.000,00; automático $350,00; manual $0,00; neto $1.650,00; lista aplicada: precio normal<br>`QA-PRM-061-V0-B` × 1 u: precio $1.000,00; automático $250,00; manual $0,00; neto $750,00; lista aplicada: precio normal | Total **$2.400,00**. |
| 6 | Seleccionar `QA-PRM-061-V0-B`, abrir Ctrl+E, dejar 2 u y guardar. | `QA-PRM-061-V0-A` × 2 u: precio $1.000,00; automático $500,00; manual $0,00; neto $1.500,00; lista aplicada: precio normal<br>`QA-PRM-061-V0-B` × 2 u: precio $1.000,00; automático $500,00; manual $0,00; neto $1.500,00; lista aplicada: precio normal | Total **$3.000,00**. |
| 7 | Seleccionar `QA-PRM-061-V0-A`, abrir Ctrl+E, dejar 3 u y guardar. | `QA-PRM-061-V0-A` × 3 u: precio $1.000,00; automático $600,00; manual $0,00; neto $2.400,00; lista aplicada: precio normal<br>`QA-PRM-061-V0-B` × 2 u: precio $1.000,00; automático $500,00; manual $0,00; neto $1.500,00; lista aplicada: precio normal | Total **$3.900,00**. |
| 8 | Seleccionar `QA-PRM-061-V0-B`, abrir Ctrl+E, dejar 1 u y guardar. | `QA-PRM-061-V0-A` × 3 u: precio $1.000,00; automático $450,00; manual $0,00; neto $2.550,00; lista aplicada: precio normal<br>`QA-PRM-061-V0-B` × 1 u: precio $1.000,00; automático $250,00; manual $0,00; neto $750,00; lista aplicada: precio normal | Total **$3.300,00**. |
| 9 | Seleccionar `QA-PRM-061-V0-B`, abrir Ctrl+E, dejar 2 u y guardar. | `QA-PRM-061-V0-A` × 3 u: precio $1.000,00; automático $600,00; manual $0,00; neto $2.400,00; lista aplicada: precio normal<br>`QA-PRM-061-V0-B` × 2 u: precio $1.000,00; automático $500,00; manual $0,00; neto $1.500,00; lista aplicada: precio normal | Total **$3.900,00**. |
| 10 | Abrir cobro en efectivo del perfil QA, ingresar $3.900,00 y cancelar antes de confirmar. | `QA-PRM-061-V0-A` × 3 u: precio $1.000,00; automático $600,00; manual $0,00; neto $2.400,00; lista aplicada: precio normal<br>`QA-PRM-061-V0-B` × 2 u: precio $1.000,00; automático $500,00; manual $0,00; neto $1.500,00; lista aplicada: precio normal | Total **$3.900,00**. Conserva toda la canasta; sin venta cobrada, pago ni movimientos. |
| 11 | Retomar el cobro en efectivo del perfil QA, ingresar $3.900,00 y confirmar una sola vez. | `QA-PRM-061-V0-A` × 3 u: precio $1.000,00; automático $600,00; manual $0,00; neto $2.400,00; lista aplicada: precio normal<br>`QA-PRM-061-V0-B` × 2 u: precio $1.000,00; automático $500,00; manual $0,00; neto $1.500,00; lista aplicada: precio normal | Total **$3.900,00**. Una venta y un cobro en efectivo del perfil QA; vuelto cero. Stock: `QA-PRM-061-V0-A` −3 u; `QA-PRM-061-V0-B` −2 u. |

## Notas del recorrido

- Totales: 2A+B=2400; 2A+2B=3000; 3A+2B=3900; 3A+B=3300.
- La línea conserva ID del combo aunque su descuento incluya el beneficio del sobrante.

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
- Datos existentes: `catalogo-comercial-v1`, ejemplo `COMBO-SOBRANTE`. A = `QA-SEED-COMBO-A` y B = `QA-SEED-COMBO-B`, precio base $1.000 cada uno; combo A ×1 + B ×1 por $1.500 y 10 % para A sobrante. Ajeno = `QA-SEED-NORMAL`, $1.000.
- Usar unidades enteras. El ejemplo seed fija 2A + B por $2.400; las demás cantidades de esta ficha usan las mismas reglas y productos, con expectativas derivadas manualmente.

## Pasos y resultados esperados

1. Cargar A ×2 + B ×1. **Esperado:** bruto $3.000, un combo por $1.500 más A sobrante a $900, descuento total $600 y neto $2.400. Solo una unidad de A recibe el 10 % individual.

2. Agregar Ajeno ×1. **Esperado:** bruto $4.000, descuento $600, neto $3.400; Ajeno no completa otro combo ni recibe la oferta. Quitar Ajeno. **Esperado:** vuelve a $2.400.

3. Editar B a ×2. **Esperado:** 2A + 2B forman dos combos, bruto $4.000, descuento $1.000, neto $3.000; ninguna unidad de A queda para el 10 % individual.

4. Editar A a ×3. **Esperado:** bruto $5.000, dos combos por $3.000 más A sobrante a $900, descuento total $1.100, neto $3.900. La venta mantiene los dos productos correctos y sus cantidades.

5. Reducir B a ×1. **Esperado:** 3A + B, bruto $4.000; un combo $1.500 y dos A sobrantes a $900 cada uno, descuento total $700, neto $3.300. Volver B a ×2. **Esperado:** vuelve a $3.900 sin conservar descuentos del estado anterior.

6. Abrir y cancelar el cobro. **Esperado:** conserva 3A + 2B y neto $3.900, sin venta cobrada ni movimientos de stock/caja. Retomar y confirmar $3.900 una sola vez. **Esperado:** una venta y un cobro, caja +$3.900, stock A −3, B −2; Ajeno sin cambios.

## Evidencia y límites

Guardar cantidad de aplicaciones del combo, descuento total y neto al pasar por 1 → 2 → 1 → 2 combos. En 3A + 2B, la suma automática es $1.000 de combo + $100 individual; verificarla sin exigir que ambas promociones ocupen dos filas distintas.

No cubre sobrantes consumidos por otro combo, combinaciones agrupadas ni fracciones. Datos, contratos de perfil, localizadores de grilla/leyenda/edición y automatización deben prepararse antes de ejecutar. Escribir esta ficha o aplicar un seed parecido no acredita que el caso haya pasado.

## Recuperación

La cancelación del cobro debe devolver las mismas cantidades e importe sin cerrar la operación. Para las variantes abandonadas, confirmar salida y verificar ausencia de venta cobrada y movimientos de stock/caja. Si una comprobación falla, conservar evidencia privada antes de restaurar el baseline; no borrar filas ni modificar descuentos para conseguir el resultado. Cada perfil independiente comienza con datos controlados y no reutiliza operaciones anteriores.

## Anexo técnico y trazabilidad

Fuente ERP verificada: commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; `src/ModuloFinanzas/Entidades/OfertaComboCalculador.java`, `src/ModuloVentas/Servicios/OfertaComboService.java` y `test/ModuloFinanzas/Entidades/OfertaComboCalculadorTest.java`. `OfertaComboCalculadorTest.repiteComboConCantidadesDecimalesYDejaSobrante` orienta la repetición; `OfertaComboService` evalúa primero combo y después `calcularTradicional` sobre sobrantes. Datos exactos iniciales: ejemplo seed `COMBO-SOBRANTE`.

Comprobar UI y persistencia mediante lecturas acotadas por operación/contexto: bruto `vecTotal`, automático `vecOferta`, manual `vecOfertaManual` cuando corresponda, neto `venTotal`, identidad/leyenda del combo, un cobro y deltas declarados. El número de filas de pago no se deduce sin revisar el contrato del cobro simple. Selectores y oráculos para estas variantes permanecen pendientes de calibración; no usar coordenadas fijas. Registrar SHA256/build JAR, paquete, perfil y versión de datos. INFO resume, DEBUG muestra pasos y TRACE agrega diagnóstico saneado; un fallo informa paso, esperado, observado, categoría y evidencia, con causa no determinada si no está demostrada. No exponer filas completas, credenciales ni árboles privados.
<!-- END ORIGINAL OFFER DESIGN -->

</details>
