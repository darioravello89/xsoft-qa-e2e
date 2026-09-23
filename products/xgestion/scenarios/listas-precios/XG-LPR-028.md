---
{"id":"XG-LPR-028","title":"Acordar la prioridad entre lista elegida y cantidad en Restobar","product":"xgestion","module":"listas-precios","tags":["xgestion","regression","precios","listas-precios","listas-prioridad"],"status":"planned"}
---

# XG-LPR-028 — Acordar la prioridad entre lista elegida y cantidad en Restobar

## Objetivo

Definir y luego automatizar un precio consistente cuando el plato tiene lista elegida y escala por cantidad.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P1.** Etapa 2: condiciones comerciales; Restobar también depende de etapa 5. Sin Robot ni resultado aprobado. Ver [mapa de listas](../../docs/listas-precios.md).

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete autorizado, JAR/entorno identificados y baseline restaurable.
- Operación local, comprobante interno no fiscal, IVA 0 %, stock suficiente, sin impresión, pagos externos, ofertas ni descuentos adicionales salvo indicación expresa.
- Fixture Restobar NUEVO PENDIENTE: A normal=$1.000; L manual=$950; escala q>=5=$800; cuenta abierta con L; sin ofertas/extras. ORÁCULO PENDIENTE antes de habilitar suite.
- Roles, datos adicionales, acceso por teclado/JAB y oráculos de lectura pendientes de preparar/verificar para esta ficha. Un ejemplo seed disponible no acredita esos requisitos.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Registrar prioridad funcional aprobada para cada entrada. | Matriz acordada para código, picker con lista propia, consolidación, editor y cambio de lista; sin ella, caso BLOQUEADO. |
| 2 | Cargar A × 5 por cada vía en cuentas independientes. | Comparar con oráculo: $4.000 si domina escala o $4.750 si domina lista; no aprobar ambas como equivalentes. |
| 3 | Repetir completando 4→5 y cambiando lista en cuenta cargada. | Cantidad 5 sin duplicación; precio, lista de renglón y total siguen regla acordada para esa vía. |
| 4 | Cancelar cobro y conservar diferencias. | No convertir observado en esperado ni cobrar para ocultar discrepancias. |

## Variantes y dependencias

Consolidación de formTicket consulta cantidad primero; carga considera lista por renglón y cambio general pasa por TicketVenta. Puede revelar divergencia real: definir resultado requerido antes de atribuir defecto.

También queda pendiente verificar origen automático del primer ticket según vía de apertura. No extrapolar el resolvedor cliente/turno/fija de FormVenta a Restobar o App Mozos/QR.

## Evidencia y límites

Registrar selector de lista, contexto, productos/cantidades, precio unitario, bruto, descuentos, neto y moneda antes/después. Comprobar por identidad lista de cabecera y renglones, documento y efectos de stock/cobro con lectura acotada; no volcar filas completas. Conservar implementación separada de validación real del JAR. INFO resume; DEBUG muestra pasos; TRACE añade diagnóstico saneado. Todo fallo conserva paso, esperado/observado y evidencia; causa no determinada si no está demostrada.

## Recuperación

Ante una discrepancia, detener la confirmación y conservar el informe privado. Cancelar diálogos y cerrar únicamente procesos propios del runner; una cuenta Restobar puede haber persistido cambios. Restaurar el baseline antes de repetir o cambiar perfil. No corregir precios con SQL durante una venta ni editar el esperado para que coincida con lo observado.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada en commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; estas referencias describen reglas/riesgos, no una ejecución E2E.

- `src/ModuloRestobar/Vistas/formTicket.java:348-362 y 3277-3288; src/ModuloVentas/Entidades/TicketVenta.java:3207-3235`.
- `src/ModuloVentas/Vistas/FormVenta.java:2267-2281`.
- `src/ModuloVentas/Entidades/TicketVenta.java:2974-3045`.

Registrar SHA256/build del JAR, paquete, perfil, fecha/horario y responsable en evidencia local. Los nombres QA son públicos; credenciales, nombres privados y capturas de autenticación no se publican.

