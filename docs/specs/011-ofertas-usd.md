# Ofertas USD: regresión P0

Plan aprobado: cinco casos XG-PRM-080..084 (producto, familia, subfamilia,
marca y sector), trece variantes obligatorias, sin corregir el ERP.

## Contrato comercial

Producto USD 100, oferta LXO+$CU con Paga=50 en moneda del producto,
cotización 1500 ARS/USD, documento interno 99 y cobro ARS, IVA 0.
Una unidad promocionada: bruto ARS 150000, descuento ARS 75000, neto ARS 75000.
Dos unidades: bruto ARS 300000, descuento ARS 150000, neto ARS 150000.
Los importes esperados son datos públicos fijos; nunca provienen del calculador ERP.

Cada alcance tiene variantes desde una y desde dos unidades, agrupación OFF.
Familia, subfamilia y marca agregan mínimo dos con agrupación ON: A1+B1 debe
activar la oferta solo en ON. Hay productos excluidos y categorías independientes
por variante. Se edita 1→2→1, se agregan/retiran productos, se cancela y retoma
el cobro verificando una sola venta y deltas de stock/caja.

## Incrementos

1. Modelo y seed: moneda explícita con ARS por defecto; USD usa ID 2 validado
   contra DOL; nunca convertir Paga=50 a pesos ni modificar monedas globales.
2. Runner: calibración ofertas-usd-v1, renglones USD, total ARS, cotización visible
   1500, tres selectores de moneda de cobro ARS; sin cambiar el perfil para pasar.
   Un perfil faltante o incompatible bloquea; una discrepancia comercial falla.
3. Persistencia: comprobar snapshots originales USD y operativos ARS, moneda
   del comprobante/pago/vuelto, cotización y movimientos mediante SELECT acotados.
4. Catálogo, fichas, grupo ofertas-usd y mapa Excel; validación real pendiente.

## Verificación

Primero pruebas sintéticas negativas (ARS 50, moneda incorrecta, doble conversión,
descuento duplicado, evidencia incompleta), luego implementación y regresión ARS.
Ejecutar `.venv\Scripts\python -m pytest`, Ruff, Robocop, `qa.cmd check`, generador
de documentación `--check`, `qa.cmd coverage --check` y dry-run regression.
Comando real: `qa.cmd run --product xgestion --group ofertas-usd --seed catalogo-comercial-v1`.

Mantener aislamiento, sanitización y trabajo previo del checkout. No commit/push
sin pedido. No declarar validación real sin Windows QA offline, paquete calibrado
y SHA256 del JAR. Fallo o bloqueo P0 impide acreditar aceptación de ofertas.
Presupuestos, listas, otros tipos de oferta, impuestos y cotizaciones adicionales
no quedan acreditados por estos cinco casos.

## Evidencia técnica de implementación — 2026-09-23

- Pytest completo: 807 aprobados, 38 omitidos. Las omisiones corresponden a
  37 pruebas de integración que requieren `XSOFT_SEED_MYSQL_BIN` (MySQL 5.7
  x64 aislado) y una de enlaces simbólicos no permitidos por la cuenta.
  El binario de XAMPP inspeccionado es MariaDB 10.4.32, incompatible con ese
  harness; no se utilizó su servicio ni sus datos.
- Ruff y Robocop sin errores; catálogo: 298 documentados, 96 implementados,
  202 pendientes. Documentación generada: 85 archivos, ninguno desactualizado.
- `qa.cmd coverage --check` correcto. Excel revisado visualmente: PRM-080..084
  con prioridad P0, automatizados y validación real pendiente.
- Dry-run regression: 96 casos únicos validados en seco; reporte local
  `reports/20260923T172339Z-dry-run-9e3893`. No acredita comportamiento del ERP.
- `qa.cmd doctor --product xgestion`: BLOQUEADO por falta del paquete QA
  privado. Aplicación real del seed, calibración, ejecución sobre el JAR y
  registro de su SHA256 quedan pendientes; no hay aceptación real acreditada.
