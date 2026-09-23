"""Validar lo que recibe QA en Excel sin requerir Office ni runtime de autoría en CI."""

import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from framework.coverage import build_coverage

ROOT = Path(__file__).resolve().parents[1]
NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def cell_value(cell):
    if cell.get("t") == "inlineStr":
        return "".join(cell.itertext())
    value = cell.find("s:v", NS)
    return value.text if value is not None else ""


def test_published_workbook_contains_cases_backlog_and_counts_without_false_pass():
    model = build_coverage(ROOT)
    xgestion = next(product for product in model["products"] if product["id"] == "xgestion")
    with zipfile.ZipFile(ROOT / "docs/coverage/xgestion-cobertura.xlsx") as archive:
        book = ET.fromstring(archive.read("xl/workbook.xml"))
        assert [sheet.get("name") for sheet in book.findall("s:sheets/s:sheet", NS)] == [
            "Resumen", "Grupos", "Escenarios", "Por detallar", "Ejemplos seed",
        ]
        sheets = [ET.fromstring(archive.read(f"xl/worksheets/sheet{i}.xml")) for i in range(1, 6)]
        for sheet in sheets:
            assert not [cell for cell in sheet.findall(".//s:c", NS) if cell.get("t") == "e"]
            assert sheet.find("s:sheetViews/s:sheetView/s:pane", NS).get("ySplit") == "6"
        summary = {cell.get("r"): cell_value(cell) for cell in sheets[0].findall(".//s:c", NS)}
        assert [int(summary[f"B{i}"]) for i in range(7, 12)] == [
            xgestion["counts"][key] for key in ("documented", "implemented", "planned", "manual", "real_validated")
        ]
        cases = sheets[2].findall("s:sheetData/s:row", NS)
        actual = {}
        for row in cases:
            number = int(row.get("r"))
            if number < 7:
                continue
            cells = {cell.get("r"): cell_value(cell) for cell in row.findall("s:c", NS)}
            if cells.get(f"A{number}"):
                actual[cells[f"A{number}"]] = (cells[f"C{number}"], cells[f"D{number}"])
        labels = {"implemented": "Automatizado", "planned": "Pendiente", "manual": "Manual"}
        assert actual == {case["id"]: (labels[case["status"]], "Pendiente")
                          for case in model["scenarios"] if case["product"] == "xgestion"}
        seed_cells = {cell.get("r"): cell_value(cell) for cell in sheets[4].findall(".//s:c", NS)}
        assert seed_cells["F6"] == "Validación real"
        assert seed_cells["G6"] == "Escenario E2E"
        for number, example in enumerate(model["seed_examples"], start=7):
            assert seed_cells[f"A{number}"] == example["id"]
            assert seed_cells[f"F{number}"] == "Pendiente"
            if example.get("e2e_scenario"):
                assert seed_cells[f"G{number}"] == (
                    f"{example['e2e_scenario']} · {labels[example['e2e_status']]}\n{example['e2e_doc_url']}"
                )
            else:
                assert seed_cells[f"G{number}"] == "Sin ficha"
        assert "26 ejemplos seed: 26 vinculados a fichas y 0 sin ficha" in summary["A32"]
        tables = [ET.fromstring(archive.read(name)) for name in archive.namelist()
                  if name.startswith("xl/tables/table") and name.endswith(".xml")]
        assert len(tables) == 4
        assert all(table.find("s:autoFilter", NS) is not None for table in tables)
        assert not any("vbaProject" in name or "externalLinks" in name for name in archive.namelist())


def test_group_labels_preserve_every_member_and_keep_large_groups_readable():
    model = build_coverage(ROOT)
    expected = {group["id"]: group["members"] for group in model["groups"] if group["product"] == "xgestion"}
    with zipfile.ZipFile(ROOT / "docs/coverage/xgestion-cobertura.xlsx") as archive:
        groups = ET.fromstring(archive.read("xl/worksheets/sheet2.xml"))
    seen = {}
    for row in groups.findall("s:sheetData/s:row", NS):
        number = int(row.get("r"))
        if number < 7:
            continue
        cells = {cell.get("r"): cell_value(cell) for cell in row.findall("s:c", NS)}
        group = cells.get(f"C{number}")
        if not group:
            continue
        display = cells[f"I{number}"]
        expanded = []
        if display != "Por detallar":
            for token in re.split(r",\s*|\n", display):
                if ".." not in token:
                    expanded.append(token)
                    continue
                first, end = token.split("..")
                match = re.fullmatch(r"(.+?-)(\d+)", first)
                assert match is not None and end.isdigit(), f"Rango ilegible: {token}"
                prefix, start = match.groups()
                assert len(start) == len(end) and int(start) < int(end), f"Rango inválido: {token}"
                expanded.extend(f"{prefix}{value:0{len(start)}}" for value in range(int(start), int(end) + 1))
        assert expanded == expected[group], f"El resumen alteró miembros, huecos o prefijos del grupo {group}"
        if group in {"regression", "promociones"}:
            assert float(row.get("ht")) <= 160, f"El grupo {group} ocupa demasiado alto para leer el mapa"
        seen[group] = display
    assert set(seen) == set(expected)
    assert seen["promociones"] == "XG-PRM-001..084"
    assert seen["ofertas-usd"] == "XG-PRM-080..084"
