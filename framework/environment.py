"""Preflight sin iniciar aplicaciones ni modificar red o bases."""

import os
import platform
import subprocess
import sys
from pathlib import Path

import javaproperties

from framework.config import Profile
from framework.errors import QAError
from framework.paths import protect, safe_path

_OFFER_PROFILES = {
    "base": ("true", "true", "false"),
    "general-off": ("false", "true", "false"),
    "offers-off": ("true", "false", "false"),
    "allowed-warning-on": ("true", "true", "true"),
    "allowed-warning-off": ("true", "true", "false"),
}


def _offer_properties(name, company_id):
    if name not in _OFFER_PROFILES or type(company_id) is not int or company_id <= 0:
        raise QAError("El perfil de ofertas debe identificar una variante y empresa QA válidas.")
    general, offers, warning = _OFFER_PROFILES[name]
    recalculate = "venta.recalcularProductosAlCambiarListaPrecioVenta"
    # Config.java and FormVentaDetalle.java: permissions/warning are global;
    # only the recalculation switch uses empresa.<id> precedence.
    return {"venta.permitirDescuentosEdicionArticulos": general,
            "venta.permitirDescuentosManualesArticulosConOferta": offers,
            "alertas.advertirDescuentosManualesArticulosConOferta": warning,
            "venta.listadeprecio.elegir": "true", "pedirPagoAlCerrarTicket": "true", recalculate: "true",
            f"empresa.{company_id}.{recalculate}": "true"}


def ensure_offline() -> None:
    if os.name != "nt":
        raise QAError("Las pruebas de XGestión necesitan Windows x64 y una PC/VM dedicada.")
    command = "@(Get-NetAdapter -IncludeHidden -ErrorAction Stop | Where-Object Status -eq 'Up').Count"
    try:
        result = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", command],
                                capture_output=True, text=True, timeout=20, check=True)
        count = int(result.stdout.strip())
    except (OSError, ValueError, subprocess.SubprocessError):
        raise QAError("No se pudo verificar aislamiento de red. Revisar adaptadores en la VM QA.") from None
    if count:
        raise QAError("La PC/VM tiene adaptadores de red activos. Desconectarlos antes de ejecutar el JAR QA.")


def doctor(profile: Profile, *, calibration: bool = True) -> list[str]:
    if os.name != "nt" or platform.machine().lower() not in ("amd64", "x86_64") or sys.maxsize <= 2**32:
        raise QAError("XGestión requiere Windows x64 en PC/VM dedicada; check y dry-run sí son multiplataforma.")
    if sys.version_info[:2] != (3, 12):
        raise QAError("Ejecutar setup para preparar Python 3.12.")
    java_home = Path(profile.env("QA_JAVA_HOME"))
    if not all((java_home / "bin" / file).is_file() for file in ("java.exe", "jabswitch.exe", "WindowsAccessBridge-64.dll")):
        raise QAError("QA_JAVA_HOME debe apuntar a Java 17 x64 con Java Access Bridge.")
    try:
        java_env = {k: v for k, v in os.environ.items() if k.upper() not in
                    {"JAVA_TOOL_OPTIONS", "_JAVA_OPTIONS", "JDK_JAVA_OPTIONS", "CLASSPATH"}}
        version = subprocess.run([str(java_home / "bin/java.exe"), "-version"], capture_output=True,
                                 text=True, timeout=15, check=True, env=java_env)
    except (OSError, subprocess.SubprocessError):
        raise QAError("No se pudo ejecutar el runtime Java configurado.") from None
    if 'version "17.' not in version.stderr + version.stdout or "64-Bit" not in version.stderr + version.stdout:
        raise QAError("El perfil inicial requiere Java 17 de 64 bits.")
    try:
        import importlib.util
        available = importlib.util.find_spec("RPA.JavaAccessBridge")
        if available is None or importlib.util.find_spec("pymysql") is None:
            raise ImportError
    except (ImportError, ModuleNotFoundError):
        raise QAError("Faltan dependencias de XGestión. Repetir qa.cmd setup.") from None
    with profile.asset("config").open("rb") as source:
        config = javaproperties.load(source)
    if any(not config.get(key) for key in ("licencia", "conexionUsuario", "conexionPassword")):
        raise QAError("El paquete debe incluir licencia QA y conexión cifrada válidas en config.properties.")
    ensure_offline()
    import ctypes
    from ctypes import wintypes

    ctypes.windll.user32.OpenInputDesktop.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    ctypes.windll.user32.OpenInputDesktop.restype = wintypes.HANDLE
    ctypes.windll.user32.SwitchDesktop.argtypes = [wintypes.HANDLE]
    ctypes.windll.user32.SwitchDesktop.restype = wintypes.BOOL
    ctypes.windll.user32.CloseDesktop.argtypes = [wintypes.HANDLE]
    ctypes.windll.user32.CloseDesktop.restype = wintypes.BOOL
    if ctypes.windll.user32.GetSystemMetrics(0x1000):
        raise QAError("Usar la consola local de la PC/VM QA; esta suite no se ejecuta por RDP.")
    desktop = ctypes.windll.user32.OpenInputDesktop(0, False, 0x0100)
    if not desktop:
        raise QAError("El escritorio está bloqueado o no está disponible.")
    try:
        accessible = ctypes.windll.user32.SwitchDesktop(desktop)
    finally:
        ctypes.windll.user32.CloseDesktop(desktop)
    if not accessible or not ctypes.windll.user32.GetForegroundWindow():
        raise QAError("El escritorio debe estar abierto, desbloqueado y accesible desde consola local.")
    if calibration:
        from products.xgestion.contracts import load_assets
        load_assets(profile)
    return ["Paquete y hashes verificados", "Java 17 x64 / Python 3.12", "Red desconectada",
            "Configuración QA presente", "Calibración validada" if calibration else "Modo inspección de login"]


def prepare_app_config(profile: Profile, *, offer_profile=None, company_id=None) -> dict:
    overrides = _offer_properties(offer_profile, company_id) if offer_profile is not None else {}
    directory = profile.runtime / "app"
    if not directory.resolve().is_relative_to(profile.runtime.resolve()):
        raise QAError("La carpeta de ejecución de XGestión sale del runtime privado.")
    directory.mkdir(exist_ok=True)
    protect(directory)
    with profile.asset("config").open("rb") as source:
        values = javaproperties.load(source)
    values.update({"conexionIp": "127.0.0.1", "conexionPuerto": "13317", "conexionBaseDatos": "xsoft_qa",
                   "sincronizadorActiva": "false"})
    values.update(overrides)
    # Las credenciales cifradas las prepara el administrador con el ERP, no se reimplementa su cifrado.
    destination = safe_path(directory, "config.properties")
    with destination.open("w", encoding="ascii", newline="\n") as target:
        javaproperties.dump(values, target, timestamp=False)
    protect(destination)
    with destination.open("rb") as target:
        actual = javaproperties.load(target)
    if actual != values:
        raise QAError("La copia local de configuración no coincide con el perfil preparado.")
    return {"profile": offer_profile or "baseline", "properties": overrides}
