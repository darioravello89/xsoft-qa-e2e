"""Artefactos locales: metadatos explícitos y redacción de secretos conocidos."""

import html
import io
import json
from pathlib import Path
from urllib.parse import quote, quote_plus
from xml.etree import ElementTree

from framework.errors import QAError


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
        if path.is_file() and path.suffix.lower() in {".html", ".xml", ".json", ".log", ".txt", ".csv"}:
            original = path.read_text(encoding="utf-8", errors="replace")
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
