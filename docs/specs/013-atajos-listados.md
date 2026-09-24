# Atajos de los 13 listados CRUD

## Pedido y criterio de aceptación

Fuente solicitada: XGestion2 `3f8648035380535f639da140d208fd299a096593`,
`release/189-lts`. El pedido del usuario define el alcance: 13 listados,
navegación, identidad, búsqueda, orden, ocho modales de filtros y cinco
ausencias de modal. No se modifica el ERP para hacer pasar la prueba.

Cada pantalla tendrá una ficha XG-KEY independiente, variantes obligatorias,
datos de preparación y registro de evidencia. Una ficha sólo se implementa
cuando su recorrido completo puede automatizarse; escribirla, inspeccionar
Java o compilar no acredita ejecución. No se agregan Robot vacíos ni PASS
por ausencia de controles. Un impedimento de laboratorio es BLOQUEADO,
distinto de un defecto reproducido del producto.

## Hechos verificados y dependencias

- Checkout ERP limpio y HEAD exacto al comenzar. El JAR existente de `dist`
  era anterior; se construye desde `git archive` del commit, en `.local`,
  con salidas propias. No se crea un worktree ni se reutilizan clases.
- `ListadoCrudTeclado` instala foco, flechas circulares y Enter. Los trece
  callbacks comparten la apertura del doble clic. Eso es trazabilidad estática.
- Compras conserva búsqueda + apertura automática si queda una sola fila.
- Cliente: no editar movimiento asociado a venta. Proveedor: no editar
  movimiento asociado a remito/factura. Abrir no debe persistir cambios.
- `qa.cmd doctor --product xgestion` bloquea por falta de paquete QA privado.
  Faltan baseline, licencia/configuración, VM/PC exclusiva y calibración JAB.
- No está demostrada una señal JAB de una recarga lógica completa, ni una
  acción accesible de X para el JDialog nativo. Tampoco se presume que las
  trece tablas permitan ordenar por encabezado. Se registran como pendientes
  de observabilidad, sin inventar selectores ni contadores.

## Incrementos

1. Construir artefacto exacto, verificar contenido FAT, registrar ruta y SHA256.
2. Fichas y matriz: datos inequívocos, acciones visibles, filtros por pantalla,
   restricciones, checklist y evidencia esperada; actualizar grupos y Excel.
3. Con paquete/laboratorio: inspeccionar JAB del artefacto, calibrar nombres,
   roles y estados. No extraer identidad de una columna oculta.
4. Automatizar primero foco/selección/apertura, luego filtros y sus cierres.
   Red/green sintético para selección incorrecta, lectura incompleta, foco
   forzado, ID oculto, doble recarga y evidencia faltante antes del recorrido.
5. Ejecutar los trece recorridos reales, conservar reporte por pantalla y
   defectos reproducibles. No cerrar KEY ni ACC-010 con dry-run.

## Archivos y verificaciones

- Fichas: `products/xgestion/scenarios/atajos-listados/`.
- Matriz y procedimiento: `products/xgestion/docs/atajos-listados.md`.
- Evidencia pública sin secretos: `products/xgestion/docs/evidencia-atajos-3f8648035.md`.
- Registro común: `products/xgestion/groups.json`; Excel generado por `qa.cmd coverage`.
- Ejecutar Ruff, Robocop, pytest, `qa.cmd check`, `qa.cmd coverage --check`
  y dry-run de regresión. Son verificaciones del repositorio, no del ERP.
- Sin `package.json` en la raíz; no hay npm lint/stylelint aplicables.

## Límites

Estado de entrega: incrementos 1 y 2 completados. Incrementos 3 a 5 pendientes:
el usuario confirmó que todavía no hay VM ni paquete. Ningún caso nuevo está
automatizado o ejecutado; ver evidencia por pantalla y controles del repositorio.

No emitir comprobantes, imprimir, exportar datos privados, modificar permisos
ni guardar editores durante estos recorridos. Las restricciones se prueban
con usuarios preparados en el paquete y movimientos de origen conocido.
No conectar el JAR a la instalación cotidiana para resolver el bloqueo.
Sin calibración y datos no se inventa una suite ejecutable: las fichas quedan
`planned`, seleccionables en el catálogo, sin archivo Robot.

## Actualización posterior

La continuación incorporó `suites/atajos_listados.robot` y su biblioteca JAB
para los trece casos; las fichas pasaron a `implemented`. La restricción de
este documento correspondía a la entrega anterior sin código de prueba.
`implemented` no acredita ejecución ni resultado del ERP: el perfil privado,
la VM, la calibración y las señales ACC-011/012/013 siguen pendientes. Ver
`products/xgestion/docs/atajos-automatizacion.md` para el estado actual.
