"""Fail closed on unknown database automation before any seed writes."""

from copy import deepcopy

import pytest

from framework.errors import QAError
from products.xgestion.seeds.model import SeedTable
from products.xgestion.seeds.triggers import CURRENT_FUNCTION, LEGACY_FUNCTION, check_triggers

TABLES = [SeedTable("articulos", ("Empresa", "artId"), ("artCodigo",), [])]
BODY = ("BEGIN SELECT fEnviarSincronizacion(NEW.Empresa,0,0,NEW.artId,"
        "'articulos','insert',NEW.usuario_insert) INTO @resultado; END")
PK = ("Empresa", "Sucursal", "Computadora", "ID", "Tabla", "ID_Computadora", "fecha_insert")


def trigger(**changes):
    return {"name": "articulos_AFTER_INSERT", "table_name": "articulos", "timing": "AFTER",
            "event": "INSERT", "orientation": "ROW", "body": BODY, **changes}


class MetadataConnection:
    def __init__(self):
        self.triggers = [trigger()]
        self.queue_triggers = []
        self.routines = [{"body": "RETURN 1", "kind": "int", "security_type": "DEFINER",
                          "routine_type": "FUNCTION"}]
        self.parameters = [{"position": i, "name": name, "mode": "IN", "kind": kind,
                            "length": 255 if kind == "varchar" else None}
                           for i, (name, kind) in enumerate([
                               ("p_empresa", "int"), ("p_sucursal", "int"), ("p_computadora", "int"),
                               ("p_id", "int"), ("p_tabla", "varchar"), ("p_accion", "varchar"),
                               ("p_usuario", "varchar")], 1)]
        self.queue = [{"engine": "InnoDB", "table_type": "BASE TABLE"}]
        self.dependencies = [{"engine": "InnoDB", "table_type": "BASE TABLE"}]
        self.indexes = [{"name": "PRIMARY", "field": field, "prefix_length": None} for field in PK]
        self.foreign_keys = []
        self.columns = [{"name": name, "kind": kind, "extra": ""} for name, kind in [
            ("Empresa", "int"), ("Sucursal", "int"), ("Computadora", "int"), ("ID", "int"),
            ("Tabla", "varchar"), ("Accion", "varchar"), ("SucursalesDestino", "varchar"),
            ("ComputadorasDestino", "varchar"), ("ID_Computadora", "int"),
            ("fecha_insert", "datetime"), ("usuario_insert", "varchar"),
            ("fecha_update", "datetime"), ("usuario_update", "varchar")]]
        self.calls = []

    def cursor(self):
        return self

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return None

    def execute(self, sql, values=()):
        self.calls.append((sql, values))
        if "information_schema.TRIGGERS" in sql:
            self.result = self.queue_triggers if values == ("t_int_sincronizador",) else self.triggers
        elif "information_schema.ROUTINES" in sql:
            self.result = self.routines
        elif "information_schema.PARAMETERS" in sql:
            self.result = self.parameters
        elif "information_schema.TABLES" in sql:
            self.result = self.queue if values == ("t_int_sincronizador",) else self.dependencies
        elif "information_schema.STATISTICS" in sql:
            self.result = self.indexes
        elif "information_schema.KEY_COLUMN_USAGE" in sql:
            self.result = self.foreign_keys
        elif "information_schema.COLUMNS" in sql:
            self.result = self.columns
        else:
            raise AssertionError(f"Unexpected query: {sql}")

    def fetchall(self):
        return deepcopy(self.result)


def test_absent_triggers_do_not_require_or_execute_a_function():
    connection = MetadataConnection()
    connection.triggers = []
    check_triggers(connection, TABLES)
    assert len(connection.calls) == 1


@pytest.mark.parametrize("event", ["INSERT", "UPDATE"])
def test_payment_trigger_requires_the_exact_reviewed_body_and_audit_actor(event):
    connection = MetadataConnection()
    action = event.lower()
    body = (f"BEGIN SELECT fEnviarSincronizacion(NEW.Empresa,0,0,NEW.pagId,"
            f"'_pagos','{action}',NEW.usuario_{action}) INTO @resultado; END")
    connection.triggers = [trigger(name=f"_pagos_AFTER_{event}", table_name="_pagos", event=event, body=body)]
    tables = [SeedTable("_pagos", ("Empresa", "pagId"), ("pagNombre",), [])]
    check_triggers(connection, tables)
    assert all(sql.startswith("SELECT ") for sql, _ in connection.calls)
    connection.triggers[0]["body"] = body.replace("NEW.pagId", "NEW.otroId")
    with pytest.raises(QAError, match="cuerpo"):
        check_triggers(connection, tables)


@pytest.mark.parametrize(("body", "kind"), [("RETURN 1", "int"),
                                           (LEGACY_FUNCTION, "bit"), (CURRENT_FUNCTION, "int")])
def test_known_complete_function_variants_and_exact_source_trigger_are_accepted(body, kind):
    connection = MetadataConnection()
    connection.routines[0].update(body=body, kind=kind)
    check_triggers(connection, TABLES)
    assert all(sql.lstrip().startswith("SELECT ") for sql, _ in connection.calls)


@pytest.mark.parametrize("change", [
    {"timing": "BEFORE"}, {"event": "DELETE"}, {"orientation": "STATEMENT"},
    {"name": "my_custom_trigger"}, {"body": BODY.replace("0,0", "1,0")},
    {"body": BODY.replace("'articulos'", "'ofertas'")},
    {"body": BODY.replace("END", "DELETE FROM otras; END")},
    {"body": BODY + " /* unknown addition */"},
    {"body": BODY.replace("fEnviarSincronizacion", "other.fEnviarSincronizacion")},
])
def test_unknown_or_before_trigger_is_rejected_without_evaluating_function(change):
    connection = MetadataConnection()
    connection.triggers = [trigger(**change)]
    with pytest.raises(QAError, match="trigger"):
        check_triggers(connection, TABLES)
    assert len(connection.calls) == 1


def test_duplicate_trigger_for_one_event_is_rejected():
    connection = MetadataConnection()
    connection.triggers *= 2
    with pytest.raises(QAError, match="trigger"):
        check_triggers(connection, TABLES)


@pytest.mark.parametrize("body", [None, "RETURN 2", "BEGIN DELETE FROM otras; RETURN 1; END",
                                  CURRENT_FUNCTION.replace("'t_fin_impuestos'", "' t_fin_impuestos'"),
                                  CURRENT_FUNCTION.replace("t_int_sincronizador", "otra_cola"),
                                  CURRENT_FUNCTION + " /* unverified */"])
def test_missing_modified_or_unknown_function_body_is_rejected(body):
    connection = MetadataConnection()
    connection.routines[0]["body"] = body
    with pytest.raises(QAError, match="función"):
        check_triggers(connection, TABLES)


def test_whitespace_changes_outside_literals_do_not_invalidate_source_definition():
    connection = MetadataConnection()
    connection.triggers[0]["body"] = BODY.replace("SELECT", "\n\tSELECT\n\t")
    connection.routines[0]["body"] = "\n RETURN\t1;\n"
    check_triggers(connection, TABLES)


@pytest.mark.parametrize("change", [{"kind": "varchar"}, {"security_type": "INVOKER"},
                                   {"routine_type": "PROCEDURE"}])
def test_function_metadata_must_match_known_contract(change):
    connection = MetadataConnection()
    connection.routines[0].update(change)
    with pytest.raises(QAError, match="función"):
        check_triggers(connection, TABLES)


def test_function_signature_is_not_inferred_from_body():
    connection = MetadataConnection()
    connection.parameters[-1]["length"] = 1
    with pytest.raises(QAError, match="parámetros"):
        check_triggers(connection, TABLES)


@pytest.mark.parametrize("attribute", ["queue_triggers", "foreign_keys"])
def test_queue_must_not_propagate_writes_to_uncertified_objects(attribute):
    connection = MetadataConnection()
    setattr(connection, attribute, [{"name": "arbitrary"}])
    with pytest.raises(QAError, match="cola"):
        check_triggers(connection, TABLES)


def test_queue_must_be_transactional_base_table():
    connection = MetadataConnection()
    connection.queue[0]["engine"] = "MyISAM"
    with pytest.raises(QAError, match="InnoDB"):
        check_triggers(connection, TABLES)


def test_queue_must_not_have_extra_unique_keys_or_prefixes():
    connection = MetadataConnection()
    connection.indexes.append({"name": "uk_other", "field": "ID", "prefix_length": None})
    with pytest.raises(QAError, match="clave"):
        check_triggers(connection, TABLES)
    connection.indexes.pop()
    connection.indexes[0]["prefix_length"] = 1
    with pytest.raises(QAError, match="clave"):
        check_triggers(connection, TABLES)


def test_both_documented_queue_primary_key_orders_are_accepted():
    connection = MetadataConnection()
    connection.indexes[3], connection.indexes[4] = connection.indexes[4], connection.indexes[3]
    check_triggers(connection, TABLES)


def test_queue_generated_or_extra_columns_are_rejected():
    connection = MetadataConnection()
    connection.columns[0]["extra"] = "STORED GENERATED"
    with pytest.raises(QAError, match="columnas"):
        check_triggers(connection, TABLES)


def test_known_function_cannot_resolve_context_reads_through_a_view():
    connection = MetadataConnection()
    connection.routines[0]["body"] = CURRENT_FUNCTION
    connection.dependencies[0]["table_type"] = "VIEW"
    with pytest.raises(QAError, match="dependencia"):
        check_triggers(connection, TABLES)


def test_rejection_does_not_expose_untrusted_sql_or_private_names():
    connection = MetadataConnection()
    connection.triggers[0].update(name="PRIVATE-TOKEN", body="CALL exfiltrate('PRIVATE-TOKEN')")
    with pytest.raises(QAError) as error:
        check_triggers(connection, TABLES)
    assert "PRIVATE-TOKEN" not in str(error.value)
