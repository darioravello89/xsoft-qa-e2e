import json
import sys
from datetime import date
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from framework import cli, runner
from framework.errors import QAError
from products.xgestion.seeds import command

NAME = "catalogo-comercial-v1"


@pytest.fixture
def engine(monkeypatch):
    module = SimpleNamespace(
        describe_seed=Mock(return_value={"name": NAME, "reference_date": "2026-09-21",
                                        "counts": {"products": 12, "tables": 4}}),
        render_seed=Mock(return_value="-- Vista previa pública\nSELECT 'QA-SEED-TEST';\n"),
        apply_seed=Mock(return_value={"name": NAME, "reference_date": "2026-09-21",
                                     "counts": {"inserted": 12, "updated": 0, "unchanged": 0},
                                     "tables": []}),
    )
    monkeypatch.setattr(command, "_engine", lambda: module)
    monkeypatch.setitem(sys.modules, "products.xgestion.seeds.engine", module)
    return module


@pytest.mark.parametrize("dry_run", [False, True])
def test_preview_is_offline_without_profile_or_database(tmp_path, monkeypatch, capsys, engine, dry_run):
    monkeypatch.setattr(command, "load_profile", lambda *_: pytest.fail("No leer perfil privado"))
    monkeypatch.setattr(command, "ensure_offline", lambda: pytest.fail("No comprobar red para preview"))
    monkeypatch.setattr(command, "MySQLSandbox", lambda *_: pytest.fail("No crear DB"))
    assert command.run_seed(tmp_path, dry_run=dry_run) == 0
    output = capsys.readouterr().out
    assert NAME in output and "sin conexión" in output and "no verificados" in output
    engine.apply_seed.assert_not_called()
    assert not (tmp_path / ".local").exists()


def test_preview_can_export_reviewable_sql_without_private_data(tmp_path, engine, capsys):
    assert command.run_seed(tmp_path, export=True, reference_date=date(2026, 9, 21)) == 0
    export = tmp_path / "work/seed-preview.sql"
    assert export.read_text(encoding="utf-8") == engine.render_seed.return_value
    assert str(export) in capsys.readouterr().out
    engine.render_seed.assert_called_once_with(reference_date=date(2026, 9, 21))


def prepared_apply(tmp_path, monkeypatch, engine):
    order = []
    fixture_path = tmp_path / "fixtures.json"
    fixture_path.write_text((Path(__file__).resolve().parents[1] /
                             "products/xgestion/examples/fixtures.example.json").read_text(encoding="utf-8"),
                            encoding="utf-8")
    profile = SimpleNamespace(values={"QA_DB_PASSWORD": "SEED-PRIVATE-CANARY"},
                              manifest={"mysql_version": "5.7.44", "app_version": "2.02.189-lts",
                                        "files": {"dump": {"sha256": "a" * 64}}},
                              asset=lambda _: fixture_path)
    monkeypatch.setattr(command, "load_profile", lambda *_: order.append("profile") or profile)
    monkeypatch.setattr(command, "ensure_offline", lambda: order.append("offline"))
    server = SimpleNamespace(start=lambda: order.append("start"), restore=lambda: order.append("restore"),
                             stop=lambda: order.append("stop"))
    monkeypatch.setattr(command, "MySQLSandbox", lambda _: server)
    result = engine.apply_seed.return_value
    engine.apply_seed.side_effect = lambda *a, **k: order.append("apply") or result
    return order, server, profile


def test_apply_restores_only_owned_sandbox_then_seeds_and_stops(tmp_path, monkeypatch, engine, capsys):
    order, server, profile = prepared_apply(tmp_path, monkeypatch, engine)
    assert command.run_seed(tmp_path, apply=True) == 0
    assert order.index("offline") < order.index("start") < order.index("restore") < order.index("apply")
    assert order[-1] == "stop"
    assert engine.apply_seed.call_args.args[0] is server
    report = next((tmp_path / "reports").glob("*-seed-*/seed-summary.json"))
    payload = json.loads(report.read_text(encoding="utf-8"))
    assert payload["status"] == "seed-applied" and payload["counts"]["inserted"] == 12
    assert payload["baseline_sha256"] == profile.manifest["files"]["dump"]["sha256"]
    assert "SEED-PRIVATE-CANARY" not in report.read_text(encoding="utf-8")
    assert "E2E" in capsys.readouterr().out
    assert not (tmp_path / ".local/run.lock").exists()
    assert not (tmp_path / "reports/latest.json").exists()


def test_apply_failure_stops_database_and_records_sanitized_block(tmp_path, monkeypatch, engine, capsys):
    order, _, _ = prepared_apply(tmp_path, monkeypatch, engine)
    engine.apply_seed.side_effect = QAError("Colisión SEED-PRIVATE-CANARY")
    assert command.run_seed(tmp_path, apply=True) == 2
    assert order[-1] == "stop"
    report = next((tmp_path / "reports").glob("*-seed-*/seed-summary.json"))
    payload = json.loads(report.read_text(encoding="utf-8"))
    assert payload["status"] == "blocked"
    assert "SEED-PRIVATE-CANARY" not in report.read_text(encoding="utf-8")
    output = capsys.readouterr()
    assert "SEED-PRIVATE-CANARY" not in output.out + output.err


def test_apply_does_not_start_mysql_when_isolation_is_blocked(tmp_path, monkeypatch, engine):
    order, _, _ = prepared_apply(tmp_path, monkeypatch, engine)
    monkeypatch.setattr(command, "ensure_offline", Mock(side_effect=QAError("Red activa")))
    assert command.run_seed(tmp_path, apply=True) == 2
    assert "start" not in order and "restore" not in order
    engine.apply_seed.assert_not_called()


def test_cli_seed_and_run_flags_are_explicit_and_preserve_default(tmp_path, monkeypatch):
    seed_call, run_call = Mock(return_value=0), Mock(return_value=0)
    monkeypatch.setattr(command, "run_seed", seed_call)
    monkeypatch.setattr(cli, "run", run_call)
    assert cli.main(["seed", "--dry-run", "--reference-date", "2026-09-21", "--export"], root=tmp_path) == 0
    assert seed_call.call_args.kwargs == {"apply": False, "dry_run": True, "export": True,
                                          "reference_date": date(2026, 9, 21)}
    assert cli.main(["run", "--dry-run", "--seed", NAME], root=tmp_path) == 0
    assert run_call.call_args.kwargs["seed"] == NAME
    assert cli.main(["run", "--dry-run"], root=tmp_path) == 0
    assert "seed" not in run_call.call_args.kwargs


def test_cli_rejects_incompatible_seed_actions_and_other_products(tmp_path):
    with pytest.raises(SystemExit) as error:
        cli.parser().parse_args(["seed", "--dry-run", "--apply"])
    assert error.value.code == 2
    assert cli.main(["seed", "--product", "xportal"], root=tmp_path) == 2


def test_runner_dryrun_seed_is_described_without_profile_or_database(tmp_path, monkeypatch, engine, capsys):
    from test_groups_cli import make_catalog

    make_catalog(tmp_path)
    monkeypatch.setattr(runner, "load_profile", lambda *_: pytest.fail("No acceder al perfil"))
    monkeypatch.setattr(runner, "build_robot_reports", lambda *_: None)
    monkeypatch.setattr(runner, "execute_robot", lambda *a, **k: {
        "code": 0, "case_results": [{"id": "XG-VEN-001", "title": "Venta", "status": "validated-only"}],
        "total": 1})
    assert runner.run(tmp_path, "xgestion", "ventas", dry_run=True, seed=NAME) == 0
    summary = next((tmp_path / "reports").glob("*/summary.json"))
    payload = json.loads(summary.read_text(encoding="utf-8"))
    assert payload["seed"]["status"] == "preview-only"
    assert payload["seed"]["name"] == NAME
    assert "sin conexión" in capsys.readouterr().out
    engine.apply_seed.assert_not_called()


@pytest.mark.parametrize("seed", [None, NAME])
def test_runner_only_applies_requested_seed_after_restore(tmp_path, monkeypatch, engine, seed):
    from test_groups_cli import make_catalog

    from framework.fixtures import mysql

    make_catalog(tmp_path)
    order, server, profile = prepared_apply(tmp_path, monkeypatch, engine)
    profile.manifest["files"].update({name: {"sha256": "b" * 64} for name in ("app", "fixtures", "locators")})
    monkeypatch.setattr(runner, "load_profile", lambda *_: profile)
    monkeypatch.setattr(runner, "doctor", lambda *a, **k: None)
    monkeypatch.setattr(runner, "prepare_app_config", lambda *_: None)
    monkeypatch.setattr(runner, "ensure_offline", lambda: None)
    monkeypatch.setattr(mysql, "MySQLSandbox", lambda *_: server)
    monkeypatch.setattr(runner, "build_robot_reports", lambda *_: None)
    monkeypatch.setattr(runner, "version", lambda _: "test")

    def execute(*args, **kwargs):
        order.append("robot")
        return {"code": 0, "case_results": [{"id": "XG-VEN-001", "title": "Venta", "status": "passed"}]}

    monkeypatch.setattr(runner, "execute_robot", execute)
    assert runner.run(tmp_path, "xgestion", "ventas", seed=seed) == 0
    if seed:
        assert order.index("restore") < order.index("apply") < order.index("robot")
        engine.apply_seed.assert_called_once()
    else:
        engine.apply_seed.assert_not_called()
    assert order[-1] == "stop"


def prepared_run(tmp_path, monkeypatch, engine):
    from test_groups_cli import make_catalog

    from framework.fixtures import mysql

    make_catalog(tmp_path)
    order, server, profile = prepared_apply(tmp_path, monkeypatch, engine)
    profile.manifest["files"].update({name: {"sha256": "b" * 64} for name in ("app", "fixtures", "locators")})
    monkeypatch.setattr(runner, "load_profile", lambda *_: profile)
    monkeypatch.setattr(runner, "doctor", lambda *a, **k: None)
    monkeypatch.setattr(runner, "prepare_app_config", lambda *_: None)
    monkeypatch.setattr(runner, "ensure_offline", lambda: None)
    monkeypatch.setattr(mysql, "MySQLSandbox", lambda *_: server)
    monkeypatch.setattr(runner, "build_robot_reports", lambda *_: None)
    monkeypatch.setattr(runner, "version", lambda _: "test")
    monkeypatch.setattr(runner, "execute_robot", lambda *a, **k: {
        "code": 0, "case_results": [{"id": "XG-VEN-001", "title": "Venta", "status": "passed"}]})
    return order, server, profile


@pytest.mark.parametrize("interface", ["command", "runner"])
@pytest.mark.parametrize("stage,expected_code", [("partial_restore", 2), ("apply_cancel", 130),
                                                ("cleanup", 2), ("cancel_and_cleanup", 130)])
def test_seed_lifecycle_failures_keep_requested_metadata_and_never_report_false_success(
        tmp_path, monkeypatch, engine, capsys, interface, stage, expected_code):
    prepare = prepared_run if interface == "runner" else prepared_apply
    order, server, profile = prepare(tmp_path, monkeypatch, engine)
    profile.values["QA_LOGIN_PASSWORD"] = "blocked"
    if stage == "partial_restore":
        server.restore = Mock(side_effect=QAError("Dump parcial SEED-PRIVATE-CANARY"))
    if stage in {"apply_cancel", "cancel_and_cleanup"}:
        engine.apply_seed.side_effect = KeyboardInterrupt
    if stage in {"cleanup", "cancel_and_cleanup"}:
        def failed_cleanup():
            order.append("stop")
            raise QAError("Cierre blocked SEED-PRIVATE-CANARY")
        server.stop = failed_cleanup
    invoke = (lambda: runner.run(tmp_path, "xgestion", "ventas", seed=NAME)) if interface == "runner" else (
        lambda: command.run_seed(tmp_path, apply=True))
    assert invoke() == expected_code
    path = next((tmp_path / "reports").glob("*/summary.json" if interface == "runner" else "*/seed-summary.json"))
    payload = json.loads(path.read_text(encoding="utf-8"))
    state = "cancelled" if expected_code == 130 else "blocked"
    assert payload["status"] == state and payload["exit_code"] == expected_code
    seed = payload["seed"] if interface == "runner" else payload
    assert seed["name"] == NAME
    assert seed["status"] == ("seed-applied" if interface == "runner" and stage == "cleanup" else state)
    assert order[-1] == "stop"
    assert not (tmp_path / ".local/run.lock").exists()
    if stage == "partial_restore":
        engine.apply_seed.assert_not_called()
    assert "SEED-PRIVATE-CANARY" not in path.read_text(encoding="utf-8")
    output = capsys.readouterr()
    assert "SEED-PRIVATE-CANARY" not in output.out + output.err


@pytest.mark.parametrize("interface", ["command", "runner"])
@pytest.mark.parametrize("kind", ["event", "report"])
def test_final_evidence_failure_never_returns_success(tmp_path, monkeypatch, engine, capsys, interface, kind):
    prepare = prepared_run if interface == "runner" else prepared_apply
    prepare(tmp_path, monkeypatch, engine)
    if kind == "event":
        original_emit = command.EventWriter.emit

        def fail_final_event(self, level, event, message, **details):
            if event == "run_end":
                raise OSError("SEED-PRIVATE-CANARY")
            return original_emit(self, level, event, message, **details)

        monkeypatch.setattr(command.EventWriter, "emit", fail_final_event)
    elif interface == "runner":
        monkeypatch.setattr(runner, "write_run_report", Mock(side_effect=OSError("SEED-PRIVATE-CANARY")))
    else:
        original_write = Path.write_text

        def fail_seed_report(path, *args, **kwargs):
            if path.name == "seed-summary.json":
                raise OSError("SEED-PRIVATE-CANARY")
            return original_write(path, *args, **kwargs)

        monkeypatch.setattr(Path, "write_text", fail_seed_report)
    invoke = (lambda: runner.run(tmp_path, "xgestion", "ventas", seed=NAME)) if interface == "runner" else (
        lambda: command.run_seed(tmp_path, apply=True))
    assert invoke() == 2
    summary = list((tmp_path / "reports").glob("*/summary.json" if interface == "runner" else "*/seed-summary.json"))
    if summary:
        payload = json.loads(summary[0].read_text(encoding="utf-8"))
        assert payload["status"] == "blocked" and payload["exit_code"] == 2
    output = capsys.readouterr()
    assert "SEED-PRIVATE-CANARY" not in output.out + output.err


def test_report_failure_does_not_turn_a_real_cancellation_into_success_or_regular_failure(
        tmp_path, monkeypatch, engine):
    prepared_run(tmp_path, monkeypatch, engine)
    engine.apply_seed.side_effect = KeyboardInterrupt
    monkeypatch.setattr(runner, "write_run_report", Mock(side_effect=OSError("Report unavailable")))
    assert runner.run(tmp_path, "xgestion", "ventas", seed=NAME) == 130
    summary = next((tmp_path / "reports").glob("*/summary.json"))
    payload = json.loads(summary.read_text(encoding="utf-8"))
    assert payload["status"] == payload["seed"]["status"] == "cancelled"
