---
{"id":"XG-LPR-010","title":"Mantener el precio de un horario que cruza medianoche","product":"xgestion","module":"listas-precios","tags":["xgestion","regression","precios","listas-precios","listas-horario"],"status":"planned"}
---

# XG-LPR-010 — Mantener el precio de un horario que cruza medianoche

## Objetivo

Conservar el precio nocturno al pasar al día siguiente y retirarlo fuera de su intervalo.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P1.** Etapa 2: condiciones comerciales; Restobar también depende de etapa 5. Sin Robot ni resultado aprobado. Ver [mapa de listas](../../docs/listas-precios.md).

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete autorizado, JAR/entorno identificados y baseline restaurable.
- Operación local, comprobante interno no fiscal, IVA 0 %, stock suficiente, sin impresión, pagos externos, ofertas ni descuentos adicionales salvo indicación expresa.
- Fixture NUEVO PENDIENTE: T=22:00–10:00 con A=$850; S=$900; sin cliente con lista. Corridas temporales aisladas antes y después de medianoche.
- Roles, datos adicionales, acceso por teclado/JAB y oráculos de lectura pendientes de preparar/verificar para esta ficha. Un ejemplo seed disponible no acredita esos requisitos.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Abrir ventas a las 21:59 y 22:00. | A × 1 pasa de S=$900 a T=$850. |
| 2 | Abrir ventas a las 23:30, 00:00 y 10:00:59. | En las tres corresponde T=$850. |
| 3 | Abrir venta a las 10:01. | Corresponde S=$900. |
| 4 | Cerrar sin cobrar cada control. | No arrastra cuenta ni precio de otra corrida. |

## Variantes y dependencias

El cambio de fecha civil no corta el intervalo nocturno. No extender este criterio a vigencias de ofertas: tienen otra fuente.

## Evidencia y límites

Registrar selector de lista, contexto, productos/cantidades, precio unitario, bruto, descuentos, neto y moneda antes/después. Comprobar por identidad lista de cabecera y renglones, documento y efectos de stock/cobro con lectura acotada; no volcar filas completas. Conservar implementación separada de validación real del JAR. INFO resume; DEBUG muestra pasos; TRACE añade diagnóstico saneado. Todo fallo conserva paso, esperado/observado y evidencia; causa no determinada si no está demostrada.

## Recuperación

Ante una discrepancia, detener la confirmación y conservar el informe privado. Cancelar diálogos y cerrar únicamente procesos propios del runner; una cuenta Restobar puede haber persistido cambios. Restaurar el baseline antes de repetir o cambiar perfil. No corregir precios con SQL durante una venta ni editar el esperado para que coincida con lo observado.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada en commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; estas referencias describen reglas/riesgos, no una ejecución E2E.

- `src/ModuloConfiguracion/Servicios/TurnoListaPrecioHorarioPolicy.java:12-66`.
- `src/ModuloConfiguracion/Entidades/Turno.java:207-237`.

Registrar SHA256/build del JAR, paquete, perfil, fecha/horario y responsable en evidencia local. Los nombres QA son públicos; credenciales, nombres privados y capturas de autenticación no se publican.

