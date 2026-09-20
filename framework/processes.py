"""Own the Robot process tree, including Java, for the whole subprocess lifetime.

Windows assigns the suspended child to a private Job before any application code
runs. This also owns descendants after the original process exits. POSIX uses a
new session/process group, which ordinary Robot/Java children inherit.
"""

from __future__ import annotations

import ctypes
import os
import signal
import subprocess
from ctypes import wintypes
from pathlib import Path

import psutil


class _WindowsJob:
    """Minimal Win32 Job Object with kill-on-close and no breakaway permission."""

    def __init__(self):
        class BasicLimits(ctypes.Structure):
            _fields_ = [
                ("process_time", ctypes.c_int64), ("job_time", ctypes.c_int64),
                ("flags", wintypes.DWORD), ("min_working_set", ctypes.c_size_t),
                ("max_working_set", ctypes.c_size_t), ("active_processes", wintypes.DWORD),
                ("affinity", ctypes.c_size_t), ("priority", wintypes.DWORD),
                ("scheduling", wintypes.DWORD),
            ]

        class IOCounters(ctypes.Structure):
            _fields_ = [(name, ctypes.c_uint64) for name in
                        ("read_ops", "write_ops", "other_ops", "read_bytes", "write_bytes", "other_bytes")]

        class ExtendedLimits(ctypes.Structure):
            _fields_ = [
                ("basic", BasicLimits), ("io", IOCounters),
                ("process_memory", ctypes.c_size_t), ("job_memory", ctypes.c_size_t),
                ("peak_process_memory", ctypes.c_size_t), ("peak_job_memory", ctypes.c_size_t),
            ]

        self.kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        signatures = {
            "CreateJobObjectW": ([wintypes.LPVOID, wintypes.LPCWSTR], wintypes.HANDLE),
            "SetInformationJobObject": ([wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID, wintypes.DWORD], wintypes.BOOL),
            "AssignProcessToJobObject": ([wintypes.HANDLE, wintypes.HANDLE], wintypes.BOOL),
            "OpenThread": ([wintypes.DWORD, wintypes.BOOL, wintypes.DWORD], wintypes.HANDLE),
            "ResumeThread": ([wintypes.HANDLE], wintypes.DWORD),
            "CloseHandle": ([wintypes.HANDLE], wintypes.BOOL),
        }
        for name, (arguments, result) in signatures.items():
            function = getattr(self.kernel, name)
            function.argtypes, function.restype = arguments, result
        self.handle = self.kernel.CreateJobObjectW(None, None)
        if not self.handle:
            raise ctypes.WinError(ctypes.get_last_error())
        limits = ExtendedLimits()
        limits.basic.flags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        if not self.kernel.SetInformationJobObject(self.handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)):
            error = ctypes.WinError(ctypes.get_last_error())
            self.close()
            raise error

    def attach_and_resume(self, process):
        # Popen owns this native process handle. PID reuse cannot change its target.
        if not self.kernel.AssignProcessToJobObject(self.handle, int(process._handle)):
            raise ctypes.WinError(ctypes.get_last_error())
        threads = psutil.Process(process.pid).threads()
        if len(threads) != 1:
            raise OSError("No se pudo identificar el hilo inicial suspendido del runner.")
        thread = self.kernel.OpenThread(0x0002, False, threads[0].id)  # THREAD_SUSPEND_RESUME
        if not thread:
            raise ctypes.WinError(ctypes.get_last_error())
        try:
            if self.kernel.ResumeThread(thread) == 0xFFFFFFFF:
                raise ctypes.WinError(ctypes.get_last_error())
        finally:
            self.kernel.CloseHandle(thread)

    def close(self):
        if self.handle:
            handle, self.handle = self.handle, None
            if not self.kernel.CloseHandle(handle):
                raise ctypes.WinError(ctypes.get_last_error())


def _stop_owned_tree(process, job):
    if job is not None:
        # Closing our unnamed Job kills its descendants even if Robot exited.
        job.close()
    else:
        # Group was created atomically by Popen(start_new_session=True).
        # Kill the group before communicate()/wait() reaps the original parent.
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    if process.poll() is None:
        # Also handles failure to assign a still-suspended Windows child to its Job.
        process.kill()
    process.wait(timeout=5)


def run_owned_process(command: list[str], *, cwd: Path, env: dict, timeout: int) -> subprocess.CompletedProcess:
    """Capture bytes like subprocess.run, with scoped cleanup on timeout/Ctrl+C.

    No matching by executable names, no global Java termination, and no attaching
    to preexisting processes. Failure to establish Windows isolation fails closed.
    """
    if timeout <= 0:
        raise ValueError("timeout debe ser positivo")
    job = _WindowsJob() if os.name == "nt" else None
    process = None
    try:
        options = {"creationflags": 0x00000004 | subprocess.CREATE_NO_WINDOW} if job else {"start_new_session": True}
        process = subprocess.Popen(command, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, **options)
        if job:
            job.attach_and_resume(process)
        stdout, stderr = process.communicate(timeout=timeout)
        return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)
    except BaseException as error:
        if process is not None:
            # Do not poll/reap Robot first: it may have exited with children alive.
            _stop_owned_tree(process, job)
            stdout, stderr = process.communicate(timeout=5)
            if isinstance(error, subprocess.TimeoutExpired):
                error.output, error.stderr = stdout, stderr
        raise
    finally:
        if job:
            job.close()
        if process:
            if process.stdout:
                process.stdout.close()
            if process.stderr:
                process.stderr.close()
