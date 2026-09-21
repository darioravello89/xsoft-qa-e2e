import json

from framework.events import EventWriter, assertion_failed, diagnostic
from framework.robot_listener import QAListener


def test_event_is_sanitized_before_file_write_and_does_not_stringify_objects(tmp_path):
    class PrivateObject:
        def __str__(self):
            raise AssertionError("No debe serializar objetos arbitrarios")

    writer = EventWriter(tmp_path / "events.jsonl", secrets=["synthetic<&canary"])
    writer.emit("TRACE", "diagnostic", "Dato synthetic<&canary\x1b[31m", password="unknown-private",
                url="https://user:unknown-private@example.test/?token=unknown-token",
                detail=PrivateObject())
    raw = writer.path.read_text(encoding="utf-8")
    assert "synthetic" not in raw
    assert "unknown-private" not in raw
    assert "unknown-token" not in raw
    assert "\\u001b" not in raw
    event = json.loads(raw)
    assert event["password"] == "[REDACTADO]"
    assert event["detail"] == "[DATO OMITIDO]"


def test_product_diagnostics_are_safe_noops_without_listener():
    diagnostic("Fuera de Robot", count=2)
    assertion_failed("Fuera de Robot", expected=2, observed=1)


def test_success_clears_transient_assertion_without_publishing_failure(tmp_path):
    from robot.api import TestSuite as RobotSuite

    library = tmp_path / "RetryLibrary.py"
    library.write_text(
        "from framework.events import assertion_failed, diagnostic\n"
        "def successful_retry():\n"
        "    assertion_failed('Valor transitorio', expected=2, observed=1)\n"
        "    diagnostic('Reintento completado', attempts=2)\n",
        encoding="utf-8",
    )
    suite = RobotSuite("Retry")
    suite.resource.imports.library(library.as_posix())
    test = suite.tests.create("Recupera", tags=["XG-VEN-001"])
    test.body.create_keyword("Successful Retry")
    listener = QAListener(tmp_path, secrets=[])
    result = suite.run(output=None, log=None, report=None, console="none", listener=listener)
    events = [json.loads(line) for line in listener.writer.path.read_text(encoding="utf-8").splitlines()]
    assert result.return_code == 0, result.suite.tests[0].message
    assert not any(event["event"] == "failure" for event in events)
    assert events[-1]["event"] == "listener_closed"
    ended = next(event for event in events if event["event"] == "case_end")
    assert ended["status"] == "passed"
    assert "failure" not in ended


def test_real_failure_has_business_step_expected_observed_and_no_stale_context(tmp_path):
    from robot.api import TestSuite as RobotSuite

    library = tmp_path / "AssertionLibrary.py"
    library.write_text(
        "from framework.events import assertion_failed\n"
        "def verify_stock():\n"
        "    assertion_failed('Stock incorrecto', expected=8, observed=9)\n"
        "    raise AssertionError('Stock incorrecto')\n",
        encoding="utf-8",
    )
    suite = RobotSuite("Assertions")
    suite.resource.imports.library(library.as_posix())
    suite.tests.create("Falla", tags=["XG-VEN-001"]).body.create_keyword("Verify Stock")
    suite.tests.create("Otro fallo", tags=["XG-VEN-002"]).body.create_keyword("Fail", args=["Otro problema"])
    listener = QAListener(tmp_path, secrets=[])
    suite.run(output=None, log=None, report=None, console="none", listener=listener)
    events = [json.loads(line) for line in listener.writer.path.read_text(encoding="utf-8").splitlines()]
    failures = [event["failure"] for event in events if event["event"] == "case_end"]
    assert failures[0]["step"] == "Verify Stock"
    assert failures[0]["expected"] == 8, failures[0]
    assert failures[0]["observed"] == 9
    assert failures[0]["category"] == "functional_assertion"
    assert failures[0]["cause"] == "No determinada"
    assert failures[1]["observed"] == "Otro problema"


def test_standard_robot_assertion_is_functional_and_caught_failure_is_not_reused(tmp_path):
    from robot.api import TestSuiteBuilder

    source = tmp_path / "control.robot"
    source.write_text(
        "*** Test Cases ***\nAsercion Robot\n    [Tags]    XG-VEN-001\n"
        "    Should Be Equal As Integers    2    1\n"
        "Recuperacion y fallo de control\n    [Tags]    XG-VEN-002\n"
        "    TRY\n        Fail    FALLA_TRANSITORIA\n    EXCEPT\n        No Operation\n    END\n"
        "    IF    ${NO_EXISTE}\n        No Operation\n    END\n", encoding="utf-8",
    )
    listener = QAListener(tmp_path, secrets=[])
    result = TestSuiteBuilder().build(source).run(output=None, log=None, report=None, console="none", listener=listener)
    events = [json.loads(line) for line in listener.writer.path.read_text(encoding="utf-8").splitlines()]
    cases = [event for event in events if event["event"] == "case_end"]
    assert cases[0]["status"] == "failed"
    assert cases[0]["failure"]["category"] == "functional_assertion"
    assert cases[1]["failure"]["message"] == result.suite.tests[1].message
    assert "FALLA_TRANSITORIA" not in cases[1]["failure"]["message"]


def test_real_robot_retry_recovers_without_failure_summary(tmp_path):
    from robot.api import TestSuite as RobotSuite

    library = tmp_path / "RetryReal.py"
    library.write_text(
        "from framework.events import assertion_failed\nattempts = 0\n"
        "def eventually_ready():\n    global attempts\n    attempts += 1\n    if attempts == 1:\n"
        "        assertion_failed('Todavía no', expected=2, observed=1)\n"
        "        raise AssertionError('Todavía no')\n", encoding="utf-8",
    )
    suite = RobotSuite("Retry real")
    suite.resource.imports.library(library.as_posix())
    suite.tests.create("Se recupera", tags=["XG-VEN-001"]).body.create_keyword(
        "Wait Until Keyword Succeeds", args=["2x", "0.01s", "Eventually Ready"])
    listener = QAListener(tmp_path, secrets=[])
    result = suite.run(output=None, log=None, report=None, console="none", listener=listener)
    events = [json.loads(line) for line in listener.writer.path.read_text(encoding="utf-8").splitlines()]
    final = next(event for event in events if event["event"] == "case_end")
    assert result.return_code == 0
    assert final["status"] == "passed"
    assert "failure" not in final


def test_nested_caught_failure_and_lowercase_assertions_follow_robot_semantics(tmp_path):
    from robot.api import TestSuiteBuilder

    source = tmp_path / "nested.robot"
    source.write_text(
        "*** Test Cases ***\nAsercion normalizada\n    [Tags]    XG-VEN-001\n"
        "    should_be_equal_as_integers    2    1\n"
        "Falla en keyword padre\n    [Tags]    XG-VEN-002\n    Recover And Later Fail\n"
        "*** Keywords ***\nRecover And Later Fail\n"
        "    TRY\n        Fail    FALLA_YA_RECUPERADA\n    EXCEPT\n        No Operation\n    END\n"
        "    IF    ${NO_EXISTE}\n        No Operation\n    END\n", encoding="utf-8",
    )
    listener = QAListener(tmp_path, secrets=[])
    result = TestSuiteBuilder().build(source).run(output=None, log=None, report=None, console="none", listener=listener)
    events = [json.loads(line) for line in listener.writer.path.read_text(encoding="utf-8").splitlines()]
    cases = [event for event in events if event["event"] == "case_end"]
    assert cases[0]["status"] == "failed"
    assert cases[1]["failure"]["message"] == result.suite.tests[1].message
    assert "FALLA_YA_RECUPERADA" not in cases[1]["failure"]["message"]
