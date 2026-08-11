"""Pack acceptance drills: list them, run them, report them honestly.

Contract: the drills section of tools/CLI_CONTRACTS.md.

A drill is one cold-agent scenario with deterministic criteria, held in
a hash-committed spec under `benchmark/drills/`. This module reads the
frozen manifest, verifies each spec against its recorded sha256, parses
the numbered criteria out of the spec, materialises the drill's
scenario into a scratch directory and runs one grader per criterion.

Three verdicts per criterion and no fourth:

- `pass`   a grader ran against the materialised scenario and exited 0.
- `fail`   a grader ran and exited non-zero.
- `manual` no grader exists for that criterion, or the scenario could
  not be materialised, so the criterion is prose a human must judge.

A manual criterion is never counted as a pass. The drill's own verdict
follows from that: `false` if any criterion failed, `true` only when
every criterion was machine-evaluated and passed, and `null` with a
stated reason in every other case. There is no path through this module
that reports a green drill on unevaluated prose.

Layout the runner expects, all under `benchmark/drills/`:

    MANIFEST.json          the frozen index, one entry per pack
    <pack>.md              the frozen spec, and the only copy of it
    scenarios/<pack>/      the fixture tree the drill materialises
    graders/<pack>/cN.py   one grader per numbered criterion
    RESULTS.json           the append-only run ledger

A grader follows the same contract as the frozen benchmark criteria
scripts: `argv[1]` is the scratch directory, it prints one JSON object
`{"id", "pass", "reason"}` on stdout and exits 0 on pass, non-zero on
fail. Stdlib only. Exit 2 is reserved: it means the grader ran and
could not settle the criterion in this environment, which is recorded
as manual rather than as a failure of the work.
"""

from __future__ import annotations

import datetime as _dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from .repo import content_sha256  # line-ending normalised, see its docstring

MANIFEST_REL = "benchmark/drills/MANIFEST.json"
SCENARIOS_REL = "benchmark/drills/scenarios"
GRADERS_REL = "benchmark/drills/graders"
RESULTS_REL = "benchmark/drills/RESULTS.json"

PASS = "pass"
FAIL = "fail"
MANUAL = "manual"

# The criteria block is the first heading whose text names criteria.
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
_ITEM_RE = re.compile(r"^ {0,3}(\d{1,2})\.\s+(.*)$")
_GRADER_TIMEOUT_S = 600


class DrillError(Exception):
    """The drill cannot run at all: exit 2 territory."""


# ---------------------------------------------------------------- manifest


def load_manifest(root) -> dict:
    path = Path(root) / MANIFEST_REL
    if not path.is_file():
        raise DrillError("no drill manifest at %s" % MANIFEST_REL)
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise DrillError("drill manifest does not parse: %s" % exc)
    if not isinstance(doc.get("drills"), dict) or not doc["drills"]:
        raise DrillError("drill manifest lists no drills")
    return doc


def packs(root, manifest=None) -> list:
    manifest = manifest or load_manifest(root)
    return sorted(manifest["drills"])


# ------------------------------------------------------------------- spec


def _strip_front_matter(text: str) -> str:
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    if end == -1:
        return text
    return text[end + 4:]


def parse_spec(text: str) -> dict:
    """Pull the drill title and its numbered criteria out of a spec.

    Only the first criteria section is read, so a numbered list in the
    scoring or freeze notes is never mistaken for a criterion.
    """
    body = _strip_front_matter(text)
    lines = body.splitlines()

    title = ""
    for line in lines:
        m = _HEADING_RE.match(line)
        if m and m.group(1) == "#":
            title = m.group(2).strip()
            break

    start = None
    level = 0
    heading = None
    for i, line in enumerate(lines):
        m = _HEADING_RE.match(line)
        if m and "criteri" in m.group(2).lower():
            start = i + 1
            level = len(m.group(1))
            heading = m.group(2).strip()
            break
    if start is None:
        return {"drill": title, "criteria": [], "criteria_section": None}

    section = []
    for line in lines[start:]:
        m = _HEADING_RE.match(line)
        if m and len(m.group(1)) <= level:
            break
        section.append(line)

    criteria = []
    current = None
    for line in section:
        m = _ITEM_RE.match(line)
        if m:
            current = {"id": "c%s" % m.group(1), "n": int(m.group(1)),
                       "text": m.group(2).strip()}
            criteria.append(current)
            continue
        if current is not None and line.strip():
            current["text"] = (current["text"] + " " + line.strip()).strip()
        elif current is not None and not line.strip():
            current = None

    # Numbering must be 1..n in order, or the parse is not trustworthy.
    expected = list(range(1, len(criteria) + 1))
    if [c["n"] for c in criteria] != expected:
        raise DrillError(
            "criteria in the spec are not numbered 1..n in order: %s"
            % [c["n"] for c in criteria])
    return {"drill": title, "criteria": criteria, "criteria_section": heading}


def read_spec(root, pack, manifest=None) -> dict:
    """Read one frozen spec and check it against its recorded hash."""
    manifest = manifest or load_manifest(root)
    entry = manifest["drills"].get(pack)
    if entry is None:
        raise DrillError("no drill for pack %r; known packs: %s"
                         % (pack, ", ".join(sorted(manifest["drills"]))))
    path = Path(root) / entry["spec"]
    if not path.is_file():
        raise DrillError("frozen drill spec missing: %s" % entry["spec"])
    actual = content_sha256(path)
    recorded = entry.get("sha256")
    if recorded and actual != recorded:
        raise DrillError(
            "frozen drill spec changed since freeze: %s recorded %s, found %s"
            % (entry["spec"], recorded, actual))
    parsed = parse_spec(path.read_text(encoding="utf-8"))
    parsed.update({
        "pack": pack,
        "spec": entry["spec"],
        "sha256": actual,
        "frozen_before_authoring": entry.get("frozen_before_authoring"),
        "wave": entry.get("wave"),
    })
    return parsed


# ------------------------------------------------------------- scenario


def scenario_dir(root, pack) -> Path:
    return Path(root) / SCENARIOS_REL / pack


def grader_dir(root, pack) -> Path:
    return Path(root) / GRADERS_REL / pack


def grader_for(root, pack, n):
    path = grader_dir(root, pack) / ("c%d.py" % n)
    return path if path.is_file() else None


def _git(cwd, *args):
    return subprocess.run(["git", "-C", str(cwd), *args],
                          capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


_NOISE_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
               "node_modules", ".venv"}


def _ignore_build_artefacts(directory, names):
    """copytree filter: never carry bytecode into a drill scratch tree.

    A scenario directory accumulates __pycache__ from anyone who ran its
    code locally. Git never sees it, so the committed scenario looks
    clean, but copytree copies what is on disk and the baseline commit
    below then contains it. A verifier found parser.cpython-314.pyc in
    the git index of a freshly materialised coding scratch, dated before
    the session that materialised it, which makes the baseline commit
    machine-dependent and feeds stale bytecode to any criterion that
    diffs against it. The benchmark harness had the same defect.
    """
    return {n for n in names
            if n in _NOISE_DIRS or n.endswith((".pyc", ".pyo"))}


def materialise(root, pack, dest):
    """Copy the drill's frozen scenario into a scratch directory.

    Returns (scratch_path_or_None, reason). The scenario is committed as
    a baseline so criteria that diff against the starting tree have one.
    """
    src = scenario_dir(root, pack)
    if not src.is_dir():
        return None, ("no frozen scenario at %s/%s; the drill's fixture was "
                      "never built" % (SCENARIOS_REL, pack))
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    scratch = dest / pack
    if scratch.exists():
        shutil.rmtree(scratch)
    shutil.copytree(src, scratch, ignore=_ignore_build_artefacts)
    if shutil.which("git"):
        _git(scratch, "init", "-q")
        _git(scratch, "add", "-A")
        _git(scratch, "-c", "user.name=drill",
             "-c", "user.email=drill@pattertech.invalid",
             "commit", "-q", "-m", "drill baseline")
    return scratch, "materialised from %s/%s" % (SCENARIOS_REL, pack)


def run_grader(grader, scratch):
    """Run one grader against the scratch tree. Returns (verdict, reason).

    Exit 0 is a pass and any other code a fail, with one exception:
    exit 2 means the grader ran and could not settle the criterion in
    this environment, usually because the tool it drives is not
    installed. That is the manual verdict, not a fail. A grader has no
    way to distinguish "the work is wrong" from "I cannot look" through
    a boolean, and reporting the second as the first invents failures on
    any machine without the toolchain. Manual still blocks a green
    drill, so the safe direction is preserved.
    """
    try:
        proc = subprocess.run(
            [sys.executable, str(grader), str(scratch)],
            capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=_GRADER_TIMEOUT_S)
    except subprocess.TimeoutExpired:
        return FAIL, "grader timed out after %ds" % _GRADER_TIMEOUT_S
    reason = ""
    for line in reversed(proc.stdout.splitlines()):
        line = line.strip()
        if line.startswith("{"):
            try:
                doc = json.loads(line)
            except ValueError:
                continue
            reason = str(doc.get("reason", ""))
            break
    if not reason:
        reason = (proc.stderr.strip().splitlines() or [""])[-1]
    if proc.returncode == 0:
        return PASS, reason or "grader exited 0"
    if proc.returncode == 2:
        return MANUAL, reason or "grader could not settle this criterion here"
    return FAIL, reason or "grader exited %d" % proc.returncode


# ------------------------------------------------------------------- run


def run_drill(root, pack, scratch_root=None, manifest=None, attempt=None):
    """Run one drill and return its `{pack, drill, pass, criteria}` row.

    With `attempt` the graders run against the tree a cold agent
    delivered. Without it they run against a freshly materialised
    scenario, which grades the untouched fixture: useful to prove a
    drill discriminates, never a substitute for the run itself. The
    cold-agent session is the harness's job, not this command's.
    """
    spec = read_spec(root, pack, manifest=manifest)
    owned_scratch = scratch_root is None and attempt is None
    if owned_scratch:
        scratch_root = tempfile.mkdtemp(prefix="eos-drill-")
    try:
        if attempt is not None:
            scratch = Path(attempt)
            if not scratch.is_dir():
                raise DrillError("attempt directory not found: %s" % attempt)
            why = "grading the delivered attempt at %s" % scratch
        else:
            scratch, why = materialise(root, pack, scratch_root)
        rows = []
        for crit in spec["criteria"]:
            grader = grader_for(root, pack, crit["n"])
            if grader is None:
                rows.append({
                    "id": crit["id"], "verdict": MANUAL,
                    "reason": "no grader at %s/%s/c%d.py; the criterion is "
                              "prose a human must judge"
                              % (GRADERS_REL, pack, crit["n"]),
                })
                continue
            if scratch is None:
                rows.append({
                    "id": crit["id"], "verdict": MANUAL,
                    "reason": "grader present but %s" % why,
                })
                continue
            verdict, reason = run_grader(grader, scratch)
            rows.append({"id": crit["id"], "verdict": verdict,
                         "reason": reason})
    finally:
        if owned_scratch and scratch_root:
            shutil.rmtree(scratch_root, ignore_errors=True)

    failed = [r["id"] for r in rows if r["verdict"] == FAIL]
    manual = [r["id"] for r in rows if r["verdict"] == MANUAL]
    if not rows:
        verdict = None
        reason = "the frozen spec declares no numbered criteria"
    elif failed:
        verdict = False
        reason = "%d of %d criteria failed: %s" % (
            len(failed), len(rows), ", ".join(failed))
    elif manual:
        verdict = None
        cause = ("no scenario and no graders" if scratch is None
                 else "no grader for every criterion")
        reason = ("%d of %d criteria are manual and were not evaluated, so "
                  "the drill has no verdict (%s)"
                  % (len(manual), len(rows), cause))
    else:
        verdict = True
        reason = "all %d criteria evaluated and passed" % len(rows)

    return {
        "pack": pack,
        "drill": spec["drill"] or pack,
        "pass": verdict,
        "criteria": rows,
        "reason": reason,
        "counts": {"total": len(rows),
                   "pass": len(rows) - len(failed) - len(manual),
                   "fail": len(failed), "manual": len(manual)},
        "graded": "attempt" if attempt is not None else "scenario-baseline",
        "spec": spec["spec"],
        "sha256": spec["sha256"],
        "frozen_before_authoring": spec["frozen_before_authoring"],
    }


def run_all(root, scratch_root=None, manifest=None):
    manifest = manifest or load_manifest(root)
    return [run_drill(root, pack, scratch_root=scratch_root,
                      manifest=manifest)
            for pack in packs(root, manifest)]


def summarise(results) -> dict:
    return {
        "drills": len(results),
        "passed": sum(1 for r in results if r["pass"] is True),
        "failed": sum(1 for r in results if r["pass"] is False),
        "unresolved": sum(1 for r in results if r["pass"] is None),
        "frozen_before_authoring": sum(
            1 for r in results if r.get("frozen_before_authoring") is True),
    }


def exit_code(results) -> int:
    """0 only when every requested drill passed outright."""
    if not results:
        return 2
    if any(r["pass"] is False for r in results):
        return 1
    if any(r["pass"] is not True for r in results):
        return 1
    return 0


# ------------------------------------------------------------------ list


def list_drills(root, manifest=None) -> list:
    manifest = manifest or load_manifest(root)
    rows = []
    for pack in packs(root, manifest):
        entry = manifest["drills"][pack]
        path = Path(root) / entry["spec"]
        row = {
            "pack": pack,
            "spec": entry["spec"],
            "sha256": entry.get("sha256"),
            "frozen_before_authoring": entry.get("frozen_before_authoring"),
            "wave": entry.get("wave"),
        }
        if not path.is_file():
            row.update({"spec_present": False, "hash_ok": False,
                        "criteria": None, "graders": 0, "scenario": False,
                        "runnable": False})
            rows.append(row)
            continue
        actual = content_sha256(path)
        row["spec_present"] = True
        row["hash_ok"] = (actual == entry.get("sha256"))
        try:
            parsed = parse_spec(path.read_text(encoding="utf-8"))
            count = len(parsed["criteria"])
        except DrillError:
            count = None
        row["drill"] = (parsed["drill"] if count is not None else None)
        row["criteria"] = count
        row["graders"] = sum(
            1 for n in range(1, (count or 0) + 1)
            if grader_for(root, pack, n) is not None)
        row["scenario"] = scenario_dir(root, pack).is_dir()
        row["runnable"] = bool(
            row["hash_ok"] and row["scenario"] and count
            and row["graders"] == count)
        rows.append(row)
    return rows


# --------------------------------------------------------------- results


def append_results(root, results, date=None):
    """Append one entry per run to the append-only RESULTS ledger."""
    path = Path(root) / RESULTS_REL
    if path.is_file():
        doc = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(doc.get("runs"), list):
            raise DrillError("RESULTS.json is malformed: no runs list")
    else:
        doc = {
            "version": 1,
            "note": ("Append-only ledger of pack acceptance drill runs. One "
                     "entry per drill per run. Rows are never rewritten or "
                     "removed. A pass of null means the drill had no verdict, "
                     "which is not a pass."),
            "runs": [],
        }
    stamp = date or _dt.date.today().isoformat()
    before = len(doc["runs"])
    for row in results:
        doc["runs"].append({
            "date": stamp,
            "pack": row["pack"],
            "drill": row["drill"],
            "pass": row["pass"],
            "reason": row["reason"],
            "counts": row["counts"],
            "graded": row.get("graded"),
            "criteria": row["criteria"],
            "spec": row["spec"],
            "sha256": row["sha256"],
            "frozen_before_authoring": row["frozen_before_authoring"],
        })
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8",
                   newline="\n")
    os.replace(tmp, path)
    return len(doc["runs"]) - before
