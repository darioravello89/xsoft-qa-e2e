---
{"id": "XG-VEN-002", "title": "Cancelar venta sin persistir", "product": "xgestion", "module": "ventas", "tags": ["xgestion", "regression", "ventas", "escritura"], "status": "implemented", "test": "products/xgestion/suites/ventas.robot"}
---

# XG-VEN-002 — Cancelar venta sin persistir

## Precondiciones

Paquete privado, calibración JAB por SHA256 y VM QA offline. Dump restaurado por el runner, usuario/empresa/sucursal/computadora y producto conforme fixtures.json. Escritorio desbloqueado y ejecución serial.

## Pasos y resultados esperados

1. Ingresar como QA; tomar snapshot SQL antes de abrir la venta.
2. Cargar dos unidades y comprobar total 2000 ARS.
3. Cancelar la venta y confirmar descarte en UI.
4. Comprobar cierre del formulario y mismos IDs de ventas, stock y caja que antes.

## Evidencia y límites

No anular ni borrar registros por SQL. Independiente de XG-VEN-001. Implementación disponible; GUI real pendiente hasta aceptar el paquete. Unit tests y dry-run no certifican este resultado.
