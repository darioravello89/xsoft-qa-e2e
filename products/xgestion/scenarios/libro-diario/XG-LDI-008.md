---
{"id":"XG-LDI-008","title":"Consultar históricos y comprobantes sin alterar el movimiento","product":"xgestion","module":"libro-diario","tags":["xgestion","regression","libro-diario","comprobantes","monedas"],"status":"planned"}
---

# XG-LDI-008 — Consultar históricos y comprobantes sin alterar el movimiento

## Objetivo

Consultar históricos y comprobantes sin alterar el movimiento, desde el trabajo de la persona que administra dinero o realiza el cierre.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P1, etapa 4 del roadmap.** Ficha del [mapa de Libro Diario y Caja](../../docs/libro-diario-caja.md). No tiene Robot ni validación real; las variantes integradas necesitan su laboratorio propio.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. JAR identificado por SHA256; sin ejecutar fiscal, bancos, correo, mensajería ni impresoras reales.
- Perfil base: empresa/sucursal/puesto/operador QA identificados, ARS y medios manuales sin integración. El perfil declara turno habilitado o diario, cierre normal/ciego y salida del sistema al cerrar; no cambiar configuración para evitar una comprobación.
- Productos, clientes, proveedores, conceptos, movimientos y turnos de esta ficha son **datos sintéticos pendientes de preparar**. El seed comercial actual no garantiza estos saldos ni identidades. Falta contrato de datos/oráculos, permisos y calibración de pantallas; sin ellos se informa bloqueo.
- Libro Diario y Caja tienen alcances diferentes: conciliar los efectos por origen y contexto; no exigir igual cantidad de filas ni igual saldo entre sus consultas.
- Movimientos de ayer: ARS $100, USD 10 con cotización guardada $1.000 y operativo $10.000; cotización actual distinta $1.100. Documento con referencia a comprobante de QA y otro sin archivo. Filtro histórico explícito.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Abrir Libro Diario y buscar ayer. | No confunde vista inicial de hoy con ausencia del histórico; al filtrar aparece el conjunto esperado. |
| Consultar moneda, importe original y cotización del USD. | Conserva USD 10/$1.000/ARS $10.000, sin revalorizar con $1.100 actual. |
| Recargar y alternar intervalos sin resultados/con resultados. | No modifica movimientos ni conserva totales de un filtro anterior. |
| Revisar presencia o ausencia del acceso al comprobante. | La referencia se corresponde con su movimiento; consultar no produce alta/baja ni movimiento financiero adicional. |

## Variantes y dependencias

Abrir el comprobante usa un dominio externo en la fuente: queda fuera del perfil offline hasta disponer de recurso sintético y red expresamente autorizada. No descargar archivos reales. Exportación o impresión histórica necesita calibrar una acción de usuario disponible; la existencia de un método no basta para darla por accesible.

## Evidencia y límites

Registrar identidad completa, fecha/intervalo, importe original y operativo, medio, estado y documento de origen; contrastar interfaz y lecturas acotadas por deltas. No atribuir éxito al cierre de una ventana. Las variantes pendientes de regla, datos o laboratorio quedan bloqueadas y no acreditan el caso completo.

## Recuperación

Conservar evidencia antes de recuperar. Cancelar por interfaz cuando corresponda; ante error financiero comprobar primero qué se guardó y evitar repetición ciega. Restaurar el baseline privado antes de otra variante; no borrar movimientos ni retocar saldos para hacer coincidir el esperado.

## Anexo técnico y trazabilidad

Fuente inspeccionada XGestion2: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas de esa revisión:

- `src/ModuloFinanzas/Vistas/FormLibroDiario.java:260-290`.
- `src/ModuloFinanzas/Vistas/FormLibroDiario.java:368-425`.
- `test/ModuloFinanzas/Entidades/FormLibroDiarioDominioPolicyTest.java:14-20`.

Las referencias y tests de apoyo no acreditan ejecución E2E ni equivalencia del JAR. Registrar versión del paquete/perfil y evidencia privada saneada. INFO resume, DEBUG muestra pasos y TRACE aporta diagnóstico acotado; ante fallo conservar paso, esperado, observado, categoría y evidencia. Sin prueba causal, indicar causa no determinada. No imprimir credenciales, configuración completa ni filas completas.

