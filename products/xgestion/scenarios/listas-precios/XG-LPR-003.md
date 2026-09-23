---
{"id":"XG-LPR-003","title":"Elegir una lista fija por empresa sobre el default de sucursal","product":"xgestion","module":"listas-precios","tags":["xgestion","regression","precios","listas-precios","listas-sucursal","listas-prioridad"],"status":"planned"}
---

# XG-LPR-003 — Elegir una lista fija por empresa sobre el default de sucursal

## Objetivo

Usar la lista configurada para la empresa aun cuando la sucursal tenga otra base.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P1.** Etapa 2: condiciones comerciales; Restobar también depende de etapa 5. Sin Robot ni resultado aprobado. Ver [mapa de listas](../../docs/listas-precios.md).

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete autorizado, JAR/entorno identificados y baseline restaurable.
- Operación local, comprobante interno no fiscal, IVA 0 %, stock suficiente, sin impresión, pagos externos, ofertas ni descuentos adicionales salvo indicación expresa.
- Fixture NUEVO PENDIENTE: S1 A=$900; fija global F1 A=$800; fija de empresa F2 A=$700; ambas listas activas y accesibles. Sin lista de cliente ni turno.
- Roles, datos adicionales, acceso por teclado/JAB y oráculos de lectura pendientes de preparar/verificar para esta ficha. Un ejemplo seed disponible no acredita esos requisitos.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Abrir venta con configuración global F1 y sin clave de empresa. | Selector F1; A × 2=$1.600. |
| 2 | Reiniciar desde perfil con clave de empresa F2. | Selector F2; A × 2=$1.400. |
| 3 | Cancelar cobro y volver a la venta. | Mantiene el precio del perfil y no produce cobros. |
| 4 | Restaurar perfil base de sucursal y abrir venta. | Selector S1; A × 2=$1.800, sin residuos de F2. |

## Variantes y dependencias

Clave de empresa presente prevalece sobre la global. Clave vacía/no numérica usa el fallback del parser (-1); validar diagnóstico saneado sin publicar configuración completa.

## Evidencia y límites

Registrar selector de lista, contexto, productos/cantidades, precio unitario, bruto, descuentos, neto y moneda antes/después. Comprobar por identidad lista de cabecera y renglones, documento y efectos de stock/cobro con lectura acotada; no volcar filas completas. Conservar implementación separada de validación real del JAR. INFO resume; DEBUG muestra pasos; TRACE añade diagnóstico saneado. Todo fallo conserva paso, esperado/observado y evidencia; causa no determinada si no está demostrada.

## Recuperación

Ante una discrepancia, detener la confirmación y conservar el informe privado. Cancelar diálogos y cerrar únicamente procesos propios del runner; una cuenta Restobar puede haber persistido cambios. Restaurar el baseline antes de repetir o cambiar perfil. No corregir precios con SQL durante una venta ni editar el esperado para que coincida con lo observado.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada en commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; estas referencias describen reglas/riesgos, no una ejecución E2E.

- `src/ModuloPrincipal/Entidades/Config.java:89 y 421-435`.
- `src/ModuloVentas/Servicios/VentaListaPrecioPrioridadPolicy.java:37-74`.
- `src/ModuloVentas/Vistas/FormVenta.java:3413-3491`.

Registrar SHA256/build del JAR, paquete, perfil, fecha/horario y responsable en evidencia local. Los nombres QA son públicos; credenciales, nombres privados y capturas de autenticación no se publican.

