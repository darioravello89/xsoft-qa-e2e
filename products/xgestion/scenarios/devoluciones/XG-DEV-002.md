---
{"id":"XG-DEV-002","title":"Anular una venta con pagos combinados y conciliar cada medio","product":"xgestion","module":"devoluciones","tags":["xgestion","regression","devoluciones","cobros-combinados","cobros","monedas","caja","stock"],"status":"planned"}
---

# XG-DEV-002 — Anular una venta con pagos combinados y conciliar cada medio

## Objetivo

Devolver una venta pagada por varios medios sin perder parte del importe ni compensarlo dos veces.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 4.**
Ver [mapa de cobros y documentos](../../docs/cobros-documentos.md).
No tiene Robot, seed propio ni ejecución real del JAR. Los resultados son criterios de aceptación; los pasos con contrato pendiente no afirman que esa funcionalidad exista ni se habilitan por observar la pantalla.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. Identificar JAR/SHA256, empresa, sucursal, puesto, operador y documentos de control.
- Datos QA-COB/QA-PRE/QA-DEV e importes de esta ficha son **propuestas sintéticas pendientes de seed y calibración**. `catalogo-comercial-v1` no acredita estos documentos, pagos o estados.
- Perfil local no fiscal; sin impresión, integraciones de pago, correo ni red. Sin ofertas, descuentos, recargos, impuestos adicionales ni financiación salvo variante explícita. Medios manuales QA separados de pasarelas reales.
- Venta cerrada ARS 2.000; efectivo ARS 800 y tarjeta manual ARS 1.200, sin vuelto, ajustes ni pagos futuros. Dos productos con stock conocido.
- Devolución de dinero habilitada y perfil local no fiscal; ambos medios manuales sin interacción con bancos/proveedores externos.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Consultar los pagos de la venta y su total. | Dos importes activos 800/1.200 vinculados al mismo documento, neto 2.000. |
| Anular con motivo y devolución de dinero explícita. | Devolución total ARS 2.000: efectivo 800 y tarjeta manual 1.200 en el registro local; no se afirma reintegro real por una pasarela. |
| Consultar caja por medio y stock. | Cada medio conserva su compensación y el stock vuelve una sola vez; no aparece otra salida por el total además de las devoluciones por medio. |
| Actualizar y consultar otra venta de control. | Sin nuevas devoluciones ni cambios ajenos. |

## Variantes y dependencias

Variante con vuelto: antes de automatizar, acordar a qué medio se atribuye y en qué orden se devuelve. La consulta fuente de pagos para anulación no declara ORDER BY; el esperado por medio no puede depender de un orden accidental. ARS/USD, pagos futuros y descuentos/recargos requieren contrato separado de devolución y moneda histórica. No trasladar directamente el reparto de cuotas.

Calibrar controles accesibles para el JAR antes de automatizar; los nombres/atajos leídos en fuente no sustituyen calibración. No usar coordenadas fijas ni extender permisos de doble clic de otras pantallas. Preparar oráculos independientes por identidad, importe original/operativo, medio, moneda y contexto; toda regla no confirmada se resuelve antes de habilitar su variante.

## Evidencia y límites

Contrastar documento, pagos, saldo, caja e inventario según el alcance de los pasos, con importes iniciales/finales y deltas esperados. Separar estados de preparación, persistencia de borrador/pagos y cierre definitivo. No exigir ausencia de todo registro cuando puede existir historia inactiva. Libro diario y caja pueden tener representaciones distintas: no sumar filas indiscriminadamente como dinero duplicado.

Registrar en informe privado JAR/SHA256, commit del harness, paquete, perfil, variante e identidades saneadas. INFO resume, DEBUG describe pasos y TRACE aporta diagnóstico acotado; todo fallo conserva paso, esperado, observado, categoría y evidencia. Causa no determinada si no hay prueba causal; nunca credenciales, configuración privada completa ni filas enteras.

## Recuperación

Conservar evidencia y consultar el estado antes de repetir una confirmación incierta. Cancelar por interfaz cuando el paso lo permita; no improvisar pagos compensatorios ni SQL comercial. Si no existe procedimiento aprobado para el estado parcial, mantener el bloqueo. Restaurar baseline antes de otra variante; anular una operación no reemplaza restaurar el laboratorio.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Rutas y líneas relativas a XGestion2:

- `src/ModuloVentas/Entidades/TicketVenta.java:3348-3382`.
- `src/ModuloVentas/Entidades/VentaPago.java:121-133`.
- `src/ModuloVentas/Vistas/FormVentas.java:1426-1439`.
- `test/ModuloVentas/Entidades/VentaTotalesCalculadorTest.java:87-105`.

Las referencias describen reglas o riesgos; los tests fuente no acreditan el flujo E2E del JAR. Las modalidades pendientes de contrato están delimitadas arriba, sin inventar su soporte.

