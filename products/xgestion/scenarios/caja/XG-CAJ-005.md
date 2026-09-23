---
{"id":"XG-CAJ-005","title":"Arquear cada medio y separar efectivo ARS de USD","product":"xgestion","module":"caja","tags":["xgestion","regression","caja","cierre-caja","monedas","cobros"],"status":"planned"}
---

# XG-CAJ-005 — Arquear cada medio y separar efectivo ARS de USD

## Objetivo

Arquear cada medio y separar efectivo ARS de USD, desde el trabajo de la persona que administra dinero o realiza el cierre.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 4 del roadmap.** Ficha del [mapa de Libro Diario y Caja](../../docs/libro-diario-caja.md). No tiene Robot ni validación real; las variantes integradas necesitan su laboratorio propio.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. JAR identificado por SHA256; sin ejecutar fiscal, bancos, correo, mensajería ni impresoras reales.
- Perfil de esta ficha: cierre ciego habilitado, turno abierto identificado y medios manuales sin integración. Declarar empresa/sucursal/puesto/operador y salida del sistema al cerrar; no cambiar configuración para evitar una comprobación. Se admite cerrar este turno de QA una vez por variante.
- Productos, clientes, proveedores, conceptos, movimientos y turnos de esta ficha son **datos sintéticos pendientes de preparar**. El seed comercial actual no garantiza estos saldos ni identidades. Falta contrato de datos/oráculos, permisos y calibración de pantallas; sin ellos se informa bloqueo.
- Libro Diario y Caja tienen alcances diferentes: conciliar los efectos por origen y contexto; no exigir igual cantidad de filas ni igual saldo entre sus consultas.
- Baseline preparado: efectivo ARS esperado $1.500, transferencia $500 y tarjeta manual $1.000/2 comprobantes; total ARS $3.000. Medios configurados por importe/cantidad/ambos según ficha. Variante USD separada: esperado físico USD 10 con cotización original $1.000.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Abrir cierre ciego del turno correcto e informar efectivo con billetes $1.000 + $500. | Contado ARS $1.500, sin atribuirlo a transferencia/tarjeta. Todavía no se exige visualizar esperado ni diferencia. |
| Informar transferencia $500 y tarjeta $1.000 con 2 comprobantes; completar con cero los demás campos obligatorios. | Todos los conteos están completos; total contado base ARS $3.000. El turno sigue abierto hasta confirmar. |
| Confirmar el cierre una vez y consultar el resumen resultante. | Turno cerrado y un único registro de conteo. Cada medio coincide con su importe/cantidad esperada; diferencias cero. Recién aquí se comparan esperado y diferencia. |
| Restaurar el baseline para la variante USD, informar USD 10 en su panel, completar los otros conteos del perfil y confirmar su cierre. | Resumen: contado y esperado USD 10, diferencia USD 0; no se agrega nominalmente 10 a pesos. Esta variante no reutiliza el turno ya cerrado. |
| Consultar las referencias de origen del resumen de cada variante. | Se separan original USD, equivalente operativo y ARS físico; no se vuelve a convertir ni duplicar una cobranza. |

## Variantes y dependencias

Cantidad, importe, ambos y ninguno son configuraciones distintas. El resumen fuente presenta USD por separado, mientras el total general usa acumuladores ARS/no efectivo: definir y aprobar cómo concilia cada cobro USD antes de acreditar la variante mixta. No fijar un total global USD por suposición. Fallback legacy de medio inválido a efectivo requiere fixture explícito.

## Evidencia y límites

Registrar identidad completa, fecha/intervalo, importe original y operativo, medio, estado y documento de origen; contrastar interfaz y lecturas acotadas por deltas. No atribuir éxito al cierre de una ventana. Las variantes pendientes de regla, datos o laboratorio quedan bloqueadas y no acreditan el caso completo.

## Recuperación

Conservar evidencia antes de recuperar. Cancelar por interfaz cuando corresponda; ante error financiero comprobar primero qué se guardó y evitar repetición ciega. Restaurar el baseline privado antes de otra variante; no borrar movimientos ni retocar saldos para hacer coincidir el esperado.

## Anexo técnico y trazabilidad

Fuente inspeccionada XGestion2: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas de esa revisión:

- `src/ModuloVentas/Vistas/FormCierreCajaCiego.java:130-221`.
- `src/ModuloVentas/Vistas/FormCierreCajaCiego.java:265-280`.
- `src/ModuloVentas/Vistas/FormCierreCajaCiego.java:291-329`.
- `src/ModuloVentas/Vistas/FormCierreCajaCiego.java:410-443`.
- `test/ModuloVentas/Entidades/CajaValoresEsperadoPorPagoTest.java:16-56`.

Las referencias y tests de apoyo no acreditan ejecución E2E ni equivalencia del JAR. Registrar versión del paquete/perfil y evidencia privada saneada. INFO resume, DEBUG muestra pasos y TRACE aporta diagnóstico acotado; ante fallo conservar paso, esperado, observado, categoría y evidencia. Sin prueba causal, indicar causa no determinada. No imprimir credenciales, configuración completa ni filas completas.
