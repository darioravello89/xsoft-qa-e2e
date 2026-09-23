---
{"id":"XG-RES-035","title":"Recibir pedidos QR con opciones válidas y política de pago","product":"xgestion","module":"restobar","tags":["xgestion","regression","restobar","mozos-qr","restobar-opciones","kds","pagos-externos"],"status":"planned"}
---

# XG-RES-035 — Recibir pedidos QR con opciones válidas y política de pago

## Objetivo

Recibir pedidos QR con opciones válidas y política de pago, desde la perspectiva del mozo, cajero o supervisor que opera el pedido.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 5 con dependencia de laboratorio de etapa 6.**
Referencia de planificación: **R20**. Ver [mapa de Restobar](../../docs/restobar.md).
No tiene suite Robot, seed automático ni validación real del JAR. Los resultados siguientes son criterios esperados, no resultados obtenidos.

## Precondiciones y datos

- Paquete QA sintético, Windows exclusivo y escritorio visible. La preparación de carta, mesas, ingredientes, permisos y perfiles de este caso está **pendiente**; `catalogo-comercial-v1` no certifica estos datos.
- Perfil local por defecto: ARS, comprobante interno no fiscal, impuestos y cubiertos $0 salvo indicación, sin ofertas, listas ni beneficios adicionales. Las integraciones se habilitan solo en el laboratorio indicado.
- Canal QR QA, mesa ocupada, grupo obligatorio Guarnición máx. 1; opción por peso min. 0,25/máx. 2/paso 0,25 y extra $40 por unidad. Perfiles pago al cierre y prepago separados.
- QR, backend y pagos sandbox autorizados; no usar proveedor real.
- Preparar y registrar antes de ejecutar los IDs propios de empresa, sucursal, puesto, cuenta, mesa y productos. Mantener una operación de control ajena al caso para verificar aislamiento.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Enviar plato sin guarnición obligatoria o con peso 0,30. | El canal rechaza el pedido inválido; XGestión no agrega un consumo parcial. |
| Elegir una guarnición y peso 0,75 válido, extra $30. | XGestión recibe cantidades, opciones e importes congelados de la ronda correcta. |
| Enviar otra ronda válida sobre la cuenta existente. | Se conserva la cuenta según política; no se confunde ronda nueva con otra mesa o pago. |
| Completar pago al cierre o prepago en su laboratorio y consultar KDS. | Se cumple la habilitación de cocina y el cobro propios del perfil, sin duplicar confirmaciones. |

## Variantes y límites

Grupo/opción ajenos, opción repetida, máximo de selecciones excedido, límites 0,25 y 2, peso 0/negativo/2,25; reenvío de la misma ronda. Las reglas QR no se atribuyen al picker Swing sin verificación.

## Dependencias para automatizar

Preparar el baseline privado reproducible y sus datos, declarar el perfil, calibrar acciones accesibles sobre el SHA256 del JAR y construir comprobaciones por identidad. Utilizar atajos/acciones accesibles verificados; no tomar una posición de pantalla como identidad. Si el control o laboratorio no está disponible, mantener el caso pendiente y explicar el bloqueo.

## Evidencia y límites

Conservar UI y valores esperados/observados de cada transición. En una cuenta abierta distinguir lo guardado de lo cobrado: salir de la pantalla no es abandonar la venta. Registrar por separado **estado de cuenta, ocupación de mesa y estado de cocina** cuando apliquen.

Comparar operaciones, consumos, opciones, importes y efectos de stock/pagos por identidad y deltas según el caso, con lecturas autorizadas y saneadas. Las salidas de cocina, fiscalización y dispositivos requieren evidencia del extremo receptor; un log o test unitario no la sustituye. Registrar versión/SHA256 del JAR, commit del harness, paquete, perfil, IDs y reporte privado.

## Recuperación

Ante una discrepancia conservar primero la evidencia y cancelar o retomar por la interfaz según los pasos del caso. No borrar ni corregir registros comerciales para obtener un resultado aprobado. Restaurar el baseline QA antes de otra variante; para un cierre de resultado ambiguo conciliar la operación antes de reintentar, evitando cobrar o consumir ingredientes dos veces.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas relativas a XGestion2:

- `test/ModuloRestobar/AppMozo/QrMesaOpcionesTest.java`
- `src/ModuloRestobar/AppMozo/QrMesaRoundProcessor.java`
- `test/ModuloRestobar/AppMozo/QrMesaPolicyTest.java`

La lectura de fuente/tests orienta el riesgo y el criterio; no acredita la ejecución del artefacto. INFO resume, DEBUG describe acciones de negocio y TRACE añade diagnóstico saneado. Un fallo conserva paso, esperado, observado, categoría y evidencia; causa no determinada si falta prueba causal. No registrar credenciales, filas completas ni configuración privada.

