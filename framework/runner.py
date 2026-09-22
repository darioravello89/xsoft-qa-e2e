"""Runner serial que separa simulación, fallo funcional y bloqueo de entorno."""

import json
import os
import platform
import subprocess
import sys
import time
from collections import Counter
from contextlib import ExitStack
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path
from uuid import uuid4

from framework.catalog import select_cases, validate_catalog
from framework.config import load_profile
from framework.environment import doctor, ensure_offline, prepare_app_config
from framework.errors import QAError
from framework.events import EventStream, EventWriter, format_event, normalize_level
from framework.paths import protect
from framework.reporting import (
    STATUS_LABELS,
    build_robot_reports,
    safe_value,
    sanitize_artifacts,
    write_run_report,
    write_summary,
)


class RunLock:
    def __init__(self, directory: Path):
        self.directory = directory
        self.path = directory / "run.lock"

    def __enter__(self):
        self.directory.mkdir(parents=True, exist_ok=True)
        try:
            with self.path.open("x", encoding="utf-8") as lock:
                json.dump({"pid": os.getpid()}, lock)
        except FileExistsError:
            raise QAError("Ya hay una ejecución o un lock pendiente. Revisar el proceso antes de quitar .local/run.lock.") from None
        return self

    def __exit__(self, *_):
        self.path.unlink(missing_ok=True)


def exit_status(code: int, total: int, failed: int, skipped: int) -> int:
    if code >= 251 or total == 0 or skipped:
        return 2
    return 1 if code or failed else 0


def new_run(root: Path, mode: str) -> Path:
    reports = root / "reports"
    reports.mkdir(exist_ok=True)
    if not reports.resolve().is_relative_to(root.resolve()):
        raise QAError("La carpeta de informes sale del checkout.")
    protect(reports)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    directory = reports / f"{stamp}-{mode}-{uuid4().hex[:6]}"
    directory.mkdir()
    protect(directory)
    return directory


def failure_result(case, *, status="blocked", category="evidence_incomplete", reason, step="Preparación"):
    return {"id": case["id"], "title": case["title"], "status": status,
            "failure": {"step": step, "message": reason, "expected": "Completar el caso con evidencia verificable.",
                        "observed": reason, "category": category, "cause": "No determinada",
                        "evidence": ["events.jsonl", "console.log"]}}


def _groups_for_run(root, product, cases):
    from framework.catalog import group_overview
    return [group for group in group_overview(root, product, cases=cases)
            if any(group["id"] in case["tags"] for case in cases)]


def summarize_groups(groups, cases, results):
    by_id = {result["id"]: result for result in results}
    summaries = []
    for group in groups:
        members = [case for case in cases if group["id"] in case["tags"]]
        summaries.append({**{key: group[key] for key in ("id", "title", "description", "stage") if key in group},
                          "selected": len(members),
                          "counts": dict(Counter(by_id[case["id"]]["status"] for case in members))})
    return summaries


def execute_robot(root, directory, cases, *, dry_run, secrets, log_level, groups, timeout=1800, emit=None,
                  seed_context=None):
    """Run synthetic or real suites through the same owned process and event path."""
    from framework.processes import run_owned_process

    command = [sys.executable, "-m", "robot", "--outputdir", str(directory), "--pythonpath", str(root),
               "--pythonpath", str(Path(__file__).resolve().parent.parent),
               "--name", "Xsoft QA" + (" - SOLO VALIDACION EN SECO" if dry_run else ""),
               "--listener", "framework.robot_listener.QAListener", "--console", "none",
               "--loglevel", "INFO", "--log", "NONE", "--report", "NONE"]
    for group in groups:
        description = safe_value(f"{group['title']} ({group['id']}): {group['description']}", secrets)
        command.extend(["--metadata", f"Grupo {group['id']}:{description}"])
    if dry_run:
        command.append("--dryrun")
    for case in cases:
        command.extend(["--include", case["id"]])
    command.append(str(root / "products/xgestion/suites"))
    env = os.environ.copy()
    # Secrets never enter command arguments or files used to initialize the listener.
    env.update({"XSOFT_QA_ROOT": str(root), "XSOFT_QA_RUN_DIR": str(directory), "PYTHONUTF8": "1",
                "XSOFT_QA_REDACTIONS": json.dumps(secrets), "XSOFT_QA_DRY_RUN": "1" if dry_run else "0"})
    # Nunca heredar una aprobación de seed de otra ejecución o de un dry-run.
    applied = seed_context if not dry_run and seed_context and seed_context.get("status") == "seed-applied" else {}
    env.update({"XSOFT_QA_SEED": applied.get("name", ""),
                "XSOFT_QA_SEED_DATE": applied.get("reference_date", "")})
    interrupted = None
    result = None
    with EventStream(directory / "events.jsonl", level=log_level, secrets=secrets, emit=emit) as stream:
        try:
            result = run_owned_process(command, cwd=root, env=env, timeout=timeout)
        except KeyboardInterrupt:
            interrupted = (130, "cancelled", "cancelled", "Ejecución cancelada por el operador.")
        except subprocess.TimeoutExpired:
            interrupted = (2, "blocked", "timeout", "La ejecución superó el tiempo máximo permitido.")
        except Exception:
            interrupted = (2, "blocked", "automation_error", "No se pudo completar el proceso Robot propio.")
    events = stream.events
    ended = [event for event in events if event["event"] == "case_end"]
    results = {event["case_id"]: {"id": event["case_id"], "title": event["name"], "status": event["status"],
                                "elapsed_seconds": event["elapsed_seconds"],
                                **({"failure": event["failure"]} if "failure" in event else {})} for event in ended}
    incomplete_reason = stream.error
    stats = None
    if not interrupted:
        try:
            from robot.api import ExecutionResult

            sanitize_artifacts(directory, secrets)
            execution = ExecutionResult(str(directory / "output.xml"))
            stats = execution.statistics.total
            robot_tests = []

            def collect(suite):
                robot_tests.extend(suite.tests)
                for child in suite.suites:
                    collect(child)

            collect(execution.suite)
            expected_ids = {case["id"] for case in cases}
            actual_ids = [next((tag for tag in test.tags if tag in expected_ids), None) for test in robot_tests]
            if (set(actual_ids) != expected_ids or len(actual_ids) != len(cases)
                    or len(ended) != len(cases) or set(results) != expected_ids
                    or not any(event["event"] == "listener_closed" for event in events)):
                incomplete_reason = "Faltan casos o eventos finales en la evidencia de Robot."
            for test, case_id in zip(robot_tests, actual_ids, strict=True):
                if case_id in results and test.status != next(
                        event["robot_status"] for event in ended if event["case_id"] == case_id):
                    incomplete_reason = "El resultado final XML difiere del progreso registrado."
        except Exception:
            incomplete_reason = "El resultado XML no existe, está incompleto o no se puede leer."
    if interrupted or incomplete_reason:
        code, state, category, reason = interrupted or (2, "blocked", "evidence_incomplete", incomplete_reason)
        # Completed individual cases remain evidence; unfinished cases are never successes.
        for case in cases:
            if incomplete_reason or case["id"] not in results:
                results[case["id"]] = failure_result(case, status=state, category=category, reason=reason,
                                                    step="Ejecución Robot")
        failure = failure_result(cases[0], status=state, category=category, reason=reason, step="Ejecución Robot")["failure"]
        if result is not None and not any(event["event"] == "listener_ready" for event in events):
            # Robot cannot report its own listener/import failure through that listener.
            # Include only a bounded, sanitized stderr excerpt; never dump raw stdout.
            excerpt = safe_value(result.stderr.decode("utf-8", errors="replace")[:2000], secrets)
            if excerpt:
                failure["observed"] = excerpt
        event = EventWriter(directory / "events.jsonl", secrets=secrets).emit(
            "INFO", "run_error", reason, failure=failure)
        message = format_event(event)
        with (directory / "console.log").open("a", encoding="utf-8") as log:
            log.write(message + "\n")
        (emit or (lambda text: print(text, flush=True)))(message)
    else:
        code = exit_status(result.returncode, stats.total, stats.failed, stats.skipped)
        if any(item["status"] == "blocked" for item in results.values()):
            code = 2
    return {"code": code, "case_results": [results[case["id"]] for case in cases],
            "total": len(cases), "failed": sum(item["status"] == "failed" for item in results.values()),
            "skipped": stats.skipped if stats else 0}


def run(root: Path, product: str, group: str | None = None, scenario: str | None = None,
        dry_run: bool = False, inspect: bool = False, *, log_level: str = "INFO", seed: str | None = None) -> int:
    if seed and (product != "xgestion" or seed != "catalogo-comercial-v1" or inspect):
        raise QAError("El seed catalogo-comercial-v1 solo admite ejecución o dry-run de xgestion.")
    started = time.monotonic()
    log_level = normalize_level(log_level)
    cases = select_cases(validate_catalog(root), product, group, scenario)
    required_seed = None if inspect else next((case["seed"] for case in cases if case.get("seed")), None)
    seed = seed or required_seed
    groups = _groups_for_run(root, product, cases)
    mode = "dry-run" if dry_run else "inspection" if inspect else "e2e"
    directory = new_run(root, mode)
    secrets, extra = [], ({"seed": {"name": seed, "status": "not_run"}} if seed else {})
    code, status, sandbox = 2, "blocked", None
    writer = EventWriter(directory / "events.jsonl", secrets=secrets)
    interrupted = False

    def remember_interruption(error_type, *_):
        nonlocal interrupted
        if error_type is not None and issubclass(error_type, KeyboardInterrupt):
            interrupted = True

    def progress(event, message, **details):
        payload = writer.emit("INFO", event, message, **details)
        text = format_event(payload)
        with (directory / "console.log").open("a", encoding="utf-8") as log:
            log.write(text + "\n")
        print(text, flush=True)

    selected_group = next((item for item in groups if item["id"] == group), None)
    selection = (f"Grupo: {selected_group['title']} ({group})" if selected_group else
                 f"Caso: {cases[0]['title']} ({scenario})" if scenario else "Selección de escenarios")
    progress("run_start", f"{selection}. Casos: {len(cases)}. " +
             ("Validación en seco: no se ejecuta XGestion." if dry_run else "Preparando ejecución de QA."))
    if required_seed:
        progress("preflight", f"La selección requiere {required_seed}; "
                 "se preparará sobre el baseline QA restaurado." if not dry_run else
                 f"La selección requiere {required_seed}; en seco sólo se revisa su catálogo.")
    try:
        with RunLock(root / ".local"), ExitStack() as resources:
            profile = None
            if seed and dry_run:
                from products.xgestion.seeds.engine import describe_seed
                extra["seed"] = {**describe_seed(), "status": "preview-only"}
                progress("preflight", f"Catálogo {seed}: vista previa sin conexión; no se aplica ningún dato.")
            if not dry_run:
                profile = load_profile(root)
                secrets.extend(v for k, v in profile.values.items()
                               if any(label in k.upper() for label in ("PASSWORD", "USER", "SECRET", "TOKEN", "KEY")))
                progress("preflight", "Comprobando requisitos del entorno.")
                doctor(profile, calibration=not inspect)
                prepare_app_config(profile)
                from framework.fixtures.mysql import MySQLSandbox
                sandbox = MySQLSandbox(profile)
                resources.callback(sandbox.stop)
                resources.push(remember_interruption)
                progress("restore", "Iniciando la base local de QA y restaurando los datos del paquete.")
                sandbox.start()
                sandbox.restore()
                ensure_offline()
                extra.update({"app_version": profile.manifest["app_version"],
                         "jar_sha256": profile.manifest["files"]["app"]["sha256"],
                         "baseline_sha256": profile.manifest["files"]["dump"]["sha256"],
                         "fixtures_sha256": profile.manifest["files"]["fixtures"]["sha256"],
                         "locators_sha256": profile.manifest["files"]["locators"]["sha256"],
                         "python_version": platform.python_version(), "robot_version": version("robotframework"),
                         "rpa_version": version("rpaframework"), "java_major": 17})
                if seed:
                    from products.xgestion.seeds.command import read_seed_fixtures
                    from products.xgestion.seeds.engine import apply_seed
                    progress("preflight", f"Aplicando y verificando catálogo extra {seed} sobre el baseline restaurado.")
                    extra["seed"] = {**apply_seed(sandbox, read_seed_fixtures(profile)), "status": "seed-applied"}
            if inspect:
                from products.xgestion.inspection import inspect_login
                inspect_login(profile, directory)
                code, status = 0, "inspection-only"
            else:
                extra.update(execute_robot(root, directory, cases, dry_run=dry_run, secrets=secrets,
                                           log_level=log_level, groups=groups, seed_context=extra.get("seed")))
                code = extra.pop("code")
                interrupted = interrupted or code == 130
                status = ("validated-only" if dry_run and code == 0 else "passed" if code == 0
                          else "failed" if code == 1 else "cancelled" if code == 130 else "blocked")
    except KeyboardInterrupt:
        code, status = 130, "cancelled"
        extra["reason"] = "Ejecución cancelada por el operador."
    except QAError as error:
        code, status = (130, "cancelled") if interrupted else (2, "blocked")
        extra["reason"] = safe_value(str(error), secrets)
    except (Exception, SystemExit):
        code, status = (130, "cancelled") if interrupted else (2, "blocked")
        extra["reason"] = "Fallo técnico del runner. Revisar doctor y dependencias; no se aprobó la suite."
    finally:
        if seed and extra["seed"]["status"] == "not_run":
            extra["seed"]["status"] = "cancelled" if status == "cancelled" else "blocked"

        def final_progress(event, message, **details):
            nonlocal code, status
            try:
                progress(event, message, **details)
            except (Exception, KeyboardInterrupt) as error:
                code, status = ((130, "cancelled") if code == 130 or isinstance(error, KeyboardInterrupt)
                                else (2, "blocked"))
                extra["report_error"] = "No se pudo registrar toda la evidencia de progreso."

        category = "cancelled" if status == "cancelled" else "environment_block"
        if "case_results" not in extra:
            extra["case_results"] = [failure_result(case, status="not-run" if inspect and code == 0 else status,
                                                   category=category,
                                                   reason=extra.get("reason", "Inspección; caso no ejecutado."))
                                     for case in cases]
        if "reason" in extra:
            final_progress("run_error", extra["reason"], failure=failure_result(
                cases[0], category=category, reason=extra["reason"], step="Preparación o cierre del entorno")["failure"])
        try:
            build_robot_reports(directory, secrets)
        except Exception:
            if code != 130:
                code, status = 2, "blocked"
            extra["report_error"] = "No se pudo generar el informe HTML a partir del XML saneado."
            final_progress("run_error", extra["report_error"], failure=failure_result(
                cases[0], reason=extra["report_error"], step="Generación del informe")["failure"])
        extra["groups"] = summarize_groups(groups, cases, extra["case_results"])
        extra["elapsed_seconds"] = round(time.monotonic() - started, 3)
        extra["counts"] = dict(Counter(case["status"] for case in extra["case_results"]))
        extra = safe_value(extra, secrets)
        official_report_attempted = False
        try:
            write_summary(directory, status=status, mode=mode, cases=[c["id"] for c in cases], code=code, **extra)
            official_report_attempted = True
            write_run_report(directory, {"status": status, "mode": mode, **extra})
            counts = ", ".join(f"{STATUS_LABELS.get(key, key)}={count}" for key, count in extra["counts"].items())
            progress("run_end", f"Resultado final: {STATUS_LABELS[status]}. {counts}. "
                     f"Duración: {extra['elapsed_seconds']:.2f} s. Informe: {directory}", status=status)
            (root / "reports/latest.json").write_text(json.dumps({"directory": directory.name}), encoding="utf-8")
        except (Exception, KeyboardInterrupt) as error:
            code, status = ((130, "cancelled") if code == 130 or isinstance(error, KeyboardInterrupt)
                            else (2, "blocked"))
            extra["report_error"] = "La evidencia final está incompleta; no se acredita una ejecución aprobada."
            try:
                write_summary(directory, status=status, mode=mode, cases=[c["id"] for c in cases], code=code, **extra)
                if official_report_attempted:
                    (directory / "report.html").unlink(missing_ok=True)
                write_run_report(directory, {"status": status, "mode": mode, **extra})
            except Exception:
                # Do not leave a green Robot/partial report as the official result.
                try:
                    (directory / "report.html").unlink(missing_ok=True)
                except OSError:
                    pass
            print(safe_value(f"{STATUS_LABELS[status]}: {extra['report_error']} Informe local: {directory}", secrets),
                  file=sys.stderr)
    return code
