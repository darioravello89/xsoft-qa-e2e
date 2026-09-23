---
{"id":"XG-LDI-006","title":"Respetar el acceso financiero del operador y el contexto autorizado","product":"xgestion","module":"libro-diario","tags":["xgestion","regression","libro-diario","permisos"],"status":"planned"}
---

# XG-LDI-006 — Respetar el acceso financiero del operador y el contexto autorizado

## Objetivo

Respetar el acceso financiero del operador y el contexto autorizado, desde el trabajo de la persona que administra dinero o realiza el cierre.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 4 del roadmap.** Ficha del [mapa de Libro Diario y Caja](../../docs/libro-diario-caja.md). No tiene Robot ni validación real; las variantes integradas necesitan su laboratorio propio.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. JAR identificado por SHA256; sin ejecutar fiscal, bancos, correo, mensajería ni impresoras reales.
- Perfil base: empresa/sucursal/puesto/operador QA identificados, ARS y medios manuales sin integración. El perfil declara turno habilitado o diario, cierre normal/ciego y salida del sistema al cerrar; no cambiar configuración para evitar una comprobación.
- Productos, clientes, proveedores, conceptos, movimientos y turnos de esta ficha son **datos sintéticos pendientes de preparar**. El seed comercial actual no garantiza estos saldos ni identidades. Falta contrato de datos/oráculos, permisos y calibración de pantallas; sin ellos se informa bloqueo.
- Libro Diario y Caja tienen alcances diferentes: conciliar los efectos por origen y contexto; no exigir igual cantidad de filas ni igual saldo entre sus consultas.
- Usuarios sintéticos QA-FIN-SI y QA-FIN-NO; configuración efectiva MenuApp con acceso Finanzas/Libro Diario habilitado y deshabilitado, respectivamente. Empresa con módulo Finanzas habilitado. Movimiento control $100.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Ingresar con QA-FIN-NO y revisar el menú. | Libro Diario no se ofrece según la configuración de acceso; no se ejecuta alta/baja como ese usuario. |
| Cerrar sesión e ingresar con QA-FIN-SI. | Libro Diario queda disponible con el contexto y operador correctos. |
| Registrar ingreso QA de $100 y consultarlo. | Se atribuye al usuario autorizado, sin heredar operador de la sesión anterior. |
| Repetir con empresa cuyo módulo Finanzas esté deshabilitado en perfil preparado. | No se ofrece el circuito deshabilitado; el movimiento control no cambia. |

## Variantes y dependencias

La fuente confirma visibilidad del menú, no permisos granulares separados de lectura/alta/baja. Una variante de solo lectura o supervisor necesita regla aprobada y mecanismo de aplicación antes de automatizar; no asumir que existe. El fixture multicontexto y cambios de sesión permanecen bajo aislamiento del runner.

## Evidencia y límites

Registrar identidad completa, fecha/intervalo, importe original y operativo, medio, estado y documento de origen; contrastar interfaz y lecturas acotadas por deltas. No atribuir éxito al cierre de una ventana. Las variantes pendientes de regla, datos o laboratorio quedan bloqueadas y no acreditan el caso completo.

## Recuperación

Conservar evidencia antes de recuperar. Cancelar por interfaz cuando corresponda; ante error financiero comprobar primero qué se guardó y evitar repetición ciega. Restaurar el baseline privado antes de otra variante; no borrar movimientos ni retocar saldos para hacer coincidir el esperado.

## Anexo técnico y trazabilidad

Fuente inspeccionada XGestion2: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas de esa revisión:

- `src/Utilidades/Utils/MenuUtil.java:18-24`.
- `src/ModuloPrincipal/Vistas/AppXGestion.java:839-841`.
- `src/ModuloPrincipal/Vistas/AppXGestion.java:1480-1482`.
- `src/ModuloPrincipal/Vistas/AppXGestion.java:4080-4088`.

Las referencias y tests de apoyo no acreditan ejecución E2E ni equivalencia del JAR. Registrar versión del paquete/perfil y evidencia privada saneada. INFO resume, DEBUG muestra pasos y TRACE aporta diagnóstico acotado; ante fallo conservar paso, esperado, observado, categoría y evidencia. Sin prueba causal, indicar causa no determinada. No imprimir credenciales, configuración completa ni filas completas.

