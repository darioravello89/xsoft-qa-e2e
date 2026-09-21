"""Disposable, local integration MySQL; separate from the product sandbox protocol.

This developer-only harness reads the installed binary but never reads its
configuration or data, nor starts/stops an installed Windows service.
"""

from __future__ import annotations

import json
import os
import re
import secrets
import socket
import subprocess
import time
import uuid
from contextlib import contextmanager
from pathlib import Path

import pymysql

from framework.paths import protect


def checked_work_path(root: Path, candidate: Path) -> Path:
    root, candidate = root.absolute(), candidate.absolute()
    work = root / "work"
    if candidate == work or not candidate.is_relative_to(work):
        raise ValueError("El datadir efímero debe permanecer dentro de repo/work.")
    for path in [candidate, *candidate.parents]:
        if path.exists() or path.is_symlink():
            attributes = getattr(path.lstat(), "st_file_attributes", 0)
            if path.is_symlink() or attributes & 0x400:
                raise ValueError("repo/work no puede contener junctions ni enlaces.")
    if not candidate.resolve().is_relative_to(work.resolve()):
        raise ValueError("El datadir efímero resuelve fuera de repo/work.")
    return candidate


class EphemeralMySQL:
    def __init__(self, root: Path, binary_path: Path | None = None):
        configured = binary_path or os.environ.get("XSOFT_SEED_MYSQL_BIN")
        if not configured:
            raise ValueError("La integración requiere XSOFT_SEED_MYSQL_BIN explícito; no busca servicios instalados.")
        self.binary = Path(configured).resolve()
        self.basedir = self.binary.parent.parent
        self.version = None
        self.directory = checked_work_path(root, root / "work" / ("seed-mysql-" + uuid.uuid4().hex))
        self.datadir = checked_work_path(root, self.directory / "data")
        self.pidfile = self.directory / "mysql.pid"
        self.password = secrets.token_hex(32)
        self.process = None
        self.log = None
        self.port = None

    def _open(self, database=None, *, dict_cursor=False):
        return pymysql.connect(host="127.0.0.1", port=self.port, user="root", password=self.password,
                               database=database, charset="utf8mb4", autocommit=False,
                               connect_timeout=2, read_timeout=10, write_timeout=10,
                               cursorclass=pymysql.cursors.DictCursor if dict_cursor else pymysql.cursors.Cursor)

    def _verify(self, connection):
        if self.process is None or self.process.poll() is not None:
            raise RuntimeError("MySQL efímero no pertenece a este proceso activo.")
        if int(self.pidfile.read_text(encoding="ascii").strip()) != self.process.pid:
            raise RuntimeError("PID inesperado en instancia efímera.")
        with connection.cursor(pymysql.cursors.Cursor) as cursor:
            cursor.execute("SELECT @@datadir, @@port, @@version")
            datadir, port, version = cursor.fetchone()
        if Path(datadir).resolve() != self.datadir.resolve() or port != self.port or version != self.version:
            raise RuntimeError("Identidad inesperada en instancia efímera.")

    @contextmanager
    def connection(self, *, dict_cursor=False):
        connection = self._open("xsoft_qa", dict_cursor=dict_cursor)
        try:
            self._verify(connection)
            yield connection
        finally:
            connection.rollback()
            connection.close()

    def start(self):
        if os.name != "nt" or self.binary.name.lower() != "mysqld.exe" or not self.binary.is_file():
            raise RuntimeError("El harness requiere un binario Windows MySQL 5.7 x64 explícito.")
        version_result = subprocess.run([str(self.binary), "--no-defaults", "--version"],
                                        capture_output=True, text=True, timeout=10,
                                        creationflags=subprocess.CREATE_NO_WINDOW, check=False)
        version_match = re.search(r"Ver (5\.7\.\d+) for Win64", version_result.stdout)
        if version_result.returncode or not version_match:
            raise RuntimeError("El harness requiere MySQL 5.7 x64; no admite MariaDB ni otra familia.")
        self.version = version_match.group(1)
        self.directory.mkdir(parents=True, exist_ok=False)
        protect(self.directory)
        self.datadir.mkdir()
        self.log = (self.directory / "mysql.log").open("wb")
        executable = str(self.binary)
        base = [executable, "--no-defaults", f"--basedir={self.basedir}", f"--datadir={self.datadir}"]
        flags = subprocess.CREATE_NO_WINDOW
        init_file = self.directory / "init.sql"
        try:
            initialized = subprocess.run([*base, "--initialize-insecure", "--explicit-defaults-for-timestamp=1"],
                                         cwd=self.directory, stdin=subprocess.DEVNULL, stdout=self.log,
                                         stderr=self.log, timeout=45, creationflags=flags, check=False)
            if initialized.returncode:
                raise RuntimeError(f"Falló inicialización efímera; evidencia privada: {self.directory}")
            with socket.socket() as probe:
                probe.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
                probe.bind(("127.0.0.1", 0))
                self.port = probe.getsockname()[1]
            if self.port == 13317:
                raise RuntimeError("El harness no usa el puerto productivo QA 13317.")
            init_file.write_text(
                f"ALTER USER 'root'@'localhost' IDENTIFIED BY '{self.password}';\n"
                f"CREATE USER 'root'@'127.0.0.1' IDENTIFIED BY '{self.password}';\n"
                "GRANT ALL PRIVILEGES ON *.* TO 'root'@'127.0.0.1' WITH GRANT OPTION;\n", encoding="utf-8")
            command = [*base, f"--port={self.port}", "--bind-address=127.0.0.1",
                       f"--pid-file={self.pidfile}", f"--init-file={init_file}", "--skip-name-resolve",
                       "--local-infile=0", "--secure-file-priv=NULL", "--general-log=0", "--skip-log-bin",
                       "--explicit-defaults-for-timestamp=1", "--console"]
            self.process = subprocess.Popen(command, cwd=self.directory, stdin=subprocess.DEVNULL,
                                            stdout=self.log, stderr=self.log, creationflags=flags)
            deadline = time.monotonic() + 30
            while time.monotonic() < deadline:
                if self.process.poll() is not None:
                    raise RuntimeError(f"MySQL efímero terminó al iniciar: {self.directory}")
                try:
                    with self._open() as connection:
                        self._verify(connection)
                        with connection.cursor() as cursor:
                            cursor.execute("CREATE DATABASE xsoft_qa CHARACTER SET utf8mb4")
                        connection.commit()
                    (self.directory / "identity.json").write_text(json.dumps({
                        "pid": self.process.pid, "port": self.port, "version": self.version,
                        "datadir": str(self.datadir), "database": "xsoft_qa"}), encoding="utf-8")
                    return self
                except (pymysql.Error, FileNotFoundError):
                    time.sleep(0.1)
            raise RuntimeError(f"MySQL efímero no quedó disponible: {self.directory}")
        except BaseException:
            self.stop()
            raise
        finally:
            init_file.unlink(missing_ok=True)

    def stop(self):
        try:
            if self.process is not None and self.process.poll() is None:
                try:
                    with self._open() as connection:
                        self._verify(connection)
                        with connection.cursor() as cursor:
                            cursor.execute("SHUTDOWN")
                    self.process.wait(timeout=10)
                except (pymysql.Error, RuntimeError, OSError, subprocess.TimeoutExpired):
                    self.process.terminate()
                    try:
                        self.process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        self.process.kill()
                        self.process.wait(timeout=5)
        finally:
            if self.log:
                self.log.close()

    def __enter__(self):
        return self.start()

    def __exit__(self, *_):
        self.stop()
