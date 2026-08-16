"""v1-to-v2 seed migration: read-only planning, fixture-only apply.

plan(seed_root) analyses a v1 seed without writing anything: it reads
the lock-book header for scale and pin, inventories the seed against
the v1 scale matrix (kernel/SCALE_MATRIX.md, embedded below as data)
and proposes a route. apply(seed_root, plan) performs the v1-to-v2
transforms, defaults to dry_run, and refuses to run against a git
repository so it is only ever exercised on fixture copies.
"""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

from tools.eos import taskops
from tools.eos.frontmatter import parse as parse_front_matter

# The v1 scale matrix, from kernel/SCALE_MATRIX.md (the law of what a
# compiled seed contains). Path to the scales that require it.
V1_MATRIX = {
    "AGENTS.md": ("S", "M", "L"),
    "CLAUDE.md": ("S", "M", "L"),
    "OPERATORS_GUIDE.md": ("S", "M", "L"),
    "docs/VENTURE_BRIEF.md": ("S", "M", "L"),
    "docs/LOCKBOOK.md": ("S", "M", "L"),
    "docs/EOS_FEEDBACK.md": ("S", "M", "L"),
    "docs/COMPILE_REPORT.md": ("S", "M", "L"),
    "docs/WORKLOG.md": ("S",),
    "org/CONSTITUTION.md": ("M", "L"),
    "org/START.md": ("M", "L"),
    "org/OPERATING_MODEL.md": ("M", "L"),
    "org/STATE.md": ("M", "L"),
    "org/TEMPLATES.md": ("M", "L"),
    "org/CADENCE.md": ("M", "L"),
    "org/QUESTIONS.md": ("M", "L"),
    "org/QUEUE.md": ("M",),
    "org/roles/PLAN.md": ("M", "L"),
    "org/roles/WORK.md": ("M", "L"),
    "org/roles/VERIFY.md": ("M", "L"),
    "org/playbooks/CATALOGUE.md": ("L",),
    "org/work/NEXT.md": ("L",),
}

_QUEUE_ROW_RE = re.compile(r"^###\s+(WO-\d{4})\s+·\s+(.+)$")
_LEGACY_RULING_RE = re.compile(
    r"^\s*-\s+((?:GD|WG)-[A-Z0-9]+-\d{3})\s*·\s*(.*?)\s*·\s*"
    r"(argued|inherited)\s*·\s*(.*?)\s*$"
)
_ROLE_NOTE = (
    "# %s\n\n"
    "This role charter is superseded in EOS v2. Sessions are routed by\n"
    "the task router under kernel/POLICY_SPEC.md: the tier ruled from\n"
    "declared facts and derived signals decides the mode, artefacts and\n"
    "verification, not a standing role file. The original charter is\n"
    "preserved in git history.\n"
)


def _venture_name(seed_root, lockbook_text):
    for line in lockbook_text.splitlines():
        m = re.match(r"^#\s+(.+?)\s+lock-book\s*$", line.strip())
        if m:
            return m.group(1)
    return Path(seed_root).name


def _legacy_rulings(lockbook_text):
    """Parsed legacy header rows, retaining each row byte-for-byte as text."""
    rows = []
    lines = lockbook_text.splitlines()
    if not lines or lines[0].strip() != "---":
        return rows
    end = next((i for i, line in enumerate(lines[1:60], 1)
                if line.strip() == "---"), None)
    if end is None:
        return rows
    for line in lines[1:end]:
        match = _LEGACY_RULING_RE.match(line)
        if match:
            rows.append({
                "wargame": match.group(1),
                "decision": match.group(2),
                "execution": match.group(3),
                "note": match.group(4),
                "legacy_text": line,
            })
    return rows


def _ruling_code(venture):
    code = re.sub(r"[^A-Za-z0-9]", "", str(venture)).upper()
    return code or "VENTURE"


def _structured_rulings(venture, eos_commit, rows, today):
    code = _ruling_code(venture)
    rulings = []
    selection = []
    for number, row in enumerate(rows, 1):
        ruling_id = "RUL-%s-%03d" % (code, number)
        reason = row["note"] or "Migrated from the legacy lock-book row."
        rulings.append({
            "id": ruling_id,
            "wargame": row["wargame"],
            "doctrines": [],
            "decision": row["decision"],
            "execution": ("argued" if row["execution"] == "argued"
                          else "legacy-inherited"),
            "reason": reason,
            "decided": today,
            "review": "on-change-of:eos-pin",
            "departures": [],
            "binding_scope_changes": [],
            "legacy_text": row["legacy_text"],
        })
        selection.append({
            "wargame": row["wargame"],
            "disposition": "selected",
            "reason": reason,
            "ruling": ruling_id,
            "facts": [],
        })
    return {
        "version": 1,
        "venture": venture,
        "eos_commit": eos_commit,
        "selection_log": selection,
        "rulings": rulings,
        "legacy_migration": {
            "source": "docs/LOCKBOOK.md front-matter rulings",
            "migrated_at": "%sT00:00:00Z" % today,
            "unparsed_rows": [],
        },
    }


def _replace_legacy_rulings_header(text):
    """Replace the delimiter list with one pointer to structured JSON."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return text
    end = next((i for i, line in enumerate(lines[1:60], 1)
                if line.strip() == "---"), None)
    if end is None:
        return text
    header = lines[1:end]
    out = []
    skipping = False
    for line in header:
        if line.strip() == "rulings:":
            skipping = True
            continue
        if skipping and re.match(r"^\s+-\s+", line):
            continue
        skipping = False
        out.append(line)
    if not any(line.startswith("rulings_record:") for line in out):
        out.append("rulings_record: docs/RULINGS.json")
    return "\n".join([lines[0], *out, lines[end], *lines[end + 1:]]) + "\n"


def plan(seed_root):
    """Read-only analysis of a v1 seed; returns a migration-state dict."""
    seed_root = Path(seed_root)
    lockbook_path = seed_root / "docs" / "LOCKBOOK.md"

    if not lockbook_path.is_file():
        return {
            "version": 1,
            "venture": seed_root.name,
            "pin_current": "none",
            "route": "fresh-inception",
            "steps": [{"id": "session-0", "status": "pending",
                       "desc": "no lock-book found: run a fresh v2 Session 0"}],
            "provenance_preserved": [],
            "report_path": "org/reports/migration-%s.md" % seed_root.name,
        }

    lockbook_text = lockbook_path.read_text(encoding="utf-8")
    fm = parse_front_matter(lockbook_text).data
    scale = fm.get("scale", "S")
    version = fm.get("eos_version", "unknown")
    commit = fm.get("eos_commit", "unknown")
    pin = "%s@%s" % (version, commit)
    venture = _venture_name(seed_root, lockbook_text)

    missing = [path for path, scales in V1_MATRIX.items()
               if scale in scales and not (seed_root / path).is_file()]
    extra_note = "inventory complete" if not missing else (
        "missing against the v1 matrix: " + ", ".join(missing))

    # Route heuristic per the plan: a pin predating 1.0.0 predates the
    # kernel freeze, so the seed recompiles from its rulings; a 1.x pin
    # upgrades in place; no lock-book means fresh inception. Pins are written by hand and appear as 1.0.0, v1.0.0 or pre-1.0.0,
    # so read the first version-like number rather than anchoring at the
    # string start; an unreadable pin stays on the conservative route.
    stated = str(version).strip()
    prerelease = stated.lower().startswith("pre-")
    m = re.search(r"(\d+)\.(\d+)", stated)
    if m is None:
        route = "recompile"
    elif prerelease or int(m.group(1)) < 1:
        route = "recompile"
    else:
        route = "apply"

    steps = [
        {"id": "pin-policy", "status": "pending",
         "desc": "lock-book header gains the v2 policy pin"},
    ]
    if _legacy_rulings(lockbook_text) and not (
            seed_root / "docs" / "RULINGS.json").is_file():
        steps.append({"id": "structured-rulings", "status": "pending",
                      "desc": "losslessly convert legacy lock-book rows to "
                              "docs/RULINGS.json"})
    if any((seed_root / "org" / "roles" / n).is_file()
           for n in ("PLAN.md", "WORK.md", "VERIFY.md")):
        steps.append({"id": "roles-to-tier-note", "status": "pending",
                      "desc": "role charters swap for the tier policy note"})
    # M-shape ventures carry a queue file; L-shape ventures carry per-file
    # work orders under org/work/. Both convert to task records, and the
    # L shape is the larger job, so it must not go unreported.
    work_items = seed_root / "org" / "work" / "items"
    if work_items.is_dir():
        n = len(list(work_items.glob("*.md")))
        steps.append({"id": "work-orders-to-tasks", "status": "pending",
                      "desc": "convert %d work orders under org/work/items/ "
                              "to task records" % n})
    if (seed_root / "org" / "QUEUE.md").is_file():
        steps.append({"id": "queue-to-tasks", "status": "pending",
                      "desc": "queue rows become org/tasks/T-####.json records"})
    if (seed_root / "docs" / "WORKLOG.md").is_file():
        steps.append({"id": "worklog-note", "status": "pending",
                      "desc": "WORKLOG gains the migration note"})
    steps.append({"id": "inventory", "status": "pending", "desc": extra_note})

    return {
        "version": 1,
        "venture": venture,
        "pin_current": pin,
        "route": route,
        "steps": steps,
        "provenance_preserved": [
            "docs/LOCKBOOK.md rulings",
            "org/decisions/",
            "org/logs/",
        ],
        "report_path": "org/reports/migration-%s.md" % venture,
    }


def _queue_rows(queue_text):
    rows = []
    for line in queue_text.splitlines():
        m = _QUEUE_ROW_RE.match(line.strip())
        if m:
            rows.append((m.group(1), m.group(2).strip()))
    return rows


def apply(seed_root, plan_doc, *, dry_run=True, today=None):
    """Apply the v1-to-v2 transforms to a fixture seed.

    Refuses a git repository outright: this build only ever transforms
    tmp copies of fixture seeds. dry_run (the default) reports what
    would change and writes nothing. org/logs are never touched.
    """
    seed_root = Path(seed_root)
    if (seed_root / ".git").exists():
        raise ValueError(
            "refusing to apply: %s is a git repository; migrate apply runs "
            "on fixture seed copies only in this build" % seed_root)
    today = today or date.today().isoformat()
    changes = []
    result = json.loads(json.dumps(plan_doc))  # deep copy, stays JSON-safe

    def mark(step_id, status):
        for step in result["steps"]:
            if step["id"] == step_id:
                step["status"] = status

    # 1. Lock-book header gains the policy pin and structured Rulings pointer.
    lockbook = seed_root / "docs" / "LOCKBOOK.md"
    if lockbook.is_file():
        text = lockbook.read_text(encoding="utf-8")
        changed_text = text
        if "policy_pin:" not in text:
            changes.append("docs/LOCKBOOK.md: add policy_pin to the header")
            lines = changed_text.splitlines()
            for i in range(1, min(len(lines), 60)):
                if lines[i].strip() == "---":
                    lines.insert(i, "policy_pin: kernel/POLICY_SPEC.md@v2")
                    break
            changed_text = "\n".join(lines) + "\n"

        legacy_rows = _legacy_rulings(changed_text)
        rulings_path = seed_root / "docs" / "RULINGS.json"
        if legacy_rows and not rulings_path.is_file():
            changes.append(
                "docs/LOCKBOOK.md rulings -> docs/RULINGS.json: %d rows"
                % len(legacy_rows))
            document = _structured_rulings(
                result["venture"],
                parse_front_matter(changed_text).data.get("eos_commit", "unknown"),
                legacy_rows,
                today,
            )
            changed_text = _replace_legacy_rulings_header(changed_text)
            if not dry_run:
                rulings_path.write_text(
                    json.dumps(document, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8", newline="\n")
                mark("structured-rulings", "done")
        if not dry_run:
            if changed_text != text:
                lockbook.write_text(changed_text, encoding="utf-8", newline="\n")
            mark("pin-policy", "done")

    # 2. Role charters swap for the tier policy note.
    roles_dir = seed_root / "org" / "roles"
    if roles_dir.is_dir():
        for role_file in sorted(roles_dir.glob("*.md")):
            changes.append("org/roles/%s: swap for the tier policy note" % role_file.name)
            if not dry_run:
                role_file.write_text(_ROLE_NOTE % role_file.stem,
                                     encoding="utf-8", newline="\n")
        if not dry_run:
            mark("roles-to-tier-note", "done")

    # 3. Queue rows become task records.
    queue = seed_root / "org" / "QUEUE.md"
    if queue.is_file():
        rows = _queue_rows(queue.read_text(encoding="utf-8"))
        for wo_id, title in rows:
            changes.append("org/QUEUE.md %s -> task record: %s" % (wo_id, title))
        if not dry_run:
            for wo_id, title in rows:
                task_id = taskops.next_task_id(seed_root)
                record = {
                    "id": task_id,
                    "intent": "%s (migrated from %s)" % (title, wo_id),
                    "declared": {"capabilities": [], "side_effects": []},
                    "mode": "standard",
                    "tier_proposed": "R1",
                    "tier_ruled": "R1",
                    "reasons": [],
                    "status": "proposed",
                    "owner_session": "migrate-apply",
                    "claims": [],
                    "timestamps": {
                        "opened": "%sT00:00" % today,
                        "updated": "%sT00:00" % today,
                    },
                }
                taskops.create_task(seed_root, record)
            mark("queue-to-tasks", "done")

    # 4. WORKLOG gains the migration note.
    worklog = seed_root / "docs" / "WORKLOG.md"
    if worklog.is_file():
        changes.append("docs/WORKLOG.md: append the migration note")
        if not dry_run:
            with worklog.open("a", encoding="utf-8") as fh:
                fh.write("\n## %s migrated to EOS v2\n\n"
                         "Queue rows became task records; role charters "
                         "swapped for the tier policy note; rulings, "
                         "decisions and logs carried verbatim.\n" % today)
            mark("worklog-note", "done")

    if not dry_run:
        mark("inventory", "done")

    # The updated migration-state stays schema-valid on its own under
    # the 'state' key; dry-run metadata rides alongside, never inside.
    return {"state": result, "dry_run": dry_run, "changes": changes}
