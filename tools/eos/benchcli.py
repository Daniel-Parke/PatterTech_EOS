"""Thin subprocess wrappers over the frozen benchmark suite.

benchmark/runner.py and benchmark/score.py are frozen under
benchmark/FREEZE_MANIFEST.json. This module never imports them and
never reimplements any scoring: every call is a subprocess with the
arguments passed straight through, so the frozen behaviour is the only
behaviour.

drills is a stub in this build: packs do not exist yet, so it returns
not-yet-implemented findings for the CLI to surface.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

try:  # The lane T1 findings module is canonical once present.
    from tools.eos.findings import Finding, Findings
except ImportError:  # Reuse the fallback shipped with taskops.
    from tools.eos.taskops import Finding, Findings


def _invoke(root, script, args):
    script_path = Path(root) / "benchmark" / script
    if not script_path.is_file():
        raise FileNotFoundError("frozen benchmark script missing: %s" % script_path)
    return subprocess.run(
        [sys.executable, str(script_path), *[str(a) for a in args]],
        cwd=str(root), capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    )


def runner(root, args):
    """Invoke the frozen benchmark/runner.py with pass-through args."""
    return _invoke(root, "runner.py", args)


def score(root, args):
    """Invoke the frozen benchmark/score.py with pass-through args."""
    return _invoke(root, "score.py", args)


def drills(action, pack=None):
    """Drills stub: packs are not built yet in this build."""
    if action not in ("list", "run"):
        raise ValueError("drills action must be 'list' or 'run': %r" % (action,))
    findings = Findings()
    target = pack or "(all packs)"
    findings.add(Finding(
        "DR000", "error", "benchmark/drills",
        "drills %s %s: not yet implemented; pack acceptance drills land "
        "with the pack waves" % (action, target)))
    return findings
