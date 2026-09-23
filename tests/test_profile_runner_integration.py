"""Runner-owned restore/config/process ordering and aggregate evidence."""

import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from test_profile_runs import outcome

from framework import runner
from framework.fixtures import mysql
from products.xgestion.seeds import engine

REAL_EXECUTE_ROBOT = runner.execute_robot


@pytest.fixture
def prepared(tmp_path, monkeypatch):
    order = []
    ids = ("XG-PRM-001", "XG-PRM-070", "XG-PRM-079")
    cases = [{"id": key, "title": key, "product": "xgestion", "status": "implemented",
              "tags": ["promociones"], "seed": "catalogo-comercial-v1"} for key in ids]
    fixtures = Path(__file__).resolve().parents[1] / "products/xgestion/examples/fixtures.example.json"
    profile = SimpleNamespace(values={"QA_DB_PASSWORD": "PRIVATE-CANARY"}, runtime=tmp_path,
                              asset=lambda _: fixtures,
                              manifest={"app_version": "test", "files": {
                                  name: {"sha256": "a" * 64} for name in ("app", "dump", "fixtures", "locators")}})
    sandbox = SimpleNamespace(start=lambda: order.append(("start",)),
                              restore=lambda: order.append(("restore",)),
                              stop=lambda: order.append(("stop",)))
    monkeypatch.setattr(runner, "validate_catalog", lambda _: cases)
    monkeypatch.setattr(runner, "_groups_for_run", lambda *a: [])
    monkeypatch.setattr(runner, "load_profile", lambda _: profile)
    monkeypatch.setattr(runner, "doctor", lambda *a, **k: order.append(("doctor",)))
    monkeypatch.setattr(runner, "ensure_offline", lambda: order.append(("offline",)))
    monkeypatch.setattr(runner, "version", lambda _: "test")
    monkeypatch.setattr(mysql, "MySQLSandbox", lambda _: sandbox)

    def config(*args, **kwargs):
        order.append(("config", kwargs.get("offer_profile")))
        return {"profile": kwargs.get("offer_profile", "baseline")}

    def seed(*args, **kwargs):
        order.append(("seed", kwargs.get("journey_profile")))
        return {"name": "catalogo-comercial-v1", "reference_date": "2026-09-22"}

    monkeypatch.setattr(runner, "prepare_app_config", config)
    monkeypatch.setattr(engine, "apply_seed", seed)
    codes = {}

    def execute(root, directory, selected, **kwargs):
        context = kwargs.get("profile_context")
        order.append(("robot", context["variant"] if context else None, tuple(row["id"] for row in selected)))
        assert kwargs["seed_context"]["status"] == "seed-applied" or kwargs["dry_run"]
        variant = context["variant"] if context else None
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "console.log").write_text("PRIVATE-CANARY", encoding="utf-8")
        rows = [outcome(row["id"], codes.get(variant, 0))["case_results"][0] for row in selected]
        if kwargs["dry_run"]:
            for row in rows:
                row["status"] = "validated-only"
        return {"code": codes.get(variant, 0), "case_results": rows, "total": len(rows),
                "failed": sum(row["status"] == "failed" for row in rows), "skipped": 0}

    monkeypatch.setattr(runner, "execute_robot", execute)
    return tmp_path, order, codes


def latest(root):
    record = json.loads((root / "reports/latest.json").read_text(encoding="utf-8"))
    directory = root / "reports" / record["directory"]
    return directory, json.loads((directory / "summary.json").read_text(encoding="utf-8"))


def test_mixed_selection_restores_each_profile_and_keeps_one_result_per_id(prepared):
    root, order, _ = prepared
    assert runner.run(root, "xgestion") == 0
    executions = [item for item in order if item[0] == "robot"]
    assert len(executions) == 8
    assert executions[0] == ("robot", None, ("XG-PRM-001",))
    assert [item[1] for item in executions[1:]] == [
        "active", "inactive", "active-again", "general-off", "offers-off",
        "allowed-warning-on", "allowed-warning-off",
    ]
    for index, entry in enumerate(order):
        if entry[0] != "robot" or entry[1] is None:
            continue
        since_previous = order[max(i for i in range(index) if order[i][0] == "restore"):index]
        assert any(item[0] == "seed" and item[1] == (entry[2][0], entry[1]) for item in since_previous)
        assert any(item[0] == "config" for item in since_previous)
    assert order[-1] == ("config", None) or order[-1] == ("stop",)
    directory, summary = latest(root)
    assert summary["counts"] == {"passed": 3} and summary["total"] == 3
    assert len(summary["case_results"]) == len(set(summary["cases"])) == 3
    assert [len(row.get("phases", [])) for row in summary["case_results"]] == [0, 3, 4]
    report = (directory / "report.html").read_text(encoding="utf-8")
    assert "cases/XG-PRM-070/inactive/report.html" in report
    assert "cases/standard/report.html" in report
    assert "PRIVATE-CANARY" not in "".join(path.read_text(encoding="utf-8") for path in directory.rglob("*.log"))
    assert not (root / ".local/run.lock").exists()


@pytest.mark.parametrize("code,status", [(1, "failed"), (2, "blocked"), (130, "cancelled")])
def test_profile_failure_preserves_status_and_stops_unsafe_continuation(prepared, code, status):
    root, order, codes = prepared
    codes["inactive"] = code
    assert runner.run(root, "xgestion") == code
    _, summary = latest(root)
    assert summary["case_results"][1]["status"] == status
    if code != 1:
        assert summary["case_results"][2]["status"] == status
        assert len([item for item in order if item[0] == "robot"]) == 3
        assert all(not phase["executed"] for phase in summary["case_results"][2]["phases"])
    assert ("stop",) in order


def test_dry_run_does_not_expand_profiles_or_prepare_runtime(prepared):
    root, order, _ = prepared
    assert runner.run(root, "xgestion", dry_run=True) == 0
    assert [item[0] for item in order] == ["robot"]
    _, summary = latest(root)
    assert summary["counts"] == {"validated-only": 3}
    assert not any(row.get("phases") for row in summary["case_results"])


def test_ordinary_block_omits_all_profiles_without_another_restore(prepared):
    root, order, codes = prepared
    codes[None] = 2
    assert runner.run(root, "xgestion") == 2
    assert len([item for item in order if item[0] == "restore"]) == 1
    _, summary = latest(root)
    assert summary["counts"] == {"blocked": 3}
    assert all(not phase["executed"] for row in summary["case_results"][1:] for phase in row["phases"])


def test_profile_seed_failure_keeps_sanitized_diagnostics_and_stops(prepared, monkeypatch):
    from framework.errors import QAError

    root, order, _ = prepared
    original = engine.apply_seed

    def fail_profile(*args, **kwargs):
        if kwargs.get("journey_profile") == ("XG-PRM-070", "inactive"):
            raise QAError("Colisión de fixture PRIVATE-CANARY")
        return original(*args, **kwargs)

    monkeypatch.setattr(engine, "apply_seed", fail_profile)
    assert runner.run(root, "xgestion") == 2
    assert len([item for item in order if item[0] == "robot"]) == 2
    directory, summary = latest(root)
    assert summary["counts"] == {"passed": 1, "blocked": 2}
    log = (directory / "cases/XG-PRM-070/inactive/console.log").read_text(encoding="utf-8")
    assert "Colisión de fixture" in log and "PRIVATE-CANARY" not in log
    assert ("stop",) in order


def test_cleanup_config_failure_cannot_leave_global_success(prepared, monkeypatch):
    from framework.errors import QAError

    root, order, _ = prepared
    original = runner.prepare_app_config

    def cleanup(*args, **kwargs):
        if not kwargs:
            raise QAError("No se pudo restaurar configuración PRIVATE-CANARY")
        return original(*args, **kwargs)

    monkeypatch.setattr(runner, "prepare_app_config", cleanup)
    assert runner.run(root, "xgestion") == 2
    directory, summary = latest(root)
    assert summary["status"] == "blocked"
    assert "PRIVATE-CANARY" not in json.dumps(summary)
    assert "BLOQUEADO" in (directory / "report.html").read_text(encoding="utf-8")
    assert ("stop",) in order


def test_failed_phase_html_never_leaves_a_passed_child_summary(prepared, monkeypatch):
    root, _, _ = prepared
    original = runner.write_run_report

    def report(directory, payload):
        if directory.name == "active":
            (directory / "report.html").write_text("partial success", encoding="utf-8")
            raise OSError("PRIVATE-CANARY")
        return original(directory, payload)

    monkeypatch.setattr(runner, "write_run_report", report)
    assert runner.run(root, "xgestion") == 2
    directory, summary = latest(root)
    assert summary["case_results"][1]["status"] == "blocked"
    child = directory / "cases/XG-PRM-070/active"
    assert not (child / "report.html").exists()
    detail = json.loads((child / "summary.json").read_text(encoding="utf-8"))
    assert detail["status"] == "blocked" and detail["exit_code"] == 2
    assert detail["case_results"][0]["status"] == "blocked"
    assert "PRIVATE-CANARY" not in repr(detail)


def test_real_robot_profile_chain_preserves_events_xml_and_sanitized_html(prepared, monkeypatch):
    from test_reporting import html_result_strings

    root, _, _ = prepared
    monkeypatch.setattr(runner, "execute_robot", REAL_EXECUTE_ROBOT)
    suite = root / "products/xgestion/suites/synthetic.robot"
    suite.parent.mkdir(parents=True)
    library = root / "SyntheticProfiles.py"
    library.write_text(
        "import json, os\nfrom framework.events import assertion_failed\n"
        "def check_profile(case_id):\n"
        "    variant = os.environ['XSOFT_QA_OFFER_VARIANT']\n"
        "    assert json.loads(os.environ['XSOFT_QA_OFFER_PROFILE']) == "
        "{'case_id': case_id, 'variant': variant}\n"
        "    if variant == 'inactive':\n"
        "        assertion_failed('Total distinto', expected=2000, observed=1000)\n"
        "        raise AssertionError('Total distinto')\n",
        encoding="utf-8",
    )
    suite.write_text(
        f"*** Settings ***\nLibrary    {library.as_posix()}\n*** Test Cases ***\n"
        "Normal\n    [Tags]    XG-PRM-001    promociones\n    Log    PRIVATE-CANARY\n"
        "Vigencia\n    [Tags]    XG-PRM-070    promociones\n"
        "    Log    PRIVATE-CANARY\n    Check Profile    XG-PRM-070\n"
        "Permisos\n    [Tags]    XG-PRM-079    promociones\n"
        "    Log    PRIVATE-CANARY\n    Check Profile    XG-PRM-079\n",
        encoding="utf-8",
    )
    assert runner.run(root, "xgestion", log_level="TRACE") == 1
    directory, summary = latest(root)
    assert summary["counts"] == {"passed": 2, "failed": 1}
    assert summary["case_results"][1]["failure"]["expected"] == 2000
    events = [json.loads(line) for line in (directory / "events.jsonl").read_text(encoding="utf-8").splitlines()]
    assert sorted(event["case_id"] for event in events if event["event"] == "case_end") == sorted(summary["cases"])
    outputs = list(directory.rglob("output.xml"))
    assert len(outputs) == 8 and not (directory / "output.xml").exists()
    for output in outputs:
        assert "PRIVATE-CANARY" not in output.read_text(encoding="utf-8")
        assert not any("PRIVATE-CANARY" in item for item in html_result_strings(output.with_name("log.html")))
