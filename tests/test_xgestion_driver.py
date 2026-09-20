import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from products.xgestion.driver import JarProcess, SemanticDriver


class DriverTests(unittest.TestCase):
    def test_label_uses_accessible_name_but_empty_password_does_not(self):
        bridge = Mock()
        bridge.get_element_text.return_value = ""
        driver = SemanticDriver(bridge, 42, {})
        driver.find = Mock(return_value=SimpleNamespace(name="Empresa QA", role="label"))
        self.assertEqual(driver.text("label"), "Empresa QA")
        driver.find.return_value = SimpleNamespace(name="Contraseña", role="password text")
        self.assertEqual(driver.text("password"), "")

    def test_ambiguous_selector_never_clicks_first_match(self):
        jab = Mock()
        jab.list_java_windows.return_value = [SimpleNamespace(pid=42, title="QA")]
        jab.get_elements.return_value = [SimpleNamespace(showing=True), SimpleNamespace(showing=True)]
        driver = SemanticDriver(jab, 42, {"windows": {"main": "QA"},
            "elements": {"button": {"window": "main", "query": "role:push button and name:Guardar"}}})
        with self.assertRaisesRegex(Exception, "ambiguo"):
            driver.find("button", timeout=0)
        jab.click_element.assert_not_called()

    def test_foreign_window_with_same_title_blocks(self):
        jab = Mock()
        jab.list_java_windows.return_value = [SimpleNamespace(pid=42, title="QA"), SimpleNamespace(pid=99, title="QA")]
        driver = SemanticDriver(jab, 42, {"windows": {"main": "QA"},
            "elements": {"button": {"window": "main", "query": "role:push button"}}})
        with self.assertRaisesRegex(Exception, "otra instancia"):
            driver.find("button", timeout=0)
        jab.select_window_by_title.assert_not_called()

    def test_launch_never_puts_credentials_in_arguments_or_logs(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "bin").mkdir()
            (root / "bin" / "java.exe").touch()
            (root / "app").mkdir()
            (root / "app" / "config.properties").touch()
            (root / "candidate.jar").touch()
            profile = SimpleNamespace(runtime=root, asset=lambda _: root / "candidate.jar",
                                      env=lambda name, default=None: str(root))
            child = Mock(pid=42)
            with patch("products.xgestion.driver.subprocess.Popen", return_value=child) as popen, \
                 patch.dict("os.environ", {"JAVA_TOOL_OPTIONS": "-javaagent:foreign.jar", "QA_LOGIN_PASSWORD": "secret"}):
                managed = JarProcess(profile)
                managed.start()
                args, kwargs = popen.call_args
                self.assertEqual(args[0][-2:], ["-jar", str(root / "candidate.jar")])
                self.assertEqual(kwargs["stdout"], subprocess.DEVNULL)
                self.assertEqual(kwargs["stderr"], subprocess.DEVNULL)
                self.assertFalse(kwargs["shell"])
                self.assertNotIn("JAVA_TOOL_OPTIONS", kwargs["env"])
                self.assertNotIn("QA_LOGIN_PASSWORD", kwargs["env"])
                child.poll.return_value = None
                managed.stop()
                child.terminate.assert_called_once()
                managed.stop()
                child.terminate.assert_called_once()


if __name__ == "__main__":
    unittest.main()
