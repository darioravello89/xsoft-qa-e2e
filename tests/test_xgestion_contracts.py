import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from products.xgestion.contracts import REQUIRED_ELEMENTS, load_assets


class ProfileStub:
    def __init__(self, root):
        self.root = root

    def asset(self, key):
        return self.root / {"app": "app.jar", "fixtures": "fixtures.json", "locators": "locators.json"}[key]


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.profile = ProfileStub(Path(self.tmp.name))
        self.profile.asset("app").write_bytes(b"qa-only-candidate")
        self.fixture = {
            "schema_version": 1,
            "context": {"empresa": 91, "sucursal": 2, "computadora": 3, "usuario_id": 7,
                        "empresa_label": "Empresa QA", "sucursal_label": "Sucursal QA", "usuario_label": "7-qa"},
            "product": {"id": 11, "code": "QA-001", "name": "Producto QA", "unit_price": "1000.00", "quantity": 2},
            "sale": {"cash_payment_id": 1, "non_fiscal_document_id": 99},
            "nonexistent_product_code": "QA-NO-EXISTE",
            "ui": {"products_empty_text": "0"},
        }
        self.locators = {
            "schema_version": 1,
            "calibration": {"status": "verified", "app_sha256": hashlib.sha256(b"qa-only-candidate").hexdigest(),
                            "verified_by": "qa", "verified_at": "2026-09-19T12:00:00Z", "jab_version": "test"},
            "windows": {"main": "XGESTION QA"},
            "elements": {name: {"window": "main", "query": "role:label and name:" + name}
                         for name in REQUIRED_ELEMENTS},
        }

    def write(self):
        self.profile.asset("fixtures").write_text(json.dumps(self.fixture), encoding="utf-8")
        self.profile.asset("locators").write_text(json.dumps(self.locators), encoding="utf-8")

    def test_accepts_only_complete_verified_matching_candidate(self):
        self.write()
        self.assertEqual(load_assets(self.profile)[0]["product"]["quantity"], 2)

    def test_draft_and_wrong_jar_block(self):
        self.locators["calibration"]["status"] = "draft"
        self.write()
        with self.assertRaisesRegex(Exception, "calibraci"):
            load_assets(self.profile)
        self.locators["calibration"]["status"] = "verified"
        self.locators["calibration"]["app_sha256"] = "0" * 64
        self.write()
        with self.assertRaisesRegex(Exception, "SHA256"):
            load_assets(self.profile)

    def test_missing_selector_and_fiscal_document_block(self):
        self.locators["elements"].pop(REQUIRED_ELEMENTS[0])
        self.write()
        with self.assertRaisesRegex(Exception, "locator"):
            load_assets(self.profile)
        self.locators["elements"][REQUIRED_ELEMENTS[0]] = {"window": "main", "query": "role:label and name:ok"}
        self.fixture["sale"]["non_fiscal_document_id"] = 1
        self.write()
        with self.assertRaisesRegex(Exception, "fiscal"):
            load_assets(self.profile)

    def test_invalid_fixture_still_blocks_under_python_optimization(self):
        result = subprocess.run(
            [sys.executable, "-O", "-c", "from products.xgestion.contracts import validate_fixtures; validate_fixtures({})"],
            cwd=Path(__file__).resolve().parents[1], capture_output=True, text=True, check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("QAError", result.stderr)
        self.assertIn("fixtures.json", result.stderr)


if __name__ == "__main__":
    unittest.main()
