---
{"id":"XG-FIN-002","title":"Conciliar recepción y pago a proveedor desde caja","product":"xgestion","module":"conciliacion","tags":["xgestion","regression","conciliacion","integridad-operaciones","compras","cuenta-corriente","caja","stock"],"status":"planned"}
---

# XG-FIN-002 — Conciliar recepción y pago a proveedor desde caja

## Objetivo

Comprobar recepción, deuda y pago de una compra sin confundir los registros financieros con dos egresos.

## Estado y alcance

**Pendiente de automatizar (`planned`), prioridad P0.** Etapas 3–4, integridad entre circuitos.
Ver [roadmap de circuitos críticos](../../docs/circuitos-criticos.md). No tiene Robot, seed propio ni evidencia del JAR.

## Precondiciones y datos

- Windows QA aislado, JAR identificado, baseline recuperable y paquete autorizado. Sin fiscal, correo, servicios externos ni impresoras salvo laboratorio expresamente preparado.
- Proveedor QA-FIN-P1 sin saldo, artículo QA-FIN-B stock 50 y costo ARS 100; recibir 10 unidades por ARS 1.000, IVA 0. Caja ARS 5.000. Sin actualizaciones de precios, costo universal ni listas; aceptar envío de la compra a cuenta proveedor. Datos nuevos pendientes.
- Nombres QA e importes son requisitos públicos de fixtures futuros; no están creados por esta ficha ni garantizados por el seed comercial. Calibración de controles y lecturas por identidad pendientes.
- Definir moneda, concepto, medio, empresa, sucursal, puesto, operador y período antes de ejecutar. No cambiar datos mediante SQL para corregir una operación en curso.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Recibir y confirmar el remito de 10 unidades, aceptando la cuenta corriente del proveedor. | Stock 60 y deuda ARS 1.000. Guardar sólo borrador no satisface este paso. Usar el contrato REM-001. |
| 2 | En Egreso de caja registrar ARS 400, efectivo, concepto de pago y proveedor QA-FIN-P1. | Deuda pendiente ARS 600; salida real de caja ARS 400, fondo ARS 4.600. Stock sigue en 60. |
| 3 | Consultar cuenta proveedor, caja y Libro Diario. | Un pago en cuenta proveedor. La representación de movimiento de caja y la del concepto elegido corresponden al mismo egreso; no sumarlas como ARS 800. Libro Diario predeterminado excluye el concepto movimientoCaja. |
| 4 | Reabrir las consultas y rechazar una segunda operación de pago. | Se conservan deuda ARS 600 y caja ARS 4.600; cancelar no crea pagos ni altera la recepción. |

## Variantes y dependencias

Sin marcar pago a proveedor, un egreso no debe cancelar su deuda. Proveedor distinto no modifica QA-FIN-P1. Comparar aparte con pago manual desde cuenta proveedor: no prometer que produce los mismos registros. Anular recepción se trata en REM-024, sin restauración automática de costos.

Las dependencias sin procedimiento reproducible bloquean la variante. Un resultado observado no se convierte automáticamente en el resultado esperado. La aprobación exige todos los pasos y variantes habilitadas del perfil, identificando cuáles siguen pendientes.

## Evidencia y límites

Registrar importes antes/después, identidad de documentos y deltas de deuda, caja, stock y movimientos relevantes. Cada dominio tiene su alcance: dos representaciones técnicas no acreditan dos movimientos de dinero. Conservar lectura acotada y saneada, sin filas completas, credenciales ni datos privados en el repositorio.

INFO muestra caso y resultado; DEBUG acciones de negocio; TRACE controles, esperas y diagnóstico saneado. Todo fallo incluye paso, esperado, observado y evidencia; causa no determinada si no está demostrada. Un dry-run no acredita estos resultados.

## Recuperación

Cancelar las acciones no confirmadas. Ante persistencia incierta, consultar antes de reintentar y no ejecutar compensaciones improvisadas. Conservar evidencia privada, cerrar sólo procesos propios y restaurar el baseline mediante el procedimiento del laboratorio. La anulación de negocio no reemplaza la restauración técnica de datos.

## Anexo técnico y trazabilidad

Fuente inspeccionada: XGestion2 `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`.
Los tests fuente son insumos de reglas/riesgos, no evidencia de ejecución del JAR.

- `src/ModuloVentas/Vistas/FormEgresoDeCaja.java:299-351`.
- `src/ModuloProveedores/Entidades/CtaCteProveedor.java:57-94`.
- `src/ModuloFinanzas/Vistas/FormLibroDiario.java:355-404`.

Registrar build/SHA256 del JAR, perfil, paquete, fecha, responsable, IDs y reporte privado al validar. Cambios posteriores de fuente obligan a revisar el contrato antes de ejecutar.
