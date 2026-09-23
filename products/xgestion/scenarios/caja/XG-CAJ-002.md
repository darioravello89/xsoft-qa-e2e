---
{"id":"XG-CAJ-002","title":"Conciliar ventas cobradas y vuelto con la caja de cada medio","product":"xgestion","module":"caja","tags":["xgestion","regression","caja","ventas","cobros","efectivo"],"status":"planned"}
---

# XG-CAJ-002 — Conciliar ventas cobradas y vuelto con la caja de cada medio

## Objetivo

Conciliar ventas cobradas y vuelto con la caja de cada medio, desde el trabajo de la persona que administra dinero o realiza el cierre.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0, etapa 4 del roadmap.** Ficha del [mapa de Libro Diario y Caja](../../docs/libro-diario-caja.md). No tiene Robot ni validación real; las variantes integradas necesitan su laboratorio propio.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. JAR identificado por SHA256; sin ejecutar fiscal, bancos, correo, mensajería ni impresoras reales.
- Perfil base: empresa/sucursal/puesto/operador QA identificados, ARS y medios manuales sin integración. El perfil declara turno habilitado o diario, cierre normal/ciego y salida del sistema al cerrar; no cambiar configuración para evitar una comprobación.
- Productos, clientes, proveedores, conceptos, movimientos y turnos de esta ficha son **datos sintéticos pendientes de preparar**. El seed comercial actual no garantiza estos saldos ni identidades. Falta contrato de datos/oráculos, permisos y calibración de pantallas; sin ellos se informa bloqueo.
- Libro Diario y Caja tienen alcances diferentes: conciliar los efectos por origen y contexto; no exigir igual cantidad de filas ni igual saldo entre sus consultas.
- Turno QA con fondo efectivo $5.000. Producto ARS $1.000 sin ofertas/impuestos. Venta efectivo 2 unidades/$2.000, recibido $3.000/vuelto $1.000. Otra venta transferencia manual $1.500, sin integración.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Cargar la venta de $2.000 y cancelar antes de confirmar el cobro. | El fondo sigue $5.000; no incorpora la venta pendiente al dinero disponible. |
| Retomar y cobrar, recibido $3.000/vuelto $1.000. | Caja incorpora neto $2.000, no recibido bruto $3.000; efectivo esperado $7.000. |
| Cobrar la venta de $1.500 por transferencia manual. | Transferencia esperada $1.500; efectivo permanece $7.000. |
| Consultar ventas, movimientos y cierre del mismo turno. | Recaudación $3.500 y total operativo $8.500 incluyendo fondo; identidades y medios se corresponden una vez. |

## Variantes y dependencias

Descuentos/devolución/anulación requieren originales y reglas propios; no considerar un movimiento manual como sustituto de una venta real. En cierre tradicional Efectivo puede mostrar recaudación de ventas y Fondo por separado; comparar cada campo con su significado, no exigir $7.000 en todo campo llamado efectivo.

## Evidencia y límites

Registrar identidad completa, fecha/intervalo, importe original y operativo, medio, estado y documento de origen; contrastar interfaz y lecturas acotadas por deltas. No atribuir éxito al cierre de una ventana. Las variantes pendientes de regla, datos o laboratorio quedan bloqueadas y no acreditan el caso completo.

## Recuperación

Conservar evidencia antes de recuperar. Cancelar por interfaz cuando corresponda; ante error financiero comprobar primero qué se guardó y evitar repetición ciega. Restaurar el baseline privado antes de otra variante; no borrar movimientos ni retocar saldos para hacer coincidir el esperado.

## Anexo técnico y trazabilidad

Fuente inspeccionada XGestion2: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas y líneas de esa revisión:

- `src/ModuloVentas/Entidades/CajaValores.java:224-268`.
- `src/ModuloVentas/Vistas/FormCierreDeCaja.java:762-806`.
- `test/ModuloVentas/Entidades/CajaValoresEsperadoPorPagoTest.java:16-56`.

Las referencias y tests de apoyo no acreditan ejecución E2E ni equivalencia del JAR. Registrar versión del paquete/perfil y evidencia privada saneada. INFO resume, DEBUG muestra pasos y TRACE aporta diagnóstico acotado; ante fallo conservar paso, esperado, observado, categoría y evidencia. Sin prueba causal, indicar causa no determinada. No imprimir credenciales, configuración completa ni filas completas.

