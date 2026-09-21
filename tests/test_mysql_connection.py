"""Seed connections must belong to the exact private process and database."""

from types import SimpleNamespace
from unittest.mock import MagicMock, Mock

import pymysql
import pytest

from framework.errors import QAError
from framework.fixtures.mysql import MySQLSandbox


def sandbox(tmp_path, monkeypatch):
    profile = SimpleNamespace(root=tmp_path, runtime=tmp_path / ".local/xgestion",
                              manifest={"mysql_version": "5.7.44"},
                              env=lambda *_: "PRIVATE-DB-CANARY")
    instance = MySQLSandbox(profile)
    monkeypatch.setattr(instance, "_assert_owned_server", Mock())
    connection = MagicMock()
    cursor = connection.cursor.return_value.__enter__.return_value
    cursor.fetchone.return_value = {"datadir": str(instance.datadir), "port": 13317,
                                    "version": "5.7.44", "database_name": "xsoft_qa"}
    connect = Mock(return_value=connection)
    monkeypatch.setattr(pymysql, "connect", connect)
    return instance, connection, cursor, connect


def test_connection_requires_own_live_server_before_open(tmp_path, monkeypatch):
    instance, _, _, connect = sandbox(tmp_path, monkeypatch)
    instance._assert_owned_server.side_effect = QAError("No pertenece al runner")
    with pytest.raises(QAError, match="pertenece"):
        with instance.connection():
            pytest.fail("No se debe entregar conexión")
    connect.assert_not_called()


@pytest.mark.parametrize("key,value", [("datadir", "C:/foreign"), ("port", 3306),
                                       ("version", "5.7.43"), ("database_name", "production")])
def test_identity_on_same_connection_is_checked_before_yield(tmp_path, monkeypatch, key, value):
    instance, connection, cursor, _ = sandbox(tmp_path, monkeypatch)
    cursor.fetchone.return_value[key] = value
    with pytest.raises(QAError, match="identidad"):
        with instance.connection():
            pytest.fail("No se debe entregar conexión ajena")
    connection.rollback.assert_called_once()
    connection.close.assert_called_once()


def test_connection_uses_fixed_target_parameters_and_never_implicit_commit(tmp_path, monkeypatch):
    instance, connection, _, connect = sandbox(tmp_path, monkeypatch)
    with instance.connection() as actual:
        assert actual is connection
    options = connect.call_args.kwargs
    assert (options["host"], options["port"], options["database"]) == ("127.0.0.1", 13317, "xsoft_qa")
    assert options["autocommit"] is False and options["local_infile"] is False
    assert options["cursorclass"] is pymysql.cursors.DictCursor
    connection.commit.assert_not_called()
    connection.rollback.assert_called_once()
    connection.close.assert_called_once()


def test_database_errors_do_not_expose_driver_text_or_parameters(tmp_path, monkeypatch):
    instance, connection, _, _ = sandbox(tmp_path, monkeypatch)
    with pytest.raises(QAError) as failure:
        with instance.connection():
            raise pymysql.IntegrityError("PRIVATE-DB-CANARY SQL values")
    assert "PRIVATE-DB-CANARY" not in str(failure.value)
    assert "SQL values" not in str(failure.value)
    connection.rollback.assert_called_once()
    connection.close.assert_called_once()


def test_different_port_attribute_cannot_redirect_seed(tmp_path, monkeypatch):
    instance, _, _, connect = sandbox(tmp_path, monkeypatch)
    instance.port = 3306
    with pytest.raises(QAError, match="13317"):
        with instance.connection():
            pytest.fail("Puerto ajeno")
    connect.assert_not_called()
