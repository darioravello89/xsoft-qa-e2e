import json
from pathlib import Path

import pytest

from framework import catalog, cli
from framework.errors import QAError


def make_catalog(root):
    product = root / "products/xgestion"
    (product / "scenarios").mkdir(parents=True)
    (product / "suites").mkdir()
    groups = [
        {"id": "smoke", "title": "Comprobación rápida", "description": "Revisar lo básico.", "stage": 0},
        {"id": "ventas", "title": "Venta cotidiana", "description": "Vender y cancelar.", "stage": 1},
        {"id": "promociones", "title": "Promociones", "description": "Aplicar ofertas.", "stage": 2},
    ]
    (product / "groups.json").write_text(json.dumps({"groups": groups}), encoding="utf-8")
    cases = [
        ("XG-VEN-001", "Venta en efectivo", "implemented", ["smoke", "ventas", "lectura"]),
        ("XG-VEN-003", "Cambiar cantidad", "planned", ["ventas"]),
        ("XG-VEN-004", "Verificar manualmente", "manual", ["ventas"]),
    ]
    for case_id, title, status, tags in cases:
        metadata = {"id": case_id, "title": title, "product": "xgestion", "module": "ventas",
                    "tags": tags, "status": status}
        if status == "implemented":
            metadata["test"] = "products/xgestion/suites/ventas.robot"
        (product / "scenarios" / f"{case_id}.md").write_text(
            "---\n" + json.dumps(metadata) + "\n---\n", encoding="utf-8")
    (product / "suites/ventas.robot").write_text(
        "*** Test Cases ***\nVenta\n    [Tags]    XG-VEN-001    smoke    ventas    lectura\n    No Operation\n",
        encoding="utf-8")
    return product


def test_group_overview_counts_each_status_and_keeps_empty_groups(tmp_path):
    make_catalog(tmp_path)
    cases = catalog.validate_catalog(tmp_path)
    groups = {item["id"]: item for item in catalog.group_overview(tmp_path, "xgestion", cases)}
    assert groups["ventas"]["title"] == "Venta cotidiana"
    assert groups["ventas"]["counts"] == {"implemented": 1, "planned": 1, "manual": 1}
    assert groups["promociones"]["counts"] == {"implemented": 0, "planned": 0, "manual": 0}
    assert groups["smoke"]["counts"]["implemented"] == 1
    assert [item["id"] for item in catalog.select_cases(cases, "xgestion", "ventas", None)] == ["XG-VEN-001"]
    assert [item["id"] for item in catalog.select_cases(cases, "xgestion", "lectura", None)] == ["XG-VEN-001"]
    with pytest.raises(QAError, match="ejecutables"):
        catalog.select_cases(cases, "xgestion", "promociones", None)


@pytest.mark.parametrize("payload", [
    {}, {"groups": []}, {"groups": "ventas"},
    {"groups": [{"id": "ventas", "title": " ", "description": "Prueba", "stage": 1}]},
    {"groups": [{"id": "Ventas!", "title": "Venta", "description": "Prueba", "stage": 1}]},
    {"groups": [{"id": "ventas", "title": "Venta", "description": "Prueba", "stage": True}]},
    {"groups": [{"id": "ventas", "title": "Venta", "description": "Prueba", "stage": -1}]},
])
def test_invalid_group_registry_is_not_silently_ignored(tmp_path, payload):
    product = make_catalog(tmp_path)
    (product / "groups.json").write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(QAError, match="grupos"):
        catalog.validate_catalog(tmp_path)


def test_duplicate_group_id_and_missing_registry_are_errors(tmp_path):
    product = make_catalog(tmp_path)
    registry = product / "groups.json"
    group = json.loads(registry.read_text(encoding="utf-8"))["groups"][0]
    registry.write_text(json.dumps({"groups": [group, group]}), encoding="utf-8")
    with pytest.raises(QAError, match="grupos"):
        catalog.load_groups(tmp_path, "xgestion")
    registry.unlink()
    with pytest.raises(QAError, match="grupos"):
        catalog.validate_catalog(tmp_path)
    assert catalog.load_groups(tmp_path, "mozos") == []


def test_catalog_rejects_scenarios_without_a_registered_module(tmp_path):
    product = make_catalog(tmp_path)
    path = product / "scenarios/XG-VEN-003.md"
    path.write_text(path.read_text(encoding="utf-8").replace('"module": "ventas"', '"module": "vnetas"'),
                    encoding="utf-8")
    with pytest.raises(QAError, match="XG-VEN-003"):
        catalog.validate_catalog(tmp_path)


def test_catalog_reports_malformed_module_without_crashing(tmp_path):
    product = make_catalog(tmp_path)
    path = product / "scenarios/XG-VEN-003.md"
    path.write_text(path.read_text(encoding="utf-8").replace('"module": "ventas"', '"module": ["ventas"]'),
                    encoding="utf-8")
    with pytest.raises(QAError, match="Markdown"):
        catalog.validate_catalog(tmp_path)


def test_cli_lists_named_groups_and_filters_planned_cases(tmp_path, capsys):
    make_catalog(tmp_path)
    assert cli.main(["list", "--groups"], root=tmp_path) == 0
    output = capsys.readouterr().out
    assert "Venta cotidiana" in output and "Vender y cancelar." in output
    assert "1 implementados" in output and "1 pendientes" in output and "1 manuales" in output
    assert "Promociones" in output and "sin pruebas ejecutables" in output
    assert cli.main(["list", "--group", "ventas"], root=tmp_path) == 0
    output = capsys.readouterr().out
    assert "XG-VEN-001" in output and "XG-VEN-003" in output and "XG-VEN-004" in output
    assert "pendiente" in output.lower() and "manual" in output.lower()
    assert cli.main(["list", "--group", "lectura"], root=tmp_path) == 0
    output = capsys.readouterr().out
    assert "XG-VEN-001" in output and "XG-VEN-003" not in output


def test_cli_check_reports_implemented_and_planned_separately(tmp_path, capsys):
    make_catalog(tmp_path)
    assert cli.main(["check"], root=tmp_path) == 0
    output = capsys.readouterr().out
    assert "3 documentados" in output and "1 implementados" in output
    assert "1 pendientes" in output and "1 manuales" in output


def test_list_group_options_are_mutually_exclusive():
    with pytest.raises(SystemExit) as error:
        cli.parser().parse_args(["list", "--groups", "--group", "ventas"])
    assert error.value.code == 2


@pytest.mark.parametrize("requested,expected", [(None, "INFO"), ("debug", "DEBUG"), ("TrAcE", "TRACE")])
def test_cli_passes_log_level_without_changing_legacy_selection(tmp_path, monkeypatch, requested, expected):
    calls = []
    monkeypatch.setattr(cli, "run", lambda *args, **kwargs: calls.append((args, kwargs)) or 0)
    arguments = ["run", "--group", "ventas", "--dry-run"]
    if requested:
        arguments += ["--log-level", requested]
    assert cli.main(arguments, root=tmp_path) == 0
    assert calls == [((tmp_path, "xgestion", "ventas", None, True), {"log_level": expected})]


def test_cli_rejects_unknown_log_level_before_running(monkeypatch):
    monkeypatch.setattr(cli, "run", lambda *args, **kwargs: pytest.fail("No debe ejecutar"))
    with pytest.raises(SystemExit) as error:
        cli.main(["run", "--log-level", "secrets"])
    assert error.value.code == 2


@pytest.mark.parametrize("selection,group,scenario", [
    ([], "smoke", None), (["--scenario", "XG-VEN-001"], None, "XG-VEN-001"),
])
def test_cli_keeps_default_smoke_and_exact_scenario_selection(tmp_path, monkeypatch, selection, group, scenario):
    calls = []
    monkeypatch.setattr(cli, "run", lambda *args, **kwargs: calls.append((args, kwargs)) or 0)
    assert cli.main(["run", *selection], root=tmp_path) == 0
    assert calls == [((tmp_path, "xgestion", group, scenario, False), {"log_level": "INFO"})]


def test_menu_blocks_empty_group_and_runs_numbered_group_with_log_choice(tmp_path, monkeypatch, capsys):
    make_catalog(tmp_path)
    answers = iter(["4", "", "promociones", "4", "", "2", "2", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    calls = []
    monkeypatch.setattr(cli, "run", lambda *args, **kwargs: calls.append((args, kwargs)) or 0)
    assert cli.menu(tmp_path) == 0
    output = capsys.readouterr().out
    assert "Promociones" in output and "sin pruebas ejecutables" in output
    assert "3. Promociones" not in output
    assert "Paso a paso" in output and "Diagnóstico" in output
    assert calls == [((tmp_path, "xgestion", "ventas", None, False), {"log_level": "DEBUG"})]


def test_menu_numbers_only_groups_with_executable_cases(tmp_path, monkeypatch, capsys):
    make_catalog(tmp_path)
    answers = iter(["4", "", "3", "0"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(cli, "run", lambda *args, **kwargs: pytest.fail("No debe ejecutar un grupo pendiente"))
    assert cli.menu(tmp_path) == 0
    output = capsys.readouterr().out
    assert "Grupo no reconocido" in output
    assert "3. Promociones" not in output


def test_menu_eof_during_nested_prompt_exits_without_traceback(tmp_path, monkeypatch):
    make_catalog(tmp_path)
    answers = iter(["4", ""])

    def answer(_):
        try:
            return next(answers)
        except StopIteration:
            raise EOFError from None

    monkeypatch.setattr("builtins.input", answer)
    assert cli.main([], root=tmp_path) == 0


def test_public_registry_contains_available_and_planned_capabilities():
    root = Path(__file__).resolve().parents[1]
    groups = {item["id"] for item in catalog.load_groups(root, "xgestion")}
    assert {"smoke", "regression", "ventas", "stock", "precios", "promociones", "cobros", "monedas",
            "cuenta-corriente", "permisos", "caja", "mesas", "mozos-qr", "fiscal", "recuperacion"} <= groups


def test_pending_offer_backlog_is_visible_but_never_selected_for_execution():
    root = Path(__file__).resolve().parents[1]
    cases = catalog.validate_catalog(root)
    pending_ids = {"XG-PRM-077", "XG-PRM-078"}
    planned = [case for case in cases if case["status"] == "planned" and case["id"].startswith("XG-PRM-")]
    assert {case["id"] for case in planned} == pending_ids
    assert all("test" not in case for case in planned)
    groups = {group["id"]: group for group in catalog.group_overview(root, "xgestion", cases)}
    for group, count in {"promociones-alcances": 36, "promociones-agrupadas": 21,
                         "promociones-combos": 5, "promociones-condiciones": 15, "ofertas-usd": 5}.items():
        pending = 2 if group == "promociones-condiciones" else 0
        assert groups[group]["counts"] == {"implemented": count - pending, "planned": pending, "manual": 0}
        selected = catalog.select_cases(cases, "xgestion", group, None)
        assert len(selected) == len({case["id"] for case in selected}) == count - pending
        assert not pending_ids.intersection(case["id"] for case in selected)
    for identifier in pending_ids:
        with pytest.raises(QAError, match="ejecutables"):
            catalog.select_cases(cases, "xgestion", None, identifier)
    promotions = catalog.select_cases(cases, "xgestion", "promociones", None)
    assert {case["id"] for case in promotions} == {
        f"XG-PRM-{number:03}" for number in range(1, 85)
    } - pending_ids
    regression = catalog.select_cases(cases, "xgestion", "regression", None)
    assert len(regression) == len({case["id"] for case in regression}) == 112
    assert not pending_ids.intersection(case["id"] for case in regression)


@pytest.mark.parametrize("group,count", [
    ("restobar", 40), ("listas-precios", 28),
])
def test_new_operational_backlog_is_visible_without_enabling_execution(group, count):
    root = Path(__file__).resolve().parents[1]
    cases = catalog.validate_catalog(root)
    overview = next(item for item in catalog.group_overview(root, "xgestion", cases) if item["id"] == group)
    assert overview["counts"] == {"implemented": 0, "planned": count, "manual": 0}
    with pytest.raises(QAError, match="ejecutables"):
        catalog.select_cases(cases, "xgestion", group, None)
    selected = catalog.select_cases(cases, "xgestion", "regression", None)
    assert len(selected) == len({case["id"] for case in selected}) == 112
    pending = [case for case in cases if group in case["tags"]]
    assert all(not case.get("test") and not case.get("seed") for case in pending)
    assert not {case["id"] for case in pending}.intersection(case["id"] for case in selected)


@pytest.mark.parametrize("group,prefix,count", [
    ("ctacte-clientes", "CCC", 10), ("ctacte-proveedores", "CCP", 8), ("cuotas", "CUO", 6),
    ("libro-diario", "LDI", 8), ("caja", "CAJ", 10), ("conciliacion", "FIN", 10),
    ("inventario", "INV", 4), ("respaldos", "BKP", 2),
    ("cobros-combinados", "COB", 8), ("presupuestos", "PRE", 6), ("devoluciones", "DEV", 6),
    ("fiscal", "FEL", 6), ("pagos-externos", "PEX", 6), ("concurrencia", "CON", 4),
    ("actualizacion", "ACT", 4), ("beneficios", "BEN", 6),
])
def test_critical_circuits_are_planned_and_cannot_be_executed(group, prefix, count):
    root = Path(__file__).resolve().parents[1]
    cases = catalog.validate_catalog(root)
    documented = [case for case in cases if case["id"].startswith(f"XG-{prefix}-")
                  and int(case["id"].rsplit("-", 1)[1]) <= count]
    assert {case["id"] for case in documented} == {f"XG-{prefix}-{number:03}" for number in range(1, count + 1)}
    assert all(case["status"] == "planned" and group in case["tags"] for case in documented)
    assert all("test" not in case and "seed" not in case for case in documented)
    if group in {"libro-diario", "caja", "conciliacion"}:
        assert all(case["status"] == "implemented" for case in
                   catalog.select_cases(cases, "xgestion", group, None))
    else:
        with pytest.raises(QAError, match="ejecutables"):
            catalog.select_cases(cases, "xgestion", group, None)
    regression = catalog.select_cases(cases, "xgestion", "regression", None)
    assert len(regression) == len({case["id"] for case in regression}) == 112
    assert not {case["id"] for case in documented}.intersection(case["id"] for case in regression)


def test_keyboard_groups_select_unique_cases_with_real_validation_pending():
    root = Path(__file__).resolve().parents[1]
    cases = catalog.validate_catalog(root)
    keyboard = catalog.select_cases(cases, "xgestion", "atajos-listados", None)
    filters = catalog.select_cases(cases, "xgestion", "filtros-listados", None)
    assert {case["id"] for case in keyboard} == {f"XG-KEY-{number:03}" for number in range(1, 14)}
    assert len(filters) == 8
    assert {case["id"] for case in filters} <= {case["id"] for case in keyboard}


def test_integrated_circuits_select_only_implemented_and_preserve_remito_backlog():
    root = Path(__file__).resolve().parents[1]
    cases = catalog.validate_catalog(root)
    selected = catalog.select_cases(cases, "xgestion", "circuitos-completos", None)
    assert {case["id"] for case in selected} == {"XG-FIN-011", "XG-FIN-013", "XG-FIN-014"}
    assert len(selected) == 3
    receipt = catalog.select_cases(cases, "xgestion", "remitos", None)
    assert [case["id"] for case in receipt] == ["XG-FIN-013"]
    backlog = [case for case in cases if case["id"].startswith("XG-REM-")]
    assert len(backlog) == 24 and all(case["status"] == "planned" for case in backlog)
    with pytest.raises(QAError, match="ejecutables"):
        catalog.select_cases(cases, "xgestion", None, "XG-FIN-012")
