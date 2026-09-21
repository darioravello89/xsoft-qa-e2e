"""Artefactos locales: metadatos explícitos y redacción de secretos conocidos."""

import html
import io
import json
import math
import re
from pathlib import Path
from urllib.parse import quote, quote_plus
from xml.etree import ElementTree

from framework.errors import QAError

_PRIVATE_KEY = re.compile(r"password|passwd|secret|token|authorization|cookie|credential|api.?key|sql|params|rows", re.I)
_ANSI = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
_ASSIGNMENT = re.compile(
    r"(?i)((?:password|passwd|token|secret|api[_-]?key|authorization|cookie)\s*[\"']?\s*[:=]\s*)"
    r"(?:\"[^\"]*\"|'[^']*'|[^\s&,;]+)")
_STRUCTURAL_VALUES = {"INFO", "DEBUG", "TRACE", "PASS", "FAIL", "SKIP", "NOT RUN", "passed", "failed", "blocked",
                      "cancelled", "validated-only", "functional_assertion", "environment_block", "automation_error",
                      "not_run", "timeout", "evidence_incomplete", "seed-applied", "preview-only"}
_EVENT_NAMES = {"listener_ready", "listener_closed", "case_start", "case_end", "step_start", "step_end",
                "diagnostic", "run_start", "preflight", "restore", "run_end", "run_error"}
STATUS_LABELS = {"passed": "OK", "failed": "FALLÓ", "blocked": "BLOQUEADO", "cancelled": "CANCELADO",
                 "validated-only": "VALIDADO EN SECO", "inspection-only": "INSPECCIÓN", "not-run": "NO EJECUTADO"}


def safe_value(value, secrets: list[str], *, key=""):
    """Sanitize before serialization; never stringify arbitrary data or objects."""
    if _PRIVATE_KEY.search(key):
        return "[REDACTADO]"
    if value is None or isinstance(value, (bool, int)):
        return value
    if isinstance(value, float):
        return value if math.isfinite(value) else "[DATO OMITIDO]"
    if isinstance(value, str):
        if key == "event" and value in _EVENT_NAMES:
            return value
        if key in {"id", "case_id"} and re.fullmatch(r"[A-Z]{2,8}-[A-Z]{2,8}-\d{3}", value):
            return value
        if key in {"level", "status", "robot_status", "category"} and value in _STRUCTURAL_VALUES:
            return value
        value = redact(value, secrets)
        value = _ANSI.sub("", value)
        value = re.sub(r"[\x00-\x1f\x7f]", " ", value)
        value = re.sub(r"(https?://)[^/\s@]+@", r"\1[REDACTADO]@", value)
        value = re.sub(r"(?i)\bBearer\s+[^\s,;]+", "Bearer [REDACTADO]", value)
        return _ASSIGNMENT.sub(r"\1[REDACTADO]", value)[:4000]
    if isinstance(value, dict):
        return {str(name): safe_value(item, secrets, key=str(name)) for name, item in value.items()
                if isinstance(name, str)}
    if isinstance(value, (list, tuple)):
        return [safe_value(item, secrets) for item in value]
    return "[DATO OMITIDO]"


def redact(value: str, secrets: list[str]) -> str:
    representations = set()
    for secret in secrets:
        if secret:
            representations.update((secret, html.escape(secret), html.escape(secret, quote=False),
                                    json.dumps(secret)[1:-1], quote(secret, safe=""), quote_plus(secret)))
    for secret in sorted(representations, key=len, reverse=True):
        value = value.replace(secret, "[REDACTADO]")
    return value


def redact_xml(value: str, secrets: list[str]) -> str:
    """Preserva tags/atributos XML aunque un secreto coincida con sus nombres."""
    try:
        document = ElementTree.fromstring(value)
    except ElementTree.ParseError:
        # Un output interrumpido puede estar truncado; se sanea y Rebot lo rechazará.
        return redact(value, secrets)
    for node in document.iter():
        if node.text:
            node.text = redact(node.text, secrets)
        if node.tail:
            node.tail = redact(node.tail, secrets)
        for key, content in node.attrib.items():
            # Robot usa status, id, conteos y tiempos como estructura del resultado.
            # Coincidir con una clave breve no debe convertir PASS/0 en datos inválidos.
            if key in {"name", "source", "owner", "value"}:
                node.set(key, redact(content, secrets))
    return ElementTree.tostring(document, encoding="unicode")


def sanitize_artifacts(directory: Path, secrets: list[str]) -> None:
    for path in directory.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".html", ".xml", ".json", ".jsonl", ".log", ".txt", ".csv"}:
            original = path.read_text(encoding="utf-8", errors="replace")
            if path.suffix.lower() == ".json":
                try:
                    clean = json.dumps(safe_value(json.loads(original), secrets), ensure_ascii=False, indent=2)
                except (ValueError, TypeError):
                    clean = redact(original, secrets)
            elif path.suffix.lower() == ".jsonl":
                try:
                    clean = "".join(json.dumps(safe_value(json.loads(line), secrets), ensure_ascii=False) + "\n"
                                    for line in original.splitlines())
                except (ValueError, TypeError):
                    clean = redact(original, secrets)
            else:
                clean = redact_xml(original, secrets) if path.suffix.lower() == ".xml" else redact(original, secrets)
            if original != clean:
                path.write_text(clean, encoding="utf-8")


def build_robot_reports(directory: Path, secrets: list[str]) -> None:
    """Genera HTML sólo desde XML saneado, antes de que Robot comprima mensajes.

    Robot debe ejecutarse con --log NONE --report NONE. Reemplazar secretos en
    HTML ya generado no alcanza: sus mensajes pueden estar en zlib/base64.
    """
    for name in ("log.html", "report.html"):
        (directory / name).unlink(missing_ok=True)
    sanitize_artifacts(directory, secrets)
    output = directory / "output.xml"
    if not output.is_file():
        return
    from robot import rebot

    try:
        code = rebot(
            str(output), outputdir=str(directory), output="NONE", log="log.html", report="report.html",
            stdout=io.StringIO(), stderr=io.StringIO(),
        )
    except (Exception, SystemExit):
        raise QAError("No se pudo generar el reporte Robot desde la evidencia saneada.") from None
    if code >= 251 or not all((directory / name).is_file() for name in ("log.html", "report.html")):
        raise QAError("La evidencia Robot está incompleta; no se generó un reporte válido.")


def write_summary(directory: Path, *, status: str, mode: str, cases: list[str], code: int, **extra) -> None:
    payload = {"status": status, "mode": mode, "cases": cases, "exit_code": code, **extra}
    (directory / "summary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_run_report(directory: Path, payload: dict) -> None:
    """The official report includes runner completion, not only Robot statistics."""
    robot_report = directory / "report.html"
    if robot_report.exists():
        robot_report.replace(directory / "robot-report.html")

    def esc(value):
        return html.escape(str(value))

    status = payload["status"]
    label = STATUS_LABELS.get(status, status)
    banner = ("Esta ejecución no acredita una suite aprobada. Revisar el bloqueo y la evidencia."
              if status in {"blocked", "cancelled"} else
              "Validación técnica; no acredita pruebas reales sobre XGestion."
              if status in {"validated-only", "inspection-only"} else
              "Resultado de la ejecución y sus comprobaciones.")
    parts = ["<!doctype html><html lang='es'><meta charset='utf-8'><title>Resultado QA</title>",
             "<style>body{font:16px system-ui;max-width:1100px;margin:2rem auto;padding:1rem}"
             "td,th{padding:.7rem;border-bottom:1px solid #ccc;text-align:left}table{border-collapse:collapse;width:100%}"
             ".notice{padding:1rem;background:#fff3cc}pre{white-space:pre-wrap}</style>",
             f"<h1>Resultado: {esc(label)}</h1><p class='notice'>{esc(banner)}</p>",
             f"<p>Modo: {esc(payload['mode'])} · Duración: {esc(payload.get('elapsed_seconds', 0))} s</p>"]
    if payload.get("app_version"):
        parts.append(f"<p>Versión XGestion: {esc(payload['app_version'])}<br>"
                     f"SHA-256 del JAR: <code>{esc(payload.get('jar_sha256', 'No disponible'))}</code></p>")
    for key in ("reason", "report_error"):
        if payload.get(key):
            parts.append(f"<p>{esc(payload[key])}</p>")
    parts.append("<h2>Casos seleccionados</h2><table><tr><th>Caso</th><th>Resultado</th><th>Detalle</th></tr>")
    for case in payload.get("case_results", []):
        detail = ""
        if failure := case.get("failure"):
            detail = "<br>".join(f"{esc(name)}: {esc(failure.get(key, ''))}" for name, key in
                                (("Paso", "step"), ("Comprobación", "message"), ("Esperado", "expected"),
                                 ("Observado", "observed"), ("Categoría", "category"), ("Causa", "cause")))
        parts.append(f"<tr><td>{esc(case['id'])}: {esc(case['title'])}</td>"
                     f"<td>{esc(STATUS_LABELS.get(case['status'], case['status']))}</td><td>{detail}</td></tr>")
    parts.append("</table><h2>Grupos</h2>")
    for group in payload.get("groups", []):
        counts = ", ".join(f"{STATUS_LABELS.get(key, key)}: {count}" for key, count in group["counts"].items())
        parts.append(f"<p><strong>{esc(group['title'])} ({esc(group['id'])})</strong>: "
                     f"{esc(group['description'])}<br>{esc(counts)}</p>")
    parts.append("<h2>Evidencia local privada</h2><ul>")
    for name, title in (("log.html", "Pasos Robot"), ("robot-report.html", "Estadísticas Robot (detalle parcial)"),
                        ("events.jsonl", "Eventos saneados"), ("console.log", "Consola saneada"),
                        ("summary.json", "Resumen estructurado")):
        if (directory / name).is_file():
            parts.append(f"<li><a href='{name}'>{title}</a></li>")
    parts.append("</ul></html>")
    (directory / "report.html").write_text("\n".join(parts), encoding="utf-8")
