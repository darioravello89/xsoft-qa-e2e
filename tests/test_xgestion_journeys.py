"""Contratos de UI y secuencia; los dobles no prueban accesibilidad del JAR."""

from decimal import Decimal
from unittest.mock import Mock

import pytest

from products.xgestion import library as module
from products.xgestion.library import XGestionLibrary, parse_ars, parse_payment, parse_quantity
from products.xgestion.oracles import Snapshot


@pytest.fixture
def sale(monkeypatch):
    monkeypatch.setattr(module, "UI_TIMEOUT", 0)
    library = XGestionLibrary()
    library.journeys = True
    library.fixtures = {"product": {"code": "QA", "name": "Artículo QA"}, "nonexistent_product_code": "ABSENT",
                        "sales_journeys": {"unknown_notice": "status", "unknown_notice_text": "Codigo inexistente.",
                            "repeated_product_rows": 1,
                            "defaults": {"customer": "Consumidor final", "price_list": "General", "document": "Interno"}}}
    library.driver = Mock()
    library.driver.locators = {"elements": {"sale.lines": {"column_count": 5,
        "columns": {"code": 0, "name": 1, "quantity": 2, "unit_price": 3, "total": 4}}}}
    library.driver.table_rows.return_value = [["QA", "Artículo QA", "2.0", "$ 1.000,00", "$ 2.000,00"]]
    texts = {"sale.total": "2.000,00", "sale.quantity": "1", "payment.total": "2000.00",
             "payment.amount": "3000", "payment.change": "1000.00"}
    library.driver.text.side_effect = lambda alias: texts[alias]
    library.before = Snapshot(frozenset({1}), Decimal(10), Decimal(20))
    oracle = Mock()
    oracle.snapshot.return_value = library.before
    oracle.verify_sale.return_value = 2
    library._oracle = Mock(return_value=oracle)
    library.verify_context = Mock()
    return library, texts, oracle


def test_content_requires_product_quantity_subtotals_and_total(sale):
    library, _, _ = sale
    library._assert_sale_content(2)


def test_source_formats_do_not_confuse_decimal_points_with_thousands():
    assert parse_quantity("2.0") == Decimal(2)
    assert parse_quantity("0.125") == Decimal("0.125")
    assert parse_ars("$\u00a01.000,00") == Decimal(1000)
    assert parse_payment("2000.00") == Decimal(2000)
    assert parse_payment("3000") == Decimal(3000)
    assert parse_payment("0.00") == Decimal(0)


@pytest.mark.parametrize("value", ["USD --", "2.000,00", "NaN", "", "2.000"])
def test_payment_never_silently_accepts_another_format(value):
    with pytest.raises(AssertionError):
        parse_payment(value)


@pytest.mark.parametrize("notice,rows", [("status", 1), ("dialog", 2)])
def test_unknown_code_preserves_sale_then_allows_valid_product(sale, notice, rows):
    library, _, oracle = sale
    library.fixtures["sales_journeys"].update(unknown_notice=notice, repeated_product_rows=rows)
    initial = [["QA", "Artículo QA", "1.0", "$ 1.000,00", "$ 1.000,00"]]
    after = [["QA", "Artículo QA", "2.0", "$ 1.000,00", "$ 2.000,00"]] if rows == 1 else initial * 2
    library.driver.table_rows.side_effect = [initial, initial, after]
    library.driver.text.side_effect = ["1.000,00", "1.000,00", "2.000,00"]
    library.unknown_code_in_sale()
    oracle.snapshot.assert_called_once()
    assert (("click", ("sale.unknown_dismiss",), {}) in library.driver.method_calls) == (notice == "dialog")
    library.driver.type.assert_any_call("sale.code", "QA", enter=True)


def test_cancel_payment_rejects_mutated_grid_even_with_same_total(sale):
    library, texts, _ = sale
    texts.update({"payment.amount": "2000", "payment.change": "0.00"})
    initial = library.driver.table_rows.return_value
    library.driver.table_rows.side_effect = [initial, [["WRONG", *initial[0][1:]]]]
    with pytest.raises(AssertionError, match="conservados"):
        library.cancel_cash_payment()


def test_edit_changes_existing_product_and_checks_result(sale):
    library, texts, _ = sale
    initial = [["QA", "Artículo QA", "1.0", "$ 1.000,00", "$ 1.000,00"]]
    library.driver.table_rows.side_effect = [initial, library.driver.table_rows.return_value]
    library.driver.text.side_effect = ["1.000,00", texts["sale.total"]]
    library.edit_sale_quantity()
    library.driver.edit_sale_row.assert_called_once_with("sale.lines", 0, "QA")
    actions = library.driver.method_calls
    identity = actions.index(("expect", ("editor.product", "Artículo QA"), {}))
    edit = actions.index(("type", ("editor.quantity", "2"), {}))
    save = actions.index(("click", ("editor.save",), {}))
    assert identity < edit < save


def test_wrong_editor_product_prevents_saving(sale):
    library, texts, _ = sale
    library.driver.table_rows.return_value[0][2:] = ["1.0", "$ 1.000,00", "$ 1.000,00"]
    texts["sale.total"] = "1.000,00"
    library.driver.expect.side_effect = AssertionError("Producto distinto")
    with pytest.raises(AssertionError):
        library.edit_sale_quantity()
    library.driver.type.assert_not_called()
    assert ("click", ("editor.save",), {}) not in library.driver.method_calls


@pytest.mark.parametrize("mutation", [False, True])
def test_rejected_abandon_preserves_ui_and_persistence(sale, mutation):
    library, texts, oracle = sale
    library.driver.table_rows.return_value[0][2:] = ["1.0", "$ 1.000,00", "$ 1.000,00"]
    texts["sale.total"] = "1.000,00"
    if mutation:
        oracle.snapshot.return_value = Snapshot(frozenset({1}), Decimal(9), Decimal(20))
        with pytest.raises(AssertionError):
            library.reject_abandon()
    else:
        library.reject_abandon()
    assert ("keys", ("sale.code", "esc"), {}) in library.driver.method_calls
    assert ("click", ("sale.cancel_reject",), {}) in library.driver.method_calls
    assert ("click", ("sale.cancel_confirm",), {}) not in library.driver.method_calls


def test_grid_format_error_does_not_publish_cell_text(sale, monkeypatch):
    library, _, _ = sale
    library.driver.table_rows.return_value[0][3] = "PRIVATE_GRID_CONTENT_CANARY"
    record = Mock()
    monkeypatch.setattr(module, "assertion_failed", record)
    with pytest.raises(AssertionError):
        library._assert_sale_content(2)
    assert record.called
    assert "CANARY" not in str(record.call_args_list)


def test_change_failure_has_expected_and_observed_values(sale, monkeypatch):
    library, texts, _ = sale
    texts["payment.change"] = "0.00"
    record = Mock()
    monkeypatch.setattr(module, "assertion_failed", record)
    with pytest.raises(AssertionError):
        library.collect_with_change()
    assert record.call_args.kwargs == {"expected": "1000", "observed": "0.00"}


@pytest.mark.parametrize("lines,total", [([["QA", "Artículo QA", "1", "0", "0"]], "0"), ([], "1.000,00")])
def test_new_sale_rejects_residual_line_or_total(sale, lines, total):
    library, texts, _ = sale
    library.driver.table_rows.return_value = lines
    texts["sale.total"] = total
    with pytest.raises(AssertionError):
        library._assert_new_sale()


@pytest.mark.parametrize("change", ["code", "name", "quantity", "price", "line_total", "rows", "total"])
def test_a_matching_final_total_does_not_hide_bad_line_or_product(sale, change):
    library, texts, _ = sale
    columns = {"code": 0, "name": 1, "quantity": 2, "price": 3, "line_total": 4}
    if change in columns:
        library.driver.table_rows.return_value[0][columns[change]] = "OTRO" if change in {"code", "name"} else "1"
    elif change == "rows":
        library.driver.table_rows.return_value *= 2
    else:
        texts["sale.total"] = "1.000,00"
    with pytest.raises(AssertionError):
        library._assert_sale_content(2)


def test_change_is_checked_before_confirming_and_after_leaving_amount(sale):
    library, _, oracle = sale
    library.collect_with_change()
    actions = library.driver.method_calls
    tab = actions.index(("keys", ("payment.amount", "tab"), {}))
    check = actions.index(("text", ("payment.change",), {}))
    confirm = actions.index(("click", ("payment.confirm",), {}))
    assert tab < check < confirm
    library.verify_sale()
    oracle.verify_sale.assert_called_once_with(library.before, received=Decimal("3000"))


def test_wrong_change_never_confirms_payment(sale):
    library, texts, _ = sale
    texts["payment.change"] = "0"
    with pytest.raises(AssertionError):
        library.collect_with_change()
    assert ("click", ("payment.confirm",), {}) not in library.driver.method_calls


def test_cancel_payment_checks_unchanged_persistence_and_ui(sale):
    library, texts, oracle = sale
    texts.update({"payment.amount": "2000", "payment.change": "0.00"})
    library.cancel_cash_payment()
    assert ("click", ("payment.cancel",), {}) in library.driver.method_calls
    oracle.snapshot.assert_called_once()
    oracle.verify_sale.assert_not_called()


def test_cancel_payment_rejects_a_silent_sale_or_stock_change(sale):
    library, texts, oracle = sale
    texts.update({"payment.amount": "2000", "payment.change": "0.00"})
    oracle.snapshot.return_value = Snapshot(frozenset({1, 2}), Decimal(8), Decimal(2020))
    with pytest.raises(AssertionError):
        library.cancel_cash_payment()


def test_unknown_code_requires_identical_contents_before_adding_again(sale):
    library, texts, _ = sale
    texts["sale.total"] = "1.000,00"
    library.driver.table_rows.side_effect = [
        [["QA", "Artículo QA", "1", "1.000,00", "1.000,00"]],
        [["ABSENT", "Artículo QA", "1", "1.000,00", "1.000,00"]],
    ]
    with pytest.raises(AssertionError):
        library.unknown_code_in_sale()
    typed = [call for call in library.driver.method_calls if call[0] == "type"]
    assert typed == [("type", ("sale.code", "ABSENT"), {"enter": True})]


def test_next_sale_after_payment_observes_reset_without_opening_menu(sale):
    library, _, oracle = sale
    library.persisted_sale_id = 2
    library.after_paid = Snapshot(frozenset({1, 2}), Decimal(8), Decimal(2020))
    library._assert_new_sale = Mock()
    library._select_document = Mock()
    library.continue_after_payment()
    library._assert_new_sale.assert_called_once()
    library._select_document.assert_called_once()
    assert not any(call[0] == "click" and str(call[1][0]).startswith("menu.")
                   for call in library.driver.method_calls)
    assert library.before.sale_ids == frozenset({1})
    oracle.snapshot.assert_not_called()


def test_second_abandon_keeps_original_reference_and_first_sale_identity(sale):
    library, _, oracle = sale
    library.persisted_sale_id = 2
    library.after_paid = Snapshot(frozenset({1, 2}), Decimal(8), Decimal(2020))
    oracle.snapshot.return_value = library.after_paid
    library.verify_only_first_sale()
    oracle.verify_sale.assert_called_once_with(library.before, received=Decimal("2000"), expected_sale_id=2)


def test_reopen_after_abandon_never_replaces_baseline(sale):
    library, _, _ = sale
    original = library.before
    library._open_sale = Mock()
    library.continue_after_abandon()
    library._open_sale.assert_called_once()
    assert library.before is original


def test_reset_checks_empty_grid_and_quantity_defaults_before_second_product(sale):
    library, texts, _ = sale
    texts["sale.total"] = "0"
    library.driver.table_rows.return_value = []
    library._assert_new_sale()
    library.driver.expect.assert_any_call("sale.customer", "Consumidor final")
    library.driver.expect.assert_any_call("sale.document", "Interno")
    texts["sale.quantity"] = "2"
    with pytest.raises(AssertionError):
        library._assert_new_sale()


def test_start_with_missing_extension_blocks_before_launching_process(monkeypatch):
    import framework.config

    monkeypatch.setattr(framework.config, "load_profile", Mock())
    monkeypatch.setattr(module, "load_assets", lambda profile: ({}, {}))
    process = Mock()
    monkeypatch.setattr(module, "JarProcess", process)
    with pytest.raises(Exception, match="ventas-etapa1"):
        XGestionLibrary().start("ventas-etapa1")
    process.assert_not_called()
