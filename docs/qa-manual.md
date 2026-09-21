# Aceptación de la plataforma y primera ejecución real

Estado inicial: **pendiente** de paquete privado legítimo, calibración y ejecución sobre XGestion. Completar este protocolo antes de acreditar la plataforma para QA rutinaria.

La ampliación de roadmap/grupos/logs se revisa primero **sin abrir XGestion**: `qa.cmd check`, `list --groups`, `list --group ventas`, menú y dry-run deben mostrar siete casos implementados y siete planificados. Los planificados no se ejecutan; las referencias R01–R20 de Restobar no cuentan como fichas. Usar los tests del framework con canarios sintéticos para revisar sanitización y fallos en INFO/DEBUG/TRACE. Eso acepta el funcionamiento técnico de la ampliación, no el producto.

```text
QA MANUAL — XSOFT QA E2E

1. Preparar una VM Windows limpia y exclusiva, con consola del hipervisor.
   No usar RDP. Confirmar que no hay instalaciones/bases productivas.

2. Con Internet disponible, clonar el repositorio y ejecutar:
   .\qa.cmd setup --product xgestion --bundle C:\QA\paquete.zip
   Esperado: requisitos instalados, paquete verificado y entorno local listo.
   Repetir setup con el mismo paquete y verificar comportamiento idempotente.
   Desconectar la red y crear un snapshot limpio antes de cualquier inspect
   o run. En PC física, preparar una imagen recuperable equivalente.

3. Verificar que .env.local y .local/ están ignorados por Git.
   No imprimir valores ni adjuntar estos archivos. Con un paquete de prueba
   sintético, verificar que hashes inválidos/rutas ajenas sean rechazados.

4. Desconectar la red de la VM y ejecutar:
   .\qa.cmd doctor --product xgestion
   Esperado: valida requisitos o explica exactamente la condición pendiente.
   Confirmar rechazo de sesión RDP, red activa y runtime sin propiedad válida
   mediante los tests del framework, sin desactivar controles para operar.

5. Completar docs/calibracion.md para el JAR recibido. Confirmar acceso,
   contexto, búsqueda, grilla y diálogos de venta. Registrar evidencia privada
   y calibración asociada al SHA-256 del JAR. No inventar selectores.
   Si doctor bloquea sólo por calibración inicial, usar inspect según esa guía;
   la inspección mantiene los demás controles. Importar el mapa y repetir doctor.

6. Ejecutar .\qa.cmd list --product xgestion --groups y
   .\qa.cmd list --product xgestion --group ventas.
   Abrir .\qa.cmd sin argumentos, Ver grupos y Ejecutar grupo.
   Esperado: nombres/descripciones/conteos comprensibles; siete casos
   implementados y siete planned en el catálogo general. En ventas hay
   dos implementados y siete planned. Los pendientes no pueden ejecutarse.
   Elegir nivel 1 Resumen, 2 Paso a paso o 3 Diagnóstico en el menú.

7. Ejecutar .\qa.cmd run --product xgestion --group smoke.
   Esperado: casos de acceso/consulta coinciden con su descripción y datos;
   no hay conexiones externas, fiscalización ni impresión.

8. Ejecutar .\qa.cmd run --product xgestion --group ventas.
   Esperado: cancelación no persiste ni altera stock/caja; venta efectiva
   registra las dos unidades, total esperado y deltas de stock/caja correctos.

9. Repetir la regresión completa tres veces, una ejecución a la vez:
   .\qa.cmd run --product xgestion --group regression
   Esperado: resultados consistentes desde baseline, sin intervención manual
   para arreglar datos entre casos y sin afectar bases o procesos ajenos.

10. Abrir .\qa.cmd report --latest. Revisar versión, casos y errores.
    report.html es el resumen oficial del runner: estado global, grupos y
    fallos. robot-report.html y log.html son el detalle parcial de Robot y
    sus pasos, generados desde XML saneado; no reemplazan el estado global.
    Verificar que contraseñas/cadenas de conexión no aparecen en reportes,
    consola ni diagnósticos. Usar canarios sintéticos para esta comprobación.
    INFO muestra caso/resultado/resumen; DEBUG agrega pasos y TRACE diagnóstico
    saneado. Un fallo informa paso, esperado, observado, categoría y evidencia
    en todos los niveles. Si no se probó la causa, indica causa no determinada.
    Primero conservar el reporte antes de repetir con otro nivel, porque el
    runner restaura el baseline en cada ejecución.

11. Mantener la VM sin red después de la ejecución: el JAR puede instalar
    un agente persistente. Antes de reconectar, conservar evidencia por un
    canal local privado y restaurar el snapshot o imagen limpia anterior al ERP.
    Registrar responsable, fecha, commit, hash JAR, identificación del paquete,
    resultados de las tres repeticiones y ubicación privada de la evidencia.

12. Ejecutar Ruff, Robocop, pytest, qa.cmd check y
    qa.cmd run --group regression --dry-run. Registrar
    estos resultados como controles técnicos, separados del E2E real.

No marcar este protocolo aprobado si falta un paso real. Documentar el bloqueo
y el requisito faltante; no subir paquetes, bases, secretos o reportes a GitHub.
```

La futura aceptación de Venta cotidiana incorpora XG-VEN-003 a XG-VEN-009 solo después de implementarlos/calibrarlos. Probar cada uno de forma independiente y en grupo, incluidos los dos recorridos consecutivos dentro del mismo proceso. No cambiar sus estados ni afirmar que se ejecutaron como parte de la revisión documental. Seguir [roadmap](../products/xgestion/docs/roadmap.md) y [cobertura](../products/xgestion/docs/cobertura.md).
