"""Contratos del ejecutor al preparar, editar y elegir destinos de pago."""
import json
from datetime import date
from unittest.mock import Mock

import pytest

from framework.errors import QAError
from products.xgestion.offer_journeys.library import XGestionOfferJourneysLibrary
from products.xgestion.offer_journeys.payments import CASES as PAYMENTS
from products.xgestion.offer_journeys.profiled import CASES as PROFILES


@pytest.mark.parametrize("case_id, selected, receipt", [
    ("XG-PRM-070", "", ""), ("XG-PRM-079", "general-off", "{}"),
    ("XG-PRM-070", "inactive", '{"case_id":"XG-PRM-079","variant":"inactive"}'),
    ("XG-PRM-008", "principal", ""), ("XG-PRM-008", "", "{}"),
])
def test_forged_partial_or_missing_profile_receipt_never_starts(monkeypatch, case_id, selected, receipt):
    monkeypatch.setenv("XSOFT_QA_SEED", "catalogo-comercial-v1")
    monkeypatch.setenv("XSOFT_QA_SEED_DATE", date.today().isoformat())
    monkeypatch.setenv("XSOFT_QA_OFFER_VARIANT", selected)
    monkeypatch.setenv("XSOFT_QA_OFFER_PROFILE", receipt)
    library = XGestionOfferJourneysLibrary()
    library.start = Mock()
    with pytest.raises(QAError):
        library.run_journey(case_id)
    library.start.assert_not_called()


def test_profile_runs_only_verified_phase_with_all_steps(monkeypatch):
    monkeypatch.setenv("XSOFT_QA_SEED", "catalogo-comercial-v1")
    monkeypatch.setenv("XSOFT_QA_SEED_DATE", date.today().isoformat())
    monkeypatch.setenv("XSOFT_QA_OFFER_VARIANT", "inactive")
    monkeypatch.setenv("XSOFT_QA_OFFER_PROFILE", json.dumps({"case_id": "XG-PRM-070", "variant": "inactive"}))
    library = XGestionOfferJourneysLibrary()
    library.start, library.login, library._perform, library.stop = Mock(), Mock(), Mock(), Mock()
    library.run_journey("XG-PRM-070")
    library.start.assert_called_once_with("ventas-etapa1")
    assert [c.args[0] for c in library._perform.call_args_list] == list(PROFILES["XG-PRM-070"].variants[1].steps)
    library.stop.assert_called_once()


def test_restricted_manual_does_not_write_or_force_focus():
    library = XGestionOfferJourneysLibrary()
    library.variant = PROFILES["XG-PRM-079"].variants[0]
    library.driver = Mock()
    library._assert_basket, library._open_editor = Mock(), Mock()
    library.expected = library.variant.steps[2].expected
    step = next(s for s in library.variant.steps if s.action == "manual_blocked")
    library._edit_manual(step, library.variant.products[0])
    library.driver.type.assert_not_called()
    library.driver.expect_state.assert_any_call("editor.manual", "editable", False)
    library.driver.expect_state.assert_any_call("editor.manual", "focusable", False)
    library.driver.expect_state.assert_any_call("editor.manual_percent", "checked", False)
    library.driver.click.assert_called_once_with("editor.save")


def test_manual_amount_saved_before_comparing_recalculated_basket():
    library = XGestionOfferJourneysLibrary()
    library.variant = PROFILES["XG-PRM-079"].variants[-1]
    library.driver = Mock()
    library._assert_basket, library._open_editor = Mock(), Mock()
    library.expected = library.variant.steps[2].expected
    library.fixtures = {"offer_journeys": {"manual_warning_observation": {"duration_seconds": 4, "max_sample_gap_seconds": 1}}}
    step = next(s for s in library.variant.steps if s.action == "manual")
    library._edit_manual(step, library.variant.products[0])
    library.driver.type.assert_called_once_with("editor.manual", "100")
    library.driver.expect_state.assert_any_call("editor.manual_percent", "checked", False)
    library.driver.observe_notice.assert_called_once()
    assert library.driver.observe_notice.call_args.kwargs["expected"] is False


def test_payment_picker_checks_id_even_when_public_name_matches():
    library = XGestionOfferJourneysLibrary()
    library.driver = Mock()
    library.driver.locators = {"elements": {"payment_picker.lines": {"columns": {"id": 0, "name": 1, "discount": 2}}}}
    library.driver.table_rows.return_value = [["4", "QA-PRM-TARJETA", "0"]]
    with pytest.raises(AssertionError):
        library._pick_payment("card")
    library.driver.keys.assert_not_called()


def test_payment_confirmation_uses_current_destination_not_cash_fixture():
    library = XGestionOfferJourneysLibrary()
    library.variant = PAYMENTS["XG-PRM-073"].variants[-1]
    library.payment_ref, library.payment_id = "card", 989903
    library.before = Mock()
    library.driver = Mock()
    library._pick_payment = Mock()
    library._open_payment()
    library._pick_payment.assert_called_once_with("card")
    library.driver.expect_choice.assert_called_once_with(
        "payment.method", ("QA-PRM-TARJETA", "989903|QA-PRM-TARJETA"))


@pytest.mark.parametrize("correct", [True, False])
def test_regular_cash_uses_verified_id_and_enter_not_a_cell_click(correct):
    library = XGestionOfferJourneysLibrary()
    library.variant = PROFILES["XG-PRM-070"].variants[-1]
    library.before = Mock()
    library.fixtures = {"sale": {"cash_payment_id": 1}}
    library.driver = Mock()
    library.driver.locators = {"elements": {"payment_picker.lines": {
        "columns": {"id": 0, "name": 1, "discount": 2}}}}
    library.driver.table_rows.return_value = [["1" if correct else "9", "Efectivo privado", "0"]]
    if correct:
        library._open_payment()
        library.driver.select_sale_row.assert_called_once_with("payment_picker.lines", 0, "1")
        library.driver.keys.assert_called_once_with("payment_picker.search", "enter")
        library.driver.expect_choice.assert_called_once_with(
            "payment.method", ("Efectivo privado", "1|Efectivo privado"))
    else:
        with pytest.raises(AssertionError):
            library._open_payment()
        library.driver.keys.assert_not_called()
    library.driver.click.assert_called_once_with("sale.close")


def test_teardown_stops_owned_process_even_if_evidence_capture_fails():
    library = XGestionOfferJourneysLibrary()
    library.screenshot = Mock(side_effect=QAError("synthetic unavailable"))
    library.stop = Mock()
    with pytest.raises(QAError):
        library.finish_journey()
    library.stop.assert_called_once()

