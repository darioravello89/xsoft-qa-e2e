"""Runner serial que separa simulación, fallo funcional y bloqueo de entorno."""

import json
import os
import platform
import sys
from contextlib import ExitStack
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path
from uuid import uuid4

from framework.catalog import select_cases, validate_catalog
from framework.config import load_profile
from framework.environment import doctor, ensure_offline, prepare_app_config
from framework.errors import QAError
from framework.paths import protect
from framework.reporting import build_robot_reports, redact, write_summary


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
    return directory


def run(root: Path, product: str, group: str | None = None, scenario: str | None = None,
        dry_run: bool = False, inspect: bool = False) -> int:
    cases = select_cases(validate_catalog(root), product, group, scenario)
    mode = "dry-run" if dry_run else "inspection" if inspect else "e2e"
    directory = new_run(root, mode)
    secrets, extra = [], {}
    code, status, sandbox = 2, "blocked", None
    try:
        with RunLock(root / ".local"), ExitStack() as resources:
            profile = None
            if not dry_run:
                profile = load_profile(root)
                secrets = [v for k, v in profile.values.items() if "PASSWORD" in k or "USER" in k]
                doctor(profile, calibration=not inspect)
                prepare_app_config(profile)
                from framework.fixtures.mysql import MySQLSandbox
                sandbox = MySQLSandbox(profile)
                resources.callback(sandbox.stop)
                sandbox.start()
                sandbox.restore()
                ensure_offline()
                extra = {"app_version": profile.manifest["app_version"],
                         "jar_sha256": profile.manifest["files"]["app"]["sha256"],
                         "baseline_sha256": profile.manifest["files"]["dump"]["sha256"],
                         "fixtures_sha256": profile.manifest["files"]["fixtures"]["sha256"],
                         "locators_sha256": profile.manifest["files"]["locators"]["sha256"],
                         "python_version": platform.python_version(), "robot_version": version("robotframework"),
                         "rpa_version": version("rpaframework"), "java_major": 17}
            if inspect:
                from products.xgestion.inspection import inspect_login
                inspect_login(profile, directory)
                code, status = 0, "inspection-only"
            else:
                command = [sys.executable, "-m", "robot", "--outputdir", str(directory), "--pythonpath", str(root),
                           "--name", "Xsoft QA" + (" - SOLO VALIDACION EN SECO" if dry_run else ""),
                           "--loglevel", "INFO", "--consolecolors", "off", "--log", "NONE", "--report", "NONE"]
                if dry_run:
                    command.append("--dryrun")
                for case in cases:
                    command.extend(["--include", case["id"]])
                command.append(str(root / "products/xgestion/suites"))
                env = os.environ.copy()
                env.update({"XSOFT_QA_ROOT": str(root), "XSOFT_QA_RUN_DIR": str(directory), "PYTHONUTF8": "1"})
                from framework.processes import run_owned_process
                result = run_owned_process(command, cwd=root, env=env, timeout=1800)
                log = redact(result.stdout.decode("utf-8", errors="replace") + result.stderr.decode("utf-8", errors="replace"), secrets)
                (directory / "console.log").write_text(log, encoding="utf-8")
                print(log)
                from robot.api import ExecutionResult
                if (directory / "output.xml").exists():
                    execution = ExecutionResult(str(directory / "output.xml"))
                    stats = execution.statistics.total
                    code = exit_status(result.returncode, stats.total, stats.failed, stats.skipped)
                    def has_environment_error(suite):
                        return any("QAError:" in test.message for test in suite.tests) or any(
                            has_environment_error(child) for child in suite.suites)
                    if has_environment_error(execution.suite):
                        code = 2
                    extra.update(total=stats.total, failed=stats.failed, skipped=stats.skipped)
                status = "validated-only" if dry_run and code == 0 else "passed" if code == 0 else "failed" if code == 1 else "blocked"
    except KeyboardInterrupt:
        code, status = 130, "cancelled"
    except QAError as error:
        code, status = 2, "blocked"
        print(redact(str(error), secrets))
        extra["reason"] = redact(str(error), secrets)
    except (Exception, SystemExit):
        code, status = 2, "blocked"
        extra["reason"] = "Fallo técnico del runner. Revisar doctor y dependencias; no se aprobó la suite."
        print(extra["reason"])
    finally:
        write_summary(directory, status=status, mode=mode, cases=[c["id"] for c in cases], code=code, **extra)
        try:
            build_robot_reports(directory, secrets)
        except Exception:
            code, status = 2, "blocked"
            extra["report_error"] = "No se pudo generar el informe HTML a partir del XML saneado."
            write_summary(directory, status=status, mode=mode, cases=[c["id"] for c in cases], code=code, **extra)
        (root / "reports/latest.json").write_text(json.dumps({"directory": directory.name}), encoding="utf-8")
        print(f"Informe local: {directory}")
    return code
