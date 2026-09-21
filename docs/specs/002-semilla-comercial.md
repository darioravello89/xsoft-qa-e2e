# Seed comercial de XGestión

## Objetivo y alcance

Preparar una batería fija de productos, variantes, stock, listas y ofertas para que QA y su IA usen los mismos códigos y datos en cada escenario. Es una ampliación solicitada sobre el roadmap: crea datos y sus upserts, no convierte los casos planificados en E2E implementados.

El repositorio dueño es `xsoft-qa-e2e`. El contrato se contrasta con DDL, migraciones, DAO y tests de XGestion2 `release/189-lts`, commit `f34238183d494259bed1279dd7d9aac0ce16a3ae`. El DDL histórico por sí solo no alcanza: faltan columnas y algunas claves fueron migradas.

## Decisiones y límites

- Catálogo público `catalogo-comercial-v1`, códigos `QA-SEED-*` e IDs reservados. Los productos actuales de `fixtures.json` permanecen intactos.
- Contexto empresa/sucursal/computadora/usuario leído del paquete privado; fecha de referencia explícita en el resultado. Las fechas de stock y vigencia se generan de forma determinista para esa referencia.
- Upserts parametrizados por claves reales; comprobar también todos los índices únicos y el código de producto, que no tiene restricción UNIQUE. Ante una colisión ajena se rechaza el lote completo.
- Tablas transaccionales, esquema compatible y catálogos globales verificados antes de escribir. Aplicar y verificar en una transacción; omitir filas idénticas para no disparar actualizaciones ni colas por una repetición.
- Stock inicial como movimientos identificables de cantidad fija, nunca suma acumulativa. Reaplicar no limpia ventas previas: el flujo de QA restaura el baseline antes del seed.
- Ofertas y listas acotadas a productos/categorías propios. No cambiar asignaciones de empresa, clientes, sucursal ni turnos. La selección y configuración de cada variante se documenta.
- No crear licencias, usuarios, credenciales ni modificar el esquema del ERP. No conectar servicios instalados ni bases compartidas. Solo la instancia privada iniciada y verificada por el runner puede recibir el seed.

## Estructura y comandos

`products/xgestion/seeds/` contiene el modelo, datos de productos, precios/ofertas, motor de upserts y comandos. Tests bajo `tests/test_seed_*.py`; documentación de uso y matriz bajo el producto.

- `qa.cmd seed --product xgestion --dry-run`: describir/generar el plan SQL público sin credenciales, paquete ni conexión. No acredita compatibilidad con una base real.
- `qa.cmd seed --product xgestion --apply`: restaurar el baseline exclusivamente en la instancia privada, aplicar y verificar el catálogo.
- `qa.cmd run --product xgestion --group ventas --seed catalogo-comercial-v1`: aplicar el catálogo después de restaurar, antes de iniciar el JAR. Sin `--seed`, conservar el comportamiento existente.
- `python -m ruff check .`, `python -m robocop check products`, `python -m pytest -q`, `qa.cmd check` y regresión en seco.

Estilo: datos explícitos con importes decimales textuales, nombres de tablas/columnas declarados en código, valores enviados por parámetros. El SQL exportado es una vista para revisión; se aplica mediante el comando protegido.

## Secuencia y aceptación

1. Contrastar esquema y reglas; definir catálogo y expectativas por variante.
2. Probar validación de contexto, colisiones, esquema incompatible y segunda aplicación sin duplicación; implementar el motor.
3. Conectar preview/aplicación y ejecución opt-in sin alterar los siete casos actuales.
4. Verificar upserts sobre MySQL efímero con datos sintéticos y esquema de referencia; revisar seguridad y documentación; correr controles completos.

La aceptación técnica exige estabilidad de IDs/valores al repetir con el mismo contexto y fecha, rollback ante error, ausencia de escrituras a registros ajenos y métricas inserted/updated/unchanged verificadas. Validar SQL con una base sintética no acredita comportamiento del JAR. La aceptación funcional conserva sus requisitos de paquete, perfil y calibración del laboratorio.
