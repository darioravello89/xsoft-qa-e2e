import hashlib
import json
import zipfile

import pytest

from framework.bundle import import_bundle
from framework.config import load_profile, parse_env, read_manifest
from framework.errors import QAError
from framework.paths import safe_path


def package(tmp_path, *, corrupt=False, extra=None):
    files = {
        "app": ("app/xgestion.jar", b"synthetic jar"),
        "mysql": ("database/mysql.zip", b"synthetic portable archive"),
        "dump": ("database/baseline.sql", b"SELECT 1;"),
        "config": ("config/config.properties", b"licencia=synthetic\n"),
        "fixtures": ("config/fixtures.json", b"{}"),
        "locators": ("config/locators.json", b"{}"),
        "credentials": (
            "config/credentials.env",
            b"QA_LOGIN_USER=qa\nQA_LOGIN_PASSWORD=synthetic-login\nQA_DB_PASSWORD=synthetic-db\n",
        ),
    }
    manifest = {
        "schema_version": 1, "product": "xgestion", "app_version": "2.02.189-lts",
        "mysql_version": "5.7.44",
        "files": {k: {"path": p, "sha256": hashlib.sha256(b).hexdigest()} for k, (p, b) in files.items()},
    }
    archive = tmp_path / "package.zip"
    with zipfile.ZipFile(archive, "w") as out:
        out.writestr("manifest.json", json.dumps(manifest))
        for key, (path, value) in files.items():
            out.writestr(path, b"wrong" if corrupt and key == "app" else value)
        if extra:
            out.writestr(extra, "unexpected")
    return archive


@pytest.mark.parametrize("name", ["../escape", "/absolute", "C:/escape", "dir\\escape", "NUL", "x:stream", "a./b"])
def test_reject_unsafe_paths(tmp_path, name):
    with pytest.raises(QAError):
        safe_path(tmp_path, name)


def test_symlink_escape_rejected(tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    base = tmp_path / "base"
    base.mkdir()
    try:
        (base / "link").symlink_to(outside, target_is_directory=True)
    except OSError:
        pytest.skip("El sistema no permite crear symlinks en esta cuenta")
    with pytest.raises(QAError):
        safe_path(base, "link/file")


def test_env_values_are_data_and_windows_paths_survive():
    values = parse_env('QA_JAVA_HOME=C:\\tools\\java\nQA_LOGIN_PASSWORD="$(echo nope) # a"\n')
    assert values["QA_JAVA_HOME"] == "C:\\tools\\java"
    assert values["QA_LOGIN_PASSWORD"] == "$(echo nope) # a"


@pytest.mark.parametrize("content", ["QA_LOGIN_PASSWORD=x\nQA_LOGIN_PASSWORD=y", "BAD=value", "malformed"])
def test_invalid_env_fails_without_echoing_values(content):
    with pytest.raises(QAError) as error:
        parse_env(content)
    assert "value" not in str(error.value)


def test_import_is_idempotent_and_preserves_local_settings(tmp_path):
    archive = package(tmp_path)
    root = tmp_path / "repo"
    root.mkdir()
    import_bundle(root, archive)
    env = root / ".env.local"
    original = env.read_text(encoding="utf-8")
    env.write_text(original + '\nQA_JAVA_HOME="C:/local/java"\n', encoding="utf-8")
    import_bundle(root, archive)
    assert load_profile(root).env("QA_JAVA_HOME") == "C:/local/java"
    assert load_profile(root).asset("app").read_bytes() == b"synthetic jar"


def test_corrupt_archive_does_not_install_profile(tmp_path):
    archive = package(tmp_path, corrupt=True)
    root = tmp_path / "repo"
    root.mkdir()
    with pytest.raises(QAError):
        import_bundle(root, archive)
    assert not (root / ".env.local").exists()
    assert not (root / ".local/xgestion/bundle").exists()


def test_archive_traversal_rejected_before_writing(tmp_path):
    archive = package(tmp_path, extra="../../escape.env")
    root = tmp_path / "repo"
    root.mkdir()
    with pytest.raises(QAError):
        import_bundle(root, archive)
    assert not (tmp_path / "escape.env").exists()


def test_profile_detects_tampered_jar(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    import_bundle(root, package(tmp_path))
    profile = load_profile(root)
    profile.asset("app").write_bytes(b"changed")
    with pytest.raises(QAError):
        load_profile(root)


def test_existing_env_is_not_overwritten(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    env = root / ".env.local"
    env.write_text("QA_LOGIN_PASSWORD=existing\n", encoding="utf-8")
    with pytest.raises(QAError):
        import_bundle(root, package(tmp_path))
    assert env.read_text(encoding="utf-8") == "QA_LOGIN_PASSWORD=existing\n"


@pytest.mark.parametrize("content", [[], None, {"files": []}, {
    "schema_version": 1, "product": "xgestion", "app_version": "2.02.189-lts", "mysql_version": "5.7.44",
    "files": ["app", "mysql", "dump", "config", "fixtures", "locators", "credentials"],
}])
def test_invalid_manifest_shape_has_public_error(tmp_path, content):
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(content), encoding="utf-8")
    with pytest.raises(QAError):
        read_manifest(path)


def test_calibration_changes_only_locators_and_preserves_idempotent_setup(tmp_path, monkeypatch):
    import products.xgestion.contracts
    from framework.bundle import calibrate

    root = tmp_path / "repo"
    root.mkdir()
    archive = package(tmp_path)
    import_bundle(root, archive)
    before = load_profile(root)
    old = before.manifest
    env = (root / ".env.local").read_bytes()
    candidate = tmp_path / "locators.json"
    candidate.write_text('{"calibration":"synthetic"}', encoding="utf-8")
    # Contract validation is covered by product tests; this test isolates the import transaction.
    monkeypatch.setattr(products.xgestion.contracts, "load_assets", lambda profile: ({}, {}))
    calibrate(root, candidate)
    imported = load_profile(root)
    assert imported.asset("locators").read_bytes() == candidate.read_bytes()
    for key in old["files"]:
        if key != "locators":
            assert imported.manifest["files"][key] == old["files"][key]
    import_bundle(root, archive)
    assert load_profile(root).asset("locators").read_bytes() == candidate.read_bytes()
    assert (root / ".env.local").read_bytes() == env


def test_invalid_calibration_does_not_change_profile(tmp_path, monkeypatch):
    import products.xgestion.contracts
    from framework.bundle import calibrate

    root = tmp_path / "repo"
    root.mkdir()
    import_bundle(root, package(tmp_path))
    old = load_profile(root).asset("locators").read_bytes()
    def reject(profile):
        raise QAError("Mapa no calibrado")
    monkeypatch.setattr(products.xgestion.contracts, "load_assets", reject)
    with pytest.raises(QAError):
        calibrate(root, tmp_path / "missing.json")
    assert load_profile(root).asset("locators").read_bytes() == old
