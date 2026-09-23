---
{"id":"XG-PRM-047","title":"Agrupar por subfamilia: descuento de $150 por unidad entre productos","product":"xgestion","module":"promociones","tags":["xgestion","regression","promociones","promociones-agrupadas","ofertas-subfamilia","escritura"],"status":"implemented","test":"products/xgestion/suites/ofertas/agrupadas.robot","seed":"catalogo-comercial-v1"}
---

# XG-PRM-047 — Agrupar por subfamilia: descuento de $150 por unidad entre productos

## Objetivo

El vendedor combina artículos de una misma subfamilia, comprueba qué beneficio corresponde y corrige la venta sin conservar descuentos que ya no corresponden.

<!-- BEGIN GENERATED OFFER JOURNEY -->

## Recorrido de automatización

Estado del catálogo: **implemented**. Automatización catalogada en [`agrupadas.robot`](../../suites/ofertas/agrupadas.robot). Validación real: **pendiente**; requiere ejecutar el JAR exacto en el laboratorio calibrado.

Las tablas siguientes son los datos y pasos actuales del recorrido. Los importes son expectativas fijas, no resultados medidos. El diseño anterior queda al final como referencia histórica para conservar reglas, variantes y límites; sus estados y códigos no describen la implementación actual.

```powershell
.\qa.cmd run --product xgestion --scenario XG-PRM-047 --seed catalogo-comercial-v1 --log-level DEBUG
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
| A | `QA-PRM-047-V0-A` | $1.000,00 | unidad | 985700 / 985700 / 985700 | QA-PRM-047-V0-MARCA-A |
| B | `QA-PRM-047-V0-B` | $1.000,00 | unidad | 985700 / 985700 / 985700 | QA-PRM-047-V0-MARCA-B |
| E | `QA-PRM-047-V0-E` | $1.000,00 | unidad | 985700 / 985709 / 985700 | QA-PRM-047-V0-MARCA-A |

### Ofertas preparadas

| Oferta | Incluye | Regla | Agrupación | Estado / vigencia inclusiva | Medios habilitados |
| --- | --- | --- | --- | --- | --- |
| `QA-PRM-047-V0` | Subfamilia `985700` | $150,00 de descuento por unidad | ON | Activa; hoy -365 días a hoy +365 días | Todos |

Las fechas se refieren a la fecha local usada al preparar el seed; Windows y MySQL deben coincidir. No se modifica el reloj durante el recorrido.

### Pasos y resultados esperados

| Paso | Acción del usuario | Canasta completa después del paso | Resultado |
| ---: | --- | --- | --- |
| 1 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 2 | Cargar 1 u de `QA-PRM-047-V0-A` por código. | `QA-PRM-047-V0-A` × 1 u: precio $1.000,00; automático $150,00; manual $0,00; neto $850,00; lista aplicada: precio normal | Total **$850,00**. |
| 3 | Cargar 1 u de `QA-PRM-047-V0-E` por código. | `QA-PRM-047-V0-A` × 1 u: precio $1.000,00; automático $150,00; manual $0,00; neto $850,00; lista aplicada: precio normal<br>`QA-PRM-047-V0-E` × 1 u: precio $1.000,00; automático $0,00; manual $0,00; neto $1.000,00; lista aplicada: precio normal | Total **$1.850,00**. |
| 4 | Seleccionar `QA-PRM-047-V0-E`, abrir Ctrl+E y elegir Eliminar. | `QA-PRM-047-V0-A` × 1 u: precio $1.000,00; automático $150,00; manual $0,00; neto $850,00; lista aplicada: precio normal | Total **$850,00**. |
| 5 | Cargar 1 u de `QA-PRM-047-V0-B` por código. | `QA-PRM-047-V0-A` × 1 u: precio $1.000,00; automático $150,00; manual $0,00; neto $850,00; lista aplicada: precio normal<br>`QA-PRM-047-V0-B` × 1 u: precio $1.000,00; automático $150,00; manual $0,00; neto $850,00; lista aplicada: precio normal | Total **$1.700,00**. |
| 6 | Seleccionar `QA-PRM-047-V0-A`, abrir Ctrl+E, dejar 2 u y guardar. | `QA-PRM-047-V0-A` × 2 u: precio $1.000,00; automático $300,00; manual $0,00; neto $1.700,00; lista aplicada: precio normal<br>`QA-PRM-047-V0-B` × 1 u: precio $1.000,00; automático $150,00; manual $0,00; neto $850,00; lista aplicada: precio normal | Total **$2.550,00**. |
| 7 | Seleccionar `QA-PRM-047-V0-B`, abrir Ctrl+E y elegir Eliminar. | `QA-PRM-047-V0-A` × 2 u: precio $1.000,00; automático $300,00; manual $0,00; neto $1.700,00; lista aplicada: precio normal | Total **$1.700,00**. |
| 8 | Seleccionar `QA-PRM-047-V0-A`, abrir Ctrl+E, dejar 1 u y guardar. | `QA-PRM-047-V0-A` × 1 u: precio $1.000,00; automático $150,00; manual $0,00; neto $850,00; lista aplicada: precio normal | Total **$850,00**. |
| 9 | Abandonar la venta y confirmar la salida sin cobrar. | Sin renglones en la operación. | Sin venta cobrada, pago ni cambios de stock o destino de cobro. |
| 10 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 11 | Cargar 1 u de `QA-PRM-047-V0-A` por código. | `QA-PRM-047-V0-A` × 1 u: precio $1.000,00; automático $150,00; manual $0,00; neto $850,00; lista aplicada: precio normal | Total **$850,00**. |
| 12 | Cargar 1 u de `QA-PRM-047-V0-B` por código. | `QA-PRM-047-V0-A` × 1 u: precio $1.000,00; automático $150,00; manual $0,00; neto $850,00; lista aplicada: precio normal<br>`QA-PRM-047-V0-B` × 1 u: precio $1.000,00; automático $150,00; manual $0,00; neto $850,00; lista aplicada: precio normal | Total **$1.700,00**. |
| 13 | Abrir cobro en efectivo del perfil QA, ingresar $1.700,00 y cancelar antes de confirmar. | `QA-PRM-047-V0-A` × 1 u: precio $1.000,00; automático $150,00; manual $0,00; neto $850,00; lista aplicada: precio normal<br>`QA-PRM-047-V0-B` × 1 u: precio $1.000,00; automático $150,00; manual $0,00; neto $850,00; lista aplicada: precio normal | Total **$1.700,00**. Conserva toda la canasta; sin venta cobrada, pago ni movimientos. |
| 14 | Retomar el cobro en efectivo del perfil QA, ingresar $1.700,00 y confirmar una sola vez. | `QA-PRM-047-V0-A` × 1 u: precio $1.000,00; automático $150,00; manual $0,00; neto $850,00; lista aplicada: precio normal<br>`QA-PRM-047-V0-B` × 1 u: precio $1.000,00; automático $150,00; manual $0,00; neto $850,00; lista aplicada: precio normal | Total **$1.700,00**. Una venta y un cobro en efectivo del perfil QA; vuelto cero. Stock: `QA-PRM-047-V0-A` −1 u; `QA-PRM-047-V0-B` −1 u. |

## Variante 2: agrupacion-off

### Productos preparados

| Referencia | Código | Precio base | Unidad | Familia / subfamilia / sector | Marca |
| --- | --- | ---: | --- | --- | --- |
| A | `QA-PRM-047-V1-A` | $1.000,00 | unidad | 985710 / 985710 / 985710 | QA-PRM-047-V1-MARCA-A |
| B | `QA-PRM-047-V1-B` | $1.000,00 | unidad | 985710 / 985710 / 985710 | QA-PRM-047-V1-MARCA-B |
| E | `QA-PRM-047-V1-E` | $1.000,00 | unidad | 985710 / 985719 / 985710 | QA-PRM-047-V1-MARCA-A |

### Ofertas preparadas

| Oferta | Incluye | Regla | Agrupación | Estado / vigencia inclusiva | Medios habilitados |
| --- | --- | --- | --- | --- | --- |
| `QA-PRM-047-V1` | Subfamilia `985710` | $150,00 de descuento por unidad | OFF | Activa; hoy -365 días a hoy +365 días | Todos |

Las fechas se refieren a la fecha local usada al preparar el seed; Windows y MySQL deben coincidir. No se modifica el reloj durante el recorrido.

### Pasos y resultados esperados

| Paso | Acción del usuario | Canasta completa después del paso | Resultado |
| ---: | --- | --- | --- |
| 1 | Abrir una venta nueva y comprobar el contexto QA. | Sin renglones en la operación. | Total **$0,00**. ARS; precio normal y efectivo del perfil QA. |
| 2 | Cargar 1 u de `QA-PRM-047-V1-A` por código. | `QA-PRM-047-V1-A` × 1 u: precio $1.000,00; automático $150,00; manual $0,00; neto $850,00; lista aplicada: precio normal | Total **$850,00**. |
| 3 | Cargar 1 u de `QA-PRM-047-V1-B` por código. | `QA-PRM-047-V1-A` × 1 u: precio $1.000,00; automático $150,00; manual $0,00; neto $850,00; lista aplicada: precio normal<br>`QA-PRM-047-V1-B` × 1 u: precio $1.000,00; automático $150,00; manual $0,00; neto $850,00; lista aplicada: precio normal | Total **$1.700,00**. |
| 4 | Seleccionar `QA-PRM-047-V1-A`, abrir Ctrl+E, dejar 2 u y guardar. | `QA-PRM-047-V1-A` × 2 u: precio $1.000,00; automático $300,00; manual $0,00; neto $1.700,00; lista aplicada: precio normal<br>`QA-PRM-047-V1-B` × 1 u: precio $1.000,00; automático $150,00; manual $0,00; neto $850,00; lista aplicada: precio normal | Total **$2.550,00**. |
| 5 | Abandonar la venta y confirmar la salida sin cobrar. | Sin renglones en la operación. | Sin venta cobrada, pago ni cambios de stock o destino de cobro. |

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

**Pendiente de automatizar (`planned`), prioridad P1, etapa 2.** No hay test Robot asociado ni validación real del JAR. Fórmula `$`: descuento de $150 por cada unidad incluida, sin mínimo. Consultar el [índice de pendientes](../../docs/promociones-pendientes.md). Agrupación de productos distintos solo se contempla para familia, subfamilia y marca.

## Precondiciones y datos

- Windows QA exclusivo y offline; paquete autorizado, baseline restaurable y JAR identificado. Usuario vendedor con permiso de carga/edición/cobro y abandono sin supervisor. Empresa, sucursal y puesto propios, stock suficiente.
- ARS, precio base $1.000,00 por unidad para A, B y Ajeno; unidades enteras, IVA 0 %, sin otros impuestos. Comprobante interno 99, efectivo exacto, diálogo de cobro habilitado, sin impresión ni fiscalización.
- Lista **Ninguna Lista** (ID 0); cliente/turno sin lista automática, otros descuentos/recargos en cero y fidelización deshabilitada. Oferta activa y vigente para la sucursal QA y todos los medios de pago. No hay combos ni ofertas superpuestas.
- **NUEVO PENDIENTE DE PREPARAR:** perfil QA-XG-PRM-047, productos A y B exclusivos de una misma subfamilia, un producto Ajeno de otra subfamilia y la oferta indicada. Son nombres funcionales propuestos, sin IDs asignados ni filas disponibles en el seed actual. Preparar dos copias del perfil: agrupación activada y desactivada, con idénticos datos y una sola regla comercial.
- A y B pertenecen a la misma subfamilia. Ajeno debe pertenecer a otra subfamilia de la misma familia, para demostrar que la coincidencia de familia no basta.
- La agrupación se cambia en la preparación de cada perfil independiente, nunca mientras una venta está abierta ni mediante una escritura para forzar el esperado. Requiere preparación/calibración de perfiles y controles accesibles; aún pendientes. Los datos propuestos no se aplican en esta entrega.

## Pasos y resultados esperados

1. Abrir una venta vacía con agrupación **activada** y cargar A ×1. **Esperado:** bruto $1.000,00, descuento $150,00, neto $850,00.

2. Agregar Ajeno ×1, conservando A ×1. **Esperado:** bruto $2.000,00, descuento $150,00, neto $1.850,00. Ajeno conserva neto $1.000,00 y no participa en el beneficio ni en su mínimo.

3. Quitar Ajeno y agregar B ×1. **Esperado:** dos productos distintos incluidos, bruto $2.000,00, descuento $300,00, neto $1.700,00. Cada unidad tiene la misma regla; activar agrupación no duplica el descuento.

4. Editar A de ×1 a ×2. **Esperado:** A ×2 + B ×1, bruto $3.000,00, descuento $450,00, neto $2.550,00. Quitar B. **Esperado:** A ×2, bruto $2.000,00, descuento $300,00, neto $1.700,00.

5. Reducir A a ×1. **Esperado:** bruto $1.000,00, descuento $150,00, neto $850,00; no conserva un descuento de la cantidad anterior. Abandonar y confirmar. **Esperado:** no queda una venta cobrada ni movimientos de stock/caja.

6. En una ejecución independiente restaurada, usar la copia con agrupación **desactivada**. Cargar A ×1 + B ×1. **Esperado:** bruto $2.000,00, descuento $300,00, neto $1.700,00. Cambiar A a ×2. **Esperado:** bruto $3.000,00, descuento $450,00, neto $2.550,00. El total coincide con la variante agrupada porque esta fórmula no tiene mínimo; la igualdad es el resultado correcto, no una prueba de que el interruptor carezca de efecto en las demás fórmulas. Abandonar sin efectos.

7. Restaurar el perfil agrupado inicial y cargar A ×1 + B ×1. Abrir y cancelar el cobro. **Esperado:** se conserva neto $1.700,00 y no se registra venta cobrada ni cambios en stock/caja. Retomar el cobro y confirmar una sola vez $1.700,00 en efectivo. **Esperado:** una venta y un cobro por ese importe, caja +$1.700,00, stock A −1 y B −1; Ajeno sin cambios.

## Evidencia y límites

Guardar identidad visible de los artículos, condición de agrupación del perfil, cantidades y bruto/oferta/neto en cada transición, incluyendo Ajeno, cancelación y cobro final. Los importes anteriores son expectativas calculadas manualmente desde la regla, no resultados de ejecución. Verificar la suma del descuento y del neto de las filas contra el total; una etiqueta porcentual aislada no prueba el importe. Esta ficha no cubre fracciones, listas, otros medios de pago, cruces de ofertas ni Restobar.

## Recuperación

Cancelar el cobro debe volver al mismo contenido e importe. Abandonar las variantes previas no debe producir una venta cobrada ni movimientos de stock/caja. Conservar evidencia privada ante un fallo antes de restaurar el perfil; no borrar ni corregir operaciones en la base. La siguiente variante comienza desde su baseline controlado y no reutiliza la venta anterior.

## Anexo técnico y trazabilidad

Fuente ERP verificada: commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; `src/ModuloFinanzas/Entidades/OfertaAplicacionCalculador.java`, `test/ModuloFinanzas/Entidades/OfertaAplicacionCalculadorAgrupacionTest.java` (siete tipos por familia/subfamilia/marca y agrupación desactivada), `test/ModuloFinanzas/Entidades/OfertaPrecioTest.java`. La configuración agrupada está en `Configuracion.agrupada`; no habilitarla por sector o para combinar productos ajenos.

Selectores para edición por teclado, eliminación y comprobación de oferta pendientes de verificar en el JAR recibido. Contrastar operación e identidad con lecturas acotadas: `vecTotal` bruto, `vecOferta` descuento automático, `venTotal` neto; sin descuentos adicionales, un cobro final y deltas de stock/caja declarados. No imprimir filas completas ni datos privados. Registrar SHA256/build del JAR, paquete, perfil, versión de datos y fecha. INFO resume, DEBUG muestra pasos y TRACE diagnóstico saneado. Un fallo siempre informa paso, esperado, observado, categoría y evidencia; causa no determinada si no está demostrada.
<!-- END ORIGINAL OFFER DESIGN -->

</details>
