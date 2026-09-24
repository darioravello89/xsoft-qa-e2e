# Circuitos completos: producto, venta, deuda, dinero y cierre

## Objetivo y contrato

Pedido del 2026-09-24: seguir productos ARS/USD desde la compra hasta la venta,
su stock, Libro Diario, cuenta corriente y cierre de caja. Conservar los IDs
existentes y distinguir recorridos parciales de circuitos completos.
La PC del usuario todavía no tiene VM ni paquete privado QA.

Fuente ERP inspeccionada: `0adea394095e4ceff54344bf38cbf21b7c01a5e8`.
Los esperados son criterios comerciales independientes; el código fuente
documenta puntos de entrada y persistencia, no acredita ejecución del JAR.

- Venta cobrada: un documento, salida de stock por cantidad base y entrada
  por el neto cobrado. Conservar moneda del artículo, documento y cobro.
- Venta a cuenta corriente: salida de stock una sola vez, cargo y anticipo
  del cliente correcto; dinero sólo por lo recibido. Un abono posterior
  reduce deuda y registra cobro sin crear otra venta ni restar stock.
- Compra recibida: entrada de stock sólo para renglones recibidos con Suma
  stock; costos según flags y moneda; precio de venta fijo se conserva,
  precio calculado cambia según margen. Borrador no equivale a recepción.
- Cierre: período, empresa/sucursal/puesto/operador y medios correctos.
  No sumar como efectivo todos los registros de movimientos_finanzas ni
  registrar el cobro de una deuda anterior como venta del turno actual.
- Cada confirmación necesita evidencia por identidad completa y deltas.
  Cancelar/reabrir no debe duplicar venta, recepción, deuda ni dinero.

## Datos y variantes

Perfil inicial sin impuestos, promociones, listas ni financiación, cotización
1500 ARS/USD. Separar producto USD de documento USD: vender un producto USD
en comprobante ARS no acredita cuenta corriente USD ni cobro en USD.

Extender `catalogo-comercial-v1` con productos propios QA-CIR: ARS/USD a
precio fijo y calculado, fracción USD, bulto USD, servicio USD y control.
Reutilizar las unidades y monedas existentes; no modificar catálogos globales.
Clientes, turnos y saldos se preparan en el paquete privado o mediante una
extensión verificada; no inventar identidades ni saldos a partir del observado.

## Implementación por incrementos

1. Comparar la cobertura y registrar flujos, checkpoints, variantes pendientes
   y productos disponibles/faltantes, con importes reproducibles.
2. Agregar los productos fijos con claves/identidades reservadas al motor de
   upserts existente. Probar aislamiento, monedas, flags y no colisión.
3. Actualizar fichas, grupos, README y mapa JSON/Excel. Un flujo documentado
   no cambia a implemented hasta tener acciones de UI y oráculos completos.
4. Preparar guía de primera ejecución: VM/PC dedicada, paquete privado,
   setup, snapshot, aislamiento, doctor, calibración, smoke y grupos disponibles.
5. Implementar automatización de nuevas pantallas sólo con contrato de datos
   y acciones sustentado por fuente/paquete; calibración y aceptación real
   requieren el JAR y el escritorio QA. No asumir selector ni modo de cierre.

## Herramientas y validación

Python/Robot/Java Access Bridge y el runner `qa.cmd` existentes, sin nuevas
dependencias ni modificaciones del ERP. Código Python con importaciones
explícitas y Decimal para importes; fixtures públicos sin secretos.

Tests en `tests/`, seed en `products/xgestion/seeds/`, fichas en
`products/xgestion/scenarios/` y documentación en `products/xgestion/docs/`.
Ejecutar Ruff, Robocop, pytest, `qa.cmd check`, `qa.cmd seed --dry-run`,
`qa.cmd coverage --check` y dry-run de regression. Revisar Excel generado.

## Límites y aceptación

No aplicar seeds a la instalación cotidiana ni a una DB compartida. Sin
fiscal, servicios externos o impresoras físicas. Abrir/Cerrar Turno persiste
el cierre y abre FormCierreDeCaja(false): se verifican los totales y se sale
con Escape, sin imprimir. Configurar ventas.cerrarSistemaConCierreDeTurno=false.
No convertir una falta de laboratorio en resultado aprobado.

El usuario confirmó implementar las pantallas. FIN-011/013/014 automatizan
venta, remito y cierre; FIN-012 queda planned por decisión explícita del usuario:
no autoriza doble clic para abrir la cuenta del cliente. ACC-010 requiere un
atajo o botón antes de automatizar ese acceso; no se sustituye por una API/SQL.

Conservar explícitamente pendientes: otras cotizaciones, impuestos,
descuentos/listas, USD como moneda del documento/deuda/cobro, anulación,
recepción parcial, fallos transaccionales, otros contextos y concurrencia.
No commit/push sin pedido. No modificar scripts de aislamiento para operar
en esta PC de trabajo. La primera ejecución real queda condicionada a
preparar el ambiente que el usuario confirmó ausente.

## Verificación de la entrega — 2026-09-24

- Ruff y Robocop: sin errores. No existe package.json; no hay scripts npm aplicables.
- Pytest completo: **864 passed, 38 skipped**. Omisiones: integración MySQL
  opt-in sin binario QA configurado y un control de symlink no soportado por la cuenta.
- Catálogo: 302 documentados, 99 implementados, 203 pendientes, 0 manuales.
- Documentación generada de ofertas: 85 archivos, ninguno desactualizado.
- Seed offline: 395 artículos, 163 ofertas, nueve listas, 1424 filas en 13 tablas.
  Vista previa; no acredita aplicación real de upserts en MySQL.
- Dry-run regression: 99 VALIDADO EN SECO. Dry-run circuitos-completos: 3.
- Excel/JSON/manifiesto vigentes; resumen y cuatro filas FIN inspeccionadas.
- Doctor: BLOQUEADO por paquete privado ausente. No se ejecutó JAR ni E2E real;
  calibración, VM, MySQL y aceptación del producto permanecen pendientes.

La revisión agregó rechazo de perfil mal formado, columnas monetarias faltantes
y evidencia incompleta de productos de control. Las pruebas sintéticas cubren
recepción duplicada, deuda sin stock, monedas/cotización, costos y precios fijos,
cobro único, controles excluidos, cancelación y cierre asociado sin repetir dinero.
