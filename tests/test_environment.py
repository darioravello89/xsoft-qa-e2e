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


@pytest.mark.parametrize("name,general,offers,warning", [
    ("base", "true", "true", "false"), ("general-off", "false", "true", "false"),
    ("offers-off", "true", "false", "false"), ("allowed-warning-on", "true", "true", "true"),
    ("allowed-warning-off", "true", "true", "false"),
])
def test_offer_profile_sets_only_declared_runtime_properties(tmp_path, name, general, offers, warning):
    source = tmp_path / "imported.properties"
    company_key = "empresa.90001.venta.recalcularProductosAlCambiarListaPrecioVenta"
    original = {company_key: "false", "licencia": "SYNTHETIC-LICENSE", "other.setting": "keep",
                "pedirPagoAlCerrarTicket": "false"}
    with source.open("w", encoding="ascii") as handle:
        javaproperties.dump(original, handle, timestamp=False)
    runtime = tmp_path / "runtime"
    runtime.mkdir()
    profile = SimpleNamespace(runtime=runtime, asset=lambda _: source)
    receipt = environment.prepare_app_config(profile, offer_profile=name, company_id=90001)
    with (runtime / "app/config.properties").open("rb") as handle:
        actual = javaproperties.load(handle)
    assert actual["venta.permitirDescuentosEdicionArticulos"] == general
    assert actual["venta.permitirDescuentosManualesArticulosConOferta"] == offers
    assert actual["alertas.advertirDescuentosManualesArticulosConOferta"] == warning
    assert actual["venta.listadeprecio.elegir"] == "true" and actual[company_key] == "true"
    assert actual["pedirPagoAlCerrarTicket"] == "true"
    assert actual["other.setting"] == "keep" and actual["licencia"] == "SYNTHETIC-LICENSE"
    assert actual["sincronizadorActiva"] == "false" and actual["conexionBaseDatos"] == "xsoft_qa"
    assert receipt["profile"] == name and "SYNTHETIC-LICENSE" not in repr(receipt)
    with source.open("rb") as handle:
        assert javaproperties.load(handle) == original


@pytest.mark.parametrize("name,company", [("arbitrary", 90001), ("base", None), ("base", True),
                                         ("base", 0), ("base", "../other")])
def test_invalid_offer_profiles_do_not_write_config(tmp_path, name, company):
    profile = SimpleNamespace(runtime=tmp_path, asset=lambda _: pytest.fail("Do not read private config"))
    with pytest.raises(QAError):
        environment.prepare_app_config(profile, offer_profile=name, company_id=company)
    assert not (tmp_path / "app").exists()
