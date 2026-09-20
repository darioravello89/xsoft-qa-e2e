---
{"id": "XG-PRO-002", "title": "Buscar producto inexistente", "product": "xgestion", "module": "productos", "tags": ["xgestion", "smoke", "regression", "productos", "lectura"], "status": "implemented", "test": "products/xgestion/suites/smoke.robot"}
---

# XG-PRO-002 — Buscar producto inexistente

## Precondiciones

Paquete privado, calibración JAB por SHA256 y VM QA offline. Dump restaurado por el runner, usuario/empresa/sucursal/computadora y producto conforme fixtures.json. Escritorio desbloqueado y ejecución serial.

## Pasos y resultados esperados

1. Ingresar como QA y abrir listado de productos.
2. Buscar código garantizado ausente; afirmar indicador vacío calibrado.

## Evidencia y límites

No confundir un listado anterior o una excepción con cero resultados. Implementación disponible; GUI real pendiente hasta aceptar el paquete. Unit tests y dry-run no certifican este resultado.
