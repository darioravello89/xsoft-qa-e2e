"""Calibración interactiva: la persona navega, el inspector sólo observa su PID."""

import json
import logging
import time

from framework.errors import QAError
from products.xgestion.driver import JarProcess, create_bridge, private_input


def sanitize(value, secrets):
    text = str(value)
    for secret in sorted((value for value in secrets if value), key=len, reverse=True):
        text = text.replace(secret, "[redactado]")
    return text


def safe_nodes(nodes, secrets):
    result = []
    for node in nodes:
        role = str(getattr(node, "role", ""))
        editable = "text" in role.lower() or "password" in role.lower()
        result.append({
            "role": sanitize(role, secrets),
            "name": "[campo omitido]" if editable else sanitize(getattr(node, "name", ""), secrets),
            "description": "" if editable else sanitize(getattr(node, "description", ""), secrets),
            "ancestry": getattr(node, "ancestry", None),
            "indexInParent": getattr(node, "indexInParent", None),
        })
    return result


def inspect_login(profile, run_dir):
    process = JarProcess(profile)
    previous_logging = logging.root.manager.disable
    logging.disable(logging.CRITICAL)
    bridge = None
    try:
        bridge = create_bridge(profile)
        pid = process.start()
        deadline = time.monotonic() + 120
        while not any(w.pid == pid for w in bridge.list_java_windows()):
            if process.process.poll() is not None:
                raise QAError("El JAR terminó antes de publicar una ventana accesible.")
            if time.monotonic() >= deadline:
                raise QAError("JAB no detectó el JAR propio. La viabilidad GUI todavía no está demostrada.")
            time.sleep(0.5)
        run_dir.mkdir(parents=True, exist_ok=True)
        secrets = [value for key, value in profile.values.items()
                   if "PASSWORD" in key or "TOKEN" in key or key == "QA_LOGIN_USER"]
        index = 0
        while True:
            index += 1
            snapshots = []
            with private_input():
                windows = list(bridge.list_java_windows())
                for window in windows:
                    if window.pid != pid:
                        continue
                    # Nunca seleccionar por título si otro proceso tiene uno idéntico.
                    if sum(w.title == window.title for w in windows) != 1:
                        raise QAError("Título Java ambiguo durante inspección; cerrar instancias ajenas.")
                    import re
                    bridge.select_window_by_title("^" + re.escape(window.title) + "$", timeout=5)
                    bridge.application_refresh()
                    snapshots.append({"title": sanitize(window.title, secrets),
                                      "elements": safe_nodes(bridge.get_locator_tree(), secrets)})
            if not snapshots:
                raise QAError("El JAR QA ya no tiene ventanas accesibles.")
            target = run_dir / f"jab-snapshot-{index:02d}.json"
            target.write_text(json.dumps({"pid": pid, "windows": snapshots}, ensure_ascii=False, indent=2),
                              encoding="utf-8")
            print(f"Estructura guardada: {target}")
            print("Navegar manualmente en XGestion QA; no escribir credenciales en esta consola.")
            try:
                choice = input("Enter: observar ventanas actuales | q: terminar: ").strip().lower()
            except EOFError:
                choice = "q"
            if choice == "q":
                return target
    finally:
        try:
            process.stop()
            if bridge is not None:
                try:
                    bridge.shutdown_jab()
                except Exception:
                    pass
        finally:
            logging.disable(previous_logging)
