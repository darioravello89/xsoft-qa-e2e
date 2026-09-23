---
{"id":"XG-REC-004","title":"Reconocer una venta ya cobrada cuando se pierde la confirmación visual","product":"xgestion","module":"recuperacion","tags":["xgestion","regression","recuperacion","ventas","cobros","stock"],"status":"planned"}
---

# XG-REC-004 — Reconocer una venta ya cobrada cuando se pierde la confirmación visual

## Objetivo

Volver a operar después de perder la interfaz sin repetir un cobro que ya quedó guardado.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P0.** Ver [continuidad operativa](../../docs/continuidad-operativa.md). Sin Robot, seed ni evidencia del JAR. Corte posterior al commit de una venta. Se complementa con [FIN-009](../conciliacion/XG-FIN-009.md), que trata confirmaciones repetidas: aquí no se repite el botón, se pierde la confirmación visual y se reconcilia al reiniciar.

## Precondiciones y datos

- VM QA exclusiva offline; A × 2 a ARS 1.000, stock inicial 10 y pago exacto ARS 2.000; sin fiscal, impresión, cuotas, listas ni servicios.
- Punto de interrupción posterior al commit y anterior a la señal final de UI, verificado por mecanismo pendiente. Registrar identidad completa de la venta/correlación sin depender del mensaje perdido.
- Procedimiento de reinicio sobre la misma base, conservando evidencia y sin restaurar el baseline hasta finalizar la conciliación. La capacidad actual del runner para este flujo debe prepararse.
- Todos los fixtures mencionados son sintéticos y **NO están creados por esta entrega**. Faltan paquete, controles accesibles, perfiles y lectores por identidad. No escribir SQL comercial durante el recorrido ni debilitar las guardas del runner.

## Pasos y resultados esperados

| Acción del usuario o responsable QA | Resultado esperado |
| --- | --- |
| Confirmar el cobro y provocar el corte de interfaz en el punto posterior al commit preparado. | La UI no entrega una confirmación fiable; el caso no se marca FALLÓ por ausencia del mensaje ni OK sin comprobar persistencia. |
| Reiniciar el JAR y buscar la operación por su identidad/correlación. | Venta cerrada por ARS 2.000, un cobro de ARS 2.000 y stock A = 8. No pedir ni ejecutar otro cobro. |
| Abrir el comprobante histórico y cerrar su consulta. | Conserva importes y estado; consultar no añade pago ni descuento de stock. |
| Crear una venta distinta de A × 1 y cobrar ARS 1.000. | Dos ventas distintas en total: ARS 2.000 y ARS 1.000; stock final 7 y cobros acumulados ARS 3.000. La segunda no reutiliza la identidad de la primera. |

## Variantes y dependencias

- Si la inyección no acredita si el corte fue antes o después del commit, tratarlo como resultado indeterminado: consulta completa antes de decidir continuar.
- Comprobante existente convertido a venta requiere identidad y regla de conversión propias; no inferirlas del alta simple.
- Un pago externo podría tener otro extremo persistido; está fuera de este caso local y necesita contrato de conciliación específico.

## Evidencia y límites

Comparar número/contexto, total, pago, renglones y stock del cierre persistido con la nueva operación. Conservar orden de los acontecimientos; la continuidad no se aprueba mediante una compensación posterior.

Un perfil, procedimiento u oráculo faltante produce BLOQUEADO antes de la acción dependiente. Ningún resultado observado se adopta como esperado para aprobar. INFO resume y explica fallos; DEBUG muestra acciones de negocio; TRACE agrega diagnóstico saneado. Conservar paso, esperado/observado y causa no determinada si no está demostrada.

## Recuperación

Reconocer la venta existente y continuar con otra intención de compra. Si no puede localizarse inequívocamente, detener el cobro y conservar estado/evidencia; nunca crear una venta equivalente para obtener un mensaje de éxito.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: commit `daa002d597d0fa7380ace204d3727085c52d1415`. Las rutas siguientes son relativas a XGestion2; las clases/tests describen reglas y riesgos, no ejecuciones E2E.

- `src/ModuloVentas/Vistas/FormVenta.java:6338-6348`: validaciones y commit antes de continuar la UI.
- `src/ModuloVentas/Vistas/FormVenta.java:1916-1962`: reapertura de cerrado en modo lectura.
- `test/ModuloVentas/Vistas/FormVentaCierreCobroPolicyTest.java` y `test/ModuloVentas/Entidades/TicketVentaSiguienteIdPolicyTest.java`.

Registrar SHA256/build del JAR, paquete, perfil, ámbito, IDs y reporte privado. No publicar credenciales, configuración completa, copias de bases, payloads, filas completas ni logs crudos.

