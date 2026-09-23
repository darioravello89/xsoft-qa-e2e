---
{"id":"XG-PEX-002","title":"Confirmar transferencias de la venta sin contar canceladas o repetidas","product":"xgestion","module":"pagos-externos","tags":["xgestion","regression","pagos-externos","cobros","recuperacion","integridad-operaciones"],"status":"planned"}
---

# XG-PEX-002 — Confirmar transferencias de la venta sin contar canceladas o repetidas

## Objetivo

Cobrar con las transferencias correctas y suficientes, conservando su identidad y evitando aplicar dos veces el mismo dinero.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P0; etapa 6.** Ver [mapa de facturación y pagos externos](../../docs/facturacion-pagos-externos.md). Sin suite Robot, seed nuevo ni validación real del JAR. Los resultados son criterios por comprobar, no resultados obtenidos.

Transferencia Mercado Pago con cuenta de sandbox activa. El cierre requiere confirmación del operador sobre transferencias reconocidas; detectar una transferencia no equivale a aceptarla ni prueba que pertenezca a la venta.

## Precondiciones y datos

- **Laboratorio futuro, todavía no disponible:** Windows QA exclusivo, JAR/paquete identificados, base sintética y servicios de homologación/sandbox. Faltan adaptación del runner, política de red acotada, perfiles, oráculos y calibración. La v1 exige red desconectada: estas fichas no autorizan reconectar la VM, desactivar guardas ni operar contra producción.
- Los alias QA-FEL/QA-PEX son datos propuestos **NO creados**; no representan identidades fiscales, cuentas de pago, certificados ni credenciales válidas. El seed comercial actual no prepara esta batería. El paquete privado deberá aportar las identidades de prueba aceptadas y su manifiesto.
- Declarar empresa, sucursal, puesto, operador, cliente, moneda, medio e identidad de la operación. Mantener otra operación de control. Sin promociones, cuenta corriente, cuotas, emisión combinada con pago externo ni impresión/envío de comprobantes salvo una variante definida.
- Preparar una consulta independiente y autorizada del estado remoto por identidad y su correspondencia local. Si falta esa consulta, el caso queda BLOQUEADO: el mensaje de la UI, un request o un mock no acreditan autorización/cobro.
- QA-PEX-TR: venta ARS 2.000. Transferencias de prueba propuestas T1 ARS 800 y T2 ARS 1.200, con IDs distintos y titular/contexto acordados; T3 ARS 2.000 pertenece a otra operación de control.
- Baseline sin transferencias aplicadas. Medios sin recargo/vuelto, sin cuenta corriente ni pagos múltiples. Preparación, límites de selección por cuenta/empresa y oráculo de uso único todavía pendientes.

## Pasos y resultados esperados

| Acción del usuario | Resultado esperado |
| --- | --- |
| Abrir la escucha o selector y detectar T1; cancelar/rechazar su confirmación. | La detección no se registra como cobro confirmado; venta sin cierre y total confirmado del intento cancelado ARS 0. |
| Retomar el cobro, verificar identidad de T1 y aceptarla. | Quedan ARS 800 confirmados y ARS 1.200 por cobrar; no se cierra la venta como pagada totalmente. |
| Elegir T2 y confirmar después de verificar su identidad. | Total confirmado ARS 2.000 y un cierre comercial; ambos IDs quedan relacionados con la venta según el contrato, sin apropiarse de T3. |
| Consultar nuevamente venta, transferencias y operación de control. | Un solo pago neto ARS 2.000 en la venta; T3 y su operación conservan su estado. Consultar no vuelve a aplicar T1/T2. |
| En baseline independiente, intentar seleccionar T1 dos veces y luego reutilizarla en otra operación. | No se acredita como ARS 1.600 ni se paga otra venta con el mismo ID. Si la UI/servicio admite la duplicación, registrar discrepancia; la protección de uso único aún no está acreditada. |

## Variantes, límites y recuperación del recorrido

- Selección repetida, transferencia tardía tras timeout y transferencia detectada de importe distinto son variantes separadas con estado remoto controlado. No preparar resultados mediante edición de listas en memoria.
- El acumulador local revisado agrega transferencias; no demuestra deduplicación global ni reserva transaccional entre puestos. Esta ficha expresa un objetivo P0 pendiente y requiere verificar el contrato de identidad/uso antes de automatizar.
- Cancelar puede limpiar la selección local sin revertir una transferencia ya realizada en sandbox. Consultar ambos extremos antes de repetir o recuperar; no enviar otra transferencia por tener un diálogo vacío.

## Evidencia y recuperación común

Registrar por separado solicitud, estado remoto y estado local, con importe, moneda, identidad completa y marcas de tiempo; comprobar otra operación sin cambios. Una confirmación ambigua requiere conciliación antes de reintentar. No cargar otro cobro, volver a emitir ni corregir registros para obtener un aprobado.

Conservar evidencia antes de recuperar el baseline. Restaurar la base local no borra comprobantes ni pagos del servicio de pruebas: el procedimiento del laboratorio debe tratar ambos extremos y conservar sus vínculos. No publicar certificados, tokens, credenciales, documentos personales, XML/payloads fiscales, QR utilizables ni respuestas/filas completas. Los logs crudos del ERP permanecen privados y deben sanearse antes de incorporarlos al informe.

Antes de automatizar: preparar datos/oráculos, calibrar controles accesibles sobre el SHA256 del JAR y acordar el procedimiento de fallo/recuperación. No usar coordenadas fijas ni ampliar a estas pantallas el permiso de doble clic de Venta. INFO resume, DEBUG describe pasos y TRACE aporta diagnóstico saneado. Un fallo conserva paso, esperado, observado, categoría y evidencia; causa no determinada si falta prueba causal.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `daa002d597d0fa7380ace204d3727085c52d1415`. Rutas relativas a XGestion2:

- `src/ModuloVentas/Vistas/Dialogs/formTicketCierre.java:1085-1137`: aceptación, selección adicional y cancelación.
- `src/ModuloVentas/Vistas/Dialogs/formTicketCierre.java:1532-1658`: escucha, timeout y elección de transferencias.
- `src/ModuloVentas/Vistas/Dialogs/formTicketCierre.java:1669-1703,1934-1954`: total confirmado y acumulador.
- `test/ModuloVentas/Vistas/Dialogs/MercadoPagoCobroConfirmadoPolicyTest.java:15-28`: total confirmado integrado.

Los tests citados descubren reglas y riesgos; no prueban la integración de extremo a extremo. Registrar además commit del harness, versión/SHA256 del JAR, paquete, perfil y reporte privado. La disponibilidad y el contrato vigente de cada servicio de pruebas deben verificarse antes de habilitarlo; esta ficha no certifica su disponibilidad actual.

