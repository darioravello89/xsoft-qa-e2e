---
{"id":"XG-LDI-004","title":"Reconocer el origen de cada movimiento sin duplicar dinero o deuda","product":"xgestion","module":"libro-diario","tags":["xgestion","regression","libro-diario","cuenta-corriente","cobros"],"status":"planned"}
---

# XG-LDI-004 — Reconocer el origen de cada movimiento sin duplicar dinero o deuda

## Objetivo

Reconocer el origen de cada movimiento sin duplicar dinero o deuda, desde el trabajo de la persona que administra dinero o realiza el cierre.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 4 del roadmap.** Ficha del [mapa de Libro Diario y Caja](../../docs/libro-diario-caja.md). No tiene Robot ni validación real; las variantes integradas necesitan su laboratorio propio.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. JAR identificado por SHA256; sin ejecutar fiscal, bancos, correo, mensajería ni impresoras reales.
- Perfil base: empresa/sucursal/puesto/operador QA identificados, ARS y medios manuales sin integración. El perfil declara turno habilitado o diario, cierre normal/ciego y salida del sistema al cerrar; no cambiar configuración para evitar una comprobación.
- Productos, clientes, proveedores, conceptos, movimientos y turnos de esta ficha son **datos sintéticos pendientes de preparar**. El seed comercial actual no garantiza estos saldos ni identidades. Falta contrato de datos/oráculos, permisos y calibración de pantallas; sin ellos se informa bloqueo.
- Libro Diario y Caja tienen alcances diferentes: conciliar los efectos por origen y contexto; no exigir igual cantidad de filas ni igual saldo entre sus consultas.
- Baseline caja $1.000 y proveedor QA con deuda $500. Ingreso de caja $200 con Contabiliza habilitado y concepto propio QA; egreso por pago al proveedor $100. Medios manuales ARS. Cada acción usa referencia única.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Registrar ingreso de caja $200 y seleccionar el concepto. | Caja aumenta $200; Libro Diario muestra la representación del concepto, sin exigir que incluya además concepto movimientoCaja. |
| Pagar $100 al proveedor desde egreso de caja con envío a su cuenta corriente. | Caja neta queda $1.100; deuda del proveedor $400; Libro Diario refleja el concepto del pago. |
| Consultar cada efecto por su referencia y contexto. | Identifica representación de caja, concepto y cuenta proveedor; la duplicidad técnica esperada no duplica el dinero. |
| Restaurar y repetir ingreso con Contabiliza deshabilitado. | Caja aumenta $200 sin exigir un ingreso adicional visible en el Libro Diario predeterminado. |

## Variantes y dependencias

El concepto movimientoCaja es 1 y Libro Diario lo excluye por defecto. No comparar una suma indiscriminada de movimientos con el saldo de caja. Variantes cobro de cliente y venta deben usar sus orígenes respectivos, no registrar manualmente sustitutos.

## Evidencia y límites

Registrar identidad completa, fecha/intervalo, importe original y operativo, medio, estado y documento de origen; contrastar interfaz y lecturas acotadas por deltas. No atribuir éxito al cierre de una ventana. Las variantes pendientes de regla, datos o laboratorio quedan bloqueadas y no acreditan el caso completo.

## Recuperación

Conservar evidencia antes de recuperar. Cancelar por interfaz cuando corresponda; ante error financiero comprobar primero qué se guardó y evitar repetición ciega. Restaurar el baseline privado antes de otra variante; no borrar movimientos ni retocar saldos para hacer coincidir el esperado.

## Anexo técnico y trazabilidad

Fuente inspeccionada XGestion2: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas de esa revisión:

- `src/Utilidades/Constantes.java:106-122`.
- `src/ModuloFinanzas/Vistas/FormLibroDiario.java:260-265`.
- `src/ModuloVentas/Vistas/FormIngresoDeCaja.java:104-170`.
- `src/ModuloVentas/Vistas/FormEgresoDeCaja.java:299-346`.
- `src/ModuloVentas/Entidades/CajaValores.java:208-268`.

Las referencias y tests de apoyo no acreditan ejecución E2E ni equivalencia del JAR. Registrar versión del paquete/perfil y evidencia privada saneada. INFO resume, DEBUG muestra pasos y TRACE aporta diagnóstico acotado; ante fallo conservar paso, esperado, observado, categoría y evidencia. Sin prueba causal, indicar causa no determinada. No imprimir credenciales, configuración completa ni filas completas.
