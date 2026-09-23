---
{"id":"XG-LPR-002","title":"Separar las listas entre sucursales y reconocer el alcance global","product":"xgestion","module":"listas-precios","tags":["xgestion","regression","precios","listas-precios","listas-sucursal"],"status":"planned"}
---

# XG-LPR-002 — Separar las listas entre sucursales y reconocer el alcance global

## Objetivo

Vender en cada sucursal con sus propios precios y evitar que una lista de otra sucursal se aplique automáticamente.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P1.** Etapa 2: condiciones comerciales; Restobar también depende de etapa 5. Sin Robot ni resultado aprobado. Ver [mapa de listas](../../docs/listas-precios.md).

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete autorizado, JAR/entorno identificados y baseline restaurable.
- Operación local, comprobante interno no fiscal, IVA 0 %, stock suficiente, sin impresión, pagos externos, ofertas ni descuentos adicionales salvo indicación expresa.
- Fixture NUEVO PENDIENTE: S1 con única lista A=$900, S2 con única lista A=$1.100, S3 sin lista propia y una lista global G con A=$950. A normal=$1.000; fija=-1; sin cliente ni turno con lista.
- Roles, datos adicionales, acceso por teclado/JAB y oráculos de lectura pendientes de preparar/verificar para esta ficha. Un ejemplo seed disponible no acredita esos requisitos.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Abrir una venta en S1. | Lista S1; A × 1=$900. |
| 2 | En otra corrida restaurada, entrar en S2. | Lista S2; A × 1=$1.100; no hereda S1. |
| 3 | En otra corrida, abrir venta en S3. | Ninguna; A × 1=$1.000. G no se convierte por sí sola en default de sucursal. |
| 4 | Preparar G como fija explícita y abrir otra venta en S3. | Se admite G por su alcance global; A × 1=$950. |

## Variantes y dependencias

Repetir cambio de sesión S1→S2 identificando el contexto. No conectar varios puestos simultáneos: concurrencia queda fuera.

## Evidencia y límites

Registrar selector de lista, contexto, productos/cantidades, precio unitario, bruto, descuentos, neto y moneda antes/después. Comprobar por identidad lista de cabecera y renglones, documento y efectos de stock/cobro con lectura acotada; no volcar filas completas. Conservar implementación separada de validación real del JAR. INFO resume; DEBUG muestra pasos; TRACE añade diagnóstico saneado. Todo fallo conserva paso, esperado/observado y evidencia; causa no determinada si no está demostrada.

## Recuperación

Ante una discrepancia, detener la confirmación y conservar el informe privado. Cancelar diálogos y cerrar únicamente procesos propios del runner; una cuenta Restobar puede haber persistido cambios. Restaurar el baseline antes de repetir o cambiar perfil. No corregir precios con SQL durante una venta ni editar el esperado para que coincida con lo observado.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada en commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; estas referencias describen reglas/riesgos, no una ejecución E2E.

- `src/ModuloProveedores/Entidades/ListaPrecio.java:240-287`.
- `src/ModuloVentas/Servicios/VentaListaPrecioPrioridadPolicy.java:37-74`.
- `src/ModuloVentas/Vistas/FormVenta.java:3413-3491`.

Registrar SHA256/build del JAR, paquete, perfil, fecha/horario y responsable en evidencia local. Los nombres QA son públicos; credenciales, nombres privados y capturas de autenticación no se publican.

