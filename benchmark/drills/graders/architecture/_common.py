"""Shared helpers for the DRILL-ARCH-001 graders. Stdlib only.

Not a grader. The runner looks for `c<N>.py` by name, so this file is
never mistaken for a criterion.

Exit codes follow the grader contract: 0 pass, 1 fail, 2 the criterion
cannot be settled in this environment. The third exists because three
of these criteria drive `lint-imports`, and a machine without
import-linter installed would otherwise report the agent's work as
broken when the truth is that nothing looked at it.
"""

import configparser
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

PASS, FAIL, UNSETTLED = 0, 1, 2

CONFIG_NAMES = (".importlinter", "setup.cfg", "tox.ini", "pyproject.toml")


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


def find_config(scratch):
    """Return (path, parsed_sections) for the first parseable config.

    parsed_sections maps a section name to a dict of its options, for
    both the INI forms and the pyproject table, so a caller can reason
    about contracts without caring which file carried them.
    """
    for name in CONFIG_NAMES:
        path = Path(scratch) / name
        if not path.is_file():
            continue
        if name == "pyproject.toml":
            sections = _from_pyproject(path)
        else:
            sections = _from_ini(path)
        if sections is not None:
            return path, sections
    return None, None


def _from_ini(path):
    parser = configparser.ConfigParser()
    try:
        parser.read(path, encoding="utf-8")
    except configparser.Error:
        return None
    out = {}
    for section in parser.sections():
        if section == "importlinter" or section.startswith("importlinter:"):
            out[section] = dict(parser.items(section))
    return out or None


def _from_pyproject(path):
    try:
        import tomllib
    except ImportError:
        return None
    try:
        with open(path, "rb") as handle:
            doc = tomllib.load(handle)
    except (OSError, ValueError):
        return None
    tool = doc.get("tool", {}).get("importlinter")
    if not isinstance(tool, dict):
        return None
    out = {"importlinter": {k: v for k, v in tool.items()
                            if k != "contracts"}}
    for i, contract in enumerate(tool.get("contracts", []) or []):
        if isinstance(contract, dict):
            out["importlinter:contract:%d" % i] = dict(contract)
    return out


def as_list(value):
    """Contract options are newline lists in INI and real lists in TOML."""
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return [str(v).strip() for v in value if str(v).strip()]
    return [line.strip() for line in str(value).splitlines() if line.strip()]


def contracts(sections):
    """Every contract section, as a dict of its options."""
    return [opts for name, opts in sections.items()
            if name.startswith("importlinter:contract")]


def top_package(module):
    return str(module).split(".", 1)[0].strip()


def lint_available():
    if shutil.which("lint-imports"):
        return True
    try:
        import importlinter  # noqa: F401
    except ImportError:
        return False
    return True


def run_lint(scratch):
    """Run lint-imports in the scratch tree. Returns (returncode, output)."""
    if shutil.which("lint-imports"):
        cmd = ["lint-imports"]
    else:
        cmd = [sys.executable, "-m", "importlinter.cli", "lint-imports"]
    env = dict(os.environ)
    env["PYTHONPATH"] = str(scratch) + os.pathsep + env.get("PYTHONPATH", "")
    try:
        proc = subprocess.run(cmd, cwd=str(scratch), capture_output=True,
                              text=True, encoding="utf-8", errors="replace",
                              timeout=240, env=env)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, str(exc)
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def require_lint(cid):
    if not lint_available():
        emit(cid, UNSETTLED,
             "import-linter is not installed here, so this criterion was "
             "not settled. That is a gap in the environment, not a finding "
             "against the delivered tree.")


def catalogue_modules(scratch):
    """Every catalogue module file, public and private."""
    root = Path(scratch) / "catalogue"
    if not root.is_dir():
        return []
    return sorted(p for p in root.rglob("*.py") if p.name != "__init__.py")


def read(path):
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def imports_of(text):
    """Module names imported by a Python source string, roughly.

    Good enough for a fixture this size: the graders only ask which top
    level package a delivered file reaches for, and a regex over import
    statements answers that without executing anything.
    """
    found = set()
    for match in re.finditer(r"^\s*from\s+([\w.]+)\s+import\s", text, re.M):
        found.add(match.group(1))
    for match in re.finditer(r"^\s*import\s+([\w.]+(?:\s*,\s*[\w.]+)*)",
                             text, re.M):
        for part in match.group(1).split(","):
            found.add(part.strip())
    return {f for f in found if f}
