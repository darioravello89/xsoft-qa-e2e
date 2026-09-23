---
{"id":"XG-CAJ-010","title":"Reimprimir el cierre guardado sin recalcularlo con operaciones nuevas","product":"xgestion","module":"caja","tags":["xgestion","regression","caja","cierre-caja","impresion","comprobantes"],"status":"planned"}
---

# XG-CAJ-010 — Reimprimir el cierre guardado sin recalcularlo con operaciones nuevas

## Objetivo

Reimprimir el cierre guardado sin recalcularlo con operaciones nuevas, desde el trabajo de la persona que administra dinero o realiza el cierre.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 4 del roadmap.** Ficha del [mapa de Libro Diario y Caja](../../docs/libro-diario-caja.md). No tiene Robot ni validación real; las variantes integradas necesitan su laboratorio propio.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. JAR identificado por SHA256; sin ejecutar fiscal, bancos, correo, mensajería ni impresoras reales.
- Perfil base: empresa/sucursal/puesto/operador QA identificados, ARS y medios manuales sin integración. El perfil declara turno habilitado o diario, cierre normal/ciego y salida del sistema al cerrar; no cambiar configuración para evitar una comprobación.
- Productos, clientes, proveedores, conceptos, movimientos y turnos de esta ficha son **datos sintéticos pendientes de preparar**. El seed comercial actual no garantiza estos saldos ni identidades. Falta contrato de datos/oráculos, permisos y calibración de pantallas; sin ellos se informa bloqueo.
- Libro Diario y Caja tienen alcances diferentes: conciliar los efectos por origen y contexto; no exigir igual cantidad de filas ni igual saldo entre sus consultas.
- Cierre ciego confirmado con snapshot: contado/esperado ARS $1.000, diferencia $0, turno y fecha conocidos. Operaciones posteriores de otro turno por $500. Dispositivo de pruebas o salida controlada autorizada pendiente; no imprimir en un comercio real.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Pedir reimprimir el último cierre y cancelar. | No genera cierre/movimiento ni salida. |
| Aceptar reimpresión de la caja seleccionada. | Usa snapshot del cierre $1.000, con identidad/fecha y leyenda REIMPRESION; no suma los $500 posteriores. |
| Provocar fallo de impresión controlado, reintentar y luego cancelar en variante separada. | Solo cambia el intento de salida; no crea otro arqueo/cierre ni altera dinero. |
| Probar baseline sin cierre o snapshot inválido/no reconstruible. | Informa indisponibilidad; no inventa valores esperados desde saldos actuales. |

## Variantes y dependencias

Legacy solo efectivo puede reconstruirse si importes son consistentes; legacy con medios no efectivo carece de detalle suficiente y se rechaza. El servicio recupera último cierre de esta terminal, no cualquier cierre arbitrario. Requiere laboratorio de impresión; que exista ficha no habilita dispositivo/red.

## Evidencia y límites

Registrar identidad completa, fecha/intervalo, importe original y operativo, medio, estado y documento de origen; contrastar interfaz y lecturas acotadas por deltas. No atribuir éxito al cierre de una ventana. Las variantes pendientes de regla, datos o laboratorio quedan bloqueadas y no acreditan el caso completo.

## Recuperación

Conservar evidencia antes de recuperar. Cancelar por interfaz cuando corresponda; ante error financiero comprobar primero qué se guardó y evitar repetición ciega. Restaurar el baseline privado antes de otra variante; no borrar movimientos ni retocar saldos para hacer coincidir el esperado.

## Anexo técnico y trazabilidad

Fuente inspeccionada XGestion2: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas de esa revisión:

- `src/ModuloVentas/Servicios/CierreCajaCiegoReimpresionService.java:30-128`.
- `src/ModuloVentas/Vistas/FormCierreCajaCiego.java:691-701`.
- `test/ModuloVentas/Servicios/CierreCajaCiegoReimpresionServiceTest.java:17-52`.

Las referencias y tests de apoyo no acreditan ejecución E2E ni equivalencia del JAR. Registrar versión del paquete/perfil y evidencia privada saneada. INFO resume, DEBUG muestra pasos y TRACE aporta diagnóstico acotado; ante fallo conservar paso, esperado, observado, categoría y evidencia. Sin prueba causal, indicar causa no determinada. No imprimir credenciales, configuración completa ni filas completas.

