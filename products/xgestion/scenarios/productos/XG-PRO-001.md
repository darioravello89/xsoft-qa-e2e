---
{"id": "XG-PRO-001", "title": "Buscar producto conocido", "product": "xgestion", "module": "productos", "tags": ["xgestion", "smoke", "regression", "productos", "lectura"], "status": "implemented", "test": "products/xgestion/suites/smoke.robot"}
---

# XG-PRO-001 — Buscar producto conocido

## Precondiciones

Paquete privado, calibración JAB por SHA256 y VM QA offline. Dump restaurado por el runner, usuario/empresa/sucursal/computadora y producto conforme fixtures.json. Escritorio desbloqueado y ejecución serial.

## Pasos y resultados esperados

1. Ingresar como QA y abrir Productos → Listado de Productos.
2. Buscar el código fixture y afirmar el nombre exacto de su resultado.

## Evidencia y límites

Resultado visible y captura; no modifica el artículo. Implementación disponible; GUI real pendiente hasta aceptar el paquete. Unit tests y dry-run no certifican este resultado.
