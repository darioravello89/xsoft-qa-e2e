"""Regresiones con XML/HTML reales de Robot, incluidos mensajes comprimidos."""

import base64
import io
import json
import re
import zlib
from xml.etree import ElementTree

import pytest
from robot import rebot
from robot.api import ExecutionResult
from robot.api import TestSuite as RobotSuite

from framework.errors import QAError
from framework.reporting import build_robot_reports, sanitize_artifacts


def robot_run(directory, message, *, html=True):
    suite = RobotSuite("QA reporting regression")
    case = suite.tests.create("Preservar evidencia sin secretos")
    case.body.create_keyword("Log", args=[message])
    result = suite.run(
        outputdir=str(directory), output="output.xml",
        log="log.html" if html else "NONE", report="report.html" if html else "NONE",
        stdout=io.StringIO(), stderr=io.StringIO(),
    )
    if html:
        rebot(str(directory / "output.xml"), outputdir=str(directory), output="NONE",
              log="log.html", report="report.html", stdout=io.StringIO(), stderr=io.StringIO())
    return result


def html_result_strings(path):
    document = path.read_text(encoding="utf-8")
    blocks = re.findall(
        r'window\.output\["strings"\] = window\.output\["strings"\]\.concat\((.*?)\);',
        document, flags=re.DOTALL,
    )
    assert blocks, "El reporte real debe contener el modelo de resultados de Robot"
    strings = []
    for block in blocks:
        for value in json.loads(block.replace("\\x3c", "\\u003c")):
            strings.append(value[1:] if value.startswith("*") else
                           zlib.decompress(base64.b64decode(value)).decode("utf-8"))
    return strings


def test_real_compressed_robot_report_does_not_retain_canary(tmp_path):
    canary = "QA_ONLY_SYNTHETIC_CANARY_5cb762"
    message = "A" * 250 + canary + "B" * 250
    assert robot_run(tmp_path, message).return_code == 0
    assert any(canary in value for value in html_result_strings(tmp_path / "log.html"))
    build_robot_reports(tmp_path, [canary])
    assert all(canary not in value for value in html_result_strings(tmp_path / "log.html"))
    assert all(canary not in value for value in html_result_strings(tmp_path / "report.html"))
    assert canary not in (tmp_path / "output.xml").read_text(encoding="utf-8")


def test_secret_matching_xml_tag_does_not_damage_output_schema(tmp_path):
    assert robot_run(tmp_path, "robot", html=False).return_code == 0
    sanitize_artifacts(tmp_path, ["robot"])
    tree = ElementTree.parse(tmp_path / "output.xml")
    assert tree.getroot().tag == "robot"
    assert any("[REDACTADO]" in (node.text or "") for node in tree.iter("msg"))


def test_missing_robot_output_does_not_fabricate_html(tmp_path):
    (tmp_path / "console.log").write_text("synthetic-secret", encoding="utf-8")
    build_robot_reports(tmp_path, ["synthetic-secret"])
    assert not (tmp_path / "report.html").exists()
    assert (tmp_path / "console.log").read_text(encoding="utf-8") == "[REDACTADO]"


def test_failed_case_still_produces_report(tmp_path):
    suite = RobotSuite("QA failure report")
    suite.tests.create("Fallo real del caso").body.create_keyword("Fail", args=["assertion-synthetic"])
    result = suite.run(outputdir=str(tmp_path), output="output.xml", log="NONE", report="NONE",
                       stdout=io.StringIO(), stderr=io.StringIO())
    assert result.return_code == 1
    build_robot_reports(tmp_path, [])
    assert (tmp_path / "report.html").is_file()
    assert any("assertion-synthetic" in value for value in html_result_strings(tmp_path / "log.html"))


def test_truncated_output_rejects_report_and_removes_stale_html(tmp_path):
    (tmp_path / "output.xml").write_text("<robot><msg>secret-synthetic", encoding="utf-8")
    (tmp_path / "log.html").write_text("old unsafe html", encoding="utf-8")
    with pytest.raises(QAError):
        build_robot_reports(tmp_path, ["secret-synthetic"])
    assert not (tmp_path / "log.html").exists()
    assert "secret-synthetic" not in (tmp_path / "output.xml").read_text(encoding="utf-8")


def test_secret_equal_to_result_status_keeps_robot_statistics_valid(tmp_path):
    assert robot_run(tmp_path, "PASS", html=False).return_code == 0
    build_robot_reports(tmp_path, ["PASS"])
    result = ExecutionResult(str(tmp_path / "output.xml"))
    assert result.statistics.total.passed == 1
    assert result.suite.tests[0].body[0].messages[0].message == "[REDACTADO]"


def test_resanitizing_events_and_summary_preserves_machine_contract(tmp_path):
    payload = {"event": "case_end", "status": "passed", "id": "XG-VEN-001", "message": "case secret-status"}
    (tmp_path / "events.jsonl").write_text(json.dumps(payload) + "\n", encoding="utf-8")
    (tmp_path / "summary.json").write_text(json.dumps(payload), encoding="utf-8")
    build_robot_reports(tmp_path, ["case", "passed", "status", "XG-VEN-001"])
    for name in ("events.jsonl", "summary.json"):
        result = json.loads((tmp_path / name).read_text(encoding="utf-8"))
        assert result["event"] == "case_end"
        assert result["status"] == "passed"
        assert result["id"] == "XG-VEN-001"
        assert "case" not in result["message"]


def test_official_run_report_marks_global_block_even_if_robot_passed(tmp_path):
    from framework.reporting import write_run_report

    assert robot_run(tmp_path, "Caso sintético aprobado").return_code == 0
    payload = {"status": "blocked", "mode": "e2e", "elapsed_seconds": 1,
               "case_results": [{"id": "XG-VEN-001", "title": "Caso", "status": "passed"}],
               "groups": [], "reason": "Falta evidencia de finalización <unsafe>"}
    write_run_report(tmp_path, payload)
    document = (tmp_path / "report.html").read_text(encoding="utf-8")
    assert "BLOQUEADO" in document
    assert "no acredita" in document
    assert "&lt;unsafe&gt;" in document
    assert (tmp_path / "robot-report.html").is_file()


def test_sanitizing_summary_does_not_truncate_large_selected_catalog(tmp_path):
    payload = {"case_results": [{"id": f"XG-VEN-{index:03}", "status": "passed"} for index in range(125)]}
    (tmp_path / "summary.json").write_text(json.dumps(payload), encoding="utf-8")
    build_robot_reports(tmp_path, ["passed"])
    result = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))
    assert result == payload


@pytest.mark.parametrize("status", ["seed-applied", "preview-only"])
def test_seed_status_remains_structural_when_a_secret_matches_it(tmp_path, status):
    payload = {"seed": {"status": status, "message": f"Valor privado {status}"}}
    (tmp_path / "summary.json").write_text(json.dumps(payload), encoding="utf-8")
    build_robot_reports(tmp_path, [status])
    result = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))
    assert result["seed"]["status"] == status
    assert result["seed"]["message"] == "Valor privado [REDACTADO]"
