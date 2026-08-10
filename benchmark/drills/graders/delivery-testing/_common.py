"""Shared helpers for the delivery-testing drill graders. Stdlib only.

Not a grader. The runner looks for `c<N>.py` by name, so this file and
the `oracle/` directory beside it are never mistaken for criteria.

Exit codes follow the grader contract: 0 pass, 1 fail, 2 the criterion
cannot be settled in this environment. The third exists because most of
these criteria drive pytest, and a machine without pytest installed
would otherwise report the agent's work as broken when the truth is
that nothing looked at it.

Two things live here rather than in the scenario tree, on purpose:

- `oracle/` holds the hidden pricing oracle and the authoritative
  recording of the real gateway's response. The frozen spec puts them
  at `.drill/oracle/` in the tree under test, so the graders write them
  into a throwaway copy at that path when they need them. Shipping them
  inside the scenario would hand the agent the answer and tell it that
  it is being graded.
- The pristine scenario is read straight out of the repository, so a
  grader can always compare what was delivered against what was handed
  over, and can revert one file without trusting the attempt's git
  history.
"""

import ast
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PASS, FAIL, UNSETTLED = 0, 1, 2

HERE = Path(__file__).resolve().parent
PRISTINE = HERE.parents[1] / "scenarios" / "delivery-testing"
ORACLE = HERE / "oracle"

PRICING_MODULE = "pricing"
SCHEDULING_MODULE = "scheduling"
FAKES_FILE = "fakes.py"
SCHEDULE_TEST = "tests/test_schedule.py"
RECORDING_NAME = "real_gateway_recording.json"
ORACLE_TEST_NAME = "test_pricing_oracle.py"

IGNORED = shutil.ignore_patterns(
    ".git", "__pycache__", ".pytest_cache", "*.egg-info", ".tox", ".venv")


# ------------------------------------------------------------- plumbing


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


def copy_tree(scratch, prefix):
    """A throwaway copy of the delivered tree. Caller removes the work dir."""
    work = Path(tempfile.mkdtemp(prefix=prefix))
    copy = work / "tree"
    shutil.copytree(scratch, copy, ignore=IGNORED)
    return work, copy


# --------------------------------------------------------------- pytest


def pytest_available():
    try:
        import importlib.util
        return importlib.util.find_spec("pytest") is not None
    except (ImportError, ValueError):
        return False


def require_pytest(cid):
    if not pytest_available():
        emit(cid, UNSETTLED,
             "pytest is not installed for %s, so this criterion was not "
             "settled. That is a gap in the environment, not a finding "
             "against the delivered tree." % Path(sys.executable).name)


def run_pytest(tree, *args, timeout=300):
    """Run pytest inside `tree`. Returns (returncode, combined output)."""
    cmd = [sys.executable, "-m", "pytest", "-q", "--tb=no", "-rf",
           "-p", "no:cacheprovider", *args]
    env = dict(os.environ)
    env["PYTHONPATH"] = str(tree) + os.pathsep + env.get("PYTHONPATH", "")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        proc = subprocess.run(cmd, cwd=str(tree), capture_output=True,
                              text=True, encoding="utf-8", errors="replace",
                              timeout=timeout, env=env)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, str(exc)
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


_NODE_RE = re.compile(r"^(?:FAILED|ERROR)\s+(\S+)", re.M)


def failing_nodes(output):
    """Node ids from pytest's short summary. Empty when nothing failed."""
    return {m.group(1) for m in _NODE_RE.finditer(output or "")}


def tail(output, limit=240):
    return " ".join((output or "").split())[-limit:]


# ---------------------------------------------------------------- trees


def test_files(tree):
    """Every pytest-shaped file in a tree, as paths."""
    root = Path(tree)
    found = []
    for path in root.rglob("*.py"):
        if any(part in (".git", "__pycache__", ".drill") for part in
               path.parts):
            continue
        name = path.name
        if name.startswith("test_") or name.endswith("_test.py") \
                or name == "conftest.py":
            found.append(path)
    return sorted(found)


def relative(tree, path):
    return Path(path).relative_to(tree).as_posix()


def changed_files(tree, suffix=".py"):
    """Delivered files that are new or differ from the pristine scenario."""
    out = []
    for path in Path(tree).rglob("*" + suffix):
        if any(part in (".git", "__pycache__", ".drill") for part in
               path.parts):
            continue
        rel = relative(tree, path)
        original = PRISTINE / rel
        if not original.is_file() or read(original) != read(path):
            out.append(path)
    return sorted(out)


def parse(path):
    """Parse a Python file, or None when it does not compile."""
    try:
        return ast.parse(read(path))
    except SyntaxError:
        return None


def imported_names(node):
    """Module names imported anywhere in a parsed tree."""
    names = set()
    for sub in ast.walk(node):
        if isinstance(sub, ast.Import):
            for alias in sub.names:
                names.add(alias.name)
        elif isinstance(sub, ast.ImportFrom) and sub.module:
            names.add(sub.module)
    return names


def touches_module(node, module):
    """True when a parsed file imports or names the given module."""
    for name in imported_names(node):
        if name == module or name.startswith(module + "."):
            return True
    for sub in ast.walk(node):
        if isinstance(sub, ast.Name) and sub.id == module:
            return True
        if isinstance(sub, ast.Constant) and isinstance(sub.value, str) \
                and sub.value.startswith(module + "."):
            return True
    return False


def dotted(node):
    """The dotted name of a Name or Attribute expression, or ''."""
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
        return ".".join(reversed(parts))
    return ""


def public_classes(path):
    """Public class names defined in a module file."""
    node = parse(path)
    if node is None:
        return []
    return [n.name for n in ast.walk(node)
            if isinstance(n, ast.ClassDef) and not n.name.startswith("_")]


# --------------------------------------------------------------- oracle


def install_oracle(copy, *names):
    """Write the hidden oracle files into `.drill/oracle/` of a copy."""
    target = Path(copy) / ".drill" / "oracle"
    target.mkdir(parents=True, exist_ok=True)
    written = []
    for name in names:
        source = ORACLE / name
        if not source.is_file():
            return None, "oracle file missing from the drill: %s" % name
        shutil.copyfile(source, target / name)
        written.append((target / name))
    return written, ""


def restore_pristine(copy, rel):
    """Put one file back the way the scenario shipped it."""
    source = PRISTINE / rel
    if not source.is_file():
        return False
    target = Path(copy) / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    return True
