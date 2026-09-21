# Datos fijos para practicar ventas y ampliar pruebas

`catalogo-comercial-v1` prepara una batería pública de datos sintéticos: **48 artículos, 19 ofertas, 5 listas y 6 precios de lista**, con catálogos auxiliares y 43 movimientos iniciales de stock. Permite volver a los mismos productos y condiciones sin inventar datos para cada caso.

El seed es opcional. Los siete casos automatizados actuales siguen usando el producto del paquete privado —90001 en el ejemplo— y no cambian al incorporar esta batería. Los artículos nuevos tienen códigos `QA-SEED-*` e IDs reservados `980xxx`. Crear los datos no agrega casos Robot ni acredita ventas, ofertas, impuestos o stock del JAR.

## Revisar sin instalar el producto

Con las dependencias Python del repositorio instaladas:

```powershell
.\qa.cmd seed --dry-run
.\qa.cmd seed --dry-run --export
.\qa.cmd seed --dry-run --export --reference-date 2026-09-21
```

La vista previa no necesita paquete privado, credenciales ni MySQL; no abre una conexión. `qa.cmd` usa el entorno preparado por `setup`, que también comprueba Java. Para revisar con solo las dependencias Python, ejecutar `python -m framework.cli seed --dry-run --export`; esta vía no requiere Java. Muestra conteos y puede guardar `work/seed-preview.sql`. La fecha explícita hace reproducible la revisión; omitirla usa el día local. El archivo exportado contiene sentencias con marcadores `%s` y comentarios con datos públicos de ejemplo. Es material de revisión, no un script para pegar en phpMyAdmin: omitiría los controles de identidad, esquema, transacción y aislamiento del runner. El contexto de la vista previa es ilustrativo; aplicar usa el contexto de `fixtures.json`.

## Preparar el laboratorio o ejecutar con la batería

Después de importar un paquete autorizado, en Windows QA aislado y offline:

```powershell
.\qa.cmd seed --apply
.\qa.cmd run --product xgestion --group regression --seed catalogo-comercial-v1
```

**`seed --apply` restaura el baseline y reemplaza los datos actuales de la base privada `127.0.0.1:13317/xsoft_qa`.** Después verifica el esquema, las dependencias y las colisiones, aplica los datos y comprueba las filas; al terminar cierra su MySQL. No abre XGestion y no ejecuta E2E. Conserva un `seed-summary.json` privado con el resultado. No usar esta operación para conservar ventas de una ejecución anterior.

`run --seed catalogo-comercial-v1` restaura y aplica la batería dentro de la misma preparación que precede a Robot. Conserva los controles normales de paquete, JAR, escritorio, aislamiento, selectores y exclusión de ejecuciones simultáneas. Un `run` sin `--seed` restaura solamente el baseline. `inspect` también restaura: ejecutarlo después de `seed --apply` no conserva el catálogo preparado. Una futura validación GUI de estos nuevos datos debe sembrar dentro del ciclo de su recorrido; no iniciar por fuera una instalación cotidiana del ERP.

La fecha de aplicación debe coincidir con `CURDATE()` de la instancia QA. Una fecha histórica puede usarse en la vista previa, pero se bloquea al aplicar. El ERP suma stock del año corriente y decide vigencia de ofertas con su reloj: no alterar silenciosamente esas fechas para obtener un resultado esperado.

## Productos para venta cotidiana

Los precios son finales por unidad base. Salvo indicación, moneda ARS, IVA 0%, unidad entera, activo, precio 1000 y stock inicial 100. Las existencias son entradas iniciales del catálogo, no promesas de saldo después de vender.

| ID | Código completo | Datos preparados / uso |
| --- | --- | --- |
| 980001 | `QA-SEED-NORMAL` | Producto simple: 1000; dos unidades suman 2000 sin condiciones comerciales adicionales. |
| 980002 | `QA-SEED-KG` | KG, precio 2000, stock 10,500; carga manual fraccionada. |
| 980003 | `QA-SEED-BULTO` | 12 unidades por bulto; precio por bulto 10800; stock 120 unidades. |
| 980004 | `QA-SEED-STOCK-CERO` | Stock inicial 0. |
| 980005 | `QA-SEED-STOCK-UNO` | Stock inicial 1. |
| 980006 | `QA-SEED-STOCK-NEGATIVO` | Stock inicial −3. |
| 980007 | `QA-SEED-INACTIVO` | Desactivado; conserva movimiento inicial 10. |
| 980008 | `QA-SEED-USD` | Precio USD 10, stock 20; la cotización la aporta el perfil. |
| 980009 | `QA-SEED-REDONDEO` | KG, precio 10,01, stock 10; permite explorar importes fraccionarios. |
| 980010 | `QA-SEED-IVA105` | Neto 100 + IVA 10,50 = final 110,50. |
| 980011 | `QA-SEED-IVA21` | Neto 100 + IVA 21 = final 121. |
| 980012 | `QA-SEED-IVA27` | Neto 100 + IVA 27 = final 127. |
| 980013 | `QA-SEED-NO-GRAVADO` | Precio 100; categoría No gravado. |
| 980014 | `QA-SEED-EXENTO` | Precio 100; categoría Exento. |
| 980015 | `QA-SEED-PADRE` | Padre de variantes; no agrega stock propio. |
| 980016 | `QA-SEED-VAR-ROJO-S` | Hijo Rojo/S, stock 10. |
| 980017 | `QA-SEED-VAR-AZUL-M` | Hijo Azul/M, stock 20. |
| 980018 | `QA-SEED-COMPUESTO` | Precio 1500; consume 2 componentes A + 2 B, sin stock propio. |
| 980019 | `QA-SEED-COMPONENTE-A` | Precio 500, stock 100. |
| 980020 | `QA-SEED-COMPONENTE-B` | Precio 250, stock 100. |
| 980021 | `QA-SEED-MATERIA-PRIMA` | KG, precio 1000, stock 30; no se trata como búsqueda de producto común. |
| 980022 | `QA-SEED-RECETA` | Precio 2500; composición con 0,250 KG de materia prima, sin stock propio. |
| 980023 | `QA-SEED-CARNICERIA` | Tipo Carnicería del ERP, KG, precio 8000, stock 15. |
| 980024 | `QA-SEED-SERVICIO` | Precio 500, sin control de stock. |
| 980025 | `QA-SEED-OPCIONES` | Precio 2500; opciones porción normal/doble de 0,100/0,200 KG de materia prima. |

Stock cero/negativo no implica que la venta deba rechazarse siempre. La regla depende de la configuración del perfil, permisos y recorrido. El bulto expresa unidades base; no crea un segundo inventario. `RECETA` usa composición de productos y no prepara por sí misma todas las reglas de platos/comandas de Restobar. KG y Carnicería usan `balanza` vacía: no configuran etiquetas, lector ni hardware.

## Productos, ofertas y listas comerciales

Los siguientes 23 artículos parten de precio ARS 1000, IVA 0% y stock 100. Los KG permiten decimales. Sus ofertas se acotan al artículo o a una familia, subfamilia, marca o sector propios; ninguna oferta se define como universal ni se aplica al fixture 90001.

| ID(s) de artículo | Código(s), todos con prefijo `QA-SEED-` | Condición preparada |
| --- | --- | --- |
| 980101 | `PCT` | 10% de descuento. |
| 980102 | `IMP` | Descuento de importe 150. |
| 980103 | `2X1` | Lleva 2, paga 1. |
| 980104 | `2DA50` | Segunda unidad al 50%. |
| 980105 | `MIN-PCT` | Desde 2 unidades, 10%. |
| 980106 | `MIN-IMP` | Desde 2 unidades, descuento 150 por unidad. |
| 980107 | `MIN-PRECIO` | Desde 2 unidades, precio unitario 800. |
| 980108 / 980109 | `COMBO-A` / `COMBO-B` | Un A + un B por 1500; oferta adicional de 10% para A sobrante. |
| 980110 / 980111 / 980112 | `EXPIRADA` / `FUTURA` / `INACTIVA` | Ofertas que no corresponden por vigencia o estado. |
| 980113 / 980114 / 980115 / 980116 | `FAMILIA` / `SUBFAMILIA` / `MARCA` / `SECTOR` | 10% por cada alcance exclusivo. |
| 980117 / 980118 | `KG-MIN0` / `KG-MIN1` | Precio 800 con mínimo 0 o 1 KG. |
| 980119 / 980120 / 980121 | `GRUPO-A` / `GRUPO-B` / `GRUPO-C` | Oferta agrupada 3×2 sobre su familia exclusiva. |
| 980122 | `LISTAS` | Precio base y listas explícitas ARS/USD; detalle de lista inactiva. |
| 980123 | `CANTIDAD` | Precios por umbral 2/5 y prioridad de lista elegida. |

Las ofertas usan IDs 980101–980119 en su propia tabla. La vigencia activa es relativa a la fecha de referencia (365 días antes/después); la expirada termina el día anterior y la futura comienza al día siguiente. No se asignan medios de pago específicos ni ofertas globales de terceros.

| ID de lista | Nombre | Detalles preparados |
| --- | --- | --- |
| 980101 | `QA-SEED-LISTA-ARS` | LISTAS a 750 ARS; CANTIDAD a 950 ARS. |
| 980102 | `QA-SEED-LISTA-USD` | LISTAS a 2,50 USD. |
| 980103 | `QA-SEED-LISTA-CANTIDAD-2` | CANTIDAD a 900 desde 2 unidades. |
| 980104 | `QA-SEED-LISTA-CANTIDAD-5` | CANTIDAD a 800 desde 5 unidades. |
| 980105 | `QA-SEED-LISTA-INACTIVA` | Lista y detalle desactivados, precio 500 para LISTAS. |

El seed no asigna listas a clientes, turnos, usuarios ni sucursales por defecto. Los escenarios deben declarar la lista seleccionada, moneda, cotización, configuración de precios por cantidad y reglas de combinación antes de comparar montos. Tampoco desactiva ofertas ajenas que ya contenga el baseline: el responsable debe preparar el perfil sin condiciones generales que contaminen los ejemplos.

`PRICING_CASES` en [pricing.py](../seeds/pricing.py) conserva 26 ejemplos con resultado calculado desde reglas de fuente, todos `manual_pending`. Ejemplos: PCT×3 → 2700; IMP×3 → 2550; 2X1×3 → 2000; segunda al 50%×3 → 2500; combo A+B → 1500; combo 2A+B con descuento al sobrante → 2400. Son candidatos de aceptación con perfil explícito, no resultados obtenidos del JAR ni nuevas fichas ejecutables.

Para fraccionados: 0,500 KG con mínimo 0 → 400; con mínimo 1 → 500; 1 KG con mínimo 1 → 800. Hay diferencias entre el cálculo aislado y el filtro de aplicabilidad cuando mínimo 0 se combina con cantidades mayores: no extrapolar estas tres muestras a toda cantidad sin comprobar el recorrido real.

## Requisitos y comportamiento al repetir

Se reutilizan empresa, sucursal, computadora y usuario existentes del fixture; no se crean usuarios, cajas, licencias ni credenciales. El preflight exige el esquema compatible, claves y columnas necesarias y catálogos globales coherentes:

- Unidad 1 `UN` entera y unidad 2 `KG` decimal.
- Moneda 1 con código AFIP `PES`; moneda 2 con código `DOL`.
- IVA 1/2/3 al 0%, IVA 4 al 10,50%, IVA 5 al 21% e IVA 6 al 27%.

Los globales se validan y no se sobrescriben. Los catálogos propios incluyen familia/subfamilia/ubicación/proveedor base 980001; colores 980001/980002, talles 980003/980004; categorías comerciales 980113/980114/980119 y ubicación 980116. Los IDs se interpretan dentro de cada tabla y empresa, no como una secuencia global única.

Las composiciones necesitan además que sus IDs de componentes no existan en otra empresa del baseline: algunas consultas heredadas del ERP omiten ese filtro. El seed detecta esa ambigüedad y bloquea; no corrige el ERP ni renumera artículos de terceros.

Cada fila declara clave primaria e identidad estable. Si una PK reservada o un código/nombre reservado corresponde a otra identidad, el seed bloquea antes de aplicar: no toma posesión de la fila por coincidir un número. No modifica el esquema para adaptarlo, ni renumera datos ajenos. Con las mismas entradas, el upsert inserta lo faltante, actualiza diferencias propias y deja sin cambios lo idéntico. Los resúmenes distinguen esas tres situaciones.

El preflight también protege los recorridos frente a referencias que no coinciden con la PK de una fila del seed:

- Rechaza IDs reservados y códigos que coincidan con el producto o el código inexistente del fixture, incluyendo cambios de mayúsculas y espacios finales, antes de abrir la conexión del seed.
- Busca códigos alternativos en `producto_codigo` sin ignorar filas inactivas, porque algunos caminos del ERP todavía pueden resolverlas.
- Rechaza composiciones, opciones y detalles de listas adicionales que referencien productos o listas del catálogo. Para composiciones comprueba también otras empresas y relaciones inactivas: existen consultas del ERP que omiten esos filtros.
- Exige identidad funcional de listas por empresa e ID, además de su PK con sucursal; una cabecera de otra sucursal con el mismo ID puede alterar los joins del ERP.
- Rechaza ofertas ajenas vigentes que alcancen los productos seed, incluidos combos; también artículos ajenos que ya usen sus familias, subfamilias, sectores, marcas o padres. Esta última comprobación evita que una oferta nueva del seed cambie el precio de un producto ajeno.

Estas verificaciones bloquean el lote; no desactivan ofertas, eliminan aliases ni corrigen relaciones ajenas para hacerlo pasar. Un bloqueo aporta información para preparar de nuevo el baseline aislado.

El stock inicial es **un movimiento fijo reservado por producto**; no se agrega nuevamente cada vez ni se calcula «stock deseado menos stock actual». No se sobrescribe `artStock` ni `productos_stock`, ni se borran movimientos de ventas para recuperar existencias. Los saldos pueden cambiar al vender. La repetición de la API de seed mantiene su movimiento; el comando público `--apply`, además, restaura primero el baseline y por eso descarta la operación anterior de esa base QA.

La recuperación es volver a una restauración controlada. Un fallo de preflight deja la preparación rechazada; no continuar a Robot ni editar manualmente el marcador de propiedad. Guardar el resumen local y corregir paquete, contexto, catálogo o esquema en su origen. Cambiar nombres/IDs directamente en la DB para eludir una colisión rompe el contrato.

## Evidencia y límites

La referencia inspeccionada es XGestion2 `release/189-lts`, commit `f34238183d494259bed1279dd7d9aac0ce16a3ae`. No demuestra equivalencia con un JAR recibido. Rutas siguientes relativas a ese repositorio:

| Regla | Fuente relevante |
| --- | --- |
| Campos y precios de artículos | `DATABASE_SCHEMA.sql:494`; `src/ModuloProductos/Entidades/Articulo.java:1994`; `src/ModuloProductos/Vistas/FormProducto.java:3335`. `CantidadImpuestos` corresponde a otros impuestos/ITC; IVA se guarda aparte. |
| Stock real | `Articulo.java:1124` suma movimientos activos del año; `:2683` reúne variantes. |
| Migraciones que el DDL antiguo no incluye | `src/ModuloPrincipal/Entidades/VerificadorDeBaseDeDatos.java:2221` precio de composición; `:3572` venta/compra de movimiento; `:3832` PK de stock con computadora modificadora; `:3872` precio por bulto. |
| Unidades, IVA y moneda | Verificador `:838`, `:1060`, `:1173`; `src/Utilidades/Constantes.java:668`. |
| Normal, variante y carnicería; color/talle | `src/Utilidades/Enums/TipoProducto.java:3`; `TipoVariante.java:3`; `FormProducto.java:1587`. |
| Composición y opciones | `src/ModuloProductos/Entidades/ProductoHijo.java:115`; `ProductoOpciones.java:87`; `DATABASE_SCHEMA.sql:1176` y `:1195`. |
| Bultos | `src/ModuloVentas/Vistas/FormVentaProductoCantidadPolicy.java:32`; `src/ModuloVentas/Vistas/PrecioBultoVentaPolicy.java:13`. |
| Ofertas y combos | `src/Utilidades/Enums/TipoOfertaDescuento.java`; `src/ModuloFinanzas/Entidades/OfertaAplicacionCalculador.java`; `src/ModuloVentas/Servicios/OfertaComboService.java`. Cada muestra comercial enlaza su test o fuente en `PRICING_CASES`. |
| Listas y prioridad | `src/ModuloProveedores/Entidades/ListaPrecioDetalle.java`; `test/ModuloVentas/Vistas/FormVentaListaPrecioPrioridadPolicyTest.java`. |

Las comprobaciones Python verifican datos, invariantes y el motor; una prueba SQL sobre un esquema sintético acredita el comportamiento del seed en ese esquema. Ninguna reemplaza la comprobación del paquete real ni GUI/venta sobre el JAR. Quedan fuera activación fiscal, impresión, balanza física, listas por cliente/turno asignadas automáticamente e integraciones externas. Para ampliar escenarios, usar el [roadmap](roadmap.md) y actualizar la [cobertura](cobertura.md) solo con evidencia del nivel realmente ejecutado.

Esta es una batería inicial de ejemplos concretos, no la combinatoria completa del producto. Quedan como extensiones explícitas el ingreso manual de precio o nombre, otros impuestos/ITC, ofertas condicionadas por medio de pago, asignaciones de listas por cliente o turno y sus cruces con descuentos, moneda, cantidades, bultos, permisos y recuperación. Cada extensión necesita datos propios, configuración declarada y expectativas observables; no se considera cubierta porque exista un artículo parecido ni porque el seed se aplique correctamente.
