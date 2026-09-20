import json
import os
import subprocess
import sys
import time

import psutil
import pytest

from framework.processes import run_owned_process


def alive(pid):
    try:
        return psutil.Process(pid).is_running() and psutil.Process(pid).status() != psutil.STATUS_ZOMBIE
    except psutil.NoSuchProcess:
        return False


def assert_stopped(pids):
    deadline = time.monotonic() + 3
    while any(alive(pid) for pid in pids) and time.monotonic() < deadline:
        time.sleep(0.02)
    assert not [pid for pid in pids if alive(pid)]


def test_success_captures_bytes_and_preserves_nonzero_exit_code(tmp_path):
    result = run_owned_process(
        [sys.executable, "-c", "import sys; print('hello'); print('problem', file=sys.stderr); sys.exit(3)"],
        cwd=tmp_path, env=os.environ.copy(), timeout=5,
    )
    assert result.returncode == 3
    assert result.stdout.strip() == b"hello"
    assert result.stderr.strip() == b"problem"


@pytest.mark.parametrize("parent_exits", [False, True])
def test_timeout_closes_own_tree_and_leaves_other_process_alive(tmp_path, parent_exits):
    # A parent that has already exited leaves the child's pipe open: this is the
    # case a late psutil.children() lookup cannot recover on Windows.
    record = tmp_path / "pids.json"
    program = tmp_path / "parent.py"
    program.write_text(
        "import json, os, pathlib, subprocess, sys, time\n"
        "child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(8)'])\n"
        "pathlib.Path(sys.argv[1]).write_text(json.dumps([os.getpid(), child.pid]))\n"
        f"{'sys.exit(0)' if parent_exits else 'time.sleep(8)'}\n",
        encoding="utf-8",
    )
    outsider = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(8)"],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    pids = []
    try:
        with pytest.raises(subprocess.TimeoutExpired):
            run_owned_process([sys.executable, str(program), str(record)],
                              cwd=tmp_path, env=os.environ.copy(), timeout=1)
        assert record.exists(), "The dummy process never reached the child creation step"
        pids = json.loads(record.read_text())
        assert_stopped(pids)
        assert outsider.poll() is None
    finally:
        if outsider.poll() is None:
            outsider.terminate()
        outsider.wait(timeout=3)
        # Test cleanup in case a regression is discovered; only recorded PIDs.
        for pid in pids:
            if alive(pid):
                psutil.Process(pid).kill()


def test_keyboard_interrupt_closes_real_child_tree(tmp_path, monkeypatch):
    record = tmp_path / "interrupt-pids.json"
    program = tmp_path / "interrupt-parent.py"
    program.write_text(
        "import json, os, pathlib, subprocess, sys, time\n"
        "child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(8)'])\n"
        "pathlib.Path(sys.argv[1]).write_text(json.dumps([os.getpid(), child.pid]))\n"
        "time.sleep(8)\n",
        encoding="utf-8",
    )
    original = subprocess.Popen.communicate
    interrupted = False

    def interrupt_once(process, *args, **kwargs):
        nonlocal interrupted
        if not interrupted:
            interrupted = True
            deadline = time.monotonic() + 3
            while not record.exists() and time.monotonic() < deadline:
                time.sleep(0.02)
            assert record.exists(), "Dummy did not initialize before the simulated Ctrl+C"
            raise KeyboardInterrupt
        return original(process, *args, **kwargs)

    monkeypatch.setattr(subprocess.Popen, "communicate", interrupt_once)
    try:
        with pytest.raises(KeyboardInterrupt):
            run_owned_process([sys.executable, str(program), str(record)],
                              cwd=tmp_path, env=os.environ.copy(), timeout=5)
        assert_stopped(json.loads(record.read_text()))
    finally:
        if record.exists():
            for pid in json.loads(record.read_text()):
                if alive(pid):
                    psutil.Process(pid).kill()
