"""Documentación reproducible sin perder identidad ni diseño funcional previo."""

import importlib.util
from pathlib import Path

import pytest
from robot.api import TestSuiteBuilder as RobotSuiteBuilder

from products.xgestion.offer_journeys.catalog import get_journey

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "update-offer-journey-docs.py"
SPEC = importlib.util.spec_from_file_location("offer_journey_docs", SCRIPT)
DOCS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DOCS)


def _original(identifier, status="planned"):
    return (f'---\n{{"id":"{identifier}","title":"Título conservado","status":"{status}",'
            '"tags":["promociones"]}\n---\n\n'
            f'# {identifier} — Título conservado\n\n## Objetivo\n\nConservar el objetivo.\n\n'
            '## Estado y alcance\n\nDiseño previo.\n\n## Variantes\n\nNo perder esta variante.\n')


def test_render_is_idempotent_and_preserves_metadata_title_and_original_design():
    original = _original("XG-PRM-063")
    updated = DOCS.update_document(original, get_journey("XG-PRM-063"))
    assert DOCS.update_document(updated, get_journey("XG-PRM-063")) == updated
    metadata, end = DOCS.metadata_from(updated)
    assert metadata["id"] == "XG-PRM-063"
    assert metadata["title"] == "Título conservado"
    assert metadata["tags"] == ["promociones", "escritura"]
    assert updated[end:].startswith(original.split("---\n", 2)[2].split("## Estado y alcance")[0])
    assert "No perder esta variante." in updated
    assert "referencia histórica" in updated
    assert updated.count(DOCS.GENERATED_START) == updated.count(DOCS.ARCHIVE_START) == 1
    assert "Estado del catálogo: **implemented**" in updated
    assert "Validación real: **pendiente**" in updated


def test_render_uses_literal_rounding_and_manual_amounts_without_recalculating_offers():
    updated = DOCS.update_document(_original("XG-PRM-063"), get_journey("XG-PRM-063"))
    assert "QA-PRM-063-V1-A" in updated
    assert "automático $2,79; manual $1,00; neto $6,21" in updated
    assert "automático $3,11; manual $0,00; neto $6,89" in updated
    assert "Total **$20,00**" in updated
    assert "Permisos general y sobre ofertas habilitados" in updated


def test_payment_and_price_list_actions_name_selected_medium_and_applied_price():
    payment = DOCS.update_document(_original("XG-PRM-076"), get_journey("XG-PRM-076"))
    assert "QA-PRM-TARJETA" in payment
    assert "QA-PRM-EFECTIVO" in payment
    assert "Total **$2.000,00**" in payment
    price_list = DOCS.update_document(_original("XG-PRM-072"), get_journey("XG-PRM-072"))
    assert "QA-PRM-072-LISTA-SIN-A" in price_list
    assert "precio $750,00" in price_list
    assert "lista aplicada: precio normal" in price_list


def test_updated_frontmatter_status_is_reflected_without_touching_its_content():
    original = _original("XG-PRM-008", "implemented")
    updated = DOCS.update_document(original, get_journey("XG-PRM-008"))
    assert '"status":"implemented"' in updated
    assert "Automatización catalogada" in updated
    assert "Validación real: **pendiente**" in updated


def test_usd_docs_distinguish_seed_currency_visible_rows_and_operational_totals():
    updated = DOCS.update_document(_original("XG-PRM-080"), get_journey("XG-PRM-080"))
    assert "precio final USD 50,00 por unidad" in updated
    assert "USD 100,00" in updated and "Total **$75.000,00**" in updated
    assert "ofertas-usd-v1" in updated and "cotización 1500 ARS/USD" in updated
    assert "la regla USD 50 proviene del incidente" in updated
    assert "precio final $50,00" not in updated


def test_mismatched_identity_or_broken_markers_stop_instead_of_overwriting():
    with pytest.raises(ValueError, match="identidad"):
        DOCS.update_document(_original("XG-PRM-008"), get_journey("XG-PRM-009"))
    original = _original("XG-PRM-008") + DOCS.GENERATED_START
    with pytest.raises(ValueError, match="marcadores"):
        DOCS.update_document(original, get_journey("XG-PRM-008"))


def test_generated_suites_have_exact_effective_tags_and_one_case_per_catalog_entry(tmp_path):
    generated = DOCS.artifacts()
    suites = {path: content for path, content in generated.items() if path.suffix == ".robot"}
    metadata = {path.stem: DOCS.metadata_from(content)[0]
                for path, content in generated.items() if path.suffix == ".md"}
    assert len(suites) == 10
    assert len(metadata) == 75
    assert "XG-PRM-077" not in metadata and "XG-PRM-078" not in metadata
    found = []
    for path, content in suites.items():
        target = tmp_path / path.name
        target.write_text(content, encoding="utf-8")
        suite = RobotSuiteBuilder().build(target)
        assert all(len(line) <= 120 for line in content.splitlines())
        for test in suite.tests:
            identifier = test.name.split(" ", 1)[0]
            found.append(identifier)
            assert set(test.tags) == {*metadata[identifier]["tags"], identifier}
            assert test.teardown.name == "Finalizar Recorrido De Ofertas"
            assert not test.setup.name
    assert len(found) == len(set(found)) == 75
