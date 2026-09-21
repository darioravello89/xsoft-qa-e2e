"""Validar lo que recibe QA en Excel sin requerir Office ni runtime de autoría en CI."""

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
        tables = [ET.fromstring(archive.read(name)) for name in archive.namelist()
                  if name.startswith("xl/tables/table") and name.endswith(".xml")]
        assert len(tables) == 4
        assert all(table.find("s:autoFilter", NS) is not None for table in tables)
        assert not any("vbaProject" in name or "externalLinks" in name for name in archive.namelist())
