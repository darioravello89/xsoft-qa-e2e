---
{"id":"XG-RES-017","title":"Respetar la receta vigente al validar exclusiones y compatibilidad","product":"xgestion","module":"restobar","tags":["xgestion","regression","restobar","restobar-recetas","restobar-opciones"],"status":"planned"}
---

# XG-RES-017 — Respetar la receta vigente al validar exclusiones y compatibilidad

## Objetivo

Respetar la receta vigente al validar exclusiones y compatibilidad, desde la perspectiva del mozo, cajero o supervisor que opera el pedido.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P1; etapa 5.**
Referencia de planificación: **Recetas**. Ver [mapa de Restobar](../../docs/restobar.md).
No tiene suite Robot, seed automático ni validación real del JAR. Los resultados siguientes son criterios esperados, no resultados obtenidos.

## Precondiciones y datos

- Paquete QA sintético, Windows exclusivo y escritorio visible. La preparación de carta, mesas, ingredientes, permisos y perfiles de este caso está **pendiente**; `catalogo-comercial-v1` no certifica estos datos.
- Perfil local por defecto: ARS, comprobante interno no fiscal, impuestos y cubiertos $0 salvo indicación, sin ofertas, listas ni beneficios adicionales. Las integraciones se habilitan solo en el laboratorio indicado.
- Perfiles separados del mismo plato: A receta actual queso 0,05 kg; B solo receta legacy 0,03 kg; C ambas (actual 0,05, legacy 0,20); D ninguna. Opción quitar queso 0,04 kg.
- Paquetes sintéticos por modelo de receta pendientes; ninguna modificación directa de DB durante UI.
- Preparar y registrar antes de ejecutar los IDs propios de empresa, sucursal, puesto, cuenta, mesa y productos. Mantener una operación de control ajena al caso para verificar aislamiento.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| En A seleccionar la exclusión de 0,04 kg. | La opción es válida respecto de 0,05 kg. |
| En B intentar la misma exclusión. | Se rechaza porque la receta legacy disponible contiene solo 0,03 kg. |
| En C repetir y luego intentar una exclusión de 0,06 kg. | 0,04 se permite y 0,06 se rechaza; no se suman las dos recetas ni se usa el límite legacy mayor. |
| En D intentar la exclusión y luego cancelar. | Se rechaza la exclusión sin receta y el pedido original queda intacto. |

## Variantes y límites

Recetas inactivas y otro ingrediente de control. La compatibilidad del límite no demuestra que los dos modelos compartan consumo, alta o anulación; esos circuitos necesitan perfil específico.

## Dependencias para automatizar

Preparar el baseline privado reproducible y sus datos, declarar el perfil, calibrar acciones accesibles sobre el SHA256 del JAR y construir comprobaciones por identidad. Utilizar atajos/acciones accesibles verificados; no tomar una posición de pantalla como identidad. Si el control o laboratorio no está disponible, mantener el caso pendiente y explicar el bloqueo.

## Evidencia y límites

Conservar UI y valores esperados/observados de cada transición. En una cuenta abierta distinguir lo guardado de lo cobrado: salir de la pantalla no es abandonar la venta. Registrar por separado **estado de cuenta, ocupación de mesa y estado de cocina** cuando apliquen.

Comparar operaciones, consumos, opciones, importes y efectos de stock/pagos por identidad y deltas según el caso, con lecturas autorizadas y saneadas. Las salidas de cocina, fiscalización y dispositivos requieren evidencia del extremo receptor; un log o test unitario no la sustituye. Registrar versión/SHA256 del JAR, commit del harness, paquete, perfil, IDs y reporte privado.

## Recuperación

Ante una discrepancia conservar primero la evidencia y cancelar o retomar por la interfaz según los pasos del caso. No borrar ni corregir registros comerciales para obtener un resultado aprobado. Restaurar el baseline QA antes de otra variante; para un cierre de resultado ambiguo conciliar la operación antes de reintentar, evitando cobrar o consumir ingredientes dos veces.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`. Rutas relativas a XGestion2:

- `src/Utilidades/Pickers/FormProductoOpcionesPicker.java`
- `src/ModuloRestobar/Entidades/PlatoReceta.java`
- `src/ModuloProductos/Entidades/ProductoHijo.java`

La lectura de fuente/tests orienta el riesgo y el criterio; no acredita la ejecución del artefacto. INFO resume, DEBUG describe acciones de negocio y TRACE añade diagnóstico saneado. Un fallo conserva paso, esperado, observado, categoría y evidencia; causa no determinada si falta prueba causal. No registrar credenciales, filas completas ni configuración privada.

