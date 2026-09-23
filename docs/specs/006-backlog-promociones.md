# Escenarios pendientes de promociones

## Objetivo y alcance

Desglosar la ampliación de promociones solicitada en fichas de usuario `planned`,
con grupos visibles y mapa Excel actualizado. Las 21 automatizaciones existentes
conservan su estado; documentar un caso no implementa Robot ni acredita el JAR.

La matriz cruza las siete fórmulas tradicionales con sus cinco alcances y trata
los combos por separado. Agrupar productos distintos aplica solamente a familia,
subfamilia y marca. Cada ficha incluye aplicación, exclusión y límites pertinentes,
sin inventar combinaciones que el ERP no permite.

## Entregables y secuencia

1. **XG-PRM-008..038:** tres umbrales por producto y siete fórmulas por cada uno de
   los otros cuatro alcances. Conservar los casos básicos PRM-001..004.
2. **XG-PRM-039..059:** siete fórmulas agrupadas por familia, subfamilia y marca;
   comprobar productos distintos, desactivar agrupación, exclusión y recálculo.
3. **XG-PRM-060..079:** cinco recorridos de combos y quince de fracciones,
   prioridad, vigencia, listas, medios de pago, aislamiento y descuentos.
4. Registrar subgrupos, índice de fórmulas/alcances, datos disponibles y faltantes;
   vincular ejemplos seed a fichas cuando coinciden exactamente. Actualizar las
   guías y regenerar JSON, XLSX y manifiesto usando el generador del repositorio.
5. Comprobar catálogo, selección de pendientes, documentación, lint, tests del
   framework, dry-run y representación del Excel. Revisión final independiente.

## Estructura y convenciones

- Fichas: `products/xgestion/scenarios/promociones/`, con el formato de
  `templates/scenario.md`, encabezado JSON y sin campo `test`.
- Índice funcional: `products/xgestion/docs/promociones-pendientes.md`.
- Nombres y grupos: `products/xgestion/groups.json`; los IDs no cambian al automatizar.
- Datos sugeridos nuevos deben indicarse como pendientes de preparar. Este lote
  no aplica upserts, modifica el seed comercial ni abre una base o aplicación.
  Las referencias entre ejemplos existentes y fichas sí se mantienen actualizadas.
- Fuente inspeccionada: XGestion2 `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`.
  Las expectativas basadas en código se contrastarán con el JAR al implementar.

Ejemplo de estado: `"status":"planned"`, `"module":"promociones"`,
`"tags":["xgestion","regression","promociones","promociones-alcances"]`.

## Verificación y criterios de aceptación

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m robocop check products
.\.venv\Scripts\python.exe -m pytest
.\qa.cmd check
.\qa.cmd list --product xgestion --groups
.\qa.cmd list --product xgestion --group promociones-alcances
.\qa.cmd coverage
.\qa.cmd coverage --check
.\qa.cmd run --product xgestion --group regression --dry-run
```

- 93 fichas: 21 implementadas y 72 pendientes; 0 validaciones reales registradas.
- Cada pendiente tiene objetivo, perfil, datos, pasos/esperados, recuperación,
  evidencia, prioridad, dependencias y referencia fuente.
- El runner sigue seleccionando únicamente los 21 implementados; una selección
  de un grupo íntegramente pendiente o de un ID nuevo informa que no es ejecutable.
- Excel, catálogo y guías muestran los mismos conteos. El mapa no expresa los
  casos documentados como porcentaje de cobertura total del ERP.
- Los datos privados, contratos de ejecución y suites implementadas quedan fuera
  de esta ampliación de documentación. La aceptación real requiere paquete y
  calibración, como los casos actuales.
