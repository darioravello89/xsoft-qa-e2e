"""Publicación reproducible del mapa; comprobar vigencia no requiere Node ni secretos."""

import hashlib
import json
import os
import subprocess
import tempfile
import zipfile
from datetime import UTC, datetime
from pathlib import Path
from xml.etree import ElementTree as ET

from framework.coverage import build_coverage
from framework.errors import QAError

GENERATORS = ("framework/coverage.py", "framework/coverage_export.py", "scripts/build-coverage.mjs")
OUTPUT = "docs/coverage/xgestion-cobertura.xlsx"


def json_bytes(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def generator_hashes(root: Path) -> dict:
    # Normalize Git's Windows/Linux checkout line endings; Excel bytes remain exact.
    return {name: sha256((root / name).read_bytes().replace(b"\r\n", b"\n")) for name in GENERATORS}


def runtime() -> tuple[Path, Path]:
    dependencies = Path.home() / ".cache/codex-runtimes/codex-primary-runtime/dependencies/node"
    executable = "node.exe" if os.name == "nt" else "node"
    node = Path(os.environ.get("QA_COVERAGE_NODE", str(dependencies / "bin" / executable)))
    modules = Path(os.environ.get("QA_COVERAGE_MODULES", str(dependencies / "node_modules")))
    if not node.is_file() or not (modules / "@oai/artifact-tool/package.json").is_file():
        raise QAError(
            "Para regenerar el Excel, usar el runtime de hojas de cálculo del mantenedor/IA. "
            "Configurar QA_COVERAGE_NODE y QA_COVERAGE_MODULES con su Node y node_modules. "
            "QA puede descargar el Excel existente; coverage --check no requiere Node. Ver docs/cobertura.md."
        )
    return node.resolve(), modules.resolve()


def check_coverage(root: Path) -> Path:
    output = root / OUTPUT
    expected = json_bytes(build_coverage(root))
    try:
        actual = output.with_suffix(".json").read_bytes().replace(b"\r\n", b"\n")
        manifest = json.loads(output.with_suffix(".manifest.json").read_text(encoding="utf-8"))
        if not isinstance(manifest, dict):
            raise ValueError("manifest")
        if (actual != expected or manifest.get("schema_version") != 1
                or manifest.get("data_sha256") != sha256(expected)
                or manifest.get("workbook_sha256") != sha256(output.read_bytes())
                or manifest.get("generators") != generator_hashes(root)):
            raise ValueError("stale")
    except (OSError, ValueError, TypeError):
        raise QAError(
            "Mapa de cobertura ausente, alterado o desactualizado. Ejecutar qa.cmd coverage "
            "y guardar JSON, XLSX y manifest juntos."
        ) from None
    return output


def export_coverage(root: Path) -> Path:
    data = json_bytes(build_coverage(root))
    node, modules = runtime()
    output = root / OUTPUT
    work = root / "work"
    work.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="coverage-", dir=work) as directory:
        temporary = Path(directory) / output.name
        temporary.with_suffix(".json").write_bytes(data)
        environment = os.environ.copy()
        environment["QA_COVERAGE_MODULES"] = str(modules)
        try:
            subprocess.run(
                [str(node), str(root / "scripts/build-coverage.mjs"),
                 str(temporary.with_suffix(".json")), str(temporary)],
                cwd=root, env=environment, check=True, capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=180,
            )
            with zipfile.ZipFile(temporary) as workbook:
                for member in ("[Content_Types].xml", "xl/workbook.xml"):
                    workbook.getinfo(member)
                for member in workbook.namelist():
                    if member.startswith("xl/worksheets/") and member.endswith(".xml"):
                        sheet = ET.fromstring(workbook.read(member))
                        if any(cell.get("t") == "e" for cell in sheet.iter()
                               if cell.tag.endswith("}c")):
                            raise ValueError("El Excel contiene celdas con errores de cálculo.")
        except (OSError, subprocess.SubprocessError, zipfile.BadZipFile, KeyError, ValueError, ET.ParseError) as error:
            detail = (f"Node terminó con código {error.returncode}. {(error.stderr or '')[-1500:]}"
                      if isinstance(error, subprocess.CalledProcessError) else str(error))
            raise QAError(f"No se pudo generar el mapa de cobertura; se conserva el anterior. {detail}") from None
        manifest = {
            "schema_version": 1,
            "generated_at_utc": datetime.now(UTC).isoformat(timespec="seconds"),
            "data_sha256": sha256(data),
            "workbook_sha256": sha256(temporary.read_bytes()),
            "generators": generator_hashes(root),
        }
        temporary.with_suffix(".manifest.json").write_bytes(json_bytes(manifest))
        output.parent.mkdir(parents=True, exist_ok=True)
        # Build all three before replacing. Any interrupted publication is rejected by --check.
        for suffix in (".json", ".xlsx", ".manifest.json"):
            temporary.with_suffix(suffix).replace(output.with_suffix(suffix))
    return check_coverage(root)
