"""MySQL proof of the restore DEFINER lifecycle; never points at an installed service."""

import os
import secrets
from pathlib import Path

import pymysql
import pytest
from seed_mysql_runtime import EphemeralMySQL

ROOT = Path(__file__).resolve().parents[1]
pytestmark = pytest.mark.skipif(
    os.name != "nt" or not os.environ.get("XSOFT_SEED_MYSQL_BIN"),
    reason="Requiere Windows y XSOFT_SEED_MYSQL_BIN explícito; usa datadir y puerto efímeros propios",
)


def test_limited_locked_definer_preserves_triggers_login_block_and_transaction_rollback():
    """DROP USER reproduces the old failure; retaining ACCOUNT LOCK fixes the same objects."""
    account = "fixture_" + secrets.token_hex(6)
    password = secrets.token_hex(32)
    with EphemeralMySQL(ROOT) as server, server.connection() as admin:
        with admin.cursor() as root:
            root.execute("CREATE DATABASE xsoftXqa")
            root.execute("CREATE TABLE xsoftXqa.unrelated (id INT PRIMARY KEY) ENGINE=InnoDB")
            root.execute("CREATE USER %s@'127.0.0.1' IDENTIFIED BY %s", (account, password))
            root.execute("GRANT ALL PRIVILEGES ON `xsoft\\_qa`.* TO %s@'127.0.0.1'", (account,))

        def imported_connection():
            return pymysql.connect(host="127.0.0.1", port=server.port, user=account, password=password,
                                   database="xsoft_qa", autocommit=False, connect_timeout=2)

        with imported_connection() as importer, importer.cursor() as cursor:
            cursor.execute("CREATE TABLE probe_business (id INT PRIMARY KEY) ENGINE=InnoDB")
            cursor.execute("CREATE TABLE probe_queue (id INT PRIMARY KEY) ENGINE=InnoDB")
            cursor.execute("CREATE FUNCTION fixture_send(value_id INT) RETURNS INT MODIFIES SQL DATA "
                           "SQL SECURITY DEFINER BEGIN INSERT INTO probe_queue VALUES (value_id); RETURN 1; END")
            cursor.execute("CREATE TRIGGER fixture_business_insert AFTER INSERT ON probe_business FOR EACH ROW "
                           "BEGIN SELECT fixture_send(NEW.id) INTO @fixture_result; END")
            # The importer cannot assign a privileged definer or read system users.
            with pytest.raises(pymysql.Error) as privileged_definer:
                cursor.execute("CREATE DEFINER='root'@'localhost' FUNCTION disallowed_definer() "
                               "RETURNS INT DETERMINISTIC RETURN 1")
            assert privileged_definer.value.args[0] == 1227
            with pytest.raises(pymysql.Error):
                cursor.execute("SELECT User FROM mysql.user")
            with pytest.raises(pymysql.Error):
                cursor.execute("SELECT id FROM xsoftXqa.unrelated")

        with admin.cursor() as root:
            root.execute("DROP USER %s@'127.0.0.1'", (account,))
            with pytest.raises(pymysql.Error) as orphan:
                root.execute("INSERT INTO probe_business VALUES (1)")
            assert orphan.value.args[0] == 1449
            admin.rollback()
            # Same objects, same limited definer identity, now retained and login-locked.
            root.execute("CREATE USER %s@'127.0.0.1' IDENTIFIED BY %s ACCOUNT LOCK", (account, password))
            root.execute("GRANT ALL PRIVILEGES ON `xsoft\\_qa`.* TO %s@'127.0.0.1'", (account,))
            root.execute("INSERT INTO probe_business VALUES (2)")
            admin.commit()
            root.execute("INSERT INTO probe_business VALUES (3)")
            for table in ("probe_business", "probe_queue"):
                root.execute(f"SELECT COUNT(*) FROM {table}")
                assert root.fetchone() == (2,)
            admin.rollback()
            for table in ("probe_business", "probe_queue"):
                root.execute(f"SELECT id FROM {table}")
                assert root.fetchall() == ((2,),)
        with pytest.raises(pymysql.Error) as locked_login:
            imported_connection()
        assert locked_login.value.args[0] == 3118
