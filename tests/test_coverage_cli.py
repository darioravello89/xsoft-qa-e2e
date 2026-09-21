"""Public coverage commands remain offline and distinguish export from validation."""

import sys
from types import ModuleType

import pytest

from framework import cli
from framework.errors import QAError


@pytest.fixture
def exporter(monkeypatch, tmp_path):
    module = ModuleType("framework.coverage_export")
    output = tmp_path / "products/xgestion/coverage/mapa-cobertura.xlsx"
    calls = []

    def export(root):
        calls.append(("export", root))
        return output

    def check(root):
        calls.append(("check", root))
        return output

    def forbidden(*args, **kwargs):
        pytest.fail("Coverage no debe iniciar E2E ni cargar un perfil privado.")

    module.export_coverage = export
    module.check_coverage = check
    monkeypatch.setitem(sys.modules, "framework.coverage_export", module)
    for name in ("run", "doctor", "load_profile", "import_bundle", "calibrate"):
        monkeypatch.setattr(cli, name, forbidden)
    return module, calls, output


def test_coverage_parser_defaults_to_xgestion_export():
    args = cli.parser().parse_args(["coverage"])
    assert args.product == "xgestion"
    assert args.check is False


@pytest.mark.parametrize("product_args", [[], ["--product", "xgestion"]])
@pytest.mark.parametrize("check", [False, True])
def test_coverage_dispatches_exact_action_and_reports_path_without_claiming_e2e(
        tmp_path, capsys, exporter, product_args, check):
    _, calls, output = exporter
    args = ["coverage", *product_args, *(["--check"] if check else [])]
    assert cli.main(args, root=tmp_path) == 0
    assert calls == [("check" if check else "export", tmp_path)]
    captured = capsys.readouterr()
    assert str(output) in captured.out
    assert "no ejecuta E2E" in captured.out
    assert ("vigente" if check else "generado") in captured.out.lower()
    assert captured.err == ""


@pytest.mark.parametrize("check", [False, True])
def test_coverage_errors_are_actionable_and_check_never_regenerates(
        tmp_path, capsys, exporter, check):
    module, calls, _ = exporter

    def rejected(root):
        raise QAError("El mapa está desactualizado; ejecutar qa.cmd coverage.")

    if check:
        module.check_coverage = rejected
    else:
        module.export_coverage = rejected
    assert cli.main(["coverage", *(["--check"] if check else [])], root=tmp_path) == 2
    captured = capsys.readouterr()
    assert "BLOQUEADO: El mapa está desactualizado" in captured.err
    assert "qa.cmd coverage" in captured.err
    assert "generado" not in captured.out.lower() and "vigente" not in captured.out.lower()
    assert calls == []


@pytest.mark.parametrize("product", ["xportal", "mozos", "consultador", "unknown"])
def test_coverage_rejects_products_without_a_supported_map(exporter, product):
    with pytest.raises(SystemExit) as error:
        cli.main(["coverage", "--product", product])
    assert error.value.code == 2
    assert exporter[1] == []
