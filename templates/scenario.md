---
{"id":"PROD-MOD-001","title":"Reemplazar por recorrido de usuario","product":"producto","module":"modulo","tags":["regression","modulo"],"status":"planned"}
---

# PROD-MOD-001 — Comportamiento observable

## Objetivo

Describir la capacidad concreta que debe comprobar este caso.

## Estado y alcance

`planned` hasta implementar la automatización. Al pasar a `implemented`, añadir `test` con la ruta al `.robot` y mantener ID/tags coincidentes. La implementación tampoco acredita ejecución real por sí sola. Indicar etapa/familia del roadmap.

## Precondiciones y datos

- Versión del producto y preparación del entorno.
- Identificadores de fixture y estado inicial requerido, sin secretos.
- Efectos permitidos y forma de recuperar el estado inicial.
- Configuración que condiciona el comportamiento y variantes fuera del caso.

## Pasos y resultados esperados

1. Acción del usuario y evidencia observable esperada.
2. Siguiente acción y aserción independiente del resultado obtenido.

## Evidencia y límites

Indicar UI, lectura de persistencia u otra fuente que prueba el resultado. Registrar los aspectos fuera del caso. Implementación del test y ejecución real son hitos diferentes.

## Recuperación

Qué hace el usuario al cancelar/corregir/reintentar y cómo se restaura después el entorno QA. No ocultar fallos mediante limpieza de datos.

## Anexo técnico y trazabilidad

Selectores pendientes/verificados, oráculos de lectura y fuente de la regla. No incluir secretos. Registrar versión/hash JAR, paquete y perfil en la evidencia privada. INFO resume, DEBUG muestra pasos y TRACE añade diagnóstico saneado; un fallo siempre informa esperado/observado, paso, categoría y evidencia, o causa no determinada si no puede demostrarse.
