"""El mapa publicado debe fallar cerrado si no corresponde al catálogo actual."""

import json
import shutil
import zipfile
from pathlib import Path

import pytest

from framework import coverage_export
from framework.errors import QAError

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def export_repo(tmp_path, monkeypatch):
    for relative in coverage_export.GENERATORS:
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, destination)
    monkeypatch.setattr(coverage_export, "build_coverage", lambda root: {"schema_version": 1, "scenarios": []})
    monkeypatch.setattr(coverage_export, "runtime", lambda: (Path("node"), Path("modules")))

    def build(arguments, **kwargs):
        with zipfile.ZipFile(arguments[3], "w") as workbook:
            workbook.writestr("[Content_Types].xml", "<Types/>")
            workbook.writestr("xl/workbook.xml", "<workbook/>")

    monkeypatch.setattr(coverage_export.subprocess, "run", build)
    return tmp_path


def test_export_and_check_need_no_private_profile_or_runtime_for_check(export_repo, monkeypatch):
    output = coverage_export.export_coverage(export_repo)
    assert output.is_file()
    monkeypatch.setattr(coverage_export, "runtime", lambda: pytest.fail("--check no necesita Node"))
    assert coverage_export.check_coverage(export_repo) == output
    data = json.loads(output.with_suffix(".json").read_text(encoding="utf-8"))
    assert data == {"schema_version": 1, "scenarios": []}


@pytest.mark.parametrize("change", ["source", "builder", "xlsx", "json", "manifest", "missing"])
def test_stale_or_damaged_export_is_rejected(export_repo, monkeypatch, change):
    output = coverage_export.export_coverage(export_repo)
    if change == "source":
        monkeypatch.setattr(coverage_export, "build_coverage", lambda root: {"schema_version": 2})
    elif change == "builder":
        (export_repo / "scripts/build-coverage.mjs").write_text("// changed", encoding="utf-8")
    elif change == "missing":
        output.unlink()
    elif change == "manifest":
        output.with_suffix(".manifest.json").write_text("null", encoding="utf-8")
    else:
        target = output if change == "xlsx" else output.with_suffix(".json")
        target.write_bytes(b"broken")
    with pytest.raises(QAError, match="coverage"):
        coverage_export.check_coverage(export_repo)


def test_failed_builder_preserves_previous_deliverable(export_repo, monkeypatch):
    output = coverage_export.export_coverage(export_repo)
    original = output.read_bytes()

    def fail(*args, **kwargs):
        raise coverage_export.subprocess.TimeoutExpired("node", 180)

    monkeypatch.setattr(coverage_export.subprocess, "run", fail)
    with pytest.raises(QAError, match="generar"):
        coverage_export.export_coverage(export_repo)
    assert output.read_bytes() == original
    assert coverage_export.check_coverage(export_repo) == output


def test_missing_runtime_has_actionable_error(monkeypatch, tmp_path):
    monkeypatch.setenv("QA_COVERAGE_NODE", str(tmp_path / "missing.exe"))
    monkeypatch.setenv("QA_COVERAGE_MODULES", str(tmp_path / "modules"))
    with pytest.raises(QAError, match="QA_COVERAGE_NODE"):
        coverage_export.runtime()


def test_excel_formula_errors_are_not_published(export_repo, monkeypatch):
    output = coverage_export.export_coverage(export_repo)
    original = output.read_bytes()

    def broken_workbook(arguments, **kwargs):
        with zipfile.ZipFile(arguments[3], "w") as workbook:
            workbook.writestr("[Content_Types].xml", "<Types/>")
            workbook.writestr("xl/workbook.xml", "<workbook/>")
            workbook.writestr("xl/worksheets/sheet1.xml", '<worksheet xmlns="urn:sheet">'
                              '<c r="A1" t="e"><v>Function is not implemented</v></c></worksheet>')

    monkeypatch.setattr(coverage_export.subprocess, "run", broken_workbook)
    with pytest.raises(QAError, match="errores de cálculo"):
        coverage_export.export_coverage(export_repo)
    assert output.read_bytes() == original
