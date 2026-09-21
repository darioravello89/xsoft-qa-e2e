"""Mapa público determinista: implementación, planificación y evidencia son capas distintas."""

import hashlib
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import quote

from framework.catalog import PRODUCTS, load_groups, validate_catalog
from framework.errors import QAError
from products.xgestion.seeds.pricing import PRICING_CASES

REPOSITORY_URL = "https://github.com/darioravello89/xsoft-qa-e2e"
ROADMAP = "products/xgestion/docs/roadmap.md"
MATRIX = "products/xgestion/docs/cobertura.md"
PRICING = "products/xgestion/seeds/pricing.py"
TITLES = {"xgestion": "XGestión", "xportal": "XPORTAL", "mozos": "Mozos Flutter", "consultador": "Consultador"}
STATUSES = ("implemented", "planned", "manual")
# Contrato de las tres tablas de variantes existentes; cambiar su formato requiere revisar el parser.
VARIANT_HEADERS = {
    2: ["Familia / grupos", "Variantes a desglosar", "Riesgo / resultado a observar"],
    3: ["Familia / grupos", "Variantes a desglosar", "Resultado / dependencia"],
    5: ["Familia / grupos", "Variantes observadas o por detallar", "Límite de interpretación"],
}


def _url(path: str, line: int | None = None) -> str:
    return f"{REPOSITORY_URL}/blob/main/{quote(path, safe='/')}" + (f"#L{line}" if line else "")


def _public_path(root: Path, relative: str) -> Path:
    path = root / relative
    if (path.resolve() != path or not path.is_file() or path.suffix not in {".md", ".json", ".robot", ".py"}
            or not path.is_relative_to(root / "products")
            or any(part.startswith(".") or part in {"reports", "work"} for part in Path(relative).parts)):
        raise QAError(f"Fuente pública ausente o redirigida: {relative}")
    return path


def _counts(cases: list[dict]) -> dict:
    return {"documented": len(cases), **{status: sum(case["status"] == status for case in cases)
                                      for status in STATUSES}, "real_validated": 0}


def _plain(value: str) -> str:
    return value.replace("`", "").replace("**", "").strip()


def _slug(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def _cells(row: str) -> list[str]:
    return [cell.strip().replace("\\|", "|") for cell in re.split(r"(?<!\\)\|", row.strip())[1:-1]]


def _markdown(content: str) -> tuple[dict, list[dict]]:
    """Leer las tablas públicas actuales sin dividir variantes de texto libre en supuestos casos."""
    lines = content.splitlines()
    stages, tables = {}, []
    stage, section = None, ""
    for index, line in enumerate(lines):
        if line.startswith("#"):
            section = line.lstrip("# ")
            match = re.match(r"## Etapa (\d+) — (.+)", line)
            if match:
                stage = int(match[1])
                stages[stage] = {"id": stage, "title": match[2], "priority": None}
            elif line.startswith("## "):
                stage = None
        if stage is not None and line.startswith("**Prioridad"):
            stages[stage]["priority"] = "/".join(dict.fromkeys(re.findall(r"\bP[012]\b", line))) or None
        if not line.startswith("|") or index + 1 >= len(lines):
            continue
        separator = _cells(lines[index + 1])
        if not separator or not all(re.fullmatch(r":?-{3,}:?", cell) for cell in separator):
            continue
        headers = _cells(line)
        if len(headers) != len(separator):
            raise QAError("Tabla pública de cobertura con columnas inconsistentes.")
        rows = []
        for row_index in range(index + 2, len(lines)):
            if not lines[row_index].startswith("|"):
                break
            values = _cells(lines[row_index])
            if len(values) != len(headers):
                raise QAError("Tabla pública de cobertura con columnas inconsistentes.")
            rows.append({"values": values, "line": row_index + 1})
        tables.append({"headers": headers, "rows": rows, "stage": stage, "section": section})
    return stages, tables


def _backlog(root: Path, group_ids: set[str]) -> tuple[list[dict], dict]:
    stages, roadmap_tables = _markdown(_public_path(root, ROADMAP).read_text(encoding="utf-8-sig"))
    _, matrix_tables = _markdown(_public_path(root, MATRIX).read_text(encoding="utf-8-sig"))
    restobar_tables = [table for table in roadmap_tables if table["section"] == "Backlog de recorridos de Restobar"
                      and table["headers"] == ["Ref.", "Recorrido de usuario y variantes que hay que cubrir",
                                                "Prioridad / dependencia"]]
    family_tables = [table for table in matrix_tables if table["section"] == "Matriz funcional y variantes"
                     and table["headers"] == ["Familia", "Variantes incluidas en el mapa",
                                               "Estado de automatización / siguiente paso"]]
    if len(restobar_tables) != 1 or not restobar_tables[0]["rows"]:
        raise QAError("Falta la tabla pública de backlog Restobar o cambió su formato.")
    if len(family_tables) != 1 or not family_tables[0]["rows"]:
        raise QAError("Falta la matriz pública de familias o cambió su formato.")
    variant_tables = []
    for stage, headers in VARIANT_HEADERS.items():
        section = f"Etapa {stage} — {stages.get(stage, {}).get('title', '')}"
        matches = [table for table in roadmap_tables if table["stage"] == stage and table["section"] == section]
        if len(matches) != 1 or matches[0]["headers"] != headers or not matches[0]["rows"]:
            raise QAError(f"Falta la tabla de variantes de la etapa {stage} o cambió su formato.")
        variant_tables.append(matches[0])
    if any(table["headers"][0] == "Familia / grupos" and table not in variant_tables for table in roadmap_tables):
        raise QAError("Tabla de variantes fuera de las secciones esperadas; revisar el contrato del roadmap.")
    restobar, families, variants = [], [], []
    seen = set()
    for row in restobar_tables[0]["rows"]:
        identifier, title, dependency = row["values"]
        priority = re.match(r"(P[012])\s*;\s*(.+)", dependency)
        if not re.fullmatch(r"R\d{2,}", identifier) or identifier in seen or priority is None:
            raise QAError("Backlog Restobar con referencia duplicada o prioridad inválida.")
        seen.add(identifier)
        restobar.append({"id": identifier, "product": "xgestion", "stage": 5, "title": _plain(title),
                         "priority": priority[1], "dependencies": _plain(priority[2]), "status": "planned",
                         "validation": "pending", "doc_url": _url(ROADMAP, row["line"])})
    for row in family_tables[0]["rows"]:
        title, descriptions, next_step = map(_plain, row["values"])
        families.append({"id": "familia-" + _slug(title), "product": "xgestion", "title": title,
                         "variants": descriptions, "source_status": next_step, "validation": "pending",
                         "doc_url": _url(MATRIX, row["line"])})
    for table in variant_tables:
        for row in table["rows"]:
            title, descriptions, limits = row["values"]
            groups = re.findall(r"`([^`]+)`", title)
            if not groups or not set(groups).issubset(group_ids):
                raise QAError("Familia del roadmap con grupos desconocidos.")
            name = _plain(title.split(":", 1)[0])
            variants.append({"id": f"etapa-{table['stage']}-" + _slug(name), "product": "xgestion",
                             "stage": table["stage"], "title": name, "groups": groups,
                             "priority": stages[table["stage"]]["priority"], "variants": _plain(descriptions),
                             "limits": _plain(limits), "validation": "pending", "doc_url": _url(ROADMAP, row["line"])})
    return list(stages.values()), {"restobar": sorted(restobar, key=lambda row: int(row["id"][1:])),
                                  "families": families, "roadmap_variants": variants}


def build_coverage(root: Path) -> dict:
    """Derivar cobertura de fuentes públicas; jamás abrir reportes, perfiles o evidencia privada."""
    root = root.resolve()
    documents = sorted(path for path in (root / "products").glob("*/scenarios/**/*.md")
                       if path.name.lower() != "readme.md")
    source_paths = {ROADMAP, MATRIX, PRICING}
    source_paths.update(path.relative_to(root).as_posix() for path in documents)
    source_paths.update(path.relative_to(root).as_posix() for path in (root / "products").rglob("*.robot"))
    for product in PRODUCTS:
        source_paths.add(f"products/{product}/README.md")
        if (root / f"products/{product}/groups.json").exists():
            source_paths.add(f"products/{product}/groups.json")
    # Validar las rutas antes de que el catálogo/Robot lean su contenido.
    for relative in sorted(source_paths):
        _public_path(root, relative)
    cases = validate_catalog(root)
    documents_by_id = {json.loads(path.read_text(encoding="utf-8-sig").split("---", 2)[1])["id"]:
                       path.relative_to(root).as_posix() for path in documents}
    registries = {product: load_groups(root, product) for product in PRODUCTS}
    stages, backlog = _backlog(root, {group["id"] for group in registries["xgestion"]})
    priorities = {stage["id"]: stage["priority"] for stage in stages}
    scenarios, groups, products = [], [], []
    for product, product_status in PRODUCTS.items():
        members = [case for case in cases if case["product"] == product]
        registry = {group["id"]: group for group in registries[product]}
        products.append({"id": product, "title": TITLES[product], "status": product_status,
                         "counts": _counts(members), "doc_url": _url(f"products/{product}/README.md"),
                         "validation": "pending"})
        for case in sorted(members, key=lambda case: case["id"]):
            stage = registry.get(case["module"], {}).get("stage")
            document = documents_by_id[case["id"]]
            test = case.get("test") if case["status"] == "implemented" else None
            scenarios.append({"id": case["id"], "title": case["title"], "product": product,
                              "module": case["module"], "status": case["status"],
                              "groups": [group for group in registry if group in case["tags"]],
                              "stage": stage, "priority": priorities.get(stage) if product == "xgestion" else None,
                              "priority_basis": "roadmap-stage" if stage in priorities else None,
                              "doc_path": document, "doc_url": _url(document), "test_path": test,
                              "test_url": _url(test) if test else None, "validation": "pending"})
        for group in registry.values():
            selected = [case for case in members if group["id"] in case["tags"]]
            counts = _counts(selected)
            status = ("partial" if counts["implemented"] else "planned" if counts["planned"]
                      else "manual" if counts["manual"] else "no-scenarios")
            groups.append({**group, "product": product, "members": sorted(case["id"] for case in selected),
                           "counts": counts, "status": status, "validation": "pending"})
    seed_examples = [{**json.loads(json.dumps(case)), "status": "pending", "validation": "pending",
                      "product": "xgestion", "doc_url": _url(PRICING)} for case in PRICING_CASES]
    sources = [{"path": relative,
                "sha256": hashlib.sha256(_public_path(root, relative).read_bytes().replace(b"\r\n", b"\n")).hexdigest(),
                "url": _url(relative)} for relative in sorted(source_paths)]
    return {"schema_version": 1, "repository_url": REPOSITORY_URL,
            "counts": {**_counts(cases), "groups": len(groups), "backlog_restobar": len(backlog["restobar"]),
                       "backlog_families": len(backlog["families"]),
                       "roadmap_variant_families": len(backlog["roadmap_variants"]), "seed_examples": len(seed_examples)},
            "products": products, "scenarios": scenarios, "groups": groups, "stages": stages,
            "backlog": backlog, "seed_examples": seed_examples, "sources": sources,
            "limitations": ["Implementado no equivale a validado en el producto: la evidencia real sigue pendiente.",
                            "Los grupos se superponen; sus miembros no se suman para contar escenarios.",
                            "Familias, variantes, backlog Restobar y ejemplos del seed no son fichas de escenarios.",
                            "Las matrices de familias se superponen; no representan unidades adicionales de cobertura.",
                            "No se calcula un porcentaje de cobertura del ERP ni se leen reportes privados."]}
