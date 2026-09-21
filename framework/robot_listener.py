"""Robot 7 listener: business progress without raw arguments or console dumps."""

import json
import os
from pathlib import Path

from framework.catalog import CASE_ID
from framework.events import EventWriter, _listener
from framework.reporting import safe_value


class QAListener:
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, directory=None, *, secrets=None, dry_run=None):
        directory = Path(directory or os.environ["XSOFT_QA_RUN_DIR"])
        if secrets is None:
            secrets = json.loads(os.environ.get("XSOFT_QA_REDACTIONS", "[]"))
        self.writer = EventWriter(directory / "events.jsonl", secrets=secrets)
        self.dry_run = dry_run if dry_run is not None else os.environ.get("XSOFT_QA_DRY_RUN") == "1"
        self.case_id, self.frames, self.failures = None, [], []
        self.token = _listener.set(self)
        self.writer.emit("TRACE", "listener_ready", "Listener de progreso preparado.")

    def start_test(self, data, result):
        self.case_id = next((tag for tag in data.tags if CASE_ID.fullmatch(tag)), result.id)
        self.frames, self.failures = [], []
        self.writer.emit("INFO", "case_start", f"Inicia: {data.name}", case_id=self.case_id,
                         name=data.name, robot_id=result.id)

    def start_keyword(self, data, result):
        name = (result.name or data.name).rsplit(".", 1)[-1].replace(" ", "").replace("_", "").casefold()
        builtin_assertion = (getattr(result, "owner", None) == "BuiltIn"
                             and (name.startswith("should") or name == "fail"))
        self.frames.append({"step": data.name, "assertion": None, "failure": None,
                            "builtin_assertion": builtin_assertion})
        if len(self.frames) == 1:
            self.writer.emit("DEBUG", "step_start", f"Paso: {data.name}", case_id=self.case_id, step=data.name)

    def remember_assertion(self, message, expected, observed):
        if self.frames:
            self.frames[-1]["assertion"] = safe_value(
                {"message": message, "expected": expected, "observed": observed}, self.writer.secrets)

    def trace(self, message, details):
        self.writer.emit("TRACE", "diagnostic", message, case_id=self.case_id,
                         step=self.frames[-1]["step"] if self.frames else None, details=details)

    def step(self, message):
        if self.frames:
            self.frames[-1]["step"] = safe_value(message, self.writer.secrets)
            self.frames[-1]["assertion"] = None
        self.writer.emit("DEBUG", "step_start", f"Paso: {message}", case_id=self.case_id, step=message)

    def _failure(self, step, message, assertion=None, builtin_assertion=False):
        category = ("environment_block" if "QAError:" in message else "functional_assertion"
                    if assertion or builtin_assertion else "automation_error")
        return {"step": step or "Preparación del caso", "category": category, "cause": "No determinada",
                "message": assertion["message"] if assertion else message or "El paso no se completó.",
                "expected": assertion.get("expected") if assertion and assertion.get("expected") is not None
                else "El paso debe completar su verificación.",
                "observed": assertion.get("observed") if assertion and assertion.get("observed") is not None
                else message or "El paso no terminó correctamente.",
                "evidence": ["events.jsonl", "output.xml"]}

    def end_keyword(self, data, result):
        if not self.frames:
            return
        frame = self.frames.pop()
        # Child failures caught by Wait Until Keyword Succeeds or TRY/EXCEPT do not
        # become case failures if the enclosing keyword ultimately succeeds.
        if result.status == "FAIL":
            child = frame["failure"]
            failure = (child[1] if child and child[0] and child[0] in result.message else
                       self._failure(frame["step"], result.message, frame["assertion"], frame["builtin_assertion"]))
            if self.frames:
                self.frames[-1]["failure"] = (result.message, failure)
            else:
                self.failures.append((result.message, failure))
        if not self.frames:
            self.writer.emit("DEBUG", "step_end", f"Paso terminado: {data.name} ({result.status})",
                             case_id=self.case_id, step=data.name, robot_status=result.status)

    def end_test(self, data, result):
        if result.status == "PASS":
            status, label = ("validated-only", "VALIDADO EN SECO") if self.dry_run else ("passed", "OK")
            details = {}
        else:
            # Control blocks can catch a top-level keyword failure and fail later.
            # Only reuse details belonging to the final Robot error, not a caught one.
            failure = next((detail for message, detail in reversed(self.failures) if message and message in result.message),
                           None) or self._failure(None, result.message)
            if result.status == "SKIP":
                failure["category"] = "not_run"
            status = "blocked" if failure["category"] in {"environment_block", "not_run", "automation_error"} else "failed"
            label, details = ("BLOQUEADO" if status == "blocked" else "FALLÓ"), {"failure": failure}
        self.writer.emit("INFO", "case_end", f"{label}: {data.name}", case_id=self.case_id,
                         name=data.name, status=status, robot_status=result.status,
                         elapsed_seconds=result.elapsed_time.total_seconds(), **details)
        self.case_id, self.frames, self.failures = None, [], []

    def close(self):
        self.writer.emit("TRACE", "listener_closed", "Listener de progreso finalizado.")
        _listener.reset(self.token)
