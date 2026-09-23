"""El mapa público cuenta fichas únicas y nunca acredita pruebas del producto."""

import hashlib
import json
import re
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
    assert data["counts"]["documented"] == 298
    assert {key: data["counts"][key] for key in ("implemented", "planned", "manual", "real_validated")} == {
        "implemented": 96, "planned": 202, "manual": 0, "real_validated": 0,
    }
    assert len({case["id"] for case in data["scenarios"]}) == 298
    assert {case["validation"] for case in data["scenarios"]} == {"pending"}
    pending = [case for case in data["scenarios"] if case["status"] == "planned"]
    assert {case["id"] for case in pending} == {"XG-PRM-077", "XG-PRM-078"} | {
        f"XG-{prefix}-{number:03}" for prefix, count in (
            ("REM", 24), ("RES", 40), ("LPR", 28), ("CCC", 10), ("CCP", 8), ("CUO", 6),
            ("LDI", 8), ("CAJ", 10), ("FIN", 10), ("INV", 4), ("BKP", 2),
            ("COB", 8), ("PRE", 6), ("DEV", 6), ("FEL", 6), ("PEX", 6),
            ("REC", 4), ("CON", 4), ("ACT", 4), ("BEN", 6),
        )
        for number in range(1, count + 1)
    }
    assert all(case["test_url"] is None for case in pending)
    assert len(data["products"]) == 4
    assert {product["id"]: product["status"] for product in data["products"]} == {
        "xgestion": "implemented", "xportal": "planned", "mozos": "planned", "consultador": "planned",
    }


def test_groups_are_overlapping_selections_not_extra_cases():
    data = build_coverage(ROOT)
    groups = {group["id"]: group for group in data["groups"]}
    assert groups["ventas"]["counts"]["implemented"] == 9
    assert groups["ventas"]["counts"]["planned"] == 12
    assert groups["ventas"]["status"] == "partial"
    assert groups["smoke"]["status"] == "partial"
    assert groups["mesas"]["members"]
    assert groups["mesas"]["status"] == "planned"
    assert groups["mesas"]["counts"]["implemented"] == 0
    assert groups["smoke"]["counts"]["implemented"] == 5
    assert groups["promociones"]["counts"]["implemented"] == 82
    assert groups["promociones"]["counts"]["planned"] == 2
    assert len(groups["promociones"]["members"]) == 84
    assert len(groups["regression"]["members"]) == 298
    assert groups["regression"]["counts"]["implemented"] == 96
    assert groups["regression"]["counts"]["planned"] == 202
    assert len(set().union(*(set(group["members"]) for group in data["groups"]))) == 298
    case = next(case for case in data["scenarios"] if case["id"] == "XG-VEN-003")
    assert case["stage"] == 1
    assert case["priority"] == "P0"
    assert case["status"] == "implemented"
    assert case["test_url"].endswith("products/xgestion/suites/ventas.robot")
    assert case["doc_url"].endswith("products/xgestion/scenarios/ventas/XG-VEN-003.md")


def test_usd_critical_group_is_implemented_without_claiming_real_validation():
    data = build_coverage(ROOT)
    identifiers = {f"XG-PRM-{number:03}" for number in range(80, 85)}
    cases = [case for case in data["scenarios"] if case["id"] in identifiers]
    assert len(cases) == 5
    for case in cases:
        assert (case["priority"], case["priority_basis"], case["status"], case["validation"]) == (
            "P0", "scenario", "implemented", "pending")
        assert {"ofertas-usd", "regression", "promociones"} <= set(case["groups"])
    group = next(group for group in data["groups"] if group["id"] == "ofertas-usd")
    assert set(group["members"]) == identifiers
    assert group["counts"] == {"documented": 5, "implemented": 5, "planned": 0,
                               "manual": 0, "real_validated": 0}


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
    assert after["counts"]["documented"] == 298
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
    assert data["counts"]["documented"] == 299
    assert data["counts"]["planned"] == 203
    assert data["counts"]["implemented"] == 96
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
    expected.update({
        "MIN-PCT-Q2": "XG-PRM-008", "MIN-IMP-Q2": "XG-PRM-009", "MIN-PRECIO-Q2": "XG-PRM-010",
        "FAMILIA": "XG-PRM-011", "SUBFAMILIA": "XG-PRM-018", "MARCA": "XG-PRM-025", "SECTOR": "XG-PRM-032",
        "AGRUPADA-3X2": "XG-PRM-041", "COMBO": "XG-PRM-060", "COMBO-SOBRANTE": "XG-PRM-061",
        "KG-MIN0-0500": "XG-PRM-065", "KG-MIN1-0500": "XG-PRM-066", "KG-MIN1-1000": "XG-PRM-066",
        "LISTA-ARS": "XG-LPR-019", "LISTA-USD": "XG-LPR-020", "CANTIDAD-Q1": "XG-LPR-016",
        "CANTIDAD-Q2": "XG-LPR-016", "CANTIDAD-Q5": "XG-LPR-016", "LISTA-PRIORIDAD": "XG-LPR-017",
    })
    linked = {item["id"]: item for item in data["seed_examples"] if item.get("e2e_scenario")}
    assert {identifier: item["e2e_scenario"] for identifier, item in linked.items()} == expected
    assert sum(item["e2e_status"] == "implemented" for item in linked.values()) == 20
    assert sum(item["e2e_status"] == "planned" for item in linked.values()) == 6
    scenarios = {case["id"]: case for case in data["scenarios"]}
    for item in linked.values():
        assert item["e2e_status"] == scenarios[item["e2e_scenario"]]["status"]
        folder = "listas-precios" if item["e2e_scenario"].startswith("XG-LPR-") else "promociones"
        assert item["e2e_doc_url"].endswith(f"/scenarios/{folder}/{item['e2e_scenario']}.md")
        assert item["validation"] == "pending"
    assert all(item["status"] == "manual_pending" for item in PRICING_CASES)
    assert all(item["e2e_status"] is None and item["e2e_doc_url"] is None
               for item in data["seed_examples"] if not item.get("e2e_scenario"))
    assert data["counts"]["documented"] == 298
    assert data["counts"]["seed_examples"] == 26
    assert data["counts"]["real_validated"] == 0


def test_missing_seed_scenario_is_rejected_instead_of_exporting_a_broken_link(monkeypatch):
    monkeypatch.setitem(PRICING_CASES[0], "e2e_scenario", "XG-PRM-999")
    with pytest.raises(QAError, match="Ejemplo seed.*escenario"):
        build_coverage(ROOT)


def test_restobar_roadmap_references_resolve_to_planned_scenarios_without_extra_counts():
    data = build_coverage(ROOT)
    scenarios = {case["id"]: case for case in data["scenarios"]}
    for reference in data["backlog"]["restobar"]:
        related = re.findall(r"XG-RES-\d{3}", reference["title"])
        assert related, f"{reference['id']} perdió el vínculo con las fichas"
        assert all(scenarios[identifier]["status"] == "planned" for identifier in related)
        assert reference["id"] not in scenarios
    assert len(scenarios) == data["counts"]["documented"] == 298
