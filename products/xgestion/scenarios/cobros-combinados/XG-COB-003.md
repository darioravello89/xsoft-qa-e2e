---
{"id":"XG-COB-003","title":"Cancelar un cobro combinado y retomarlo sin arrastrar pagos","product":"xgestion","module":"cobros-combinados","tags":["xgestion","regression","cobros-combinados","cobros","recuperacion","stock"],"status":"planned"}
---

# XG-COB-003 — Cancelar un cobro combinado y retomarlo sin arrastrar pagos

## Objetivo

Volver a la venta al cancelar el reparto y cobrar después sólo los importes que se confirmen.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 3.**
Ver [mapa de cobros y documentos](../../docs/cobros-documentos.md).
No tiene Robot, seed propio ni ejecución real del JAR. Los resultados son criterios de aceptación; los pasos con contrato pendiente no afirman que esa funcionalidad exista ni se habilitan por observar la pantalla.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. Identificar JAR/SHA256, empresa, sucursal, puesto, operador y documentos de control.
- Datos QA-COB/QA-PRE/QA-DEV e importes de esta ficha son **propuestas sintéticas pendientes de seed y calibración**. `catalogo-comercial-v1` no acredita estos documentos, pagos o estados.
- Perfil local no fiscal; sin impresión, integraciones de pago, correo ni red. Sin ofertas, descuentos, recargos, impuestos adicionales ni financiación salvo variante explícita. Medios manuales QA separados de pasarelas reales.
- Venta ARS 2.000 en preparación; primer intento con efectivo ARS 500. Segundo intento con efectivo 800/tarjeta manual 1.200.
- Sin pago previo confirmado, sin cuotas ni ajustes del medio; stock inicial 10 y finanzas de control identificadas.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Abrir Multiple e ingresar efectivo ARS 500; elegir Cancelar. | Regresa al cobro sin cerrar venta; los pagos del intento cancelado quedan anulados/inactivos y no hay ingreso definitivo ni consumo de stock. |
| Cancelar también el cierre principal y volver a vender. | Se conservan productos y total ARS 2.000; no se acredita un pago por sólo salir del diálogo. |
| Retomar el cobro y cargar el reparto 800/1.200. | Resumen ARS 2.000 sin sumar los 500 del primer intento. |
| Finalizar y consultar la operación. | Un cierre, dos pagos efectivos del reparto final y stock 8. Los rastros inactivos del intento anterior no se cuentan como cobranza. |

## Variantes y dependencias

Cancelar sin cargar líneas y tras varias líneas. Distinguir Escape/Cancelar del diálogo múltiple y salida del cierre principal. Con reparto exacto, Cobrar puede confirmar automáticamente el cierre principal: no proponer una cancelación posterior como si siguiera abierto.

Calibrar controles accesibles para el JAR antes de automatizar; los nombres/atajos leídos en fuente no sustituyen calibración. No usar coordenadas fijas ni extender permisos de doble clic de otras pantallas. Preparar oráculos independientes por identidad, importe original/operativo, medio, moneda y contexto; toda regla no confirmada se resuelve antes de habilitar su variante.

## Evidencia y límites

Contrastar documento, pagos, saldo, caja e inventario según el alcance de los pasos, con importes iniciales/finales y deltas esperados. Separar estados de preparación, persistencia de borrador/pagos y cierre definitivo. No exigir ausencia de todo registro cuando puede existir historia inactiva. Libro diario y caja pueden tener representaciones distintas: no sumar filas indiscriminadamente como dinero duplicado.

Registrar en informe privado JAR/SHA256, commit del harness, paquete, perfil, variante e identidades saneadas. INFO resume, DEBUG describe pasos y TRACE aporta diagnóstico acotado; todo fallo conserva paso, esperado, observado, categoría y evidencia. Causa no determinada si no hay prueba causal; nunca credenciales, configuración privada completa ni filas enteras.

## Recuperación

Conservar evidencia y consultar el estado antes de repetir una confirmación incierta. Cancelar por interfaz cuando el paso lo permita; no improvisar pagos compensatorios ni SQL comercial. Si no existe procedimiento aprobado para el estado parcial, mantener el bloqueo. Restaurar baseline antes de otra variante; anular una operación no reemplaza restaurar el laboratorio.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Rutas y líneas relativas a XGestion2:

- `src/ModuloVentas/Vistas/Dialogs/DialogCobroMultiple.java:536-541`.
- `src/ModuloVentas/Entidades/VentaPago.java:524-543`.
- `src/ModuloVentas/Vistas/Dialogs/formTicketCierre.java:582-625`.

Las referencias describen reglas o riesgos; los tests fuente no acreditan el flujo E2E del JAR. Las modalidades pendientes de contrato están delimitadas arriba, sin inventar su soporte.

