# Complemento de escenarios críticos de XGestión

## Objetivo y alcance

Completar los nueve circuitos identificados en la revisión solicitada por el
usuario. Esta entrega amplía el catálogo documental y sus grupos; no implementa
Robot, fixtures, cambios del ERP ni habilita servicios o pruebas reales.

| Lote | IDs nuevos | Cantidad | Mapa |
| --- | --- | ---: | --- |
| Cobros combinados, presupuestos y devoluciones/anulaciones | COB-001..008, PRE-001..006, DEV-001..006 | 20 | cobros-documentos.md |
| Facturación y pagos externos | FEL-001..006, PEX-001..006 | 12 | facturacion-pagos-externos.md |
| Interrupciones, concurrencia y actualización | REC-001..004, CON-001..004, ACT-001..004 | 12 | continuidad-operativa.md |
| Descuentos, impuestos y fidelización | BEN-001..006 | 6 | beneficios-impuestos.md |

Son 50 fichas `planned`: 293 documentadas, 91 implementadas y 202 pendientes.
Los grupos y variantes no agregan IDs. PRM-077/078 continúan pendientes del
paquete de varias empresas/sucursales. Ningún resultado real se infiere.

## Secuencia de implementación

1. Contrastar fuente y fichas existentes; enlazar LPR-022, FIN-003/004/009,
   RES y BKP cuando cubran parte del recorrido, sin reemplazar sus IDs.
2. Crear fichas por lote con datos, perfil, pasos/resultados, recuperación,
   evidencia y referencias al commit fuente inspeccionado.
3. Registrar grupos, integrar README/roadmap/matriz y dependencias de datos.
4. Regenerar el Excel, JSON y manifiesto desde las fuentes; revisar conteos,
   enlaces, filtros y selección exclusiva de los 91 casos implementados.

## Contratos y límites

- Las reglas no verificadas se distinguen de invariantes de integridad;
  una variante con contrato pendiente no se ejecuta ni se considera aprobada.
- Cobro manual, integrado y fiscal son perfiles distintos. Homologación,
  concurrencia y sincronización requieren laboratorios y aislamiento propios;
  esta documentación no autoriza conectar la VM offline ni quitar controles.
- Interrumpir después de confirmar exige consultar el estado antes de
  reintentar. Restaurar una VM no revierte por sí mismo un cobro externo.
- Una actualización se ensaya sobre una copia descartable, con versiones y
  baseline identificados. No se presupone downgrade ni rollback automático.
- No extender el permiso de doble clic del editor de Venta a otros controles.
- Cada ficha mantiene `status: planned`, sin `test`, `seed` ni evidencia ficticia.
- Fuente ERP inspeccionada para este lote: `daa002d597d0fa7380ace204d3727085c52d1415`.
  Las referencias de fichas anteriores conservan sus commits históricos.

## Validación y aceptación

Usar los controles existentes: `.venv\Scripts\python.exe -m ruff check .`,
`.venv\Scripts\python.exe -m robocop check products`,
`.venv\Scripts\python.exe -m pytest`, `qa.cmd check`, `qa.cmd coverage`,
`qa.cmd coverage --check` y `qa.cmd run --product xgestion --group regression --dry-run`.
Actualizar únicamente las expectativas del catálogo afectadas. No agregar
tests que repliquen la prosa. Comprobar 293 IDs únicos, 202 pendientes sin
selección ejecutable, enlaces y legibilidad del Excel. Sin commit/push.
