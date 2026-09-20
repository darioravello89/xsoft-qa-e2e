"""Límites de rutas compartidos por importación y runtime."""

import os
import re
import subprocess
from pathlib import Path

from framework.errors import QAError

_DEVICES = re.compile(r"^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)", re.I)


def safe_path(base: Path, relative: str) -> Path:
    if (not isinstance(relative, str) or not relative
            or any(c in relative for c in '\\:<>"|?*') or any(ord(c) < 32 for c in relative)):
        raise QAError("Ruta inválida en el paquete privado.")
    parts = relative.split("/")
    if any(p in ("", ".", "..") or p.endswith((".", " ")) or _DEVICES.match(p) for p in parts):
        raise QAError("Ruta fuera del directorio privado o incompatible con Windows.")
    path = base.joinpath(*parts)
    if not path.resolve().is_relative_to(base.resolve()):
        raise QAError("El destino sale del directorio privado.")
    return path


def protect(path: Path) -> None:
    """ACL de cuenta actual y SYSTEM, o modo privado en POSIX. Falla cerrado."""
    if os.name != "nt":
        path.chmod(0o700 if path.is_dir() else 0o600)
        return
    user = subprocess.check_output(["whoami"], text=True).strip()
    scope = "(OI)(CI)" if path.is_dir() else ""
    result = subprocess.run(
        ["icacls", str(path), "/inheritance:r", "/grant:r", f"{user}:{scope}F", f"*S-1-5-18:{scope}F"],
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise QAError("No se pudieron restringir los permisos de los archivos privados.")
