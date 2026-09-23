---
{"id":"XG-INV-002","title":"Transferir existencias al destino correcto y conciliar el estado","product":"xgestion","module":"inventario","tags":["xgestion","regression","inventario","stock","permisos"],"status":"planned"}
---

# XG-INV-002 — Transferir existencias al destino correcto y conciliar el estado

## Objetivo

Mover mercadería entre dos sucursales conservando la existencia total y la relación entre el documento, la salida y la entrada.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P0; inventario, etapa 6.** Ver [mapa](../../docs/inventario-respaldos.md). Transferencia directa local: no se modela un envío en tránsito ni una aceptación remota que esta pantalla no demuestra.

## Precondiciones y datos

- VM Windows QA exclusiva, offline, cierre anual completo. S1 y S2 pertenecen a una sola empresa sintética en la misma base QA local; no contactar sucursales reales.
- **Fixtures sintéticos nuevos, NO creados:** A stockeable, S1 = 10 unidades, S2 = 4; B de control, S1 = 20 y S2 = 8. Transferir A × 3, costo unitario ARS 500, IVA 0, sin actualización de precios. Preparar identidades, detalle activo, Recibido y Suma stock activados.
- Rol autorizado; permiso restringido y navegación del listado pendientes de calibrar. La leyenda de fuente ofrece F5 Destino, F9 Cargar transferencia y ESC Salir; verificar esos controles en el JAR.

## Pasos y resultados esperados

| Acción del usuario | Resultado esperado |
| --- | --- |
| Abrir una transferencia de S1 y cargar A × 3. Intentar confirmar con origen/destino inválido o destino S1. | Solicita sucursal válida o cambiar destino; no descuenta ni suma stock. Puede existir el borrador, pero no una transferencia cerrada. |
| Elegir destino S2, revisar A × 3 e importe ARS 1.500; rechazar la confirmación. | La propuesta permanece disponible; A conserva S1 = 10 y S2 = 4. |
| Confirmar Cargar transferencia una sola vez. | Documento cerrado, tipo transferencia, origen S1 y destino S2. A queda S1 = 7 y S2 = 7; suma total 14. B no cambia. |
| Consultar el documento y ambos listados de existencias. | Los movimientos -3/+3 corresponden al mismo documento; no hay entrada adicional en S1 ni salida en S2. |
| Cerrar/reabrir la consulta del documento cerrado. | Estado y cantidades se conservan; consultar no vuelve a transferir. |

## Variantes y dependencias

- Cancelar el diálogo de cantidad y volver a cargar; rechazar la salida y continuar; aceptar la salida antes de confirmar. En todos, exigir ausencia de movimientos de transferencia; la política de conservar/eliminar borradores debe verificarse aparte.
- Repetir con MP de 1,250 kg sobre saldos iniciales S1 = 5,000 y S2 = 2,000: final 3,750 y 3,250; la UI redondea algunas columnas a dos decimales, por lo que el oráculo conserva tres.
- Origen elegido diferente de la sucursal del puesto: preparar tres sucursales; mover solo entre origen/destino declarados. No confundir identidad del documento con ámbito del movimiento.
- Fallo entre salida y entrada: mecanismo de inyección aún pendiente. El criterio de integridad exige conciliar ambos lados; un cierre parcial no se aprueba ni se reintenta automáticamente. La fuente no demuestra una transacción atómica global.
- Anulación de transferencia y rol restringido requieren ruta/permiso calibrados; no asumir que anular un remito de compra revierte una transferencia de dos lados.

## Evidencia y límites

Guardar cantidades iniciales/finales por sucursal, identidad/estado del documento y movimientos enlazados. El cierre de la ventana no acredita éxito. El listado de stock es evidencia adicional P1; la conservación de existencias es P0. No probar sincronización ni recepción por red en esta ficha.

## Recuperación

Antes de confirmar, usar la cancelación visible. Tras confirmar o ante timeout, consultar por identidad y conciliar stock antes de repetir. No generar una transferencia inversa para ocultar el fallo. Conservar el diagnóstico y restaurar la VM/baseline para la siguiente variante.

## Anexo técnico y trazabilidad

Fuente ERP: commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`.

- `src/ModuloStocks/Vistas/FormNuevaTransferencia.java:440-480,522-565`: leyenda, validaciones, confirmación y salida.
- `src/ModuloProductos/Entidades/Compra.java:539-595`: cierre y procesamiento sucesivo de envío/recepción.
- `src/ModuloProductos/Entidades/CompraDetalle.java:277-365`: detalle recibido, Suma stock, origen/destino.
- `src/ModuloPrincipal/Vistas/AppXGestion.java:4023-4033`: acceso a transferencias sujeto a cierre anual.
- `test/ModuloStocks/Vistas/FormNuevaTransferenciaValorizacionPolicyTest.java` y `TransferenciaValorizacionPolicyTest.java`: apoyo de valorización, no prueba del circuito completo.

Selectores, lector de movimientos y baseline pendientes. Registrar JAR/paquete/perfil; INFO resume, DEBUG muestra acciones y TRACE solo diagnóstico saneado.

