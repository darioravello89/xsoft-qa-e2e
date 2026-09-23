# Automatización de las promociones pendientes

## Objetivo

Implementar los recorridos PRM-008..079 desde las fichas aprobadas, conservando
IDs y diferenciando automatización técnica de validación real. Los cambios locales
del backlog 006 forman parte del punto de partida de esta ampliación.

## Diseño y orden de trabajo

1. Datos públicos por recorrido y variante: artículos/categorías/ofertas exclusivos,
   acciones de usuario y expectativas fijas por renglón, sin copiar el calculador ERP.
2. Extensión del seed por las tablas comerciales verificadas, más tres medios manuales QA en `_pagos`, conservando controles de identidad, aislamiento,
   esquema y transacción. La preparación escribe; los recorridos solo usan UI y
   oráculos de lectura. Nunca modificar datos comerciales desde los keywords.
3. Ejecutor de recorridos: varias líneas, cantidad por teclado, quitar líneas,
   cancelar/retomar, confirmar y contrastar persistencia por identidad y deltas.
4. Fórmulas/alcances PRM-008..038, agrupadas PRM-039..059 y combos PRM-060..064.
   Los perfiles de agrupación ON/OFF usan conjuntos distintos preparados de antemano.
5. Condiciones PRM-065..079, agregando contratos calibrados solo cuando el comportamiento
   y los datos estén respaldados por fuente. Varias empresas/sucursales requieren
   un paquete QA de esos contextos. El usuario confirmó que no existe: PRM-077/078 permanecen pendientes.
6. Actualizar fichas implementadas junto con Robot, docs y mapa. Mantener `planned`
   las fichas cuyo recorrido completo no esté implementado; nunca usar SKIP/PASS como
   sustituto de un caso faltante o de un requisito de laboratorio.

## Estructura

`products/xgestion/offer_journeys/` encapsula datos de casos, contrato, biblioteca
y oráculos. El seed reutiliza sus datos públicos, sin depender de bibliotecas UI.
Las suites Robot conservan IDs, grupos y diagnósticos INFO/DEBUG/TRACE.

Cada acción de edición compara todas las líneas y el total. Cancelar contrasta
las cinco tablas comerciales y existencias de todos los productos. Confirmar exige
una única venta, líneas/beneficios correctos, stock y pago atribuibles a la operación.
Los resultados esperados se definen antes de ejecutar y nunca se toman de la UI/DB.

## Límites y evidencias

- Fuente ERP: commit inspeccionado y documentado en cada lote; JAR y selectores
  requieren calibración privada para su SHA256, como el contrato existente.
- El paquete actual no se presume válido para medios, permisos o contextos nuevos.
- No tocar ERP, servicios externos, fiscalización, impresión ni aislamiento.
- No crear worktrees, no publicar ni subir credenciales, reportes o paquetes privados.
- Los guards existentes se mantienen; si un esquema difiere, corregir el paquete
  o el contrato respaldado por evidencia, sin relajar comprobaciones para aprobar.

## Verificaciones

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m robocop check products
.\.venv\Scripts\python.exe -m pytest
.\qa.cmd check
.\qa.cmd coverage
.\qa.cmd coverage --check
.\qa.cmd run --product xgestion --group regression --dry-run
```

Tests del framework: discrepancias de línea y total, duplicados, cancelación,
ausencia de evidencia, formato decimal, datos/contratos incompletos y seed aislado.
Cada incremento debe pasar sus controles antes de ampliar el siguiente. El informe
final separará casos implementados, pendientes concretos y ejecución real no realizada.
