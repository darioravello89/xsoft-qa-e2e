---
{"id":"XG-LPR-022","title":"Reabrir un presupuesto con su lista, moneda y precios guardados","product":"xgestion","module":"listas-precios","tags":["xgestion","regression","precios","listas-precios","listas-prioridad"],"status":"planned"}
---

# XG-LPR-022 — Reabrir un presupuesto con su lista, moneda y precios guardados

## Objetivo

Retomar una cotización guardada sin multiplicar importes ni reemplazarla por el default de una venta nueva.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P1.** Etapa 2: condiciones comerciales; Restobar también depende de etapa 5. Sin Robot ni resultado aprobado. Ver [mapa de listas](../../docs/listas-precios.md).

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete autorizado, JAR/entorno identificados y baseline restaurable.
- Operación local, comprobante interno no fiscal, IVA 0 %, stock suficiente, sin impresión, pagos externos, ofertas ni descuentos adicionales salvo indicación expresa.
- Fixture NUEVO PENDIENTE: presupuesto interno A × 2, lista USD a USD 2,50, moneda del documento USD, total USD 5 y cotización 1.000; base actual distinta. Sin ofertas. Control separado ARS A × 2 a $750, total $1.500.
- Roles, datos adicionales, acceso por teclado/JAB y oráculos de lectura pendientes de preparar/verificar para esta ficha. Un ejemplo seed disponible no acredita esos requisitos.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Abrir el presupuesto USD. | Recupera lista y moneda; total USD 5, no USD 5.000 ni precio del default actual. |
| 2 | Cerrar y reabrir sin editar. | Misma identidad, dos unidades, total USD 5 y cotización guardada. |
| 3 | Guardar sin modificar y consultar nuevamente. | No duplica documento ni convierte otra vez originales. |
| 4 | Repetir el control ARS. | Conserva $1.500 en las reaperturas. |

## Variantes y dependencias

Variantes futuras: precio de catálogo modificado después de guardar y edición de cantidad. La apertura carga detalle persistido; no acredita qué precio debe usar la edición posterior con catálogo cambiado.

Guardar/reabrir necesita paquete y oráculo de identidad propios, además de calibración. No queda cubierto por PRM-071/072.

## Evidencia y límites

Registrar selector de lista, contexto, productos/cantidades, precio unitario, bruto, descuentos, neto y moneda antes/después. Comprobar por identidad lista de cabecera y renglones, documento y efectos de stock/cobro con lectura acotada; no volcar filas completas. Conservar implementación separada de validación real del JAR. INFO resume; DEBUG muestra pasos; TRACE añade diagnóstico saneado. Todo fallo conserva paso, esperado/observado y evidencia; causa no determinada si no está demostrada.

## Recuperación

Ante una discrepancia, detener la confirmación y conservar el informe privado. Cancelar diálogos y cerrar únicamente procesos propios del runner; una cuenta Restobar puede haber persistido cambios. Restaurar el baseline antes de repetir o cambiar perfil. No corregir precios con SQL durante una venta ni editar el esperado para que coincida con lo observado.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada en commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; estas referencias describen reglas/riesgos, no una ejecución E2E.

- `src/ModuloVentas/Vistas/FormVenta.java:1916-1962`.
- `test/ModuloVentas/Entidades/TicketVentaPresupuestoCotizacionTest.java:100-120 y 293-313`.

Registrar SHA256/build del JAR, paquete, perfil, fecha/horario y responsable en evidencia local. Los nombres QA son públicos; credenciales, nombres privados y capturas de autenticación no se publican.

