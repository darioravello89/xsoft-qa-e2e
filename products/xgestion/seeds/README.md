# Catálogo comercial reproducible

La guía para QA y el inventario están en [Datos fijos](../docs/seed.md). Este directorio declara datos sintéticos públicos; no contiene un dump, credenciales ni resultados E2E.

| Archivo | Responsabilidad |
| --- | --- |
| [model.py](model.py) | `SeedContext`, `SeedTable`, nombre/versionado y mezcla de tablas sin claves duplicadas. |
| [products.py](products.py) | 25 productos, catálogos, variantes, composición/opciones y stock inicial fijo; requisitos de unidades, monedas e IVA. |
| [pricing.py](pricing.py) | 23 productos comerciales, 19 ofertas, 5 listas, 6 detalles y 26 ejemplos `manual_pending`. |
| [engine.py](engine.py) | Vista previa; controles de esquema/contexto/propiedad; upserts parametrizados y verificación. |
| [isolation.py](isolation.py) | Rechazo de ofertas, códigos alternativos y relaciones ajenas que contaminarían los escenarios. |
| [triggers.py](triggers.py) | Certificación de los automatismos conocidos de sincronización antes de escribir; sin deshabilitarlos. |
| [command.py](command.py) | Ciclo autorizado del comando: perfil privado, exclusión mutua, aislamiento, restauración y reporte. |

La fuente de reglas es XGestion2 `f34238183d494259bed1279dd7d9aac0ce16a3ae`; su correspondencia con el JAR debe verificarse por separado. `DATABASE_SCHEMA.sql` es insuficiente sin las migraciones del verificador: el seed bloquea ante incompatibilidad y no modifica el esquema ERP.

## Contrato para ampliar

1. Reservar identidad `QA-SEED-*` e IDs libres dentro del namespace del catálogo; no reutilizar 90001 ni datos del fixture actual.
2. Declarar `SeedTable(name, keys, identity, rows, natural_keys)` con la PK real, identidad estable de propiedad y claves naturales que deban ser únicas aunque MySQL no tenga ese índice.
3. Usar valores exactos, sin `float`; precios como texto decimal o `Decimal`, fechas desde `SeedContext.reference_date`. No usar el reloj dentro de los constructores ni leer configuración privada.
4. Reutilizar `article(...)`, `stock_row(...)` y las constantes de claves al añadir productos comerciales. No incluir `artStock` para fabricar un saldo. Los movimientos nuevos tienen cantidad fija, PK estable y fecha explícita.
5. Acotar toda oferta/lista al catálogo propio; una categoría compartida puede contaminar otros casos. No asignar listas por defecto ni sobrescribir catálogos globales; declarar nuevos requisitos y comprobarlos.
6. Añadir tests de invariantes, colisiones o persistencia pertinentes. Los ejemplos de montos son expectativas a validar con el perfil, no un reemplazo del calculador del ERP ni evidencia de GUI.
7. Actualizar inventario, requisitos, trazabilidad y los escenarios afectados. Si cambia el contrato de propiedad o identidad, evaluar una nueva versión de catálogo en lugar de apropiarse de filas existentes.

## Revisión y ejecución

```powershell
.\qa.cmd seed --dry-run --export --reference-date 2026-09-21
.\qa.cmd seed --apply
.\qa.cmd run --product xgestion --group regression --seed catalogo-comercial-v1
```

La primera línea es revisión sin conexión. Las otras dos restauran la base privada QA y requieren su paquete y aislamiento; no ejecutarlas sobre servicios compartidos. El SQL exportado con `%s` conserva parámetros separados y comentarios públicos de ejemplo: no es un instalador SQL independiente. Usar el runner para aplicar y conservar el reporte local.

## Pruebas de integración del mantenedor

Los tests ordinarios no requieren MySQL. Para probar upserts, colisiones, rollback y triggers sobre MySQL 5.7 Windows x64, establecer `XSOFT_SEED_MYSQL_BIN` con la ruta explícita de `mysqld.exe` y ejecutar `python -m pytest tests/test_seed_*mysql*.py`. En PowerShell, usar `python -m pytest -q` para incluir todas las pruebas sin depender de la expansión del comodín. El harness inicia una instancia efímera con `--no-defaults`, directorio nuevo en `work/`, puerto loopback libre distinto de 13317 y credenciales aleatorias. No usa la configuración, datos ni servicio instalado. Cierra solo el proceso que creó y conserva evidencia local privada en `work/seed-mysql-*`.

El [DDL sintético de referencia](../../../tests/fixtures/xgestion_seed_schema.sql) incluye únicamente estructura inspeccionada y migraciones identificadas. No reemplaza el baseline privado. Su única excepción exacta en `.gitignore` no habilita subir dumps.
