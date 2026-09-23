---
{"id":"XG-LPR-026","title":"Distinguir la lista del mozo o cadete de cambiar el cliente en Restobar","product":"xgestion","module":"listas-precios","tags":["xgestion","regression","precios","listas-precios","listas-cliente","listas-prioridad"],"status":"planned"}
---

# XG-LPR-026 — Distinguir la lista del mozo o cadete de cambiar el cliente en Restobar

## Objetivo

Comprender qué cambios de atención alteran la lista sin importar la prioridad de Venta cotidiana.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P1.** Etapa 2: condiciones comerciales; Restobar también depende de etapa 5. Sin Robot ni resultado aprobado. Ver [mapa de listas](../../docs/listas-precios.md).

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete autorizado, JAR/entorno identificados y baseline restaurable.
- Operación local, comprobante interno no fiscal, IVA 0 %, stock suficiente, sin impresión, pagos externos, ofertas ni descuentos adicionales salvo indicación expresa.
- Fixture Restobar NUEVO PENDIENTE: cuenta abierta A × 2; M con L-M A=$800, D con L-D A=$700, C con L-C A=$750 pero descuento 0. Sin escalas/ofertas; recálculo ON.
- Roles, datos adicionales, acceso por teclado/JAB y oráculos de lectura pendientes de preparar/verificar para esta ficha. Un ejemplo seed disponible no acredita esos requisitos.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Elegir mozo M. | Cambia responsable y lista L-M; A × 2=$1.600. |
| 2 | Cambiar solamente al cliente C. | Cliente C; conserva L-M/$1.600: esta acción no invoca el resolvedor de FormVenta. |
| 3 | En cuenta delivery preparada, elegir cadete D. | Responsable y lista L-D; A × 2=$1.400; no asigna lista del cliente por analogía. |
| 4 | Cancelar cobro en cada cuenta. | Cuentas abiertas; sin cobro ni cambios de preparación. |

## Variantes y dependencias

Cancelar pickers no cambia responsable/lista. Origen de pedido QR/app y primera lista requieren integración aparte, no quedan acreditados por estos pickers.

Precios proceden de listas declaradas por los pickers del fixture; no equivalen a prioridad global cliente→turno en Restobar.

## Evidencia y límites

Registrar selector de lista, contexto, productos/cantidades, precio unitario, bruto, descuentos, neto y moneda antes/después. Comprobar por identidad lista de cabecera y renglones, documento y efectos de stock/cobro con lectura acotada; no volcar filas completas. Conservar implementación separada de validación real del JAR. INFO resume; DEBUG muestra pasos; TRACE añade diagnóstico saneado. Todo fallo conserva paso, esperado/observado y evidencia; causa no determinada si no está demostrada.

## Recuperación

Ante una discrepancia, detener la confirmación y conservar el informe privado. Cancelar diálogos y cerrar únicamente procesos propios del runner; una cuenta Restobar puede haber persistido cambios. Restaurar el baseline antes de repetir o cambiar perfil. No corregir precios con SQL durante una venta ni editar el esperado para que coincida con lo observado.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada en commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; estas referencias describen reglas/riesgos, no una ejecución E2E.

- `src/ModuloRestobar/Vistas/formTicket.java:5571-5637`.
- `src/ModuloRestobar/Vistas/formTicket.java:5288-5325 y 5645-5652`.

Registrar SHA256/build del JAR, paquete, perfil, fecha/horario y responsable en evidencia local. Los nombres QA son públicos; credenciales, nombres privados y capturas de autenticación no se publican.

