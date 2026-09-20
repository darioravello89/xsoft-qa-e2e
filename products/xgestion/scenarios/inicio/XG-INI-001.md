---
{"id": "XG-INI-001", "title": "Inicio muestra acceso", "product": "xgestion", "module": "inicio", "tags": ["xgestion", "smoke", "regression", "inicio", "lectura"], "status": "implemented", "test": "products/xgestion/suites/smoke.robot"}
---

# XG-INI-001 — Inicio muestra acceso

## Precondiciones

Paquete privado, calibración JAB por SHA256 y VM QA offline. Dump restaurado por el runner, usuario/empresa/sucursal/computadora y producto conforme fixtures.json. Escritorio desbloqueado y ejecución serial.

## Pasos y resultados esperados

1. Arrancar el JAR desde el runner.
2. Esperar la ventana de login del PID propio y verificar usuario, contraseña y ENTRAR accesibles.

## Evidencia y límites

No conecta otra instalación ni elige controles por coordenadas. Implementación disponible; GUI real pendiente hasta aceptar el paquete. Unit tests y dry-run no certifican este resultado.
