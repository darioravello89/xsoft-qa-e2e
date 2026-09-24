---
{"id": "XG-KEY-010", "title": "Atajos en compras", "product": "xgestion", "module": "atajos-listados", "priority": "P0", "tags": ["xgestion", "regression", "atajos-listados", "lectura", "p0", "filtros-listados"], "status": "implemented", "test": "products/xgestion/suites/atajos_listados.robot"}
---

# XG-KEY-010 — Atajos en compras

## Objetivo y estado

Operar **Compras** por teclado conservando identidad y restricciones.
**Recorrido Robot implementado; ejecución real JAB no realizada.**
La [guía de automatización](../../docs/atajos-automatizacion.md) explica el paquete privado y los bloqueos. El dry-run no acredita PASS del ERP.

## Perfil y datos

PC/VM Windows QA exclusiva, offline y escritorio visible. JAR exacto del commit que se ejecutará, con SHA-256 y paquete privado de roles y datos dedicados,
calibración JAB de nombres/roles/estados. A/B/C inequívocos; búsquedas de cero,
una y varias filas, filtros iniciales A y borrador B preparados antes de probar.
Identidad esperada: **Tipo, número, proveedor, fecha y sucursal del comprobante**. No suponer accesible el ID de columna oculta.

## Pasos y resultados

| Paso | Acción | Resultado esperado |
| ---: | --- | --- |
| 1 | Abrir Compras; desde otro control usar Ctrl+B. | Foco real en buscador y leyenda gris de atajos visible junto a él. |
| 2 | Buscar conjunto vacío, B solo y A/B/C; probar ↑/↓ desde buscador. | Cero filas: sin selección/apertura; con filas: selección y foco reales en tabla. |
| 3 | Recorrer tabla con ↑/↓, incluidos ambos extremos. | Selección única y paso circular; una fila permanece seleccionada. |
| 4 | Enter en primera, intermedia y última fila; comprobar destino y cancelar sin guardar. | Remito → carga de remito; Carnicería → carga de carne; Factura y Transferencia → orden de compra. Contrastar tipo, número, proveedor, fecha y sucursal del comprobante. |
| 5 | Buscar conservando/excluyendo B; cambiar orden por mecanismo de UI y volver a abrir. | Identidad conservada si sigue visible; selección limpia si desaparece; nunca abrir por índice viejo. Orden inaccesible bloquea su variante. |
| 6 | Enter en buscador con cero, uno y varios resultados. | Acción de búsqueda original conservada; Compras abre automáticamente si sólo hay una fila. |
| 7 | Completar controles de filtros/ausencia indicados abajo; regresar al listado. | Valores aplicados/cancelados correctos, navegación recuperada y ninguna escritura por abrir/cancelar. |

## Variantes obligatorias

- Ejecutar **N01–N12** de la [matriz común](../../docs/atajos-listados.md#variantes-comunes-obligatorias-n01n12); cada variante necesita resultado propio.
- F01–F09, usando: **Sucursal; Proveedor; Estado; Desde; Hasta; Tipo de compra**. F08 sólo para fechas/cascada cuando existen.
- Repetir con Remito, Factura, Transferencia y Carnicería, en estados disponibles del paquete (borrador/recibido cuando corresponda). Enter en BUSCADOR busca y abre si queda una sola fila; con cero/varias sólo busca. Enter en TABLA abre la seleccionada. En ambas rutas verificar tipo e identidad, sin guardar, emitir, recibir o imprimir. Cancelar conserva stock, deuda y precios.
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
- `src/ModuloStocks/Vistas/FormListadoOrdenesCompras.java`; apertura compartida de Enter/doble clic.
- `src/Utilidades/Componentes/ListadoCrudTeclado.java` y
  `src/Utilidades/Componentes/DialogoFiltrosCrud.java` (si hay filtros).
- La inspección de fuente orienta el esperado; no sustituye ejecución real JAB.
