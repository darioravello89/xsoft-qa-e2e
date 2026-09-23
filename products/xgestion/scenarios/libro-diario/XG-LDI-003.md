---
{"id":"XG-LDI-003","title":"Filtrar movimientos y conciliar totales e importes ARS y USD","product":"xgestion","module":"libro-diario","tags":["xgestion","regression","libro-diario","monedas","permisos"],"status":"planned"}
---

# XG-LDI-003 — Filtrar movimientos y conciliar totales e importes ARS y USD

## Objetivo

Filtrar movimientos y conciliar totales e importes ARS y USD, desde el trabajo de la persona que administra dinero o realiza el cierre.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 4 del roadmap.** Ficha del [mapa de Libro Diario y Caja](../../docs/libro-diario-caja.md). No tiene Robot ni validación real; las variantes integradas necesitan su laboratorio propio.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. JAR identificado por SHA256; sin ejecutar fiscal, bancos, correo, mensajería ni impresoras reales.
- Perfil base: empresa/sucursal/puesto/operador QA identificados, ARS y medios manuales sin integración. El perfil declara turno habilitado o diario, cierre normal/ciego y salida del sistema al cerrar; no cambiar configuración para evitar una comprobación.
- Productos, clientes, proveedores, conceptos, movimientos y turnos de esta ficha son **datos sintéticos pendientes de preparar**. El seed comercial actual no garantiza estos saldos ni identidades. Falta contrato de datos/oráculos, permisos y calibración de pantallas; sin ellos se informa bloqueo.
- Libro Diario y Caja tienen alcances diferentes: conciliar los efectos por origen y contexto; no exigir igual cantidad de filas ni igual saldo entre sus consultas.
- Empresa E1/sucursal S1/puesto P1: ingreso ARS $1.000, egreso ARS $250 e ingreso original USD 10 con cotización $1.000 = ARS $10.000, todos hoy. Controles en ayer, otro usuario/medio, P2 $3.000 y empresa E2 $5.000; paquete multicontexto y alcance autorizado todavía pendientes.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Aplicar filtros del conjunto E1/S1/P1/hoy y referencias QA-LDI-003. | Solo el conjunto autorizado; ingresos ARS $11.000, egresos $250, saldo $10.750. |
| Filtrar por medio, concepto, ingreso/egreso y usuario. | Filas y resumen aplican exactamente el mismo filtro, sin arrastrar importes del filtro anterior. |
| Revisar la fila USD y su presentación. | Original USD 10/cotización $1.000 y operativo ARS $10.000; no sumar nominalmente USD 10 a pesos. |
| Crear variante USD con cotización cero/ausente y corregirla a $1.000. | Se rechaza el dato inválido; al corregir se registra una sola conversión y un solo movimiento. |

## Variantes y dependencias

Intervalos vacíos muestran cero sin valores anteriores; fechas límite e historial con moneda nula ARS requieren fixture. La consulta fuente no muestra predicado Empresa en su WHERE: el alcance de empresa debe acordarse y reproducirse con controles antes de acreditar aislamiento. No declarar defecto confirmado por inspección.

## Evidencia y límites

Registrar identidad completa, fecha/intervalo, importe original y operativo, medio, estado y documento de origen; contrastar interfaz y lecturas acotadas por deltas. No atribuir éxito al cierre de una ventana. Las variantes pendientes de regla, datos o laboratorio quedan bloqueadas y no acreditan el caso completo.

## Recuperación

Conservar evidencia antes de recuperar. Cancelar por interfaz cuando corresponda; ante error financiero comprobar primero qué se guardó y evitar repetición ciega. Restaurar el baseline privado antes de otra variante; no borrar movimientos ni retocar saldos para hacer coincidir el esperado.

## Anexo técnico y trazabilidad

Fuente inspeccionada XGestion2: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas de esa revisión:

- `src/ModuloFinanzas/Vistas/FormLibroDiario.java:260-265`.
- `src/ModuloFinanzas/Vistas/FormLibroDiario.java:355-416`.
- `src/ModuloFinanzas/Vistas/FormLibroDiarioMovimiento.java:269-319`.

Las referencias y tests de apoyo no acreditan ejecución E2E ni equivalencia del JAR. Registrar versión del paquete/perfil y evidencia privada saneada. INFO resume, DEBUG muestra pasos y TRACE aporta diagnóstico acotado; ante fallo conservar paso, esperado, observado, categoría y evidencia. Sin prueba causal, indicar causa no determinada. No imprimir credenciales, configuración completa ni filas completas.

