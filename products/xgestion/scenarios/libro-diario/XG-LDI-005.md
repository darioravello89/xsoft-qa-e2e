---
{"id":"XG-LDI-005","title":"Anular solo el movimiento seleccionado y conservar su trazabilidad","product":"xgestion","module":"libro-diario","tags":["xgestion","regression","libro-diario","permisos","devoluciones"],"status":"planned"}
---

# XG-LDI-005 — Anular solo el movimiento seleccionado y conservar su trazabilidad

## Objetivo

Anular solo el movimiento seleccionado y conservar su trazabilidad, desde el trabajo de la persona que administra dinero o realiza el cierre.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 4 del roadmap.** Ficha del [mapa de Libro Diario y Caja](../../docs/libro-diario-caja.md). No tiene Robot ni validación real; las variantes integradas necesitan su laboratorio propio.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. JAR identificado por SHA256; sin ejecutar fiscal, bancos, correo, mensajería ni impresoras reales.
- Perfil base: empresa/sucursal/puesto/operador QA identificados, ARS y medios manuales sin integración. El perfil declara turno habilitado o diario, cierre normal/ciego y salida del sistema al cerrar; no cambiar configuración para evitar una comprobación.
- Productos, clientes, proveedores, conceptos, movimientos y turnos de esta ficha son **datos sintéticos pendientes de preparar**. El seed comercial actual no garantiza estos saldos ni identidades. Falta contrato de datos/oráculos, permisos y calibración de pantallas; sin ellos se informa bloqueo.
- Libro Diario y Caja tienen alcances diferentes: conciliar los efectos por origen y contexto; no exigir igual cantidad de filas ni igual saldo entre sus consultas.
- Dos movimientos sintéticos comparten número local 9001 en misma empresa/sucursal pero puestos P1/P2: ingreso $100 y $300. Sus identidades completas difieren. Usuario autorizado, motivo QA-LDI-005. Baseline multicontexto aún pendiente.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Seleccionar el ingreso $100 de P1, pedir eliminar y cancelar. | Ambos movimientos conservan estado y total; no registra anulación. |
| Volver a seleccionar P1 y confirmar con motivo. | Criterio de aceptación: solo P1 queda inactivo; P2 $300 permanece activo e inalterado. |
| Consultar resumen y trazabilidad por identidad completa. | Solo se excluyen $100; se identifica operador/fecha y el motivo por el canal auditable acordado. |
| Recargar o consultar desde P2. | El movimiento de P2 y el resto de efectos de su contexto siguen sin cambios. |

## Variantes y dependencias

Riesgo por reproducir: la baja recibe computadora pero su UPDATE filtra empresa/sucursal/número sin computadora; el parámetro motivo no se usa allí. No se declara bug validado ni se adapta el esperado a esa omisión. Si no existe evidencia auditable del motivo, registrar el faltante; no inventarla en el harness. Anular asiento de origen no sustituye devolución/anulación comercial completa.

## Evidencia y límites

Registrar identidad completa, fecha/intervalo, importe original y operativo, medio, estado y documento de origen; contrastar interfaz y lecturas acotadas por deltas. No atribuir éxito al cierre de una ventana. Las variantes pendientes de regla, datos o laboratorio quedan bloqueadas y no acreditan el caso completo.

## Recuperación

Conservar evidencia antes de recuperar. Cancelar por interfaz cuando corresponda; ante error financiero comprobar primero qué se guardó y evitar repetición ciega. Restaurar el baseline privado antes de otra variante; no borrar movimientos ni retocar saldos para hacer coincidir el esperado.

## Anexo técnico y trazabilidad

Fuente inspeccionada XGestion2: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas de esa revisión:

- `src/ModuloFinanzas/Vistas/FormLibroDiario.java:292-306`.
- `src/ModuloFinanzas/Vistas/FormLibroDiarioEliminar.java:78-104`.
- `src/ModuloFinanzas/Entidades/MovimientoFinanzas.java:382-395`.

Las referencias y tests de apoyo no acreditan ejecución E2E ni equivalencia del JAR. Registrar versión del paquete/perfil y evidencia privada saneada. INFO resume, DEBUG muestra pasos y TRACE aporta diagnóstico acotado; ante fallo conservar paso, esperado, observado, categoría y evidencia. Sin prueba causal, indicar causa no determinada. No imprimir credenciales, configuración completa ni filas completas.

