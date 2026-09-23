---
{"id":"XG-CAJ-004","title":"Pagar a un proveedor desde caja y reducir solo su deuda","product":"xgestion","module":"caja","tags":["xgestion","regression","caja","cuenta-corriente","cobros"],"status":"planned"}
---

# XG-CAJ-004 — Pagar a un proveedor desde caja y reducir solo su deuda

## Objetivo

Pagar a un proveedor desde caja y reducir solo su deuda, desde el trabajo de la persona que administra dinero o realiza el cierre.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 4 del roadmap.** Ficha del [mapa de Libro Diario y Caja](../../docs/libro-diario-caja.md). No tiene Robot ni validación real; las variantes integradas necesitan su laboratorio propio.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. JAR identificado por SHA256; sin ejecutar fiscal, bancos, correo, mensajería ni impresoras reales.
- Perfil base: empresa/sucursal/puesto/operador QA identificados, ARS y medios manuales sin integración. El perfil declara turno habilitado o diario, cierre normal/ciego y salida del sistema al cerrar; no cambiar configuración para evitar una comprobación.
- Productos, clientes, proveedores, conceptos, movimientos y turnos de esta ficha son **datos sintéticos pendientes de preparar**. El seed comercial actual no garantiza estos saldos ni identidades. Falta contrato de datos/oráculos, permisos y calibración de pantallas; sin ellos se informa bloqueo.
- Libro Diario y Caja tienen alcances diferentes: conciliar los efectos por origen y contexto; no exigir igual cantidad de filas ni igual saldo entre sus consultas.
- Caja efectivo $1.000, deuda proveedor QA-PROV-A $500, proveedor B $700 y cliente C $300 como controles. Egreso $200 en efectivo con Enviar a cuenta corriente del proveedor activado.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Completar pago a A por $200 y rechazar la confirmación. | Caja $1.000/deuda A $500; controles sin cambios. |
| Confirmar el pago una sola vez y rechazar impresión. | Caja $800/deuda A $300, proveedor B $700/cliente C $300. |
| Consultar movimiento de caja, concepto y cuenta del proveedor. | Son efectos diferenciados del mismo pago: no sumar ambas representaciones como egreso $400. |
| Reabrir consultas del turno/proveedor. | Importes persisten y no se genera otro pago por consultar. |

## Variantes y dependencias

Variante sin envío a cuenta corriente conserva deuda A $500 aunque caja egresa $200. Transferencia usa su saldo propio. Fallo entre escritura financiera y cuenta proveedor necesita laboratorio de CAJ-009; no asumir que ambas operaciones son atómicas.

## Evidencia y límites

Registrar identidad completa, fecha/intervalo, importe original y operativo, medio, estado y documento de origen; contrastar interfaz y lecturas acotadas por deltas. No atribuir éxito al cierre de una ventana. Las variantes pendientes de regla, datos o laboratorio quedan bloqueadas y no acreditan el caso completo.

## Recuperación

Conservar evidencia antes de recuperar. Cancelar por interfaz cuando corresponda; ante error financiero comprobar primero qué se guardó y evitar repetición ciega. Restaurar el baseline privado antes de otra variante; no borrar movimientos ni retocar saldos para hacer coincidir el esperado.

## Anexo técnico y trazabilidad

Fuente inspeccionada XGestion2: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas de esa revisión:

- `src/ModuloVentas/Vistas/FormEgresoDeCaja.java:307-346`.
- `src/ModuloVentas/Entidades/CajaValores.java:224-268`.
- `src/ModuloFinanzas/Vistas/FormLibroDiario.java:260-265`.

Las referencias y tests de apoyo no acreditan ejecución E2E ni equivalencia del JAR. Registrar versión del paquete/perfil y evidencia privada saneada. INFO resume, DEBUG muestra pasos y TRACE aporta diagnóstico acotado; ante fallo conservar paso, esperado, observado, categoría y evidencia. Sin prueba causal, indicar causa no determinada. No imprimir credenciales, configuración completa ni filas completas.

