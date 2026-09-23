"""Accesibilidad con estados verificables y observación acotada de avisos."""
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from framework.errors import QAError
from products.xgestion.driver import SemanticDriver


def driver(states="enabled,visible,showing,editable,focusable"):
    item = SimpleNamespace(node=SimpleNamespace(context_info=SimpleNamespace(states=states), refresh=Mock()))
    result = SemanticDriver(Mock(), 88, {"elements": {}})
    result.find = Mock(return_value=item)
    return result


def test_manual_editability_is_observed_without_forcing_focus():
    target = driver()
    target.expect_state("editor.manual", "editable", True)
    with pytest.raises(AssertionError):
        target.expect_state("editor.manual", "editable", False)


def test_missing_accessibility_states_do_not_prove_restriction():
    with pytest.raises(QAError):
        driver("").expect_state("editor.manual", "editable", False)


def test_toggle_uses_checked_state_even_when_selected_is_absent():
    target = driver("enabled,visible,checked")
    target.expect_state("editor.manual_percent", "checked", True)
    with pytest.raises(AssertionError):
        target.expect_state("editor.manual_percent", "checked", False)
    driver("enabled,visible").expect_state("editor.manual_percent", "checked", False)


def test_button_calls_native_accessible_action_without_coordinate_fallback():
    target = driver()
    target.find.return_value.enabled = True
    target.find.return_value.node.click = Mock()
    target.click("editor.save")
    target.find.return_value.node.click.assert_called_once_with()
    target.bridge.click_element.assert_not_called()


def test_missing_native_action_blocks_and_keeps_native_output_private(capsys, caplog):
    import logging
    target = driver()
    target.find.return_value.enabled = True

    def unavailable():
        print("NATIVE-ACTION-PRIVATE-CANARY")
        logging.error("NATIVE-ACTION-PRIVATE-CANARY")
        raise NotImplementedError("NATIVE-ACTION-PRIVATE-CANARY")

    target.find.return_value.node.click = unavailable
    with pytest.raises(QAError) as error:
        target.click("editor.save")
    captured = capsys.readouterr()
    assert "CANARY" not in str(error.value) + captured.out + captured.err + caplog.text
    target.bridge.click_element.assert_not_called()


class NativeElement:
    def __init__(self, node, scaling_factor=1, index=0, column_count=None):
        self.node = node
        self.role, self.name, self.text = node.role, node.name, node.text
        self.enabled = True
        self.row = index // column_count if column_count else 0
        self.col = index % column_count if column_count else 0


@pytest.mark.parametrize("columns,values", [
    (2, ["989801", "QA-LISTA-A", "989802", "QA-LISTA-B"]),
    (3, ["4", "QA-TARJETA", "0", "5", "QA-TRANSFERENCIA", "0"]),
])
def test_table_uses_native_columns_even_when_hidden_id_shares_screen_position(columns, values):
    children = [SimpleNamespace(role="label", name=value, text="",
                                context_info=SimpleNamespace(indexInParent=index, x=100, y=40))
                for index, value in enumerate(values)]
    node = SimpleNamespace(role="table", name="", text="", children=children, refresh=Mock(),
                           context_info=SimpleNamespace(childrenCount=len(children)),
                           table=SimpleNamespace(table=SimpleNamespace(rowCount=2, columnCount=columns)))
    target = driver()
    target.find.return_value = NativeElement(node)
    # RPA 33 infers one column from equal x coordinates, even for a hidden ID column.
    target.bridge.read_table.return_value = [[SimpleNamespace(text=value, name="")] for value in values]
    assert target.table_rows("payment_picker.lines") == [values[:columns], values[columns:]]
    target.bridge.read_table.assert_not_called()


def test_choice_reads_selected_accessible_child_instead_of_combo_label():
    target = driver()
    node = target.find.return_value.node
    node.context = 17
    node.context_info.accessibleSelection = True
    node._jab_wrapper = Mock()
    node._jab_wrapper.get_accessible_selection_count_from_context.return_value = 1
    node._jab_wrapper.get_accessible_selection_from_context.return_value = 31
    node._jab_wrapper.get_context_info.return_value.name = "989902|QA-PRM-TRANSFERENCIA"
    target.expect_choice("payment.method", ("989902|QA-PRM-TRANSFERENCIA", "QA-PRM-TRANSFERENCIA"))
    node._jab_wrapper.get_accessible_selection_from_context.assert_called_once_with(17, 0)


def test_notice_absence_requires_continuous_bounded_observation(monkeypatch):
    import products.xgestion.driver as module
    tick = [0.0]
    monkeypatch.setattr(module.time, "monotonic", lambda: tick[0])
    monkeypatch.setattr(module.time, "sleep", lambda seconds: tick.__setitem__(0, tick[0] + seconds))
    target = driver()
    target._present = Mock(return_value=False)
    action = Mock()
    target.observe_notice("editor.manual_warning", action, expected=False, duration=1, max_gap=.5)
    action.assert_called_once()
    assert target._present.call_count >= 10


def test_slow_action_cannot_prove_absence(monkeypatch):
    import products.xgestion.driver as module
    tick = [0.0]
    monkeypatch.setattr(module.time, "monotonic", lambda: tick[0])
    target = driver()
    target._present = Mock(return_value=False)
    with pytest.raises(QAError, match="observaci"):
        target.observe_notice("editor.manual_warning", lambda: tick.__setitem__(0, 2),
                              expected=False, duration=4, max_gap=1)


def test_notice_unexpected_is_functional_failure(monkeypatch):
    import products.xgestion.driver as module
    monkeypatch.setattr(module.time, "monotonic", lambda: 0)
    target = driver()
    target._present = Mock(side_effect=[False, True])
    with pytest.raises(AssertionError):
        target.observe_notice("editor.manual_warning", Mock(), expected=False)

