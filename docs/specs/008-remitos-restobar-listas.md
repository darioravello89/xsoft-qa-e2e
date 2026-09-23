# Ampliación del mapa: remitos, Restobar y listas de precios

## Objetivo y alcance

Desglosar los recorridos solicitados para recepción de remitos de compra,
`formTicket` (incluidas opciones y recetas) y selección/prioridad de listas.
La entrega agrega fichas `planned`, grupos visibles y documentación de datos,
dependencias y resultados. Conserva las 91 automatizaciones existentes.
Escribir una ficha no ejecuta el producto ni habilita una suite.

«Carga de remito» corresponde a `FormCargaDeRemito`, recepción de una compra.
El remito emitido al vender es otro circuito. La fuente se usa para descubrir
reglas y riesgos, con referencia XGestion2
`4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; las reglas ambiguas requieren una
decisión y evidencia del JAR antes de automatizar, sin copiar un posible error
como resultado esperado.

## Entregables y secuencia

1. Remitos: fichas `scenarios/remitos/XG-REM-###.md` y `docs/remitos.md` del producto.
   Separar borrador, confirmación/recepción, corrección, costos/listas y anulación.
2. Restobar: `scenarios/restobar/XG-RES-###.md` y `docs/restobar.md`.
   Relacionar R01–R20 con fichas estables; distinguir cuenta, mesa, cocina,
   opciones, receta actual y receta heredada. La impresión por comensal no
   acredita cobros separados.
3. Listas: `scenarios/listas-precios/XG-LPR-###.md` y `docs/listas-precios.md`.
   Cliente, sucursal, fija, turno horario, cantidades, moneda y recuperación;
   tratar Venta y Restobar por separado y referenciar PRM-071/072 sin duplicarlos.
4. Registrar grupos, actualizar roadmap/matriz/README y backlog de accesibilidad.
   Vincular ejemplos seed únicamente cuando coincidan con el recorrido.
5. Regenerar JSON/Excel/manifiesto; comprobar selección de pendientes, conteos,
   enlaces, lint, tests del framework y dry-run. Revisar el Excel visualmente.

## Formato y límites

```json
{"id":"XG-REM-001","title":"Recibir una compra","product":"xgestion","module":"remitos","tags":["remitos","compras","regression"],"status":"planned"}
```

- Cada ficha incluye objetivo de usuario, perfil, datos concretos, variantes,
  pasos/resultados, recuperación, evidencia y trazabilidad técnica separada.
- Sin `test`, sin Robot simulado y sin marcador `seed` para datos todavía no
  implementados. Los códigos sugeridos no acreditan que estén instalados.
- Las dependencias de dispositivos, canales, fiscal y varios contextos quedan
  declaradas; no se amplía la ejecución offline existente ni se usan servicios.
- Los grupos se superponen; sólo las fichas aportan IDs al conteo del catálogo.
  R01–R20 siguen siendo referencias del roadmap y no agregan casos adicionales.
- No modificar el ERP ni bases, no usar worktrees y no hacer commit/push.

## Comprobaciones

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m robocop check products
.\.venv\Scripts\python.exe -m pytest
.\qa.cmd check
.\qa.cmd list --product xgestion --groups
.\qa.cmd coverage
.\qa.cmd coverage --check
.\qa.cmd run --product xgestion --group regression --dry-run
```

Aceptación: los tres mapas y sus fichas son navegables desde el README/Excel;
todo caso nuevo aparece pendiente y no ejecutable; la regresión sigue
seleccionando 91 IDs únicos. El número de validaciones reales no aumenta.
