---
{"id":"XG-LDI-001","title":"Registrar ingreso y egreso manual con concepto y medio correctos","product":"xgestion","module":"libro-diario","tags":["xgestion","regression","libro-diario","cobros"],"status":"planned"}
---

# XG-LDI-001 — Registrar ingreso y egreso manual con concepto y medio correctos

## Objetivo

Registrar ingreso y egreso manual con concepto y medio correctos, desde el trabajo de la persona que administra dinero o realiza el cierre.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 4 del roadmap.** Ficha del [mapa de Libro Diario y Caja](../../docs/libro-diario-caja.md). No tiene Robot ni validación real; las variantes integradas necesitan su laboratorio propio.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. JAR identificado por SHA256; sin ejecutar fiscal, bancos, correo, mensajería ni impresoras reales.
- Perfil base: empresa/sucursal/puesto/operador QA identificados, ARS y medios manuales sin integración. El perfil declara turno habilitado o diario, cierre normal/ciego y salida del sistema al cerrar; no cambiar configuración para evitar una comprobación.
- Productos, clientes, proveedores, conceptos, movimientos y turnos de esta ficha son **datos sintéticos pendientes de preparar**. El seed comercial actual no garantiza estos saldos ni identidades. Falta contrato de datos/oráculos, permisos y calibración de pantallas; sin ellos se informa bloqueo.
- Libro Diario y Caja tienen alcances diferentes: conciliar los efectos por origen y contexto; no exigir igual cantidad de filas ni igual saldo entre sus consultas.
- Conceptos propios QA-FIN-INGRESO y QA-FIN-EGRESO activos y compatibles con su tipo; medio manual QA efectivo. Saldo inicial del filtro $0. Crear ingreso $1.000,25 y egreso $250,10, descripciones únicas QA-LDI-001-I/E.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Abrir Ingreso, completar fecha/contexto/concepto/medio y $1.000,25; guardar. | Un ingreso visible de $1.000,25, egreso cero y contexto seleccionado. |
| Abrir Egreso por $250,10 con su concepto compatible. | Un egreso visible de $250,10 y ningún ingreso invertido. |
| Filtrar ambas referencias y revisar resumen. | Ingresos $1.000,25; egresos $250,10; saldo $750,15. |
| Salir y volver a consultar. | Persisten ambas identidades una sola vez, sin duplicarse por recargar. |

## Variantes y dependencias

Repetir coma/punto decimal y cambio de sucursal/puesto con fixtures autorizados. Los conceptos manuales se definen fuera de caja/venta/servicio; no se espera que este registro aislado modifique caja operativa ni deuda.

## Evidencia y límites

Registrar identidad completa, fecha/intervalo, importe original y operativo, medio, estado y documento de origen; contrastar interfaz y lecturas acotadas por deltas. No atribuir éxito al cierre de una ventana. Las variantes pendientes de regla, datos o laboratorio quedan bloqueadas y no acreditan el caso completo.

## Recuperación

Conservar evidencia antes de recuperar. Cancelar por interfaz cuando corresponda; ante error financiero comprobar primero qué se guardó y evitar repetición ciega. Restaurar el baseline privado antes de otra variante; no borrar movimientos ni retocar saldos para hacer coincidir el esperado.

## Anexo técnico y trazabilidad

Fuente inspeccionada XGestion2: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas de esa revisión:

- `src/ModuloFinanzas/Vistas/FormLibroDiarioMovimiento.java:200-247`.
- `src/ModuloFinanzas/Vistas/FormLibroDiarioMovimiento.java:254-321`.
- `src/ModuloFinanzas/Vistas/FormLibroDiario.java:368-416`.

Las referencias y tests de apoyo no acreditan ejecución E2E ni equivalencia del JAR. Registrar versión del paquete/perfil y evidencia privada saneada. INFO resume, DEBUG muestra pasos y TRACE aporta diagnóstico acotado; ante fallo conservar paso, esperado, observado, categoría y evidencia. Sin prueba causal, indicar causa no determinada. No imprimir credenciales, configuración completa ni filas completas.

