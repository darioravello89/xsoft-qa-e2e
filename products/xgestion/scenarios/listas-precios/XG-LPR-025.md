---
{"id":"XG-LPR-025","title":"Cambiar la lista de una cuenta Restobar abierta","product":"xgestion","module":"listas-precios","tags":["xgestion","regression","precios","listas-precios","listas-prioridad"],"status":"planned"}
---

# XG-LPR-025 — Cambiar la lista de una cuenta Restobar abierta

## Objetivo

Corregir el precio de una cuenta abierta respetando la opción de recalcular, sin alterar mesa o cocina.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P1.** Etapa 2: condiciones comerciales; Restobar también depende de etapa 5. Sin Robot ni resultado aprobado. Ver [mapa de listas](../../docs/listas-precios.md).

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete autorizado, JAR/entorno identificados y baseline restaurable.
- Operación local, comprobante interno no fiscal, IVA 0 %, stock suficiente, sin impresión, pagos externos, ofertas ni descuentos adicionales salvo indicación expresa.
- Fixture Restobar NUEVO PENDIENTE: cuenta abierta ya persistida con A × 2 a $1.000; L A=$750. Sin cocina, extras, cubiertos cobrados, ofertas ni escalas; mesa vinculada conocida.
- Roles, datos adicionales, acceso por teclado/JAB y oráculos de lectura pendientes de preparar/verificar para esta ficha. Un ejemplo seed disponible no acredita esos requisitos.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Abrir cuenta y elegir L con recálculo ON. | Conserva A × 2; lista L; total $1.500. |
| 2 | Cancelar cobro y volver a la cuenta. | Conserva cuenta, mesa y total; no queda cobrada ni emite comanda. |
| 3 | En otro baseline repetir con recálculo OFF. | Selecciona L pero A × 2 mantiene $2.000; cabecera/detalle conservan identidades. |
| 4 | Cerrar ventana y revisar cuenta abierta. | No duplica cuenta ni desvincula mesa por el cambio. |

## Variantes y dependencias

Cuenta abierta persistida; no venta nueva sin cabecera. Estado de cuenta, mesa y cocina se observa por separado. El cruce con extras corresponde a [XG-RES-021](../restobar/XG-RES-021.md).

Restobar persiste cambios; abandonar la ventana no los revierte. Restaurar baseline entre variantes.

## Evidencia y límites

Registrar selector de lista, contexto, productos/cantidades, precio unitario, bruto, descuentos, neto y moneda antes/después. Comprobar por identidad lista de cabecera y renglones, documento y efectos de stock/cobro con lectura acotada; no volcar filas completas. Conservar implementación separada de validación real del JAR. INFO resume; DEBUG muestra pasos; TRACE añade diagnóstico saneado. Todo fallo conserva paso, esperado/observado y evidencia; causa no determinada si no está demostrada.

## Recuperación

Ante una discrepancia, detener la confirmación y conservar el informe privado. Cancelar diálogos y cerrar únicamente procesos propios del runner; una cuenta Restobar puede haber persistido cambios. Restaurar el baseline antes de repetir o cambiar perfil. No corregir precios con SQL durante una venta ni editar el esperado para que coincida con lo observado.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada en commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; estas referencias describen reglas/riesgos, no una ejecución E2E.

- `src/ModuloRestobar/Vistas/formTicket.java:5288-5325 y 5645-5652`.

Registrar SHA256/build del JAR, paquete, perfil, fecha/horario y responsable en evidencia local. Los nombres QA son públicos; credenciales, nombres privados y capturas de autenticación no se publican.

