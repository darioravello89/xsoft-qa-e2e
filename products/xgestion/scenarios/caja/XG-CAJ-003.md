---
{"id":"XG-CAJ-003","title":"Registrar ingresos y egresos respetando el saldo del medio elegido","product":"xgestion","module":"caja","tags":["xgestion","regression","caja","cobros","recuperacion"],"status":"planned"}
---

# XG-CAJ-003 — Registrar ingresos y egresos respetando el saldo del medio elegido

## Objetivo

Registrar ingresos y egresos respetando el saldo del medio elegido, desde el trabajo de la persona que administra dinero o realiza el cierre.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 4 del roadmap.** Ficha del [mapa de Libro Diario y Caja](../../docs/libro-diario-caja.md). No tiene Robot ni validación real; las variantes integradas necesitan su laboratorio propio.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. JAR identificado por SHA256; sin ejecutar fiscal, bancos, correo, mensajería ni impresoras reales.
- Perfil base: empresa/sucursal/puesto/operador QA identificados, ARS y medios manuales sin integración. El perfil declara turno habilitado o diario, cierre normal/ciego y salida del sistema al cerrar; no cambiar configuración para evitar una comprobación.
- Productos, clientes, proveedores, conceptos, movimientos y turnos de esta ficha son **datos sintéticos pendientes de preparar**. El seed comercial actual no garantiza estos saldos ni identidades. Falta contrato de datos/oráculos, permisos y calibración de pantallas; sin ellos se informa bloqueo.
- Libro Diario y Caja tienen alcances diferentes: conciliar los efectos por origen y contexto; no exigir igual cantidad de filas ni igual saldo entre sus consultas.
- Saldo inicial efectivo $1.000/transferencia manual $200. Alerta por egreso mayor al disponible ON. Ingreso efectivo $500 y egreso efectivo $400 con conceptos/descripcion QA.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Ingresar $500 de efectivo y confirmar. | Disponible efectivo $1.500, transferencia $200. |
| Pedir egreso $400 y rechazar primero la confirmación; luego aceptarlo. | Rechazo conserva $1.500; aceptación deja $1.100 una sola vez. |
| Intentar egreso efectivo $1.100,01 y transferencia $200,01 en corridas controladas. | Se rechazan por exceder saldo del medio elegido, sin usar dinero del otro medio. |
| Desde saldo efectivo $1.100 retirar exactamente $1.100. | Se permite el límite exacto y efectivo queda $0. |

## Variantes y dependencias

Perfil alerta OFF permite exceso de un importe positivo: esa configuración no debe reinterpretarse como bloqueo obligatorio. Cero/negativo siguen sujetos a validación. Campos obligatorios, cancelar picker de concepto en ingreso y cambio de usuario/turno completan variantes con baseline propio.

## Evidencia y límites

Registrar identidad completa, fecha/intervalo, importe original y operativo, medio, estado y documento de origen; contrastar interfaz y lecturas acotadas por deltas. No atribuir éxito al cierre de una ventana. Las variantes pendientes de regla, datos o laboratorio quedan bloqueadas y no acreditan el caso completo.

## Recuperación

Conservar evidencia antes de recuperar. Cancelar por interfaz cuando corresponda; ante error financiero comprobar primero qué se guardó y evitar repetición ciega. Restaurar el baseline privado antes de otra variante; no borrar movimientos ni retocar saldos para hacer coincidir el esperado.

## Anexo técnico y trazabilidad

Fuente inspeccionada XGestion2: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas de esa revisión:

- `src/ModuloVentas/Vistas/FormIngresoDeCaja.java:107-149`.
- `src/ModuloVentas/Vistas/FormEgresoDeCaja.java:299-377`.
- `test/ModuloVentas/Entidades/CajaSaldoDisponibleServiceTest.java:17-86`.
- `test/ModuloVentas/Vistas/FormEgresoDeCajaSaldoDisponiblePolicyTest.java:20-62`.

Las referencias y tests de apoyo no acreditan ejecución E2E ni equivalencia del JAR. Registrar versión del paquete/perfil y evidencia privada saneada. INFO resume, DEBUG muestra pasos y TRACE aporta diagnóstico acotado; ante fallo conservar paso, esperado, observado, categoría y evidencia. Sin prueba causal, indicar causa no determinada. No imprimir credenciales, configuración completa ni filas completas.

