# Preparar el paquete privado de XGestion

Esta tarea corresponde al responsable técnico de QA. El QA que ejecuta pruebas recibe un ZIP listo para importar. El paquete se distribuye por un canal privado autorizado, fuera de Git y de los prompts de IA.

## Contenido

El ZIP lleva `manifest.json` en la raíz y archivos en rutas relativas sin `..`, rutas absolutas ni enlaces que salgan del paquete. Usar [manifest.example.json](../templates/manifest.example.json) como estructura; reemplazar todos los hashes de ejemplo por SHA-256 calculados sobre los archivos finales.

| Entrada en `files` | Archivo | Condición |
| --- | --- | --- |
| `app` | JAR ejecutable | Build `2.02.189-lts` identificado y aprobado para QA. |
| `dump` | SQL | Baseline saneado, compatible con MySQL `5.7.44` y reservado para QA. |
| `mysql` | ZIP portable MySQL | Distribución Windows x64 `5.7.44`; no una instalación del host. |
| `config` | `config.properties` | Configuración legítima del perfil sandbox y licencia QA vigente para uso offline. |
| `fixtures` | JSON | Contexto, producto y medios/documentos concretos del baseline. |
| `locators` | JSON | Selectores accesibles calibrados contra el SHA-256 de `app`. |
| `credentials` | Archivo `.env` | Variables privadas descritas abajo. |

El hash detecta archivos diferentes o corruptos; no acredita quién preparó el paquete. Recibirlo únicamente de la persona responsable y por el canal privado del equipo.

## Preparar aplicación, datos y configuración

1. Usar una base QA ya aislada y eliminar datos personales, integraciones activas, credenciales productivas y colas de trabajo externas antes de producir el dump. La infraestructura importa un dump saneado; no sanitiza una copia de producción automáticamente.
2. Mantener esquema, versión y datos necesarios del ERP. El baseline debe contener empresa/sucursal/computadora/usuario QA válidos, licencia offline vigente y una caja utilizable. No generar ni adulterar una licencia desde este repositorio.
3. Apagar cloud, SyncV2 y perfiles de integración en la configuración y datos del entorno. Desactivar fiscalización, impresión y comanda para los casos iniciales. Esos controles complementan la desconexión de red; no la reemplazan.
4. Preparar un producto simple, activo, con stock suficiente, cantidad del escenario igual a `2` y precio final ARS `1000.00` por unidad, sin descuentos ni recargos: total ARS `2000.00`. Elegir un código inexistente que tampoco se interprete como código de balanza u otro atajo del ERP.
5. Seleccionar pago efectivo y comprobante interno no fiscal `99` —presupuesto—, cerrado mediante Cobrar sin F9. Registrar sus IDs existentes en el fixture. Verificar que impuestos, unidad y redondeo del baseline mantienen el total esperado.
6. Verificar que el dump solo contiene la base de negocio esperada y no incluye usuarios/schemas de sistema, tareas externas ni instrucciones para redirigir restauraciones fuera de la instancia QA.

La instancia destino siempre es propia del runner: `127.0.0.1:13317`, base `xsoft_qa`, usuario `root` de esa instancia privada. No reutilizar el servicio MySQL de XAMPP ni un schema en un servidor compartido. La cuenta root se limita a esta instancia descartable porque el ERP requiere operaciones como `SET GLOBAL`.

`conexionUsuario` debe contener `root` cifrado por el ERP, y `conexionPassword` debe contener la misma contraseña de `QA_DB_PASSWORD`, también cifrada con el mecanismo del ERP. El runner conserva esos valores y no reimplementa ni publica sus claves de cifrado; fuerza únicamente host, puerto, base y sincronización desactivada al generar su configuración local.

El SQL se importa con una cuenta propia limitada exactamente a `xsoft_qa`: no debe contener instrucciones globales, `GTID_PURGED`, grants ni `DEFINER` de cuentas externas al importador, incluido `DEFINER=root@localhost`. Preparar las definiciones de funciones, procedimientos, vistas y triggers omitiendo ese `DEFINER` explícito o usando `CURRENT_USER`, sin quitar los objetos ni cambiar su lógica. El runner no reescribe un dump arbitrario ni eleva los permisos para importarlo; un respaldo incompatible debe prepararlo nuevamente el responsable QA.

La cuenta importadora se conserva como `DEFINER` de los objetos restaurados y queda con `ACCOUNT LOCK` al terminar, incluso si falla la importación. Esto impide nuevos logins y permite que los triggers y funciones sigan ejecutándose con permisos del schema privado. Su contraseña efímera no se guarda en el registro del runtime. En una restauración posterior solo se elimina una cuenta anterior registrada como propia cuando ya no existe ningún objeto que la referencie; nunca se eliminan cuentas por compartir un prefijo. Una importación parcial bloquea la preparación y no acredita un seed ni un caso E2E aprobado.

## Credenciales locales

El archivo privado de credenciales contiene:

- `QA_LOGIN_USER`: usuario QA de XGestion.
- `QA_LOGIN_PASSWORD`: contraseña de ese usuario QA.
- `QA_DB_PASSWORD`: contraseña dedicada de la instancia local QA.
- `QA_JAVA_HOME`: opcional; el setup puede detectar Java 17 si se omite. Si se informa, debe señalar el JDK de esa PC, no el del equipo que preparó el ZIP.

El setup importa estos valores a `.env.local`, ignorado por Git. No ejecutar comandos que impriman el archivo. No usar contraseñas de producción. Las URLs futuras `XPORTAL_BASE_URL` y `CONSULTADOR_BASE_URL` también se configuran localmente cuando se incorporen esos productos.

## Fixtures y selectores

`fixtures.json` tiene `schema_version: 1` y las siguientes secciones:

| Sección | Campos |
| --- | --- |
| `context` | `empresa`, `sucursal`, `computadora`, `usuario_id`, `empresa_label`, `sucursal_label`, `usuario_label` |
| `product` | `id`, `code`, `name`, `unit_price` como decimal textual, `quantity: 2` |
| `sale` | `cash_payment_id`, `non_fiscal_document_id` |
| `ui` | `products_empty_text`, texto exacto observado para una búsqueda sin resultados |
| Raíz | `nonexistent_product_code` |

Los IDs referencian registros reales del baseline; los labels son textos exactos visibles en la UI. Revisar los ejemplos y validadores de `products/xgestion/` antes de generar una versión del paquete.

El [catálogo comercial opcional](../products/xgestion/docs/seed.md) agrega productos `QA-SEED-*`, ofertas y listas con IDs reservados `980xxx` después de restaurar. No reemplaza `fixtures.json` ni el producto simple 90001 del ejemplo. El baseline debe conservar contexto, unidades, monedas, IVA y esquema compatibles; el seed los valida y no migra el ERP ni modifica catálogos globales. Prepararlo sin ofertas generales o listas por defecto que alteren los montos de los ejemplos. Un `run` normal no aplica esta batería; se solicita con `--seed catalogo-comercial-v1`. `qa.cmd seed --apply` también es explícito y restaura primero la base QA, descartando sus datos operativos anteriores.

`locators.json` lleva `schema_version: 1`, `windows`, `elements` y `calibration`. Cada elemento asocia `window` con una ventana declarada y `query` con una búsqueda de Java Access Bridge. La calibración verificada debe registrar `status: verified`, `app_sha256`, `verified_by`, `verified_at` y `jab_version`. El archivo de ejemplo en estado borrador bloquea el E2E hasta la [calibración real](calibracion.md). Para actualizar solo esos selectores localmente, usar `qa.cmd calibrate --locators C:\QA\locators.json`, que valida el mapa y conserva un respaldo.

## Verificar e importar

Calcular hashes sin abrir el contenido sensible:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath C:\QA\paquete\app\XGestion.jar
```

Repetir para cada archivo declarado, completar el manifest y generar el ZIP. En Windows QA con Internet disponible para instalar requisitos:

```powershell
.\qa.cmd setup --product xgestion --bundle C:\QA\paquete.zip
```

Después desconectar la red y ejecutar `doctor`. Una importación correcta no verifica que todos los selectores o reglas del escenario funcionen: eso se acredita con el E2E real.

## Reemplazo y recuperación

Cerrar XGestion y terminar la ejecución antes de cambiar un paquete. El setup conserva el perfil existente: repetir el mismo paquete es idempotente; importar uno distinto se bloquea. En esta versión, preparar un nuevo clon normal en otra carpeta QA para importar un paquete diferente y conservar el anterior. No usar worktrees ni ejecutar dos perfiles simultáneamente, pues comparten el puerto local reservado.

La restauración del baseline de una ejecución solo corresponde al runtime propio con marcador de propiedad válido; si el runner rechaza una ruta o instancia, investigar la causa en lugar de editar el marcador. No eliminar manualmente una carpeta MySQL ni usar herramientas de restauración sobre bases compartidas.
