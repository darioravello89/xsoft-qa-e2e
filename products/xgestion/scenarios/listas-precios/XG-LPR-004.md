---
{"id":"XG-LPR-004","title":"Trabajar sin lista base sin anular las condiciones del cliente o turno","product":"xgestion","module":"listas-precios","tags":["xgestion","regression","precios","listas-precios","listas-prioridad"],"status":"planned"}
---

# XG-LPR-004 — Trabajar sin lista base sin anular las condiciones del cliente o turno

## Objetivo

Entender la opción Ninguna de la configuración fija y cobrar según las condiciones superiores que sí correspondan.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P1.** Etapa 2: condiciones comerciales; Restobar también depende de etapa 5. Sin Robot ni resultado aprobado. Ver [mapa de listas](../../docs/listas-precios.md).

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete autorizado, JAR/entorno identificados y baseline restaurable.
- Operación local, comprobante interno no fiscal, IVA 0 %, stock suficiente, sin impresión, pagos externos, ofertas ni descuentos adicionales salvo indicación expresa.
- Fixture NUEVO PENDIENTE: fija=0, sucursal A=$900, normal A=$1.000, cliente C con A=$750 y turno T con A=$850. Perfiles separados, descuentos del cliente en cero.
- Roles, datos adicionales, acceso por teclado/JAB y oráculos de lectura pendientes de preparar/verificar para esta ficha. Un ejemplo seed disponible no acredita esos requisitos.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Abrir venta sin cliente con lista ni turno aplicable. | Ninguna; A × 1=$1.000. |
| 2 | Repetir con turno T activo. | T; A × 1=$850, aunque la base fija sea Ninguna. |
| 3 | Repetir eligiendo C y con T activo. | C; A × 1=$750. |
| 4 | Abandonar cada operación. | Ninguna crea un cobro; no mezcla precios entre perfiles. |

## Variantes y dependencias

No interpretar fija=0 como bloqueo de toda lista. Elegir manualmente Ninguna es otra acción; no equivale al valor base de configuración.

## Evidencia y límites

Registrar selector de lista, contexto, productos/cantidades, precio unitario, bruto, descuentos, neto y moneda antes/después. Comprobar por identidad lista de cabecera y renglones, documento y efectos de stock/cobro con lectura acotada; no volcar filas completas. Conservar implementación separada de validación real del JAR. INFO resume; DEBUG muestra pasos; TRACE añade diagnóstico saneado. Todo fallo conserva paso, esperado/observado y evidencia; causa no determinada si no está demostrada.

## Recuperación

Ante una discrepancia, detener la confirmación y conservar el informe privado. Cancelar diálogos y cerrar únicamente procesos propios del runner; una cuenta Restobar puede haber persistido cambios. Restaurar el baseline antes de repetir o cambiar perfil. No corregir precios con SQL durante una venta ni editar el esperado para que coincida con lo observado.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada en commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; estas referencias describen reglas/riesgos, no una ejecución E2E.

- `src/ModuloVentas/Servicios/VentaListaPrecioPrioridadPolicy.java:37-74`.
- `src/ModuloVentas/Vistas/FormVenta.java:3413-3491`.
- `src/ModuloVentas/Vistas/FormVenta.java:7327-7335`.

Registrar SHA256/build del JAR, paquete, perfil, fecha/horario y responsable en evidencia local. Los nombres QA son públicos; credenciales, nombres privados y capturas de autenticación no se publican.

