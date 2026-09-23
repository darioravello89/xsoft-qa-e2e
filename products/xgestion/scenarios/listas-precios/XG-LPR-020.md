---
{"id":"XG-LPR-020","title":"Convertir el precio USD de una lista a la moneda de la venta","product":"xgestion","module":"listas-precios","tags":["xgestion","regression","precios","listas-precios","listas-prioridad"],"status":"planned"}
---

# XG-LPR-020 — Convertir el precio USD de una lista a la moneda de la venta

## Objetivo

Cobrar una lista en dólares sin confundir su precio original con el equivalente en pesos.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P0.** Etapa 2: condiciones comerciales; Restobar también depende de etapa 5. Sin Robot ni resultado aprobado. Ver [mapa de listas](../../docs/listas-precios.md).

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete autorizado, JAR/entorno identificados y baseline restaurable.
- Operación local, comprobante interno no fiscal, IVA 0 %, stock suficiente, sin impresión, pagos externos, ofertas ni descuentos adicionales salvo indicación expresa.
- Reutilizable del seed: QA-SEED-LISTAS y lista 980102 a USD 2,50; ejemplo LISTA-USD. Perfil NUEVO PENDIENTE: cotización empresa/venta ARS 1.000 por USD, moneda contable ARS y conversión habilitada; sin ofertas.
- Roles, datos adicionales, acceso por teclado/JAB y oráculos de lectura pendientes de preparar/verificar para esta ficha. Un ejemplo seed disponible no acredita esos requisitos.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Elegir lista USD y cargar una unidad. | Original USD 2,50; equivalente contable ARS 2.500; moneda identificada. |
| 2 | Completar dos unidades. | Original USD 5,00 y total ARS 5.000; no convierte dos veces. |
| 3 | Cancelar/retomar cobro en efectivo ARS. | Mantiene ARS 5.000 y cotización 1.000. |
| 4 | Cobrar ARS 5.000 y consultar comprobante. | Conserva original, equivalente, lista y cotización; una venta/cobro. |

## Variantes y dependencias

Repetir cotización 2.000 desde baseline: una unidad equivale a ARS 5.000. Pago USD/vuelto mixto pertenecen a otro circuito y no se incluyen por tener lista USD.

No usar cotización de mercado ni actualizar por red: son datos del laboratorio y requieren perfil de moneda verificado.

## Evidencia y límites

Registrar selector de lista, contexto, productos/cantidades, precio unitario, bruto, descuentos, neto y moneda antes/después. Comprobar por identidad lista de cabecera y renglones, documento y efectos de stock/cobro con lectura acotada; no volcar filas completas. Conservar implementación separada de validación real del JAR. INFO resume; DEBUG muestra pasos; TRACE añade diagnóstico saneado. Todo fallo conserva paso, esperado/observado y evidencia; causa no determinada si no está demostrada.

## Recuperación

Ante una discrepancia, detener la confirmación y conservar el informe privado. Cancelar diálogos y cerrar únicamente procesos propios del runner; una cuenta Restobar puede haber persistido cambios. Restaurar el baseline antes de repetir o cambiar perfil. No corregir precios con SQL durante una venta ni editar el esperado para que coincida con lo observado.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada en commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; estas referencias describen reglas/riesgos, no una ejecución E2E.

- `src/ModuloProveedores/Entidades/ListaPrecioDetalle.java:1310-1327`.
- `src/ModuloVentas/Entidades/TicketVenta.java:2974-3045`.
- `src/ModuloVentas/Vistas/FormVenta.java:3516-3562; src/ModuloVentas/Entidades/VentaCotizacionPolicy.java:11-15`.
- `test/ModuloVentas/Entidades/TicketVentaPresupuestoCotizacionTest.java:100-120 y 293-313`.

Registrar SHA256/build del JAR, paquete, perfil, fecha/horario y responsable en evidencia local. Los nombres QA son públicos; credenciales, nombres privados y capturas de autenticación no se publican.

