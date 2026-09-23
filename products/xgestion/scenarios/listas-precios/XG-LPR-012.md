---
{"id":"XG-LPR-012","title":"Ignorar horarios inactivos, incompletos o de otra empresa","product":"xgestion","module":"listas-precios","tags":["xgestion","regression","precios","listas-precios","listas-horario"],"status":"planned"}
---

# XG-LPR-012 — Ignorar horarios inactivos, incompletos o de otra empresa

## Objetivo

Evitar que un horario no aplicable cambie el precio de venta.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P1.** Etapa 2: condiciones comerciales; Restobar también depende de etapa 5. Sin Robot ni resultado aprobado. Ver [mapa de listas](../../docs/listas-precios.md).

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete autorizado, JAR/entorno identificados y baseline restaurable.
- Operación local, comprobante interno no fiscal, IVA 0 %, stock suficiente, sin impresión, pagos externos, ofertas ni descuentos adicionales salvo indicación expresa.
- Fixture NUEVO PENDIENTE: S A=$900; candidato T A=$850 por variante: inactivo, sin lista, inicio=fin, inicio/fin nulos o de otra empresa. Hora controlada 10:00.
- Roles, datos adicionales, acceso por teclado/JAB y oráculos de lectura pendientes de preparar/verificar para esta ficha. Un ejemplo seed disponible no acredita esos requisitos.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Ejecutar control positivo con T activo 08:00–15:00. | T; A × 1=$850; luego abandonar. |
| 2 | Restaurar una variante inválida y abrir venta. | S; A × 1=$900. |
| 3 | Elegir cliente sin lista para provocar nueva resolución. | Sigue S; no queda precio residual de T. |
| 4 | Abandonar la operación. | Sin cobro ni cambio de stock. |

## Variantes y dependencias

Repetir cada causa por separado, con perfil identificado. La ausencia de toda regla de precios no basta como control: se exige el paso positivo.

## Evidencia y límites

Registrar selector de lista, contexto, productos/cantidades, precio unitario, bruto, descuentos, neto y moneda antes/después. Comprobar por identidad lista de cabecera y renglones, documento y efectos de stock/cobro con lectura acotada; no volcar filas completas. Conservar implementación separada de validación real del JAR. INFO resume; DEBUG muestra pasos; TRACE añade diagnóstico saneado. Todo fallo conserva paso, esperado/observado y evidencia; causa no determinada si no está demostrada.

## Recuperación

Ante una discrepancia, detener la confirmación y conservar el informe privado. Cancelar diálogos y cerrar únicamente procesos propios del runner; una cuenta Restobar puede haber persistido cambios. Restaurar el baseline antes de repetir o cambiar perfil. No corregir precios con SQL durante una venta ni editar el esperado para que coincida con lo observado.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada en commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; estas referencias describen reglas/riesgos, no una ejecución E2E.

- `src/ModuloConfiguracion/Entidades/Turno.java:207-237`.
- `src/ModuloConfiguracion/Servicios/TurnoListaPrecioHorarioPolicy.java:12-66`.
- `src/ModuloVentas/Vistas/FormVenta.java:3413-3491`.

Registrar SHA256/build del JAR, paquete, perfil, fecha/horario y responsable en evidencia local. Los nombres QA son públicos; credenciales, nombres privados y capturas de autenticación no se publican.

