---
{"id": "XG-AUT-001", "title": "Credenciales inválidas", "product": "xgestion", "module": "autenticacion", "tags": ["xgestion", "smoke", "regression", "autenticacion", "lectura"], "status": "implemented", "test": "products/xgestion/suites/smoke.robot"}
---

# XG-AUT-001 — Credenciales inválidas

## Precondiciones

Paquete privado, calibración JAB por SHA256 y VM QA offline. Dump restaurado por el runner, usuario/empresa/sucursal/computadora y producto conforme fixtures.json. Escritorio desbloqueado y ejecución serial.

## Pasos y resultados esperados

1. Ingresar usuario y clave inválidos mediante controles UI.
2. Verificar Acceso Invalido; cerrar aviso y comprobar ambos campos vacíos.

## Evidencia y límites

No captura login ni registra credenciales. Implementación disponible; GUI real pendiente hasta aceptar el paquete. Unit tests y dry-run no certifican este resultado.
