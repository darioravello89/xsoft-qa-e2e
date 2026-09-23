# Aceptación de la plataforma y primera ejecución real

Estado inicial: **pendiente** de paquete privado legítimo, calibración y ejecución sobre XGestion. Completar este protocolo antes de acreditar la plataforma para QA rutinaria.

La ampliación de roadmap/grupos/logs se revisa primero **sin abrir XGestion**: `qa.cmd check`, `list --groups`, `list --group ventas`, `list --group promociones`, menú y dry-run deben distinguir 96 implementados —cinco smoke, nueve ventas y 82 promociones— de 202 pendientes (PRM-077/078 más remitos, Restobar, listas y circuitos críticos). Los planificados no se ejecutan; las referencias R01–R20 de Restobar no cuentan como fichas. Usar los tests del framework con canarios sintéticos para revisar sanitización y fallos en INFO/DEBUG/TRACE. Eso acepta el funcionamiento técnico de la ampliación, no el producto.

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
   contexto, búsqueda, grilla y diálogos de venta. Preparar sales_journeys
   con columnas, aviso y defaults calibrados para VEN-003 a VEN-009. Registrar evidencia privada
   y calibración asociada al SHA-256 del JAR. No inventar selectores.
   Si doctor bloquea sólo por calibración inicial, usar inspect según esa guía;
   la inspección mantiene los demás controles. Importar el mapa y repetir doctor.
   Para PRM-001 a PRM-007 completar products/xgestion/docs/promociones.md:
   perfil ARS, interno 99, Ninguna Lista, otros descuentos y puntos desactivados;
   promociones-v1, ventas-etapa1 y ventas-teclado-v1 para el mismo SHA256 del JAR.

6. Ejecutar .\qa.cmd list --product xgestion --groups y
   .\qa.cmd list --product xgestion --group ventas.
   Abrir .\qa.cmd sin argumentos, Ver grupos y Ejecutar grupo.
   Esperado: nombres/descripciones/conteos comprensibles; 96 casos
   implementados y 202 planned en el catálogo general. En ventas hay
   nueve implementados y doce planned; en promociones, 77 implementados y 2 planned.
   Consultar promociones-alcances, promociones-agrupadas, promociones-combos
   y promociones-condiciones: 31, 21, 5 y 13 implementados respectivamente.
   Sólo promociones-condiciones conserva 2 pendientes (PRM-077/078).
   Los pendientes no pueden ejecutarse.
   Elegir nivel 1 Resumen, 2 Paso a paso o 3 Diagnóstico en el menú.

7. Ejecutar .\qa.cmd run --product xgestion --group smoke.
   Esperado: casos de acceso/consulta coinciden con su descripción y datos;
   no hay conexiones externas, fiscalización ni impresión.

8. Ejecutar .\qa.cmd run --product xgestion --group ventas.
   Esperado: cancelación no persiste ni altera stock/caja; venta efectiva
   registra las dos unidades, total esperado y deltas de stock/caja correctos.
   Comprobar aviso de código ausente; recibido 3000/vuelto 1000; cancelación
   intermedia sin persistencia y un solo cobro posterior. VEN-008 mantiene
   la misma ventana tras cobrar; VEN-009 reabre sin reiniciar el proceso.

9. Revisar .\qa.cmd list --product xgestion --group promociones.
   Ejecutar cada ID PRM de forma independiente, por ejemplo:
   .\qa.cmd run --product xgestion --scenario XG-PRM-001 --log-level DEBUG
   y luego el grupo completo:
   .\qa.cmd run --product xgestion --group promociones --log-level DEBUG
   Esperado: anuncia el seed requerido y lo prepara después de restaurar;
   compara bruto/oferta/neto, edita la misma línea y cancela sin movimientos.
   Al retomar persiste una sola venta/cobro y los deltas esperados de stock/caja.
   Vencida/futura/inactiva exigen antes el control PCT x 1 = 900 abandonado
   sin efectos. Abrir .\qa.cmd report --latest y registrar los siete resultados,
   SHA256/build JAR, paquete, perfil, fecha del seed y evidencia privada.

10. Repetir la regresión completa tres veces, una ejecución a la vez:
   .\qa.cmd run --product xgestion --group regression
   Esperado: resultados consistentes desde baseline, sin intervención manual
   para arreglar datos entre casos y sin afectar bases o procesos ajenos.

11. Abrir .\qa.cmd report --latest. Revisar versión, casos y errores.
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

12. Mantener la VM sin red después de la ejecución: el JAR puede instalar
    un agente persistente. Antes de reconectar, conservar evidencia por un
    canal local privado y restaurar el snapshot o imagen limpia anterior al ERP.
    Registrar responsable, fecha, commit, hash JAR, identificación del paquete,
    resultados de las tres repeticiones y ubicación privada de la evidencia.

13. Ejecutar Ruff, Robocop, pytest, qa.cmd check, qa.cmd coverage --check y
    qa.cmd run --group regression --dry-run. Registrar
    estos resultados como controles técnicos, separados del E2E real.

No marcar este protocolo aprobado si falta un paso real. Documentar el bloqueo
y el requisito faltante; no subir paquetes, bases, secretos o reportes a GitHub.
```

La aceptación de Venta cotidiana conserva los nueve casos de venta, incluidos los siete incorporados después del lote inicial. Probar cada uno de forma independiente y en grupo, incluidos los dos recorridos consecutivos dentro del mismo proceso. VEN-003/007 usan botón y Ctrl+E con `ventas-teclado-v1` calibrado; sin esa feature conservan el doble clic legado sobre la celda JAB. Comprobar identidad del producto y cambio de la misma fila; en 007, también rechazo del abandono sin mutaciones intermedias. Las 14 fichas anteriores a promociones —cinco smoke y nueve ventas— conservan su alcance.

La aceptación de [promociones](../products/xgestion/docs/promociones.md) añade siete casos y exige registrar sus resultados por separado, junto con SHA256/build JAR y perfil. Confirmar los importes de cada ficha, la cancelación sin persistencia y el cobro posterior único; no extender ese resultado a combos, listas ni demás ejemplos del seed. Una revisión documental, un test Python o un dry-run no acredita ejecución real. Seguir [roadmap](../products/xgestion/docs/roadmap.md) y [cobertura](../products/xgestion/docs/cobertura.md).

La ampliación de [canastas de ofertas](../products/xgestion/docs/canastas-ofertas.md) agrega 70 recorridos: probar alcances, agrupadas, combos, fechas, listas y medios manuales. Para PRM-070 y PRM-079 verificar todas las fases desde baseline, un único resultado por caso y el bloqueo ante evidencia incompleta. Registrar el perfil observado, el SHA256 del JAR y el informe por fase. PRM-077/078 permanecen pendientes hasta disponer del paquete de varias empresas/sucursales. Las leyendas visuales de combos de PRM-060/062 conservan su comprobación manual pendiente de accesibilidad; la automatización verifica la identidad de la oferta persistida.

La ampliación documental agrega 24 remitos, 40 Restobar y 28 listas. Verificar que `list --group remitos`, `restobar` y `listas-precios` permite leer sus fichas y que el menú no los ofrece para ejecutar. El dry-run de regresión conserva 96 casos; ninguna de las 92 fichas nuevas puede aparecer aprobada.

Para la ampliación de circuitos críticos, revisar `list --group ctacte-clientes`,
`ctacte-proveedores`, `cuotas`, `libro-diario`, `caja`, `conciliacion`,
`inventario` y `respaldos`. El [mapa central](../products/xgestion/docs/circuitos-criticos.md)
enlaza 58 fichas nuevas planned. Deben verse en Excel y menú como pendientes,
sin habilitar ejecución ni aumentar los 96 casos del dry-run. Confirmar que
cada variante informa los datos, permisos y preparación todavía faltantes.

## Complemento de escenarios críticos

El [mapa complementario](../products/xgestion/docs/complementos-criticos.md) añade 50 fichas
planned de cobros/documentos, servicios, continuidad y beneficios. Revisar
los filtros del catálogo y del Excel; deben conservar 96 implementados,
202 pendientes y ninguna validación real inferida. Los casos nuevos no se
ejecutan. Datos, accesibilidad y laboratorios propios siguen pendientes.

## Ofertas USD P0

Seguir [el perfil y las trece variantes](../products/xgestion/docs/ofertas-usd.md), seleccionando `ofertas-usd`. Comprobar los cinco IDs PRM-080..084 en menú/Excel, prioridad P0 y validación real pendiente. En el JAR calibrado: USD 100 con precio final USD 50 debe cobrar ARS 75000 a cotización 1500; con dos unidades ARS 150000. Cambiar cantidad y cancelar/retomar no duplica descuentos ni cobros. El informe debe identificar moneda, esperado y observado incluso en INFO. No aprobar si falta alguna variante, perfil o evidencia.
