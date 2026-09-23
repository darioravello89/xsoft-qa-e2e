---
{"id":"XG-LPR-015","title":"Cambiar la lista sin recalcular los productos ya cargados","product":"xgestion","module":"listas-precios","tags":["xgestion","regression","precios","listas-precios","listas-prioridad"],"status":"planned"}
---

# XG-LPR-015 — Cambiar la lista sin recalcular los productos ya cargados

## Objetivo

Conservar precios pactados de renglones existentes cuando el perfil deshabilita el recálculo por cambio de lista.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P0.** Etapa 2: condiciones comerciales; Restobar también depende de etapa 5. Sin Robot ni resultado aprobado. Ver [mapa de listas](../../docs/listas-precios.md).

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete autorizado, JAR/entorno identificados y baseline restaurable.
- Operación local, comprobante interno no fiscal, IVA 0 %, stock suficiente, sin impresión, pagos externos, ofertas ni descuentos adicionales salvo indicación expresa.
- Fixture NUEVO PENDIENTE: recálculo OFF; normal A=$1.000/B=$2.000; L1 A=$750/B=$1.500; sin cliente/turno, precio por cantidad ni ofertas.
- Roles, datos adicionales, acceso por teclado/JAB y oráculos de lectura pendientes de preparar/verificar para esta ficha. Un ejemplo seed disponible no acredita esos requisitos.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Con Ninguna cargar A × 2. | A mantiene precio $1.000; total $2.000. |
| 2 | Elegir L1. | Selector L1, pero A × 2 sigue totalizando $2.000. |
| 3 | Agregar B × 1, que no estaba en la venta. | B usa $1.500 de L1; total canasta $3.500. |
| 4 | Cancelar/retomar cobro y confirmar $3.500. | Un cobro; A conserva su precio y B el de L1, con identidades de lista por renglón. |

## Variantes y dependencias

Repetir con recálculo ON desde cero: al elegir L1 A × 2 pasa a $1.500; con B × 1 totaliza $3.000. No modificar el perfil durante la operación.

Agregar nuevamente A después del cambio puede implicar consolidación de precios; requiere oráculo propio y no queda acreditado con B.

## Evidencia y límites

Registrar selector de lista, contexto, productos/cantidades, precio unitario, bruto, descuentos, neto y moneda antes/después. Comprobar por identidad lista de cabecera y renglones, documento y efectos de stock/cobro con lectura acotada; no volcar filas completas. Conservar implementación separada de validación real del JAR. INFO resume; DEBUG muestra pasos; TRACE añade diagnóstico saneado. Todo fallo conserva paso, esperado/observado y evidencia; causa no determinada si no está demostrada.

## Recuperación

Ante una discrepancia, detener la confirmación y conservar el informe privado. Cancelar diálogos y cerrar únicamente procesos propios del runner; una cuenta Restobar puede haber persistido cambios. Restaurar el baseline antes de repetir o cambiar perfil. No corregir precios con SQL durante una venta ni editar el esperado para que coincida con lo observado.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada en commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; estas referencias describen reglas/riesgos, no una ejecución E2E.

- `src/ModuloVentas/Vistas/FormVenta.java:3565-3575`.
- `src/ModuloVentas/Entidades/TicketVenta.java:2974-3045`.
- `src/ModuloVentas/Vistas/FormVenta.java:2267-2281`.

Registrar SHA256/build del JAR, paquete, perfil, fecha/horario y responsable en evidencia local. Los nombres QA son públicos; credenciales, nombres privados y capturas de autenticación no se publican.

