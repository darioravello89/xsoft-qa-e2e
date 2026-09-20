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
Leé AGENTS.md y los casos del grupo ventas de XGestion. Listá los escenarios
y sus efectos. Ejecutá doctor y, si cumple los requisitos del entorno
aislado, corré qa.cmd run --product xgestion --group ventas. Al terminar,
indicá casos ejecutados, resultado y ubicación del reporte local sin
credenciales ni datos sensibles. No publiques artefactos ni hagas commits.
```

## Investigar un fallo

```text
Leé AGENTS.md. Necesito diagnosticar el fallo del caso [ID]. Usá el último
reporte local y su Markdown. Separá problemas de entorno, selectores,
datos y comportamiento del producto. No imprimas secretos. No cambies el
resultado esperado ni desactives aserciones para conseguir un PASS.
Entregá causa comprobada, evidencia saneada y corrección propuesta.
```

## Agregar cobertura

```text
Leé AGENTS.md, docs/nuevas-features.md y templates/scenario.md. Incorporá
pruebas para [funcionalidad y criterio de aceptación] dentro de [producto].
Reutilizá recursos existentes. Actualizá Markdown, tags, tests y datos del
paquete conjuntamente. No inventes selectores, credenciales ni esquemas.
Ejecutá las validaciones técnicas y declará qué falta para la prueba real.
No modifiques el producto ni publiques cambios sin un pedido específico.
```
