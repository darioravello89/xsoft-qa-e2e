---
{"id":"XG-PEX-001","title":"Distinguir un cobro manual de la confirmación integrada de Mercado Pago","product":"xgestion","module":"pagos-externos","tags":["xgestion","regression","pagos-externos","cobros","recuperacion"],"status":"planned"}
---

# XG-PEX-001 — Distinguir un cobro manual de la confirmación integrada de Mercado Pago

## Objetivo

Saber cuándo el operador registra un pago declarado manualmente y cuándo el cierre requiere una transferencia confirmada por la integración.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 6.** Ver [mapa de facturación y pagos externos](../../docs/facturacion-pagos-externos.md). Sin suite Robot, seed nuevo ni validación real del JAR. Los resultados son criterios por comprobar, no resultados obtenidos.

Caso de frontera entre perfiles. No duplica promociones por medio de pago [PRM-074..076](../promociones/XG-PRM-074.md); esos recorridos offline no prueban el proveedor externo.

## Precondiciones y datos

- **Laboratorio futuro, todavía no disponible:** Windows QA exclusivo, JAR/paquete identificados, base sintética y servicios de homologación/sandbox. Faltan adaptación del runner, política de red acotada, perfiles, oráculos y calibración. La v1 exige red desconectada: estas fichas no autorizan reconectar la VM, desactivar guardas ni operar contra producción.
- Los alias QA-FEL/QA-PEX son datos propuestos **NO creados**; no representan identidades fiscales, cuentas de pago, certificados ni credenciales válidas. El seed comercial actual no prepara esta batería. El paquete privado deberá aportar las identidades de prueba aceptadas y su manifiesto.
- Declarar empresa, sucursal, puesto, operador, cliente, moneda, medio e identidad de la operación. Mantener otra operación de control. Sin promociones, cuenta corriente, cuotas, emisión combinada con pago externo ni impresión/envío de comprobantes salvo una variante definida.
- Preparar una consulta independiente y autorizada del estado remoto por identidad y su correspondencia local. Si falta esa consulta, el caso queda BLOQUEADO: el mensaje de la UI, un request o un mock no acreditan autorización/cobro.
- QA-PEX-A: venta nueva de dos unidades a ARS 1.000, total ARS 2.000, stock inicial 10 y caja sin movimiento de la venta.
- Dos baselines separados: sin cuenta Mercado Pago activa, cobro manual; con cuenta exclusiva de sandbox activa y cero transferencias confirmadas. En ambos se escribe inicialmente ARS 2.000 en el importe; sin cuenta corriente ni pagos múltiples.
- Preparación del perfil activo y consulta independiente de transferencias pendientes. Cambiar de perfil solo por el paquete QA, sin dar de alta o desactivar cuentas reales.

## Pasos y resultados esperados

| Acción del usuario | Resultado esperado |
| --- | --- |
| Con el perfil sin cuenta activa, seleccionar el medio Mercado Pago/transferencia y registrar ARS 2.000 manuales. | La ruta manual permite registrar el importe declarado; no se presenta como confirmación del proveedor ni exige inventar un ID de transacción remota. |
| Revisar evidencia local del cierre manual. | Una venta de ARS 2.000 y su registro local conforme al perfil; stock pasa de 10 a 8 una vez. El informe identifica este resultado como manual, sin acreditar dinero en Mercado Pago. |
| Restaurar el baseline integrado, elegir Transferencia e ingresar ARS 2.000 sin seleccionar transferencias confirmadas. | No permite cerrar como totalmente pagado por ese importe escrito: confirmado ARS 0, pendiente ARS 2.000. Venta sin cierre definitivo. |
| Cancelar el cobro integrado y consultar operación/control. | No se creó un pago externo ni una venta cerrada por el intento manual; productos y total quedan disponibles para continuar. |

## Variantes, límites y recuperación del recorrido

- La política diferenciada aplica a transferencia con cuenta activa. QR y Point tienen diálogos y comprobaciones propias en PEX-003/005; no generalizar esta validación a cualquier opción con nombre Mercado Pago.
- La existencia/selección de cuenta activa, usuario y puesto debe declararse; un nombre de medio no prueba que se haya usado integración.
- La variante manual puede ejecutarse offline cuando tenga automatización propia; esta ficha conjunta permanece planned y bloqueada para el perfil integrado hasta adaptar el runner.

## Evidencia y recuperación común

Registrar por separado solicitud, estado remoto y estado local, con importe, moneda, identidad completa y marcas de tiempo; comprobar otra operación sin cambios. Una confirmación ambigua requiere conciliación antes de reintentar. No cargar otro cobro, volver a emitir ni corregir registros para obtener un aprobado.

Conservar evidencia antes de recuperar el baseline. Restaurar la base local no borra comprobantes ni pagos del servicio de pruebas: el procedimiento del laboratorio debe tratar ambos extremos y conservar sus vínculos. No publicar certificados, tokens, credenciales, documentos personales, XML/payloads fiscales, QR utilizables ni respuestas/filas completas. Los logs crudos del ERP permanecen privados y deben sanearse antes de incorporarlos al informe.

Antes de automatizar: preparar datos/oráculos, calibrar controles accesibles sobre el SHA256 del JAR y acordar el procedimiento de fallo/recuperación. No usar coordenadas fijas ni ampliar a estas pantallas el permiso de doble clic de Venta. INFO resume, DEBUG describe pasos y TRACE aporta diagnóstico saneado. Un fallo conserva paso, esperado, observado, categoría y evidencia; causa no determinada si falta prueba causal.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Rutas relativas a XGestion2:

- `src/ModuloVentas/Vistas/Dialogs/MercadoPagoCobroConfirmadoPolicy.java:9-27`: manual frente a transferencias confirmadas.
- `src/ModuloVentas/Vistas/Dialogs/formTicketCierre.java:1669-1703`: validación del importe confirmado.
- `test/ModuloVentas/Vistas/Dialogs/MercadoPagoCobroConfirmadoPolicyTest.java:15-58`: perfiles activos/inactivos.

Los tests citados descubren reglas y riesgos; no prueban la integración de extremo a extremo. Registrar además commit del harness, versión/SHA256 del JAR, paquete, perfil y reporte privado. La disponibilidad y el contrato vigente de cada servicio de pruebas deben verificarse antes de habilitarlo; esta ficha no certifica su disponibilidad actual.

