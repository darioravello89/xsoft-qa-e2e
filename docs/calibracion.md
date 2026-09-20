# Calibrar XGestion para el JAR recibido

La calibración la realiza una persona con conocimiento del producto, una vez por build/UI que cambie. Su objetivo es comprobar que Java Access Bridge identifica los controles y que los casos interactúan con el XGestion real. Los selectores de ejemplo no son selectores verificados.

## Preparación

Usar Windows QA exclusivo, Java 17 x64, bridge habilitado y la licencia/configuración privadas correctas. Instalar antes de desconectar la red. Mantener consola local o del hipervisor visible, sin RDP y sin usuarios trabajando dentro del ERP.

Después de setup y con la red desconectada, crear un snapshot limpio de la VM antes del primer `inspect` o `run`. Para PC física, preparar una imagen recuperable equivalente. Mantener Windows offline después de probar; antes de reconectarlo, guardar evidencia por un canal local privado y restaurar ese snapshot o imagen.

Confirmar el SHA-256 del JAR importado y ejecutar:

```powershell
.\qa.cmd doctor --product xgestion
.\qa.cmd inspect --product xgestion
```

En un paquete con selectores todavía en borrador, `doctor` bloqueará por calibración pendiente. Resolver primero cualquier otro requisito que indique. `inspect` está diseñado para completar esa calibración: permite observar el JAR sin exigir selectores verificados y mantiene los controles de red, escritorio, configuración y propiedad de la instancia. Después de importar el mapa verificado, repetir `doctor` y exigir que termine sin bloqueos antes de ejecutar escenarios.

`inspect` prepara/restaura la instancia QA propia y abre el JAR para una inspección supervisada. El responsable navega manualmente por la aplicación; al presionar Enter en la consola se captura el árbol de ventanas del proceso propio. Con `q` termina la inspección y se cierra ese JAR. No es un E2E ni acredita una venta. La salida se conserva localmente y no debe publicarse; seguir también la [guía del producto](../products/xgestion/docs/calibracion.md).

## Prueba técnica mínima

1. Verificar que el bridge se conecta al proceso Java correcto y detecta la ventana de acceso.
2. Identificar usuario/contraseña, acción de login y mensaje de error sin guardar secretos en la salida.
3. Verificar ventana principal y contexto visible de empresa, sucursal y usuario.
4. Identificar búsqueda, grilla de productos y mensajes de producto inexistente.
5. Recorrer apertura/cancelación de venta y los diálogos de medio de pago/efectivo, comprobando que se pueden operar y leer sus resultados.
6. Cada alias debe encontrar un solo control visible en la ventana esperada. Usar propiedades estables y semánticas; no resolver ambigüedad mediante índice de aparición ni coordenadas.

Si el árbol no expone un control necesario, registrar ventana, alias y evidencia saneada. La ejecución permanece bloqueada; un cambio de producto o de estrategia requiere tratar ese problema explícitamente.

## Resultado y mantenimiento

Completar un `locators.json` privado fuera del bundle importado, con los títulos exactos de ventana y queries que exige el adaptador. Cuando todos los aliases hayan sido comprobados, registrar `calibration.status: verified`, hash del JAR, responsable, fecha ISO y versión de Java Access Bridge. Importarlo mediante:

```powershell
.\qa.cmd calibrate --locators C:\QA\locators.json
```

Este comando valida mapa completo y SHA-256 del JAR, respalda la versión anterior y actualiza exclusivamente los selectores y su hash en el manifest local. Repetir setup con el ZIP original conserva la calibración local. No editar directamente archivos importados ni eliminar marcadores para forzar su aceptación.

Para distribuir la calibración a otra estación, el responsable incorpora el archivo verificado y su hash al paquete privado final. Un paquete diferente completo se importa en un nuevo clon normal; el perfil anterior se conserva. Ejecutar un solo perfil a la vez.

Ejecutar los casos reales después de calibrar. Si cambia el JAR, la calibración anterior no se presume válida: comparar comportamiento y repetir la verificación para el nuevo hash. No marcar un borrador como `verified` solo para superar `doctor`.
