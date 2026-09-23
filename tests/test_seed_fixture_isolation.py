import copy
import json
from datetime import date
from pathlib import Path
from unittest.mock import MagicMock, Mock, sentinel

import pytest

from framework.errors import QAError
from products.xgestion.contracts import validate_fixtures
from products.xgestion.seeds import engine
from products.xgestion.seeds.model import SeedContext


@pytest.fixture
def fixtures():
    path = Path(__file__).resolve().parents[1] / "products/xgestion/examples/fixtures.example.json"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("field", ["product", "nonexistent_product_code"])
@pytest.mark.parametrize("code", ["QA-SEED-NORMAL", "qa-seed-normal", "QA-SEED-NORMAL  ", "qa-seed-normal  "])
def test_seed_code_collision_blocks_before_connecting(fixtures, field, code):
    if field == "product":
        fixtures[field]["code"] = code
    else:
        fixtures[field] = code
    validate_fixtures(fixtures)  # The fixture is valid; it is the seed that must reject the collision.
    original = copy.deepcopy(fixtures)
    sandbox = Mock()
    sandbox.connection.side_effect = AssertionError("No abrir MySQL ante una colisión de fixture.")

    with pytest.raises(QAError, match="colisiona con los fixtures originales"):
        engine.apply_seed(sandbox, fixtures, reference_date=date(2026, 9, 21))

    sandbox.connection.assert_not_called()
    assert fixtures == original


def test_seed_id_collision_blocks_before_connecting_even_with_a_different_code(fixtures):
    fixtures["product"]["id"] = 980001
    sandbox = Mock()
    sandbox.connection.side_effect = AssertionError("No abrir MySQL ante un ID reservado.")

    with pytest.raises(QAError, match="colisiona con los fixtures originales"):
        engine.apply_seed(sandbox, fixtures, reference_date=date(2026, 9, 21))

    sandbox.connection.assert_not_called()


def test_original_fixture_delegates_unchanged_context_to_guarded_seed(fixtures, monkeypatch):
    original = copy.deepcopy(fixtures)
    sandbox = MagicMock()
    sandbox.connection.return_value.__enter__.return_value = sentinel.connection
    apply = Mock(return_value={"counts": {"inserted": 0, "updated": 0, "unchanged": 1}})
    monkeypatch.setattr(engine, "apply_to_connection", apply)
    reference_date = date(2026, 9, 21)

    result = engine.apply_seed(sandbox, fixtures, reference_date=reference_date)

    declared = fixtures["context"]
    apply.assert_called_once_with(sentinel.connection, SeedContext(
        declared["empresa"], declared["sucursal"], declared["computadora"],
        declared["usuario_id"], reference_date,
    ))
    sandbox.connection.assert_called_once_with()
    assert result == apply.return_value
    assert fixtures == original


def test_profile_is_applied_to_catalog_and_forwarded_to_guarded_connection(fixtures, monkeypatch):
    sandbox = MagicMock()
    sandbox.connection.return_value.__enter__.return_value = sentinel.connection
    apply = Mock(return_value={"catalog_sha256": "profile-fingerprint"})
    monkeypatch.setattr(engine, "apply_to_connection", apply)
    profile = ("XG-PRM-070", "inactive")

    assert engine.apply_seed(sandbox, fixtures, journey_profile=profile) == apply.return_value

    assert apply.call_args.kwargs == {"journey_profile": profile}
    assert apply.call_args.args[0] == sentinel.connection


def test_invalid_profile_is_rejected_before_opening_database(fixtures):
    sandbox = Mock()
    with pytest.raises(QAError, match="[Pp]erfil"):
        engine.apply_seed(sandbox, fixtures, journey_profile=("XG-PRM-070", "typo"))
    sandbox.connection.assert_not_called()


def test_new_journey_product_collision_is_guarded_before_connecting(fixtures):
    fixtures["product"]["id"] = 981801  # XG-PRM-008, disjoint from original 980xxx battery.
    sandbox = Mock()
    with pytest.raises(QAError, match="colisiona con los fixtures originales"):
        engine.apply_seed(sandbox, fixtures)
    sandbox.connection.assert_not_called()
