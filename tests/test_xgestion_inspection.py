import unittest
from types import SimpleNamespace

from products.xgestion.inspection import safe_nodes, sanitize


class InspectionTests(unittest.TestCase):
    def test_editable_fields_never_export_name_description_or_text(self):
        node = SimpleNamespace(role="password text", name="secret", description="secret", text="secret",
                               ancestry=2, indexInParent=4)
        data = safe_nodes([node], ["secret"])[0]
        self.assertNotIn("text", data)
        self.assertEqual(data["name"], "[campo omitido]")
        self.assertEqual(data["description"], "")
        self.assertEqual(data["indexInParent"], 4)

    def test_secrets_in_label_are_also_redacted(self):
        self.assertEqual(sanitize("Usuario: qa-password", ["qa", "qa-password"]), "Usuario: [redactado]")


if __name__ == "__main__":
    unittest.main()
