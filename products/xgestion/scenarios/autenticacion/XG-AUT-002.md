---
{"id": "XG-AUT-002", "title": "Login y contexto QA", "product": "xgestion", "module": "autenticacion", "tags": ["xgestion", "smoke", "regression", "autenticacion", "lectura"], "status": "implemented", "test": "products/xgestion/suites/smoke.robot"}
---

# XG-AUT-002 — Login y contexto QA

## Precondiciones

Paquete privado, calibración JAB por SHA256 y VM QA offline. Dump restaurado por el runner, usuario/empresa/sucursal/computadora y producto conforme fixtures.json. Escritorio desbloqueado y ejecución serial.

## Pasos y resultados esperados

1. Ingresar con las credenciales locales del usuario QA.
2. Verificar textos exactos de empresa, sucursal y usuario.

## Evidencia y límites

Captura posterior a autenticación; el contexto debe coincidir con el fixture. Implementación disponible; GUI real pendiente hasta aceptar el paquete. Unit tests y dry-run no certifican este resultado.
