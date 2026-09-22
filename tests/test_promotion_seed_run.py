"""El seed requerido por el caso tiene el mismo recorrido desde menú, grupo o ID."""

import json
from unittest.mock import Mock

import pytest
from test_groups_cli import make_catalog
from test_seed_command import prepared_apply

from framework import runner
from framework.fixtures import mysql
from products.xgestion.seeds import engine

NAME = "catalogo-comercial-v1"


@pytest.fixture
def required_catalog(tmp_path):
    make_catalog(tmp_path)
    path = next((tmp_path / "products").glob("*/scenarios/**/*.md"))
    content = path.read_text(encoding="utf-8")
    case = json.loads(content.split("---", 2)[1])
    case["seed"] = NAME
    path.write_text("---\n" + json.dumps(case) + "\n---\n", encoding="utf-8")
    return tmp_path, case["id"]


@pytest.mark.parametrize("selection", ["group", "scenario", "all", "inspect"])
def test_required_seed_is_prepared_before_robot_with_no_explicit_flag(required_catalog, monkeypatch, selection):
    root, case_id = required_catalog
    prepared = Mock()
    prepared.apply_seed.return_value = {"name": NAME, "reference_date": "2026-09-22"}
    order, server, profile = prepared_apply(root, monkeypatch, prepared)
    profile.manifest["files"].update({name: {"sha256": "b" * 64} for name in ("app", "fixtures", "locators")})
    monkeypatch.setattr(runner, "load_profile", lambda *_: profile)
    monkeypatch.setattr(runner, "doctor", lambda *a, **k: None)
    monkeypatch.setattr(runner, "prepare_app_config", lambda *_: None)
    monkeypatch.setattr(runner, "ensure_offline", lambda: None)
    monkeypatch.setattr(mysql, "MySQLSandbox", lambda *_: server)
    monkeypatch.setattr(runner, "build_robot_reports", lambda *_: None)
    monkeypatch.setattr(runner, "version", lambda _: "test")
    monkeypatch.setattr(engine, "apply_seed", prepared.apply_seed)

    def execute(*args, **kwargs):
        order.append("robot")
        assert kwargs["seed_context"] == {"name": NAME, "reference_date": "2026-09-22", "status": "seed-applied"}
        return {"code": 0, "case_results": [{"id": case_id, "title": "Venta", "status": "passed"}]}

    monkeypatch.setattr(runner, "execute_robot", execute)
    if selection == "inspect":
        from products.xgestion import inspection
        monkeypatch.setattr(inspection, "inspect_login", lambda *a: order.append("inspect"))
    args = {"group": "ventas"} if selection == "group" else {"scenario": case_id} if selection == "scenario" else {}
    if selection == "inspect":
        args["inspect"] = True
    assert runner.run(root, "xgestion", **args) == 0
    if selection == "inspect":
        assert "inspect" in order and "robot" not in order
        prepared.apply_seed.assert_not_called()
        return
    assert order.index("restore") < order.index("apply") < order.index("robot") < order.index("stop")
    payload = json.loads(next((root / "reports").glob("*/summary.json")).read_text(encoding="utf-8"))
    assert payload["seed"]["status"] == "seed-applied"


def test_required_seed_dry_run_never_reads_private_profile(required_catalog, monkeypatch):
    root, case_id = required_catalog
    monkeypatch.setattr(runner, "load_profile", Mock(side_effect=AssertionError("no perfil")))
    monkeypatch.setattr(runner, "build_robot_reports", lambda *_: None)
    monkeypatch.setattr(runner, "execute_robot", lambda *a, **k: {
        "code": 0, "case_results": [{"id": case_id, "title": "Venta", "status": "validated-only"}]})
    monkeypatch.setattr(engine, "apply_seed", Mock(side_effect=AssertionError("no DB")))
    assert runner.run(root, "xgestion", dry_run=True) == 0
    payload = json.loads(next((root / "reports").glob("*/summary.json")).read_text(encoding="utf-8"))
    assert payload["seed"]["status"] == "preview-only"


@pytest.mark.parametrize("status,dry_run,expected", [("seed-applied", False, NAME),
                                                   ("preview-only", False, ""),
                                                   ("seed-applied", True, ""), (None, False, "")])
def test_seed_receipt_never_inherits_another_run(tmp_path, monkeypatch, status, dry_run, expected):
    from framework import processes

    received = {}

    def capture(*args, **kwargs):
        received.update(kwargs["env"])
        raise KeyboardInterrupt

    monkeypatch.setenv("XSOFT_QA_SEED", "APPROVAL-FROM-OLD-RUN")
    monkeypatch.setenv("XSOFT_QA_SEED_DATE", "1999-01-01")
    monkeypatch.setattr(processes, "run_owned_process", capture)
    cases = [{"id": "XG-PRM-001", "title": "Promoción", "tags": ["promociones"]}]
    result = runner.execute_robot(tmp_path, tmp_path, cases, dry_run=dry_run, secrets=[], log_level="INFO",
                                  groups=[], seed_context={"status": status, "name": NAME,
                                                           "reference_date": "2026-09-22"} if status else None)
    assert received["XSOFT_QA_SEED"] == expected
    assert received["XSOFT_QA_SEED_DATE"] == ("2026-09-22" if expected else "")
    assert result["code"] == 130
