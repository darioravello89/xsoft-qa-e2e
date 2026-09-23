---
{"id":"XG-CAJ-007","title":"Cerrar un turno por el circuito normal y conservar su balance","product":"xgestion","module":"caja","tags":["xgestion","regression","caja","cierre-caja","permisos"],"status":"planned"}
---

# XG-CAJ-007 — Cerrar un turno por el circuito normal y conservar su balance

## Objetivo

Cerrar un turno por el circuito normal y conservar su balance, desde el trabajo de la persona que administra dinero o realiza el cierre.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 4 del roadmap.** Ficha del [mapa de Libro Diario y Caja](../../docs/libro-diario-caja.md). No tiene Robot ni validación real; las variantes integradas necesitan su laboratorio propio.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. JAR identificado por SHA256; sin ejecutar fiscal, bancos, correo, mensajería ni impresoras reales.
- Perfil base: empresa/sucursal/puesto/operador QA identificados, ARS y medios manuales sin integración. El perfil declara turno habilitado o diario, cierre normal/ciego y salida del sistema al cerrar; no cambiar configuración para evitar una comprobación.
- Productos, clientes, proveedores, conceptos, movimientos y turnos de esta ficha son **datos sintéticos pendientes de preparar**. El seed comercial actual no garantiza estos saldos ni identidades. Falta contrato de datos/oráculos, permisos y calibración de pantallas; sin ellos se informa bloqueo.
- Libro Diario y Caja tienen alcances diferentes: conciliar los efectos por origen y contexto; no exigir igual cantidad de filas ni igual saldo entre sus consultas.
- Turno abierto: fondo efectivo $1.000, ventas cobradas efectivo $2.000, transferencia $500, egreso caja efectivo $300. Total operativo esperado $3.200; efectivo físico $2.700/transferencia $500. Cierre ciego OFF, salida automática OFF.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Consultar cierre/balance del turno antes de finalizar. | Muestra componentes y total $3.200; consultar no crea otro cierre. |
| Solicitar Cerrar turno y acreditar operador autorizado. | Confirma el cierre de ese turno una vez; estado pasa a cerrado. |
| Omitir impresión y consultar nuevamente el turno histórico. | Balance conserva fondo/ventas/egreso y total; omitir impresión no reabre el turno. |
| Abrir el siguiente turno con fondo propio declarado. | No arrastra ventas/egresos anteriores como actividad nueva. |

## Variantes y dependencias

Perfil salida automática ON necesita controlar terminación del proceso como comportamiento esperado, no fallo. Consultar un turno abierto y elegir imprimir puede ofrecer finalizarlo: registrar explícitamente aceptar/rechazar, sin asumir que toda impresión es de solo lectura. Impresión física necesita laboratorio específico.

## Evidencia y límites

Registrar identidad completa, fecha/intervalo, importe original y operativo, medio, estado y documento de origen; contrastar interfaz y lecturas acotadas por deltas. No atribuir éxito al cierre de una ventana. Las variantes pendientes de regla, datos o laboratorio quedan bloqueadas y no acreditan el caso completo.

## Recuperación

Conservar evidencia antes de recuperar. Cancelar por interfaz cuando corresponda; ante error financiero comprobar primero qué se guardó y evitar repetición ciega. Restaurar el baseline privado antes de otra variante; no borrar movimientos ni retocar saldos para hacer coincidir el esperado.

## Anexo técnico y trazabilidad

Fuente inspeccionada XGestion2: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas de esa revisión:

- `src/ModuloEmpleados/Vistas/FormAbrirCerrarTurno.java:163-200`.
- `src/ModuloVentas/Vistas/FormCierreDeCaja.java:575-588`.
- `src/ModuloVentas/Vistas/FormCierreDeCaja.java:739-806`.

Las referencias y tests de apoyo no acreditan ejecución E2E ni equivalencia del JAR. Registrar versión del paquete/perfil y evidencia privada saneada. INFO resume, DEBUG muestra pasos y TRACE aporta diagnóstico acotado; ante fallo conservar paso, esperado, observado, categoría y evidencia. Sin prueba causal, indicar causa no determinada. No imprimir credenciales, configuración completa ni filas completas.

