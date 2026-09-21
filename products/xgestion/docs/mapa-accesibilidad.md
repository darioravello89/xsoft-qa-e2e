# Mapa de teclado y accesibilidad de XGestión

Este mapa describe el contrato previsto por la implementación del checkout ERP. Los nombres y atajos deben observarse nuevamente mediante Java Access Bridge en el FAT JAR exacto antes de registrar `ventas-teclado-v1`; la fuente y los tests técnicos no constituyen un PASS del producto.

| Pantalla | Acción o control | Atajo y contexto | Nombre accesible estable | Escenario relacionado |
| --- | --- | --- | --- | --- |
| Acceso | Usuario / Contraseña / Ingresar | Tab y Shift+Tab; Enter activa Ingresar | `Usuario`, `Contraseña`, `Ingresar` | XG-INI-001, XG-AUT-001/002 |
| Principal | Contexto actual | Sin atajo; contenido dinámico | Descripciones `Empresa actual`, `Sucursal actual`, `Usuario actual` | XG-AUT-002 |
| Productos | Buscar | Enter desde la búsqueda | `Buscar productos` | XG-PRO-001/002 |
| Productos | Resultados | Flechas arriba/abajo cuando corresponde | `Resultados de productos` | XG-PRO-001/002 |
| Venta | Código / cantidad previa | Enter conserva la carga existente; con teclado numérico activo, `*` confirma | `Código y cantidad`, `Cantidad` | XG-VEN-001–009 |
| Venta | Editar renglón seleccionado | `Ctrl+E` con Venta activa; botón y doble clic ejecutan la misma acción | `Editar renglón` | XG-VEN-003/007; XG-ACC-001 |
| Venta | Grilla y total | Flechas seleccionan; Tab recorre grilla y acciones | `Renglones de la venta`, `Total` | XG-VEN-001–009 |
| Editor | Cantidad / Guardar / Cancelar | Enter Guardar; Escape Cancelar | `Producto del renglón`, `Cantidad del renglón`, `Guardar cambios`, `Cancelar edición` | XG-VEN-003/007 |
| Cobro | Importe / Cobrar / Cancelar | F1 Descuento, F2 Pago múltiple, F3 Forma de cobro, F4 Importe; F5/F6/F7 sólo si la integración visible está disponible; Enter Cobrar; Escape Cancelar | `Importe recibido`, `Cobrar venta`, `Cancelar cobro` | XG-VEN-001/005/006/007 |
| Confirmación | Aceptar / Cancelar o rechazar | Enter Aceptar; Escape Cancelar/Rechazar | `Aceptar confirmación`, `Cancelar confirmación` | XG-VEN-002/007/009 |

En Venta normal se mantienen F1 Productos, F2 Forma de pago, F3 Lista, F4 Imprimir cuando está habilitado, F5 Presupuesto, F6 Cobrar/Cerrar, F7 Cuenta corriente, F8 Cliente, F9 Factura electrónica, F10 Peso, F11 Consulta, F12 Comprobante y Escape Abandonar. Con `venta.atajosNumericos`, Num1–Num9/Num0 reemplazan F1–F10; F3, F11, F12, Escape y Ctrl+E permanecen. Cuando Código consume el teclado numérico, la leyenda muestra `Numérico: cantidad · * confirmar` en lugar de anunciar acciones numéricas inaccesibles desde ese foco.

Las leyendas visibles y los tooltips derivan de las mismas acciones/bindings. Los atajos de fondo tienen alcance de la ventana de Venta y no deben dispararse detrás de diálogos modales. Cancelar edición, cancelar cobro y rechazar abandono son acciones distintas.

## Estado de verificación

- Implementación y pruebas técnicas: realizadas en `release/189-lts`, commit ERP `488b91d2a36ba469c975c0132a029f7a0380e5d2`.
- SHA256 de FAT JAR y observación JAB: pendientes por falta del paquete/laboratorio privado.
- `ventas-teclado-v1`: no habilitada hasta recalibrar `sale.edit` y `editor.cancel` para el JAR exacto.
- Restobar: sólo recibe las mejoras de diálogos compartidos. Sus brechas propias permanecen en el [backlog](backlog-accesibilidad.csv) y no forman parte de los casos ejecutables de Venta.
