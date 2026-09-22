# Promociones simples: primer lote E2E

## Objetivo y alcance

Continuar la etapa 2 autorizada del roadmap con siete recorridos independientes,
XG-PRM-001 a XG-PRM-007, agrupados en `promociones` y `regression`.
Perfil: ARS, efectivo exacto, comprobante interno 99, sin impresión ni fiscalización,
stock suficiente y productos de `catalogo-comercial-v1`. Validación real del JAR pendiente.

| Caso | Ejemplo seed | Cantidad inicial / total ARS | Cantidad final / total ARS |
| --- | --- | --- | --- |
| XG-PRM-001 | PCT-Q3 | 1 / 900 | 3 / 2700 |
| XG-PRM-002 | IMP-Q3 | 1 / 850 | 3 / 2550 |
| XG-PRM-003 | 2X1-Q3 | 1 / 1000 | 3 / 2000 |
| XG-PRM-004 | 2DA50-Q3 | 1 / 1000 | 3 / 2500 |
| XG-PRM-005 | EXPIRADA | 2 / 2000 | 1 / 1000 |
| XG-PRM-006 | FUTURA | 2 / 2000 | 1 / 1000 |
| XG-PRM-007 | INACTIVA | 2 / 2000 | 1 / 1000 |

Cada recorrido carga el producto, edita la misma línea por Ctrl+E, observa su
recálculo, cancela el cobro sin persistencia, retoma y cobra una sola vez.
Compara producto, cantidad, precio base, subtotal bruto, oferta y neto con
expectativas públicas fijas. No reproduce el algoritmo comercial del ERP.

En los tres casos sin oferta se exige antes un control positivo: PCT × 1 = 900,
seguido de abandono sin efectos. Si el control falla, el caso no continúa.

## Contrato y límites

La calibración privada debe declarar `promociones-v1`, `ventas-etapa1` y
`ventas-teclado-v1` para el SHA256 del JAR. La configuración comercial debe excluir
otros descuentos, listas y beneficios. La columna de oferta y los importes
requieren observación JAB; no inventar selectores ni habilitar features por fuente.
El seed se prepara después de restaurar la base QA y antes de abrir XGestion.
Las fichas lo declaran mediante `seed`; el runner resuelve esa dependencia también
desde el menú y por ID, sin exigir un flag adicional. Dry-run sólo describe los datos.
No mutar configuración o datos de negocio desde los keywords.

La persistencia conserva `vecPrecio=1000` y `vecTotal=cantidad×1000`; `vecOferta`
registra la oferta. Comprobar neto, identidad de oferta, ausencia de otros descuentos,
un único cobro, stock y caja mediante SELECT acotados al contexto y la operación.
Fuente ERP: `925589278503f2d339beeb0a79f773c605512dd8`; seed: `pricing.py`.

## Plan y aceptación

1. Contrato y pruebas: bloquear perfil incompleto, seed ausente o calibración
   incompatible; expectativas estáticas y oráculo de descuentos, con pruebas RED/GREEN.
2. Recorridos: biblioteca específica de promociones que reutiliza sesión, driver,
   cancelación y diagnósticos; siete fichas y casos Robot, sin cambiar los nueve de Venta.
3. Cobertura y revisión: README, roadmap y matriz actualizados; regenerar Excel/JSON;
   revisión independiente y comprobaciones técnicas. Registrar pendiente JAR real.

INFO conserva el resumen; DEBUG muestra acciones comerciales y TRACE diagnóstico
saneado. Una discrepancia debe indicar paso, esperado y observado, sin volcar filas
privadas. No agregar dependencias, cambiar aislamiento ni modificar el ERP.

## Comandos y validación

```powershell
.\qa.cmd list --product xgestion --group promociones
.\qa.cmd run --product xgestion --group promociones --seed catalogo-comercial-v1 --log-level DEBUG
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m robocop check products
.\.venv\Scripts\python.exe -m pytest
.\qa.cmd check
.\qa.cmd coverage
.\qa.cmd coverage --check
.\qa.cmd run --product xgestion --group regression --dry-run
```

Tests del framework cubren rechazo de datos, discrepancias, recálculo, cancelación
sin mutaciones, identidad de producto/oferta y ausencia de pagos duplicados. Los
controles existentes de procesos y saneamiento deben seguir pasando. No confundir
dobles de UI ni dry-run con aceptación real sobre el FAT JAR.
