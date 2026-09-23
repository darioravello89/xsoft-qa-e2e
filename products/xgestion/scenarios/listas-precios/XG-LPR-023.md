---
{"id":"XG-LPR-023","title":"Consultar una venta histórica sin recalcular sus listas","product":"xgestion","module":"listas-precios","tags":["xgestion","regression","precios","listas-precios","listas-prioridad"],"status":"planned"}
---

# XG-LPR-023 — Consultar una venta histórica sin recalcular sus listas

## Objetivo

Ver el importe realmente cobrado aunque el precio actual de la lista haya cambiado.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P0.** Etapa 2: condiciones comerciales; Restobar también depende de etapa 5. Sin Robot ni resultado aprobado. Ver [mapa de listas](../../docs/listas-precios.md).

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete autorizado, JAR/entorno identificados y baseline restaurable.
- Operación local, comprobante interno no fiscal, IVA 0 %, stock suficiente, sin impresión, pagos externos, ofertas ni descuentos adicionales salvo indicación expresa.
- Fixture NUEVO PENDIENTE: venta interna cerrada A × 2 a $750/u, total $1.500; catálogo actual de esa lista A=$900. Control anulado separado; sin comprobantes fiscales ni impresión.
- Roles, datos adicionales, acceso por teclado/JAB y oráculos de lectura pendientes de preparar/verificar para esta ficha. Un ejemplo seed disponible no acredita esos requisitos.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Abrir venta cerrada desde consulta. | Dos unidades y total histórico $1.500; no usa precio actual $900. |
| 2 | Revisar edición de productos/lista. | Documento en lectura; no permite repriciar los renglones del cobro pasado. |
| 3 | Cerrar consulta y reabrir. | Misma identidad/importes, sin cobros nuevos. |
| 4 | Repetir documento anulado del fixture. | Conserva histórico y estado; consultar no reactiva la venta. |

## Variantes y dependencias

No convertir esta ficha en reimpresión. Presupuesto editable es XG-LPR-022 y tiene otro contrato.

Lecturas acotadas por identidad antes/después; nunca comparar el histórico contra el precio vigente como supuesto esperado.

## Evidencia y límites

Registrar selector de lista, contexto, productos/cantidades, precio unitario, bruto, descuentos, neto y moneda antes/después. Comprobar por identidad lista de cabecera y renglones, documento y efectos de stock/cobro con lectura acotada; no volcar filas completas. Conservar implementación separada de validación real del JAR. INFO resume; DEBUG muestra pasos; TRACE añade diagnóstico saneado. Todo fallo conserva paso, esperado/observado y evidencia; causa no determinada si no está demostrada.

## Recuperación

Ante una discrepancia, detener la confirmación y conservar el informe privado. Cancelar diálogos y cerrar únicamente procesos propios del runner; una cuenta Restobar puede haber persistido cambios. Restaurar el baseline antes de repetir o cambiar perfil. No corregir precios con SQL durante una venta ni editar el esperado para que coincida con lo observado.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada en commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; estas referencias describen reglas/riesgos, no una ejecución E2E.

- `src/ModuloVentas/Vistas/FormVenta.java:1916-1962`.

Registrar SHA256/build del JAR, paquete, perfil, fecha/horario y responsable en evidencia local. Los nombres QA son públicos; credenciales, nombres privados y capturas de autenticación no se publican.

