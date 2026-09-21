"""Restore keeps narrowly privileged definers, never unknown or global accounts."""

import hashlib
import json
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from framework.errors import QAError
from framework.fixtures.mysql import MySQLSandbox


def sandbox(tmp_path, monkeypatch):
    dump = tmp_path / "baseline.sql"
    dump.write_text("-- Synthetic trusted fixture\n", encoding="utf-8")
    profile = SimpleNamespace(root=tmp_path, runtime=tmp_path / ".local/xgestion",
                              manifest={"mysql_version": "5.7.44", "files": {"dump": {
                                  "sha256": hashlib.sha256(dump.read_bytes()).hexdigest()}}},
                              env=lambda *_: "PRIVATE-ROOT-CANARY", asset=lambda _: dump)
    instance = MySQLSandbox(profile)
    instance.runtime.mkdir(parents=True)
    monkeypatch.setattr(instance, "_assert_owned_server", Mock())
    monkeypatch.setattr(instance, "_sql", Mock(return_value="0\n"))
    monkeypatch.setattr(instance, "_client", Mock())
    monkeypatch.setattr("framework.fixtures.mysql.secrets.token_urlsafe", lambda _: "PRIVATE-IMPORT-CANARY")
    return instance


def record_previous(instance, user="fixture_012345abcdef"):
    marker = instance.runtime / "mysql-restore-account.json"
    marker.write_text(json.dumps({"schema": 1, "datadir": str(instance.datadir),
                                  "user": user, "host": "127.0.0.1"}), encoding="utf-8")
    return marker


def test_restore_locks_but_does_not_drop_new_definer(tmp_path, monkeypatch):
    instance = sandbox(tmp_path, monkeypatch)
    instance.restore()
    user = instance._client.call_args.kwargs["user"]
    statements = [call.args[0] for call in instance._sql.call_args_list]
    assert statements[-1] == f"ALTER USER '{user}'@'127.0.0.1' ACCOUNT LOCK;"
    assert not any(f"DROP USER IF EXISTS '{user}'" in sql for sql in statements)
    assert any("GRANT ALL PRIVILEGES ON `xsoft\\_qa`.*" in sql for sql in statements)
    assert not any("SUPER" in sql or "ON *.*" in sql or "GRANT OPTION" in sql for sql in statements)
    marker = instance.runtime / "mysql-restore-account.json"
    assert json.loads(marker.read_text(encoding="utf-8"))["user"] == user
    assert "PRIVATE-IMPORT-CANARY" not in marker.read_text(encoding="utf-8")


def test_failed_import_still_locks_its_retained_definer(tmp_path, monkeypatch):
    instance = sandbox(tmp_path, monkeypatch)
    instance._client.side_effect = QAError("Dump incompatible")
    with pytest.raises(QAError, match="Dump incompatible"):
        instance.restore()
    assert "ACCOUNT LOCK" in instance._sql.call_args.args[0]
    assert (instance.runtime / "mysql-restore-account.json").exists()


def test_next_restore_cleans_only_recorded_unreferenced_account(tmp_path, monkeypatch):
    instance = sandbox(tmp_path, monkeypatch)
    record_previous(instance)
    instance.restore()
    statements = [call.args[0] for call in instance._sql.call_args_list]
    drop_database = next(i for i, sql in enumerate(statements) if sql.startswith("DROP DATABASE"))
    check_references = next(i for i, sql in enumerate(statements) if "information_schema.ROUTINES" in sql)
    drop_user = next(i for i, sql in enumerate(statements) if "DROP USER IF EXISTS 'fixture_012345abcdef'" in sql)
    assert drop_database < check_references < drop_user
    assert "LIKE" not in " ".join(statements)


def test_referenced_previous_account_is_preserved(tmp_path, monkeypatch):
    instance = sandbox(tmp_path, monkeypatch)
    record_previous(instance)
    instance._sql.return_value = "1\n"
    instance.restore()
    assert not any("DROP USER IF EXISTS 'fixture_012345abcdef'" in call.args[0]
                   for call in instance._sql.call_args_list)


@pytest.mark.parametrize("change", [{"user": "root"}, {"datadir": "C:/foreign"}, {"host": "%"}])
def test_invalid_restore_marker_blocks_before_drop_database(tmp_path, monkeypatch, change):
    instance = sandbox(tmp_path, monkeypatch)
    marker = record_previous(instance)
    marker.write_text(json.dumps({**json.loads(marker.read_text(encoding="utf-8")), **change}), encoding="utf-8")
    with pytest.raises(QAError, match="importador"):
        instance.restore()
    instance._sql.assert_not_called()


def test_failed_create_does_not_lock_a_user_it_did_not_create(tmp_path, monkeypatch):
    instance = sandbox(tmp_path, monkeypatch)

    def execute(statement):
        if statement.startswith("CREATE USER"):
            raise QAError("No se creó cuenta")
        return "0\n"

    instance._sql.side_effect = execute
    with pytest.raises(QAError):
        instance.restore()
    assert not any("ACCOUNT LOCK" in call.args[0] for call in instance._sql.call_args_list)
