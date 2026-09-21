"""Private, sanitized events shared by Robot, product adapters and the runner."""

import json
import os
import re
from contextvars import ContextVar
from datetime import datetime, timezone
from pathlib import Path
from threading import Event, Thread

from framework.errors import QAError
from framework.reporting import safe_value

LEVELS = {"INFO": 0, "DEBUG": 1, "TRACE": 2}
_listener = ContextVar("qa_listener", default=None)


def normalize_level(level: str) -> str:
    level = level.upper()
    if level not in LEVELS:
        raise QAError("Nivel de log inválido. Usar INFO, DEBUG o TRACE.")
    return level


class EventWriter:
    def __init__(self, path: Path, *, secrets: list[str]):
        self.path, self.secrets = Path(path), secrets
        # The containing report directory has already been restricted by the runner.
        descriptor = os.open(self.path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
        os.close(descriptor)

    def emit(self, level: str, event: str, message: str, **details) -> dict:
        payload = {"timestamp": datetime.now(timezone.utc).isoformat(), "level": normalize_level(level),
                   "event": event, "message": safe_value(message, self.secrets),
                   **safe_value(details, self.secrets)}
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(payload, ensure_ascii=False, allow_nan=False) + "\n")
            stream.flush()
        return payload


def diagnostic(message, **details) -> None:
    """Emit scalar diagnostics only; do not accept rows, arguments or arbitrary objects."""
    listener = _listener.get()
    if listener is not None:
        scalars = {key: value for key, value in details.items()
                   if value is None or isinstance(value, (str, int, float, bool))}
        listener.trace(message, scalars)


def business_step(message) -> None:
    """Name a business action inside a coarse Robot keyword, without its arguments."""
    listener = _listener.get()
    if listener is not None:
        listener.step(message)


def assertion_failed(message, *, expected=None, observed=None) -> None:
    """Remember a discrepancy; only a final Robot failure makes it a failed case.

    Polling assertions may recover. A successful keyword discards this context.
    """
    listener = _listener.get()
    if listener is not None:
        listener.remember_assertion(message, expected, observed)


def format_event(event: dict) -> str:
    case = f" {event['case_id']}" if event.get("case_id") else ""
    text = f"[{event['level']}]{case} {event['message']}"
    if failure := event.get("failure"):
        text += (f"\n  Paso: {failure['step']}\n  Comprobación: {failure.get('message', 'No completada')}"
                 f"\n  Esperado: {failure['expected']}"
                 f"\n  Observado: {failure['observed']}\n  Categoría: {failure['category']}"
                 f"\n  Causa: {failure['cause']}\n  Evidencia: {', '.join(failure['evidence'])}")
    elif event["event"] == "diagnostic" and event.get("details"):
        text += " | " + json.dumps(event["details"], ensure_ascii=False)
    # Keep untrusted data from injecting additional console records or terminal escapes.
    return re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", "", text)


class EventStream:
    """Tail flushed JSONL while run_owned_process retains control of its own tree."""
    def __init__(self, path: Path, *, level: str, secrets: list[str], emit=None):
        self.path, self.level, self.secrets = Path(path), normalize_level(level), secrets
        self.emit = emit or (lambda message: print(message, flush=True))
        self.offset = self.path.stat().st_size if self.path.exists() else 0
        self.pending, self.events = b"", []
        self.error = None
        self.stop = Event()
        self.thread = Thread(target=self._watch, name="qa-events", daemon=True)

    def drain(self):
        if not self.path.exists():
            return
        with self.path.open("rb") as stream:
            stream.seek(self.offset)
            self.pending += stream.read()
            self.offset = stream.tell()
        lines = self.pending.split(b"\n")
        self.pending = lines.pop()
        for line in lines:
            event = safe_value(json.loads(line.decode("utf-8")), self.secrets)
            self.events.append(event)
            if LEVELS[event["level"]] <= LEVELS[self.level]:
                text = format_event(event)
                with self.path.with_name("console.log").open("a", encoding="utf-8") as log:
                    log.write(text + "\n")
                self.emit(text)

    def _watch(self):
        try:
            while not self.stop.wait(0.05):
                self.drain()
        except Exception:
            self.error = "No se pudo leer el progreso saneado de Robot."

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, *_):
        self.stop.set()
        self.thread.join(timeout=5)
        if self.thread.is_alive():
            self.error = "El lector de eventos no terminó."
            return
        try:
            self.drain()
            if self.pending:
                self.error = "La última línea de eventos está incompleta."
        except Exception:
            self.error = "La evidencia de eventos está incompleta."
