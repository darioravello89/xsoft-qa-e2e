# Evidencia de atajos — 3f8648035

Fecha de preparación: **2026-09-24**.

## Artefacto exacto construido

| Dato | Valor |
| --- | --- |
| Fuente | `3f8648035380535f639da140d208fd299a096593` |
| Rama de referencia | `release/189-lts` |
| Método | `git archive` del commit; snapshot privado, sin worktree ni clases previas |
| JAR local | `C:\Users\dario\Desktop\Personal\xsoft-qa-e2e\.local\artifacts\3f8648035\dist\XGestion-3f8648035.jar` |
| SHA-256 JAR | `64306c06595f0c1600098e0ccaab4996baf62506788a5158dce4b53de3f859cf` |
| Tamaño | 175490431 bytes |
| SHA-256 del archivo de fuentes | `ea0efbcbeb9980c27f66863197d874dc45ff5c72dc9179fd3fb50d4aa2a1ec75` |
| Compilador | Temurin JDK `21.0.11+10`; source/target Java 17 del proyecto |
| Ant | `1.10.17` |
| Entrada | `ModuloPrincipal.Vistas.AppXGestion` |
| Build | `jar`: BUILD SUCCESSFUL, 3 min 39 s; salidas privadas propias |
| Verificación técnica | Verificador FAT del build: payload, classloading, balanza/jSerialComm; presentes clases de los 13 listados y los 2 helpers de teclado/filtros |
| Manifest de trazabilidad privado | `.local/artifacts/3f8648035/artifact.json` |
| Log privado de compilación | `.local/artifacts/3f8648035/build.log` |
| JAB / perfil / paquete | Sin ejecución; todavía no disponibles |

El JAR anterior de `XGestion2/dist` no se utilizó ni se reemplazó. El checkout
ERP estaba limpio al iniciar y tras la compilación. En la revisión final
aparecieron cambios posteriores en fuente; no se tocaron ni se incorporaron
al artefacto archivado de este commit. El snapshot, JAR, log y manifest están ignorados por Git.
Una nueva compilación puede generar un hash distinto: recalibrar contra el
artefacto que efectivamente se importe al paquete, sin reutilizar este hash.

## Estado real por pantalla

**B1:** no hay PC/VM exclusiva ni paquete privado; confirmado por el usuario.
`qa.cmd doctor --product xgestion` informó «Falta el paquete QA privado».
No se inició el JAR contra una instalación cotidiana ni se omitió el guard.

| Caso | Pantalla | Escenario | Automatización completa | Ejecución JAB | Defecto reproducido |
| --- | --- | --- | --- | --- | --- |
| XG-KEY-001 | Cuentas corrientes de clientes | Documentado | Pendiente | NO EJECUTADO — B1 | No determinado |
| XG-KEY-002 | Cuenta corriente de cliente | Documentado | Pendiente | NO EJECUTADO — B1 | No determinado |
| XG-KEY-003 | Cuentas corrientes de proveedores | Documentado | Pendiente | NO EJECUTADO — B1 | No determinado |
| XG-KEY-004 | Cuenta corriente de proveedor | Documentado | Pendiente | NO EJECUTADO — B1 | No determinado |
| XG-KEY-005 | Clientes | Documentado | Pendiente | NO EJECUTADO — B1 | No determinado |
| XG-KEY-006 | Productos | Documentado | Pendiente | NO EJECUTADO — B1 | No determinado |
| XG-KEY-007 | Mesas | Documentado | Pendiente | NO EJECUTADO — B1 | No determinado |
| XG-KEY-008 | Usuarios | Documentado | Pendiente | NO EJECUTADO — B1 | No determinado |
| XG-KEY-009 | Turnos | Documentado | Pendiente | NO EJECUTADO — B1 | No determinado |
| XG-KEY-010 | Compras | Documentado | Pendiente | NO EJECUTADO — B1 | No determinado |
| XG-KEY-011 | Proveedores | Documentado | Pendiente | NO EJECUTADO — B1 | No determinado |
| XG-KEY-012 | Categorías | Documentado | Pendiente | NO EJECUTADO — B1 | No determinado |
| XG-KEY-013 | Subcategorías | Documentado | Pendiente | NO EJECUTADO — B1 | No determinado |

## Hallazgos estáticos que requieren comprobarse en el JAR

No son defectos E2E confirmados ni autorizan cambiar el ERP en esta tarea.

| Pendiente | Pantallas | Evidencia y consecuencia |
| --- | --- | --- |
| Calibrar buscadores | Trece | Sólo Productos nombra explícitamente «Buscar productos» en el bloque de fuente inspeccionado; algunos usan etiqueta/tooltip. Hay que leer el árbol real, comprobar unicidad y foco. No inventar nombres para los demás. |
| Cambio de orden | Trece | Productos tiene Ordenar por/Dirección. No se encontró instalación de RowSorter en los otros doce listados ni en MyJTable. No afirmar soporte de click en encabezado ni fabricar orden desde el test. N09 sigue pendiente de mecanismo verificable. |
| Una recarga lógica | Ocho con filtros | DialogoFiltrosCrud suspende listeners al copiar valores y llama alAplicar; inspección estática no mide cuántas recargas ocurren. Falta señal observable correlacionada; tabla estable y eventos por celda no prueban unicidad. |
| X del modal | Ocho con filtros | JDialog usa DISPOSE_ON_CLOSE; no hay botón X Swing explícito. Falta comprobar acción JAB del cierre nativo. No marcar X probado por usar Escape/Alt+F4. |
| Leyenda gris junto al buscador | Trece | AccessibleName «Ayuda de teclado»; texto completo en descripción, color Label.disabledForeground o DARK_GRAY en fuente. Falta observar visibilidad/color/posición/DPI en el JAR. |
| Abrir cuenta de cliente | KEY-001 / ACC-010 | El commit incorpora Enter y conversión vista→modelo. La carencia de atajo en fuente quedó resuelta; falta validar por JAB antes de habilitar FIN-012. Doble clic sigue sin autorización. |

## Controles del repositorio de esta entrega

- Ruff y Robocop: sin errores.
- Pytest final: **866 passed, 38 skipped**. Los omitidos corresponden a
  precondiciones de tests de integración/entorno; no son validaciones del ERP.
- Catálogo: **315 fichas, 99 implementadas, 216 pendientes, 0 manuales**.
- Los nuevos grupos contienen 13 y 8 pendientes; los tests verifican que no
  sean seleccionados como ejecutables ni se sumen a los 99 de regresión.
- Dry-run de regresión: **99 VALIDADO EN SECO**. Ningún KEY ejecutado.
- Excel generado y `coverage --check` vigente; valores/estados y vistas de
  Resumen, Grupos y nuevas fichas inspeccionados. El auxiliar de inspección
  generó las imágenes y no encontró errores de fórmula; terminó después con
  un error nativo del runtime. Exportación y verificación del mapa finalizaron
  correctamente. No se ejecutó Microsoft Excel.
- 256 enlaces locales y estructura de 13 filas de accesibilidad verificados.

Estos resultados no cambian el estado NO EJECUTADO de los trece recorridos.

## Formato para incorporar una ejecución posterior

Por pantalla y variante N/F/S registrar:

```text
Caso / variante:
Fecha / operador QA:
JAR: ruta y SHA256 calculado en la VM
Paquete / perfil / calibración / versión JAB:
Resolución / DPI / rol y permisos:
Datos QA e identidad esperada:
Pasos mínimos reproducibles:
Esperado:
Observado (incluye identidad abierta, foco y selección):
Estado: OK / FALLÓ / BLOQUEADO / NO EJECUTADO
Repeticiones desde baseline:
Reporte local / captura saneada / eventos:
Defecto y causa: confirmada o no determinada
Pendientes restantes de la pantalla:
```

No guardar credenciales, nombres de personas reales, árboles completos o filas
de DB en este documento público. Adjuntar evidencia sensible sólo al reporte
local privado. Ninguna ficha aprueba con variantes obligatorias sin evidencia.
