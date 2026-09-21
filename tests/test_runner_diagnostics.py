import json
import threading

import pytest

from framework import runner
from framework.reporting import build_robot_reports, safe_value, write_run_report, write_summary


def suite(root, body, *, library=None):
    location = root / "products/xgestion/suites"
    location.mkdir(parents=True)
    settings = f"*** Settings ***\nLibrary    {library.as_posix()}\n" if library else ""
    (location / "synthetic.robot").write_text(
        settings + "*** Test Cases ***\nCaso sintético\n    [Tags]    XG-VEN-001    ventas\n" + body,
        encoding="utf-8",
    )
    return [{"id": "XG-VEN-001", "title": "Caso sintético", "tags": ["ventas"],
             "product": "xgestion", "status": "implemented"}]


def execute(root, cases, **options):
    directory = root / "report"
    directory.mkdir(exist_ok=True)
    result = runner.execute_robot(root, directory, cases, dry_run=False, secrets=[], log_level="INFO",
                                  groups=[], **options)
    return directory, result


def test_progress_arrives_before_robot_finishes_and_raw_console_is_not_emitted(tmp_path):
    cases = suite(tmp_path, "    Log To Console    RAW-PRIVATE-CANARY\n    Sleep    1.2s\n")
    started, finished = threading.Event(), threading.Event()
    messages, outcomes = [], []

    def output(message):
        messages.append(message)
        if "Inicia:" in message:
            started.set()

    def background():
        try:
            outcomes.append(execute(tmp_path, cases, emit=output))
        finally:
            finished.set()

    thread = threading.Thread(target=background)
    thread.start()
    assert started.wait(45), "Debe transmitir progreso de un Robot real"
    assert not finished.is_set(), "El progreso debe llegar antes de terminar el proceso"
    thread.join(timeout=45)
    assert not thread.is_alive()
    directory, result = outcomes[0]
    assert result["code"] == 0
    assert result["case_results"][0]["status"] == "passed"
    assert not any("RAW-PRIVATE-CANARY" in message for message in messages)
    assert "RAW-PRIVATE-CANARY" not in (directory / "console.log").read_text(encoding="utf-8")


@pytest.mark.parametrize("kind,expected_code,category", [
    ("assertion", 1, "functional_assertion"), ("blocked", 2, "environment_block"),
])
def test_real_robot_failure_has_enriched_case_summary(tmp_path, kind, expected_code, category):
    library = tmp_path / "SyntheticChecks.py"
    library.write_text(
        "from framework.events import assertion_failed\nfrom framework.errors import QAError\n"
        "def verify_result():\n" + (
            "    assertion_failed('Cantidad distinta', expected='2', observed='1')\n"
            "    raise AssertionError('Cantidad distinta')\n" if kind == "assertion" else
            "    raise QAError('No hay escritorio de QA disponible')\n"), encoding="utf-8",
    )
    directory, result = execute(tmp_path, suite(tmp_path, "    Verify Result\n", library=library))
    assert result["code"] == expected_code
    failure = result["case_results"][0]["failure"]
    assert failure["category"] == category
    assert failure["step"] == "Verify Result"
    assert failure["cause"] == "No determinada"
    assert failure["evidence"]
    build_robot_reports(directory, [])
    assert (directory / "log.html").is_file()


def test_timeout_marks_incomplete_case_blocked_not_passed(tmp_path):
    _, result = execute(tmp_path, suite(tmp_path, "    Sleep    8s\n"), timeout=1)
    assert result["code"] == 2
    assert result["case_results"][0]["status"] == "blocked"
    assert result["case_results"][0]["failure"]["category"] == "timeout"


def test_cancellation_is_recorded_for_every_selected_case(tmp_path, monkeypatch):
    from framework import processes

    def cancel(*args, **kwargs):
        raise KeyboardInterrupt

    monkeypatch.setattr(processes, "run_owned_process", cancel)
    _, result = execute(tmp_path, suite(tmp_path, "    No Operation\n"))
    assert result["code"] == 130
    assert result["case_results"][0]["status"] == "cancelled"


def test_missing_output_or_listener_never_passes(tmp_path, monkeypatch):
    from subprocess import CompletedProcess

    from framework import processes

    monkeypatch.setattr(processes, "run_owned_process", lambda *a, **k: CompletedProcess([], 0, b"", b""))
    _, result = execute(tmp_path, suite(tmp_path, "    No Operation\n"))
    assert result["code"] == 2
    assert result["case_results"][0]["failure"]["category"] == "evidence_incomplete"


def test_group_summary_is_additive_and_preserves_registry_titles():
    groups = [{"id": "ventas", "title": "Venta de mostrador", "description": "Cobrar productos", "stage": 1}]
    cases = [{"id": "XG-VEN-001", "tags": ["ventas"]}, {"id": "XG-VEN-002", "tags": ["ventas"]}]
    results = [{"id": "XG-VEN-001", "status": "passed"}, {"id": "XG-VEN-002", "status": "blocked"}]
    summary = runner.summarize_groups(groups, cases, results)
    assert summary[0]["title"] == "Venta de mostrador"
    assert summary[0]["counts"] == {"passed": 1, "blocked": 1}
    assert summary[0]["selected"] == 2


def test_all_selected_cases_get_results_when_preflight_blocks(tmp_path, monkeypatch):
    from framework.errors import QAError

    cases = suite(tmp_path, "    No Operation\n")
    monkeypatch.setattr(runner, "validate_catalog", lambda root: cases)
    monkeypatch.setattr(runner, "load_profile", lambda root: (_ for _ in ()).throw(QAError("Paquete no instalado")))
    monkeypatch.setattr(runner, "_groups_for_run", lambda *a: [])
    assert runner.run(tmp_path, "xgestion") == 2
    latest = json.loads((tmp_path / "reports/latest.json").read_text(encoding="utf-8"))
    summary = json.loads((tmp_path / "reports" / latest["directory"] / "summary.json").read_text(encoding="utf-8"))
    assert summary["cases"] == ["XG-VEN-001"]
    assert summary["case_results"][0]["status"] == "blocked"
    assert summary["case_results"][0]["failure"]["category"] == "environment_block"


@pytest.mark.parametrize("level,shows_step,shows_trace", [("INFO", False, False), ("DEBUG", True, False),
                                                       ("TRACE", True, True)])
def test_real_robot_levels_keep_failure_detail_and_redact_full_report_chain(tmp_path, level, shows_step, shows_trace):
    secret = "SYNTHETIC_CANARY_98a1"
    library = tmp_path / "DiagnosticLevels.py"
    library.write_text(
        "from framework.events import business_step, diagnostic, assertion_failed\n"
        "def verify_result():\n"
        "    business_step('Comprobar el total antes de cobrar')\n"
        "    diagnostic('Lectura técnica', duration_seconds=0.1, password='UNKNOWN_CREDENTIAL')\n"
        f"    assertion_failed('Total distinto {secret}', expected='2', observed='1 {secret}')\n"
        f"    raise AssertionError('Total distinto {secret}')\n", encoding="utf-8",
    )
    cases = suite(tmp_path, "    Verify Result\n", library=library)
    directory = tmp_path / "report"
    directory.mkdir()
    groups = [{"id": "ventas", "title": "Venta de mostrador", "description": "Cobrar productos", "stage": 1}]
    messages = []
    result = runner.execute_robot(tmp_path, directory, cases, dry_run=False, secrets=[secret], log_level=level,
                                  groups=groups, emit=messages.append)
    assert result["code"] == 1
    assert any("[DEBUG]" in message for message in messages) is shows_step
    assert any("Lectura técnica" in message for message in messages) is shows_trace
    failure = result["case_results"][0]["failure"]
    assert failure["step"] == "Comprobar el total antes de cobrar"
    assert any("Esperado: 2" in message and "Observado: 1" in message for message in messages)
    payload = safe_value({"status": "failed", "mode": "e2e", "case_results": result["case_results"],
                          "groups": runner.summarize_groups(groups, cases, result["case_results"])}, [secret])
    build_robot_reports(directory, [secret])
    write_summary(directory, cases=[cases[0]["id"]], code=1, **payload)
    write_run_report(directory, payload)
    for name in ("events.jsonl", "console.log", "output.xml", "summary.json", "report.html"):
        content = (directory / name).read_text(encoding="utf-8")
        assert secret not in content
        assert "UNKNOWN_CREDENTIAL" not in content
    from robot.api import ExecutionResult

    metadata = ExecutionResult(str(directory / "output.xml")).suite.metadata
    assert metadata["Grupo ventas"] == "Venta de mostrador (ventas): Cobrar productos"


def test_listener_boot_failure_keeps_bounded_sanitized_diagnostic(tmp_path, monkeypatch):
    from subprocess import CompletedProcess

    from framework import processes

    monkeypatch.setattr(processes, "run_owned_process", lambda *a, **k: CompletedProcess(
        [], 252, b"RAW-CONSOLE", b"Listener import failed: password=UNKNOWN_CANARY " + b"X" * 4000))
    directory, result = execute(tmp_path, suite(tmp_path, "    No Operation\n"))
    console = (directory / "console.log").read_text(encoding="utf-8")
    assert result["code"] == 2
    assert "Listener import failed" in console
    assert "UNKNOWN_CANARY" not in console
    assert "RAW-CONSOLE" not in console
    assert len(console) < 3000


def test_event_stream_does_not_repeat_parent_preparation(tmp_path):
    from framework.events import EventStream, EventWriter

    writer = EventWriter(tmp_path / "events.jsonl", secrets=[])
    writer.emit("INFO", "preflight", "Preparación ya mostrada")
    messages = []
    with EventStream(writer.path, level="INFO", secrets=[], emit=messages.append):
        writer.emit("INFO", "case_start", "Nuevo caso")
    assert len(messages) == 1
    assert "Nuevo caso" in messages[0]


def test_cleanup_error_after_finished_cases_remains_visible_and_blocks_official_report(tmp_path, monkeypatch, capsys):
    from framework.errors import QAError

    cases = suite(tmp_path, "    No Operation\n")
    monkeypatch.setattr(runner, "validate_catalog", lambda root: cases)
    monkeypatch.setattr(runner, "_groups_for_run", lambda *a: [
        {"id": "ventas", "title": "Venta de mostrador", "description": "Cobrar productos", "stage": 1}])
    monkeypatch.setattr(runner, "execute_robot", lambda *a, **k: {
        "code": 0, "case_results": [{"id": "XG-VEN-001", "title": "Caso sintético", "status": "validated-only"}]})

    def cleanup_failure(self, *args):
        self.path.unlink(missing_ok=True)
        raise QAError("No se pudo completar la limpieza sintética")

    monkeypatch.setattr(runner.RunLock, "__exit__", cleanup_failure)
    assert runner.run(tmp_path, "xgestion", group="ventas", dry_run=True) == 2
    console = capsys.readouterr().out
    assert "Grupo: Venta de mostrador (ventas). Casos: 1" in console
    assert "No se pudo completar la limpieza sintética" in console
    latest = json.loads((tmp_path / "reports/latest.json").read_text(encoding="utf-8"))
    directory = tmp_path / "reports" / latest["directory"]
    summary = json.loads((directory / "summary.json").read_text(encoding="utf-8"))
    assert summary["status"] == "blocked"
    assert "No se pudo completar la limpieza sintética" in summary["reason"]
    assert "BLOQUEADO" in (directory / "report.html").read_text(encoding="utf-8")
    assert summary["elapsed_seconds"] >= 0
