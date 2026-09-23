---
{"id":"XG-LPR-011","title":"Resolver de forma estable el minuto compartido por dos horarios","product":"xgestion","module":"listas-precios","tags":["xgestion","regression","precios","listas-precios","listas-horario","listas-prioridad"],"status":"planned"}
---

# XG-LPR-011 — Resolver de forma estable el minuto compartido por dos horarios

## Objetivo

Obtener un precio repetible en el cambio entre turnos que comparten una hora de borde.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P1.** Etapa 2: condiciones comerciales; Restobar también depende de etapa 5. Sin Robot ni resultado aprobado. Ver [mapa de listas](../../docs/listas-precios.md).

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete autorizado, JAR/entorno identificados y baseline restaurable.
- Operación local, comprobante interno no fiscal, IVA 0 %, stock suficiente, sin impresión, pagos externos, ofertas ni descuentos adicionales salvo indicación expresa.
- Fixture NUEVO PENDIENTE: T1=08:00–15:00 A=$850; T2=15:00–22:00 A=$750. T1 tiene menor ID; listas válidas, una empresa y sin cliente superior.
- Roles, datos adicionales, acceso por teclado/JAB y oráculos de lectura pendientes de preparar/verificar para esta ficha. Un ejemplo seed disponible no acredita esos requisitos.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Abrir venta a las 14:59. | T1; A × 1=$850. |
| 2 | Abrir dos ventas nuevas independientes a las 15:00. | Ambas eligen T1 por menor ID, aunque los dos intervalos incluyan el minuto. |
| 3 | Abrir venta a las 15:01. | T2; A × 1=$750. |
| 4 | En otro baseline invertir únicamente orden de IDs y repetir 15:00. | Gana T2 por menor ID; no depende del orden de carga de productos. |

## Variantes y dependencias

La política permite extremos compartidos, no superposición de duración. Para registros heredados superpuestos, documentar el mismo desempate y acordar si ese dato puede admitirse en el laboratorio.

## Evidencia y límites

Registrar selector de lista, contexto, productos/cantidades, precio unitario, bruto, descuentos, neto y moneda antes/después. Comprobar por identidad lista de cabecera y renglones, documento y efectos de stock/cobro con lectura acotada; no volcar filas completas. Conservar implementación separada de validación real del JAR. INFO resume; DEBUG muestra pasos; TRACE añade diagnóstico saneado. Todo fallo conserva paso, esperado/observado y evidencia; causa no determinada si no está demostrada.

## Recuperación

Ante una discrepancia, detener la confirmación y conservar el informe privado. Cancelar diálogos y cerrar únicamente procesos propios del runner; una cuenta Restobar puede haber persistido cambios. Restaurar el baseline antes de repetir o cambiar perfil. No corregir precios con SQL durante una venta ni editar el esperado para que coincida con lo observado.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada en commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; estas referencias describen reglas/riesgos, no una ejecución E2E.

- `src/ModuloConfiguracion/Servicios/TurnoListaPrecioHorarioPolicy.java:12-66`.
- `src/ModuloConfiguracion/Entidades/Turno.java:207-237`.

Registrar SHA256/build del JAR, paquete, perfil, fecha/horario y responsable en evidencia local. Los nombres QA son públicos; credenciales, nombres privados y capturas de autenticación no se publican.

