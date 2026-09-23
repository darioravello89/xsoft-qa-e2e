---
{"id":"XG-CAJ-008","title":"Cerrar a ciegas registrando diferencias sin inventar dinero","product":"xgestion","module":"caja","tags":["xgestion","regression","caja","cierre-caja","permisos"],"status":"planned"}
---

# XG-CAJ-008 — Cerrar a ciegas registrando diferencias sin inventar dinero

## Objetivo

Cerrar a ciegas registrando diferencias sin inventar dinero, desde el trabajo de la persona que administra dinero o realiza el cierre.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 4 del roadmap.** Ficha del [mapa de Libro Diario y Caja](../../docs/libro-diario-caja.md). No tiene Robot ni validación real; las variantes integradas necesitan su laboratorio propio.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. JAR identificado por SHA256; sin ejecutar fiscal, bancos, correo, mensajería ni impresoras reales.
- Perfil base: empresa/sucursal/puesto/operador QA identificados, ARS y medios manuales sin integración. El perfil declara turno habilitado o diario, cierre normal/ciego y salida del sistema al cerrar; no cambiar configuración para evitar una comprobación.
- Productos, clientes, proveedores, conceptos, movimientos y turnos de esta ficha son **datos sintéticos pendientes de preparar**. El seed comercial actual no garantiza estos saldos ni identidades. Falta contrato de datos/oráculos, permisos y calibración de pantallas; sin ellos se informa bloqueo.
- Libro Diario y Caja tienen alcances diferentes: conciliar los efectos por origen y contexto; no exigir igual cantidad de filas ni igual saldo entre sus consultas.
- Turno con efectivo esperado $5.000 y transferencia manual $1.000; total $6.000. Conteo físico: efectivo $4.800 y transferencia $1.000; total $5.800/diferencia -$200. Denominaciones/permisos definidos; transportes de alertas externos deshabilitados o sustituidos por laboratorio autorizado.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Abrir cierre ciego e ingresar conteo propio en cada campo requerido. | Calcula contado a partir de lo ingresado; no rellena importes con el esperado. |
| Completar con cero explícito las denominaciones no utilizadas y confirmar. | Resumen: efectivo contado $4.800/esperado $5.000/diferencia -$200; total contado $5.800/esperado $6.000. |
| Consultar turno y evidencia del cierre. | Un cierre confirmado conserva su conteo y diferencias, sin crear ingreso correctivo para forzar saldo cero. |
| En corridas separadas probar coincidencia y sobrante. | Diferencias $0 y +$200 con los conteos correspondientes; no tratar sobrante como faltante. |

## Variantes y dependencias

Umbrales y tolerancias por medio requieren configuración explícita; no inferir que toda diferencia envía alerta. El envío de correo/WhatsApp está fuera del perfil offline. Variantes USD dependen del oráculo de CAJ-005. El esperado financiero debe ser independiente de lo que el operador contó.

## Evidencia y límites

Registrar identidad completa, fecha/intervalo, importe original y operativo, medio, estado y documento de origen; contrastar interfaz y lecturas acotadas por deltas. No atribuir éxito al cierre de una ventana. Las variantes pendientes de regla, datos o laboratorio quedan bloqueadas y no acreditan el caso completo.

## Recuperación

Conservar evidencia antes de recuperar. Cancelar por interfaz cuando corresponda; ante error financiero comprobar primero qué se guardó y evitar repetición ciega. Restaurar el baseline privado antes de otra variante; no borrar movimientos ni retocar saldos para hacer coincidir el esperado.

## Anexo técnico y trazabilidad

Fuente inspeccionada XGestion2: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas de esa revisión:

- `src/ModuloVentas/Vistas/FormCierreCajaCiego.java:284-336`.
- `src/ModuloVentas/Vistas/FormCierreCajaCiego.java:347-443`.
- `src/ModuloVentas/Vistas/FormCierreCajaCiego.java:630-701`.
- `test/ModuloVentas/Vistas/FormCierreCajaCiegoNotificacionPolicyTest.java:1-67`.

Las referencias y tests de apoyo no acreditan ejecución E2E ni equivalencia del JAR. Registrar versión del paquete/perfil y evidencia privada saneada. INFO resume, DEBUG muestra pasos y TRACE aporta diagnóstico acotado; ante fallo conservar paso, esperado, observado, categoría y evidencia. Sin prueba causal, indicar causa no determinada. No imprimir credenciales, configuración completa ni filas completas.
