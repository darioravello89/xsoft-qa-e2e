"""Synthetic evidence for isolated profile phases, without starting the ERP."""

from copy import deepcopy

import pytest

from framework.profile_runs import PROFILE_VARIANTS, run_profiled_cases


def case(case_id="XG-PRM-070"):
    return {"id": case_id, "title": "Oferta por perfil", "tags": ["promociones"]}


def outcome(case_id="XG-PRM-070", code=0):
    row = {**case(case_id), "status": {0: "passed", 1: "failed", 2: "blocked", 130: "cancelled"}[code]}
    if code:
        row["failure"] = {"step": "Comprobar total", "message": "El total no coincide.",
                          "expected": 2000, "observed": 1000, "category": "functional_assertion",
                          "cause": "No determinada", "evidence": ["events.jsonl"]}
    return {"code": code, "case_results": [row], "total": 1, "failed": int(code == 1), "skipped": 0}


class Harness:
    def __init__(self):
        self.codes, self.overrides, self.errors, self.report_errors = {}, {}, {}, {}
        self.calls = []

    def prepare(self, item, variant, directory):
        self.calls.append(("prepare", item["id"], variant))
        directory.mkdir(parents=True, exist_ok=True)
        if variant in self.errors:
            raise self.errors[variant]
        return {"variant": variant}

    def execute(self, cases, directory, receipt, variant):
        assert receipt["variant"] == variant and directory.name == variant and len(cases) == 1
        self.calls.append(("execute", cases[0]["id"], variant))
        return deepcopy(self.overrides.get(variant, outcome(cases[0]["id"], self.codes.get(variant, 0))))

    def report(self, directory, result):
        self.calls.append(("report", directory.parent.name, directory.name))
        if directory.name in self.report_errors:
            raise self.report_errors[directory.name]
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "report.html").write_text("synthetic report", encoding="utf-8")

    def run(self, directory, ids=("XG-PRM-070",)):
        return run_profiled_cases([(case(key), PROFILE_VARIANTS[key]) for key in ids], directory,
                                  prepare=self.prepare, execute=self.execute, finish_report=self.report)

    def executions(self):
        return [item for item in self.calls if item[0] == "execute"]


def test_all_profiles_are_one_logical_case_with_real_report_links(tmp_path):
    rig = Harness()
    result = rig.run(str(tmp_path))
    assert (result["code"], result["total"], result["failed"], result["skipped"]) == (0, 1, 0, 0)
    row, = result["case_results"]
    assert row["status"] == "passed"
    assert [phase["variant"] for phase in row["phases"]] == list(PROFILE_VARIANTS[row["id"]])
    assert all(phase["executed"] and (tmp_path / phase["evidence"][0]).is_file() for phase in row["phases"])


def test_functional_failure_keeps_all_other_profiles_and_numeric_diagnostics(tmp_path):
    rig = Harness()
    rig.codes["inactive"] = 1
    result = rig.run(tmp_path, ("XG-PRM-070", "XG-PRM-079"))
    assert result["code"] == 1 and result["failed"] == 1 and len(rig.executions()) == 7
    assert [row["status"] for row in result["case_results"]] == ["failed", "passed"]
    row = result["case_results"][0]
    assert row["failure"]["step"].startswith("Perfil inactive:")
    assert row["failure"]["expected"] == 2000
    assert row["failure"]["evidence"] == ["cases/XG-PRM-070/inactive/report.html"]
    assert row["phases"][1]["failure"]["evidence"] == row["failure"]["evidence"]


@pytest.mark.parametrize("code,status", [(2, "blocked"), (130, "cancelled")])
def test_block_or_cancel_omits_remaining_phases_without_robot_skip_counts(tmp_path, code, status):
    rig = Harness()
    rig.codes["inactive"] = code
    result = rig.run(tmp_path, ("XG-PRM-070", "XG-PRM-079"))
    assert result["code"] == code and result["failed"] == result["skipped"] == 0
    assert [row["status"] for row in result["case_results"]] == [status, status]
    assert len(rig.executions()) == 2
    omitted = result["case_results"][0]["phases"][2:] + result["case_results"][1]["phases"]
    assert all(not phase["executed"] and not phase["evidence"] and phase["reason"] for phase in omitted)


def test_block_takes_precedence_over_previous_functional_failure(tmp_path):
    rig = Harness()
    rig.codes.update(active=1, inactive=2)
    result = rig.run(tmp_path)
    assert result["code"] == 2 and result["failed"] == 0
    assert result["case_results"][0]["failure"]["step"].startswith("Perfil inactive:")
    assert len(rig.executions()) == 2


@pytest.mark.parametrize("error,code", [(RuntimeError("password=PRIVATE"), 2),
                                       (TimeoutError("token=PRIVATE"), 2), (KeyboardInterrupt(), 130)])
def test_preparation_error_never_launches_robot_or_exposes_exception(tmp_path, error, code):
    rig = Harness()
    rig.errors["active"] = error
    result = rig.run(tmp_path)
    assert result["code"] == code and not rig.executions()
    assert "PRIVATE" not in repr(result)


@pytest.mark.parametrize("override", [None, {}, {"code": 0, "case_results": []},
                                     {"code": 1, "case_results": []}, {"code": 131}, {"code": False}])
def test_incomplete_evidence_is_blocked_never_functional_failure(tmp_path, override):
    rig = Harness()
    rig.overrides["active"] = override
    result = rig.run(tmp_path)
    assert result["code"] == 2 and result["failed"] == 0 and len(rig.executions()) == 1


@pytest.mark.parametrize("field,value", [("total", 0), ("total", 2), ("total", True), ("failed", 1),
                                        ("failed", False), ("skipped", 1), ("skipped", False)])
def test_pass_requires_exact_success_counts(tmp_path, field, value):
    rig = Harness()
    rig.overrides["active"] = outcome()
    rig.overrides["active"][field] = value
    assert rig.run(tmp_path)["code"] == 2


@pytest.mark.parametrize("failure", [None, "unstructured", {}, {"step": "Total", "message": "Distinto"}])
def test_functional_failure_needs_complete_structure(tmp_path, failure):
    rig = Harness()
    rig.overrides["active"] = outcome(code=1)
    rig.overrides["active"]["case_results"][0]["failure"] = failure
    assert rig.run(tmp_path)["code"] == 2


def test_cancel_exit_overrides_pass_event(tmp_path):
    rig = Harness()
    rig.overrides["active"] = outcome()
    rig.overrides["active"]["code"] = 130
    result = rig.run(tmp_path)
    assert result["code"] == 130 and result["case_results"][0]["status"] == "cancelled"


@pytest.mark.parametrize("error,code", [(RuntimeError("PRIVATE"), 2), (KeyboardInterrupt(), 130)])
def test_report_failure_prevents_success_and_cleans_error_text(tmp_path, error, code):
    rig = Harness()
    rig.report_errors["active"] = error
    result = rig.run(tmp_path)
    assert result["code"] == code and "PRIVATE" not in repr(result)
    assert result["case_results"][0]["phases"][0]["evidence"] == []


def test_missing_report_blocks_even_when_callback_returns(tmp_path):
    rig = Harness()
    rig.report = lambda *_: None
    assert rig.run(tmp_path)["code"] == 2


@pytest.mark.parametrize("variants", [("active",), ("inactive", "active", "active-again"),
                                     ("active", "../inactive", "active-again")])
def test_incomplete_or_changed_plan_is_rejected_before_side_effects(tmp_path, variants):
    rig = Harness()
    with pytest.raises(ValueError):
        run_profiled_cases([(case(), variants)], tmp_path, prepare=rig.prepare,
                           execute=rig.execute, finish_report=rig.report)
    assert rig.calls == []


def test_duplicate_plan_rejected_and_empty_plan_has_no_side_effects(tmp_path):
    rig = Harness()
    plan = (case(), PROFILE_VARIANTS["XG-PRM-070"])
    with pytest.raises(ValueError):
        run_profiled_cases([plan, plan], tmp_path, prepare=rig.prepare,
                           execute=rig.execute, finish_report=rig.report)
    result = rig.run(tmp_path, ())
    assert result == {"code": 0, "case_results": [], "total": 0, "failed": 0, "skipped": 0}
    assert rig.calls == []
