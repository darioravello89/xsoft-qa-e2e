---
{"id": "XG-VEN-001", "title": "Venta no fiscal en efectivo", "product": "xgestion", "module": "ventas", "tags": ["xgestion", "regression", "ventas", "escritura"], "status": "implemented", "test": "products/xgestion/suites/ventas.robot"}
---

# XG-VEN-001 — Venta no fiscal en efectivo

## Precondiciones

Paquete privado, calibración JAB por SHA256 y VM QA offline. Dump restaurado por el runner, usuario/empresa/sucursal/computadora y producto conforme fixtures.json. Escritorio desbloqueado y ejecución serial.

## Pasos y resultados esperados

1. Ingresar como QA; tomar snapshot SQL de ventas, stock y caja.
2. Abrir Nueva venta y elegir comprobante interno99 no fiscal; cargar dos unidades del fixture.
3. Verificar total UI 2000 ARS; Cerrar, seleccionar efectivo y cobrar2000.
4. Verificar exactamente una venta nueva cerrada y activa por PK completa, detalle correcto, cobro inmediato, sin CAE, stock −2 y caja +2000.

## Evidencia y límites

Venta real persistida en instancia aislada. No emitir F9, imprimir ni usar pagos externos. Implementación disponible; GUI real pendiente hasta aceptar el paquete. Unit tests y dry-run no certifican este resultado.
