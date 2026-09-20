"""Importación de paquete privado, atómica y sin ejecutar su contenido."""

import json
import shutil
import stat
import tempfile
import zipfile
from pathlib import Path

from framework.config import digest, load_profile, parse_env, read_manifest, write_env
from framework.errors import QAError
from framework.paths import protect, safe_path


def import_bundle(root: Path, archive: Path) -> None:
    root = root.resolve()
    private = root / ".local"
    private.mkdir(exist_ok=True)
    if not private.resolve().is_relative_to(root):
        raise QAError("Directorio privado redirigido fuera del repositorio.")
    protect(private)
    runtime = private / "xgestion"
    destination = runtime / "bundle"
    if not destination.resolve().is_relative_to(private.resolve()):
        raise QAError("El perfil privado no puede redirigirse fuera de .local.")
    with tempfile.TemporaryDirectory(prefix="import-", dir=private) as scratch:
        stage = Path(scratch)
        try:
            with zipfile.ZipFile(archive) as bundle:
                names = set()
                infos = bundle.infolist()
                if len(infos) > 20000 or sum(i.file_size for i in infos) > 8 * 1024**3:
                    raise QAError("El paquete supera el límite de importación (8 GiB / 20000 entradas).")
                for info in infos:
                    name = info.filename.rstrip("/")
                    safe_path(stage, name)
                    if name.casefold() in names or stat.S_ISLNK(info.external_attr >> 16):
                        raise QAError("El paquete contiene rutas repetidas o enlaces no admitidos.")
                    names.add(name.casefold())
                if bundle.getinfo("manifest.json").file_size > 65536:
                    raise QAError("El manifiesto privado supera el tamaño permitido.")
                (stage / "manifest.json").write_bytes(bundle.read("manifest.json"))
                manifest = read_manifest(stage / "manifest.json")
                for info in manifest["files"].values():
                    path = safe_path(stage, info["path"])
                    path.parent.mkdir(parents=True, exist_ok=True)
                    with bundle.open(info["path"]) as source, path.open("wb") as target:
                        shutil.copyfileobj(source, target)
                    if digest(path).lower() != info["sha256"].lower():
                        raise QAError("El SHA-256 de un archivo privado no coincide con el manifiesto.")
        except (zipfile.BadZipFile, KeyError, OSError, RuntimeError):
            raise QAError("No se pudo leer el paquete privado; revisar ZIP, manifiesto y archivos.") from None
        credentials = safe_path(stage, manifest["files"]["credentials"]["path"])
        values = parse_env(credentials.read_text(encoding="utf-8-sig"))
        if any(not values.get(k) or values[k] == "REEMPLAZAR" for k in ("QA_LOGIN_USER", "QA_LOGIN_PASSWORD", "QA_DB_PASSWORD")):
            raise QAError("El paquete no contiene credenciales QA completas.")
        if destination.exists():
            current = read_manifest(destination / "manifest.json")
            if current != manifest:
                try:
                    source = json.loads((runtime / "profile.json").read_text(encoding="utf-8"))["source_manifest"]
                except (OSError, ValueError, KeyError):
                    source = None
                if source != manifest:
                    raise QAError("Ya existe otro paquete. Usar un checkout QA separado para conservar los datos actuales.")
            load_profile(root)
            return
        env_path = root / ".env.local"
        if env_path.exists():
            raise QAError("Ya existe .env.local: conservarlo fuera del checkout antes de importar; no se sobrescribió.")
        runtime.mkdir(exist_ok=True)
        protect(runtime)
        # El stage y el destino están en el mismo volumen; se publica sólo después de validar hashes.
        stage.rename(destination)
        try:
            write_env(env_path, values)
        except BaseException:
            # Revertir únicamente lo creado por esta importación, dentro de .local.
            shutil.rmtree(destination)
            env_path.unlink(missing_ok=True)
            raise
        (runtime / "profile.json").write_text(json.dumps({"schema_version": 1, "product": "xgestion", "source_manifest": manifest}), encoding="utf-8")


def calibrate(root: Path, locators: Path) -> None:
    """Adoptar sólo un mapa verificado para el JAR actual, conservando respaldo local."""
    from copy import deepcopy
    from types import SimpleNamespace
    from uuid import uuid4

    from framework.runner import RunLock
    from products.xgestion.contracts import load_assets

    with RunLock(root / ".local"):
        profile = load_profile(root)
        candidate = SimpleNamespace(asset=lambda key: locators if key == "locators" else profile.asset(key))
        load_assets(candidate)
        target = profile.asset("locators")
        previous = target.read_bytes()
        manifest_path = profile.bundle / "manifest.json"
        old_manifest = manifest_path.read_bytes()
        archive = profile.runtime / "calibration-history"
        archive.mkdir(exist_ok=True)
        (archive / f"{uuid4().hex}.json").write_bytes(previous)
        updated = deepcopy(profile.manifest)
        updated["files"]["locators"]["sha256"] = digest(locators)
        try:
            incoming = locators.read_bytes()
            target.write_bytes(incoming)
            manifest_path.write_text(json.dumps(updated, indent=2), encoding="utf-8")
            load_profile(root)
        except BaseException:
            target.write_bytes(previous)
            manifest_path.write_bytes(old_manifest)
            raise
