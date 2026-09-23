---
{"id":"XG-LPR-017","title":"Priorizar la lista elegida sobre una escala al cargar productos","product":"xgestion","module":"listas-precios","tags":["xgestion","regression","precios","listas-precios","listas-prioridad"],"status":"planned"}
---

# XG-LPR-017 — Priorizar la lista elegida sobre una escala al cargar productos

## Objetivo

Mantener el precio de la lista elegida al cargar o consolidar cantidades que también tienen escala global.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P1.** Etapa 2: condiciones comerciales; Restobar también depende de etapa 5. Sin Robot ni resultado aprobado. Ver [mapa de listas](../../docs/listas-precios.md).

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete autorizado, JAR/entorno identificados y baseline restaurable.
- Operación local, comprobante interno no fiscal, IVA 0 %, stock suficiente, sin impresión, pagos externos, ofertas ni descuentos adicionales salvo indicación expresa.
- Reutilizable del seed: QA-SEED-CANTIDAD; lista elegida 980101 fija $950; escala desde 5 a $800. Ejemplo LISTA-PRIORIDAD. Sin ofertas, cliente ni turno.
- Roles, datos adicionales, acceso por teclado/JAB y oráculos de lectura pendientes de preparar/verificar para esta ficha. Un ejemplo seed disponible no acredita esos requisitos.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Elegir 980101 antes de agregar productos. | Selector correcto; total cero. |
| 2 | Cargar 5 unidades. | Precio $950; total $4.750, no $4.000. |
| 3 | Agregar una unidad del mismo producto. | Cantidad 6; precio $950; total $5.700. |
| 4 | Cancelar/retomar cobro y confirmar $5.700. | Un cobro,6 unidades y lista 980101 en el detalle. |

## Variantes y dependencias

Regla verificada para carga/consolidación. Cambiar la lista después de cargar puede tomar otra prioridad en TicketVenta; no reutilizar este aprobado para esa ruta.

ORÁCULO PENDIENTE para igualar carga y cambio posterior: TicketVenta.java:3012-3018 consulta cantidad antes que lista general, a diferencia de FormVenta.java:2267-2281.

## Evidencia y límites

Registrar selector de lista, contexto, productos/cantidades, precio unitario, bruto, descuentos, neto y moneda antes/después. Comprobar por identidad lista de cabecera y renglones, documento y efectos de stock/cobro con lectura acotada; no volcar filas completas. Conservar implementación separada de validación real del JAR. INFO resume; DEBUG muestra pasos; TRACE añade diagnóstico saneado. Todo fallo conserva paso, esperado/observado y evidencia; causa no determinada si no está demostrada.

## Recuperación

Ante una discrepancia, detener la confirmación y conservar el informe privado. Cancelar diálogos y cerrar únicamente procesos propios del runner; una cuenta Restobar puede haber persistido cambios. Restaurar el baseline antes de repetir o cambiar perfil. No corregir precios con SQL durante una venta ni editar el esperado para que coincida con lo observado.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada en commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; estas referencias describen reglas/riesgos, no una ejecución E2E.

- `src/ModuloVentas/Vistas/FormVenta.java:2267-2281`.
- `src/ModuloProveedores/Entidades/ListaPrecioDetalle.java:1310-1327`.
- `src/ModuloProveedores/Entidades/ListaPrecioDetalle.java:1402-1433`.
- `src/ModuloVentas/Entidades/TicketVenta.java:2974-3045`.

Registrar SHA256/build del JAR, paquete, perfil, fecha/horario y responsable en evidencia local. Los nombres QA son públicos; credenciales, nombres privados y capturas de autenticación no se publican.

