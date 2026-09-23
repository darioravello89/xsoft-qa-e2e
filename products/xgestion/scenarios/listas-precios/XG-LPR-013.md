---
{"id":"XG-LPR-013","title":"Distinguir una lista fija inexistente de volver al default de sucursal","product":"xgestion","module":"listas-precios","tags":["xgestion","regression","precios","listas-precios","listas-prioridad","listas-sucursal"],"status":"planned"}
---

# XG-LPR-013 — Distinguir una lista fija inexistente de volver al default de sucursal

## Objetivo

Identificar un dato fijo inválido sin aplicar silenciosamente otra base comercial.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P1.** Etapa 2: condiciones comerciales; Restobar también depende de etapa 5. Sin Robot ni resultado aprobado. Ver [mapa de listas](../../docs/listas-precios.md).

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete autorizado, JAR/entorno identificados y baseline restaurable.
- Operación local, comprobante interno no fiscal, IVA 0 %, stock suficiente, sin impresión, pagos externos, ofertas ni descuentos adicionales salvo indicación expresa.
- Fixture NUEVO PENDIENTE: S A=$900, normal A=$1.000; sin cliente/turno. Perfiles: fija positiva inexistente, cabecera inactiva o lista exclusiva de otra sucursal.
- Roles, datos adicionales, acceso por teclado/JAB y oráculos de lectura pendientes de preparar/verificar para esta ficha. Un ejemplo seed disponible no acredita esos requisitos.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Abrir venta con cada perfil restaurado. | Ninguna; no sustituye la fija inválida por S. |
| 2 | Cargar A × 2. | Precio normal $1.000; total $2.000. |
| 3 | Restaurar fija=-1 y repetir. | S; A × 2=$1.800: el fallback explícito sí funciona. |
| 4 | Cancelar los controles y conservar diagnóstico. | Origen fijo inválido identificado sin exponer configuración completa. |

## Variantes y dependencias

Valor mal formado, vacío o menor que -1 es una variante diferente: se normaliza al fallback -1, por lo que se espera S=$900. No confundir ID positivo inválido con sintaxis inválida.

## Evidencia y límites

Registrar selector de lista, contexto, productos/cantidades, precio unitario, bruto, descuentos, neto y moneda antes/después. Comprobar por identidad lista de cabecera y renglones, documento y efectos de stock/cobro con lectura acotada; no volcar filas completas. Conservar implementación separada de validación real del JAR. INFO resume; DEBUG muestra pasos; TRACE añade diagnóstico saneado. Todo fallo conserva paso, esperado/observado y evidencia; causa no determinada si no está demostrada.

## Recuperación

Ante una discrepancia, detener la confirmación y conservar el informe privado. Cancelar diálogos y cerrar únicamente procesos propios del runner; una cuenta Restobar puede haber persistido cambios. Restaurar el baseline antes de repetir o cambiar perfil. No corregir precios con SQL durante una venta ni editar el esperado para que coincida con lo observado.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada en commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; estas referencias describen reglas/riesgos, no una ejecución E2E.

- `src/ModuloVentas/Servicios/VentaListaPrecioPrioridadPolicy.java:37-74`.
- `src/ModuloVentas/Vistas/FormVenta.java:3413-3491`.
- `src/ModuloPrincipal/Entidades/Config.java:89 y 421-435`.
- `src/ModuloProveedores/Entidades/ListaPrecio.java:240-287`.

Registrar SHA256/build del JAR, paquete, perfil, fecha/horario y responsable en evidencia local. Los nombres QA son públicos; credenciales, nombres privados y capturas de autenticación no se publican.

