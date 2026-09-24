# Primera ejecución en tu PC, desde cero

Todavía faltan **la VM Windows de QA y el paquete privado**. Estos pasos preparan
el entorno y luego ejecutan los circuitos. No usar la instalación habitual de
XGestión, sus servicios MySQL ni una base de trabajo compartida.

## 1. Preparar la VM

Con el responsable de infraestructura, crear una VM Windows x64 exclusiva para
QA. Definir el hipervisor disponible y los recursos según el paquete; no hay un
tamaño medido para esta entrega. Entrar por la consola del hipervisor, con
escritorio visible y desbloqueado. No usar RDP. El host puede conservar Internet
y la IA; la VM deberá quedar sin red antes de ejecutar el JAR.

## 2. Conseguir el paquete privado

Solicitar al responsable de XGestión el ZIP descrito en
[Preparar paquete privado](paquete-privado.md). Debe contener JAR, licencia QA,
MySQL portable, baseline saneado, configuración, fixtures, credenciales y
selectores. Pedir expresamente el perfil
[circuitos-comerciales-v1](../products/xgestion/docs/circuitos-completos.md#perfil-privado-y-calibración),
con remitos y cierre normal, cotización 1500 y comprobantes internos.

El repo no incluye ni inventa esos archivos. Mantenerlos fuera de Git y de los
prompts. El equipo técnico debe calibrar los controles contra el SHA256 exacto
del JAR. Los ejemplos públicos `CALIBRAR` no habilitan las pruebas reales.

## 3. Instalar dentro de la VM

Con Internet habilitado sólo durante la instalación, descargar/clonar este
repositorio. Abrir PowerShell en esa carpeta. `C:\QA\paquete.zip` es una ruta
de ejemplo: reemplazarla por la del ZIP recibido.

```powershell
git clone https://github.com/darioravello89/xsoft-qa-e2e.git
cd xsoft-qa-e2e
.\qa.cmd setup --product xgestion --bundle C:\QA\paquete.zip
```

Si Git todavía no está instalado, descargar ZIP desde GitHub, extraerlo y abrir
PowerShell allí; ejecutar sólo el comando setup. El instalador prepara Python,
Java y dependencias, e importa las credenciales locales del paquete.
No editar ni pegar contraseñas en comandos. Ver quick start del [README](../README.md).

## 4. Aislar y guardar un punto limpio

Desconectar el adaptador de red de la VM desde el hipervisor. Crear un snapshot
limpio después de setup y **antes** de inspect/run. No ejecutar el ERP aún.
Para volver a conectar la VM después de las pruebas, restaurar ese snapshot
tras conservar los informes por un canal local privado: el JAR puede instalar
un agente persistente; cerrar su ventana no garantiza detenerlo.

## 5. Comprobar preparación y catálogo

```powershell
.\qa.cmd doctor --product xgestion
.\qa.cmd check
.\qa.cmd list --product xgestion --group circuitos-completos
.\qa.cmd run --product xgestion --group circuitos-completos --dry-run
```

Doctor debe aprobar el ambiente. Si falta calibración, el responsable sigue
[calibracion.md](../products/xgestion/docs/calibracion.md) y entrega el mapa
verificado; no modificar flags para omitir ese control. El dry-run debe mostrar
tres casos **VALIDADO EN SECO**. FIN-012 queda pendiente por ACC-010, sin PASS.

## 6. Ejecutar la primera prueba real y luego cada circuito

Con VM offline y escritorio disponible, ejecutar de a uno:

```powershell
.\qa.cmd run --product xgestion --group smoke --log-level INFO
.\qa.cmd run --product xgestion --scenario XG-FIN-011 --seed catalogo-comercial-v1 --log-level DEBUG
.\qa.cmd run --product xgestion --scenario XG-FIN-013 --seed catalogo-comercial-v1 --log-level DEBUG
.\qa.cmd run --product xgestion --scenario XG-FIN-014 --seed catalogo-comercial-v1 --log-level DEBUG
```

No usar el teclado/mouse mientras trabaja el runner. Cada invocación restaura
su base privada antes de aplicar el seed; los tests anteriores no son datos
necesarios para el siguiente. No se ejecuta SQL manual ni se llama Robot directo.
Si falla smoke, resolver ese bloqueo antes de los circuitos.

| Prueba | Qué esperar |
| --- | --- |
| FIN-011 | Venta ARS 300.000, recibido 350.000, vuelto 50.000; stock −2 y caja +300.000 una vez |
| FIN-013 | Remito ARS 362.400; cuatro ingresos +2 y una deuda proveedor; costos 600 ARS/60 USD. Precios calculados 1200 ARS/120 USD; venta posterior ARS 180.000 |
| FIN-014 | Apertura sin fondo, venta ARS 150.000 y cierre asociado; reporte muestra efectivo/total 150.000 sin movimientos repetidos |

Después de resolver la calibración y obtener ejecuciones correctas individuales:

```powershell
.\qa.cmd run --product xgestion --group circuitos-completos --seed catalogo-comercial-v1 --log-level INFO
```

## 7. Leer el resultado y mantener el mapa

La consola informa **OK, FALLÓ, BLOQUEADO, CANCELADO** o **VALIDADO EN SECO** y
la ruta local del informe. Un bloqueo de entorno no demuestra un defecto del ERP.
Ante fallo, leer paso/esperado/observado y el HTML local; la causa raíz puede
seguir sin determinar. No repetir cobros manualmente para destrabar el test.
Conservar informe, SHA256 del JAR, paquete y perfil con el responsable QA.

El [Excel](coverage/xgestion-cobertura.xlsx) controla qué está automatizado y qué
falta. No lee automáticamente los resultados privados ni convierte un dry-run
en aceptación real. Filtrar por **circuitos-completos**. La cuenta corriente
continúa bloqueada hasta agregar y validar el atajo de acceso al cliente.
