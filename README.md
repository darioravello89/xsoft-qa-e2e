# XSoft QA E2E

Pruebas automatizadas para que QA compruebe escenarios de XSoft con un menú o con ayuda de su IA local. Comenzamos con **XGestion de escritorio 2.02.189-lts**: acceso, búsqueda de productos y venta simple en efectivo, sin facturación fiscal ni impresión.

**Estado: suite implementada; VALIDACIÓN REAL PENDIENTE.** El repositorio incluye escenarios, controles y documentación. Para confirmar funcionamiento sobre el producto falta importar el paquete privado de QA, calibrar los selectores sobre ese JAR y completar las pruebas reales descritas en [aceptación](docs/qa-manual.md). Un `check`, un `dry-run` o un CI verde no equivalen a haber probado XGestion.

**[Descargar Excel: qué está implementado y qué falta en XGestion](docs/coverage/xgestion-cobertura.xlsx)** · [Cómo leerlo y mantenerlo actualizado](docs/cobertura.md). La foto pública separa las 14 fichas —7 implementadas y 7 planificadas— de la validación real, todavía no registrada en el mapa. Los grupos, el backlog Restobar y los ejemplos del seed no agregan casos ejecutables por sí mismos.

## Empezar por primera vez

1. Usá una **PC Windows exclusiva de QA o una VM Windows**, con escritorio visible y desbloqueado. En una VM, trabajá desde la consola del hipervisor; no por RDP. No uses tu instalación habitual de XGestion.
2. Pedile al responsable de QA el **paquete privado** para tu entorno, por ejemplo `C:\QA\paquete.zip`. Incluye la aplicación, licencia de QA vigente, base saneada, datos del escenario y credenciales. No se descarga de este repositorio. [Cómo preparar el paquete](docs/paquete-privado.md).
3. Para la instalación inicial necesitás Internet y `winget` —incluido con App Installer de Windows—. Podés descargar **Code → Download ZIP** en GitHub y extraerlo, o usar Git si ya está instalado. Abrí PowerShell dentro de la carpeta extraída, o cloná así:

   ```powershell
   git clone https://github.com/darioravello89/xsoft-qa-e2e.git
   cd xsoft-qa-e2e
   .\qa.cmd setup --product xgestion --bundle C:\QA\paquete.zip
   ```

   El instalador prepara Python 3.12, Java 17 y las dependencias cuando faltan. El instalador de Java puede mostrar un permiso de Windows. Si repetís el comando conserva una instalación compatible; no borres carpetas para resolver un error.
4. Cuando termine la instalación, **desconectá la red del Windows que ejecuta XGestion**. Si usás VM, desconectá su adaptador desde el hipervisor; el host puede seguir conectado para usar la IA. **Creá un snapshot limpio después de setup y antes del primer `inspect` o `run`**; en PC física, prepará una imagen recuperable equivalente. Conservá el Windows QA offline después de probar: el JAR puede instalar un agente con tareas persistentes. Para volver a conectarlo, restaurá previamente ese snapshot o imagen, conservando los informes por un canal local privado. Cerrar solamente XGestion no detiene necesariamente ese agente.
5. Comprobá la preparación y abrí el menú:

   ```powershell
   .\qa.cmd doctor --product xgestion
   .\qa.cmd
   ```

   Si `doctor` informa un bloqueo, seguí [solución de problemas](docs/solucion-de-problemas.md). No saltees el control. Si el único pendiente es la calibración inicial, una persona responsable usa `inspect` según la [guía de calibración del JAR](docs/calibracion.md); ese comando conserva los demás controles del entorno.
6. Elegí **Ver grupos** para conocer nombres, descripciones y cantidades. En **Ejecutar grupo**, seleccioná el número del grupo disponible y después el detalle de salida: Resumen (INFO), Paso a paso (DEBUG) o Diagnóstico (TRACE). Empezá por **smoke** y después **ventas**. Los grupos pendientes se muestran sin opción de ejecución. No toques mouse ni teclado durante la prueba y dejá el escritorio desbloqueado.
7. Abrí el resultado con `.\qa.cmd report --latest`. Revisá cada caso: **PASS** significa que sus comprobaciones terminaron bien; **FAIL** requiere revisar el detalle. Un requisito faltante bloquea la ejecución y no acredita un caso aprobado.

Las credenciales quedan en `.env.local` y el entorno de XGestion en `.local/xgestion/`, ambos fuera de Git. La instancia MySQL es propia del runner, en `127.0.0.1:13317`, con base `xsoft_qa`. Las pruebas usan datos descartables de QA; no apuntan a una base compartida de la empresa.

## Comandos para copiar y pegar

Ejecutalos desde la carpeta del repositorio. Podés usar siempre el menú con `.\qa.cmd`.

| Comando | Para qué sirve |
| --- | --- |
| `.\qa.cmd setup --product xgestion --bundle C:\QA\paquete.zip` | Instalar e importar el paquete privado. |
| `.\qa.cmd doctor --product xgestion` | Revisar requisitos y configuración sin ejecutar escenarios. |
| `.\qa.cmd list --product xgestion` | Ver casos y estado: implementado, planificado o manual. |
| `.\qa.cmd list --product xgestion --groups` | Ver nombres, descripciones, etapas y conteos por grupo. |
| `.\qa.cmd list --product xgestion --group ventas` | Ver los casos de venta, incluidos los planificados. |
| `.\qa.cmd run --product xgestion --group smoke` | Comprobar acceso y funciones básicas. |
| `.\qa.cmd run --product xgestion --group ventas` | Ejecutar escenarios de venta. |
| `.\qa.cmd run --product xgestion --group regression` | Ejecutar el conjunto de regresión disponible. |
| `.\qa.cmd run --product xgestion --scenario XG-VEN-001` | Ejecutar un caso por su identificador. |
| `.\qa.cmd run --product xgestion --group ventas --log-level DEBUG` | Ver pasos y comprobaciones durante la ejecución. |
| `.\qa.cmd run --product xgestion --group ventas --log-level TRACE` | Obtener diagnóstico técnico saneado para investigar. |
| `.\qa.cmd report --latest` | Abrir el último reporte local. |
| `.\qa.cmd inspect --product xgestion` | Ayudar al responsable a identificar controles de pantalla. |
| `.\qa.cmd calibrate --locators C:\QA\locators.json` | Importar selectores verificados para el JAR actual, con respaldo local. |
| `.\qa.cmd check` | Validar estructura, documentación y catálogo. |
| `.\qa.cmd coverage` | Mantenedor/IA: regenerar JSON, Excel y manifiesto del mapa público. |
| `.\qa.cmd coverage --check` | Comprobar los tres archivos publicados, sin necesitar Node. |
| `.\qa.cmd seed --dry-run --export` | Revisar 48 productos, 19 ofertas y 5 listas sin abrir MySQL. |
| `.\qa.cmd seed --apply` | Restaurar la base privada QA y aplicar/verificar sus upserts; reemplaza sus datos. |
| `.\qa.cmd run --product xgestion --group ventas --seed catalogo-comercial-v1` | Preparar la batería antes de ejecutar los casos implementados. |
| `.\qa.cmd run --product xgestion --group regression --dry-run` | Validar los siete escenarios sin abrir XGestion ni conectarse a MySQL. |

Los grupos filtran el mismo catálogo: un caso puede pertenecer a `regression`, `ventas` y `efectivo`; no se duplica su ejecución por tener varias etiquetas. Hoy hay **siete casos implementados y siete nuevos de Venta planificados**, que se listan pero no se ejecutan. Un grupo sin casos implementados explica el pendiente y no produce un PASS.

INFO es el nivel predeterminado: muestra cada caso y un resumen. DEBUG agrega los pasos y TRACE el diagnóstico técnico saneado. En cualquier nivel un fallo debe informar caso, paso, esperado, observado, categoría y evidencia disponible. Si la evidencia no determina la causa, se informa **causa no determinada**. Más detalle de log no cambia las comprobaciones ni habilita registrar secretos.

`qa.cmd report --latest` abre `report.html`, el resumen oficial del runner con estado global, grupos y fallos. `robot-report.html` contiene el detalle parcial de Robot y `log.html` sus pasos; se generan desde XML saneado. Para decidir el resultado de la ejecución completa usar el resumen del runner, que también registra fallos de preparación o cierre fuera de los casos Robot.

El [roadmap de XGestion](products/xgestion/docs/roadmap.md) organiza siete etapas: preparación, venta cotidiana, productos y condiciones comerciales, cobros y documentos, después de vender, Restobar e integraciones. La [cobertura y evidencia](products/xgestion/docs/cobertura.md) muestra qué existe y qué falta. El mapa de familias no equivale a cobertura de todos los procesos ni de todas sus combinaciones.

## Productos y organización

La [guía de datos fijos](products/xgestion/docs/seed.md) detalla códigos, precios, stock, variantes y resultados comerciales esperados del seed opcional. Preparar estos datos no agrega casos automatizados ni acredita su comportamiento sobre el JAR.

| Producto | Estado | Motor |
| --- | --- | --- |
| [XGestion](products/xgestion/README.md) | Implementado; ejecución real pendiente de paquete y calibración | Robot Framework + Java Access Bridge |
| [XPORTAL](products/xportal/README.md) | `planned`: sin casos ejecutables todavía | Robot Framework Browser / Playwright, diferido |
| [Mozos Flutter](products/mozos/README.md) | `planned`: app/repositorio a incorporar | Maestro Android, diferido |
| [Consultador web](products/consultador/README.md) | `planned`: URL de QA a configurar | Robot Framework Browser / Playwright, diferido |

Cada producto encapsula `scenarios/` —qué comprobar—, `suites/` —automatización— y `docs/` —operación específica—. Los adaptadores y oráculos Python viven dentro de su producto; `resources/` queda disponible para recursos Robot reutilizables. `framework/` y `scripts/` resuelven instalación, ejecución y controles comunes. Los productos pendientes no tienen tests de ejemplo que aparenten cobertura.

- [Guía para trabajar con IA](docs/guia-ia.md) y [prompts listos para usar](docs/prompts.md).
- [Agregar una funcionalidad y sus pruebas](docs/nuevas-features.md).
- [Especificación inicial](docs/specs/001-plataforma-qa.md), [decisión tecnológica](docs/decisions/001-motores-por-plataforma.md) y [plan de implementación](docs/plans/001-bootstrap.md).
- [Preparación del paquete privado](docs/paquete-privado.md), [calibración](docs/calibracion.md) y [QA de aceptación](docs/qa-manual.md).

## Validaciones para quien mantiene el proyecto

Con el entorno Python preparado, ejecutar:

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m robocop check products
.\.venv\Scripts\python.exe -m pytest
.\qa.cmd check
.\qa.cmd coverage --check
.\qa.cmd run --product xgestion --group regression --dry-run
```

El CI ejecuta estas comprobaciones en Windows y Ubuntu sin credenciales, JAR ni base privada. Los E2E de escritorio se ejecutan localmente y en serie. No subir a GitHub paquetes, bases, credenciales, licencias, reportes ni capturas de QA.

Al cambiar catálogo, grupos, roadmap o ejemplos seed, regenerar con `.\qa.cmd coverage`, revisar JSON/Excel/manifiesto y publicar los tres juntos después de pasar `--check`. Este control funciona sin Node y también se ejecuta en CI. La generación usa el runtime Node con `@oai/artifact-tool` del mantenedor o su IA; **QA no necesita instalar Node para consultar el Excel ni ejecutar E2E**. Ver [mantenimiento del mapa](docs/cobertura.md).
