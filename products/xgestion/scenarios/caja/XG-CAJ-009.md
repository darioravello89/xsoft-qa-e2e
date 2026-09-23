---
{"id":"XG-CAJ-009","title":"Cancelar o recuperar un cierre fallido sin duplicar sus efectos","product":"xgestion","module":"caja","tags":["xgestion","regression","caja","cierre-caja","recuperacion"],"status":"planned"}
---

# XG-CAJ-009 — Cancelar o recuperar un cierre fallido sin duplicar sus efectos

## Objetivo

Cancelar o recuperar un cierre fallido sin duplicar sus efectos, desde el trabajo de la persona que administra dinero o realiza el cierre.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 4 del roadmap.** Ficha del [mapa de Libro Diario y Caja](../../docs/libro-diario-caja.md). No tiene Robot ni validación real; las variantes integradas necesitan su laboratorio propio.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. JAR identificado por SHA256; sin ejecutar fiscal, bancos, correo, mensajería ni impresoras reales.
- Perfil base: empresa/sucursal/puesto/operador QA identificados, ARS y medios manuales sin integración. El perfil declara turno habilitado o diario, cierre normal/ciego y salida del sistema al cerrar; no cambiar configuración para evitar una comprobación.
- Productos, clientes, proveedores, conceptos, movimientos y turnos de esta ficha son **datos sintéticos pendientes de preparar**. El seed comercial actual no garantiza estos saldos ni identidades. Falta contrato de datos/oráculos, permisos y calibración de pantallas; sin ellos se informa bloqueo.
- Libro Diario y Caja tienen alcances diferentes: conciliar los efectos por origen y contexto; no exigir igual cantidad de filas ni igual saldo entre sus consultas.
- Turno abierto con efectivo esperado $1.000, sin cierres previos. Perfil ciego ON para validaciones y perfil normal separado. Laboratorio pendiente de fallo controlado antes de persistir cierre de turno y fallo de impresión posterior.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Dejar un conteo obligatorio vacío e intentar confirmar. | Se pide completarlo explícitamente; el turno sigue abierto y no aparece cierre confirmado. |
| Completar $1.000, pedir confirmar y responder No; después cancelar el cierre ciego. | Sigue abierto, sin registrar una aceptación ni cambiar balance. |
| Repetir en laboratorio con error al persistir cierre de turno. | No muestra éxito; identifica estado real del turno y cualquier registro de arqueo parcial antes de ofrecer repetir. |
| Retirar fallo, recuperar mediante flujo aprobado y luego simular falla solo de impresión. | Debe terminar con un solo cierre financiero efectivo. Si el turno ya cerró, falla de impresión no lo reabre ni autoriza cobrar/cerrar otra vez. |

## Variantes y dependencias

La fuente guarda movimiento de arqueo antes de cerrar turno: no presumir transacción atómica ni cero registros ante toda falla. El procedimiento para un arqueo parcial debe definirse antes de automatizar reintento; conservar bloqueo si el estado es ambiguo. Controles de procesos/aislamiento no se deshabilitan para inyectar el fallo.

## Evidencia y límites

Registrar identidad completa, fecha/intervalo, importe original y operativo, medio, estado y documento de origen; contrastar interfaz y lecturas acotadas por deltas. No atribuir éxito al cierre de una ventana. Las variantes pendientes de regla, datos o laboratorio quedan bloqueadas y no acreditan el caso completo.

## Recuperación

Conservar evidencia antes de recuperar. Cancelar por interfaz cuando corresponda; ante error financiero comprobar primero qué se guardó y evitar repetición ciega. Restaurar el baseline privado antes de otra variante; no borrar movimientos ni retocar saldos para hacer coincidir el esperado.

## Anexo técnico y trazabilidad

Fuente inspeccionada XGestion2: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas de esa revisión:

- `src/ModuloVentas/Vistas/FormCierreCajaCiego.java:284-336`.
- `src/ModuloVentas/Vistas/FormCierreCajaCiego.java:347-380`.
- `src/ModuloEmpleados/Vistas/FormAbrirCerrarTurno.java:151-191`.
- `src/ModuloVentas/Vistas/FormCierreCajaCiego.java:691-701`.

Las referencias y tests de apoyo no acreditan ejecución E2E ni equivalencia del JAR. Registrar versión del paquete/perfil y evidencia privada saneada. INFO resume, DEBUG muestra pasos y TRACE aporta diagnóstico acotado; ante fallo conservar paso, esperado, observado, categoría y evidencia. Sin prueba causal, indicar causa no determinada. No imprimir credenciales, configuración completa ni filas completas.

