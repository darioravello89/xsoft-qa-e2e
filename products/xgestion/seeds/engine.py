"""Upserts acotados al catálogo público, con preflight y transacción completa."""

import hashlib
import json
from dataclasses import asdict
from datetime import date, datetime
from decimal import Decimal

from framework.errors import QAError
from products.xgestion.seeds.model import NAME, SOURCE_COMMIT, SeedContext, merge_tables

NUMERIC = {"decimal", "numeric", "tinyint", "smallint", "mediumint", "int", "bigint", "bit", "float", "double"}


def equivalent(actual, expected, kind):
    if actual is None or expected is None:
        return actual is expected
    if kind in NUMERIC:
        if isinstance(actual, bytes):
            actual = int.from_bytes(actual, "big")
        if isinstance(expected, bool):
            expected = int(expected)
        return Decimal(str(actual)) == Decimal(str(expected))
    if kind in {"datetime", "timestamp"}:
        return datetime.fromisoformat(str(actual)) == datetime.fromisoformat(str(expected))
    return str(actual) == str(expected)


def upsert_sql(table, row):
    columns = list(row)
    names = ",".join(f"`{column}`" for column in columns)
    updates = ",".join(f"`{column}`=VALUES(`{column}`)" for column in columns if column not in table.keys)
    if not updates:
        updates = f"`{table.keys[0]}`=`{table.keys[0]}`"
    return (f"INSERT INTO `{table.name}` ({names}) VALUES ({','.join('%s' for _ in columns)}) "
            f"ON DUPLICATE KEY UPDATE {updates}", tuple(row.values()))


def query(connection, sql, values=()):
    with connection.cursor() as cursor:
        cursor.execute(sql, values)
        return list(cursor.fetchall())


def schema_for(connection, table):
    info = query(connection, "SELECT ENGINE AS engine FROM information_schema.TABLES "
                 "WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME=%s", (table.name,))
    if len(info) != 1 or info[0]["engine"] != "InnoDB":
        raise QAError(f"El seed requiere la tabla transaccional InnoDB {table.name}; no modifica el esquema.")
    fields = query(connection, "SELECT COLUMN_NAME AS name, DATA_TYPE AS kind, COLUMN_DEFAULT AS default_value, "
                   "IS_NULLABLE AS nullable, EXTRA AS extra FROM information_schema.COLUMNS "
                   "WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME=%s", (table.name,))
    columns = {field["name"]: field for field in fields}
    required = {key for row in table.rows for key in row}
    missing = required - columns.keys()
    if missing:
        raise QAError(f"Esquema incompatible en {table.name}: faltan columnas {', '.join(sorted(missing))}.")
    for row in table.rows:
        if any(field["name"] not in row and field["nullable"] == "NO" and field["default_value"] is None
               and "auto_increment" not in field["extra"] and "GENERATED" not in field["extra"] for field in fields):
            raise QAError(f"Esquema incompatible: {table.name} exige campos adicionales sin valor por defecto.")
    indexes = query(connection, "SELECT INDEX_NAME AS name, COLUMN_NAME AS field, SUB_PART AS prefix_length "
                    "FROM information_schema.STATISTICS WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME=%s "
                    "AND NON_UNIQUE=0 ORDER BY INDEX_NAME, SEQ_IN_INDEX", (table.name,))
    unique = {}
    for index in indexes:
        if (index["field"] not in columns or "GENERATED" in columns[index["field"]]["extra"]
                or any(index["field"] not in row for row in table.rows)):
            raise QAError(f"Índice único no representable en {table.name}; requiere todos sus valores explícitos.")
        unique.setdefault(index["name"], []).append((index["field"], index["prefix_length"]))
    if tuple(field for field, _ in unique.get("PRIMARY", [])) != table.keys:
        raise QAError(f"La clave primaria de {table.name} no coincide con la versión del seed.")
    return columns, list(unique.values()) + [[(key, None) for key in fields] for fields in table.natural_keys]


def matching(connection, table, fields, row, columns):
    values, clauses = [], []
    for field, prefix in fields:
        value = row.get(field, columns[field]["default_value"])
        if value is None:
            return []  # MySQL permits multiple NULL values in a UNIQUE index.
        values.append(value)
        if prefix:
            clauses.append(f"LEFT(`{field}`,{int(prefix)})=LEFT(%s,{int(prefix)})")
        else:
            clauses.append(f"`{field}`=%s")
    return query(connection, f"SELECT * FROM `{table.name}` WHERE {' AND '.join(clauses)} FOR UPDATE", tuple(values))


def same_fields(actual, expected, fields, columns):
    return all(equivalent(actual[field], expected[field], columns[field]["kind"]) for field in fields)


def check_foreign_keys(connection, tables):
    # The inspected ERP contract declares no FKs on these tables. A changed
    # constraint graph requires review, especially before cascading an update.
    names = tuple(table.name for table in tables)
    placeholders = ",".join("%s" for _ in names)
    found = query(connection, "SELECT CONSTRAINT_NAME FROM information_schema.KEY_COLUMN_USAGE "
                  "WHERE REFERENCED_TABLE_NAME IS NOT NULL AND "
                  f"((TABLE_SCHEMA=DATABASE() AND TABLE_NAME IN ({placeholders})) OR "
                  f"(REFERENCED_TABLE_SCHEMA=DATABASE() AND REFERENCED_TABLE_NAME IN ({placeholders}))) LIMIT 1",
                  names + names)
    if found:
        raise QAError("Clave foránea no certificada en tablas del seed; revisar el esquema del paquete.")


def apply_tables(connection, tables, *, preflight=None):
    """Own one transaction on a verified private connection; never print rows/errors.

    Also exercised by developer tests against an owned ephemeral server. Product
    entry points must obtain their connection through MySQLSandbox.connection().
    """
    from products.xgestion.seeds.triggers import check_triggers

    table_name = "preflight"
    connection.rollback()
    try:
        query(connection, "SET SESSION sql_mode='STRICT_ALL_TABLES,NO_ENGINE_SUBSTITUTION'")
        query(connection, "SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE")
        connection.begin()
        metadata = {table.name: schema_for(connection, table) for table in tables}
        check_foreign_keys(connection, tables)
        check_triggers(connection, tables)
        if preflight:
            preflight(connection)
        planned = []
        # Read every target and unique collision before the first business write.
        for table in tables:
            table_name = table.name
            columns, unique_keys = metadata[table.name]
            for row in table.rows:
                found = matching(connection, table, [(key, None) for key in table.keys], row, columns)
                current = found[0] if found else None
                if current and not same_fields(current, row, table.identity, columns):
                    raise QAError(f"Colisión de identidad en {table.name}; no se sobrescribe una fila ajena al seed.")
                for fields in unique_keys:
                    for other in matching(connection, table, fields, row, columns):
                        if not same_fields(other, row, table.keys, columns):
                            raise QAError(f"Colisión de clave única o código en {table.name}; revisar el baseline.")
                action = "inserted" if current is None else "unchanged" if same_fields(
                    current, row, row.keys(), columns) else "updated"
                planned.append((table, row, action))
        counts = {"inserted": 0, "updated": 0, "unchanged": 0}
        totals = {table.name: dict(counts) for table in tables}
        for table, row, action in planned:
            table_name = table.name
            if action != "unchanged":
                statement, values = upsert_sql(table, row)
                with connection.cursor() as cursor:
                    cursor.execute(statement, values)
            counts[action] += 1
            totals[table.name][action] += 1
        # Verify the entire final state, including relationships changed by triggers.
        for table, row, _ in planned:
            table_name = table.name
            columns, _ = metadata[table.name]
            stored = matching(connection, table, [(key, None) for key in table.keys], row, columns)
            if len(stored) != 1 or not same_fields(stored[0], row, row.keys(), columns):
                raise QAError(f"La verificación final de {table.name} difiere del catálogo; se revierte el lote.")
        connection.commit()
        return {"counts": counts, "tables": [{"name": name, **values} for name, values in totals.items()]}
    except BaseException as error:
        connection.rollback()
        if isinstance(error, (QAError, KeyboardInterrupt, SystemExit)):
            raise
        number = error.args[0] if error.args and type(error.args[0]) is int else "no disponible"
        raise QAError(f"Seed rechazado en {table_name}; lote revertido. Código SQL: {number}. "
                      "Revisar esquema, restricciones y datos del paquete.") from None


def catalog(context):
    from products.xgestion.seeds.pricing import pricing_tables
    from products.xgestion.seeds.products import product_tables

    return merge_tables(product_tables(context) + pricing_tables(context))


def describe_seed(reference_date=None):
    context = SeedContext(90001, 1, 1, 90001, reference_date or date.today())
    tables = catalog(context)
    by_name = {table.name: len(table.rows) for table in tables}
    return {"name": NAME, "reference_date": context.reference_date.isoformat(), "source_commit": SOURCE_COMMIT,
            "counts": {"tables": len(tables), "row_count": sum(by_name.values()), "products": by_name["articulos"],
                       "offers": by_name["ofertas"], "price_lists": by_name["t_fin_listaprecio"]},
            "tables": [{"name": table.name, "row_count": len(table.rows)} for table in tables]}


def render_seed(reference_date=None):
    """Offline review only: placeholders cannot accidentally run as a SQL batch."""
    context = SeedContext(90001, 1, 1, 90001, reference_date or date.today())
    lines = [f"-- {NAME}: PLAN PARAMETRIZADO PARA REVISION, NO EJECUTAR EN UN CLIENTE SQL.",
             "-- Aplicar mediante qa.cmd seed --apply o qa.cmd run --seed catalogo-comercial-v1.",
             "-- El comando verifica propiedad, esquema, claves y transaccion antes de escribir.",
             "-- Contexto SINTETICO de ejemplo: empresa 90001, sucursal 1, puesto 1, usuario 90001.",
             f"-- Fecha de referencia: {context.reference_date.isoformat()}; fuente ERP: {SOURCE_COMMIT}."]
    for table in catalog(context):
        lines.extend(["", f"-- Tabla {table.name}: {len(table.rows)} filas, se omiten las identicas."])
        for row in table.rows:
            sql, parameters = upsert_sql(table, row)
            lines.append("-- Parametros publicos de ejemplo: " + json.dumps(parameters, ensure_ascii=True, default=str))
            lines.append(sql + ";")
    return "\n".join(lines) + "\n"


def check_required_row(connection, table, where, expected):
    # Identifiers here belong to reviewed code, not command-line input.
    found = query(connection, f"SELECT * FROM `{table}` WHERE " + " AND ".join(f"`{key}`=%s" for key in where),
                  tuple(where.values()))
    if len(found) != 1:
        raise QAError(f"Falta el contexto o catálogo requerido en {table}; el seed no lo crea ni reemplaza.")
    kinds = query(connection, "SELECT COLUMN_NAME AS name, DATA_TYPE AS kind FROM information_schema.COLUMNS "
                  "WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME=%s", (table,))
    columns = {field["name"]: field for field in kinds}
    if not set(expected).issubset(columns) or not same_fields(found[0], expected, expected.keys(), columns):
        raise QAError(f"Catálogo global incompatible en {table}; verificar el paquete sin sobrescribirlo.")


def check_context(connection, context):
    from products.xgestion.seeds.products import REQUISITES

    server = query(connection, "SELECT DATABASE() AS db, CURDATE() AS today")[0]
    if server["db"] != "xsoft_qa":
        raise QAError("El seed solo admite la base privada xsoft_qa.")
    if str(server["today"]) != context.reference_date.isoformat():
        raise QAError("La fecha del seed debe coincidir con la fecha actual de MySQL para stock y vigencias.")
    for table, where in (
        ("_empresa", {"idEmp": context.empresa}),
        ("_sucursales", {"Empresa": context.empresa, "sucId": context.sucursal}),
        ("_computadoras", {"Empresa": context.empresa, "Sucursal": context.sucursal, "cpuId": context.computadora}),
        ("_usuarios", {"Empresa": context.empresa, "usuId": context.usuario_id}),
    ):
        check_required_row(connection, table, where, {})
    for table, key, identifier, expected in REQUISITES:
        check_required_row(connection, table, {key: identifier}, expected)


def apply_to_connection(connection, context):
    """Shared core for the guarded sandbox and the explicit synthetic DB tests."""
    from products.xgestion.seeds.isolation import check_isolation

    tables = catalog(context)
    encoded = json.dumps([asdict(table) for table in tables], sort_keys=True, default=str).encode()
    fingerprint = hashlib.sha256(encoded).hexdigest()

    def preflight(conn):
        check_context(conn, context)
        check_isolation(conn, context, tables)

    result = apply_tables(connection, tables, preflight=preflight)
    return {"name": NAME, "reference_date": context.reference_date.isoformat(), "source_commit": SOURCE_COMMIT,
            "catalog_sha256": fingerprint, **result}


def apply_seed(sandbox, fixtures, *, reference_date=None):
    from products.xgestion.contracts import validate_fixtures

    validate_fixtures(fixtures)
    declared = fixtures["context"]
    context = SeedContext(*(declared[key] for key in ("empresa", "sucursal", "computadora", "usuario_id")),
                          reference_date or date.today())
    articles = next(table.rows for table in catalog(context) if table.name == "articulos")
    fixture_codes = {value.rstrip().casefold() for value in (
        fixtures["product"]["code"], fixtures["nonexistent_product_code"])}
    if any(row["artId"] == fixtures["product"]["id"] or row["artCodigo"].casefold() in fixture_codes
           for row in articles):
        raise QAError("El catálogo seed colisiona con los fixtures originales; no se modifica el paquete.")
    with sandbox.connection() as connection:
        return apply_to_connection(connection, context)
