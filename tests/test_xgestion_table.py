"""Lecturas completas y teclas dirigidas al control propio, sin publicar sus datos."""

import logging
import sys
import traceback
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest

from framework.errors import QAError
from products.xgestion.driver import SemanticDriver

ALIAS = "sale.lines"
CANARY = "PRIVATE_CELL_CANARY"


def make_driver(row_count=2, column_count=2):
    node = SimpleNamespace(
        table=SimpleNamespace(table=SimpleNamespace(rowCount=row_count, columnCount=column_count)),
        context_info=SimpleNamespace(states="enabled,showing,focused"),
        refresh=Mock(), request_focus=Mock(),
    )
    element = SimpleNamespace(node=node, role="table", showing=True, enabled=True)
    bridge = Mock()
    bridge.list_java_windows.return_value = [SimpleNamespace(pid=42, title="QA")]
    bridge.get_elements.return_value = [element]
    bridge.read_table.return_value = [
        [SimpleNamespace(text="  A  ", name="ignored"), SimpleNamespace(text="", name="B")],
        [SimpleNamespace(text=None, name="C"), SimpleNamespace(text="D", name="ignored", showing=False)],
    ]
    driver = SemanticDriver(bridge, 42, {"windows": {"main": "QA"},
                                       "elements": {ALIAS: {"window": "main", "query": "role:table"}}})
    return driver, bridge, element


def test_table_reads_all_cells_and_falls_back_to_accessible_name():
    driver, bridge, element = make_driver()
    assert driver.table_rows(ALIAS) == [["A", "B"], ["C", "D"]]
    element.node.refresh.assert_called_once()
    bridge.get_elements.assert_called_once_with("role:table", java_elements=True, strict=True)
    bridge.read_table.assert_called_once_with(element, visible_only=False)


def test_empty_table_uses_refreshed_native_size_without_rpa_empty_table_error():
    driver, bridge, element = make_driver()
    element.node.refresh.side_effect = lambda: setattr(element.node.table.table, "rowCount", 0)
    bridge.read_table.side_effect = RuntimeError("RPA cannot infer columns from an empty table")
    assert driver.table_rows(ALIAS) == []
    bridge.read_table.assert_not_called()


@pytest.mark.parametrize("rows", [[], [["A", "B"]], [["A"], ["C", "D"]],
                                  [["A", "B", "C"], ["D", "E", "F"]],
                                  [["A", "B"], ["C", "D"], ["E", "F"]]])
def test_partial_or_inconsistent_grid_is_never_accepted(rows):
    driver, bridge, _ = make_driver()
    bridge.read_table.return_value = [[SimpleNamespace(text=value, name="") for value in row] for row in rows]
    with pytest.raises(QAError, match="incompleta"):
        driver.table_rows(ALIAS)


def test_native_size_changing_during_read_is_rejected():
    driver, bridge, element = make_driver()
    cells = bridge.read_table.return_value

    def changing_table(*_args, **_kwargs):
        element.node.table.table.rowCount = 3
        return cells

    bridge.read_table.side_effect = changing_table
    with pytest.raises(QAError, match="incompleta"):
        driver.table_rows(ALIAS)


@pytest.mark.parametrize("rows,columns", [(-1, 2), (1, 0), (1, -1), (True, 2), ("2", 2)])
def test_invalid_native_dimensions_block_before_read(rows, columns):
    driver, bridge, _ = make_driver(rows, columns)
    with pytest.raises(QAError, match="dimensiones"):
        driver.table_rows(ALIAS)
    bridge.read_table.assert_not_called()


def test_non_table_control_is_not_an_empty_table():
    driver, bridge, element = make_driver(0, 0)
    element.role = "label"
    with pytest.raises(QAError, match="tabla"):
        driver.table_rows(ALIAS)
    bridge.read_table.assert_not_called()


@pytest.mark.parametrize("method", ["table_rows", "keys"])
@pytest.mark.parametrize("unsafe", ["ambiguous", "foreign"])
def test_table_and_keys_keep_selector_uniqueness_and_process_ownership(method, unsafe):
    driver, bridge, element = make_driver()
    if unsafe == "ambiguous":
        bridge.get_elements.return_value = [element, element]
    else:
        bridge.list_java_windows.return_value.append(SimpleNamespace(pid=99, title="QA"))
    with pytest.raises(QAError, match="ambiguo|otra instancia"):
        getattr(driver, method)(ALIAS, *(("tab",) if method == "keys" else ()))
    bridge.read_table.assert_not_called()
    element.node.request_focus.assert_not_called()
    bridge.press_keys.assert_not_called()


def noise():
    logging.getLogger("RPA.JavaAccessBridge").error(CANARY)
    print(CANARY)
    print(CANARY, file=sys.stderr)


@pytest.mark.parametrize("failure", [False, True])
def test_table_native_output_and_exceptions_never_publish_cell_contents(capsys, caplog, failure):
    driver, bridge, element = make_driver(1, 1)

    class Cell:
        @property
        def text(self):
            noise()
            return CANARY

    def read(*_args, **_kwargs):
        noise()
        if failure:
            raise RuntimeError(CANARY)
        return [[Cell()]]

    def find(*_args, **_kwargs):
        noise()
        return [element]

    bridge.get_elements.side_effect = find
    element.node.refresh.side_effect = noise
    bridge.read_table.side_effect = read
    prior_disable = logging.root.manager.disable
    builtin = Mock()
    builtin.set_log_level.return_value = "TRACE"
    with patch("robot.libraries.BuiltIn.BuiltIn", return_value=builtin), \
            patch("products.xgestion.driver.diagnostic") as diagnostic:
        if failure:
            with pytest.raises(QAError) as caught:
                driver.table_rows(ALIAS)
            assert CANARY not in "".join(traceback.format_exception(caught.value))
        else:
            assert driver.table_rows(ALIAS) == [[CANARY]]
            assert diagnostic.call_args.kwargs == {"control": ALIAS, "row_count": 1, "column_count": 1}
    assert CANARY not in str(diagnostic.call_args_list)
    assert CANARY not in caplog.text
    captured = capsys.readouterr()
    assert CANARY not in captured.out + captured.err
    assert logging.root.manager.disable == prior_disable
    assert [call.args for call in builtin.set_log_level.call_args_list] == [("NONE",), ("TRACE",)]


@pytest.mark.parametrize("key", ["tab", "esc", "TAB", "ESC"])
def test_keys_require_native_focus_before_sending_a_single_allowed_key(key):
    driver, bridge, element = make_driver()
    element.node.context_info.states = "enabled,showing"
    element.node.refresh.side_effect = lambda: setattr(element.node.context_info, "states", "showing, focused")
    driver.keys(ALIAS, key)
    element.node.request_focus.assert_called_once()
    element.node.refresh.assert_called_once()
    bridge.press_keys.assert_called_once_with(key.lower())


@pytest.mark.parametrize("keys", [(), ("a",), (CANARY,), ("ctrl", "a"), ("tab", "esc"), (None,)])
def test_keys_reject_text_and_chords_before_interacting(keys):
    driver, bridge, element = make_driver()
    with pytest.raises(QAError) as caught:
        driver.keys(ALIAS, *keys)
    assert CANARY not in str(caught.value)
    bridge.list_java_windows.assert_not_called()
    element.node.request_focus.assert_not_called()
    bridge.press_keys.assert_not_called()


def test_keys_never_go_to_disabled_control_or_unconfirmed_focus():
    driver, bridge, element = make_driver()
    element.enabled = False
    with pytest.raises(QAError, match="deshabilitado"):
        driver.keys(ALIAS, "tab")
    element.node.request_focus.assert_not_called()
    element.enabled = True
    element.node.context_info.states = "enabled,not focused"
    with patch("products.xgestion.driver.time.monotonic", side_effect=[0, 0, 0, 0, 21]), \
            patch("products.xgestion.driver.time.sleep"):
        with pytest.raises(QAError, match="foco"):
            driver.keys(ALIAS, "esc")
    bridge.press_keys.assert_not_called()


@pytest.mark.parametrize("stage", ["request_focus", "refresh", "press_keys"])
def test_native_key_failures_restore_logging_without_exposing_control_contents(stage, capsys, caplog):
    driver, bridge, element = make_driver()

    def fail(*_args, **_kwargs):
        noise()
        raise RuntimeError(CANARY)

    target = bridge if stage == "press_keys" else element.node
    getattr(target, stage).side_effect = fail
    previous = logging.root.manager.disable
    with patch("products.xgestion.driver.diagnostic") as diagnostic:
        with pytest.raises(QAError) as caught:
            driver.keys(ALIAS, "tab")
    assert CANARY not in "".join(traceback.format_exception(caught.value))
    assert CANARY not in str(diagnostic.call_args_list)
    captured = capsys.readouterr()
    assert CANARY not in captured.out + captured.err + caplog.text
    assert logging.root.manager.disable == previous
    if stage != "press_keys":
        bridge.press_keys.assert_not_called()


class EditableCell:
    """JavaElement conserva propiedades copiadas; hay que reconstruir tras refresh."""

    def __init__(self, node, scaling_factor=None):
        self.node = node
        self.text, self.name = node.text_value, node.name_value
        self.enabled, self.visible, self.showing = node.enabled, node.visible, node.showing
        self.x = int(node.x * (scaling_factor or 1))
        self.y = int(node.y * (scaling_factor or 1))
        self.width = int(node.width * (scaling_factor or 1))
        self.height = int(node.height * (scaling_factor or 1))


def editable_driver():
    driver, bridge, table = make_driver()
    node = SimpleNamespace(text_value=CANARY, name_value="", enabled=True, visible=True,
                           showing=True, x=50, y=80, width=100, height=20, refresh=Mock())
    target = EditableCell(node)
    bridge.display_scale_factor = 1.5
    bridge.read_table.return_value[1][0] = target
    return driver, bridge, table, target


def test_edit_sale_row_uses_unique_code_and_refreshed_scaled_cell_geometry():
    driver, bridge, _, target = editable_driver()
    target.node.refresh.side_effect = lambda: setattr(target.node, "x", 200)
    with patch("products.xgestion.driver.diagnostic") as diagnostic:
        driver.edit_sale_row(ALIAS, 0, CANARY)
    target.node.refresh.assert_called_once()
    clicked = bridge.click_element.call_args.args[0]
    assert clicked is not target and clicked.node is target.node
    assert clicked.x == 300 and clicked.width == 150
    assert clicked.text == CANARY
    assert bridge.click_element.call_args.kwargs == {"action": False, "click_type": "double click"}
    assert CANARY not in str(diagnostic.call_args_list)


@pytest.mark.parametrize("state", ["wrong_code", "duplicate_code", "missing_cell", "empty", "foreign"])
def test_edit_sale_row_blocks_without_a_unique_complete_owned_row(state):
    driver, bridge, table, target = editable_driver()
    if state == "wrong_code":
        target.text = "ANOTHER"
    elif state == "duplicate_code":
        bridge.read_table.return_value[0][0] = target
    elif state == "missing_cell":
        bridge.read_table.return_value[1] = []
    elif state == "empty":
        table.node.table.table.rowCount = 0
    elif state == "foreign":
        bridge.list_java_windows.return_value.append(SimpleNamespace(pid=99, title="QA"))
    with pytest.raises(QAError) as caught:
        driver.edit_sale_row(ALIAS, 0, CANARY)
    assert CANARY not in str(caught.value)
    bridge.click_element.assert_not_called()


@pytest.mark.parametrize("changed", ["text_value", "enabled", "visible", "showing", "x", "width", "height"])
def test_edit_sale_row_rechecks_cell_identity_and_visibility_after_refresh(changed):
    driver, bridge, _, target = editable_driver()
    value = "ANOTHER" if changed == "text_value" else -1 if changed == "x" else 0
    target.node.refresh.side_effect = lambda: setattr(target.node, changed, value)
    with pytest.raises(QAError) as caught:
        driver.edit_sale_row(ALIAS, 0, CANARY)
    assert CANARY not in str(caught.value)
    bridge.click_element.assert_not_called()


@pytest.mark.parametrize("column,code", [(-1, CANARY), (True, CANARY), (2, CANARY), (0, ""), (0, None)])
def test_edit_sale_row_requires_a_valid_code_column_and_expected_identity(column, code):
    driver, bridge, _, _ = editable_driver()
    with pytest.raises(QAError):
        driver.edit_sale_row(ALIAS, column, code)
    bridge.click_element.assert_not_called()


@pytest.mark.parametrize("fail", [False, True])
def test_edit_sale_row_keeps_native_logs_and_click_failures_private(fail, capsys, caplog):
    driver, bridge, _, target = editable_driver()
    target.node.refresh.side_effect = noise

    def click(*_args, **_kwargs):
        noise()
        if fail:
            raise RuntimeError(CANARY)

    bridge.click_element.side_effect = click
    with patch("products.xgestion.driver.diagnostic") as diagnostic:
        if fail:
            with pytest.raises(QAError) as caught:
                driver.edit_sale_row(ALIAS, 0, CANARY)
            assert CANARY not in "".join(traceback.format_exception(caught.value))
        else:
            driver.edit_sale_row(ALIAS, 0, CANARY)
    captured = capsys.readouterr()
    assert CANARY not in captured.out + captured.err + caplog.text + str(diagnostic.call_args_list)
