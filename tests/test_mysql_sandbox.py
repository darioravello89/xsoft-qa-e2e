"""Guardrails for the private fixture server. Never starts a real database."""

import hashlib
import json
import socket
import tempfile
import unittest
import zipfile
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from framework.errors import QAError
from framework.fixtures.mysql import MySQLSandbox, extract_mysql_zip


class SandboxTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        runtime = root / ".local" / "xgestion"
        self.profile = SimpleNamespace(
            root=root,
            runtime=runtime,
            bundle=runtime / "bundle",
            manifest={"mysql_version": "5.7.44"},
            env=lambda key, default=None: {"QA_DB_PASSWORD": "local-test-password"}.get(key, default),
        )

    def test_rejects_runtime_outside_repository_before_any_process(self):
        self.profile.runtime = self.profile.root.parent / "foreign"
        with self.assertRaises(QAError), patch("subprocess.Popen") as process:
            MySQLSandbox(self.profile)
        process.assert_not_called()

    def test_rejects_existing_datadir_without_owner(self):
        sandbox = MySQLSandbox(self.profile)
        sandbox.datadir.mkdir(parents=True)
        (sandbox.datadir / "important.db").write_text("keep")
        with self.assertRaises(QAError):
            sandbox._prepare_datadir()
        self.assertEqual((sandbox.datadir / "important.db").read_text(), "keep")

    def test_rejects_occupied_port_without_starting_server(self):
        sandbox = MySQLSandbox(self.profile)
        with socket.socket() as occupied:
            occupied.bind(("127.0.0.1", 0))
            occupied.listen()
            sandbox.port = occupied.getsockname()[1]
            with self.assertRaises(QAError), patch("subprocess.Popen") as process:
                sandbox._assert_port_available()
            process.assert_not_called()

    def test_restore_requires_process_created_by_this_instance(self):
        sandbox = MySQLSandbox(self.profile)
        with self.assertRaises(QAError), patch.object(sandbox, "_sql") as query:
            sandbox.restore()
        query.assert_not_called()

    def test_stop_never_kills_a_pid_read_from_disk(self):
        sandbox = MySQLSandbox(self.profile)
        sandbox.runtime.mkdir(parents=True)
        sandbox.pidfile.write_text("12345")
        with patch("os.kill") as kill:
            sandbox.stop()
        kill.assert_not_called()
        self.assertTrue(sandbox.pidfile.exists())

    def test_rejects_owner_pointing_to_other_database(self):
        sandbox = MySQLSandbox(self.profile)
        sandbox.runtime.mkdir(parents=True)
        sandbox.ownerfile.write_text(json.dumps({"datadir": "C:/production"}))
        with self.assertRaises(QAError):
            sandbox._verify_owner()

    def test_rejects_wrong_server_datadir_before_destructive_sql(self):
        sandbox = MySQLSandbox(self.profile)
        sandbox._process = Mock(pid=3456)
        sandbox._process.poll.return_value = None
        sandbox.runtime.mkdir(parents=True)
        sandbox.pidfile.write_text("3456")
        with patch.object(sandbox, "_verify_owner"), patch.object(
            sandbox, "_sql", return_value="C:/production\t13317\t5.7.44\n"
        ) as query:
            with self.assertRaises(QAError):
                sandbox._assert_owned_server()
        self.assertEqual(query.call_count, 1)
        self.assertNotIn("DROP", query.call_args.args[0])

    def test_zip_rejects_traversal_and_does_not_write_outside(self):
        archive = self.profile.root / "bad.zip"
        with zipfile.ZipFile(archive, "w") as output:
            output.writestr("../escaped", "bad")
        with self.assertRaises(QAError):
            extract_mysql_zip(archive, self.profile.runtime / "mysql")
        self.assertFalse((self.profile.runtime / "escaped").exists())

    def test_zip_rejects_case_collisions(self):
        archive = self.profile.root / "bad.zip"
        with zipfile.ZipFile(archive, "w") as output:
            output.writestr("bin/mysql.exe", "one")
            output.writestr("bin/MYSQL.exe", "two")
        with self.assertRaises(QAError):
            extract_mysql_zip(archive, self.profile.runtime / "mysql")

    def test_zip_rejects_windows_devices(self):
        archive = self.profile.root / "bad.zip"
        with zipfile.ZipFile(archive, "w") as output:
            output.writestr("mysql/CON.txt", "bad")
        with self.assertRaises(QAError):
            extract_mysql_zip(archive, self.profile.runtime / "mysql")

    def test_password_is_only_in_private_option_file_not_command_or_environment(self):
        sandbox = MySQLSandbox(self.profile)
        captured = []

        @contextmanager
        def private_file(content):
            captured.append(content)
            yield sandbox.runtime / "private" / "options.cnf"

        result = SimpleNamespace(returncode=0, stdout=b"1\n")
        with patch.object(sandbox, "_secret_file", private_file), patch(
            "subprocess.run", return_value=result
        ) as run:
            self.assertEqual(sandbox._sql("SELECT 1;"), "1\n")
        self.assertIn(self.profile.env("QA_DB_PASSWORD"), captured[0])
        self.assertNotIn(self.profile.env("QA_DB_PASSWORD"), " ".join(run.call_args.args[0]))
        self.assertNotIn("MYSQL_PWD", run.call_args.kwargs["env"])
        self.assertIn("--binary-mode", run.call_args.args[0])
        self.assertIn("--local-infile=0", run.call_args.args[0])

    def test_private_option_file_is_removed_when_operation_fails(self):
        sandbox = MySQLSandbox(self.profile)
        temporary = None
        with self.assertRaisesRegex(RuntimeError, "simulated"):
            with sandbox._secret_file("private-test-marker") as temporary:
                self.assertEqual(temporary.read_text(), "private-test-marker")
                raise RuntimeError("simulated client failure")
        self.assertIsNotNone(temporary)
        self.assertFalse(temporary.exists())

    def test_zip_accepts_official_top_directory_layout(self):
        archive = self.profile.root / "mysql.zip"
        with zipfile.ZipFile(archive, "w") as output:
            output.writestr("mysql-5.7.44-winx64/bin/mysql.exe", "client")
            output.writestr("mysql-5.7.44-winx64/bin/mysqld.exe", "server")
        target = self.profile.runtime / "mysql"
        extract_mysql_zip(archive, target)
        self.assertEqual((target / "bin" / "mysql.exe").read_text(), "client")

    def test_existing_binary_install_requires_matching_archive(self):
        archive = self.profile.root / "mysql.zip"
        with zipfile.ZipFile(archive, "w") as output:
            output.writestr("bin/mysql.exe", "client")
            output.writestr("bin/mysqld.exe", "server")
        target = self.profile.runtime / "mysql"
        extract_mysql_zip(archive, target)
        digest = hashlib.sha256(archive.read_bytes()).hexdigest()
        self.assertEqual(json.loads((target / ".qa-archive.json").read_text())["sha256"], digest)
        with zipfile.ZipFile(archive, "a") as output:
            output.writestr("changed", "new")
        with self.assertRaises(QAError):
            extract_mysql_zip(archive, target)


if __name__ == "__main__":
    unittest.main()
