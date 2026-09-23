---
{"id":"XG-LPR-014","title":"Cancelar la elección manual de lista sin alterar la venta","product":"xgestion","module":"listas-precios","tags":["xgestion","regression","precios","listas-precios","listas-prioridad"],"status":"planned"}
---

# XG-LPR-014 — Cancelar la elección manual de lista sin alterar la venta

## Objetivo

Explorar listas y volver a la venta sin confirmar un cambio involuntario.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P1.** Etapa 2: condiciones comerciales; Restobar también depende de etapa 5. Sin Robot ni resultado aprobado. Ver [mapa de listas](../../docs/listas-precios.md).

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete autorizado, JAR/entorno identificados y baseline restaurable.
- Operación local, comprobante interno no fiscal, IVA 0 %, stock suficiente, sin impresión, pagos externos, ofertas ni descuentos adicionales salvo indicación expresa.
- Fixture NUEVO PENDIENTE: L1 A=$750; L2 A=$900; normal A=$1.000; selector habilitado, recálculo ON, sin cantidades especiales ni ofertas.
- Roles, datos adicionales, acceso por teclado/JAB y oráculos de lectura pendientes de preparar/verificar para esta ficha. Un ejemplo seed disponible no acredita esos requisitos.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Elegir L1 y cargar A × 2. | L1 y total $1.500. |
| 2 | Abrir selector, buscar L2 y cancelar sin aceptarla. | Conserva L1, A × 2 y $1.500. |
| 3 | Reabrir selector y aceptar L2. | L2 y total $1.800. |
| 4 | Cancelar cobro y volver. | Mantiene L2/$1.800 sin movimientos. |

## Variantes y dependencias

Cubrir botón Cancelar y cierre de ventana si son accesibles. No presumir que el picker filtre igual que la validación de una lista automática: esa disponibilidad debe calibrarse.

## Evidencia y límites

Registrar selector de lista, contexto, productos/cantidades, precio unitario, bruto, descuentos, neto y moneda antes/después. Comprobar por identidad lista de cabecera y renglones, documento y efectos de stock/cobro con lectura acotada; no volcar filas completas. Conservar implementación separada de validación real del JAR. INFO resume; DEBUG muestra pasos; TRACE añade diagnóstico saneado. Todo fallo conserva paso, esperado/observado y evidencia; causa no determinada si no está demostrada.

## Recuperación

Ante una discrepancia, detener la confirmación y conservar el informe privado. Cancelar diálogos y cerrar únicamente procesos propios del runner; una cuenta Restobar puede haber persistido cambios. Restaurar el baseline antes de repetir o cambiar perfil. No corregir precios con SQL durante una venta ni editar el esperado para que coincida con lo observado.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada en commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; estas referencias describen reglas/riesgos, no una ejecución E2E.

- `src/ModuloVentas/Vistas/FormVenta.java:2506-2512 y 3494-3513`.
- `src/ModuloVentas/Vistas/FormVenta.java:3565-3575`.

Registrar SHA256/build del JAR, paquete, perfil, fecha/horario y responsable en evidencia local. Los nombres QA son públicos; credenciales, nombres privados y capturas de autenticación no se publican.

