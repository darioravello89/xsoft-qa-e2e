---
{"id":"XG-LPR-019","title":"Cobrar un precio ARS de lista sin promociones","product":"xgestion","module":"listas-precios","tags":["xgestion","regression","precios","listas-precios","listas-prioridad"],"status":"planned"}
---

# XG-LPR-019 — Cobrar un precio ARS de lista sin promociones

## Objetivo

Comprobar el precio de lista en pesos como importe del producto, separado del descuento por ofertas.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P1.** Etapa 2: condiciones comerciales; Restobar también depende de etapa 5. Sin Robot ni resultado aprobado. Ver [mapa de listas](../../docs/listas-precios.md).

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete autorizado, JAR/entorno identificados y baseline restaurable.
- Operación local, comprobante interno no fiscal, IVA 0 %, stock suficiente, sin impresión, pagos externos, ofertas ni descuentos adicionales salvo indicación expresa.
- Reutilizable del seed: QA-SEED-LISTAS, lista ARS 980101 a $750; ejemplo LISTA-ARS. Sin cliente/turno, ofertas ni descuentos; moneda contable ARS.
- Roles, datos adicionales, acceso por teclado/JAB y oráculos de lectura pendientes de preparar/verificar para esta ficha. Un ejemplo seed disponible no acredita esos requisitos.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Elegir 980101 y cargar una unidad. | Precio y total $750 ARS; descuento $0. |
| 2 | Agregar segunda unidad. | Cantidad 2; bruto/neto $1.500 y descuento $0. |
| 3 | Cancelar cobro y retomarlo. | Conserva $1.500 y moneda ARS. |
| 4 | Cobrar $1.500 exactos y consultar comprobante interno. | Una venta/cobro, dos unidades; precio y lista persistidos correctos. |

## Variantes y dependencias

PRM-071 combina lista y oferta 10%. Esta ficha cubre LISTA-ARS sin oferta para aislar precio/moneda/persistencia; no acredita otra vez el cruce promocional.

## Evidencia y límites

Registrar selector de lista, contexto, productos/cantidades, precio unitario, bruto, descuentos, neto y moneda antes/después. Comprobar por identidad lista de cabecera y renglones, documento y efectos de stock/cobro con lectura acotada; no volcar filas completas. Conservar implementación separada de validación real del JAR. INFO resume; DEBUG muestra pasos; TRACE añade diagnóstico saneado. Todo fallo conserva paso, esperado/observado y evidencia; causa no determinada si no está demostrada.

## Recuperación

Ante una discrepancia, detener la confirmación y conservar el informe privado. Cancelar diálogos y cerrar únicamente procesos propios del runner; una cuenta Restobar puede haber persistido cambios. Restaurar el baseline antes de repetir o cambiar perfil. No corregir precios con SQL durante una venta ni editar el esperado para que coincida con lo observado.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada en commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; estas referencias describen reglas/riesgos, no una ejecución E2E.

- `src/ModuloProveedores/Entidades/ListaPrecioDetalle.java:1310-1327`.
- `src/ModuloVentas/Entidades/TicketVenta.java:2974-3045`.

Registrar SHA256/build del JAR, paquete, perfil, fecha/horario y responsable en evidencia local. Los nombres QA son públicos; credenciales, nombres privados y capturas de autenticación no se publican.

