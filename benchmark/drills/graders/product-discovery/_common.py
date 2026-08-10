"""Shared helpers for the product-discovery drill graders. Stdlib only.

Not a grader. The runner looks for `c<N>.py` by name, so this file is
never mistaken for a criterion.

Exit codes follow the grader contract: 0 pass, 1 fail, 2 the criterion
cannot be settled in this environment. The third is used where the thing
a criterion needs is missing from the machine rather than from the
delivered tree: the frozen fixture itself, which is the authority for
what counts as a real source, what the requested feature was called and
how many weekly active users exist. Grading a record against a fixture
that is not there would invent findings about work nobody inspected.

Three decisions worth stating, because each of them is an
interpretation of the frozen spec rather than a transcription of it.

**Wrapped lines.** The spec says "line" of the signal and risk
grammars. The house style wraps prose at seventy-two columns and the
pack's own exemplar wraps signal lines across two. A grader that matched
raw source lines would fail every record written the way the pack
teaches. So bullets are joined with their continuation lines first, the
way any Markdown reader joins them, and the grammar is matched against
the joined line.

**The feature name.** Criterion 2 says "the feature name from
`request.md`". Pulling a feature name out of English is a guess, so the
name is a fixed input of the drill, frozen here with the fixture, and
every grader that uses it first checks that it still occurs in
`request.md`. If the fixture drifts the criterion goes unsettled rather
than silently grading the wrong word.

**Dates are not statistics.** Criterion 5 extracts every integer and
decimal from the record. Dates, times and bare years are blanked before
extraction on both sides. Otherwise every day of the month in the ticket
export would enter the allowed set and the criterion would wave through
any small number at all.
"""

import csv
import json
import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

PASS, FAIL, UNSETTLED = 0, 1, 2

RECORD = "discovery.md"

REQUEST = "request.md"
PERSONAS = "personas.md"
SUPPORT = "support_export.csv"
METRICS = "metrics.json"

SCENARIO_REL = "benchmark/drills/scenarios/product-discovery"

# Fixed inputs of the drill, frozen with the fixture.
FEATURE_NAME = "barcode scanning"
FEATURE_TERMS = ("barcode",)

DECISIONS = ("BUILD", "TEST", "KILL")

WAU_KEY = "weekly_active_users"


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


def flatten(text):
    return re.sub(r"\s+", " ", text).strip()


def clip(text, limit=240):
    text = flatten(text)
    return text if len(text) <= limit else text[:limit - 1] + "…"


# ------------------------------------------------------------- the fixture


def repo_root():
    """The EOS repository this grader ships inside.

    graders/<pack>/_common.py -> graders/<pack> -> graders -> drills ->
    benchmark -> root. The graded tree is somewhere else entirely.
    """
    return Path(__file__).resolve().parents[4]


def fixture_root(cid):
    """The frozen scenario, which is the authority these criteria need.

    Not the delivered tree: a record may not legitimise an invented
    source, an edited user count or a renamed feature by writing the
    file it cites into its own delivery.
    """
    path = repo_root() / SCENARIO_REL
    if not path.is_dir():
        emit(cid, UNSETTLED,
             "the frozen scenario is not at %s, so there is nothing to "
             "check the record against here" % SCENARIO_REL)
    return path


def fixture_files(cid):
    """Every file in the frozen fixture, as relative POSIX paths."""
    root = fixture_root(cid)
    out = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if rel.startswith(".git/"):
            continue
        out.append(rel)
    return out


def is_fixture_file(name, files):
    """True when `name` names a file of the frozen fixture.

    A record may cite `support_export.csv` or `data/support_export.csv`
    and mean the same file, so both the relative path and the bare name
    are accepted. Matching is case-insensitive: the fixture is all lower
    case and a capitalised citation is a typographical difference, not
    an invented source.
    """
    name = name.strip().strip("`'\"").rstrip(".,;:)")
    if not name:
        return False
    low = name.lower().lstrip("./")
    for rel in files:
        if low == rel.lower() or low == Path(rel).name.lower():
            return True
    return False


LOOKS_LIKE_A_FILE = re.compile(r"^[\w./\\-]+\.[A-Za-z]{2,5}$")


def support_rows(cid):
    path = fixture_root(cid) / SUPPORT
    try:
        with open(path, newline="", encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle))
    except (OSError, csv.Error, UnicodeError) as exc:
        emit(cid, UNSETTLED,
             "the frozen %s will not read (%s), and the counts this "
             "criterion checks come out of it" % (SUPPORT, exc))
    if not rows:
        emit(cid, UNSETTLED, "the frozen %s holds no rows" % SUPPORT)
    return rows


def metrics_doc(cid):
    path = fixture_root(cid) / METRICS
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        emit(cid, UNSETTLED,
             "the frozen %s will not read (%s), and the population this "
             "criterion checks against comes out of it" % (METRICS, exc))


def weekly_active_users(cid):
    doc = metrics_doc(cid)
    value = doc.get(WAU_KEY)
    if not isinstance(value, int) or isinstance(value, bool):
        emit(cid, UNSETTLED,
             "the frozen %s carries no integer %s, so there is no "
             "population to compare a sample against" % (METRICS, WAU_KEY))
    return value


def require_feature_name(cid):
    """The frozen feature name, checked against the fixture that froze it."""
    text = read(fixture_root(cid) / REQUEST).lower()
    if not text:
        emit(cid, UNSETTLED,
             "the frozen %s is missing or empty, so the requested feature "
             "cannot be established" % REQUEST)
    for term in (FEATURE_NAME,) + FEATURE_TERMS:
        if term.lower() not in text:
            emit(cid, UNSETTLED,
                 "the frozen %s no longer contains %r, so this grader's "
                 "copy of the feature name has drifted from the fixture "
                 "and grading it would test the wrong word"
                 % (REQUEST, term))
    return FEATURE_NAME


# ------------------------------------------------------------- the record


def record_path(scratch):
    """`discovery.md`, at the top of the tree or anywhere below it."""
    top = Path(scratch) / RECORD
    if top.is_file():
        return top
    found = [p for p in sorted(Path(scratch).rglob(RECORD))
             if p.is_file() and ".git" not in p.parts]
    return found[0] if found else None


def record_text(cid, scratch):
    path = record_path(scratch)
    if path is None:
        emit(cid, FAIL,
             "no %s anywhere in the delivered tree, so there is no record "
             "to grade" % RECORD)
    text = read(path)
    if not text.strip():
        emit(cid, FAIL, "%s is empty" % RECORD)
    return text


_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")


def sections(text):
    """Map the exact text of each `##` heading to its body.

    Exact, because the pack says a checker reads headings literally and
    a renamed heading is a missing section. A body runs to the next
    heading at level one or two, so a `###` subheading stays inside it.
    """
    out = {}
    current = None
    body = []
    for line in text.splitlines():
        m = _HEADING.match(line)
        if m and len(m.group(1)) <= 2:
            if current is not None:
                out[current] = "\n".join(body)
            current = m.group(2).strip() if len(m.group(1)) == 2 else None
            body = []
            continue
        if current is not None:
            body.append(line)
    if current is not None:
        out[current] = "\n".join(body)
    return out


def section(text, name):
    """The body of `## <name>`, or None when no such heading exists."""
    return sections(text).get(name)


_BULLET = re.compile(r"^\s*[-*+]\s")


def logical_lines(text):
    """Lines with wrapped continuations folded back in.

    A bullet swallows the non-blank lines that follow it until a blank
    line, another bullet, a heading or a fence, which is what a Markdown
    reader does with a wrapped list item and what the house style's
    seventy-two column wrap produces.
    """
    out = []
    open_bullet = False
    for raw in text.splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped:
            out.append("")
            open_bullet = False
            continue
        if stripped.startswith("```") or stripped.startswith("~~~"):
            out.append(stripped)
            open_bullet = False
            continue
        if _HEADING.match(line):
            out.append(line)
            open_bullet = False
            continue
        if _BULLET.match(line):
            out.append(line.strip())
            open_bullet = True
            continue
        if open_bullet:
            out[-1] = out[-1] + " " + stripped
            continue
        out.append(line)
    return out


def first_non_blank(text):
    for line in (text or "").splitlines():
        if line.strip():
            return line.strip()
    return ""


def decision_of(text):
    """The verdict word under `## Decision`, or None."""
    body = section(text, "Decision")
    if body is None:
        return None
    word = first_non_blank(body)
    return word if word in DECISIONS else None


# ------------------------------------------------------------- the numbers


_ISO_DATE = re.compile(r"\b\d{4}-\d{1,2}-\d{1,2}\b")
_SLASH_DATE = re.compile(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b")
_CLOCK = re.compile(r"\b\d{1,2}:\d{2}(?::\d{2})?\b")
_YEAR = re.compile(r"\b(?:19|20)\d{2}\b")
_LIST_MARKER = re.compile(r"(?m)^(\s*)\d{1,2}[.)](\s)")
_NUMBER = re.compile(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?")


def canon(token):
    """One spelling per value, so 14, 14.0 and 1,400 do not diverge."""
    try:
        value = Decimal(str(token).replace(",", "")).normalize()
    except (InvalidOperation, ValueError):
        return None
    return format(value, "f")


def _blank_dates(text):
    text = _LIST_MARKER.sub(r"\1\2", text)
    text = _ISO_DATE.sub(" ", text)
    text = _SLASH_DATE.sub(" ", text)
    text = _CLOCK.sub(" ", text)
    return _YEAR.sub(" ", text)


def numbers_in(text):
    """Every integer and decimal in a piece of text, dates excepted."""
    found = []
    for match in _NUMBER.finditer(_blank_dates(text)):
        value = canon(match.group(0))
        if value is not None:
            found.append(value)
    return found


def numbers_with_context(text, width=90):
    """The same, each with the run of text it sits in, for reporting."""
    cleaned = _blank_dates(text)
    out = []
    for match in _NUMBER.finditer(cleaned):
        value = canon(match.group(0))
        if value is None:
            continue
        start = max(0, match.start() - width // 2)
        out.append((value, clip(cleaned[start:match.end() + width // 2], 120)))
    return out


TEXT_SUFFIXES = {".md", ".csv", ".json", ".txt", ".py", ".cfg", ".ini",
                 ".toml", ".yml", ".yaml", ".html", ".css", ".gitignore"}


def fixture_literals(cid):
    """Every number that appears anywhere in the frozen fixture."""
    root = fixture_root(cid)
    literals = set()
    for rel in fixture_files(cid):
        path = root / rel
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name != \
                ".gitignore":
            continue
        literals.update(numbers_in(read(path)))
    return literals


def filter_counts(cid):
    """Row counts reachable by a single equality filter on the export.

    One column, one value. Conjunctions are deliberately not offered:
    pairs of filters over this export reach most small integers, and an
    allowed set that holds most small integers is not checking anything.
    """
    rows = support_rows(cid)
    counts = {canon(len(rows))}
    columns = rows[0].keys()
    for column in columns:
        if column in ("subject", "body", "ticket_id", "opened_at"):
            continue
        seen = {}
        for row in rows:
            key = (row.get(column) or "").strip()
            seen[key] = seen.get(key, 0) + 1
        for value in seen.values():
            counts.add(canon(value))
    return counts


_QUOTED = re.compile(r"[\"“]([^\"”\n]{2,60})[\"”]|`([^`\n]{2,60})`")


def quoted_terms(text):
    """The search terms a record states, as it states them.

    Double quotes and backticks only. British prose is full of
    apostrophes, and treating them as quotation marks turns "the desk's
    own label" into a search term, which would hand the allowed set a
    count nobody stated.
    """
    out = []
    for match in _QUOTED.finditer(text):
        term = next(g for g in match.groups() if g is not None)
        term = term.strip()
        if term:
            out.append(term)
    return out


def keyword_counts(cid, terms):
    """How many exported tickets each stated term matches."""
    rows = support_rows(cid)
    blobs = [" ".join(str(v) for v in row.values()).lower() for row in rows]
    out = {}
    for term in terms:
        low = term.strip().lower()
        if not low:
            continue
        out[term] = sum(1 for blob in blobs if low in blob)
    return out
