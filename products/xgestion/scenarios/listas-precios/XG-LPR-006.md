---
{"id":"XG-LPR-006","title":"Cambiar o quitar el cliente y recalcular las condiciones de la venta","product":"xgestion","module":"listas-precios","tags":["xgestion","regression","precios","listas-precios","listas-cliente"],"status":"planned"}
---

# XG-LPR-006 — Cambiar o quitar el cliente y recalcular las condiciones de la venta

## Objetivo

Corregir el cliente de una venta abierta sin perder productos ni conservar el precio del cliente anterior.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P1.** Etapa 2: condiciones comerciales; Restobar también depende de etapa 5. Sin Robot ni resultado aprobado. Ver [mapa de listas](../../docs/listas-precios.md).

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete autorizado, JAR/entorno identificados y baseline restaurable.
- Operación local, comprobante interno no fiscal, IVA 0 %, stock suficiente, sin impresión, pagos externos, ofertas ni descuentos adicionales salvo indicación expresa.
- Fixture NUEVO PENDIENTE: C1 con A=$750, C2 con A=$700, C0 sin lista, turno T con A=$850. A normal=$1.000; recálculo ON; descuentos de clientes en cero.
- Roles, datos adicionales, acceso por teclado/JAB y oráculos de lectura pendientes de preparar/verificar para esta ficha. Un ejemplo seed disponible no acredita esos requisitos.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Elegir C1 y cargar A × 2. | Lista C1; total $1.500. |
| 2 | Cambiar a C2. | Conserva A × 2; lista C2; total $1.400. |
| 3 | Cambiar al cliente C0 sin lista. | Resuelve T; conserva A × 2; total $1.700. |
| 4 | Volver a C1 y cancelar cobro. | Recupera $1.500 sin duplicar renglones ni pagos. |

## Variantes y dependencias

Repetir C1→C0 sin turno y con base S=$900: total $1.800. Recálculo OFF necesita la expectativa de XG-LPR-015; conservar precios con ese perfil no prueba un fallo.

## Evidencia y límites

Registrar selector de lista, contexto, productos/cantidades, precio unitario, bruto, descuentos, neto y moneda antes/después. Comprobar por identidad lista de cabecera y renglones, documento y efectos de stock/cobro con lectura acotada; no volcar filas completas. Conservar implementación separada de validación real del JAR. INFO resume; DEBUG muestra pasos; TRACE añade diagnóstico saneado. Todo fallo conserva paso, esperado/observado y evidencia; causa no determinada si no está demostrada.

## Recuperación

Ante una discrepancia, detener la confirmación y conservar el informe privado. Cancelar diálogos y cerrar únicamente procesos propios del runner; una cuenta Restobar puede haber persistido cambios. Restaurar el baseline antes de repetir o cambiar perfil. No corregir precios con SQL durante una venta ni editar el esperado para que coincida con lo observado.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada en commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; estas referencias describen reglas/riesgos, no una ejecución E2E.

- `src/ModuloVentas/Vistas/FormVenta.java:7327-7335`.
- `src/ModuloVentas/Vistas/FormVenta.java:3413-3491`.
- `src/ModuloVentas/Vistas/FormVenta.java:3565-3575`.
- `src/ModuloVentas/Entidades/TicketVenta.java:2974-3045`.

Registrar SHA256/build del JAR, paquete, perfil, fecha/horario y responsable en evidencia local. Los nombres QA son públicos; credenciales, nombres privados y capturas de autenticación no se publican.

