---
{"id":"XG-CAJ-001","title":"Abrir turno y registrar el fondo inicial una sola vez","product":"xgestion","module":"caja","tags":["xgestion","regression","caja","permisos"],"status":"planned"}
---

# XG-CAJ-001 — Abrir turno y registrar el fondo inicial una sola vez

## Objetivo

Abrir turno y registrar el fondo inicial una sola vez, desde el trabajo de la persona que administra dinero o realiza el cierre.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 4 del roadmap.** Ficha del [mapa de Libro Diario y Caja](../../docs/libro-diario-caja.md). No tiene Robot ni validación real; las variantes integradas necesitan su laboratorio propio.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. JAR identificado por SHA256; sin ejecutar fiscal, bancos, correo, mensajería ni impresoras reales.
- Perfil base: empresa/sucursal/puesto/operador QA identificados, ARS y medios manuales sin integración. El perfil declara turno habilitado o diario, cierre normal/ciego y salida del sistema al cerrar; no cambiar configuración para evitar una comprobación.
- Productos, clientes, proveedores, conceptos, movimientos y turnos de esta ficha son **datos sintéticos pendientes de preparar**. El seed comercial actual no garantiza estos saldos ni identidades. Falta contrato de datos/oráculos, permisos y calibración de pantallas; sin ellos se informa bloqueo.
- Libro Diario y Caja tienen alcances diferentes: conciliar los efectos por origen y contexto; no exigir igual cantidad de filas ni igual saldo entre sus consultas.
- Caja QA sin turno abierto ni movimientos del día; operador autorizado. Apertura con fondo ARS $5.000 en efectivo, Contabiliza deshabilitado. Cierre por turno ON y salida automática del sistema OFF declarados en perfil.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Abrir turno mediante la acción y acceso del operador QA. | Queda identificado el turno/puesto/operador y se solicita ingreso de cambio. |
| Informar fondo $5.000 y confirmar. | Un ingreso de caja de $5.000; no se registra una venta ni se crea deuda de cliente/proveedor. |
| Consultar turno y balance. | Fondo/total esperado de caja $5.000 para ese contexto; la recaudación de ventas sigue en cero. |
| Volver a consultar sin repetir la apertura. | No crea otro turno ni duplica el fondo. |

## Variantes y dependencias

La fuente abre turno antes de mostrar ingreso de cambio: no asumir que cerrar o interrumpir ese diálogo revierte la apertura. Variante fondo cero requiere declarar aceptación operativa; no tratar cero como prueba fallida por regla de otro formulario. Históricos/otros puestos necesitan controles separados.

## Evidencia y límites

Registrar identidad completa, fecha/intervalo, importe original y operativo, medio, estado y documento de origen; contrastar interfaz y lecturas acotadas por deltas. No atribuir éxito al cierre de una ventana. Las variantes pendientes de regla, datos o laboratorio quedan bloqueadas y no acreditan el caso completo.

## Recuperación

Conservar evidencia antes de recuperar. Cancelar por interfaz cuando corresponda; ante error financiero comprobar primero qué se guardó y evitar repetición ciega. Restaurar el baseline privado antes de otra variante; no borrar movimientos ni retocar saldos para hacer coincidir el esperado.

## Anexo técnico y trazabilidad

Fuente inspeccionada XGestion2: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas de esa revisión:

- `src/ModuloEmpleados/Vistas/FormAbrirCerrarTurno.java:201-211`.
- `src/ModuloVentas/Vistas/FormIngresoDeCaja.java:104-150`.
- `src/ModuloVentas/Vistas/FormIngresoDeCaja.java:339-347`.
- `src/ModuloVentas/Entidades/CajaValores.java:224-268`.

Las referencias y tests de apoyo no acreditan ejecución E2E ni equivalencia del JAR. Registrar versión del paquete/perfil y evidencia privada saneada. INFO resume, DEBUG muestra pasos y TRACE aporta diagnóstico acotado; ante fallo conservar paso, esperado, observado, categoría y evidencia. Sin prueba causal, indicar causa no determinada. No imprimir credenciales, configuración completa ni filas completas.

