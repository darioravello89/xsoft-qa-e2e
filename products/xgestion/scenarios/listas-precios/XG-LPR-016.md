---
{"id":"XG-LPR-016","title":"Aplicar escalas de precio al alcanzar cantidades mínimas","product":"xgestion","module":"listas-precios","tags":["xgestion","regression","precios","listas-precios","listas-prioridad"],"status":"planned"}
---

# XG-LPR-016 — Aplicar escalas de precio al alcanzar cantidades mínimas

## Objetivo

Cobrar el precio unitario de la cantidad comprada sin anticipar sus mínimos.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P1.** Etapa 2: condiciones comerciales; Restobar también depende de etapa 5. Sin Robot ni resultado aprobado. Ver [mapa de listas](../../docs/listas-precios.md).

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete autorizado, JAR/entorno identificados y baseline restaurable.
- Operación local, comprobante interno no fiscal, IVA 0 %, stock suficiente, sin impresión, pagos externos, ofertas ni descuentos adicionales salvo indicación expresa.
- Reutilizable del seed: QA-SEED-CANTIDAD normal=$1.000; desde 2 unidades $900; desde 5 unidades $800. Ninguna lista elegida, sin cliente/turno ni ofertas. Perfil y calibración pendientes; sin nuevo seed en esta entrega.
- Roles, datos adicionales, acceso por teclado/JAB y oráculos de lectura pendientes de preparar/verificar para esta ficha. Un ejemplo seed disponible no acredita esos requisitos.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Abrir ventas independientes y cargar en una sola acción 1, 2 o 3 unidades. | Totales $1.000, $1.800 y $2.700; precios unitarios $1.000, $900 y $900, respectivamente. |
| 2 | Repetir en ventas independientes con una carga de 4, 5 o 6 unidades. | Totales $3.600, $4.000 y $4.800; precios unitarios $900, $800 y $800, respectivamente. |
| 3 | Preparar la variante de agregar unidades en cargas sucesivas para cruzar los mínimos de 2 y 5. | **Oráculo pendiente:** acordar antes de ejecutar el reparto entre renglones y su precio. La consolidación rechaza precios efectivos diferentes; no se puede trasladar a esta variante el total esperado de una carga única. Sin ese acuerdo, bloquear la variante y no aprobarla por observación. |
| 4 | Cancelar cobro y abandonar. | Sin cobros ni movimientos por pruebas canceladas. |

## Variantes y dependencias

Cubre los ejemplos CANTIDAD-Q1/Q2/Q5 mediante una carga directa en una venta vacía. Agregar unidades atravesando una escala y reducir por editor de 5 a 2 y luego a 1 requieren oráculos separados: verificar la ruta de recálculo, el precio y las cantidades de cada renglón. Estas variantes permanecen pendientes hasta acordar sus resultados; una carga directa correcta no las acredita.

Mínimos empatados entre dos listas globales no tienen desempate completo en la consulta. Acordar oráculo antes de preparar esa variante.

## Evidencia y límites

Registrar selector de lista, contexto, productos/cantidades, precio unitario, bruto, descuentos, neto y moneda antes/después. Comprobar por identidad lista de cabecera y renglones, documento y efectos de stock/cobro con lectura acotada; no volcar filas completas. Conservar implementación separada de validación real del JAR. INFO resume; DEBUG muestra pasos; TRACE añade diagnóstico saneado. Todo fallo conserva paso, esperado/observado y evidencia; causa no determinada si no está demostrada.

## Recuperación

Ante una discrepancia, detener la confirmación y conservar el informe privado. Cancelar diálogos y cerrar únicamente procesos propios del runner; una cuenta Restobar puede haber persistido cambios. Restaurar el baseline antes de repetir o cambiar perfil. No corregir precios con SQL durante una venta ni editar el esperado para que coincida con lo observado.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada en commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; estas referencias describen reglas/riesgos, no una ejecución E2E.

- `src/ModuloProveedores/Entidades/ListaPrecioDetalle.java:1402-1433`.
- `src/ModuloVentas/Vistas/FormVenta.java:2267-2281`.
- `src/ModuloVentas/Vistas/FormVenta.java:2298-2302`: la consolidación exige el mismo precio efectivo.
- `src/ModuloVentas/Vistas/PrecioBultoVentaPolicy.java:33-39`: compara los precios con seis decimales.
- `src/ModuloProveedores/Entidades/ListaPrecioDetalle.java:1310-1327`.

Registrar SHA256/build del JAR, paquete, perfil, fecha/horario y responsable en evidencia local. Los nombres QA son públicos; credenciales, nombres privados y capturas de autenticación no se publican.
