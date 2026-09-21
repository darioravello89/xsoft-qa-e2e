"""Harness guardrails; real MySQL requires an explicit opt-in path."""

import os
from pathlib import Path

import psutil
import pytest
from seed_mysql_runtime import EphemeralMySQL, checked_work_path

ROOT = Path(__file__).resolve().parents[1]


def test_harness_requires_explicit_binary_without_discovering_services(monkeypatch):
    monkeypatch.delenv("XSOFT_SEED_MYSQL_BIN", raising=False)
    with pytest.raises(ValueError, match="explícito"):
        EphemeralMySQL(ROOT)


def test_harness_rejects_datadir_outside_repo_work(tmp_path):
    with pytest.raises(ValueError, match="work"):
        checked_work_path(ROOT, tmp_path / "data")


@pytest.mark.skipif(os.name != "nt" or not os.environ.get("XSOFT_SEED_MYSQL_BIN"),
                    reason="Requiere Windows y XSOFT_SEED_MYSQL_BIN explícito; nunca usa un servicio instalado")
def test_real_owned_server_identity_and_shutdown():
    with EphemeralMySQL(ROOT) as server:
        process_id = server.process.pid
        assert server.port != 13317
        with server.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT @@version, @@port, @@datadir, DATABASE()")
                version, port, datadir, database = cursor.fetchone()
                assert version == server.version and port == server.port
                assert Path(datadir).resolve() == server.datadir.resolve()
                assert database == "xsoft_qa"
    assert not psutil.pid_exists(process_id)
    assert not (server.directory / "init.sql").exists()
