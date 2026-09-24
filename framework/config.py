"""Configuración explícita: no expande shell ni importa variables del proceso padre."""

import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from framework.errors import QAError
from framework.paths import safe_path

ENV_KEYS = {
    "QA_JAVA_HOME", "QA_LOGIN_USER", "QA_LOGIN_PASSWORD", "QA_DB_PASSWORD",
    "QA_KEYBOARD_RESTRICTED_USER", "QA_KEYBOARD_RESTRICTED_PASSWORD",
    "XPORTAL_BASE_URL", "CONSULTADOR_BASE_URL", "MOZOS_APK_PATH",
}
ASSETS = {"app", "mysql", "dump", "config", "fixtures", "locators", "credentials"}


def parse_env(content: str) -> dict[str, str]:
    values = {}
    for number, line in enumerate(content.splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, sep, value = line.partition("=")
        key, value = key.strip(), value.strip()
        if not sep or key not in ENV_KEYS or key in values:
            raise QAError(f"Variable desconocida, repetida o inválida en línea {number} del .env.")
        try:
            if value.startswith('"'):
                value = json.loads(value)
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
        except (ValueError, TypeError):
            raise QAError(f"Comillas inválidas en línea {number} del .env.") from None
        if not isinstance(value, str) or any(c in value for c in "\r\n\0"):
            raise QAError(f"Valor inválido en línea {number} del .env.")
        values[key] = value
    return values


def write_env(path: Path, values: dict[str, str]) -> None:
    from framework.paths import protect

    path.write_text("".join(f"{key}={json.dumps(value, ensure_ascii=False)}\n" for key, value in values.items()), encoding="utf-8")
    protect(path)


def digest(path: Path) -> str:
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def read_manifest(path: Path) -> dict:
    try:
        manifest = json.loads(path.read_text(encoding="utf-8-sig"))
        if not isinstance(manifest, dict) or not isinstance(manifest.get("files"), dict):
            raise ValueError
        if manifest["schema_version"] != 1 or manifest["product"] != "xgestion":
            raise ValueError
        if not re.fullmatch(r"[0-9A-Za-z.\-]+", manifest["app_version"]):
            raise ValueError
        if not re.fullmatch(r"(?:5\.7|8\.[04])\.\d+", manifest["mysql_version"]):
            raise ValueError
        if set(manifest["files"]) != ASSETS:
            raise ValueError
        names = set()
        for asset in manifest["files"].values():
            if not isinstance(asset, dict):
                raise ValueError
            name = asset["path"]
            safe_path(path.parent, name)
            if name.casefold() in names or not re.fullmatch(r"[a-fA-F0-9]{64}", asset["sha256"]):
                raise ValueError
            names.add(name.casefold())
        return manifest
    except (KeyError, TypeError, ValueError, OSError):
        raise QAError("manifest.json inválido: revisar versión, producto y archivos con SHA-256.") from None


@dataclass
class Profile:
    root: Path
    runtime: Path
    bundle: Path
    values: dict[str, str] = field(repr=False)
    manifest: dict = field(repr=False)

    def env(self, key: str, default: str | None = None) -> str:
        value = self.values.get(key, default)
        if value is None or not value.strip() or value == "REEMPLAZAR":
            raise QAError(f"Falta configurar {key} en .env.local.")
        return value

    def asset(self, key: str) -> Path:
        return safe_path(self.bundle, self.manifest["files"][key]["path"])


def load_profile(root: Path) -> Profile:
    root = root.resolve()
    runtime = root / ".local/xgestion"
    bundle = runtime / "bundle"
    if not (bundle / "manifest.json").is_file() or not (root / ".env.local").is_file():
        raise QAError("Falta el paquete QA privado. Ejecutar qa.cmd setup --bundle RUTA_AL_PAQUETE.")
    if not runtime.resolve().is_relative_to(root):
        raise QAError("El runtime privado no puede redirigirse fuera del repositorio.")
    manifest = read_manifest(bundle / "manifest.json")
    profile = Profile(root, runtime, bundle, parse_env((root / ".env.local").read_text(encoding="utf-8-sig")), manifest)
    for name, info in manifest["files"].items():
        path = profile.asset(name)
        if not path.is_file() or digest(path).lower() != info["sha256"].lower():
            raise QAError(f"Archivo privado ausente o modificado: {name}. Reimportar un paquete autorizado.")
    for key in ("QA_LOGIN_USER", "QA_LOGIN_PASSWORD", "QA_DB_PASSWORD"):
        profile.env(key)
    return profile
