---
{"id":"XG-LDI-002","title":"Corregir datos inválidos o cancelar un movimiento antes de guardar","product":"xgestion","module":"libro-diario","tags":["xgestion","regression","libro-diario","recuperacion"],"status":"planned"}
---

# XG-LDI-002 — Corregir datos inválidos o cancelar un movimiento antes de guardar

## Objetivo

Corregir datos inválidos o cancelar un movimiento antes de guardar, desde el trabajo de la persona que administra dinero o realiza el cierre.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 4 del roadmap.** Ficha del [mapa de Libro Diario y Caja](../../docs/libro-diario-caja.md). No tiene Robot ni validación real; las variantes integradas necesitan su laboratorio propio.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. JAR identificado por SHA256; sin ejecutar fiscal, bancos, correo, mensajería ni impresoras reales.
- Perfil base: empresa/sucursal/puesto/operador QA identificados, ARS y medios manuales sin integración. El perfil declara turno habilitado o diario, cierre normal/ciego y salida del sistema al cerrar; no cambiar configuración para evitar una comprobación.
- Productos, clientes, proveedores, conceptos, movimientos y turnos de esta ficha son **datos sintéticos pendientes de preparar**. El seed comercial actual no garantiza estos saldos ni identidades. Falta contrato de datos/oráculos, permisos y calibración de pantallas; sin ellos se informa bloqueo.
- Libro Diario y Caja tienen alcances diferentes: conciliar los efectos por origen y contexto; no exigir igual cantidad de filas ni igual saldo entre sus consultas.
- Formulario nuevo; concepto QA-FIN-INGRESO, medio QA efectivo, descripción QA-LDI-002 y objetivo $100. Baseline sin movimientos con esa referencia.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Intentar guardar omitiendo concepto, medio o descripción en corridas separadas. | Solicita el campo faltante y no registra movimiento. |
| Ingresar importe vacío, no numérico si el control lo permite, cero o negativo. | Se impide la entrada o se rechaza sin movimiento ni alteración de saldo. |
| Completar $100 y cancelar mediante botón o Escape. | No aparece QA-LDI-002 en el listado ni cambia el resumen. |
| Volver a abrir y guardar datos válidos. | Exactamente un ingreso $100; los intentos anteriores no se acumulan. |

## Variantes y dependencias

Tipos ingreso/egreso no admiten concepto del tipo contrario. Sucursal/puesto obligatorios. Cotización USD inválida se prueba en LDI-003; el permiso y la calibración no se reemplazan por editar controles internos.

## Evidencia y límites

Registrar identidad completa, fecha/intervalo, importe original y operativo, medio, estado y documento de origen; contrastar interfaz y lecturas acotadas por deltas. No atribuir éxito al cierre de una ventana. Las variantes pendientes de regla, datos o laboratorio quedan bloqueadas y no acreditan el caso completo.

## Recuperación

Conservar evidencia antes de recuperar. Cancelar por interfaz cuando corresponda; ante error financiero comprobar primero qué se guardó y evitar repetición ciega. Restaurar el baseline privado antes de otra variante; no borrar movimientos ni retocar saldos para hacer coincidir el esperado.

## Anexo técnico y trazabilidad

Fuente inspeccionada XGestion2: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas de esa revisión:

- `src/ModuloFinanzas/Vistas/FormLibroDiarioMovimiento.java:150-179`.
- `src/ModuloFinanzas/Vistas/FormLibroDiarioMovimiento.java:254-296`.

Las referencias y tests de apoyo no acreditan ejecución E2E ni equivalencia del JAR. Registrar versión del paquete/perfil y evidencia privada saneada. INFO resume, DEBUG muestra pasos y TRACE aporta diagnóstico acotado; ante fallo conservar paso, esperado, observado, categoría y evidencia. Sin prueba causal, indicar causa no determinada. No imprimir credenciales, configuración completa ni filas completas.

