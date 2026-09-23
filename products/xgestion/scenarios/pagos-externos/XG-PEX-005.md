---
{"id":"XG-PEX-005","title":"Confirmar un cobro Point con pago e importe correspondientes a la venta","product":"xgestion","module":"pagos-externos","tags":["xgestion","regression","pagos-externos","cobros","dispositivos","recuperacion"],"status":"planned"}
---

# XG-PEX-005 — Confirmar un cobro Point con pago e importe correspondientes a la venta

## Objetivo

Aceptar el pago del terminal cuando esté aprobado para el importe y operación correctos, distinguiendo un intento enviado de un cobro.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 6.** Ver [mapa de facturación y pagos externos](../../docs/facturacion-pagos-externos.md). Sin suite Robot, seed nuevo ni validación real del JAR. Los resultados son criterios por comprobar, no resultados obtenidos.

Point Smart integrado, distinto del registro manual por Posnet. Requiere dispositivo/cuenta de prueba y contrato compatible; su disponibilidad sandbox debe acreditarse antes de habilitar la ficha.

## Precondiciones y datos

- **Laboratorio futuro, todavía no disponible:** Windows QA exclusivo, JAR/paquete identificados, base sintética y servicios de homologación/sandbox. Faltan adaptación del runner, política de red acotada, perfiles, oráculos y calibración. La v1 exige red desconectada: estas fichas no autorizan reconectar la VM, desactivar guardas ni operar contra producción.
- Los alias QA-FEL/QA-PEX son datos propuestos **NO creados**; no representan identidades fiscales, cuentas de pago, certificados ni credenciales válidas. El seed comercial actual no prepara esta batería. El paquete privado deberá aportar las identidades de prueba aceptadas y su manifiesto.
- Declarar empresa, sucursal, puesto, operador, cliente, moneda, medio e identidad de la operación. Mantener otra operación de control. Sin promociones, cuenta corriente, cuotas, emisión combinada con pago externo ni impresión/envío de comprobantes salvo una variante definida.
- Preparar una consulta independiente y autorizada del estado remoto por identidad y su correspondencia local. Si falta esa consulta, el caso queda BLOQUEADO: el mensaje de la UI, un request o un mock no acreditan autorización/cobro.
- QA-PEX-POINT: venta ARS 2.000 y terminal Point QA dedicado a su puesto; otra venta ARS 500 y otro terminal/contexto como controles si el laboratorio los incorpora.
- Respuesta inicial con intención de pago aún pendiente, posterior pago aprobado ARS 2.000 e ID externo verificable.
- Variantes independientes: importe informado ARS 1.999 (diferencia clara), monto ausente y estado final sin ID. La capacidad de producir cada respuesta en el servicio de pruebas está pendiente; no presentarla como disponible.

## Pasos y resultados esperados

| Acción del usuario | Resultado esperado |
| --- | --- |
| Seleccionar Point integrado y enviar un intento desde el cierre. | El terminal/intención muestra ARS 2.000 y contexto esperado. Un request aceptado o intención creada no marca la venta como pagada. |
| Mantener el intento pendiente y revisar la venta. | No hay cierre definitivo por sólo esperar el terminal; se conserva la identidad del intento para su consulta. |
| Completar el pago de prueba y esperar la confirmación. | Aprobación e importe ARS 2.000 coinciden con el extremo de pago, sin error; se conserva el ID externo y se cierra una sola venta/cobro. |
| Consultar la venta y el pago confirmado nuevamente. | Un solo pago relacionado; importes/medio/contexto coinciden y las operaciones de control siguen iguales. |
| En el baseline de importe ARS 1.999, recibir la respuesta discrepante. | Se informa diferencia y no se aprueba como cobro válido de ARS 2.000. Conservar ambos importes; no completar manualmente el faltante para hacer pasar el caso. |

## Variantes, límites y recuperación del recorrido

- El estado técnico processed/finished no acredita por sí solo pago approved; si hay un ID, la ruta puede consultar detalle. No aprobar un terminal finalizado sin pago identificable.
- La fuente permite continuar cuando falta el importe en algunas respuestas. **Oráculo de importe ausente pendiente:** sin evidencia remota independiente de ARS 2.000, no aprobar la integración. Registrar el riesgo sin afirmar un defecto ya reproducido.
- La tolerancia técnica es una configuración/regla que debe fijarse en el perfil; usar ARS 1 de diferencia en el caso base evita apoyar el resultado en centavos no acordados.
- Comisiones, liquidación bancaria, cuotas de tarjeta, devolución y contracargo no están cubiertos por esta confirmación.

## Evidencia y recuperación común

Registrar por separado solicitud, estado remoto y estado local, con importe, moneda, identidad completa y marcas de tiempo; comprobar otra operación sin cambios. Una confirmación ambigua requiere conciliación antes de reintentar. No cargar otro cobro, volver a emitir ni corregir registros para obtener un aprobado.

Conservar evidencia antes de recuperar el baseline. Restaurar la base local no borra comprobantes ni pagos del servicio de pruebas: el procedimiento del laboratorio debe tratar ambos extremos y conservar sus vínculos. No publicar certificados, tokens, credenciales, documentos personales, XML/payloads fiscales, QR utilizables ni respuestas/filas completas. Los logs crudos del ERP permanecen privados y deben sanearse antes de incorporarlos al informe.

Antes de automatizar: preparar datos/oráculos, calibrar controles accesibles sobre el SHA256 del JAR y acordar el procedimiento de fallo/recuperación. No usar coordenadas fijas ni ampliar a estas pantallas el permiso de doble clic de Venta. INFO resume, DEBUG describe pasos y TRACE aporta diagnóstico saneado. Un fallo conserva paso, esperado, observado, categoría y evidencia; causa no determinada si falta prueba causal.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Rutas relativas a XGestion2:

- `src/Integraciones/MercadoPago/Vistas/DialogMercadoPagoPointSmart.java:181-218,299-321`: inicio y resultado.
- `src/Integraciones/MercadoPago/Vistas/DialogMercadoPagoPointSmart.java:401-419,494-561`: confirmación y estados finales.
- `src/Integraciones/MercadoPago/Vistas/DialogMercadoPagoPointSmart.java:600-631`: controles de importe y monto ausente.
- `src/ModuloVentas/Vistas/Dialogs/formTicketCierre.java:1032-1045,2014-2025`: diálogo Point e identidad externa.
- `test/Integraciones/MercadoPago/Utils/PointSmartDisponibilidadTest.java`: disponibilidad de ruta; no valida terminal real.

Los tests citados descubren reglas y riesgos; no prueban la integración de extremo a extremo. Registrar además commit del harness, versión/SHA256 del JAR, paquete, perfil y reporte privado. La disponibilidad y el contrato vigente de cada servicio de pruebas deben verificarse antes de habilitarlo; esta ficha no certifica su disponibilidad actual.

