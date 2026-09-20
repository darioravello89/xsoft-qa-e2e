"""Una entrada común para personas QA, IA local y CI."""

import argparse
import json
import os
import sys
import webbrowser
from pathlib import Path

from framework.bundle import calibrate, import_bundle
from framework.catalog import PRODUCTS, load_catalog, validate_catalog
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
    report = commands.add_parser("report")
    report.add_argument("--latest", action="store_true", help="Abrir el último informe local")
    commands.add_parser("check", help="Validar catálogo y correspondencia documentación/pruebas")
    calibration = commands.add_parser("calibrate", help="Importar un mapa de controles verificado para el JAR actual")
    calibration.add_argument("--locators", type=Path, required=True)
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


def menu(root: Path) -> int:
    while True:
        print("\nXSOFT QA\n1. Preparar perfil privado\n2. Revisar requisitos\n3. Ver escenarios")
        print("4. Ejecutar grupo\n5. Ejecutar escenario\n6. Abrir último informe\n0. Salir")
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
        elif choice in ("2", "3", "4", "5"):
            print("Productos: xgestion | xportal (pendiente) | mozos (pendiente) | consultador (pendiente)")
            product = input("Producto [xgestion]: ").strip() or "xgestion"
            if product not in PRODUCTS:
                print("Producto no reconocido.")
                continue
            arguments = [{"2": "doctor", "3": "list", "4": "run", "5": "run"}[choice], "--product", product]
            if choice == "4":
                arguments += ["--group", input("Grupo [smoke]: ").strip() or "smoke"]
            elif choice == "5":
                arguments += ["--scenario", input("ID del escenario: ").strip()]
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
            print(f"Catálogo válido: {len(cases)} escenarios documentados. Esto no ejecuta el producto.")
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
            for case in load_catalog(root):
                if case["product"] == args.product:
                    print(f"{case['id']} | {case['title']} | {', '.join(case['tags'])} | {case['status']}")
            return 0
        if args.command == "doctor":
            if args.product != "xgestion":
                raise QAError("Producto pendiente de incorporación; no hay un entorno validado.")
            for message in doctor(load_profile(root)):
                print(f"OK: {message}")
            print("Preflight completo. La licencia, la base y los selectores se comprobarán al ejecutar el JAR.")
            return 0
        if args.command == "run":
            return run(root, args.product, args.group or (None if args.scenario else "smoke"), args.scenario, args.dry_run)
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
    except (OSError, ValueError):
        print("BLOQUEADO: no se pudo leer o escribir la configuración local. Revisar permisos y formato.", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())
