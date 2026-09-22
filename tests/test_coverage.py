"""El mapa público cuenta fichas únicas y nunca acredita pruebas del producto."""

import hashlib
import json
import shutil
from pathlib import Path

import pytest

from framework.coverage import build_coverage
from framework.errors import QAError
from products.xgestion.seeds.pricing import PRICING_CASES

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def public_repo(tmp_path):
    for source in (ROOT / "products").rglob("*"):
        if source.is_file() and source.suffix in {".md", ".json", ".robot", ".py"}:
            target = tmp_path / source.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    return tmp_path


def test_current_catalog_has_unique_cases_and_no_real_validation():
    data = build_coverage(ROOT)
    assert data["schema_version"] == 1
    assert data["counts"]["documented"] == 21
    assert {key: data["counts"][key] for key in ("implemented", "planned", "manual", "real_validated")} == {
        "implemented": 21, "planned": 0, "manual": 0, "real_validated": 0,
    }
    assert len({case["id"] for case in data["scenarios"]}) == 21
    assert {case["validation"] for case in data["scenarios"]} == {"pending"}
    assert len(data["products"]) == 4
    assert {product["id"]: product["status"] for product in data["products"]} == {
        "xgestion": "implemented", "xportal": "planned", "mozos": "planned", "consultador": "planned",
    }


def test_groups_are_overlapping_selections_not_extra_cases():
    data = build_coverage(ROOT)
    groups = {group["id"]: group for group in data["groups"]}
    assert groups["ventas"]["counts"]["implemented"] == 9
    assert groups["ventas"]["counts"]["planned"] == 0
    assert groups["ventas"]["status"] == "partial"
    assert groups["smoke"]["status"] == "partial"
    assert groups["mesas"]["members"] == []
    assert groups["mesas"]["status"] == "no-scenarios"
    assert groups["smoke"]["counts"]["implemented"] == 5
    assert groups["promociones"]["counts"]["implemented"] == 7
    assert len(groups["regression"]["members"]) == 21
    assert groups["regression"]["counts"]["implemented"] == 21
    assert groups["regression"]["counts"]["planned"] == 0
    assert len(set().union(*(set(group["members"]) for group in data["groups"]))) == 21
    case = next(case for case in data["scenarios"] if case["id"] == "XG-VEN-003")
    assert case["stage"] == 1
    assert case["priority"] == "P0"
    assert case["status"] == "implemented"
    assert case["test_url"].endswith("products/xgestion/suites/ventas.robot")
    assert case["doc_url"].endswith("products/xgestion/scenarios/ventas/XG-VEN-003.md")


def test_backlog_and_examples_stay_separate_and_keep_source_limits():
    data = build_coverage(ROOT)
    backlog = data["backlog"]
    assert [item["id"] for item in backlog["restobar"]] == [f"R{i:02d}" for i in range(1, 21)]
    assert len(backlog["families"]) == 16
    assert len(backlog["roadmap_variants"]) == 16
    assert "No acreditar cobros independientes" in backlog["restobar"][10]["title"]
    assert all(item["status"] == "planned" for item in backlog["restobar"])
    assert len(data["seed_examples"]) == 26
    assert {item["status"] for item in data["seed_examples"]} == {"pending"}
    usd = next(item for item in data["seed_examples"] if item["id"] == "LISTA-USD")
    assert usd["currency"] == "USD"
    assert usd["expected_total"] == "2.50"
    assert "cotización" in usd["note"]
    assert data["counts"]["documented"] == len(data["scenarios"])


def test_output_is_deterministic_public_and_hashes_match(monkeypatch):
    original_open = Path.open

    def public_only(path, *args, **kwargs):
        if any(part in {".local", "reports"} or part.startswith(".env") for part in path.parts):
            pytest.fail("El mapa público intentó leer una fuente privada")
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, "open", public_only)
    first = build_coverage(ROOT)
    second = build_coverage(ROOT)
    assert json.dumps(first, ensure_ascii=False) == json.dumps(second, ensure_ascii=False)
    encoded = json.dumps(first, ensure_ascii=False)
    assert str(ROOT) not in encoded
    assert "generated_at" not in first
    for source in first["sources"]:
        assert source["sha256"] == hashlib.sha256((ROOT / source["path"]).read_bytes().replace(b"\r\n", b"\n")).hexdigest()
        assert source["url"].startswith("https://github.com/darioravello89/xsoft-qa-e2e/blob/main/")


def test_windows_and_linux_checkouts_produce_the_same_model(public_repo):
    before = build_coverage(public_repo)
    for source in before["sources"]:
        path = public_repo / source["path"]
        path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n"))
    unix = build_coverage(public_repo)
    for source in unix["sources"]:
        path = public_repo / source["path"]
        path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
    assert build_coverage(public_repo) == unix == before


def test_public_source_edits_change_hash_and_backlog_without_changing_case_count(public_repo):
    before = build_coverage(public_repo)
    roadmap = public_repo / "products/xgestion/docs/roadmap.md"
    content = roadmap.read_text(encoding="utf-8")
    content = content.replace("| R20 |", "| R21 | Nueva variante pública. | P2; laboratorio |\n| R20 |")
    roadmap.write_text(content, encoding="utf-8")
    after = build_coverage(public_repo)
    assert after["counts"]["backlog_restobar"] == before["counts"]["backlog_restobar"] + 1
    assert after["counts"]["documented"] == 21
    assert next(row for row in after["backlog"]["restobar"] if row["id"] == "R21")["priority"] == "P2"
    assert before["sources"] != after["sources"]


def test_duplicate_backlog_ids_and_missing_matrix_fail_instead_of_silent_loss(public_repo):
    roadmap = public_repo / "products/xgestion/docs/roadmap.md"
    original = roadmap.read_text(encoding="utf-8")
    roadmap.write_text(original.replace("| R20 |", "| R19 |"), encoding="utf-8")
    with pytest.raises(QAError, match="Restobar"):
        build_coverage(public_repo)
    roadmap.write_text(original, encoding="utf-8")
    matrix = public_repo / "products/xgestion/docs/cobertura.md"
    matrix.write_text(matrix.read_text(encoding="utf-8").replace("Variantes incluidas en el mapa", "Otro formato"),
                      encoding="utf-8")
    with pytest.raises(QAError, match="matriz"):
        build_coverage(public_repo)


def test_invalid_catalog_is_rejected_before_export(public_repo):
    case = public_repo / "products/xgestion/scenarios/ventas/XG-VEN-003.md"
    _, header, body = case.read_text(encoding="utf-8").split("---", 2)
    metadata = json.loads(header)
    metadata["status"] = "implemented"
    metadata.pop("test")
    case.write_text("---\n" + json.dumps(metadata) + "\n---" + body, encoding="utf-8")
    with pytest.raises(QAError, match="Escenario Markdown"):
        build_coverage(public_repo)


def test_new_documented_scenario_updates_counts_and_members_without_new_evidence(public_repo):
    previous = public_repo / "products/xgestion/scenarios/ventas/XG-VEN-003.md"
    new_case = previous.with_name("XG-VEN-010.md")
    _, header, body = previous.read_text(encoding="utf-8").split("---", 2)
    metadata = json.loads(header)
    metadata.update(id="XG-VEN-010", status="planned", test=None)
    body = body.replace("XG-VEN-003", "XG-VEN-010")
    new_case.write_text("---\n" + json.dumps(metadata) + "\n---" + body, encoding="utf-8")
    data = build_coverage(public_repo)
    assert data["counts"]["documented"] == 22
    assert data["counts"]["planned"] == 1
    assert data["counts"]["implemented"] == 21
    assert data["counts"]["real_validated"] == 0
    assert "XG-VEN-010" in next(group["members"] for group in data["groups"] if group["id"] == "ventas")
    planned = next(case for case in data["scenarios"] if case["id"] == "XG-VEN-010")
    assert planned["status"] == "planned"
    assert planned["test_url"] is None
    assert any(source["path"].endswith("XG-VEN-010.md") for source in data["sources"])


def test_hidden_robot_sources_are_rejected_before_catalog_reads_them(public_repo):
    private = public_repo / "products/xgestion/.local/unknown.robot"
    private.parent.mkdir()
    private.write_text("PRIVATE_CANARY_MUST_NOT_EXPORT", encoding="utf-8")
    with pytest.raises(QAError, match="Fuente pública"):
        build_coverage(public_repo)


@pytest.mark.parametrize("stage", [2, 3, 5])
@pytest.mark.parametrize("change", ["rename", "remove"])
def test_each_expected_roadmap_table_must_remain_recognizable(public_repo, stage, change):
    assert build_coverage(public_repo)["counts"]["roadmap_variant_families"] == 16
    roadmap = public_repo / "products/xgestion/docs/roadmap.md"
    content = roadmap.read_text(encoding="utf-8")
    prefix, stage_heading, section = content.partition(f"## Etapa {stage} —")
    if change == "rename":
        section = section.replace("| Familia / grupos |", "| Familias / grupos |", 1)
    else:
        start = section.index("| Familia / grupos |")
        end = section.index("\n\n", start)
        section = section[:start] + section[end:]
    roadmap.write_text(prefix + stage_heading + section, encoding="utf-8")
    with pytest.raises(QAError, match=rf"variantes.*etapa {stage}"):
        build_coverage(public_repo)


def test_changed_variant_column_meaning_requires_parser_review(public_repo):
    roadmap = public_repo / "products/xgestion/docs/roadmap.md"
    content = roadmap.read_text(encoding="utf-8")
    roadmap.write_text(content.replace("| Riesgo / resultado a observar |", "| Otros datos |", 1), encoding="utf-8")
    with pytest.raises(QAError, match="variantes.*etapa 2"):
        build_coverage(public_repo)


def test_seed_examples_link_to_existing_scenarios_without_claiming_validation():
    data = build_coverage(ROOT)
    expected = dict(zip(("PCT-Q3", "IMP-Q3", "2X1-Q3", "2DA50-Q3", "EXPIRADA", "FUTURA", "INACTIVA"),
                        (f"XG-PRM-{number:03}" for number in range(1, 8)), strict=True))
    linked = {item["id"]: item for item in data["seed_examples"] if item.get("e2e_scenario")}
    assert {identifier: item["e2e_scenario"] for identifier, item in linked.items()} == expected
    for item in linked.values():
        assert item["e2e_status"] == "implemented"
        assert item["e2e_doc_url"].endswith(f"/scenarios/promociones/{item['e2e_scenario']}.md")
        assert item["validation"] == "pending"
    assert all(item["status"] == "manual_pending" for item in PRICING_CASES)
    assert all(item["e2e_status"] is None and item["e2e_doc_url"] is None
               for item in data["seed_examples"] if not item.get("e2e_scenario"))
    assert data["counts"]["documented"] == 21
    assert data["counts"]["seed_examples"] == 26
    assert data["counts"]["real_validated"] == 0


def test_missing_seed_scenario_is_rejected_instead_of_exporting_a_broken_link(monkeypatch):
    monkeypatch.setitem(PRICING_CASES[0], "e2e_scenario", "XG-PRM-999")
    with pytest.raises(QAError, match="Ejemplo seed.*escenario"):
        build_coverage(ROOT)
