# Automatización de atajos de listados

Los 13 casos `XG-KEY-001..013` tienen una prueba Robot por pantalla en
`suites/atajos_listados.robot`. **No hay PASS real con JAB**: todavía faltan la
VM exclusiva y el paquete privado. `implemented` en el catálogo significa que
el recorrido de prueba existe; `validation: pending` significa que el producto
no fue aprobado. El dry-run comprueba estructura, no el comportamiento Swing.

La biblioteca compartida `keyboard_lists.py` ejecuta búsqueda vacía/una/varias
filas, foco Ctrl+B, flechas desde buscador y tabla, paso circular, apertura por
Enter e identidad independiente en el editor, Enter del buscador, orden,
leyenda y restricciones. En Compras exige Remito, Factura, Transferencia y
Carnicería. En ocho pantallas recorre Ctrl+F, Tab/Shift+Tab, borrador A/B,
Cancelar/Escape/X, Aplicar, Enter, fechas o cascada y selección. En las otras
cinco vigila durante dos segundos que Ctrl+F no abra un diálogo. Cada
comprobación falla o bloquea si JAB no entrega evidencia completa; no fuerza
foco ni selección durante las aserciones.

## Preparar el paquete privado

1. En la PC/VM Windows QA exclusiva, construir/importar el FAT JAR **del commit
   que efectivamente se usará**, registrar ruta y SHA-256. El
   [JAR de `6085b7f3d`](evidencia-atajos-6085b7f3d.md) ya está construido;
   el artefacto anterior de [`3f8648035`](evidencia-atajos-3f8648035.md)
   no contiene los cambios posteriores de cabecera.
2. Preparar tres registros QA A/B/C por pantalla, búsquedas 0/1/3 y un registro
   protegido. Los esperados se anotan antes de ejecutar y no se copian de la
   pantalla observada. Para Compras preparar los cuatro tipos. El seed público
   sólo cubre parte de Productos; no crea usuarios, mesas ni movimientos.
3. Fusionar las secciones de
   [fixtures de ejemplo](../examples/keyboard-lists-fixtures.example.json) y
   [locators de ejemplo](../examples/keyboard-lists-locators.example.json) con
   `fixtures.json` y `locators.json` del **paquete privado**. Son plantillas:
   cada `CALIBRAR` bloquea la prueba. Los selectores requieren nombre, rol,
   ventana y estado JAB únicos; ninguna columna ID oculta es oráculo.
4. Calibrar cada `sort_control` con un mecanismo real de la pantalla. Si el
   listado no permite cambiar orden por UI, N09 queda BLOQUEADO (ACC-011);
   no alterar datos/RowSorter desde la prueba. Las ocho X nativas requieren
   acción accesible propia (ACC-013). `reload_revision` tiene que contar **una
   recarga lógica completa por Aplicar**, no celdas ni eventos de árbol JAB
   (ACC-012). Sin esas señales el test no aprueba.
5. Guardar una captura revisada de la leyenda gris junto al buscador dentro de
   `.local/xgestion/` y registrar su ruta y SHA-256 del mismo JAR en
   `legend_evidence`. JAB comprueba texto y visibilidad; no acredita color ni
   distancia al buscador. Preparar rol restringido con credenciales locales
   `QA_KEYBOARD_RESTRICTED_USER` y `QA_KEYBOARD_RESTRICTED_PASSWORD` en
   `.env.local`, nunca en Git ni en logs. Declarar un aviso de rechazo o un
   editor de sólo lectura, según el permiso real; no inventar un bloqueo de
   apertura si el permiso sólo afecta Guardar. En movimientos de clientes usar
   una deuda asociada a venta; en proveedores, un registro de remito/factura;
   abrirlos no autoriza editar su origen.
6. Agregar `atajos-listados-v1` a `calibration.verified_features` sólo después
   de verificar aliases y valores contra ese JAR. Conservar el hash en
   `calibration.app_sha256`; `load_assets` rechaza un JAR diferente. Reconstruir
   el ZIP privado con su manifest; los ejemplos públicos no son el paquete.

```powershell
.\qa.cmd doctor --product xgestion
.\qa.cmd list --product xgestion --group atajos-listados
.\qa.cmd run --product xgestion --group atajos-listados --dry-run
.\qa.cmd run --product xgestion --scenario XG-KEY-005 --log-level DEBUG
.\qa.cmd run --product xgestion --group atajos-listados --log-level INFO
```

Para cada corrida real guardar reporte, caso/variante, SHA-256, perfil, rol,
identidad esperada y observada, foco/selección y defecto reproducible. Un
bloqueo de perfil/observabilidad no es un defecto confirmado del ERP. La
[matriz de variantes](atajos-listados.md) detalla N01–N12, F01–F09 y S01.

**Estado actual:** 13 pruebas codificadas y validadas en seco; cero ejecutadas
con JAB, cero PASS reales. La aceptación sigue detenida por falta de VM/paquete
y por ACC-011/012/013 hasta que el JAR muestre mecanismos verificables.
