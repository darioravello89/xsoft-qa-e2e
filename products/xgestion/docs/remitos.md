# Remitos de compra: carga, recepción y corrección

**24 recorridos documentados, todos pendientes de automatizar**: XG-REM-001..024. No agregan casos ejecutables ni evidencia real. Consultar el [Excel de cobertura](../../../docs/coverage/xgestion-cobertura.xlsx), el [roadmap](roadmap.md) y la [cobertura](cobertura.md).

La pantalla inspeccionada es **Carga de remito o factura**, utilizada para compras y recepción de mercadería. Un remito emitido desde Venta es otro circuito y necesita sus propias fichas; no queda cubierto por esta batería. Recibir materia prima prueba su ingreso; las recetas y su consumo pertenecen al circuito Restobar.

## Grupos para QA

| Grupo | Qué controla | Casos |
| --- | --- | --- |
| `remitos` / `compras` | Todos los remitos de esta batería. | 24 |
| `remitos-carga` | Cabecera, productos, materia prima, cantidades, bultos y validaciones. | 001..005, 011, 012 |
| `remitos-correccion` | Editar, confirmar/rechazar, borrador, descartar, lectura y anulación. | 006..010, 013, 024 |
| `remitos-stock` | Recepción, flags, bultos, destino y reversión. | 003, 005, 014, 023, 024 |
| `remitos-costos` | Costos, bonificaciones, proveedor/lista, impuestos y moneda. | 015..022 |

Los grupos se superponen: sumar sus cantidades duplica fichas. Para consultar:

```powershell
.\qa.cmd list --product xgestion --group remitos
.\qa.cmd list --product xgestion --group remitos-stock
.\qa.cmd list --product xgestion --groups
```

Permanecen `planned` hasta implementar Robot, datos y calibración. El menú debe mostrarlos pendientes, sin ofrecerlos como ejecutables.

## Mapa de recorridos

| Escenario | Grupo principal | Prioridad | Automatización |
| --- | --- | --- | --- |
| [XG-REM-001 — Recibir productos y confirmar un remito de compra](../scenarios/remitos/XG-REM-001.md) | remitos-carga | P0 | Pendiente |
| [XG-REM-002 — Buscar productos sin arrastrar una selección cancelada o inexistente](../scenarios/remitos/XG-REM-002.md) | remitos-carga | P1 | Pendiente |
| [XG-REM-003 — Recibir materia prima con cantidad fraccionaria y vencimiento](../scenarios/remitos/XG-REM-003.md) | remitos-carga | P0 | Pendiente |
| [XG-REM-004 — Corregir cantidad o costo faltante antes de agregar](../scenarios/remitos/XG-REM-004.md) | remitos-carga | P1 | Pendiente |
| [XG-REM-005 — Cargar bultos y conservar su equivalencia en unidades](../scenarios/remitos/XG-REM-005.md) | remitos-carga | P0 | Pendiente |
| [XG-REM-006 — Editar un renglón y eliminar otro antes de recibir](../scenarios/remitos/XG-REM-006.md) | remitos-correccion | P0 | Pendiente |
| [XG-REM-007 — Rechazar la confirmación y continuar el mismo remito](../scenarios/remitos/XG-REM-007.md) | remitos-correccion | P0 | Pendiente |
| [XG-REM-008 — Guardar un borrador y retomarlo antes de confirmar](../scenarios/remitos/XG-REM-008.md) | remitos-correccion | P0 | Pendiente |
| [XG-REM-009 — Salir sin guardar y recuperar el contenido original](../scenarios/remitos/XG-REM-009.md) | remitos-correccion | P0 | Pendiente |
| [XG-REM-010 — Cancelar la salida y conservar los cambios para continuar](../scenarios/remitos/XG-REM-010.md) | remitos-correccion | P1 | Pendiente |
| [XG-REM-011 — Exigir fecha de recepción y detalle antes de confirmar](../scenarios/remitos/XG-REM-011.md) | remitos-carga | P1 | Pendiente |
| [XG-REM-012 — Advertir un comprobante repetido sin bloquear la carga](../scenarios/remitos/XG-REM-012.md) | remitos-carga | P1 | Pendiente |
| [XG-REM-013 — Consultar remitos cerrados o de otra PC sin modificarlos](../scenarios/remitos/XG-REM-013.md) | remitos-correccion | P0 | Pendiente |
| [XG-REM-014 — Separar recibido de sumar stock por renglón y selección masiva](../scenarios/remitos/XG-REM-014.md) | remitos-stock | P0 | Pendiente |
| [XG-REM-015 — Elegir si el costo se actualiza con o sin bonificación](../scenarios/remitos/XG-REM-015.md) | remitos-costos | P0 | Pendiente |
| [XG-REM-016 — Repetir una compra bonificada sin descontar dos veces el costo](../scenarios/remitos/XG-REM-016.md) | remitos-costos | P0 | Pendiente |
| [XG-REM-017 — Cambiar proveedor o lista de compra sin conservar precio obsoleto](../scenarios/remitos/XG-REM-017.md) | remitos-costos | P1 | Pendiente |
| [XG-REM-018 — Combinar bonificación de producto con descuento o recargo general](../scenarios/remitos/XG-REM-018.md) | remitos-costos | P1 | Pendiente |
| [XG-REM-019 — Revisar IVA por producto al desactivar y reactivar su inclusión](../scenarios/remitos/XG-REM-019.md) | remitos-costos | P0 | Pendiente |
| [XG-REM-020 — Distinguir IVA de otros impuestos en detalle y total](../scenarios/remitos/XG-REM-020.md) | remitos-costos | P0 | Pendiente |
| [XG-REM-021 — Recibir artículos ARS y USD según la conversión configurada](../scenarios/remitos/XG-REM-021.md) | remitos-costos | P0 | Pendiente |
| [XG-REM-022 — Conservar o actualizar cotización según estado del remito](../scenarios/remitos/XG-REM-022.md) | remitos-costos | P0 | Pendiente |
| [XG-REM-023 — Recibir en sucursal destino sin sumar también en origen](../scenarios/remitos/XG-REM-023.md) | remitos-stock | P0 | Pendiente |
| [XG-REM-024 — Anular una recepción y revertir stock y deuda sin restaurar precios](../scenarios/remitos/XG-REM-024.md) | remitos-correccion | P0 | Pendiente |

Cada ficha contiene perfil, datos, acciones/resultados, variantes, recuperación y trazabilidad. Las variantes son obligaciones de cobertura; no agregan casos aprobados por estar enumeradas.

## Orden de implementación dentro de la etapa 6

1. **Contrato de compras**: baseline descartable, proveedores, documentos abiertos/cerrados/anulados, inventario y costos iniciales; controles de propiedad/colisiones del runner. Lecturas de documento, detalle, stock, costos/listas, cuenta proveedor e historial por empresa/sucursal/puesto/versión.
2. **Recepción cotidiana**: REM-001/002/004/007/008/009/011. Aceptación: cargar/corregir, guardar borrador sin recibir, confirmar una vez y recuperar el original.
3. **Cantidad y detalle**: REM-003/005/006/010/014. Aceptación: fracciones, bultos, materia prima y flags independientes. Resolver accesibilidad del editor/encabezados.
4. **Condiciones de compra**: REM-012/015..022. Aceptación: origen correcto de precio, bonificación una vez, impuestos y moneda estables; separar cambios de costo de cambios de lista.
5. **Estados y reversión**: REM-013/023/024. Contextos múltiples permanecen bloqueados hasta tener el paquete específico. Anulación exige trazabilidad de la recepción y saldo del proveedor; no es limpieza genérica.

## Datos fijos pendientes

El seed actual de ventas/ofertas no incluye el contrato completo de estos remitos. Preparar una extensión versionada con upserts del runner y controles de colisión:

- Proveedores A/B, listas de compra propias, documentos por estado, números duplicados e historial preciso de bruto/bonificación.
- Artículos unidad/fracción/materia prima, factor de bulto cero/positivo, vencimientos, precio fijo/calculado, costo universal ON/OFF y productos control.
- IVA 0/10,5/21/27, exento/no gravado, otros impuestos fijos/porcentuales y adicionales separados.
- ARS/USD, cotización guardada/actual, conversión ON/OFF y cuenta del proveedor con importe original.
- Varios puestos/sucursales para REM-013/023. Ese paquete no existe aún; no usar sucursales reales ni relajar aislamiento.

Los códigos QA-REM e importes de las fichas son requisitos de fixtures futuros. Su documentación no afirma que `catalogo-comercial-v1` ya los cree.

## Reglas que cambian el resultado esperado

- **Guardar al salir guarda un borrador abierto.** Confirmar es lo que procesa recepción y consulta cuenta corriente. Rechazar confirmación mantiene la edición.
- **Recibido y Suma stock son diferentes.** Solo líneas activas recibidas integran el total y se procesan; Suma stock controla su efecto en existencias.
- **Actualizar precio con bonificación funciona aunque Actualiza precio esté desmarcado.** Desmarcar ambos evita cambiar costo normal en el perfil sin lista ni costo universal. La lista seleccionada y el costo universal tienen rutas independientes.
- **Número duplicado es un aviso, no un bloqueo.** Busca en la empresa, incluso otro proveedor, y permite continuar.
- **Cerrado/anulado o de otra PC se consulta sin modificar.** Se vuelve a comprobar estado antes de una mutación.
- **Anular revierte stock y cuenta del proveedor, pero no restaura costos/precios anteriores.** La interfaz lo advierte. Cambiar esa regla del producto requiere decisión aparte.
- **Bultos depende del factor positivo del artículo.** Conserva cantidad base y factor aplicado; anular usa cantidad recibida, no el factor actual.
- **Cotización pertenece al documento.** Solo USD sin conversión cierra en USD; mixtos cierran en ARS. Actualizar hoy se rechaza con conversión activa y líneas ya guardadas.

## Evidencia y límites

El contrato debe demostrar documento y movimientos por identidad, no solo un total visible. Un borrador persiste datos; es incorrecto exigir ausencia absoluta de cambios en la base después de Guardar. Una confirmación con error o evidencia incompleta no aprueba porque la ventana cierre: conservar diagnóstico y comprobar posibles efectos parciales antes de repetir. Faltan diseñar fallos controlados de persistencia/recuperación; no asumir atomicidad no demostrada.

La fuente abre el editor de detalle por doble clic y usa clicks de encabezado para selección masiva. No se encontró un binding alternativo para abrir ese editor en los atajos de FormCargaDeRemito inspeccionados; el editor ya abierto sí tiene acciones propias. Falta atajo/acción accesible y leyenda calibrada. Registrar la dependencia en el backlog de accesibilidad; no guardar coordenadas fijas ni confundir autorización de otra pantalla con calibración de Remitos.

Fuera de esta primera batería: remitos emitidos desde Venta; conversión integral remito→factura de proveedor; conciliación completa de órdenes de compra/entregas parciales; impresión física, sincronización/concurrencia y fiscal externo. Las variantes de precio calculado, costo universal y fallos controlados necesitan terminar sus datos/oráculos antes de habilitarse. No se presenta este mapa como todos los escenarios posibles del módulo.

## Anexo técnico

Fuente inspeccionada XGestion2: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`.

- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:1282-1524`: validaciones, confirmación, borrador y descarte.
- `src/ModuloProductos/Entidades/Compra.java:448-531`: cierre/cuenta proveedor; `:652-700`: anulación.
- `src/ModuloProductos/Entidades/CompraDetalle.java:100-195`: recepción, costos, listas y stock; `:214-269`: reversión sin restaurar precios.
- `src/ModuloStocks/Vistas/FormCargaDeRemito.java:270-328`: atajos actuales; `:2297-2315`: abrir editor; `:2461-2532`: encabezados masivos.
- `src/ModuloStocks/Vistas/CompraCantidadCargaPolicy.java:31-89` y `CompraCotizacionRemitoPolicy.java:18-39`: bultos/moneda.
- Tests fuente citados en cada ficha orientan las reglas; no acreditan ejecución E2E.

Aceptación real: SHA256 del JAR, versión de paquete/seed, perfiles/variantes, casos y reporte privado saneado. INFO resume, DEBUG muestra pasos y TRACE conserva diagnóstico sin secretos.

