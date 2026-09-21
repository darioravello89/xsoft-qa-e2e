---
{"id":"XG-INI-001","title":"Inicio muestra acceso","product":"xgestion","module":"inicio","tags":["xgestion","smoke","regression","inicio","lectura"],"status":"implemented","test":"products/xgestion/suites/smoke.robot"}
---

# XG-INI-001 — Inicio muestra acceso

## Objetivo

Al abrir XGestion, la persona encuentra dónde ingresar su usuario y contraseña.

## Estado y perfil

Automatización implementada; **ejecución real pendiente** de paquete privado, calibración y aceptación. Lint y dry-run no acreditan este recorrido en el producto.

- Windows QA exclusivo, offline, escritorio desbloqueado y ejecución serial por el runner.
- Paquete autorizado, licencia QA vigente, base aislada restaurada y selectores calibrados para el SHA-256 del JAR.
- Usuario, empresa, sucursal y computadora QA definidos en el paquete; credenciales locales privadas.
- Datos de consulta y código ausente conocidos, preparados en el paquete saneado.

## Pasos y resultados esperados

1. Iniciar el escenario con el runner. **Esperado:** se abre la instancia de XGestion preparada para QA.
2. Observar la pantalla de acceso. **Esperado:** están disponibles los campos de usuario y contraseña y la acción ENTRAR.

## Recuperación y límites

Si falla, conservar el reporte privado y el paso observado. El runner cierra solo su proceso y prepara el baseline en la siguiente ejecución. No reparar resultados borrando datos ni modificar controles de seguridad. No se inicia sesión ni se comprueba todavía que las credenciales funcionen.

## Evidencia para QA

INFO muestra ID, resultado y resumen; DEBUG añade pasos; TRACE diagnóstico saneado. En cualquier nivel un fallo debe incluir paso, esperado, observado, categoría y evidencia disponible. Si la causa no está demostrada, informar «causa no determinada». Capturas solo de ventanas QA autenticadas, sin credenciales. Registrar versión/hash del JAR, paquete, perfil y ruta privada del reporte.

## Anexo técnico y trazabilidad

El adaptador comprueba los controles accesibles en una ventana del proceso que inició. No captura autenticación. Fuente: AppXGestion.java y Login.java.

La [cobertura](../../docs/cobertura.md) identifica la referencia XGestion2 `release/189-lts`, `f34238183d494259bed1279dd7d9aac0ce16a3ae`. Fuente y tests orientan expectativas; no demuestran equivalencia del JAR ni ejecución real. Se mantienen IDs, tags y archivo Robot existentes.
