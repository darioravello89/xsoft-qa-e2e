---
{"id":"XG-RES-034","title":"Proteger una mesa cuando llega otra ronda durante el cobro","product":"xgestion","module":"restobar","tags":["xgestion","regression","restobar","varios-puestos","mesas","cobros","mozos-qr"],"status":"planned"}
---

# XG-RES-034 — Proteger una mesa cuando llega otra ronda durante el cobro

## Objetivo

Proteger una mesa cuando llega otra ronda durante el cobro, desde la perspectiva del mozo, cajero o supervisor que opera el pedido.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 5 con dependencia de laboratorio de etapa 6.**
Referencia de planificación: **R19**. Ver [mapa de Restobar](../../docs/restobar.md).
No tiene suite Robot, seed automático ni validación real del JAR. Los resultados siguientes son criterios esperados, no resultados obtenidos.

## Precondiciones y datos

- Paquete QA sintético, Windows exclusivo y escritorio visible. La preparación de carta, mesas, ingredientes, permisos y perfiles de este caso está **pendiente**; `catalogo-comercial-v1` no certifica estos datos.
- Perfil local por defecto: ARS, comprobante interno no fiscal, impuestos y cubiertos $0 salvo indicación, sin ofertas, listas ni beneficios adicionales. Las integraciones se habilitan solo en el laboratorio indicado.
- Dos participantes QA; cuenta A de $1.000, nueva ronda B de $500. Pausas de coordinación reproducibles del laboratorio y política de rechazo/reintento definida.
- Laboratorio concurrente pendiente; no simular participantes con edición directa de tablas.
- Preparar y registrar antes de ejecutar los IDs propios de empresa, sucursal, puesto, cuenta, mesa y productos. Mantener una operación de control ajena al caso para verificar aislamiento.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Desde caja abrir el cobro de A y mantenerlo sin confirmar. | Se identifica la cuenta y total de $1.000 en proceso de cierre. |
| Desde el mozo enviar la ronda B. | La coordinación protege el cierre; no se inserta silenciosamente una ronda fuera del importe cobrado. |
| Cancelar el cobro y reintentar B conforme al resultado informado. | A y B pueden quedar en una cuenta abierta de $1.500 una sola vez si el protocolo autoriza el reintento. |
| Restaurar y repetir confirmando el cierre antes de procesar B. | El pago del pedido cerrado permanece único; el canal recibe el resultado previsto para cuenta cerrada, sin anexar consumos al histórico. |

## Variantes y límites

Orden inverso (ronda aceptada antes del cierre), timeout y retransmisión; verificar ambas pantallas y los eventos de coordinación. Congelar la política de cada orden antes de automatizar.

## Dependencias para automatizar

Preparar el baseline privado reproducible y sus datos, declarar el perfil, calibrar acciones accesibles sobre el SHA256 del JAR y construir comprobaciones por identidad. Utilizar atajos/acciones accesibles verificados; no tomar una posición de pantalla como identidad. Si el control o laboratorio no está disponible, mantener el caso pendiente y explicar el bloqueo.

## Evidencia y límites

Conservar UI y valores esperados/observados de cada transición. En una cuenta abierta distinguir lo guardado de lo cobrado: salir de la pantalla no es abandonar la venta. Registrar por separado **estado de cuenta, ocupación de mesa y estado de cocina** cuando apliquen.

Comparar operaciones, consumos, opciones, importes y efectos de stock/pagos por identidad y deltas según el caso, con lecturas autorizadas y saneadas. Las salidas de cocina, fiscalización y dispositivos requieren evidencia del extremo receptor; un log o test unitario no la sustituye. Registrar versión/SHA256 del JAR, commit del harness, paquete, perfil, IDs y reporte privado.

## Recuperación

Ante una discrepancia conservar primero la evidencia y cancelar o retomar por la interfaz según los pasos del caso. No borrar ni corregir registros comerciales para obtener un resultado aprobado. Restaurar el baseline QA antes de otra variante; para un cierre de resultado ambiguo conciliar la operación antes de reintentar, evitando cobrar o consumir ingredientes dos veces.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas relativas a XGestion2:

- `src/ModuloRestobar/AppMozo/MesaCierreProteccion.java`
- `test/ModuloRestobar/AppMozo/MesaCierreProteccionTest.java`
- `src/ModuloRestobar/Vistas/formTicket.java`

La lectura de fuente/tests orienta el riesgo y el criterio; no acredita la ejecución del artefacto. INFO resume, DEBUG describe acciones de negocio y TRACE añade diagnóstico saneado. Un fallo conserva paso, esperado, observado, categoría y evidencia; causa no determinada si falta prueba causal. No registrar credenciales, filas completas ni configuración privada.

