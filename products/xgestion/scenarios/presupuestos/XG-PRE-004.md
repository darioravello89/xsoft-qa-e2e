---
{"id":"XG-PRE-004","title":"Convertir un presupuesto en venta una sola vez","product":"xgestion","module":"presupuestos","tags":["xgestion","regression","presupuestos","ventas","cobros","stock","monedas"],"status":"planned"}
---

# XG-PRE-004 — Convertir un presupuesto en venta una sola vez

## Objetivo

Pasar de propuesta a venta cobrada manteniendo importes y aplicando stock una sola vez.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 3.**
Ver [mapa de cobros y documentos](../../docs/cobros-documentos.md).
No tiene Robot, seed propio ni ejecución real del JAR. Los resultados son criterios de aceptación; los pasos con contrato pendiente no afirman que esa funcionalidad exista ni se habilitan por observar la pantalla.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. Identificar JAR/SHA256, empresa, sucursal, puesto, operador y documentos de control.
- Datos QA-COB/QA-PRE/QA-DEV e importes de esta ficha son **propuestas sintéticas pendientes de seed y calibración**. `catalogo-comercial-v1` no acredita estos documentos, pagos o estados.
- Perfil local no fiscal; sin impresión, integraciones de pago, correo ni red. Sin ofertas, descuentos, recargos, impuestos adicionales ni financiación salvo variante explícita. Medios manuales QA separados de pasarelas reales.
- Presupuesto ARS 2.000, dos unidades a ARS 1.000; sin pago previo; stock inicial antes del presupuesto 10. Perfil principal descuento de stock del presupuesto OFF.
- Comprobante local permitido y emisión fiscal deshabilitada. **Pendiente calibrar la selección de tipo al cerrar**: la fuente propone B/C; no aceptar una emisión fiscal ni asumir tipo interno sin configurar esa ruta.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Reabrir presupuesto y solicitar cerrar como venta con el tipo local autorizado. | Muestra productos/total 2.000; preparación de cierre no acredita todavía cobro. |
| Cancelar el diálogo de cobro antes de confirmar. | No queda venta cobrada ni movimiento definitivo de dinero; conserva la operación para retomar. Estado/tipo editable exacto tras cambiar comprobante requiere contrato del perfil. |
| Retomar, recibir ARS 2.000 y confirmar. | Una venta cerrada, un cobro 2.000 y stock 8; relación/identidad con el presupuesto trazable. |
| Volver a consultar e intentar cerrar desde una vista anterior. | No duplica ingreso, documento ni descuento de stock. |

## Variantes y dependencias

USD con cotización histórica declarada y política de conversión aprobada; descuento de stock ON: si el presupuesto ya dejó stock 8, al vender debe seguir 8, sin volver a restar dos unidades. Preparar cada variante por separado. Selección de tipo/rechazo del ofrecimiento y posible recalculo de precio/moneda son contratos previos; no deducirlos del resultado de la UI.

Calibrar controles accesibles para el JAR antes de automatizar; los nombres/atajos leídos en fuente no sustituyen calibración. No usar coordenadas fijas ni extender permisos de doble clic de otras pantallas. Preparar oráculos independientes por identidad, importe original/operativo, medio, moneda y contexto; toda regla no confirmada se resuelve antes de habilitar su variante.

## Evidencia y límites

Contrastar documento, pagos, saldo, caja e inventario según el alcance de los pasos, con importes iniciales/finales y deltas esperados. Separar estados de preparación, persistencia de borrador/pagos y cierre definitivo. No exigir ausencia de todo registro cuando puede existir historia inactiva. Libro diario y caja pueden tener representaciones distintas: no sumar filas indiscriminadamente como dinero duplicado.

Registrar en informe privado JAR/SHA256, commit del harness, paquete, perfil, variante e identidades saneadas. INFO resume, DEBUG describe pasos y TRACE aporta diagnóstico acotado; todo fallo conserva paso, esperado, observado, categoría y evidencia. Causa no determinada si no hay prueba causal; nunca credenciales, configuración privada completa ni filas enteras.

## Recuperación

Conservar evidencia y consultar el estado antes de repetir una confirmación incierta. Cancelar por interfaz cuando el paso lo permita; no improvisar pagos compensatorios ni SQL comercial. Si no existe procedimiento aprobado para el estado parcial, mantener el bloqueo. Restaurar baseline antes de otra variante; anular una operación no reemplaza restaurar el laboratorio.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Rutas y líneas relativas a XGestion2:

- `src/ModuloVentas/Vistas/FormVenta.java:6216-6238`.
- `src/ModuloVentas/Vistas/FormVenta.java:6305-6346`.
- `src/ModuloVentas/Vistas/FormVenta.java:5183-5195`.

Las referencias describen reglas o riesgos; los tests fuente no acreditan el flujo E2E del JAR. Las modalidades pendientes de contrato están delimitadas arriba, sin inventar su soporte.

