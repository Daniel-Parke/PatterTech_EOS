"""Shared helpers for the DRILL-BLM-001 graders. Stdlib only.

Not a grader. The runner looks for `c<N>.py` by name, so this file is
never mistaken for a criterion.

Exit codes follow the grader contract: 0 pass, 1 fail, 2 the criterion
cannot be settled in this environment. The third exists because one
criterion runs pytest and another needs the IANA time zone database,
and a machine missing either would otherwise report the agent's work as
broken when the truth is that nothing looked at it.

Most of these criteria are claims about behaviour, not about text, so
the helper that matters here is `settle`: it runs a short probe script
in a subprocess with the delivered tree on `PYTHONPATH`, and reads back
one marked JSON verdict. The probe never runs from inside the delivered
tree and never writes to it.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PASS, FAIL, UNSETTLED = 0, 1, 2

MARKER = "@@drill-blm-verdict@@"

PROBE_PREAMBLE = '''\
import json
import sys
import traceback

MARKER = %r


def report(good, reason):
    print(MARKER + json.dumps({"ok": bool(good), "reason": str(reason)}))
    sys.stdout.flush()
    raise SystemExit(0)


def ok(reason):
    report(True, reason)


def fail(reason):
    report(False, reason)
''' % (MARKER,)

# Every probe that needs a booking builds it the same way the committed
# acceptance suite does, so a tree that satisfies the suite is not then
# tripped up by a grader inventing a different constructor.
BOOKING_SETUP = '''
import datetime as dt

from booking.api import Booking, Money, Status

RATE = Money(11000, "GBP")
CHECK_IN = dt.date(2026, 3, 5)
CHECK_OUT = dt.date(2026, 3, 8)
TAKEN_AT = dt.datetime(2026, 3, 1, 9, 0, tzinfo=dt.timezone.utc)


def a_hold(**changes):
    fields = {
        "rate": RATE,
        "check_in": CHECK_IN,
        "check_out": CHECK_OUT,
        "held_at": TAKEN_AT,
    }
    fields.update(changes)
    return Booking(**fields)
'''


def emit(cid, code, reason):
    print(json.dumps({"id": cid, "pass": code == PASS, "reason": reason}))
    sys.exit(code)


def scratch_dir():
    if len(sys.argv) < 2:
        emit("c0", FAIL, "usage: c<N>.py <scratch-dir>")
    path = Path(sys.argv[1]).resolve()
    if not path.is_dir():
        emit("c0", FAIL, "scratch dir not found: %s" % path)
    return path


def read(path):
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def normalise(text):
    """Line endings only. A checkout is allowed to change those."""
    return text.replace("\r\n", "\n").replace("\r", "\n")


# --------------------------------------------------------------- the tree


def booking_modules(scratch):
    """Every Python file in the delivered package, `__init__` included."""
    root = Path(scratch) / "booking"
    if not root.is_dir():
        return []
    return sorted(p for p in root.rglob("*.py")
                  if "__pycache__" not in p.parts)


def implementation_present(scratch):
    """Has anything at all been written into `booking/`?

    The fixture ships an empty package, so this separates "the model is
    wrong" from "there is no model". Criteria that would otherwise pass
    vacuously on an untouched tree, such as "no float appears" and "no
    dependency was added", use it as a precondition.
    """
    for path in booking_modules(scratch):
        if read(path).strip():
            return True
    return False


def require_implementation(cid, scratch):
    if not implementation_present(scratch):
        emit(cid, FAIL,
             "booking/ holds no code, so there is no model to judge; this "
             "criterion is a claim about a delivered model and an empty "
             "package cannot satisfy it")
    return scratch


IMPORT_FROM = re.compile(r"^\s*from\s+([\w.]+)\s+import\s", re.M)
IMPORT_PLAIN = re.compile(r"^\s*import\s+([\w.]+(?:\s*,\s*[\w.]+)*)", re.M)


def imports_of(text):
    """Top level module names a Python source string reaches for.

    A regex rather than an AST walk, because the graders only ask which
    top level package a delivered file names, and this answers that
    without executing anything.
    """
    found = set()
    for match in IMPORT_FROM.finditer(text):
        found.add(match.group(1).split(".", 1)[0])
    for match in IMPORT_PLAIN.finditer(text):
        for part in match.group(1).split(","):
            part = part.strip()
            if part:
                found.add(part.split(".", 1)[0])
    return {f for f in found if f}


# ------------------------------------------------------------- the probe


def build_probe(body):
    lines = normalise(body).strip("\n").splitlines()
    indented = "\n".join(("    " + line) if line.strip() else ""
                         for line in lines)
    return (
        PROBE_PREAMBLE
        + "\ntry:\n"
        + indented
        + "\n    fail('the probe ran to the end without reaching a verdict')\n"
        + "except SystemExit:\n"
        + "    raise\n"
        + "except BaseException:\n"
        + "    _lines = traceback.format_exc(limit=6).strip().splitlines()\n"
        + "    fail('the delivered tree raised while being exercised: '\n"
        + "         + (_lines[-1] if _lines else 'unknown error'))\n"
    )


def run_probe(scratch, body, timeout=180):
    """Run a probe against the delivered tree. Returns (ok_or_None, reason).

    `None` means the probe produced no verdict at all, which is a fact
    about the delivered tree rather than about the environment: it did
    not import, or it killed the interpreter.
    """
    work = tempfile.mkdtemp(prefix="drill-blm-probe-")
    try:
        script = Path(work) / "probe.py"
        script.write_text(build_probe(body), encoding="utf-8")
        env = dict(os.environ)
        env["PYTHONPATH"] = str(scratch) + os.pathsep + env.get("PYTHONPATH", "")
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        try:
            proc = subprocess.run(
                [sys.executable, str(script)], cwd=str(scratch),
                capture_output=True, text=True, encoding="utf-8",
                errors="replace", timeout=timeout, env=env)
        except (OSError, subprocess.TimeoutExpired) as exc:
            return None, "the probe could not be run: %s" % exc
        for line in reversed((proc.stdout or "").splitlines()):
            if line.startswith(MARKER):
                try:
                    doc = json.loads(line[len(MARKER):])
                except ValueError:
                    continue
                return bool(doc.get("ok")), str(doc.get("reason", ""))
        tail = " ".join((proc.stderr or proc.stdout or "").split())[-300:]
        return None, ("the probe reached no verdict (exit %d): %s"
                      % (proc.returncode, tail or "no output at all"))
    finally:
        shutil.rmtree(work, ignore_errors=True)


def settle(cid, scratch, body):
    good, reason = run_probe(scratch, body)
    if good is None:
        emit(cid, FAIL, reason)
    emit(cid, PASS if good else FAIL, reason)


# --------------------------------------------------------- the toolchain


def pytest_available():
    try:
        proc = subprocess.run([sys.executable, "-m", "pytest", "--version"],
                              capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=120)
    except (OSError, subprocess.TimeoutExpired):
        return False
    return proc.returncode == 0


def zoneinfo_available():
    try:
        from zoneinfo import ZoneInfo
    except ImportError:
        return False
    try:
        ZoneInfo("Europe/London")
    except Exception:
        return False
    return True
