"""Task record and claims operations, plus the derived view generator.

Implements the assigned-claims model from the plan (section 7.2) and
CLI_CONTRACTS.md: lanes receive claims and never acquire or mutate
them; a session not named in the committed unexpired set is refused;
expired claims surface their liveness identity and are never taken
over automatically. All writes are atomic temp-then-rename.

render_views regenerates the derived views org/TASKS.md and
org/STATE.md from the canonical records (org/tasks/*.json,
org/claims.json, org/cadence.json) and read-only git facts. Derived
views are integrator-only: no lane claim covers them and they are
never hand-edited. Output is deterministic: stable ordering, no
timestamps beyond what the records already carry.

Schema validation degrades: jsonschema imports lazily inside the
validating function, and when missing the validation returns a finding
of severity error naming the install command (exit 2 semantics are the
CLI's job).
"""

from __future__ import annotations

import json
import os
import re
import tempfile
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

try:  # The lane T1 findings module is canonical once present.
    from tools.eos.findings import Finding, Findings
except ImportError:  # Structurally identical minimal fallback.
    from dataclasses import dataclass, field

    @dataclass
    class Finding:
        check_id: str
        severity: str  # 'error' | 'warn'
        path: str
        message: str

    @dataclass
    class Findings:
        items: list = field(default_factory=list)

        def add(self, finding):
            self.items.append(finding)

        @property
        def errors(self):
            return [f for f in self.items if f.severity == "error"]

        @property
        def warns(self):
            return [f for f in self.items if f.severity == "warn"]

        def to_json(self):
            return json.dumps([vars(f) for f in self.items], indent=2)

        def to_text(self):
            return "\n".join(
                "%s %s %s: %s" % (f.severity.upper(), f.check_id, f.path, f.message)
                for f in self.items)

        def exit_code(self):
            return 1 if self.errors else 0


_TASK_ID_RE = re.compile(r"^T-(\d{4})$")
_JSONSCHEMA_INSTALL = (
    "jsonschema is required for schema validation: install with "
    "python -m pip install --require-hashes -r tools/requirements.txt "
    "(or python -m pip install jsonschema)"
)

# Derived files belong to the integrator permanently; no lane claim
# covers them.
DERIVED_FILES = (
    "index.md",
    "doctrine/wargame_index.md",
    "org/tasks.md",
    "org/state.md",
)


def _atomic_write(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=str(path.parent),
            prefix=path.name + ".", suffix=".tmp", delete=False) as tmp:
        tmp.write(text)
        tmp_name = tmp.name
    os.replace(tmp_name, str(path))
    return path


def next_task_id(root):
    """Return the next free T-#### id under org/tasks/."""
    tasks_dir = Path(root) / "org" / "tasks"
    highest = 0
    if tasks_dir.is_dir():
        for entry in tasks_dir.iterdir():
            m = _TASK_ID_RE.match(entry.stem)
            if m:
                highest = max(highest, int(m.group(1)))
    return "T-%04d" % (highest + 1)


def validate_task_record(root, record):
    """Validate a record against task-record.schema.json.

    Returns Findings. jsonschema is imported lazily; when missing the
    result carries one error finding naming the install command.
    """
    findings = Findings()
    schema_path = Path(root) / "kernel" / "schemas" / "task-record.schema.json"
    try:
        import jsonschema
    except ImportError:
        findings.add(Finding("V000", "error", str(schema_path), _JSONSCHEMA_INSTALL))
        return findings
    if not schema_path.is_file():
        findings.add(Finding("V001", "error", str(schema_path),
                             "task-record schema not found"))
        return findings
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    for err in sorted(validator.iter_errors(record), key=str):
        findings.add(Finding("V002", "error",
                             "/".join(str(p) for p in err.absolute_path) or "(root)",
                             err.message))
    return findings


def create_task(root, record):
    """Validate and write org/tasks/<id>.json atomically; return path.

    Raises ValueError when validation finds errors (missing jsonschema
    is an error finding too; the CLI maps that case to exit 2).
    """
    root = Path(root)
    task_id = record.get("id", "")
    if not _TASK_ID_RE.match(task_id):
        raise ValueError("task id must match T-####: %r" % (task_id,))
    findings = validate_task_record(root, record)
    if findings.errors:
        raise ValueError("task record invalid:\n" + findings.to_text())
    path = root / "org" / "tasks" / ("%s.json" % task_id)
    return _atomic_write(path, json.dumps(record, indent=2) + "\n")


def update_task(root, task_id, patch):
    """Shallow-merge patch into an existing record; validate; rewrite."""
    root = Path(root)
    path = root / "org" / "tasks" / ("%s.json" % task_id)
    if not path.is_file():
        raise FileNotFoundError("no task record at %s" % path)
    record = json.loads(path.read_text(encoding="utf-8"))
    for key, value in patch.items():
        if key == "timestamps" and isinstance(value, dict):
            record.setdefault("timestamps", {}).update(value)
        else:
            record[key] = value
    findings = validate_task_record(root, record)
    if findings.errors:
        raise ValueError("patched record invalid:\n" + findings.to_text())
    return _atomic_write(path, json.dumps(record, indent=2) + "\n")


def _canon(path):
    return unicodedata.normalize("NFC", str(path).replace("\\", "/")).casefold()


def _covered(diff_path, claims):
    """Exact match, or prefix match when the claim ends with a slash."""
    p = _canon(diff_path)
    for claim in claims:
        c = _canon(claim)
        if c.endswith("/"):
            if p.startswith(c):
                return True
        elif p == c:
            return True
    return False


def _parse_dt(value):
    value = value.strip()
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def verify_claims(root, claims_doc, lane_id, diff_paths, *, now=None):
    """Verify a lane's actual diff against its assigned claims.

    Assigned-claims model: refusal when the actor is not named in the
    committed set; case-folded posix compare; a trailing slash claims
    the directory prefix; renames and deletes must supply both paths in
    diff_paths; new files must fall under a claim; derived files are
    integrator-only. Expiry surfaces the liveness identity and never
    authorises takeover: recovery needs the operator or confirmed-dead
    evidence.
    """
    findings = Findings()
    now = now or datetime.now(timezone.utc)

    lanes = (claims_doc or {}).get("lanes", [])
    lane = next((l for l in lanes if l.get("lane_id") == lane_id), None)
    if lane is None:
        findings.add(Finding(
            "C001", "error", "org/claims.json",
            "refused: session %r is not named in the committed claim set; "
            "unscheduled work stays quarantined on its branch for the "
            "integrator to adopt or discard" % (lane_id,)))
        return findings

    expires = lane.get("expires")
    if expires:
        try:
            expired = _parse_dt(expires) <= now
        except ValueError:
            expired = False
            findings.add(Finding("C005", "error", "org/claims.json",
                                 "unparseable expires timestamp: %r" % (expires,)))
        if expired:
            liveness = ", ".join(
                "%s=%s" % (k, lane[k])
                for k in ("session_id", "host", "pid", "harness_task_id")
                if lane.get(k) is not None)
            findings.add(Finding(
                "C002", "error", "org/claims.json",
                "claim for lane %s expired at %s; liveness identity: %s; "
                "recovery requires the operator or confirmed-dead evidence; "
                "a timestamp alone never authorises takeover" % (
                    lane_id, expires, liveness or "none recorded")))

    claims = lane.get("path_claims", [])
    integrator = lane_id == "integrator"
    for diff_path in diff_paths:
        canon = _canon(diff_path)
        if canon in DERIVED_FILES and not integrator:
            findings.add(Finding(
                "C004", "error", diff_path,
                "derived file: regenerated only by the integrator, never "
                "claimed or edited by a lane"))
            continue
        if not _covered(diff_path, claims):
            findings.add(Finding(
                "C003", "error", diff_path,
                "outside the claims assigned to lane %s" % lane_id))
    return findings


# --- derived views ------------------------------------------------------

# Task statuses that wait on the operator: blocked outright, or parked
# in review awaiting an approval verdict (the record enum's
# awaiting-approval state).
OPERATOR_FLAG_STATUSES = ("blocked", "in-review")

_VIEW_REGEN_NOTE = (
    "Derived view. Regenerated by python -m tools.eos task views\n"
    "(integrator only); never hand-edited."
)


def _read_json(path):
    """(document, problem) without raising; problem is None when clean."""
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        return None, "unreadable: %s" % (exc,)
    try:
        return json.loads(text), None
    except ValueError as exc:
        return None, "malformed JSON: %s" % (exc,)


def _tasks_view(records):
    lines = [
        "---",
        "summary: Derived task table, one row per record under org/tasks/",
        "type: org",
        "tags: [eos]",
        "derived: true",
        "---",
        "",
        "# TASKS",
        "",
        _VIEW_REGEN_NOTE,
        "The records under org/tasks/ are canonical.",
        "",
        "| id | mode | tier | status | owner |",
        "| --- | --- | --- | --- | --- |",
    ]
    for rec in records:
        lines.append("| %s | %s | %s | %s | %s |" % (
            rec.get("id", "?"), rec.get("mode", "?"), rec.get("tier_ruled", "?"),
            rec.get("status", "?"), rec.get("owner_session", "?")))
    if not records:
        lines.append("| (no task records yet) | | | | |")
    return "\n".join(lines) + "\n"


def _state_view(records, claims_doc, cadence, branch, head):
    lines = [
        "---",
        "summary: Derived state view of claims, operator flags, cadence and machine facts",
        "type: org",
        "tags: [eos]",
        "derived: true",
        "---",
        "",
        "# STATE",
        "",
        _VIEW_REGEN_NOTE,
        "",
        "## Active claims",
        "",
    ]
    lanes = (claims_doc or {}).get("lanes", [])
    if lanes:
        lines.append("| lane | task | session | expires | claims |")
        lines.append("| --- | --- | --- | --- | --- |")
        for lane in lanes:
            lines.append("| %s | %s | %s | %s | %s |" % (
                lane.get("lane_id", "?"), lane.get("task_id", "?"),
                lane.get("session_id", "?"), lane.get("expires", "?"),
                ", ".join(lane.get("path_claims", []))))
    else:
        lines.append("No lanes hold claims.")
    lines += ["", "## Operator flags", ""]
    flagged = [r for r in records if r.get("status") in OPERATOR_FLAG_STATUSES]
    if flagged:
        for rec in flagged:
            lines.append("- %s %s: %s" % (
                rec.get("id", "?"), rec.get("status", "?"),
                rec.get("intent", "(no intent recorded)")))
    else:
        lines.append("Nothing waits on the operator.")
    lines += ["", "## Cadence", ""]
    rows = [r for r in cadence if isinstance(r, dict)] \
        if isinstance(cadence, list) else []
    if rows:
        lines.append("| cadence | frequency | next due |")
        lines.append("| --- | --- | --- |")
        for row in rows:
            lines.append("| %s | %s | %s |" % (
                row.get("id", "?"), row.get("frequency", "?"),
                row.get("next_due", "?")))
    else:
        lines.append("No cadence rows recorded.")
    lines += ["", "## Machine facts", ""]
    facts = []
    if branch:
        facts.append("branch: %s" % branch)
    if head:
        facts.append("commit: %s" % head)
    if facts:
        lines += ["```facts"] + facts + ["```"]
    else:
        lines.append("Git facts unavailable in this working copy.")
    return "\n".join(lines) + "\n"


def render_views(root):
    """Regenerate org/TASKS.md and org/STATE.md; return a findings list.

    Integrator-only, like every derived file in DERIVED_FILES. Inputs:
    the task records under org/tasks/, org/claims.json, org/cadence.json
    and read-only git facts (current branch, head commit). TASKS.md
    carries one table row per record (id, mode, tier, status, owner).
    STATE.md carries the assigned claim set, the operator flags (task
    records with a status in OPERATOR_FLAG_STATUSES), the cadence
    next-due rows and a machine-facts block the S007 check can verify.
    Regeneration is byte-stable for unchanged inputs: records sort by
    id, claim and cadence rows keep their committed order, and nothing
    is stamped with the time of rendering. A malformed input file is
    reported as an error finding and skipped, never guessed at.
    """
    root = Path(root)
    findings = []

    records = []
    tasks_dir = root / "org" / "tasks"
    if tasks_dir.is_dir():
        for path in sorted(tasks_dir.glob("T-*.json")):
            doc, problem = _read_json(path)
            if problem:
                findings.append(Finding("V003", "error", "org/tasks/%s" % path.name, problem))
            elif isinstance(doc, dict):
                records.append(doc)
    records.sort(key=lambda r: str(r.get("id", "")))

    claims_doc = None
    if (root / "org" / "claims.json").is_file():
        claims_doc, problem = _read_json(root / "org" / "claims.json")
        if problem:
            findings.append(Finding("V003", "error", "org/claims.json", problem))
            claims_doc = None

    cadence = None
    if (root / "org" / "cadence.json").is_file():
        cadence, problem = _read_json(root / "org" / "cadence.json")
        if problem:
            findings.append(Finding("V003", "error", "org/cadence.json", problem))
            cadence = None

    branch = head = None
    try:
        from tools.eos import gitfacts
    except ImportError:
        gitfacts = None
    if gitfacts is not None:
        branch = gitfacts.current_branch(root)
        head = gitfacts.rev_parse(root, "HEAD")

    _atomic_write(root / "org" / "TASKS.md", _tasks_view(records))
    _atomic_write(root / "org" / "STATE.md",
                  _state_view(records, claims_doc, cadence, branch, head))
    return findings
