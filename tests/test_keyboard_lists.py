"""Pruebas sintéticas de los límites de evidencia del recorrido JAB."""

import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from framework.errors import QAError
from products.xgestion.driver import SemanticDriver
from products.xgestion.keyboard_lists import KeyboardListsLibrary, assert_single_reload, validate_case


def test_shortcut_requires_real_jab_focus_and_never_requests_it():
    node = Mock()
    node.context_info.states = "enabled,visible"
    bridge = Mock()
    driver = SemanticDriver(bridge, 42, {})
    driver.find = Mock(return_value=SimpleNamespace(node=node))
    with pytest.raises(QAError, match="foco previo"):
        driver.press_focused("list.search", "ctrl+b")
    node.request_focus.assert_not_called()
    bridge.press_keys.assert_not_called()


def test_shortcut_only_sends_approved_chord_to_focused_control():
    node = Mock()
    node.context_info.states = "enabled,focused,showing"
    bridge = Mock()
    driver = SemanticDriver(bridge, 42, {})
    driver.find = Mock(return_value=SimpleNamespace(node=node))
    driver.press_focused("list.table", "ctrl+f")
    bridge.press_keys.assert_called_once_with("ctrl", "f")
    node.request_focus.assert_not_called()
    with pytest.raises(QAError, match="fuera del contrato"):
        driver.press_focused("list.table", "alt+f4")


def test_selected_identity_rejects_incomplete_or_ambiguous_jab_selection():
    bridge = Mock()
    driver = SemanticDriver(bridge, 42, {})

    def cell(name, selected):
        node = Mock()
        node.context_info.states = "selected,showing" if selected else "showing"
        return SimpleNamespace(text=name, name=name, node=node)

    driver._table_cells = Mock(return_value=(None, [[cell("A", True)], [cell("B", True)]], 2, 1))
    with pytest.raises(QAError, match="una sola fila"):
        driver.selected_row_identity("list.table", 0)
    driver._table_cells.return_value = (None, [[cell("", True)]], 1, 1)
    with pytest.raises(QAError, match="identidad visible"):
        driver.selected_row_identity("list.table", 0)
    driver._table_cells.return_value = (None, [[cell("A", False)]], 1, 1)
    assert driver.selected_row_identities("list.table", 0) == []


@pytest.mark.parametrize("before,after,error", [
    ("3", "3", AssertionError), ("3", "5", AssertionError),
    ("", "4", QAError), ("3", "?", QAError),
])
def test_filter_reload_requires_one_complete_signal(before, after, error):
    with pytest.raises(error):
        assert_single_reload(before, after)
    assert_single_reload("3", "4")


def test_case_with_no_private_baseline_cannot_run():
    with pytest.raises(QAError, match="perfil privado"):
        validate_case("XG-KEY-001", None, {})
    with pytest.raises(QAError, match="N01-N12"):
        validate_case("XG-KEY-001", {"search": "only a placeholder"}, {})


def test_wrong_row_is_not_treated_as_success():
    library = KeyboardListsLibrary()
    library.driver = Mock()
    library.driver.selected_row_identity.return_value = "QA-A"
    with pytest.raises(AssertionError, match="otro registro"):
        library._selected({"table": "table", "identity_column": 0}, "QA-B")
    library.driver.expect_focus.assert_not_called()


def test_public_examples_cover_all_13_but_cannot_be_used_as_verified_profiles():
    path = Path(__file__).resolve().parents[1] / "products/xgestion/examples/keyboard-lists-fixtures.example.json"
    data = json.loads(path.read_text(encoding="utf-8"))["keyboard_lists"]["cases"]
    assert len(data) == 13
    assert all(case in data for case in (f"XG-KEY-{number:03}" for number in range(1, 14)))
    with pytest.raises(QAError, match="sin calibrar"):
        validate_case("XG-KEY-005", data["XG-KEY-005"], {})


def test_private_contract_shape_can_represent_each_screen_without_indices():
    examples = Path(__file__).resolve().parents[1] / "products/xgestion/examples"
    fixture = json.loads((examples / "keyboard-lists-fixtures.example.json").read_text(encoding="utf-8"))
    locators = json.loads((examples / "keyboard-lists-locators.example.json").read_text(encoding="utf-8"))

    def calibrated(value):
        if isinstance(value, str):
            return value.replace("CALIBRAR", "QA_VERIFICADO")
        if isinstance(value, list):
            return [calibrated(item) for item in value]
        if isinstance(value, dict):
            return {key: calibrated(item) for key, item in value.items()}
        return value

    fixture, locators = calibrated(fixture), calibrated(locators)
    for case_id, data in fixture["keyboard_lists"]["cases"].items():
        assert validate_case(case_id, data, locators) is data


def test_no_filter_modal_rejects_owned_java_dialog():
    library = KeyboardListsLibrary()
    library.driver = Mock(pid=42)
    library.bridge = Mock()
    library.bridge.list_java_windows.return_value = [SimpleNamespace(pid=42, title="Filtros - Clientes")]
    with pytest.raises(AssertionError, match="modal"):
        library._no_filter_modal({"search": "search", "table": "table"})


def test_open_selected_checks_independent_destination_before_closing():
    library = KeyboardListsLibrary()
    library.driver = Mock()
    library._selected = Mock()
    library.driver.expect.side_effect = AssertionError("identidad incorrecta")
    data = {"table": "table", "detail_close": "close", "details": {
        "QA-A": {"detail.name": "QA-A", "detail.document": "DOC-QA-A"},
    }}
    with pytest.raises(AssertionError, match="identidad incorrecta"):
        library._open_selected(data, "QA-A")
    library.driver.click.assert_not_called()


def test_filter_apply_is_reached_and_activated_only_by_keyboard():
    library = KeyboardListsLibrary()
    library.driver = Mock()
    modal = {"focus_order": ["field", "apply", "cancel"], "apply": "apply"}
    library._activate_filter(modal, "apply")
    assert library.driver.press_focused.call_args_list[0].args == ("field", "tab")
    assert library.driver.press_focused.call_args_list[1].args == ("apply", "enter")
    library.driver.click.assert_not_called()


def test_filter_value_compares_exact_selected_option():
    library = KeyboardListsLibrary()
    library.driver = Mock()
    library.driver.choice_text.return_value = "Zona Norte"
    with pytest.raises(AssertionError, match="valor esperado"):
        library._expect_filter_value({"alias": "filters.zone", "kind": "choice", "b": "Norte"}, "b")
    library.driver.text.assert_not_called()
