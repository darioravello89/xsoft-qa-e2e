---
{"id":"XG-LPR-001","title":"Abrir una venta con la lista de su sucursal","product":"xgestion","module":"listas-precios","tags":["xgestion","regression","precios","listas-precios","listas-sucursal","listas-prioridad"],"status":"planned"}
---

# XG-LPR-001 — Abrir una venta con la lista de su sucursal

## Objetivo

Comenzar a vender con el precio de la sucursal sin elegir una lista en cada operación.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P1.** Etapa 2: condiciones comerciales; Restobar también depende de etapa 5. Sin Robot ni resultado aprobado. Ver [mapa de listas](../../docs/listas-precios.md).

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete autorizado, JAR/entorno identificados y baseline restaurable.
- Operación local, comprobante interno no fiscal, IVA 0 %, stock suficiente, sin impresión, pagos externos, ofertas ni descuentos adicionales salvo indicación expresa.
- Fixture NUEVO PENDIENTE DE PREPARAR: S1 con exactamente una lista activa QA-LPR-S1; A a $900 frente a precio normal $1.000. Cliente sin lista; ningún turno aplicable; configuración fija ausente o -1.
- Roles, datos adicionales, acceso por teclado/JAB y oráculos de lectura pendientes de preparar/verificar para esta ficha. Un ejemplo seed disponible no acredita esos requisitos.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Abrir una venta nueva en S1. | Selector QA-LPR-S1; operación vacía y total $0. |
| 2 | Cargar dos unidades de A. | Precio unitario $900; cantidad 2; total $1.800, sin descuento. |
| 3 | Cancelar el diálogo de cobro y volver a la venta. | Conserva lista, cantidad y $1.800; no se cobra. |
| 4 | Abandonar y abrir otra venta. | Vuelve a elegirse QA-LPR-S1; A × 1 cuesta $900. |

## Variantes y dependencias

Repetir con clave fija ausente y con -1. Si S1 tiene dos listas activas, el orden por defecto no está definido: esa variante requiere oráculo acordado; no elegir como esperado el precio que apareció.

## Evidencia y límites

Registrar selector de lista, contexto, productos/cantidades, precio unitario, bruto, descuentos, neto y moneda antes/después. Comprobar por identidad lista de cabecera y renglones, documento y efectos de stock/cobro con lectura acotada; no volcar filas completas. Conservar implementación separada de validación real del JAR. INFO resume; DEBUG muestra pasos; TRACE añade diagnóstico saneado. Todo fallo conserva paso, esperado/observado y evidencia; causa no determinada si no está demostrada.

## Recuperación

Ante una discrepancia, detener la confirmación y conservar el informe privado. Cancelar diálogos y cerrar únicamente procesos propios del runner; una cuenta Restobar puede haber persistido cambios. Restaurar el baseline antes de repetir o cambiar perfil. No corregir precios con SQL durante una venta ni editar el esperado para que coincida con lo observado.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada en commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; estas referencias describen reglas/riesgos, no una ejecución E2E.

- `src/ModuloVentas/Vistas/FormVenta.java:3413-3491`.
- `src/ModuloVentas/Servicios/VentaListaPrecioPrioridadPolicy.java:37-74`.
- `src/ModuloProveedores/Entidades/ListaPrecio.java:240-287`.

Registrar SHA256/build del JAR, paquete, perfil, fecha/horario y responsable en evidencia local. Los nombres QA son públicos; credenciales, nombres privados y capturas de autenticación no se publican.

