---
{"id":"XG-AUT-001","title":"Credenciales inválidas","product":"xgestion","module":"autenticacion","tags":["xgestion","smoke","regression","autenticacion","lectura"],"status":"implemented","test":"products/xgestion/suites/smoke.robot"}
---

# XG-AUT-001 — Credenciales inválidas

## Objetivo

La persona recibe un aviso al intentar entrar con datos inválidos y puede volver a intentarlo.

## Estado y perfil

Automatización implementada; **ejecución real pendiente** de paquete privado, calibración y aceptación. Lint y dry-run no acreditan este recorrido en el producto.

- Windows QA exclusivo, offline, escritorio desbloqueado y ejecución serial por el runner.
- Paquete autorizado, licencia QA vigente, base aislada restaurada y selectores calibrados para el SHA-256 del JAR.
- Usuario, empresa, sucursal y computadora QA definidos en el paquete; credenciales locales privadas.
- Datos de consulta y código ausente conocidos, preparados en el paquete saneado.

## Pasos y resultados esperados

1. Abrir la pantalla de acceso. **Esperado:** aparecen los campos de usuario y contraseña.
2. Ingresar los datos sintéticos inválidos y pulsar ENTRAR. **Esperado:** aparece «Acceso Invalido» sin acceder a la pantalla principal.
3. Cerrar el aviso. **Esperado:** ambos campos quedan vacíos.

## Recuperación y límites

Si falla, conservar el reporte privado y el paso observado. El runner cierra solo su proceso y prepara el baseline en la siguiente ejecución. No reparar resultados borrando datos ni modificar controles de seguridad. No usar una cuenta real para provocar fallos repetidos. No registrar valores ni capturar login.

## Evidencia para QA

INFO muestra ID, resultado y resumen; DEBUG añade pasos; TRACE diagnóstico saneado. En cualquier nivel un fallo debe incluir paso, esperado, observado, categoría y evidencia disponible. Si la causa no está demostrada, informar «causa no determinada». Capturas solo de ventanas QA autenticadas, sin credenciales. Registrar versión/hash del JAR, paquete, perfil y ruta privada del reporte.

## Anexo técnico y trazabilidad

La automatización usa datos inválidos sintéticos y verifica el texto y vaciado de campos. Fuente: Login.java.

La [cobertura](../../docs/cobertura.md) identifica la referencia XGestion2 `release/189-lts`, `f34238183d494259bed1279dd7d9aac0ce16a3ae`. Fuente y tests orientan expectativas; no demuestran equivalencia del JAR ni ejecución real. Se mantienen IDs, tags y archivo Robot existentes.
