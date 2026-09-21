# Resolver problemas de preparación y ejecución

Primero ejecutar `.\qa.cmd doctor --product xgestion` y conservar el mensaje sin secretos. No editar los controles para ignorar una falla.

| Situación | Paso siguiente |
| --- | --- |
| Windows no reconoce `winget` | Instalar/actualizar App Installer desde el canal oficial de Windows y volver a abrir PowerShell. |
| Falta Python o Java durante instalación | Mantener Internet conectado solo durante setup, revisar su mensaje y repetir `qa.cmd setup`. No cambiar globalmente la política de PowerShell. |
| No hay entorno Python para ejecutar comandos | Completar `qa.cmd setup` antes de usar el menú operativo. |
| Falta paquete o su hash no coincide | Solicitar el paquete completo al responsable. No corregir el manifest para aceptar un archivo desconocido. |
| Faltan credenciales/licencia | Reemplazar el paquete por uno legítimo de QA. No usar credenciales productivas ni adulterar licencia. |
| Hay adaptador de red activo | Cerrar XGestion, desconectar el adaptador de la VM desde el hipervisor y repetir `doctor`. El host puede permanecer online. |
| La sesión usa RDP o está bloqueada | Usar consola local o del hipervisor; desbloquear el escritorio. |
| Puerto 13317 ocupado o runtime ajeno | Identificar el proceso con el responsable. No detener servicios desconocidos ni cambiar el puerto a una base compartida. |
| MySQL no inicia/restaura | Revisar espacio, versión y preparación del paquete; restaurar solo mediante el runner y su marcador propio. |
| Selectores en borrador o de otro JAR | Seguir `docs/calibracion.md` e importar el mapa verificado con `qa.cmd calibrate --locators RUTA`. No marcar verificación sin comprobar los controles. |
| Un control no existe o aparecen varios | Registrar ventana, alias y mensaje; recalibrar sobre el JAR y contexto correctos. |
| Venta con total/stock/caja inesperados | Revisar fixture, caja y configuración del baseline. No aceptar el valor obtenido como nuevo esperado sin contrastar la regla de negocio. |
| Producto figura `planned` | Aún no tiene E2E ejecutable; completar su onboarding antes de intentar correrlo. |
| Un grupo muestra cero implementados | Consultar `qa.cmd list --product xgestion --group NOMBRE` y el roadmap. Puede tener fichas planificadas o solo una familia prevista; no intentar fabricar un PASS. |
| Un caso figura `planned` o `manual` | Su procedimiento no tiene automatización ejecutable. Revisar ficha/dependencias; `run` no lo ejecuta aunque aparezca en `list`. |
| Grupo desconocido o filtro vacío | Consultar `qa.cmd list --product xgestion --groups` y usar su ID exacto, no el número temporal del menú. |
| `list --groups --group ventas` falla | Son alternativas: usar uno para resumen de grupos u otro para los casos de un grupo. |
| INFO parece demasiado breve | Usar `--log-level DEBUG` para pasos o TRACE para diagnóstico saneado. Conservar primero la evidencia anterior; repetir restaura el entorno. |
| Un fallo no permite identificar causa | Registrar paso, esperado, observado, categoría y evidencia; informar «causa no determinada» y qué dato falta. Más detalle de log no convierte una hipótesis en causa comprobada. |

Una falla del entorno no es un defecto confirmado del ERP. Un `FAIL` con entorno y datos verificados debe investigarse contra el comportamiento esperado del escenario. Si el caso solo pasó un dry-run, no hay evidencia de ejecución de UI o base.

No eliminar una comprobación ni cambiar el esperado por el observado. Revisar primero el perfil: por ejemplo, `cartelPagoVuelto=false` cambia el flujo de cobro simple, y el bloqueo de stock depende de configuración. Los casos de Venta cotidiana requieren el perfil definido en sus fichas. Las variantes pertenecen al roadmap y no deben mezclarse en una misma ejecución sin documentarlas.
