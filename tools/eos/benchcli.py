"""Thin subprocess wrappers over the frozen benchmark suite.

benchmark/harness.py and benchmark/score.py are frozen under
benchmark/FREEZE_MANIFEST.json. This module never imports them and
never reimplements any scoring: every call is a subprocess with the
arguments passed straight through, so the frozen behaviour is the only
behaviour, and the frozen script's exit code is the one the caller
sees.

drills is different in kind: the pack acceptance drills are not part of
the frozen suite, so this module hands the work to tools.eos.drills and
only shapes the result for the CLI. It adds no scoring of its own.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from .findings import Finding, Findings


def _invoke(root, script, args):
    script_path = Path(root) / "benchmark" / script
    if not script_path.is_file():
        raise FileNotFoundError("frozen benchmark script missing: %s" % script_path)
    return subprocess.run(
        [sys.executable, str(script_path), *[str(a) for a in args]],
        cwd=str(root), capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    )


def harness(root, args):
    """Invoke benchmark/harness.py with pass-through args."""
    return _invoke(root, "harness.py", args)


def score(root, args):
    """Invoke the frozen benchmark/score.py with pass-through args."""
    return _invoke(root, "score.py", args)


def drills(root, action, pack=None, scratch=None, record=False,
           attempt=None):
    """List or run the pack acceptance drills.

    Returns `(payload, code)`. `payload` is the JSON document the CLI
    prints, `code` the process exit code: 0 when every requested drill
    passed outright, 1 on any failed criterion or any drill left without
    a verdict, 2 when the command cannot run at all.

    A drill whose criteria are all manual reports `pass: null` and is
    never counted as a pass. That is the whole point of the command.
    """
    from . import drills as drillmod

    if action not in ("list", "run"):
        raise ValueError("drills action must be 'list' or 'run': %r" % (action,))
    try:
        manifest = drillmod.load_manifest(root)
        if action == "list":
            rows = drillmod.list_drills(root, manifest=manifest)
            payload = {
                "action": "list",
                "count": len(rows),
                "runnable": sum(1 for r in rows if r["runnable"]),
                "frozen_before_authoring": sum(
                    1 for r in rows if r["frozen_before_authoring"] is True),
                "drills": rows,
            }
            bad = [r["pack"] for r in rows if not r["hash_ok"]]
            if bad:
                payload["hash_mismatch"] = bad
                return payload, 2
            return payload, 0

        if pack:
            results = [drillmod.run_drill(
                root, pack, scratch_root=scratch, manifest=manifest,
                attempt=attempt)]
        elif attempt:
            raise drillmod.DrillError(
                "--attempt grades one delivered tree, so it needs --pack")
        else:
            results = drillmod.run_all(
                root, scratch_root=scratch, manifest=manifest)
    except drillmod.DrillError as exc:
        return {"action": action, "error": str(exc)}, 2

    if record:
        drillmod.append_results(root, results)
    code = drillmod.exit_code(results)
    if pack and len(results) == 1:
        payload = dict(results[0])
        payload["recorded"] = bool(record)
        return payload, code
    return {
        "action": "run",
        "summary": drillmod.summarise(results),
        "recorded": bool(record),
        "drills": results,
    }, code


def drill_findings(payload):
    """Render a drills payload as Findings for human-readable stderr."""
    findings = Findings()
    if "error" in payload:
        findings.add(Finding("DR000", "error", "benchmark/drills",
                             payload["error"]))
        return findings
    rows = payload.get("drills") if isinstance(payload.get("drills"), list) \
        else [payload]
    for row in rows:
        if not isinstance(row, dict) or "pass" not in row:
            continue
        path = row.get("spec", "benchmark/drills")
        if row["pass"] is False:
            findings.add(Finding("DR002", "error", path,
                                 "%s: %s" % (row["pack"], row["reason"])))
        elif row["pass"] is None:
            findings.add(Finding("DR001", "error", path,
                                 "%s: %s" % (row["pack"], row["reason"])))
    return findings
