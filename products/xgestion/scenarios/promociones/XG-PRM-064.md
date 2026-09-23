---
{"id":"XG-PRM-064","title":"Completar y repetir un combo con cantidades fraccionarias","product":"xgestion","module":"promociones","tags":["xgestion","regression","promociones","promociones-combos","escritura"],"status":"implemented","test":"products/xgestion/suites/ofertas/combos.robot","seed":"catalogo-comercial-v1"}
---

# XG-PRM-064 — Completar y repetir un combo con cantidades fraccionarias

## Objetivo

El vendedor combina cantidades pesables, reconoce el límite de un combo completo y conserva los sobrantes al editar y cobrar.

<!-- BEGIN GENERATED OFFER JOURNEY -->

## Recorrido de automatización

Estado del catálogo: **implemented**. Automatización catalogada en [`combos.robot`](../../suites/ofertas/combos.robot). Validación real: **pendiente**; requiere ejecutar el JAR exacto en el laboratorio calibrado.

Las tablas siguientes son los datos y pasos actuales del recorrido. Los importes son expectativas fijas, no resultados medidos. El diseño anterior queda al final como referencia histórica para conservar reglas, variantes y límites; sus estados y códigos no describen la implementación actual.

```powershell
.\qa.cmd run --product xgestion --scenario XG-PRM-064 --seed catalogo-comercial-v1 --log-level DEBUG
```

## Perfil y preparación

Windows QA exclusivo y offline, escritorio desbloqueado, paquete autorizado y baseline restaurable. ARS, IVA 0 %, comprobante interno 99, stock suficiente, sin impresión ni fiscalización. Cliente y turno sin listas automáticas; otros descuentos, recargos y fidelización deshabilitados, salvo lo indicado en cada variante.

Preparar mediante el runner y `catalogo-comercial-v1` antes de abrir el JAR. Los códigos públicos de abajo pertenecen a este recorrido y reemplazan los ejemplos genéricos del diseño original. No cambiar reglas mediante SQL durante la venta. La falta de perfil, seed o calibración accesible se informa como bloqueo.

Cada variante inicia el JAR de forma independiente. Los perfiles de configuración de 070 y 079 además requieren su preparación y restauración por fase. Una misma ficha conserva un solo ID lógico; solo queda aprobada si todas las variantes requeridas producen evidencia completa.

**Lectura de importes:** automático y manual son descuentos totales del renglón. La grilla muestra ambos sumados en Descuentos; el informe y la evidencia de persistencia los distinguen. El neto de todos los renglones debe sumar el total de la venta.

## Variante 1: fracciones-y-limites

### Productos preparados

| Referencia | Código | Precio base | Unidad | Familia / subfamilia / sector | Marca |
| --- | --- | ---: | --- | --- | --- |
| A | `QA-PRM-064-V0-A` | $40,00 | kg | 980001 / 980001 / 980001 | QA-SEED |
| B | `QA-PRM-064-V0-B` | $20,00 | kg | 980001 / 980001 / 980001 | QA-SEED |
| E | `QA-PRM-064-V0-E` | $10,00 | unidad | 980001 / 980001 / 980001 | QA-SEED |

### Ofertas preparadas

| Oferta | Incluye | Regla | Agrupación | Estado / vigencia inclusiva | Medios habilitados |
| --- | --- | --- | --- | --- | --- |
| `QA-COMBO-987400` | 0,500 × `QA-PRM-064-V0-A` + 1,250 × `QA-PRM-064-V0-B` | Precio final del combo completo: $40,00 | No aplica: combo por componentes | Activa; hoy -365 días a hoy +365 días | Todos |

Las fechas se refieren a la fecha local usada al preparar el seed; Windows y MySQL deben coincidir. No se modifica el reloj durante el recorrido.

### Pasos y resultados esperados

| Paso | Acción del usuario | Canasta completa después del paso | Resultado |
| ---: | --- | --- | --- |
| 1 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 2 | Cargar 0,250 kg de `QA-PRM-064-V0-A` por código. | `QA-PRM-064-V0-A` × 0,250 kg: precio $40,00; automático $0,00; manual $0,00; neto $10,00; lista aplicada: precio normal | Total **$10,00**. |
| 3 | Cargar 1,250 kg de `QA-PRM-064-V0-B` por código. | `QA-PRM-064-V0-A` × 0,250 kg: precio $40,00; automático $0,00; manual $0,00; neto $10,00; lista aplicada: precio normal<br>`QA-PRM-064-V0-B` × 1,250 kg: precio $20,00; automático $0,00; manual $0,00; neto $25,00; lista aplicada: precio normal | Total **$35,00**. |
| 4 | Cargar 1 u de `QA-PRM-064-V0-E` por código. | `QA-PRM-064-V0-A` × 0,250 kg: precio $40,00; automático $0,00; manual $0,00; neto $10,00; lista aplicada: precio normal<br>`QA-PRM-064-V0-B` × 1,250 kg: precio $20,00; automático $0,00; manual $0,00; neto $25,00; lista aplicada: precio normal<br>`QA-PRM-064-V0-E` × 1 u: precio $10,00; automático $0,00; manual $0,00; neto $10,00; lista aplicada: precio normal | Total **$45,00**. |
| 5 | Seleccionar `QA-PRM-064-V0-E`, abrir Ctrl+E y elegir Eliminar. | `QA-PRM-064-V0-A` × 0,250 kg: precio $40,00; automático $0,00; manual $0,00; neto $10,00; lista aplicada: precio normal<br>`QA-PRM-064-V0-B` × 1,250 kg: precio $20,00; automático $0,00; manual $0,00; neto $25,00; lista aplicada: precio normal | Total **$35,00**. |
| 6 | Seleccionar `QA-PRM-064-V0-A`, abrir Ctrl+E, dejar 0,500 kg y guardar. | `QA-PRM-064-V0-A` × 0,500 kg: precio $40,00; automático $2,22; manual $0,00; neto $17,78; lista aplicada: precio normal<br>`QA-PRM-064-V0-B` × 1,250 kg: precio $20,00; automático $2,78; manual $0,00; neto $22,22; lista aplicada: precio normal | Total **$40,00**. |
| 7 | Seleccionar `QA-PRM-064-V0-A`, abrir Ctrl+E, dejar 1,250 kg y guardar. | `QA-PRM-064-V0-A` × 1,250 kg: precio $40,00; automático $2,22; manual $0,00; neto $47,78; lista aplicada: precio normal<br>`QA-PRM-064-V0-B` × 1,250 kg: precio $20,00; automático $2,78; manual $0,00; neto $22,22; lista aplicada: precio normal | Total **$70,00**. |
| 8 | Seleccionar `QA-PRM-064-V0-B`, abrir Ctrl+E, dejar 3,000 kg y guardar. | `QA-PRM-064-V0-A` × 1,250 kg: precio $40,00; automático $4,44; manual $0,00; neto $45,56; lista aplicada: precio normal<br>`QA-PRM-064-V0-B` × 3,000 kg: precio $20,00; automático $5,56; manual $0,00; neto $54,44; lista aplicada: precio normal | Total **$100,00**. |
| 9 | Seleccionar `QA-PRM-064-V0-B`, abrir Ctrl+E, dejar 2,490 kg y guardar. | `QA-PRM-064-V0-A` × 1,250 kg: precio $40,00; automático $2,22; manual $0,00; neto $47,78; lista aplicada: precio normal<br>`QA-PRM-064-V0-B` × 2,490 kg: precio $20,00; automático $2,78; manual $0,00; neto $47,02; lista aplicada: precio normal | Total **$94,80**. |
| 10 | Seleccionar `QA-PRM-064-V0-B`, abrir Ctrl+E, dejar 2,500 kg y guardar. | `QA-PRM-064-V0-A` × 1,250 kg: precio $40,00; automático $4,44; manual $0,00; neto $45,56; lista aplicada: precio normal<br>`QA-PRM-064-V0-B` × 2,500 kg: precio $20,00; automático $5,56; manual $0,00; neto $44,44; lista aplicada: precio normal | Total **$90,00**. |
| 11 | Seleccionar `QA-PRM-064-V0-B`, abrir Ctrl+E, dejar 3,000 kg y guardar. | `QA-PRM-064-V0-A` × 1,250 kg: precio $40,00; automático $4,44; manual $0,00; neto $45,56; lista aplicada: precio normal<br>`QA-PRM-064-V0-B` × 3,000 kg: precio $20,00; automático $5,56; manual $0,00; neto $54,44; lista aplicada: precio normal | Total **$100,00**. |
| 12 | Abrir cobro en efectivo del perfil QA, ingresar $100,00 y cancelar antes de confirmar. | `QA-PRM-064-V0-A` × 1,250 kg: precio $40,00; automático $4,44; manual $0,00; neto $45,56; lista aplicada: precio normal<br>`QA-PRM-064-V0-B` × 3,000 kg: precio $20,00; automático $5,56; manual $0,00; neto $54,44; lista aplicada: precio normal | Total **$100,00**. Conserva toda la canasta; sin venta cobrada, pago ni movimientos. |
| 13 | Retomar el cobro en efectivo del perfil QA, ingresar $100,00 y confirmar una sola vez. | `QA-PRM-064-V0-A` × 1,250 kg: precio $40,00; automático $4,44; manual $0,00; neto $45,56; lista aplicada: precio normal<br>`QA-PRM-064-V0-B` × 3,000 kg: precio $20,00; automático $5,56; manual $0,00; neto $54,44; lista aplicada: precio normal | Total **$100,00**. Una venta y un cobro en efectivo del perfil QA; vuelto cero. Stock: `QA-PRM-064-V0-A` −1,250 kg; `QA-PRM-064-V0-B` −3,000 kg. |

## Notas del recorrido

- Combo: A 0.500 kg + B 1.250 kg por 40; ambos con UME decimal.
- Totales: 35, 40, intermedio 70, 100, B 2.490=94.80, B 2.500=90, final 100.
- Stock final: A -1.250 kg, B -3.000 kg; sin balanza ni cantidades de más de tres decimales.

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

**Pendiente de automatizar (`planned`), prioridad P2, etapa 2.** Esta ficha no tiene test Robot ni validación real sobre el JAR. Forma parte del [backlog de promociones](../../docs/promociones-pendientes.md). Los combos se definen por sus componentes; no son la opción «agrupar productos» de una oferta tradicional.

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete autorizado y baseline restaurable. Registrar JAR y contexto propio de empresa/sucursal/puesto; vendedor con permiso de carga, edición, eliminación, cobro y abandono sin supervisor.
- ARS, IVA 0 %, sin otros impuestos; stock suficiente, comprobante interno 99, efectivo exacto, diálogo de cobro habilitado, sin impresión ni fiscalización. Lista Ninguna Lista (ID 0), cliente/turno sin lista automática y fidelización deshabilitada.
- Ofertas activas y vigentes para la sucursal QA, aplicables a todos los medios de pago. Otros descuentos, recargos y condiciones comerciales en cero salvo las excepciones explícitas. Preparar cada variante antes de abrir la venta; no modificar reglas mediante escrituras directas en la base durante el recorrido.
- **NUEVO PENDIENTE DE PREPARAR:** A pesable a $40/KG y B pesable a $20/KG; combo de A 0,500 KG + B 1,250 KG por $40 (base normal $45). Ajeno=$10 por unidad, sin ofertas.
- Permitir cantidades con tres decimales en A/B, stock QA suficiente y carga manual por teclado; no intervienen balanza física ni lector. No hay ofertas individuales ni otros combos.
- El seed no prepara este combo fraccionado. No reutilizar `QA-SEED-COMBO-A/B` suponiendo que tengan estas unidades, precios o componentes.

## Pasos y resultados esperados

1. Cargar A 0,250 KG + B 1,250 KG. **Esperado:** bruto/neto $35 ($10+$25), sin combo: falta A. Agregar Ajeno ×1. **Esperado:** total $45 sin oferta; el importe o cantidad del producto ajeno no completa A. Quitar Ajeno.

2. Editar A a 0,500 KG manteniendo B 1,250 KG. **Esperado:** un combo, bruto $45, descuento $5 y neto $40. Se conservan exactamente las cantidades ingresadas.

3. Editar A a 1,250 KG y B a 3,000 KG. **Esperado:** bruto $110 ($50+$60), dos combos por $80 y sobrantes A 0,250 KG=$10, B 0,500 KG=$10; descuento $10 y neto $100. No se aplica un tercer combo.

4. Reducir B a 2,490 KG manteniendo A 1,250 KG. **Esperado:** bruto $99,80; un combo consume A 0,500 KG y B 1,250 KG, quedan A 0,750 KG y B 1,240 KG; descuento $5 y neto $94,80. No redondear 2,490 a 2,500 para completar otro combo.

5. Editar B a 2,500 KG. **Esperado:** dos combos, bruto $100, descuento $10, neto $90; sobrante A 0,250 KG=$10. Volver B a 3,000 KG. **Esperado:** recupera bruto $110, descuento $10 y neto $100.

6. Abrir y cancelar el cobro. **Esperado:** conserva A 1,250 KG, B 3,000 KG y neto $100, sin venta cobrada ni movimientos de stock/caja. Retomar y confirmar una sola vez $100. **Esperado:** una venta y un cobro, caja +$100, stock A −1,250 KG y B −3,000 KG; Ajeno sin cambios.

## Evidencia y límites

Guardar cantidades con tres decimales, aplicaciones completas del combo, sobrantes y neto antes y después de cada edición. Contrastar deltas de stock en KG, sin convertirlos a unidades enteras. Los ejemplos son cálculos de regla, aún no evidencia del JAR.

Queda pendiente verificar el rechazo o normalización de más de tres decimales en una ficha específica. No extrapolar el cálculo a balanza, bultos, otras unidades ni fracciones de ofertas tradicionales. La accesibilidad del editor decimal debe calibrarse antes de implementar. Datos, contratos de perfil, localizadores de grilla/leyenda/edición y automatización deben prepararse antes de ejecutar. Escribir esta ficha o aplicar un seed parecido no acredita que el caso haya pasado.

## Recuperación

La cancelación del cobro debe devolver las mismas cantidades e importe sin cerrar la operación. Para las variantes abandonadas, confirmar salida y verificar ausencia de venta cobrada y movimientos de stock/caja. Si una comprobación falla, conservar evidencia privada antes de restaurar el baseline; no borrar filas ni modificar descuentos para conseguir el resultado. Cada perfil independiente comienza con datos controlados y no reutiliza operaciones anteriores.

## Anexo técnico y trazabilidad

Fuente ERP verificada: commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; `src/ModuloFinanzas/Entidades/OfertaComboCalculador.java`, `src/ModuloVentas/Servicios/OfertaComboService.java` y `test/ModuloFinanzas/Entidades/OfertaComboCalculadorTest.java`. `OfertaComboCalculadorTest.repiteComboConCantidadesDecimalesYDejaSobrante`, con sus precios $40/$20 y componentes 0,500/1,250; `OfertaComboCalculador` normaliza cantidades a milésimas y evalúa repeticiones completas. Los límites de 2,490/2,500 se derivan manualmente de componentes exactos.

Comprobar UI y persistencia mediante lecturas acotadas por operación/contexto: bruto `vecTotal`, automático `vecOferta`, manual `vecOfertaManual` cuando corresponda, neto `venTotal`, identidad/leyenda del combo, un cobro y deltas declarados. El número de filas de pago no se deduce sin revisar el contrato del cobro simple. Selectores y oráculos para estas variantes permanecen pendientes de calibración; no usar coordenadas fijas. Registrar SHA256/build JAR, paquete, perfil y versión de datos. INFO resume, DEBUG muestra pasos y TRACE agrega diagnóstico saneado; un fallo informa paso, esperado, observado, categoría y evidencia, con causa no determinada si no está demostrada. No exponer filas completas, credenciales ni árboles privados.
<!-- END ORIGINAL OFFER DESIGN -->

</details>
