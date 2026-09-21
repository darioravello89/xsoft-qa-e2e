"""Catálogo Markdown contrastado con la estructura Robot real."""

import json
import re
from pathlib import Path

from framework.errors import QAError
from framework.paths import safe_path

PRODUCTS = {"xgestion": "implemented", "xportal": "planned", "mozos": "planned", "consultador": "planned"}
CASE_ID = re.compile(r"^[A-Z]{2,8}-[A-Z]{2,8}-\d{3}$")
TAG = re.compile(r"[a-z][a-z0-9_-]*")


def load_groups(root: Path, product: str) -> list[dict]:
    if product not in PRODUCTS:
        raise QAError("Producto no reconocido en el catálogo de grupos.")
    path = root / "products" / product / "groups.json"
    if PRODUCTS[product] == "planned" and not path.exists():
        return []
    try:
        groups = json.loads(path.read_text(encoding="utf-8-sig"))["groups"]
        if not isinstance(groups, list) or not groups:
            raise ValueError
        seen = set()
        for group in groups:
            if not TAG.fullmatch(group["id"]) or group["id"] in seen:
                raise ValueError
            if any(not isinstance(group[key], str) or not group[key].strip() for key in ("title", "description")):
                raise ValueError
            if type(group["stage"]) is not int or not 0 <= group["stage"] <= 6:
                raise ValueError
            seen.add(group["id"])
        return groups
    except (KeyError, ValueError, TypeError, OSError):
        raise QAError(f"Catálogo de grupos inválido o ausente: products/{product}/groups.json") from None


def group_overview(root: Path, product: str, cases: list[dict] | None = None) -> list[dict]:
    groups = load_groups(root, product)
    if cases is None:
        cases = load_catalog(root)
    result = []
    for group in groups:
        members = [case for case in cases if case["product"] == product and group["id"] in case["tags"]]
        counts = {status: sum(case["status"] == status for case in members)
                  for status in ("implemented", "planned", "manual")}
        result.append({**group, "counts": counts})
    return result


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
            if any(not isinstance(info[key], str) or not info[key].strip() for key in ("title", "module")):
                raise ValueError
            if not isinstance(info["tags"], list) or not info["tags"]:
                raise ValueError
            if any(not isinstance(tag, str) or not TAG.fullmatch(tag) for tag in info["tags"]):
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
    groups_by_product = {product: {group["id"] for group in load_groups(root, product)}
                         for product, status in PRODUCTS.items() if status == "implemented"}
    for case in cases:
        if case["product"] in groups_by_product:
            groups = groups_by_product[case["product"]]
            if case["module"] not in groups or not groups.intersection(case["tags"]):
                raise QAError(f"El escenario {case['id']} no corresponde a un módulo y grupo registrados.")
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
