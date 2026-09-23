---
{"id":"XG-LPR-024","title":"Distinguir fechas de auditoría de la vigencia de una lista","product":"xgestion","module":"listas-precios","tags":["xgestion","regression","precios","listas-precios","listas-prioridad"],"status":"planned"}
---

# XG-LPR-024 — Distinguir fechas de auditoría de la vigencia de una lista

## Objetivo

Evitar confundir una lista antigua pero activa con una promoción vencida y comprobar el comportamiento en días diferentes.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P1.** Etapa 2: condiciones comerciales; Restobar también depende de etapa 5. Sin Robot ni resultado aprobado. Ver [mapa de listas](../../docs/listas-precios.md).

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete autorizado, JAR/entorno identificados y baseline restaurable.
- Operación local, comprobante interno no fiscal, IVA 0 %, stock suficiente, sin impresión, pagos externos, ofertas ni descuentos adicionales salvo indicación expresa.
- Fixture NUEVO PENDIENTE: L activa A=$750 con alta/actualización 2020; sin ofertas. T=08:00–15:00 usa L; dos días de semana diferentes a las 10:00; base S=$900, fija=-1.
- Roles, datos adicionales, acceso por teclado/JAB y oráculos de lectura pendientes de preparar/verificar para esta ficha. Un ejemplo seed disponible no acredita esos requisitos.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Abrir venta dentro del horario el primer día. | L; A × 1=$750 aunque su fecha de auditoría sea antigua. |
| 2 | Repetir otro día a igual hora sin cambiar lista/turno. | Mismo $750: la consulta horaria revisada usa inicio/fin comunes. |
| 3 | Restaurar variante con cabecera L inactiva. | Resuelve S; A × 1=$900. |
| 4 | Cancelar los controles. | Sin cobros ni cambios en fechas del catálogo. |

## Variantes y dependencias

La consulta no define desde/hasta para listas y no usa campos horarios por día de semana. Si negocio requiere calendario semanal o vencimiento, ORÁCULO PENDIENTE: acordarlo antes de automatizarlo.

Preparar cada instante antes del JAR; no cambiar fecha del host ni atribuir a la auditoría una vigencia que no define.

## Evidencia y límites

Registrar selector de lista, contexto, productos/cantidades, precio unitario, bruto, descuentos, neto y moneda antes/después. Comprobar por identidad lista de cabecera y renglones, documento y efectos de stock/cobro con lectura acotada; no volcar filas completas. Conservar implementación separada de validación real del JAR. INFO resume; DEBUG muestra pasos; TRACE añade diagnóstico saneado. Todo fallo conserva paso, esperado/observado y evidencia; causa no determinada si no está demostrada.

## Recuperación

Ante una discrepancia, detener la confirmación y conservar el informe privado. Cancelar diálogos y cerrar únicamente procesos propios del runner; una cuenta Restobar puede haber persistido cambios. Restaurar el baseline antes de repetir o cambiar perfil. No corregir precios con SQL durante una venta ni editar el esperado para que coincida con lo observado.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada en commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; estas referencias describen reglas/riesgos, no una ejecución E2E.

- `src/ModuloProveedores/Entidades/ListaPrecio.java:240-287`.
- `src/ModuloConfiguracion/Entidades/Turno.java:207-237`.
- `src/ModuloVentas/Vistas/FormVenta.java:3413-3491`.

Registrar SHA256/build del JAR, paquete, perfil, fecha/horario y responsable en evidencia local. Los nombres QA son públicos; credenciales, nombres privados y capturas de autenticación no se publican.

