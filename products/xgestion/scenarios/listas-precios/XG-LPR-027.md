---
{"id":"XG-LPR-027","title":"Reabrir una cuenta Restobar editable y preservar las históricas","product":"xgestion","module":"listas-precios","tags":["xgestion","regression","precios","listas-precios","listas-prioridad"],"status":"planned"}
---

# XG-LPR-027 — Reabrir una cuenta Restobar editable y preservar las históricas

## Objetivo

Diferenciar la actualización permitida de una cuenta abierta frente a la conservación del comprobante cerrado.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P0.** Etapa 2: condiciones comerciales; Restobar también depende de etapa 5. Sin Robot ni resultado aprobado. Ver [mapa de listas](../../docs/listas-precios.md).

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete autorizado, JAR/entorno identificados y baseline restaurable.
- Operación local, comprobante interno no fiscal, IVA 0 %, stock suficiente, sin impresión, pagos externos, ofertas ni descuentos adicionales salvo indicación expresa.
- Fixture Restobar NUEVO PENDIENTE: cuenta abierta L y A × 2 guardados a $750; catálogo actual L a $900. Control cerrado con importes originales. Sin ofertas, extras ni escalas.
- Roles, datos adicionales, acceso por teclado/JAB y oráculos de lectura pendientes de preparar/verificar para esta ficha. Un ejemplo seed disponible no acredita esos requisitos.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Abrir cuenta abierta con recálculo ON. | Aplica L vigente: dos unidades, $1.800; misma cuenta/mesa. |
| 2 | Reabrir sin cambios adicionales. | Mantiene $1.800 sin duplicar renglones ni cobros. |
| 3 | Abrir control cerrado. | Conserva histórico $1.500; modificación/selector deshabilitados. |
| 4 | En otro baseline abrir la cuenta abierta con recálculo OFF. | Conserva $1.500; el perfil explica la diferencia frente a ON. |

## Variantes y dependencias

Repetir anulado como histórico. No mezclar con presupuesto de FormVenta: ese constructor no hace el mismo recálculo de lista al abrir.

Registrar por separado cuenta, mesa y cocina. No enviar comandas ni cerrar cuentas externas.

## Evidencia y límites

Registrar selector de lista, contexto, productos/cantidades, precio unitario, bruto, descuentos, neto y moneda antes/después. Comprobar por identidad lista de cabecera y renglones, documento y efectos de stock/cobro con lectura acotada; no volcar filas completas. Conservar implementación separada de validación real del JAR. INFO resume; DEBUG muestra pasos; TRACE añade diagnóstico saneado. Todo fallo conserva paso, esperado/observado y evidencia; causa no determinada si no está demostrada.

## Recuperación

Ante una discrepancia, detener la confirmación y conservar el informe privado. Cancelar diálogos y cerrar únicamente procesos propios del runner; una cuenta Restobar puede haber persistido cambios. Restaurar el baseline antes de repetir o cambiar perfil. No corregir precios con SQL durante una venta ni editar el esperado para que coincida con lo observado.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada en commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; estas referencias describen reglas/riesgos, no una ejecución E2E.

- `src/ModuloRestobar/Vistas/formTicket.java:621 y 2220-2264`.
- `src/ModuloRestobar/Vistas/formTicket.java:5288-5325 y 5645-5652`.

Registrar SHA256/build del JAR, paquete, perfil, fecha/horario y responsable en evidencia local. Los nombres QA son públicos; credenciales, nombres privados y capturas de autenticación no se publican.

