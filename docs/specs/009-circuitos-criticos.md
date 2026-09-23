# Roadmap de saldos, caja e integridad operativa

## Objetivo

Documentar los circuitos críticos solicitados desde la visión de QA: cuentas
corrientes de clientes y proveedores, cuotas, Libro Diario, caja, anulaciones,
consultas y conciliación. Incluir inventario y recuperación de respaldos.
Esta entrega es planificación: no implementa Robot, seeds ni cambios del ERP.

## Alcance y secuencia

| Lote documental | Fichas nuevas | Entregable |
| --- | --- | --- |
| Clientes, proveedores y cuotas | CCC-001..010, CCP-001..008, CUO-001..006 | cuentas-corrientes.md |
| Libro Diario y caja | LDI-001..008, CAJ-001..010 | libro-diario-caja.md |
| Recorridos entre circuitos | FIN-001..010 | circuitos-criticos.md |
| Inventario y respaldos | INV-001..004, BKP-001..002 | inventario-respaldos.md |

Son 58 fichas `planned`: el catálogo pasa de 185 a 243 documentadas, mantiene
91 implementadas y pasa de 94 a 152 pendientes. Las variantes y los grupos
no son escenarios adicionales. Los mapas REM/RES/LPR existentes se enlazan.

1. Fijar contratos públicos y grupos; conservar todos los IDs existentes.
2. Escribir fichas con datos, pasos/resultados, variantes, recuperación,
   dependencias y trazabilidad; revisar entre autores las reglas de dinero.
3. Integrar roadmap, README, matriz y requisitos de fixtures.
4. Regenerar Excel/JSON/manifiesto y comprobar que ningún pendiente se ejecute.

## Reglas de aceptación

- Origen de deuda, cobro, caja y movimiento financiero se verifican por separado.
  Libro Diario no supone partida doble ni igualdad de filas con caja.
- No generalizar efectos de un cobro manual a cuotas o a pagos de proveedores.
- Toda expectativa ambigua se identifica como pendiente de definición antes
  de automatizar. Un riesgo encontrado en fuente no es un defecto reproducido.
- Ninguna ficha declara `test`/`seed` ni aprobación real; perfiles, controles,
  fallos controlados y paquetes de varios contextos siguen pendientes.
- Backups: exportación/importación y restauración exacta son capacidades
  distintas. No usar una importación por upserts como prueba de recuperación.
- Fuente ERP: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; anexos por ficha.
- INFO resume; DEBUG muestra pasos; TRACE conserva diagnóstico saneado.
  Los fallos siempre requieren paso, esperado, observado y evidencia.

## Validación

Revisar scripts y ejecutar Ruff, Robocop, pytest, `qa.cmd check`,
`qa.cmd coverage --check` y dry-run de regresión (91 IDs únicos).
Comprobar filtros/estados del Excel y enlaces públicos. No ejecutar ERP,
MySQL real, importaciones, servicios ni dispositivos. No commit/push.
