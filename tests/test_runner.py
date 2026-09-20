import json
from pathlib import Path

import pytest

from framework.catalog import load_catalog, select_cases, validate_catalog
from framework.errors import QAError
from framework.reporting import redact, sanitize_artifacts
from framework.runner import RunLock, exit_status


def case(root: Path, *, case_id="XG-INI-001", test_id=None):
    scenario = root / "products/xgestion/scenarios/inicio.md"
    scenario.parent.mkdir(parents=True)
    suite = root / "products/xgestion/suites/inicio.robot"
    suite.parent.mkdir(parents=True)
    metadata = {"id": case_id, "title": "Inicio", "product": "xgestion", "module": "inicio",
                "tags": ["smoke"], "status": "implemented", "test": "products/xgestion/suites/inicio.robot"}
    scenario.write_text("---\n" + json.dumps(metadata) + "\n---\n# Inicio\n", encoding="utf-8")
    suite.write_text(f"*** Test Cases ***\nInicio\n    [Tags]    {test_id or case_id}    smoke\n    No Operation\n", encoding="utf-8")
    return metadata


def test_catalog_matches_documentation_to_real_robot_tags(tmp_path):
    case(tmp_path)
    validate_catalog(tmp_path)
    assert select_cases(load_catalog(tmp_path), "xgestion", "smoke", None)[0]["id"] == "XG-INI-001"


def test_undocumented_test_is_error(tmp_path):
    case(tmp_path, test_id="XG-INI-999")
    with pytest.raises(QAError):
        validate_catalog(tmp_path)


def test_empty_selection_is_not_success(tmp_path):
    case(tmp_path)
    with pytest.raises(QAError):
        select_cases(load_catalog(tmp_path), "xgestion", "unknown", None)


def test_planned_product_cannot_run(tmp_path):
    with pytest.raises(QAError, match="pendiente"):
        select_cases([], "mozos", None, None)


def test_concurrent_run_rejected_and_lock_released(tmp_path):
    with RunLock(tmp_path):
        with pytest.raises(QAError):
            with RunLock(tmp_path):
                pytest.fail("No debe entrar una segunda ejecución")
    with RunLock(tmp_path):
        pass


def test_canary_is_redacted_in_plain_xml_json_and_url():
    secret = 'canary<&"PASSWORD'
    from html import escape
    from urllib.parse import quote
    representations = [secret, escape(secret), json.dumps(secret)[1:-1], quote(secret, safe="")]
    for value in representations:
        assert "canary" not in redact(value, [secret])


def test_all_text_reports_are_sanitized(tmp_path):
    for suffix in ("html", "xml", "json", "log", "txt"):
        (tmp_path / f"report.{suffix}").write_text("secret-CANARY", encoding="utf-8")
    sanitize_artifacts(tmp_path, ["secret-CANARY"])
    assert all("CANARY" not in p.read_text(encoding="utf-8") for p in tmp_path.iterdir())


@pytest.mark.parametrize("code,total,failed,skipped,expected", [
    (0, 2, 0, 0, 0), (1, 2, 1, 0, 1), (0, 0, 0, 0, 2),
    (0, 2, 0, 2, 2), (252, 0, 0, 0, 2), (0, 2, 0, 1, 2),
])
def test_no_tests_or_skips_cannot_report_success(code, total, failed, skipped, expected):
    assert exit_status(code, total, failed, skipped) == expected
