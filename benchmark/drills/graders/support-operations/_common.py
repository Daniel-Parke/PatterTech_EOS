"""Shared helpers for the support-operations drill graders. Stdlib only.

Not a grader. The runner looks for `c<N>.py` by name, so this file is
never mistaken for a criterion.

Exit codes follow the grader contract: 0 pass, 1 fail, 2 the criterion
cannot be settled in this environment. The third code carries real
weight here, for two reasons worth stating once rather than in every
grader.

**The checker that belongs to another repository.** Criterion 12 names
`python tools/eos_check.py --repo`. That is the EOS's own repository
check. The tree this drill grades is an ordinary support inbox, on
purpose, because a fixture carrying EOS metadata tells a cold agent it
is being tested. There is no such script in it and nothing the agent
was asked for would put one there, so that half of the criterion is
left unsettled rather than failed.

**Negative criteria over an empty tree.** Criteria 10 and 12 say what
must *not* appear under `out/`. On a tree where nothing was produced
both are vacuously true, and a fatal criterion that passes when no work
was done is measuring nothing. So when `out/` carries none of the
artefacts the drill asks for, those graders return unsettled: never a
pass, and never a fail invented against a tree nobody wrote to.

**Fixture facts.** The graders hard-code four things about the seeded
inbox, because they are properties of the frozen fixture rather than
judgements about the delivery: the run clock, which items carry no
reproduction detail, which are the billing complaints, and which items
report the same outage. They are listed below and each one is visible
in `benchmark/drills/scenarios/support-operations/`.

**Key matching.** Attempts spell keys differently (`next_action_due`,
`nextActionDue`, `next-action-due`). Keys are compared with punctuation
and case removed, so the spelling of a field never decides a criterion.
"""

import csv
import datetime as _dt
import json
import re
import sys
from pathlib import Path

PASS, FAIL, UNSETTLED = 0, 1, 2

# ------------------------------------------------------- fixture facts

ITEM_COUNT = 40
NO_REPRO_ITEMS = (9, 22, 31)          # inbox items with no reproduction
BILLING_ITEMS = (12, 35)              # the two billing complaints
OUTAGE_ITEM = 17                      # the outage itself
OUTAGE_DUPLICATES = (19, 21, 24, 28)  # four independent reports of it
OUTAGE_CLUSTER = (OUTAGE_ITEM,) + OUTAGE_DUPLICATES

# The fixed clock: `export-manifest.json` in the scenario. Read from the
# tree when it survives, so an attempt that keeps the fixture is graded
# against the fixture's own clock, and fall back to this constant when
# the manifest is gone.
RUN_CLOCK = _dt.datetime(2026, 8, 7, 17, 0, tzinfo=_dt.timezone.utc)

ARTEFACTS = ("severity_policy.md", "triage.json", "incident-0001.json",
             "comms.log", "synthesis.json")

SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules",
             ".pytest_cache", ".ruff_cache", ".mypy_cache"}
IGNORED_NAMES = {".gitkeep", ".gitignore", ".keep"}


# ------------------------------------------------------------ plumbing


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


def walk(root):
    root = Path(root)
    if not root.is_dir():
        return
    for path in sorted(root.rglob("*")):
        if SKIP_DIRS.intersection(path.parts):
            continue
        if path.is_file():
            yield path


def rel(root, path):
    try:
        return Path(path).relative_to(root).as_posix()
    except ValueError:
        return str(path)


# ------------------------------------------------------------ the tree


def out_dir(scratch):
    return Path(scratch) / "out"


def produced_files(scratch):
    """Files under out/ that are a delivery rather than fixture scaffolding."""
    return [p for p in walk(out_dir(scratch))
            if p.name not in IGNORED_NAMES and p.stat().st_size > 0]


def find_artefact(scratch, name):
    """Locate one named deliverable, preferring out/.

    The drill says out/. An attempt that put the file somewhere else has
    still written it, so it is found and the path is reported, which
    keeps the verdict about the content rather than the folder. Criteria
    10 and 12 stay scoped to out/ as written.
    """
    scratch = Path(scratch)
    direct = out_dir(scratch) / name
    if direct.is_file():
        return direct
    for path in walk(out_dir(scratch)):
        if path.name.lower() == name.lower():
            return path
    for path in walk(scratch):
        if path.name.lower() == name.lower():
            return path
    return None


def load_json(path):
    """Return (doc, error). One or the other is always None."""
    text = read(path)
    if not text.strip():
        return None, "file is empty"
    try:
        return json.loads(text), None
    except ValueError as exc:
        return None, "does not parse as JSON: %s" % exc


def run_clock(scratch):
    """The fixed clock the week is graded against."""
    path = Path(scratch) / "export-manifest.json"
    if path.is_file():
        doc, err = load_json(path)
        if isinstance(doc, dict):
            when = parse_dt(doc.get("exported_at"))
            if when is not None:
                return when
    return RUN_CLOCK


# ------------------------------------------------------------ key access


def nkey(name):
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


def get(record, *names):
    """Value of the first key matching any of `names`, punctuation-blind."""
    if not isinstance(record, dict):
        return None
    wanted = {nkey(n) for n in names}
    for key, value in record.items():
        if nkey(key) in wanted:
            return value
    return None


def has_key(record, *names):
    if not isinstance(record, dict):
        return False
    wanted = {nkey(n) for n in names}
    return any(nkey(k) in wanted for k in record)


def deep_keys(doc, prefix=""):
    """Every key anywhere in a parsed document, as dotted paths."""
    if isinstance(doc, dict):
        for key, value in doc.items():
            path = "%s.%s" % (prefix, key) if prefix else str(key)
            yield str(key), path
            yield from deep_keys(value, path)
    elif isinstance(doc, list):
        for i, value in enumerate(doc):
            yield from deep_keys(value, "%s[%d]" % (prefix, i))


def is_empty(value):
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, dict, tuple, set)):
        return len(value) == 0
    return False


def text_of(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (list, tuple, set)):
        return " ".join(text_of(v) for v in value)
    if isinstance(value, dict):
        return " ".join(text_of(v) for v in value.values())
    return str(value)


# ---------------------------------------------------------------- time

_TS = re.compile(
    r"(\d{4})-(\d{2})-(\d{2})"
    r"(?:[T ](\d{2}):(\d{2})(?::(\d{2}))?\s*(Z|[+-]\d{2}:?\d{2})?)?")


def parse_dt(value):
    """Parse the timestamp forms an attempt plausibly writes.

    Naive values are read as UTC. The fixture's clock is UTC throughout
    and a criterion that turned on a missing suffix would be grading
    punctuation.
    """
    if isinstance(value, _dt.datetime):
        return value if value.tzinfo else value.replace(
            tzinfo=_dt.timezone.utc)
    if isinstance(value, _dt.date):
        return _dt.datetime(value.year, value.month, value.day,
                            tzinfo=_dt.timezone.utc)
    if not isinstance(value, str):
        return None
    match = _TS.search(value)
    if not match:
        return None
    year, month, day, hour, minute, second, zone = match.groups()
    try:
        stamp = _dt.datetime(int(year), int(month), int(day),
                             int(hour or 0), int(minute or 0),
                             int(second or 0))
    except ValueError:
        return None
    if zone and zone not in ("Z", "z"):
        sign = 1 if zone[0] == "+" else -1
        digits = zone[1:].replace(":", "")
        offset = _dt.timedelta(hours=int(digits[:2]), minutes=int(digits[2:]))
        return stamp.replace(tzinfo=_dt.timezone(sign * offset))
    return stamp.replace(tzinfo=_dt.timezone.utc)


# ------------------------------------------------------------- triage

_ID_TAIL = re.compile(r"(\d{1,4})\s*$")

RECORD_LIST_KEYS = ("items", "records", "triage", "tickets", "entries",
                    "conversations", "inbox", "results", "rows")

ID_KEYS = ("id", "item", "item_id", "itemid", "item_number", "number",
           "no", "ticket", "ticket_id", "inbox_id", "conversation_id",
           "item_no", "index")


def normalise_id(value):
    """`17`, `"17"`, `"0017"`, `"item-17"` are all item 17."""
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if not isinstance(value, str):
        return None
    match = _ID_TAIL.search(value.strip())
    if not match:
        return None
    return int(match.group(1))


def triage_records(doc):
    """Return (records, note) where records is a list of (raw_id, dict).

    Accepts the three shapes an attempt writes: a bare list, a mapping
    with the list under a named key, or a mapping keyed by item id.
    """
    if isinstance(doc, list):
        return [(get(r, *ID_KEYS), r) for r in doc if isinstance(r, dict)], \
            "top level list"
    if not isinstance(doc, dict):
        return [], "top level is %s, not a list or a mapping" % type(doc).__name__
    for key in RECORD_LIST_KEYS:
        value = get(doc, key)
        if isinstance(value, list):
            return [(get(r, *ID_KEYS), r) for r in value
                    if isinstance(r, dict)], "list under %r" % key
    for value in doc.values():
        if isinstance(value, list) and value and all(
                isinstance(v, dict) for v in value):
            return [(get(r, *ID_KEYS), r) for r in value], "the only list in "\
                "the document"
    pairs = [(k, v) for k, v in doc.items() if isinstance(v, dict)]
    if pairs and all(normalise_id(k) is not None for k, _ in pairs):
        return [(get(v, *ID_KEYS) if get(v, *ID_KEYS) is not None else k, v)
                for k, v in pairs], "mapping keyed by item id"
    return [], "no list of records found in the document"


def load_triage(scratch):
    """Return (by_id, error). by_id maps int item id to its record."""
    path = find_artefact(scratch, "triage.json")
    if path is None:
        return None, "no triage.json under out/"
    doc, err = load_json(path)
    if err:
        return None, "%s %s" % (rel(scratch, path), err)
    records, _note = triage_records(doc)
    if not records:
        return None, "%s carries no triage records" % rel(scratch, path)
    by_id = {}
    for raw, record in records:
        num = normalise_id(raw)
        if num is not None:
            by_id[num] = record
    if not by_id:
        return None, "%s carries records with no readable item ids" \
            % rel(scratch, path)
    return by_id, None


def load_incident(scratch):
    """Return (doc, error) for incident-0001.json."""
    path = find_artefact(scratch, "incident-0001.json")
    if path is None:
        return None, "no incident-0001.json under out/"
    doc, err = load_json(path)
    if err:
        return None, "%s %s" % (rel(scratch, path), err)
    if not isinstance(doc, dict):
        return None, "incident-0001.json is not a JSON object"
    return doc, None


# ---------------------------------------------------------- customers


def customers(scratch):
    """Rows of customers.csv, or [] when the fixture's copy is gone."""
    path = Path(scratch) / "customers.csv"
    if not path.is_file():
        return []
    try:
        with open(path, newline="", encoding="utf-8",
                  errors="replace") as handle:
            return list(csv.DictReader(handle))
    except OSError:
        return []


# ------------------------------------------------- keys and headings

_MD_HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.*?)\s*#*\s*$", re.M)
_MD_LABEL = re.compile(
    r"^\s{0,6}(?:[-*+]\s+)?\*{0,2}([A-Za-z][A-Za-z0-9 _./-]{0,48})\*{0,2}\s*:",
    re.M)
_LOG_FIELD = re.compile(r"([A-Za-z][A-Za-z0-9_.-]{0,40})\s*=")
_TABLE_HEADER = re.compile(r"^\s*\|(.+)\|\s*$", re.M)


def label_positions(path, text):
    """Every key or heading in a delivered file, as (label, where) pairs.

    Criterion 10 is scoped to keys and headings rather than to prose, so
    a policy that says in a sentence which statistic it refuses to
    report is not caught by it. That is deliberate: the criterion names
    keys and headings, and a text-wide search would fail a tree for
    naming the thing it avoids.
    """
    suffix = Path(path).suffix.lower()
    out = []
    if suffix in (".json", ".jsonl", ".ndjson"):
        docs = []
        if suffix == ".json":
            try:
                docs = [json.loads(text)]
            except ValueError:
                docs = []
        else:
            for line in text.splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    docs.append(json.loads(line))
                except ValueError:
                    continue
        for doc in docs:
            for key, dotted in deep_keys(doc):
                out.append((key, "key %s" % dotted))
        if out:
            return out
    for match in _MD_HEADING.finditer(text):
        out.append((match.group(1), "heading"))
    for match in _TABLE_HEADER.finditer(text):
        for cell in match.group(1).split("|"):
            cell = cell.strip()
            if cell and not set(cell) <= set("-: "):
                out.append((cell, "table heading"))
    for match in _MD_LABEL.finditer(text):
        out.append((match.group(1).strip(), "field label"))
    for match in _LOG_FIELD.finditer(text):
        out.append((match.group(1), "log field"))
    return out
