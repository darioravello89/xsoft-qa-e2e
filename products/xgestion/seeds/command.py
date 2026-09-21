"""Offline seed preview and explicit preparation of the private QA baseline."""

import importlib
import json
import sys
from contextlib import ExitStack
from datetime import date
from pathlib import Path

from framework.config import load_profile
from framework.environment import ensure_offline
from framework.errors import QAError
from framework.events import EventWriter, format_event
from framework.fixtures.mysql import MySQLSandbox
from framework.paths import protect, safe_path
from framework.reporting import safe_value
from framework.runner import RunLock, new_run
from products.xgestion.contracts import read_json, validate_fixtures

NAME = "catalogo-comercial-v1"


def _engine():
    return importlib.import_module("products.xgestion.seeds.engine")


def read_seed_fixtures(profile):
    """Seeding needs the valid baseline context, without requiring calibrated UI locators."""
    fixtures = read_json(profile.asset("fixtures"))
    validate_fixtures(fixtures)
    return fixtures


def run_seed(root: Path, *, apply=False, dry_run=False, reference_date=None, export=False) -> int:
    if apply and dry_run:
        raise QAError("Elegir vista previa o --apply, nunca ambos.")
    reference_date = reference_date or date.today()
    engine = _engine()
    description = engine.describe_seed(reference_date=reference_date)
    if export:
        work = root / "work"
        if work.is_symlink() or not work.resolve().is_relative_to(root.resolve()):
            raise QAError("La carpeta work debe permanecer dentro del repositorio QA.")
        work.mkdir(exist_ok=True)
        destination = safe_path(work, "seed-preview.sql")
        destination.write_text(engine.render_seed(reference_date=reference_date), encoding="utf-8")
        print(f"SQL de vista previa para revisión: {destination}")
    if not apply:
        print(f"Vista previa sin conexión: {description['name']} | fecha {reference_date.isoformat()}")
        print("Cantidades del catálogo: " + json.dumps(description.get("counts", {}), ensure_ascii=False))
        print("Esquema y colisiones no verificados. No se abrió MySQL ni se modificó una base.")
        print("Para revisar SQL: agregar --export. Para restaurar y preparar solo xsoft_qa privada: --apply.")
        return 0

    directory = new_run(root, "seed")
    secrets, summary = [], {"name": NAME, "reference_date": reference_date.isoformat()}
    writer = EventWriter(directory / "events.jsonl", secrets=secrets)

    def progress(event, message, **details):
        payload = writer.emit("INFO", event, message, **details)
        print(format_event(payload), flush=True)

    code = 2
    interrupted = False

    def remember_interruption(error_type, *_):
        nonlocal interrupted
        if error_type is not None and issubclass(error_type, KeyboardInterrupt):
            interrupted = True

    try:
        with RunLock(root / ".local"), ExitStack() as resources:
            profile = load_profile(root)
            secrets.extend(value for key, value in profile.values.items()
                           if any(word in key.upper() for word in ("PASSWORD", "USER", "SECRET", "TOKEN", "KEY")))
            fixtures = read_seed_fixtures(profile)
            ensure_offline()
            summary.update({"app_version": profile.manifest["app_version"],
                            "database_version": profile.manifest["mysql_version"],
                            "baseline_sha256": profile.manifest["files"]["dump"]["sha256"]})
            sandbox = MySQLSandbox(profile)
            resources.callback(sandbox.stop)
            # Observe cancellation before a cleanup exception can replace it.
            resources.push(remember_interruption)
            progress("restore", "Restaurando el baseline en la instancia propia 127.0.0.1:13317/xsoft_qa. "
                     "Se reemplazan los datos de esa base privada.")
            sandbox.start()
            sandbox.restore()
            ensure_offline()
            progress("preflight", "Verificando esquema, identidades reservadas y catálogo antes de aplicar el seed.")
            summary.update(engine.apply_seed(sandbox, fixtures, reference_date=reference_date))
        code, summary["status"] = 0, "seed-applied"
        counts = summary.get("counts", {})
        progress("run_end", "Seed aplicado y verificado. "
                 f"Insertados: {counts.get('inserted', 0)}; actualizados: {counts.get('updated', 0)}; "
                 f"sin cambios: {counts.get('unchanged', 0)}. Esto no ejecuta ni acredita pruebas E2E.")
    except KeyboardInterrupt:
        code, summary["status"] = 130, "cancelled"
        summary["reason"] = "Preparación cancelada; volver a restaurar antes de ejecutar casos."
    except QAError as error:
        code = 130 if interrupted else 2
        summary.update(status="cancelled" if interrupted else "blocked", reason=safe_value(str(error), secrets))
    except Exception:
        code = 130 if interrupted else 2
        summary.update(status="cancelled" if interrupted else "blocked", reason="Fallo técnico al preparar el seed privado. "
                       "No se aprobó la preparación; revisar el paquete y volver a restaurar.")
    finally:
        if "reason" in summary:
            try:
                progress("run_error", summary["reason"])
            except (Exception, KeyboardInterrupt) as error:
                code = 130 if code == 130 or isinstance(error, KeyboardInterrupt) else 2
                summary.update(status="cancelled" if code == 130 else "blocked",
                               event_error="No se pudo registrar el evento final de preparación.")
        summary = safe_value({**summary, "exit_code": code}, secrets)
        report = directory / "seed-summary.json"
        try:
            report.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
            protect(report)
            print(safe_value(f"Resumen privado de preparación: {report}", secrets), file=sys.stdout)
        except (Exception, KeyboardInterrupt) as error:
            code = 130 if code == 130 or isinstance(error, KeyboardInterrupt) else 2
            # A partial or unprotected success record must not remain authoritative.
            try:
                report.unlink(missing_ok=True)
            except OSError:
                pass
            label = "CANCELADO" if code == 130 else "BLOQUEADO"
            print(f"{label}: no se pudo guardar el informe privado completo del seed; "
                  "la preparación no se acredita como aprobada.", file=sys.stderr)
    return code
