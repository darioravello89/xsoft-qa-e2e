"""Una entrada común para personas QA, IA local y CI."""

import argparse
import json
import os
import sys
import webbrowser
from datetime import date
from pathlib import Path

from framework.bundle import calibrate, import_bundle
from framework.catalog import PRODUCTS, group_overview, load_catalog, validate_catalog
from framework.config import load_profile, write_env
from framework.environment import doctor
from framework.errors import QAError
from framework.paths import safe_path
from framework.runner import run

ROOT = Path(__file__).resolve().parents[1]


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(description="Xsoft QA: elegir, ejecutar y revisar escenarios de prueba.")
    commands = cli.add_subparsers(dest="command")
    setup = commands.add_parser("setup", help="Importar el paquete privado sin sobrescribir el perfil existente")
    setup.add_argument("--product", choices=PRODUCTS, default="xgestion")
    setup.add_argument("--bundle", type=Path, help="ZIP privado entregado por el referente QA")
    for name in ("doctor", "list", "run", "inspect"):
        command = commands.add_parser(name)
        command.add_argument("--product", choices=PRODUCTS, default="xgestion")
        if name == "run":
            selection = command.add_mutually_exclusive_group()
            selection.add_argument("--group", help="Etiqueta, por ejemplo smoke, regression o ventas")
            selection.add_argument("--scenario", help="Identificador exacto, por ejemplo XG-VEN-001")
            command.add_argument("--dry-run", action="store_true", help="Validar sintaxis sin abrir el producto")
            command.add_argument("--log-level", type=str.upper, choices=("INFO", "DEBUG", "TRACE"), default="INFO",
                                 help="INFO: resumen; DEBUG: paso a paso; TRACE: diagnóstico local")
            command.add_argument("--seed", choices=("catalogo-comercial-v1",),
                                 help="Aplicar catálogo extra tras restaurar la base privada; opcional")
        if name == "list":
            selection = command.add_mutually_exclusive_group()
            selection.add_argument("--groups", action="store_true", help="Ver grupos y cantidad de casos por estado")
            selection.add_argument("--group", help="Ver los casos de un grupo o etiqueta, incluidos los pendientes")
    report = commands.add_parser("report")
    report.add_argument("--latest", action="store_true", help="Abrir el último informe local")
    commands.add_parser("check", help="Validar catálogo y correspondencia documentación/pruebas")
    calibration = commands.add_parser("calibrate", help="Importar un mapa de controles verificado para el JAR actual")
    calibration.add_argument("--locators", type=Path, required=True)
    seed = commands.add_parser("seed", help="Revisar o preparar el catálogo fijo de datos QA")
    seed.add_argument("--product", choices=PRODUCTS, default="xgestion")
    action = seed.add_mutually_exclusive_group()
    action.add_argument("--dry-run", action="store_true", help="Vista previa sin perfil privado ni conexión a DB")
    action.add_argument("--apply", action="store_true",
                        help="Restaurar baseline y aplicar seed SOLO en 127.0.0.1:13317/xsoft_qa privada; reemplaza sus datos")
    seed.add_argument("--reference-date", type=date.fromisoformat, metavar="AAAA-MM-DD",
                      help="Fecha del catálogo; al aplicar debe coincidir con la fecha del MySQL QA")
    seed.add_argument("--export", action="store_true", help="Guardar SQL revisable en work/seed-preview.sql")
    return cli


def latest_report(root: Path) -> Path:
    try:
        name = json.loads((root / "reports/latest.json").read_text(encoding="utf-8"))["directory"]
        directory = safe_path(root / "reports", name)
        report = directory / "report.html"
        if not report.exists():
            report = directory / "summary.json"
        if not report.exists():
            raise ValueError
        return report
    except (KeyError, ValueError, OSError):
        raise QAError("Todavía no hay informes. Ejecutar un grupo de pruebas primero.") from None


def counts_text(counts: dict) -> str:
    return (f"{counts['implemented']} implementados | {counts['planned']} pendientes | "
            f"{counts['manual']} manuales")


def show_groups(groups: list[dict], *, numbered: bool = False) -> None:
    for index, group in enumerate(groups, 1):
        prefix = f"{index}. " if numbered else ""
        availability = "" if group["counts"]["implemented"] else " | sin pruebas ejecutables"
        print(f"{prefix}{group['title']} [{group['id']}] | etapa {group['stage']}")
        print(f"   {group['description']}")
        print(f"   {counts_text(group['counts'])}{availability}")


def menu_group(root: Path, product: str) -> str | None:
    groups = group_overview(root, product)
    if not groups:
        print("Producto pendiente; sin pruebas ejecutables.")
        return None
    executable = [group for group in groups if group["counts"]["implemented"]]
    pending = [group for group in groups if not group["counts"]["implemented"]]
    show_groups(executable, numbered=True)
    if pending:
        print("Sin pruebas ejecutables todavía:")
        for group in pending:
            print(f"- {group['title']} [{group['id']}]")
    if not executable:
        return None
    selected = input("Número o clave del grupo [smoke]: ").strip() or "smoke"
    if selected.isdecimal() and 1 <= int(selected) <= len(executable):
        selected = executable[int(selected) - 1]["id"]
    group = next((group for group in groups if group["id"] == selected), None)
    if group is None:
        print("Grupo no reconocido. Elegir un número o una clave de la lista.")
        return None
    if not group["counts"]["implemented"]:
        print(f"{group['title']}: sin pruebas ejecutables; consultar sus escenarios pendientes o manuales.")
        return None
    return selected


def menu_log_level() -> str | None:
    print("Detalle: 1. Resumen (INFO) | 2. Paso a paso (DEBUG) | 3. Diagnóstico (TRACE)")
    selected = input("Nivel [1]: ").strip().upper() or "1"
    level = {"1": "INFO", "2": "DEBUG", "3": "TRACE"}.get(selected, selected)
    if level not in ("INFO", "DEBUG", "TRACE"):
        print("Nivel no reconocido. Elegir Resumen, Paso a paso o Diagnóstico por su número.")
        return None
    return level


def menu(root: Path) -> int:
    while True:
        print("\nXSOFT QA\n1. Preparar perfil privado\n2. Revisar requisitos\n3. Ver escenarios")
        print("4. Ejecutar grupo\n5. Ejecutar escenario\n6. Abrir último informe\n7. Ver grupos\n0. Salir")
        try:
            choice = input("Opción: ").strip()
        except EOFError:
            return 0
        if choice == "0":
            return 0
        arguments = []
        if choice == "1":
            bundle = input("Ruta del ZIP privado (sin contraseñas): ").strip().strip('"')
            arguments = ["setup", "--bundle", bundle]
        elif choice in ("2", "3", "4", "5", "7"):
            print("Productos: xgestion | xportal (pendiente) | mozos (pendiente) | consultador (pendiente)")
            product = input("Producto [xgestion]: ").strip() or "xgestion"
            if product not in PRODUCTS:
                print("Producto no reconocido.")
                continue
            arguments = [{"2": "doctor", "3": "list", "4": "run", "5": "run", "7": "list"}[choice],
                         "--product", product]
            if choice == "4":
                group = menu_group(root, product)
                if group is None:
                    continue
                arguments += ["--group", group]
            elif choice == "5":
                arguments += ["--scenario", input("ID del escenario: ").strip()]
            elif choice == "7":
                arguments += ["--groups"]
            if choice in ("4", "5"):
                level = menu_log_level()
                if level is None:
                    continue
                arguments += ["--log-level", level]
        elif choice == "6":
            arguments = ["report", "--latest"]
        else:
            print("Elegir una opción de la lista.")
            continue
        result = main(arguments, root=root)
        if result:
            print(f"Resultado {result}: revisar el mensaje anterior. No se aprobó una ejecución E2E.")


def main(argv=None, *, root: Path = ROOT) -> int:
    try:
        args = parser().parse_args(argv)
        if args.command is None:
            return menu(root)
        if args.command == "check":
            cases = validate_catalog(root)
            counts = {status: sum(case["status"] == status for case in cases)
                      for status in ("implemented", "planned", "manual")}
            print(f"Catálogo válido: {len(cases)} documentados | {counts_text(counts)}. Esto no ejecuta el producto.")
            return 0
        if args.command == "calibrate":
            calibrate(root, args.locators.resolve())
            print("Mapa de controles actualizado localmente. Se conservó un respaldo de la calibración anterior.")
            return 0
        if args.command == "setup":
            if args.product != "xgestion":
                raise QAError("La instalación de este producto está pendiente; consultar su README.")
            if args.bundle is None:
                raise QAError("Requisitos instalados. Falta --bundle RUTA_AL_PAQUETE_PRIVADO para configurar el entorno.")
            import_bundle(root, args.bundle.resolve())
            profile = load_profile(root)
            if not profile.values.get("QA_JAVA_HOME") and os.environ.get("JAVA_HOME"):
                profile.values["QA_JAVA_HOME"] = os.environ["JAVA_HOME"]
                write_env(root / ".env.local", profile.values)
            print("Paquete importado. Perfil y credenciales guardados localmente; todavía no se ejecutó XGestión.")
            print("Desconectar la red de la PC/VM QA y ejecutar qa.cmd doctor.")
            return 0
        if args.command == "list":
            if PRODUCTS[args.product] == "planned":
                print(f"{args.product}: pendiente de implementación. No hay pruebas ejecutables.")
                return 0
            cases = [case for case in load_catalog(root) if case["product"] == args.product]
            groups = group_overview(root, args.product, cases)
            if args.groups:
                show_groups(groups)
                return 0
            if args.group:
                matching = [group for group in groups if group["id"] == args.group]
                show_groups(matching)
                cases = [case for case in cases if args.group in case["tags"]]
                if not matching and not cases:
                    raise QAError("Grupo o etiqueta sin escenarios. Usar qa.cmd list --groups.")
            if not cases:
                print("Todavía no hay escenarios documentados para este grupo.")
                return 0
            labels = {group["id"]: group["title"] for group in groups}
            statuses = {"implemented": "implementado", "planned": "pendiente", "manual": "manual"}
            for case in cases:
                names = [labels[tag] for tag in case["tags"] if tag in labels]
                print(f"{case['id']} | {case['title']} | {', '.join(names)} | {statuses[case['status']]}")
            print("Implementado indica automatización disponible; no acredita una ejecución real aprobada.")
            return 0
        if args.command == "doctor":
            if args.product != "xgestion":
                raise QAError("Producto pendiente de incorporación; no hay un entorno validado.")
            for message in doctor(load_profile(root)):
                print(f"OK: {message}")
            print("Preflight completo. La licencia, la base y los selectores se comprobarán al ejecutar el JAR.")
            return 0
        if args.command == "run":
            options = {"log_level": args.log_level}
            if args.seed:
                options["seed"] = args.seed
            return run(root, args.product, args.group or (None if args.scenario else "smoke"), args.scenario,
                       args.dry_run, **options)
        if args.command == "seed":
            if args.product != "xgestion":
                raise QAError("El catálogo seed solo está disponible para xgestion.")
            from products.xgestion.seeds.command import run_seed
            return run_seed(root, apply=args.apply, dry_run=args.dry_run,
                            reference_date=args.reference_date, export=args.export)
        if args.command == "inspect":
            return run(root, args.product, group="smoke", inspect=True)
        if args.command == "report":
            report = latest_report(root)
            print(f"Abriendo informe local: {report}")
            webbrowser.open(report.as_uri())
            return 0
    except QAError as error:
        print(f"BLOQUEADO: {error}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("Ejecución cancelada.", file=sys.stderr)
        return 130
    except EOFError:
        return 0
    except (OSError, ValueError):
        print("BLOQUEADO: no se pudo leer o escribir la configuración local. Revisar permisos y formato.", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())
