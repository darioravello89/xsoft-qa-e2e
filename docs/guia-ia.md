# Trabajar con la IA local

Abrí este repositorio en la herramienta de IA que use tu equipo. Pedile que lea `AGENTS.md` antes de operar. Si XGestion corre en una VM sin red, podés conversar con la IA desde el host y copiar solamente comandos y diagnósticos saneados hacia/desde la VM.

## Ejecutar casos existentes

1. Pedí que revise requisitos con `qa.cmd doctor --product xgestion` y consulte `qa.cmd list --product xgestion`.
2. Elegí un grupo o un ID. La IA debe leer el escenario Markdown para explicar qué comprueba y qué datos modifica.
3. Ejecutá con `qa.cmd run`, en la máquina aislada. Dejá el escritorio disponible y no hagas otra tarea dentro de la VM.
4. Abrí `qa.cmd report --latest`. La IA puede ayudarte a interpretar el resultado con mensajes saneados; no necesita tus contraseñas.

No es necesario que entiendas Python o Robot para ejecutar un caso. Para crear pruebas nuevas, la IA sí debe implementar las acciones y aserciones y verificar el resultado sobre el producto; escribir un Markdown no automatiza por sí solo una prueba.

## Qué puede compartir QA

Compartí ID del caso, versión de XGestion, etapa que falló y mensaje sin datos sensibles. No pegues el contenido de `.env.local`, `config.properties`, licencias, dumps o tokens. Los reportes y árboles de accesibilidad pueden contener nombres de usuarios y artículos; mantenelos en el entorno privado.

## Cómo informar un resultado

Usá una frase como: «XG-VEN-001, build 2.02.189-lts, paquete QA identificado por su manifest: FAIL al verificar stock; reporte local disponible». Si solo se ejecutó `check` o `dry-run`, indicá «validación técnica, E2E real pendiente».

Ante un bloqueo no pidas a la IA que quite el control. Primero debe identificar si falta el paquete, la licencia offline, la calibración, el escritorio o el aislamiento de red. Los pasos habituales están en [solución de problemas](solucion-de-problemas.md).
