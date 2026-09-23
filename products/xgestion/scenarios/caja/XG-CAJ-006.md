---
{"id":"XG-CAJ-006","title":"Seleccionar el turno y puesto correctos aunque cruce medianoche","product":"xgestion","module":"caja","tags":["xgestion","regression","caja","cierre-caja","varios-puestos","permisos"],"status":"planned"}
---

# XG-CAJ-006 — Seleccionar el turno y puesto correctos aunque cruce medianoche

## Objetivo

Seleccionar el turno y puesto correctos aunque cruce medianoche, desde el trabajo de la persona que administra dinero o realiza el cierre.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 4 del roadmap.** Ficha del [mapa de Libro Diario y Caja](../../docs/libro-diario-caja.md). No tiene Robot ni validación real; las variantes integradas necesitan su laboratorio propio.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. JAR identificado por SHA256; sin ejecutar fiscal, bancos, correo, mensajería ni impresoras reales.
- Perfil base: empresa/sucursal/puesto/operador QA identificados, ARS y medios manuales sin integración. El perfil declara turno habilitado o diario, cierre normal/ciego y salida del sistema al cerrar; no cambiar configuración para evitar una comprobación.
- Productos, clientes, proveedores, conceptos, movimientos y turnos de esta ficha son **datos sintéticos pendientes de preparar**. El seed comercial actual no garantiza estos saldos ni identidades. Falta contrato de datos/oráculos, permisos y calibración de pantallas; sin ellos se informa bloqueo.
- Libro Diario y Caja tienen alcances diferentes: conciliar los efectos por origen y contexto; no exigir igual cantidad de filas ni igual saldo entre sus consultas.
- Turno histórico QA de S1/P1: 22/09/2026 22:00 a 23/09/2026 02:00. Ventas $1.000 a 23:00 y $300 a 01:00. Controles $400 antes de abrir, $200 después de cerrar y $900 en P2 durante el intervalo. Fondo cero, sin otros movimientos.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Elegir S1/P1 y buscar el turno por fecha de apertura. | Se identifica el mismo turno y sus límites completos. |
| Buscarlo por fecha de cierre del día siguiente. | Sigue disponible; no se pierde por cruzar medianoche. |
| Consultar balance y categorías del turno. | Ventas $1.300; excluye $400/$200 fuera de intervalo y $900 del otro puesto. |
| Cambiar a P2 y luego volver a P1. | Cada selección usa su identidad completa y recalcula sin arrastrar cifras. |

## Variantes y dependencias

Variante sin turnos: cierre diario filtrado por usuario seleccionado. Dos sucursales con mismo número de PC prueban valor compuesto. Exactamente en límites requiere timestamps y política inclusiva declarados en fixture. Paquete multicontexto y turnos históricos pendiente; no cambiar reloj de una instalación cotidiana.

## Evidencia y límites

Registrar identidad completa, fecha/intervalo, importe original y operativo, medio, estado y documento de origen; contrastar interfaz y lecturas acotadas por deltas. No atribuir éxito al cierre de una ventana. Las variantes pendientes de regla, datos o laboratorio quedan bloqueadas y no acreditan el caso completo.

## Recuperación

Conservar evidencia antes de recuperar. Cancelar por interfaz cuando corresponda; ante error financiero comprobar primero qué se guardó y evitar repetición ciega. Restaurar el baseline privado antes de otra variante; no borrar movimientos ni retocar saldos para hacer coincidir el esperado.

## Anexo técnico y trazabilidad

Fuente inspeccionada XGestion2: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas de esa revisión:

- `src/ModuloVentas/Vistas/FormCierreDeCaja.java:739-806`.
- `src/ModuloVentas/Entidades/CajaValores.java:176-220`.
- `test/ModuloVentas/Entidades/TurnoCajaSqlBuilderTest.java:13-51`.
- `test/ModuloVentas/Vistas/FormCierreDeCajaComputadoraSeleccionadaTest.java:10-24`.
- `test/ModuloVentas/Servicios/CierreCajaCategoriasServiceTest.java:52-103`.

Las referencias y tests de apoyo no acreditan ejecución E2E ni equivalencia del JAR. Registrar versión del paquete/perfil y evidencia privada saneada. INFO resume, DEBUG muestra pasos y TRACE aporta diagnóstico acotado; ante fallo conservar paso, esperado, observado, categoría y evidencia. Sin prueba causal, indicar causa no determinada. No imprimir credenciales, configuración completa ni filas completas.

