---
{"id":"XG-LPR-009","title":"Respetar los minutos de inicio y fin de un precio diurno","product":"xgestion","module":"listas-precios","tags":["xgestion","regression","precios","listas-precios","listas-horario"],"status":"planned"}
---

# XG-LPR-009 — Respetar los minutos de inicio y fin de un precio diurno

## Objetivo

Aplicar el precio del turno durante sus límites horarios y regresar a la base fuera de ellos.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P1.** Etapa 2: condiciones comerciales; Restobar también depende de etapa 5. Sin Robot ni resultado aprobado. Ver [mapa de listas](../../docs/listas-precios.md).

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete autorizado, JAR/entorno identificados y baseline restaurable.
- Operación local, comprobante interno no fiscal, IVA 0 %, stock suficiente, sin impresión, pagos externos, ofertas ni descuentos adicionales salvo indicación expresa.
- Fixture NUEVO PENDIENTE: T=08:00–15:00 con A=$850; S=$900; sin otras listas superiores. Cada instante requiere perfil temporal reproducible antes del JAR.
- Roles, datos adicionales, acceso por teclado/JAB y oráculos de lectura pendientes de preparar/verificar para esta ficha. Un ejemplo seed disponible no acredita esos requisitos.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Abrir ventas independientes a las 07:59 y 08:00. | 07:59 usa S=$900; 08:00 usa T=$850 para A × 1. |
| 2 | Abrir venta a las 15:00:59. | Sigue T=$850: la selección tiene precisión de minuto. |
| 3 | Abrir venta a las 15:01. | Regresa a S=$900. |
| 4 | Cancelar los controles. | Sin ventas cobradas ni cambios de stock/caja. |

## Variantes y dependencias

Inicio y fin inclusivos. No modificar el reloj del host ni durante una venta; automatización temporal y sincronización Windows/MySQL pendientes.

## Evidencia y límites

Registrar selector de lista, contexto, productos/cantidades, precio unitario, bruto, descuentos, neto y moneda antes/después. Comprobar por identidad lista de cabecera y renglones, documento y efectos de stock/cobro con lectura acotada; no volcar filas completas. Conservar implementación separada de validación real del JAR. INFO resume; DEBUG muestra pasos; TRACE añade diagnóstico saneado. Todo fallo conserva paso, esperado/observado y evidencia; causa no determinada si no está demostrada.

## Recuperación

Ante una discrepancia, detener la confirmación y conservar el informe privado. Cancelar diálogos y cerrar únicamente procesos propios del runner; una cuenta Restobar puede haber persistido cambios. Restaurar el baseline antes de repetir o cambiar perfil. No corregir precios con SQL durante una venta ni editar el esperado para que coincida con lo observado.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada en commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; estas referencias describen reglas/riesgos, no una ejecución E2E.

- `src/ModuloConfiguracion/Servicios/TurnoListaPrecioHorarioPolicy.java:12-66`.
- `src/ModuloConfiguracion/Entidades/Turno.java:207-237`.

Registrar SHA256/build del JAR, paquete, perfil, fecha/horario y responsable en evidencia local. Los nombres QA son públicos; credenciales, nombres privados y capturas de autenticación no se publican.

