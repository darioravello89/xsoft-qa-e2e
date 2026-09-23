"""Isolated promotion profiles retain one logical result per QA scenario."""

import math
from copy import deepcopy
from pathlib import Path
from time import monotonic

PROFILE_VARIANTS = {
    "XG-PRM-070": ("active", "inactive", "active-again"),
    "XG-PRM-079": ("general-off", "offers-off", "allowed-warning-on", "allowed-warning-off"),
}
_STATUS = {0: "passed", 1: "failed", 2: "blocked", 130: "cancelled"}
_RANK = {0: 0, 1: 1, 2: 2, 130: 3}


def _failure_result(case, code, reason, *, category="environment_block", step="Preparación"):
    return {"code": code, "total": 1, "failed": int(code == 1), "skipped": 0,
            "case_results": [{"id": case["id"], "title": case["title"], "status": _STATUS[code],
                              "failure": {"step": step, "message": reason,
                                          "expected": "Completar el caso con evidencia verificable.",
                                          "observed": reason, "category": category,
                                          "cause": "No determinada", "evidence": []}}]}


def _json_value(value):
    if value is None or isinstance(value, (str, bool, int)):
        return True
    if isinstance(value, float):
        return math.isfinite(value)
    if isinstance(value, list):
        return all(_json_value(item) for item in value)
    if isinstance(value, dict):
        return all(isinstance(key, str) and _json_value(item) for key, item in value.items())
    return False


def _valid_failure(value):
    if not isinstance(value, dict):
        return False
    if not all(isinstance(value.get(key), str) and value[key].strip()
               for key in ("step", "message", "category", "cause")):
        return False
    if not all(key in value and _json_value(value[key]) for key in ("expected", "observed")):
        return False
    return isinstance(value.get("evidence"), list) and all(isinstance(item, str) for item in value["evidence"])


def _exact_count(result, key, expected):
    value = result.get(key)
    return type(value) is int and value == expected


def _checked_result(case, result):
    """An exit code alone cannot approve a phase or confirm a product defect."""
    if not isinstance(result, dict):
        result = {}
    raw_code = result.get("code")
    recognized = type(raw_code) is int and raw_code in _STATUS
    code = raw_code if recognized else 2
    rows = result.get("case_results")
    valid = (recognized and isinstance(rows, list) and len(rows) == 1
             and isinstance(rows[0], dict) and rows[0].get("id") == case["id"]
             and rows[0].get("status") == _STATUS[code])
    if valid:
        row = rows[0]
        if code == 0:
            valid = (all(_exact_count(result, key, count) for key, count in
                         (("total", 1), ("failed", 0), ("skipped", 0))) and not row.get("failure"))
        else:
            valid = _valid_failure(row.get("failure"))
            if code == 1:
                valid = valid and all(_exact_count(result, key, count) for key, count in
                                      (("total", 1), ("failed", 1), ("skipped", 0)))
    if not valid:
        if code == 130:
            return _failure_result(case, 130, "La fase fue cancelada.", category="cancelled")
        return _failure_result(case, 2, "La fase no entregó un resultado completo y verificable.",
                               category="evidence_incomplete", step="Verificar evidencia de la fase")
    row = deepcopy(rows[0])
    row.update(id=case["id"], title=case["title"])
    return {**result, "code": code, "case_results": [row], "total": 1,
            "failed": int(code == 1), "skipped": 0}


def _run_phase(case, variant, directory, prepare, execute, finish_report):
    child = directory / "cases" / case["id"] / variant
    started, executed = monotonic(), False
    try:
        receipt = prepare(case, variant, child)
        executed = True
        result = _checked_result(case, execute([case], child, receipt, variant))
    except KeyboardInterrupt:
        result = _failure_result(case, 130, "La fase fue cancelada.", category="cancelled")
    except TimeoutError:
        result = _failure_result(case, 2, "La fase excedió el tiempo permitido.", category="timeout")
    except Exception:
        # Preparation exceptions may contain private credentials or configuration.
        result = _failure_result(case, 2, "No se pudo preparar o completar la fase.")
    evidence = []
    try:
        finish_report(child, result)
        report = child / "report.html"
        if not report.is_file():
            raise ValueError("Missing phase report")
        evidence = [report.relative_to(directory).as_posix()]
    except KeyboardInterrupt:
        result = _failure_result(case, 130, "Se canceló la generación de evidencia.", category="cancelled")
    except Exception:
        code = 130 if result["code"] == 130 else 2
        result = _failure_result(case, code, "No se pudo completar el informe de la fase.",
                                 category="evidence_incomplete", step="Generar informe de la fase")
    return result, {"variant": variant, "status": _STATUS[result["code"]], "executed": executed,
                    "elapsed_seconds": round(monotonic() - started, 3), "evidence": evidence}


def run_profiled_cases(plans, directory, *, prepare, execute, finish_report, initial_halt=0):
    """Real execution only; dry-run selects each logical case once without profiles.

    prepare owns baseline/config verification and returns the seed receipt.
    execute keeps owned-process and event/XML checks from execute_robot.
    finish_report must create report.html, even if preparation never made a directory.
    Callback outputs must retain the runner's sanitization guarantees.
    """
    directory = Path(directory)
    plans = [(case, tuple(variants)) for case, variants in plans]
    ids = []
    for case, variants in plans:
        case_id = case.get("id")
        if case_id not in PROFILE_VARIANTS or variants != PROFILE_VARIANTS[case_id]:
            raise ValueError("El plan debe contener todos los perfiles requeridos y en orden.")
        if not isinstance(case.get("title"), str) or not case["title"].strip():
            raise ValueError("El caso debe tener un título visible para QA.")
        ids.append(case_id)
    if len(ids) != len(set(ids)):
        raise ValueError("Un caso con perfiles no puede repetirse.")
    if initial_halt not in (0, 2, 130):
        raise ValueError("El estado previo de entorno no es válido.")
    results, halted, overall = [], initial_halt, 0
    for case, variants in plans:
        phases, logical, logical_code = [], None, 0
        for variant in variants:
            if halted:
                reason = ("No ejecutada: la ejecución fue cancelada." if halted == 130 else
                          "No ejecutada: una fase anterior dejó el entorno sin verificar.")
                result = _failure_result(case, halted, reason,
                                         category="cancelled" if halted == 130 else "environment_block")
                phase = {"variant": variant, "status": _STATUS[halted], "executed": False,
                         "elapsed_seconds": 0.0, "evidence": [], "reason": reason}
            else:
                result, phase = _run_phase(case, variant, directory, prepare, execute, finish_report)
                if result["code"] in (2, 130):
                    halted = result["code"]
            row = deepcopy(result["case_results"][0])
            if row.get("failure"):
                row["failure"]["evidence"] = list(phase["evidence"])
                phase["failure"] = deepcopy(row["failure"])
            phases.append(phase)
            if logical is None or _RANK[result["code"]] > _RANK[logical_code]:
                logical, logical_code = deepcopy(row), result["code"]
                if logical.get("failure"):
                    logical["failure"]["step"] = f"Perfil {variant}: {logical['failure']['step']}"
        logical["elapsed_seconds"] = round(sum(phase["elapsed_seconds"] for phase in phases), 3)
        logical["phases"] = phases
        results.append(logical)
        if _RANK[logical_code] > _RANK[overall]:
            overall = logical_code
    return {"code": overall, "case_results": results, "total": len(results),
            "failed": sum(row["status"] == "failed" for row in results), "skipped": 0}
