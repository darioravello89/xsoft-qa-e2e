---
{"id":"XG-DEV-004","title":"Resolver una devolución cuando hubo anticipo y pagos posteriores","product":"xgestion","module":"devoluciones","tags":["xgestion","regression","devoluciones","cuenta-corriente","ctacte-clientes","cobros","caja"],"status":"planned"}
---

# XG-DEV-004 — Resolver una devolución cuando hubo anticipo y pagos posteriores

## Objetivo

Determinar qué deuda se compensa y qué dinero se devuelve cuando el cliente pagó en momentos distintos.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 4.**
Ver [mapa de cobros y documentos](../../docs/cobros-documentos.md).
No tiene Robot, seed propio ni ejecución real del JAR. Los resultados son criterios de aceptación; los pasos con contrato pendiente no afirman que esa funcionalidad exista ni se habilitan por observar la pantalla.

## Precondiciones y datos

- Windows QA exclusivo y offline, escritorio visible, paquete privado autorizado y baseline recuperable. Identificar JAR/SHA256, empresa, sucursal, puesto, operador y documentos de control.
- Datos QA-COB/QA-PRE/QA-DEV e importes de esta ficha son **propuestas sintéticas pendientes de seed y calibración**. `catalogo-comercial-v1` no acredita estos documentos, pagos o estados.
- Perfil local no fiscal; sin impresión, integraciones de pago, correo ni red. Sin ofertas, descuentos, recargos, impuestos adicionales ni financiación salvo variante explícita. Medios manuales QA separados de pasarelas reales.
- Propuesta de fixture: venta ARS 2.000, anticipo ARS 400 y abono posterior ARS 600; saldo neto ARS 1.000 antes de anular.
- El abono posterior es global a la cuenta salvo que se verifique imputación explícita. La anulación simple sin abonos posteriores ya está en [CCC-009](../ctacte-clientes/XG-CCC-009.md); esta ficha agrega esa diferencia.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Antes de ejecutar, identificar origen del anticipo y abono y acordar su tratamiento. | Contrato firmado indica si el abono posterior corresponde a esta venta o queda como crédito global; sin esa regla no se habilita la prueba. |
| Iniciar la anulación y cancelar en el diálogo de motivo. | Venta, saldo 1.000, pagos e inventario sin cambios. |
| Confirmar sólo el circuito aprobado con su devolución. | Si se acuerda devolver todo lo recibido e imputado: egreso total 1.000 y saldo final 0. Si se devuelve sólo anticipo: egreso 400 y abono global 600 a favor, sin hacerlo desaparecer. La variante se elige antes, no según lo observado. |
| Consultar originales, compensaciones y otra deuda de control. | El dinero y la deuda se explican sin devolver dos veces ni compensar obligaciones ajenas. |

## Variantes y dependencias

**Pendiente de contrato**, no se demuestra ninguna de las dos alternativas como funcionalidad vigente. La anulación leída invierte un movimiento asociado y calcula devolución con pagado/vuelto de cabecera; eso no demuestra asignar el abono global posterior. Cuotas, varios documentos y saldos multimoneda quedan fuera hasta definir su propio circuito.

Calibrar controles accesibles para el JAR antes de automatizar; los nombres/atajos leídos en fuente no sustituyen calibración. No usar coordenadas fijas ni extender permisos de doble clic de otras pantallas. Preparar oráculos independientes por identidad, importe original/operativo, medio, moneda y contexto; toda regla no confirmada se resuelve antes de habilitar su variante.

## Evidencia y límites

Contrastar documento, pagos, saldo, caja e inventario según el alcance de los pasos, con importes iniciales/finales y deltas esperados. Separar estados de preparación, persistencia de borrador/pagos y cierre definitivo. No exigir ausencia de todo registro cuando puede existir historia inactiva. Libro diario y caja pueden tener representaciones distintas: no sumar filas indiscriminadamente como dinero duplicado.

Registrar en informe privado JAR/SHA256, commit del harness, paquete, perfil, variante e identidades saneadas. INFO resume, DEBUG describe pasos y TRACE aporta diagnóstico acotado; todo fallo conserva paso, esperado, observado, categoría y evidencia. Causa no determinada si no hay prueba causal; nunca credenciales, configuración privada completa ni filas enteras.

## Recuperación

Conservar evidencia y consultar el estado antes de repetir una confirmación incierta. Cancelar por interfaz cuando el paso lo permita; no improvisar pagos compensatorios ni SQL comercial. Si no existe procedimiento aprobado para el estado parcial, mantener el bloqueo. Restaurar baseline antes de otra variante; anular una operación no reemplaza restaurar el laboratorio.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Rutas y líneas relativas a XGestion2:

- `src/ModuloVentas/Entidades/TicketVenta.java:3315-3346`.
- `src/ModuloFinanzas/Entidades/CtaCteCliente.java:130-207`.
- `test/ModuloVentas/Entidades/VentaTotalesCalculadorTest.java:93-100`.

Las referencias describen reglas o riesgos; los tests fuente no acreditan el flujo E2E del JAR. Las modalidades pendientes de contrato están delimitadas arriba, sin inventar su soporte.

