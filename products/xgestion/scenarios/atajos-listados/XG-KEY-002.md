---
{"id": "XG-KEY-002", "title": "Atajos en cuenta corriente de cliente", "product": "xgestion", "module": "atajos-listados", "priority": "P0", "tags": ["xgestion", "regression", "atajos-listados", "lectura", "p0", "filtros-listados"], "status": "planned"}
---

# XG-KEY-002 — Atajos en cuenta corriente de cliente

## Objetivo y estado

Operar **Cuenta corriente de cliente** por teclado conservando identidad y restricciones.
**Documentado; automatización pendiente; ejecución real no realizada.**
No hay archivo Robot ni PASS por dry-run. Ver [evidencia del artefacto](../../docs/evidencia-atajos-3f8648035.md).

## Perfil y datos

PC/VM Windows QA exclusiva, offline y escritorio visible. JAR exacto del commit
`3f8648035380535f639da140d208fd299a096593`, paquete privado con roles y datos dedicados,
calibración JAB de nombres/roles/estados. A/B/C inequívocos; búsquedas de cero,
una y varias filas, filtros iniciales A y borrador B preparados antes de probar.
Identidad esperada: **Cliente, nota única, fecha, importe y moneda del movimiento**. No suponer accesible el ID de columna oculta.

## Pasos y resultados

| Paso | Acción | Resultado esperado |
| ---: | --- | --- |
| 1 | Abrir Cuenta corriente de cliente; desde otro control usar Ctrl+B. | Foco real en buscador y leyenda gris de atajos visible junto a él. |
| 2 | Buscar conjunto vacío, B solo y A/B/C; probar ↑/↓ desde buscador. | Cero filas: sin selección/apertura; con filas: selección y foco reales en tabla. |
| 3 | Recorrer tabla con ↑/↓, incluidos ambos extremos. | Selección única y paso circular; una fila permanece seleccionada. |
| 4 | Enter en primera, intermedia y última fila; comprobar destino y cancelar sin guardar. | Editor del pago/deuda manual correcto; movimiento de venta rechazado. Contrastar cliente, nota única, fecha, importe y moneda del movimiento. |
| 5 | Buscar conservando/excluyendo B; cambiar orden por mecanismo de UI y volver a abrir. | Identidad conservada si sigue visible; selección limpia si desaparece; nunca abrir por índice viejo. Orden inaccesible bloquea su variante. |
| 6 | Enter en buscador con cero, uno y varios resultados. | Acción de búsqueda original conservada; Compras abre automáticamente si sólo hay una fila. |
| 7 | Completar controles de filtros/ausencia indicados abajo; regresar al listado. | Valores aplicados/cancelados correctos, navegación recuperada y ninguna escritura por abrir/cancelar. |

## Variantes obligatorias

- Ejecutar **N01–N12** de la [matriz común](../../docs/atajos-listados.md#variantes-comunes-obligatorias-n01n12); cada variante necesita resultado propio.
- F01–F09, usando: **Desde; Hasta**. F08 sólo para fechas/cascada cuando existen.
- Probar pago manual, deuda manual y movimiento originado por venta. Este último debe avisar «No se puede editar un registro originado por una venta.» y no abrir editor. Con filtros sin aplicar revisar el histórico completo; al aplicar fechas incluir límites y excluir anteriores/posteriores. Cancelar editor no cambia deuda ni Libro Diario.
- Roles autorizado/restringido según perfil declarado; restricciones específicas
  del registro siguen vigentes. No inferir prohibición de apertura si el permiso
  sólo limita Guardar/Eliminar; observar esos estados sin activarlos.

## Evidencia, recuperación y límites

Registrar por variante: artefacto/hash, paquete, perfil, rol, fecha, datos QA,
paso/esperado/observado, foco/selección, campos de identidad del destino y
capturas saneadas. No incluir contraseñas ni filas completas de DB.
Cerrar sin guardar; ante un desvío restaurar baseline con qa.cmd antes de repetir.
Sin lectura completa, X accesible, mecanismo de orden o señal de recarga cuando
corresponda: **BLOQUEADO**, nunca OK. Una falla funcional reproducida es **FALLÓ**.

No se acredita color por el nombre de la leyenda, ni una recarga por ver la tabla
final, ni identidad por el título de la ventana. Los bloqueos del laboratorio
no se atribuyen como defectos del producto. Ver [matriz y procedimiento](../../docs/atajos-listados.md).

## Trazabilidad técnica

- Fuente exacta: `3f8648035380535f639da140d208fd299a096593`.
- `src/ModuloFinanzas/Vistas/FormCuentaCorrienteCliente.java`; apertura compartida de Enter/doble clic.
- `src/Utilidades/Componentes/ListadoCrudTeclado.java` y
  `src/Utilidades/Componentes/DialogoFiltrosCrud.java` (si hay filtros).
- La inspección de fuente orienta el esperado; no sustituye ejecución real JAB.
