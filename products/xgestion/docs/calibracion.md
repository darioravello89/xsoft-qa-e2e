# Calibrar Java Access Bridge

Este paso lo hace una persona responsable del paquete QA una vez por JAR/perfil UI. El resto del equipo importa el paquete ya verificado. No marcar `verified` por revisar código ni por ejecutar unit tests.

Para los [trece listados del commit 3f8648035](atajos-listados.md), la calibración
está pendiente. El [artefacto exacto](evidencia-atajos-3f8648035.md) ya se
construyó. Identificar buscadores, tablas, leyendas, destinos y modales por
nombre/rol/estado en ese JAR; verificar foco sin forzarlo tras el atajo.
No reutilizar supuestos sobre columnas ID ocultas de otras suites. Registrar
identidad visible y comprobarla en la ficha abierta. Orden, X nativa y recarga
única requieren evidencia propia; si no son observables, conservar BLOQUEADO.

El lote de siete promociones requiere además la [calibración promociones-v1](promociones.md),
con columnas separadas de bruto, oferta y neto y edición por teclado. La calibración
de Venta cotidiana por sí sola no habilita ese lote. El catálogo completo tiene
99 casos: cinco de smoke, nueve de Venta cotidiana, 82 de promociones y tres circuitos. Los 70 nuevos requieren el [contrato de canastas](canastas-ofertas.md).

1. Preparar la VM Windows con escritorio interactivo desbloqueado, JDK 17 de 64 bits, JAB/DLL de 64 bits y el paquete QA válido. Después de setup, desconectar la red y crear un snapshot limpio antes de ejecutar el JAR; en PC física, una imagen recuperable equivalente. Ejecutar el doctor del repositorio. Si el único bloqueo pendiente es la calibración inicial, continuar con `inspect`, que mantiene los demás controles. La instancia MySQL debe ser exclusiva: el ERP configura variables globales del servidor al arrancar.
2. Usar `qa.cmd inspect` para obtener el árbol inicial. La inspección arranca su propio JAR; permite navegar e ingresar manualmente en la UI. Pulsar Enter en la consola captura la estructura de sus ventanas actuales; `q` termina y cierra sólo ese proceso. Nunca escribir credenciales en consola. No hay capturas de imagen ni valores de campos: éstos omiten nombres/descripciones; también se redactan secretos conocidos del perfil.
3. Confirmar que JAB ve la ventana y los controles de acceso. Si no ve el árbol, detener la aceptación: ésta es una falla de viabilidad, no un test aprobado. Verificar JAB habilitado para el runtime seleccionado y compatibilidad JDK/DLL; no sustituir por coordenadas fijas.
4. Usar las estructuras `jab-snapshot-NN.json` para completar ventanas y selectores observados. Recorrer manualmente login correcto/incorrecto, productos, venta no fiscal/efectivo y cancelación. El inspector sólo observa; estas acciones manuales ocurren en la instancia QA restaurable. Un selector de ejemplo como `role:push button and name:ENTRAR` es una hipótesis hasta observarlo en ese JAR.
5. Verificar cada selector exacto (`strict=True`) y que encuentre exactamente un elemento visible. Formularios Swing pueden repetir nombres en pestañas ocultas; incluir jerarquía/rol/nombre/índice estructural observado en el selector, nunca elegir el primer resultado de una lista.
6. Completar fixtures con textos UI reales, identidad y producto del dump. No exportar contraseñas ni árboles sin sanear. Nunca añadir capturas o valores reales al ejemplo público.
7. Documentar responsable, fecha, versión JAB y SHA256 del JAR; cambiar la calibración privada a `verified`. Importar el mapa con `qa.cmd calibrate --locators RUTA_AL_MAPA_VERIFICADO.json`: el runner actualiza solamente mapa y su hash, conservando JAR/base/credenciales. Este registro afirma calibración humana, no reemplaza el siguiente smoke automatizado. Para distribuir el paquete final al resto del equipo, incorporarlo al ZIP privado y recalcular su manifest.
8. Completar la extensión de Venta cotidiana descrita abajo antes de habilitar sus siete casos nuevos. Ejecutar los grupos `smoke` y `ventas` (catorce casos en conjunto) con restauración previa y egress bloqueado; los siete iniciales pueden aceptarse por separado con un paquete anterior. Para PRM-001..007 completar el contrato de promociones; para los otros 70, la [calibración de canastas](canastas-ofertas.md). `regression` selecciona 99 casos implementados. Validar el resumen del runner, detalle Robot y evidencias posteriores al login. Repetir la corrida desde baseline para confirmar independencia.

## Verificar la extensión `ventas-etapa1`

Preparar el [contrato `sales_journeys`](paquete.md) en el paquete privado. No inferir sus textos o valores desde ejemplos públicos. Si cambia `fixtures.json`, producir una versión nueva del paquete e importarla en un nuevo clon normal; `calibrate` modifica solamente los localizadores.

1. Abrir una venta nueva y registrar cliente, lista y comprobante predeterminados. Leer la grilla vacía. Cargar una unidad del fixture y comprobar código, nombre, cantidad 1, precio 1000 e importe final 1000. Mapear `sale.lines.column_count` y sus cinco columnas contra la tabla completa observada por JAB; distinguir código visible de ID interno y total final de subtotal.
2. Ingresar el código ausente del fixture. Registrar `unknown_notice: status` o `dialog` y el texto exacto accesible. Para diálogo, verificar `sale.unknown_dismiss`. La grilla debe permanecer igual; agregar otra unidad válida y registrar si la consolidación genera 1 o 2 filas, con cantidad total 2 e importe 2000.
3. Abrir efectivo y verificar `payment.total`, `payment.amount`, `payment.change`, `payment.confirm` y `payment.cancel`. Ingresar 3000, sacar el foco del importe y leer vuelto 1000/total 2000 antes de confirmar. No mezclar el formato de la grilla con los decimales del diálogo.
4. Cancelar un cobro antes de confirmar y comprobar que retorna a las mismas líneas y total. Calibrar por separado salir de Venta, aceptar abandono y rechazarlo: en la fuente de referencia “Cerrar” cobra, mientras Escape pide abandonar; la confirmación tiene “Aceptar” y “Cancelar”.
5. Cobrar una venta y comprobar el reinicio automático de **la misma ventana**: filas vacías, cantidad 1, total cero y defaults registrados. No abrir otra ventana para aprobar esta comprobación. Después de abandonar, abrir una nueva venta desde el menú, sin reiniciar el proceso, y comprobar esos defaults nuevamente.
6. Identificar la grilla y una única línea del fixture mediante JAB. Verificar columnas, selección y foco. En un JAR que exponga la mejora, calibrar `sale.edit` y `editor.cancel`, abrir con el botón Editar, comprobar que Cantidad recibe el foco, cancelar sin cambios y confirmar que vuelven la misma selección y el foco de la grilla. Reabrir con `Ctrl+E`, cambiar de 1 a 2, guardar y comprobar que sigue siendo la misma fila con total 2000. El doble clic queda como ruta legada sólo para paquetes anteriores.
7. Verificar además `sale.cancel_reject` en la confirmación de abandono y que la venta se conserva antes de editar/cobrar. Cancelar el cobro, retomarlo y confirmar una única vez; Enter no puede producir dos cobros.
8. Registrar `ventas-etapa1` después de comprobar los controles base sobre el hash del JAR. Agregar también `ventas-teclado-v1` únicamente cuando `sale.edit`, `editor.cancel`, foco, selección, Ctrl+E y ausencia de activación duplicada hayan sido observados en ese mismo artefacto. Importar el mapa verificado y ejecutar los casos por ID y en grupo. El registro de calibración no acredita por sí solo sus efectos de persistencia.

El inspector conserva estructuras privadas sin valores de campos sensibles; una captura del árbol no prueba que una tabla sea legible de forma completa. Verificar la lectura JAB y las acciones en el laboratorio, conservando evidencia privada saneada. XG-VEN-003/007 pertenecen al grupo `ventas`: con `ventas-teclado-v1` usan selección JAB, Cancelar y `Ctrl+E`; sin esa feature conservan temporalmente el doble clic legado. El [backlog de accesibilidad CSV](backlog-accesibilidad.csv) mantiene XG-ACC-001 a XG-ACC-005 pendientes de validación real y separa las mejoras propias de Restobar de los casos de Venta.

## Verificar accesibilidad de Restobar

Esta comprobación valida XG-ACC-002 a XG-ACC-005, pero no crea escenarios ejecutables ni permite declarar cubiertos R04/R08/R10/R13.

1. Abrir una cuenta con al menos dos consumos. Inspeccionar `Producto`, `Cantidad`, `Renglones del pedido`, `Editar` y las acciones F1-F12; confirmar nombre, rol, estado y valor sin depender de `setName`.
2. Ordenar la grilla si el JAR lo permite, seleccionar un consumo con flechas y abrirlo mediante botón y `Ctrl+E`. Sin selección, ambos deben quedar deshabilitados o ser no-op. El doble clic debe abrir la misma identidad.
3. En el editor confirmar foco y selección inicial en `Cantidad del consumo`. Pulsar Escape y verificar que no cambia el consumo y que vuelven selección, scroll y foco a la grilla. Reabrir, cambiar 1→2 y guardar una sola vez con Enter.
4. Recorrer con Tab y Shift+Tab producto, cantidad, grilla, Editar, búsqueda/paginación de familias, comprobante, notas y cada acción visible/habilitada de pedido, cocina, precuenta y cobro. Verificar que los controles ocultos o deshabilitados se omiten.
5. Abrir dos veces `FormOpcionesCierreMesa`: en la primera elegir una opción; en la segunda usar Escape y luego repetir cerrando con X. Ninguna cancelación debe reutilizar ni ejecutar la opción anterior. Verificar también 1/Num1 y 2/Num2.
6. Cancelar el cobro, continuar con la misma cuenta y retomarlo; confirmar una sola vez. Conservar evidencia privada saneada del árbol JAB, foco/selección y resultado comercial.
7. Registrar SHA256, versión JAB, perfil y fecha. Mantener XG-ACC-002 a XG-ACC-005 como `implementado_pendiente_validacion_jar` hasta completar todos los pasos sobre ese artefacto; no copiar una aprobación de otro JAR.

El adaptador usa acciones accesibles/teclado de los controles. No llama a `setProductoManual`, `TicketVenta`, métodos Java de dominio ni JDBC para generar la venta. Las consultas del oráculo son sólo `SELECT` parametrizados, acotados por empresa/sucursal/computadora y venta.

Al cambiar JAR, `app_sha256` deja de coincidir y la suite bloquea. Recalibrar y volver a aceptar; no copiar una firma de aprobación anterior. La extensión a otra versión o flujo de pagos exige fixture y mapa propios.

Conservar Windows offline después de la inspección y las pruebas. Antes de reconectarlo, guardar evidencia por un canal local privado y restaurar el snapshot o imagen limpia: cerrar el JAR no garantiza detener el agente persistente que puede instalar.

## Extensión P0 de ofertas USD

PRM-080..084 requieren [ofertas-usd-v1](ofertas-usd.md), además de canastas: originales USD, documento y cobro ARS, cotización 1500 y tres selectores monetarios del diálogo visibles. Calibrar los aliases nuevos para el SHA256 del JAR. No habilitar la extensión por copiar los ejemplos ni inferir moneda de importes sin unidad. Son cinco casos y trece variantes, todos con validación real pendiente.

## Circuitos de stock y dinero

Para FIN-011/013/014 agregar las capacidades y aliases de [circuitos-completos.md](circuitos-completos.md#perfil-privado-y-calibración). Validar columnas de remito, autenticación de turno, identidad del puesto y balance en el JAR. FIN-012 permanece pendiente hasta resolver ACC-010; no calibrar ni autorizar doble clic.
