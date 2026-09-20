import subprocess
from types import SimpleNamespace

import javaproperties
import pytest

import framework.environment as environment
from framework.errors import QAError


@pytest.mark.parametrize("output", ["1", "3", "", "unknown"])
def test_network_unverified_or_active_blocks_start(monkeypatch, output):
    monkeypatch.setattr(environment, "os", SimpleNamespace(name="nt"))
    monkeypatch.setattr(environment.subprocess, "run", lambda *a, **kw: SimpleNamespace(stdout=output))
    with pytest.raises(QAError):
        environment.ensure_offline()


def test_disconnected_adapters_allow_preflight(monkeypatch):
    monkeypatch.setattr(environment, "os", SimpleNamespace(name="nt"))
    monkeypatch.setattr(environment.subprocess, "run", lambda *a, **kw: SimpleNamespace(stdout="0\r\n"))
    environment.ensure_offline()


def test_network_command_failure_does_not_assume_offline(monkeypatch):
    monkeypatch.setattr(environment, "os", SimpleNamespace(name="nt"))
    def fail(*args, **kwargs):
        raise subprocess.CalledProcessError(1, "powershell")
    monkeypatch.setattr(environment.subprocess, "run", fail)
    with pytest.raises(QAError):
        environment.ensure_offline()


def test_app_config_pins_private_connection_without_reimplementing_encryption(tmp_path):
    source = tmp_path / "imported.properties"
    values = {"conexionIp": "unexpected.invalid", "conexionPuerto": "3306", "conexionBaseDatos": "other",
              "conexionUsuario": "synthetic-encrypted-user", "conexionPassword": "synthetic-encrypted-password",
              "licencia": "synthetic-test-license", "sincronizadorActiva": "true"}
    with source.open("w", encoding="ascii") as handle:
        javaproperties.dump(values, handle, timestamp=False)
    runtime = tmp_path / "runtime"
    runtime.mkdir()
    profile = SimpleNamespace(runtime=runtime, asset=lambda key: source)
    environment.prepare_app_config(profile)
    with (runtime / "app/config.properties").open("rb") as handle:
        actual = javaproperties.load(handle)
    assert actual["conexionIp"] == "127.0.0.1"
    assert actual["conexionPuerto"] == "13317"
    assert actual["conexionBaseDatos"] == "xsoft_qa"
    assert actual["sincronizadorActiva"] == "false"
    for key in ("conexionUsuario", "conexionPassword", "licencia"):
        assert actual[key] == values[key]
    with source.open("rb") as handle:
        assert javaproperties.load(handle) == values
