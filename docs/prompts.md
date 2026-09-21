# Prompts para copiar y pegar

## Primera ejecución

```text
Leé AGENTS.md y README.md de este repositorio. Ayudame a preparar XGestion
usando el paquete privado que ya tengo, sin mostrar credenciales. Revisá los
prerrequisitos y explicame un paso por vez cómo instalar con qa.cmd setup,
desconectar la red de la VM, ejecutar doctor y correr el grupo smoke.
Si falta una condición, explicá el bloqueo sin saltearlo. Diferenciá dry-run
de una prueba real. No modifiques otros repositorios.
```

## Ejecutar un grupo

```text
Leé AGENTS.md, el roadmap y la cobertura de XGestion. Consultá
qa.cmd list --product xgestion --groups y después
qa.cmd list --product xgestion --group ventas. Explicá los recorridos y sus
efectos, separando implementados de planificados. Ejecutá doctor y, si cumple
el entorno aislado, corré qa.cmd run --product xgestion --group ventas
--log-level INFO. Al terminar indicá casos ejecutados, resultados y reporte
local sin secretos. No publiques artefactos ni hagas commits.
```

## Investigar un fallo

```text
Leé AGENTS.md. Necesito diagnosticar el fallo del caso [ID]. Usá el último
reporte local y su Markdown. Separá problemas de entorno, selectores,
datos y comportamiento del producto. No imprimas secretos. No cambies el
resultado esperado ni desactives aserciones para conseguir un PASS.
Usá INFO para resumen, DEBUG para pasos o TRACE para diagnóstico saneado.
Conservá caso, paso, esperado, observado, categoría y evidencia disponible.
Entregá causa comprobada y corrección propuesta; si no alcanza la evidencia,
decí causa no determinada y qué comprobación falta. No inventes una causa.
```

## Agregar cobertura

```text
Leé AGENTS.md, docs/nuevas-features.md y templates/scenario.md. Incorporá
pruebas para [funcionalidad y criterio de aceptación] dentro de [producto].
Revisá primero roadmap/cobertura y reutilizá una ficha planned si existe.
Describí objetivo de usuario, perfil, datos, resultados por paso, recuperación
y límites; dejá SQL/selectores en un anexo. Reutilizá recursos y grupos.
Actualizá Markdown, tags, tests y datos del paquete conjuntamente al implementar.
No inventes selectores, credenciales ni esquemas ni conviertas un test unitario
del ERP en una supuesta prueba E2E. Incluí logs saneados por nivel.
Ejecutá las validaciones técnicas y declará qué falta para la prueba real.
No modifiques el producto ni publiques cambios sin un pedido específico.
```

## Planificar la próxima familia

```text
Leé el roadmap y la matriz de cobertura de XGestion. Planificá [familia]
desde lo que hace el usuario. Revisá variantes, configuración, roles y
dependencias, usando las fuentes/tests del producto como insumo. No ejecutes
el JAR ni modifiques otros repositorios. Documentá fichas planned sin .robot,
con datos, pasos, esperado, recuperación, evidencia y lo aún no comprobado.
Actualizá grupos/cobertura sin marcar casos como implementados o aprobados.
Para Restobar distinguí cuenta, ocupación de mesa y estado de cocina;
impresión por comensal no acredita cobros separados. No hagas commit/push.
```
