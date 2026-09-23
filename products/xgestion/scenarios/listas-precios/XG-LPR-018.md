---
{"id":"XG-LPR-018","title":"Usar la escala cuando la lista elegida no contiene el producto","product":"xgestion","module":"listas-precios","tags":["xgestion","regression","precios","listas-precios","listas-prioridad"],"status":"planned"}
---

# XG-LPR-018 — Usar la escala cuando la lista elegida no contiene el producto

## Objetivo

Cobrar un artículo sin entrada en la lista elegida pero con un precio por cantidad válido.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P1.** Etapa 2: condiciones comerciales; Restobar también depende de etapa 5. Sin Robot ni resultado aprobado. Ver [mapa de listas](../../docs/listas-precios.md).

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete autorizado, JAR/entorno identificados y baseline restaurable.
- Operación local, comprobante interno no fiscal, IVA 0 %, stock suficiente, sin impresión, pagos externos, ofertas ni descuentos adicionales salvo indicación expresa.
- Fixture NUEVO PENDIENTE: L-SIN-A activa contiene solo B a $1.500; A normal=$1.000 y escala q>=2 a $900. Puede reutilizar QA-SEED-CANTIDAD, pero L-SIN-A aún debe prepararse. Sin ofertas.
- Roles, datos adicionales, acceso por teclado/JAB y oráculos de lectura pendientes de preparar/verificar para esta ficha. Un ejemplo seed disponible no acredita esos requisitos.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Elegir L-SIN-A y cargar A × 1. | Sin entrada ni mínimo aplicable: total $1.000. |
| 2 | En otra venta elegir L-SIN-A y cargar A × 2. | Escala $900; total $1.800; identidad de lista del renglón corresponde a la escala. |
| 3 | Agregar B × 1. | B usa $1.500; total A2+B1=$3.300. |
| 4 | Cancelar cobro y abandonar. | Conserva canasta hasta abandonar; no crea cobro. |

## Variantes y dependencias

A diferencia de PRM-072, el fallback es una escala por cantidad y no precio normal. Mantener cabecera activa; no simular detalle ausente desactivando la lista.

## Evidencia y límites

Registrar selector de lista, contexto, productos/cantidades, precio unitario, bruto, descuentos, neto y moneda antes/después. Comprobar por identidad lista de cabecera y renglones, documento y efectos de stock/cobro con lectura acotada; no volcar filas completas. Conservar implementación separada de validación real del JAR. INFO resume; DEBUG muestra pasos; TRACE añade diagnóstico saneado. Todo fallo conserva paso, esperado/observado y evidencia; causa no determinada si no está demostrada.

## Recuperación

Ante una discrepancia, detener la confirmación y conservar el informe privado. Cancelar diálogos y cerrar únicamente procesos propios del runner; una cuenta Restobar puede haber persistido cambios. Restaurar el baseline antes de repetir o cambiar perfil. No corregir precios con SQL durante una venta ni editar el esperado para que coincida con lo observado.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada en commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; estas referencias describen reglas/riesgos, no una ejecución E2E.

- `src/ModuloVentas/Vistas/FormVenta.java:2267-2281`.
- `src/ModuloProveedores/Entidades/ListaPrecioDetalle.java:1402-1433`.
- `src/ModuloProveedores/Entidades/ListaPrecioDetalle.java:1310-1327`.

Registrar SHA256/build del JAR, paquete, perfil, fecha/horario y responsable en evidencia local. Los nombres QA son públicos; credenciales, nombres privados y capturas de autenticación no se publican.

