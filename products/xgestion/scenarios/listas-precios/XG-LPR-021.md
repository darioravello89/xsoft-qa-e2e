---
{"id":"XG-LPR-021","title":"Rechazar una lista USD sin cotización y recuperar la venta","product":"xgestion","module":"listas-precios","tags":["xgestion","regression","precios","listas-precios","listas-prioridad"],"status":"planned"}
---

# XG-LPR-021 — Rechazar una lista USD sin cotización y recuperar la venta

## Objetivo

Corregir una cotización inválida sin que el intento fallido altere lista, cantidades o importes.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P0.** Etapa 2: condiciones comerciales; Restobar también depende de etapa 5. Sin Robot ni resultado aprobado. Ver [mapa de listas](../../docs/listas-precios.md).

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete autorizado, JAR/entorno identificados y baseline restaurable.
- Operación local, comprobante interno no fiscal, IVA 0 %, stock suficiente, sin impresión, pagos externos, ofertas ni descuentos adicionales salvo indicación expresa.
- Fixture NUEVO PENDIENTE: A × 2 en lista ARS=$750/u, total $1.500; candidata USD=$2,50/u; recálculo ON y sin escalas. Cotización venta 0/empresa 1.000; variante separada empresa 0/venta 1.000.
- Roles, datos adicionales, acceso por teclado/JAB y oráculos de lectura pendientes de preparar/verificar para esta ficha. Un ejemplo seed disponible no acredita esos requisitos.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Elegir lista USD con cotización inválida. | Aviso Cotización requerida; conserva lista ARS, dos unidades y $1.500. |
| 2 | Cerrar aviso y revisar todos los renglones. | Ninguna conversión parcial ni cambio de identidad de lista. |
| 3 | En el perfil que permite corregir, ingresar cotización válida 1.000 y elegir USD. | Moneda contable ARS: dos unidades equivalen a ARS 5.000; selector USD correcto. |
| 4 | Cancelar y retomar cobro. | Mantiene ARS 5.000; intento rechazado sin movimientos. |

## Variantes y dependencias

Invalidación por empresa y por venta se prueban separadas. Si el rol no puede editar cotización, recuperar desde otro baseline autorizado; no cambiarla mediante SQL durante la venta.

Excluir precio por cantidad: la prevalidación USD consulta escala primero; ese cruce necesita resolver su prioridad antes de fijar el oráculo.

## Evidencia y límites

Registrar selector de lista, contexto, productos/cantidades, precio unitario, bruto, descuentos, neto y moneda antes/después. Comprobar por identidad lista de cabecera y renglones, documento y efectos de stock/cobro con lectura acotada; no volcar filas completas. Conservar implementación separada de validación real del JAR. INFO resume; DEBUG muestra pasos; TRACE añade diagnóstico saneado. Todo fallo conserva paso, esperado/observado y evidencia; causa no determinada si no está demostrada.

## Recuperación

Ante una discrepancia, detener la confirmación y conservar el informe privado. Cancelar diálogos y cerrar únicamente procesos propios del runner; una cuenta Restobar puede haber persistido cambios. Restaurar el baseline antes de repetir o cambiar perfil. No corregir precios con SQL durante una venta ni editar el esperado para que coincida con lo observado.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada en commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; estas referencias describen reglas/riesgos, no una ejecución E2E.

- `src/ModuloVentas/Vistas/FormVenta.java:3516-3562; src/ModuloVentas/Entidades/VentaCotizacionPolicy.java:11-15`.
- `src/ModuloVentas/Vistas/FormVenta.java:3413-3491`.
- `src/ModuloVentas/Vistas/FormVenta.java:2506-2512 y 3494-3513`.

Registrar SHA256/build del JAR, paquete, perfil, fecha/horario y responsable en evidencia local. Los nombres QA son públicos; credenciales, nombres privados y capturas de autenticación no se publican.

