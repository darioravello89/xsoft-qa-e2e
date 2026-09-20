"""Run a private portable MySQL, never an installed service or an arbitrary host."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import os
import re
import secrets
import shutil
import socket
import stat
import subprocess
import tempfile
import time
import zipfile
from contextlib import contextmanager
from pathlib import Path, PurePosixPath

from framework.errors import QAError


def _contained(path: Path, parent: Path) -> Path:
    """Reject traversal and Windows junctions/reparse points, including ancestors."""
    parent = parent.absolute()
    path = path.absolute()
    if path == parent or not path.is_relative_to(parent):
        raise QAError("Ruta MySQL fuera del directorio privado de QA.")
    for current in [path, *path.parents]:
        if current.exists() or current.is_symlink():
            info = current.lstat()
            if current.is_symlink() or getattr(info, "st_file_attributes", 0) & 0x400:
                raise QAError("MySQL QA no admite enlaces simbolicos ni junctions.")
    if not path.resolve().is_relative_to(parent.resolve()):
        raise QAError("La ruta MySQL resuelve fuera del directorio QA.")
    return path


def _digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def extract_mysql_zip(archive: Path, target: Path) -> Path:
    """Install a ZIP once; an existing install must belong to that exact archive."""
    _contained(target, target.parent)
    checksum = _digest(archive)
    marker = target / ".qa-archive.json"
    if target.exists():
        try:
            installed = json.loads(marker.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise QAError("La carpeta mysql existente no pertenece al instalador QA.") from exc
        if installed != {"sha256": checksum}:
            raise QAError("MySQL instalado corresponde a otro ZIP; no se reemplaza automaticamente.")
        return target
    target.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix="mysql-unpack-", dir=target.parent))
    try:
        with zipfile.ZipFile(archive) as source:
            entries = source.infolist()
            if len(entries) > 25000 or sum(item.file_size for item in entries) > 4 * 1024**3:
                raise QAError("ZIP MySQL excede los limites de extraccion.")
            seen = set()
            for entry in entries:
                name = entry.filename.replace("\\", "/")
                parts = PurePosixPath(name).parts
                mode = entry.external_attr >> 16
                if (
                    not parts or name.startswith("/") or ".." in parts
                    or any(":" in part or part.endswith((".", " "))
                           or re.fullmatch(r"(?i)(con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\..*)?", part)
                           for part in parts)
                    or stat.S_ISLNK(mode) or name.rstrip("/").casefold() in seen
                ):
                    raise QAError("ZIP MySQL contiene una ruta insegura o duplicada.")
                seen.add(name.rstrip("/").casefold())
                _contained(staging.joinpath(*parts), staging)
            for entry in entries:
                destination = staging.joinpath(*PurePosixPath(entry.filename.replace("\\", "/")).parts)
                if entry.is_dir():
                    destination.mkdir(parents=True, exist_ok=True)
                else:
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    with source.open(entry) as incoming, destination.open("xb") as output:
                        shutil.copyfileobj(incoming, output)
        candidates = [item.parent.parent for item in staging.rglob("mysqld.exe") if item.parent.name == "bin"]
        if len(candidates) != 1 or not (candidates[0] / "bin" / "mysql.exe").is_file():
            raise QAError("ZIP requiere una unica distribucion Windows con bin/mysql.exe y mysqld.exe.")
        (candidates[0] / ".qa-archive.json").write_text(json.dumps({"sha256": checksum}), encoding="utf-8")
        os.replace(candidates[0], target)
        return target
    except (OSError, zipfile.BadZipFile) as exc:
        raise QAError("No se pudo extraer el ZIP privado de MySQL.") from exc
    finally:
        # Only remove the generated staging directory, after resolving its boundary.
        if staging.exists():
            _contained(staging, target.parent)
            shutil.rmtree(staging)


class MySQLSandbox:
    host = "127.0.0.1"
    port = 13317
    database = "xsoft_qa"

    def __init__(self, profile):
        self.profile = profile
        expected = Path(profile.root).absolute() / ".local" / "xgestion"
        self.runtime = _contained(Path(profile.runtime), Path(profile.root))
        if self.runtime != expected:
            raise QAError("MySQL solo puede usar .local/xgestion del repositorio QA.")
        self.basedir = self.runtime / "mysql"
        self.datadir = self.runtime / "mysql-data"
        self.pidfile = self.runtime / "mysql.pid"
        self.ownerfile = self.runtime / "mysql-owner.json"
        self.version = str(profile.manifest.get("mysql_version", ""))
        if not re.fullmatch(r"(?:5\.7|8\.[04])\.\d+", self.version):
            raise QAError("El paquete debe declarar una version exacta MySQL 5.7, 8.0 u 8.4.")
        self.password = profile.env("QA_DB_PASSWORD", "")
        if not self.password or any(ord(char) < 32 for char in self.password):
            raise QAError("Falta QA_DB_PASSWORD local o contiene caracteres de control.")
        self._process = None
        self._log = None

    def _owner(self):
        return {"schema": 1, "product": "xgestion", "datadir": str(self.datadir),
                "basedir": str(self.basedir), "mysql_version": self.version}

    def _verify_owner(self):
        for path in (self.datadir, self.basedir, self.pidfile, self.ownerfile):
            _contained(path, self.runtime)
        try:
            actual = json.loads(self.ownerfile.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise QAError("Falta el marcador de propiedad del MySQL de QA.") from exc
        if actual != self._owner():
            raise QAError("El marcador MySQL no corresponde a este repositorio.")

    def _assert_port_available(self):
        try:
            with socket.socket() as probe:
                if hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
                    probe.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
                probe.bind((self.host, self.port))
        except OSError as exc:
            raise QAError(f"Puerto QA {self.port} ocupado. No se conectara ni detendra otro servidor.") from exc

    def _prepare_datadir(self):
        _contained(self.datadir, self.runtime)
        if self.datadir.exists():
            self._verify_owner()
            if not (self.datadir / "mysql").is_dir():
                raise QAError("Inicializacion MySQL incompleta; revisar mysql-server.log antes de recuperar.")
            return False
        self.runtime.mkdir(parents=True, exist_ok=True)
        if self.ownerfile.exists():
            self._verify_owner()
        else:
            with self.ownerfile.open("x", encoding="utf-8") as output:
                json.dump(self._owner(), output)
        self.datadir.mkdir()
        result = subprocess.run(
            [str(self.basedir / "bin" / "mysqld.exe"), "--no-defaults", "--initialize-insecure",
             f"--basedir={self.basedir}", f"--datadir={self.datadir}"],
            capture_output=True, timeout=120, creationflags=self._hidden(),
        )
        if result.returncode:
            raise QAError("No se pudo inicializar el MySQL privado. No se modifico otra instalacion.")
        return True

    @staticmethod
    def _hidden():
        return subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0

    @contextmanager
    def _secret_file(self, content: str):
        directory = _contained(self.runtime / "mysql-secrets", self.runtime)
        directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        if os.name == "nt":
            identity = subprocess.run(["whoami", "/user", "/fo", "csv", "/nh"],
                                      capture_output=True, text=True, check=True, creationflags=self._hidden())
            sid = next(csv.reader(io.StringIO(identity.stdout.strip())))[1]
            result = subprocess.run(["icacls", str(directory), "/inheritance:r", "/grant:r", f"*{sid}:(OI)(CI)F"],
                                    capture_output=True, creationflags=self._hidden())
            if result.returncode:
                raise QAError("No se pudieron proteger los archivos temporales MySQL.")
        else:
            directory.chmod(0o700)
        descriptor, filename = tempfile.mkstemp(prefix="client-", suffix=".cnf", dir=directory)
        path = Path(filename)
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as output:
                output.write(content)
            yield path
        finally:
            path.unlink(missing_ok=True)

    @staticmethod
    def _sql_literal(value: str):
        return "'" + value.replace("\\", "\\\\").replace("'", "\\'") + "'"

    def _client(self, sql=None, dump=None, user="root", password=None, database=None):
        password = self.password if password is None else password
        escaped = password.replace("\\", "\\\\").replace('"', '\\"')
        config = f'[client]\nuser={user}\npassword="{escaped}"\nhost={self.host}\nport={self.port}\nprotocol=TCP\n'
        with self._secret_file(config) as options:
            command = [str(self.basedir / "bin" / "mysql.exe"), f"--defaults-file={options}",
                       "--batch", "--raw", "--skip-column-names", "--connect-timeout=2", "--binary-mode",
                       "--local-infile=0", "--default-character-set=utf8mb4"]
            # mysql reads the user's .mylogin.cnf even with --defaults-file.
            # Force its login-file location into our private, empty directory.
            environment = {key: value for key, value in os.environ.items() if not key.upper().startswith("MYSQL_")}
            environment["MYSQL_TEST_LOGIN_FILE"] = str(options.with_suffix(".unused-login"))
            if database:
                command.append(database)
            try:
                if dump:
                    with Path(dump).open("rb") as stream:
                        result = subprocess.run(command, stdin=stream, capture_output=True,
                                                timeout=600, creationflags=self._hidden(), env=environment)
                else:
                    result = subprocess.run(command, input=sql.encode("utf-8"), capture_output=True,
                                            timeout=30, creationflags=self._hidden(), env=environment)
            except (OSError, subprocess.TimeoutExpired) as exc:
                raise QAError("El cliente MySQL privado no respondio. No se muestran credenciales ni SQL.") from exc
        if result.returncode:
            raise QAError("Operacion MySQL QA rechazada; verificar paquete, credenciales y servidor local.")
        return result.stdout.decode("utf-8", errors="replace")

    def _sql(self, statement):
        return self._client(sql=statement)

    def _assert_owned_server(self):
        if self._process is None or self._process.poll() is not None:
            raise QAError("La instancia MySQL no fue iniciada por esta ejecucion QA.")
        self._verify_owner()
        try:
            pid = int(self.pidfile.read_text(encoding="ascii").strip())
        except (OSError, ValueError) as exc:
            raise QAError("No se pudo verificar el PID del MySQL privado.") from exc
        if pid != self._process.pid:
            raise QAError("El PID MySQL no pertenece a esta ejecucion QA.")
        fields = self._sql("SELECT @@datadir, @@port, @@version;").strip().split("\t")
        if (len(fields) != 3 or Path(fields[0]).resolve() != self.datadir.resolve()
                or fields[1] != str(self.port) or fields[2].split("-")[0] != self.version):
            raise QAError("El servidor no corresponde al datadir, puerto y version privados de QA.")

    def start(self):
        if os.name != "nt":
            raise QAError("MySQL portable de XGestion requiere Windows x64.")
        if self._process is not None:
            self._assert_owned_server()
            return self
        self._assert_port_available()
        archive = self.profile.asset("mysql")
        entry = self.profile.manifest["files"]["mysql"]
        if _digest(archive) != entry["sha256"].lower():
            raise QAError("El ZIP MySQL no coincide con el hash del manifiesto.")
        extract_mysql_zip(archive, self.basedir)
        version = subprocess.run([str(self.basedir / "bin" / "mysqld.exe"), "--no-defaults", "--version"],
                                 capture_output=True, text=True, timeout=10, creationflags=self._hidden())
        if version.returncode or f"Ver {self.version}" not in version.stdout or "Win64" not in version.stdout:
            raise QAError("El binario MySQL no corresponde a la version Windows x64 del paquete.")
        fresh = self._prepare_datadir()
        command = [str(self.basedir / "bin" / "mysqld.exe"), "--no-defaults",
                   f"--basedir={self.basedir}", f"--datadir={self.datadir}", f"--port={self.port}",
                   f"--bind-address={self.host}", f"--pid-file={self.pidfile}", "--skip-name-resolve",
                   "--local-infile=0", "--secure-file-priv=NULL", "--explicit-defaults-for-timestamp=1",
                   "--general-log=0", "--skip-log-bin", "--console"]
        if self.version.startswith("8."):
            # Do not expose the extra X Protocol listener or load persisted settings.
            command.extend(["--mysqlx=0", "--persisted-globals-load=OFF"])
        # init-file sets the password before the fresh server accepts clients.
        literal = self._sql_literal(self.password)
        init_sql = (
            f"ALTER USER 'root'@'localhost' IDENTIFIED BY {literal};\n"
            f"CREATE USER 'root'@'127.0.0.1' IDENTIFIED BY {literal};\n"
            "GRANT ALL PRIVILEGES ON *.* TO 'root'@'127.0.0.1' WITH GRANT OPTION;\n"
        )
        try:
            self._log = (self.runtime / "mysql-server.log").open("ab")
            with self._secret_file(init_sql if fresh else "") as init_file:
                if fresh:
                    command.append(f"--init-file={init_file}")
                self._process = subprocess.Popen(command, cwd=self.runtime, stdin=subprocess.DEVNULL,
                                                 stdout=self._log, stderr=self._log, creationflags=self._hidden())
                deadline = time.monotonic() + 60
                while time.monotonic() < deadline:
                    if self._process.poll() is not None:
                        raise QAError("MySQL privado finalizo al iniciar; revisar mysql-server.log local.")
                    try:
                        self._assert_owned_server()
                        return self
                    except QAError:
                        time.sleep(0.25)
                raise QAError("MySQL privado no quedo disponible en 60 segundos.")
        except BaseException:
            self.stop()
            raise

    def restore(self):
        """Only drop xsoft_qa, then import with a temporary account limited to it."""
        self._assert_owned_server()
        dump = self.profile.asset("dump")
        if _digest(dump) != self.profile.manifest["files"]["dump"]["sha256"].lower():
            raise QAError("El dump cambio despues de importar el paquete QA.")
        user = "fixture_" + secrets.token_hex(6)
        password = secrets.token_urlsafe(32)
        account = f"'{user}'@'127.0.0.1'"
        self._sql("DROP DATABASE IF EXISTS `xsoft_qa`; CREATE DATABASE `xsoft_qa` CHARACTER SET utf8mb4;")
        self._sql(f"CREATE USER {account} IDENTIFIED BY {self._sql_literal(password)}; "
                  f"GRANT ALL PRIVILEGES ON `xsoft_qa`.* TO {account};")
        try:
            self._client(dump=dump, user=user, password=password, database=self.database)
        finally:
            self._assert_owned_server()
            self._sql(f"DROP USER IF EXISTS {account};")

    def stop(self):
        process = self._process
        if process is None:
            return
        try:
            if process.poll() is None:
                try:
                    self._assert_owned_server()
                    self._sql("SHUTDOWN;")
                    process.wait(timeout=15)
                except (QAError, subprocess.TimeoutExpired):
                    # A Popen handle created here is the only permitted termination target.
                    if process.poll() is None:
                        process.terminate()
                        process.wait(timeout=15)
        finally:
            if self._log:
                self._log.close()
            self._log = None
            self._process = None

    def __enter__(self):
        return self.start()

    def __exit__(self, *_):
        self.stop()
