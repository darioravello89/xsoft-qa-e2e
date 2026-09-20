"""Catálogo Markdown contrastado con la estructura Robot real."""

import json
import re
from pathlib import Path

from framework.errors import QAError
from framework.paths import safe_path

PRODUCTS = {"xgestion": "implemented", "xportal": "planned", "mozos": "planned", "consultador": "planned"}
CASE_ID = re.compile(r"^[A-Z]{2,8}-[A-Z]{2,8}-\d{3}$")


def load_catalog(root: Path) -> list[dict]:
    cases = []
    seen = set()
    for path in sorted((root / "products").glob("*/scenarios/**/*.md")):
        if path.name.lower() == "readme.md":
            continue
        try:
            content = path.read_text(encoding="utf-8-sig")
            if not content.startswith("---\n"):
                raise ValueError
            info = json.loads(content.split("---", 2)[1])
            if not CASE_ID.fullmatch(info["id"]) or info["id"] in seen:
                raise ValueError
            if info["product"] not in PRODUCTS or info["status"] not in ("implemented", "planned", "manual"):
                raise ValueError
            if not info["title"] or not info["module"] or not isinstance(info["tags"], list) or not info["tags"]:
                raise ValueError
            if any(not isinstance(tag, str) or not re.fullmatch(r"[a-z][a-z0-9_-]*", tag) for tag in info["tags"]):
                raise ValueError
            if info["status"] == "implemented":
                test = safe_path(root, info["test"])
                product_root = root / "products" / info["product"]
                if not test.is_file() or test.suffix != ".robot" or not test.resolve().is_relative_to(product_root.resolve()):
                    raise ValueError
            seen.add(info["id"])
            cases.append(info)
        except (KeyError, IndexError, ValueError, TypeError, OSError):
            raise QAError(f"Escenario Markdown inválido o duplicado: {path.relative_to(root)}") from None
    return cases


def validate_catalog(root: Path) -> list[dict]:
    from robot.api import TestSuiteBuilder

    cases = load_catalog(root)
    documented = {case["id"]: case for case in cases if case["status"] == "implemented"}
    found = set()

    def visit(suite, path):
        for test in suite.tests:
            ids = [tag for tag in test.tags if CASE_ID.fullmatch(tag)]
            if len(ids) != 1 or ids[0] in found or ids[0] not in documented:
                raise QAError(f"Prueba sin escenario documentado único: {test.name}")
            info = documented[ids[0]]
            if path != (root / info["test"]) or not set(info["tags"]).issubset(set(test.tags)):
                raise QAError(f"El escenario {ids[0]} no coincide con su suite o etiquetas.")
            found.add(ids[0])
        for child in suite.suites:
            visit(child, path)

    for path in sorted((root / "products").rglob("*.robot")):
        if not path.is_relative_to(root / "products/xgestion"):
            raise QAError("Un producto pendiente no debe incluir pruebas ejecutables.")
        visit(TestSuiteBuilder().build(path), path)
    if found != set(documented):
        raise QAError("Hay escenarios implementados sin prueba Robot correspondiente.")
    return cases


def select_cases(cases: list[dict], product: str, group: str | None, scenario: str | None) -> list[dict]:
    if PRODUCTS.get(product) != "implemented":
        raise QAError(f"El producto {product} está pendiente de implementación; no se ejecutaron pruebas.")
    selected = [c for c in cases if c["product"] == product and c["status"] == "implemented"
                and (not group or group in c["tags"]) and (not scenario or c["id"] == scenario)]
    if not selected:
        raise QAError("La selección no contiene pruebas ejecutables. Usar qa.cmd list.")
    return selected
