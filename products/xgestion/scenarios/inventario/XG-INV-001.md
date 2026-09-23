---
{"id":"XG-INV-001","title":"Ajustar ingresos y egresos de stock con motivo y cantidades válidas","product":"xgestion","module":"inventario","tags":["xgestion","regression","inventario","stock","permisos"],"status":"planned"}
---

# XG-INV-001 — Ajustar ingresos y egresos de stock con motivo y cantidades válidas

## Objetivo

Registrar una corrección de existencias en la sucursal elegida, pudiendo rechazarla antes de guardar y comprobar qué cantidad cambió y por qué.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P0; inventario, etapa 6.** Ver [mapa de inventario y respaldos](../../docs/inventario-respaldos.md). No tiene Robot ni evidencia de ejecución real. La lectura del listado es una comprobación P1 dentro de un circuito cuya integridad es P0.

## Precondiciones y datos

- Windows QA exclusivo y offline, JAR identificado, cierre anual íntegro y baseline restaurable. Sin sincronización, facturación, impresión ni dispositivos.
- **Fixtures sintéticos nuevos, NO creados:** QA-INV-A stockeable por unidad: S1 = 10,000 y S2 = 20,000; QA-INV-MP stockeable en kg: S1 = 2,500. Otra empresa conserva A = 30,000 como control. Estos datos no se presuponen disponibles en el seed comercial.
- Operador autorizado; perfil restringido y permiso concreto de acceso pendientes de identificar/calibrar. Usar el control Guardar identificado por accesibilidad; no dar por exclusivo Alt+G, pues la fuente asigna ese mnemonic también al enlace de tutorial.
- Motivos públicos: «Conteo QA ingreso» y «Merma QA». Los puntos decimales internos se presentan aquí con coma para el lector.

## Pasos y resultados esperados

| Acción del usuario | Resultado esperado |
| --- | --- |
| Abrir Ajuste rápido stock, elegir S1/A e intentar guardar sin cantidad o sin motivo. | Señala campos obligatorios; A sigue en 10,000, sin movimiento por el intento incompleto. |
| Completar ingreso 3,000 y motivo; pedir Guardar y rechazar la confirmación. | Conserva la propuesta editable, A sigue en 10,000 y no registra ajuste. |
| Guardar la misma propuesta y aceptar. | A pasa a 13,000 en S1; un ingreso de 3,000 con motivo/operador. S2 y otra empresa no cambian. |
| Volver a seleccionar A, indicar egreso 2,000 y motivo; confirmar. | A queda en 11,000; un egreso de 2,000, sin repetir el ingreso anterior. |
| Elegir materia prima MP y confirmar egreso 0,125. | MP queda en 2,375 kg; el historial conserva cantidad y unidad. A permanece en 11,000. |
| Cerrar y reabrir el listado de stock de S1 y S2. | Persisten las existencias finales y su ámbito; consultar no genera movimientos nuevos. |

## Variantes y dependencias

- Desde baselines separados: rechazar cantidad negativa, texto no numérico, 1,1234 y 10.000.000,000. Si el control impide introducirlos, registrar el rechazo visible y verificar que no persisten; no inyectarlos por API.
- Límite exacto: artículo de stock inicial 0,000 admite ingreso 9.999.999,999; desde 9.999.999,000 debe rechazar ingreso 1,000 porque el resultado excede el rango. No reutilizar este baseline para otros casos.
- **Cero está admitido por la validación actual.** No exigir un mensaje de rechazo inventado: verificar saldo sin cambio; el criterio de registrar u omitir un movimiento de cantidad cero queda pendiente de acordar.
- El stock final negativo dentro del rango también está admitido. No trasladar a ajustes un bloqueo comercial de Venta sin verificar su configuración.
- Repetir S2 como destino elegido. El signo/resultado esperado depende del saldo de esa sucursal, no del último artículo mostrado.
- La variante de rol restringido requiere permiso verificable y resultado acordado antes de automatizarla.

## Evidencia y límites

Conservar producto, unidad, sucursal, saldo inicial/final, cantidad, motivo y confirmación aceptada/rechazada. Contrastar movimientos por identidad y delta; no inferir persistencia porque se limpiaron los campos. Controles por teclado/JAB y lector de existencias pendientes. Un fallo informa paso, esperado/observado y evidencia saneada aun en INFO.

## Recuperación

Rechazar la confirmación permite corregir sin movimiento. Si Guardar devuelve un resultado ambiguo, consultar el historial antes de repetir: no compensar ni reintentar a ciegas. Conservar evidencia y restaurar el baseline del laboratorio para cada variante.

## Anexo técnico y trazabilidad

Fuente ERP: commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`.

- `src/ModuloStocks/Vistas/FormStockAjuste.java:89-108,165-207,210-253`: campos, confirmación, sucursal, decimales y rango.
- `src/ModuloPrincipal/Vistas/AppXGestion.java:3512-3519`: acceso sujeto al cierre anual.
- `test/ModuloStocks/Vistas/FormStockAjusteValidationTest.java:13-47`: rango, precisión y stock negativo.

Registrar SHA256 del JAR, paquete, perfil y reporte privado. SQL queda limitado al futuro oráculo de lectura; esta ficha no aplica datos ni modifica el ERP.
