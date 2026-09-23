---
{"id":"XG-LDI-007","title":"Recuperar un fallo al guardar sin acreditar éxito ni duplicar el importe","product":"xgestion","module":"libro-diario","tags":["xgestion","regression","libro-diario","recuperacion"],"status":"planned"}
---

# XG-LDI-007 — Recuperar un fallo al guardar sin acreditar éxito ni duplicar el importe

## Objetivo

Recuperar un fallo al guardar sin acreditar éxito ni duplicar el importe, desde el trabajo de la persona que administra dinero o realiza el cierre.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 4 del roadmap.** Ficha del [mapa de Libro Diario y Caja](../../docs/libro-diario-caja.md). No tiene Robot ni validación real; las variantes integradas necesitan su laboratorio propio.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. JAR identificado por SHA256; sin ejecutar fiscal, bancos, correo, mensajería ni impresoras reales.
- Perfil base: empresa/sucursal/puesto/operador QA identificados, ARS y medios manuales sin integración. El perfil declara turno habilitado o diario, cierre normal/ciego y salida del sistema al cerrar; no cambiar configuración para evitar una comprobación.
- Productos, clientes, proveedores, conceptos, movimientos y turnos de esta ficha son **datos sintéticos pendientes de preparar**. El seed comercial actual no garantiza estos saldos ni identidades. Falta contrato de datos/oráculos, permisos y calibración de pantallas; sin ellos se informa bloqueo.
- Libro Diario y Caja tienen alcances diferentes: conciliar los efectos por origen y contexto; no exigir igual cantidad de filas ni igual saldo entre sus consultas.
- Ingreso manual QA-LDI-007 por $100, baseline sin esa referencia. Laboratorio local autorizado capaz de provocar una falla de persistencia reproducible antes del insert y, por separado, resultado ambiguo; todavía pendiente. No interrumpir una base compartida.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Completar el ingreso y activar la falla controlada antes de guardar. | Debe informarse el fallo y no acreditarse éxito por cerrar la ventana. |
| Consultar por identidad/referencia antes de reintentar. | Falla previa al insert: cero movimientos/$0. Resultado ambiguo: determinar si existe uno por $100; si no puede determinarse, bloquear reintento. |
| Retirar la falla y repetir solo si está demostrado que no se registró. | Termina con un único ingreso $100, no dos intentos cobrados. |
| Recargar el listado y revisar evidencia técnica saneada. | Interfaz y persistencia concuerdan; conserva causa observada o causa no determinada. |

## Variantes y dependencias

Reintento por colisión de identificador y error distinto se evalúan por separado. La fuente inserta por un método que puede devolver 0 y la pantalla continúa: riesgo pendiente de reproducción. No asumir atomicidad ni corregir desde SQL los efectos parciales.

## Evidencia y límites

Registrar identidad completa, fecha/intervalo, importe original y operativo, medio, estado y documento de origen; contrastar interfaz y lecturas acotadas por deltas. No atribuir éxito al cierre de una ventana. Las variantes pendientes de regla, datos o laboratorio quedan bloqueadas y no acreditan el caso completo.

## Recuperación

Conservar evidencia antes de recuperar. Cancelar por interfaz cuando corresponda; ante error financiero comprobar primero qué se guardó y evitar repetición ciega. Restaurar el baseline privado antes de otra variante; no borrar movimientos ni retocar saldos para hacer coincidir el esperado.

## Anexo técnico y trazabilidad

Fuente inspeccionada XGestion2: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas de esa revisión:

- `src/ModuloFinanzas/Vistas/FormLibroDiarioMovimiento.java:298-321`.
- `src/ModuloFinanzas/Entidades/MovimientoFinanzas.java:190-237`.
- `test/ModuloFinanzas/Entidades/MovimientoFinanzasInsertPolicyTest.java:14-44`.

Las referencias y tests de apoyo no acreditan ejecución E2E ni equivalencia del JAR. Registrar versión del paquete/perfil y evidencia privada saneada. INFO resume, DEBUG muestra pasos y TRACE aporta diagnóstico acotado; ante fallo conservar paso, esperado, observado, categoría y evidencia. Sin prueba causal, indicar causa no determinada. No imprimir credenciales, configuración completa ni filas completas.

