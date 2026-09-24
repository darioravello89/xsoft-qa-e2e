# Atajos y filtros de los 13 listados

Fuente: XGestion2 `3f8648035380535f639da140d208fd299a096593`, `release/189-lts`.
**13 escenarios documentados, 0 automatizados, 0 ejecutados con JAB.**
El [registro de evidencia](evidencia-atajos-3f8648035.md) identifica el FAT JAR
construido y los bloqueos. No hay defectos confirmados por ejecución real.

El grupo `atajos-listados` aparece en catálogo/Excel como pendiente. No se
ofrece como suite ejecutable hasta implementar y calibrar sus recorridos.
Cada ficha requiere todas las variantes comunes y las específicas de su
pantalla; una apertura correcta no aprueba el resto del caso.

```powershell
.\qa.cmd list --product xgestion --group atajos-listados
.\qa.cmd list --product xgestion --group filtros-listados
.\qa.cmd doctor --product xgestion
```

## Pantallas e identidad visible

| Caso | Listado | Identidad a contrastar en la pantalla abierta | Filtros |
| --- | --- | --- | --- |
| [KEY-001](../scenarios/atajos-listados/XG-KEY-001.md) | Cuentas corrientes de clientes | Nombre/apellido únicos y documento del cliente en su cuenta | Comercial; fechas del informe |
| [KEY-002](../scenarios/atajos-listados/XG-KEY-002.md) | Cuenta corriente de cliente | Cliente, nota única, importe, moneda y fecha del movimiento | Desde / Hasta |
| [KEY-003](../scenarios/atajos-listados/XG-KEY-003.md) | Cuentas corrientes de proveedores | Razón social única y CUIT del proveedor en su cuenta | Desde / Hasta |
| [KEY-004](../scenarios/atajos-listados/XG-KEY-004.md) | Cuenta corriente de proveedor | Proveedor, nota única, importe, moneda y fecha del movimiento | Desde / Hasta / Tipo de movimiento |
| [KEY-005](../scenarios/atajos-listados/XG-KEY-005.md) | Clientes | Nombre/apellido únicos y documento | Sin modal |
| [KEY-006](../scenarios/atajos-listados/XG-KEY-006.md) | Productos | Código visible y nombre único | Estado / Proveedor / Categoría / Subcategoría / Ordenar por / Dirección |
| [KEY-007](../scenarios/atajos-listados/XG-KEY-007.md) | Mesas | Nombre/número único, zona y sucursal | Zona |
| [KEY-008](../scenarios/atajos-listados/XG-KEY-008.md) | Usuarios | Usuario de acceso y nombre visible únicos, sin leer contraseña | Sin modal |
| [KEY-009](../scenarios/atajos-listados/XG-KEY-009.md) | Turnos | Nombre único y horarios; mantenimiento, no apertura/cierre de caja | Sin modal |
| [KEY-010](../scenarios/atajos-listados/XG-KEY-010.md) | Compras | Tipo, número, proveedor, fecha y sucursal del comprobante | Sucursal / Proveedor / Estado / Desde / Hasta / Tipo de compra |
| [KEY-011](../scenarios/atajos-listados/XG-KEY-011.md) | Proveedores | Razón social única y CUIT | Sin modal |
| [KEY-012](../scenarios/atajos-listados/XG-KEY-012.md) | Categorías | Nombre único y orden configurado | Sin modal |
| [KEY-013](../scenarios/atajos-listados/XG-KEY-013.md) | Subcategorías | Nombre único y categoría padre | Categoría |

## Preparación de datos

El paquete privado debe declarar un conjunto pequeño por listado: tres registros
inequívocos A/B/C, sus valores esperados en la ficha, una búsqueda sin resultados,
una que deje sólo B y otra que deje A/B/C. Usar nombres QA dedicados. El orden
alfabético debe diferir del de creación para detectar confusión entre fila e ID.
No se aceptan homónimos indistinguibles ni seleccionar `fila 0` como identidad.
Las búsquedas son valores del paquete, no supuestos deducidos del observado.

| Datos adicionales | Preparación pendiente del paquete |
| --- | --- |
| Clientes y proveedores | Dos roles: autorizado y restringido; registros de prueba con documento/CUIT inequívoco, sin usar personas reales. El general de clientes debe incluir al menos un cliente con ID > 1 y cuenta activa. |
| Movimientos | Pago y deuda manuales; movimiento de venta del cliente; movimientos de remito/factura del proveedor. Notas, moneda e importes distintos y fecha anterior/dentro/posterior al rango. Preparar por circuito autorizado, sin inventar deuda por SQL. |
| Productos | Tres artículos del seed con códigos visibles únicos, proveedor/categoría/subcategoría conocidos y orden por código distinto del orden por nombre. Tres resultados en una misma página; contemplar paginación como variante adicional. |
| Mesas | Mesas inequívocas en dos zonas; sólo abrir mantenimiento, no tomar ni cerrar cuentas. |
| Usuarios y turnos | Cuentas QA dedicadas sin contraseñas en fixtures; turnos con nombres/horarios diferentes. No editar el operador autenticado. |
| Compras | Remito, Factura, Transferencia y Carnicería; número/proveedor/fecha/sucursal inequívocos; borrador y recibido cuando corresponda. Sólo abrir/cancelar, no recibir ni emitir. |
| Categorías/subcategorías | Dos padres, subcategorías diferentes por padre y registros de control fuera del filtro. |

El seed comercial actual ayuda con productos y clasificaciones, pero **no
prepara las trece pantallas**. Licencia, usuarios, movimientos, documentos,
mesas y turnos siguen dependiendo del baseline privado verificado.

## Variantes comunes obligatorias N01–N12

| Variante | Acciones | Resultado y evidencia |
| --- | --- | --- |
| N01 — Buscar | Desde otro control y desde la tabla, Ctrl+B. | JAB informa `focused` en el buscador correcto. No se solicita foco desde el driver después del atajo: eso ocultaría el defecto. |
| N02 — Vacía | Buscar el valor inexistente; verificar cero filas. Pulsar ↓ y ↑ desde el buscador. Si la tabla admite foco por Tab, Enter sin fila seleccionada. | Buscador conserva foco al usar flechas; ninguna selección ni apertura/error. No inventar foco para una tabla que no lo admite. |
| N03 — Una fila | Buscar B. Desde el buscador probar ↓ y, en una repetición independiente, ↑. En tabla, ↓ y ↑ repetidos; Enter. | Foco en tabla, B seleccionada siempre; una sola apertura de B. Cerrar sin guardar y verificar retorno al listado. |
| N04 — Varias sin selección | Buscar A/B/C y comprobar que no hay fila seleccionada. ↓ desde buscador; repetir desde estado inicial con ↑. | ↓ selecciona primera fila visible; ↑ la última. Foco cambia a tabla. Si el baseline conserva selección, registrar ese estado y usar N05; no simular que no había selección. |
| N05 — Varias con selección | Seleccionar B por teclado. Ctrl+B; ↓ y, desde B nuevamente, ↑. | Selección avanza a la siguiente/anterior respecto de B y devuelve foco a tabla. No reinicia siempre en la primera. |
| N06 — Circular | Recorrer A/B/C en tabla en ambos sentidos; ↓ desde última y ↑ desde primera. | Una selección única, sin salir de tabla: última → primera y primera → última; registro seleccionado visible. |
| N07 — Abrir identidad | Enter en primera, intermedia y última, cerrando sin guardar entre aperturas. | Tipo de pantalla y campos identificadores coinciden con la fila visible seleccionada. No basta verificar título ni que apareció una ventana. |
| N08 — Búsqueda/recarga | Seleccionar B, buscar conservándolo; luego buscar excluyéndolo; volver a A/B/C. | Si B sigue, se conserva su identidad; si desaparece, se limpia selección, Enter no abre otro registro. Flechas siguen funcionando en la tabla recargada. |
| N09 — Cambio de orden | Seleccionar B; invertir orden con el mecanismo de UI disponible; volver a recorrer y abrir. | Verificar secuencia visible realmente diferente y apertura de B, nunca el viejo índice. Si no existe mecanismo accesible de orden, BLOQUEADO y evidencia; no instalar un RowSorter desde el test ni cambiar DB para fingir esta variante. |
| N10 — Enter en buscador | Con 0, 1 y varias filas, Enter en buscador. | Busca sin abrir en 12 pantallas. En Compras abre automáticamente si queda exactamente una; validar tipo e identidad. Con 0 o varias no abre. |
| N11 — Ayuda visible | Leer ayuda de teclado junto al buscador con el listado activo, antes y después de recargar. | Texto de Ctrl+B, ↑/↓ y Enter; Ctrl+F sólo en las ocho pantallas con filtros. Visible, gris y próximo al buscador, sin recortes. JAB prueba texto/estado; color/ubicación requieren atributos legibles y/o evidencia visual del mismo JAR. No inferir color desde el nombre accesible. |
| N12 — Restricciones y recuperación | Repetir apertura con rol restringido según baseline y con registros protegidos; cancelar editor autorizado. | Mismas restricciones que la acción existente; no guardar ni alterar datos. Tras aviso/cancelación, Ctrl+B y navegación siguen funcionando. Registrar permisos concretos, no presumir que todo editor deniega apertura. |

En Productos probar también escribir una búsqueda y pulsar flecha mientras
la búsqueda diferida está pendiente: se usa la tabla del texto actual, no la
anterior. No usar esperas fijas para ocultar la carrera.

## Ocho modales: variantes F01–F09

Antes de cada variante registrar filtros aplicados A y las identidades/orden
de la tabla. El borrador B debe cambiar **todos los controles**, no sólo uno.
Repetir desde A para Cancelar, Escape y X por separado.

| Variante | Acciones | Resultado y evidencia |
| --- | --- | --- |
| F01 — Abrir | Ctrl+F desde buscador y tabla. | Un único modal con título y campos de la pantalla; la tabla queda inaccesible a navegación mientras está abierto. Ningún modal vacío. |
| F02 — Recorrido de foco | Tab por todos los campos, partes de fecha/calendario y botones; Shift+Tab en sentido inverso y en extremos. | Foco visible y JAB `focused`; no salta controles habilitados ni escapa al listado. Registrar orden real y valores antes/después; no forzar foco en cada paso. |
| F03 — Cancelar | Modificar borrador a B con teclado; enfocar Cancelar con Tab y activar con teclado; reabrir Ctrl+F. | Tabla y filtros aplicados siguen A; reapertura muestra A, no B. |
| F04 — Escape | Repetir edición B, cerrar con Escape y reabrir. | Descarta todos los cambios. Si estaba desplegado un combo/calendario, cerrar primero ese desplegable y comprobar el Escape del modal aparte. |
| F05 — X | Repetir B, activar X de cierre y reabrir. | Descarta B y conserva A. La X requiere acción accesible demostrada: Alt+F4 por sí solo no acredita haber activado X. No usar coordenadas fijas ni sustituir por Escape. |
| F06 — Aplicar | Editar B por teclado, llegar a Aplicar con Tab y activarlo una vez; esperar tabla final. | Modal cerrado, filtros B efectivos, filas y orden esperados; exactamente **una recarga lógica**, no una por control. Reabrir y verificar todos los valores B. |
| F07 — Enter predeterminado | Desde un campo de texto/fecha con desplegables cerrados, Enter. | Aplica una vez. En combo abierto, Enter confirma opción según comportamiento Swing; no confundir con Aplicar. |
| F08 — Fechas/cascada | Desde > Hasta y fecha vacía; corregir y aplicar. En Productos cambiar categoría y revisar subcategorías antes de aplicar/cancelar. | Fecha inválida advierte y no aplica; corrección permite continuar. La subcategoría pertenece al padre elegido; cancelar recupera también la subcategoría anterior. |
| F09 — Repetición y selección | Aplicar A → B → A, conservar/excluir seleccionado y recorrer tabla otra vez. | No acumula listeners/recargas; selección por identidad o limpia si el registro desaparece. No quedan controles de filtros ocultos dentro del recorrido Tab del listado. |

F08 aplica fechas en las cuatro cuentas y Compras; cascada en Productos.
Mesas/Subcategorías no tienen esos campos: F08 se registra `no_aplica` con
esa razón, nunca como PASS de validación de fechas.

**Recarga única:** una tabla final correcta no demuestra una sola consulta o
recarga. Antes de automatizar F06/F07/F09 hay que identificar una señal de
inicio/fin/contador de recarga lógica correlacionada con la acción en el JAR.
No contar cada celda ni cada evento JAB como una recarga; la reconstrucción
del árbol del driver tampoco mide las recargas del ERP. Sin señal verificable,
esta comprobación queda BLOQUEADA y el caso completo no aprueba.

## Cinco listados sin filtros: variante S01

Clientes, Usuarios, Turnos, Proveedores y Categorías: desde buscador y tabla,
Ctrl+F no abre ni roba foco hacia un modal vacío. Comprobar foco y ausencia de
un nuevo diálogo del mismo PID durante una ventana de observación continua;
volver a usar Ctrl+B/flechas/Enter. Una consulta instantánea sin diálogo no
prueba que no haya aparecido transitoriamente.

## Observación JAB y oráculos

- Abrir sólo el JAR administrado y verificar PID/ventana antes de cada acción.
- Selectores por nombre, rol, contexto de ventana y estados. Si faltan nombres
  únicos, registrar impedimento; no resolver con índices arbitrarios.
- Leer columna visible calibrada por encabezado/nombre y estado de selección.
  No asumir ID oculto ni conservar índices luego de filtrar/ordenar.
- JAB debe demostrar foco y selección **después** de la tecla sin pedir foco
  ni seleccionar la fila esperada durante la aserción.
- El código muestra callbacks compartidos con doble clic; la validación real
  usa Enter y comprueba apertura/restricciones. No se ejecuta doble clic en
  cuentas de clientes: la negativa anterior del usuario sigue vigente.
- Esperados del paquete: identidad y datos de destino preparados antes del
  test. No fabricar el esperado a partir de la misma pantalla que se valida.
- Confirmar ausencia de modificaciones al cerrar/cancelar mediante lecturas
  acotadas por identidad y contexto, sin filas completas en logs ni escrituras
  SQL. No leer contraseñas de usuarios.

## Ejecución y evidencia por pantalla

1. Preparar PC/VM exclusiva Windows, offline, escritorio visible; importar
   paquete con este JAR y hash, sin usar la instalación cotidiana.
2. Calibrar el árbol JAB de cada pantalla y editor, datos y controles de filtros.
   Guardar localmente paquete/perfil/calibración; no publicar árboles privados.
3. Implementar recorrido Robot sólo cuando las variantes tengan acciones y
   oráculos verificables. Habilitar `atajos-listados` tras pasar controles del
   framework; conservar `planned` mientras no exista automatización completa.
4. Ejecutar por pantalla con DEBUG para pasos; INFO resumido; TRACE saneado.
   Antes de estar implementado, `run --group atajos-listados` debe rechazar la
   selección. No ejecutar Robot por fuera de `qa.cmd` para saltar preflight.
5. Guardar por N/F/S: fecha, caso/variante, JAR SHA256, paquete/perfil, versión
   JAB, resolución/DPI, rol, datos QA, paso, esperado/observado, foco/selección,
   capturas sin autenticación y reporte local. Estado: no ejecutado, bloqueado,
   falló u OK. Una evidencia incompleta nunca se convierte en OK.
6. Para un defecto: repetir desde baseline, anotar pasos mínimos, frecuencia,
   pantalla, identidad esperada/abierta y adjuntar evidencia privada saneada.
   Separar hipótesis del análisis estático de reproducción real.

La [evidencia inicial](evidencia-atajos-3f8648035.md) no contiene PASS E2E.
El [backlog de accesibilidad](backlog-accesibilidad.csv) conserva ACC-010 y
los impedimentos de esta ampliación hasta comprobarlos en el FAT JAR.
