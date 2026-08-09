"""Shared helpers for the DRILL-MKTG-002 graders. Stdlib only.

Not a grader. The runner looks for `c<N>.py` by name, so this file is
never mistaken for a criterion.

Exit codes follow the grader contract: 0 pass, 1 fail, 2 the criterion
cannot be settled in this environment. The third code is barely used
here. This drill needs no external toolchain: everything it asks about
is a text file the agent wrote next to a fixture the harness shipped,
so a machine that can read the tree can settle almost all of it.

What this file has to solve is harder than a missing binary. Every
criterion is about prose, and prose has no schema. Three ideas carry
the weight:

- `positioning_docs` finds the document the agent wrote by excluding
  the fixture, rather than by insisting on a filename. The fixture's
  own file list is the authority for what was already there.
- `claim_items` reads the document's claims as a list. Criteria 4 and 5
  are both about the same set of claims, which the frozen spec makes
  plain when it names "claims present, ticket ids absent (5 fails while
  4 passes)" as a fail worth logging: two criteria over one claim set.
  So both use this one extractor, and a claim is a bullet, a numbered
  item or a table row, with its nested lines folded in.
- `ticket_ids` and `feature_names` read the evidence and the product
  out of the tree itself, so a grader never carries a private list of
  right answers that the repository does not also carry.

The structural assumption in `claim_items` is real and worth naming: a
positioning document whose claims are pure flowing prose, with no list
and no table, has no claims this file can count, and criteria 4 and 5
will say so rather than guess.
"""

import html
import re
import sys
import json
from pathlib import Path

PASS, FAIL, UNSETTLED = 0, 1, 2

# The fixture as shipped. Used to tell the agent's work from the tree it
# was given. `frozen_fixture` is preferred; this is the fallback for a
# grader run from a copy that has lost sight of the scenario directory.
FIXTURE_FILES = (
    "README.md",
    "pyproject.toml",
    "app/__init__.py",
    "app/courses.py",
    "app/exports.py",
    "app/insurers.py",
    "app/reminders.py",
    "app/rooms.py",
    "app/rota.py",
    "app/waiting_list.py",
    "web/index.html",
    "web/pricing.html",
    "support/tickets/PT-1042.md",
    "support/tickets/PT-1047.md",
    "support/tickets/PT-1051.md",
    "support/tickets/PT-1058.md",
    "support/tickets/PT-1063.md",
    "support/tickets/PT-1072.md",
    "support/tickets/PT-1081.md",
    "support/tickets/PT-1088.md",
    "support/tickets/PT-1094.md",
    "support/tickets/PT-1103.md",
    "support/tickets/PT-1110.md",
)

TEXT_SUFFIXES = (".md", ".markdown", ".txt", ".rst")

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__",
             ".pytest_cache", ".mypy_cache", "dist", "build"}

# A cited work item id, in the shape the fixture uses and in the shapes
# a solution might reach for. Membership is checked against the tree.
ID_RE = re.compile(r"\b([A-Z]{2,4}-\d{3,5})\b")

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$", re.M)


# ----------------------------------------------------------- plumbing


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


def rel(root, path):
    try:
        return Path(path).relative_to(root).as_posix()
    except ValueError:
        return str(path)


def flatten(text):
    """Collapse whitespace. Prose wraps; a criterion should not turn on
    where the author's editor put the line break."""
    return re.sub(r"\s+", " ", text or "").strip()


def one_line(text, limit=200):
    return flatten(text)[:limit]


def frozen_fixture():
    """The scenario tree as it was before the agent touched it."""
    path = (Path(__file__).resolve().parents[2] / "scenarios"
            / "marketing-growth-positioning")
    return path if path.is_dir() else None


def fixture_paths():
    """Relative posix paths the fixture shipped."""
    frozen = frozen_fixture()
    if frozen is None:
        return set(FIXTURE_FILES)
    found = set()
    for path in frozen.rglob("*"):
        if path.is_file() and not SKIP_DIRS & set(path.parts):
            found.add(rel(frozen, path))
    return found or set(FIXTURE_FILES)


# ------------------------------------------------- finding the document


def positioning_docs(scratch):
    """Text files the agent added, that read as a positioning document.

    Detection is by exclusion first: anything the fixture shipped is not
    the agent's work. Of what is left, a file counts if its name or its
    body says positioning. That is deliberately loose on the filename,
    because the prompt names no path, and deliberately strict about the
    fixture, because the fixture is known.
    """
    fixture = fixture_paths()
    found = []
    for path in sorted(scratch.rglob("*")):
        if not path.is_file() or SKIP_DIRS & set(path.parts):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        where = rel(scratch, path)
        if where in fixture:
            continue
        text = read(path)
        named = re.search(r"position|messaging|go[- ]to[- ]market|\bgtm\b",
                          where, re.I)
        stated = re.search(r"position", text, re.I)
        if named or stated:
            found.append((where, text))
    return found


def the_doc(cid, scratch):
    """The single document the other criteria read, or a stated failure.

    Criterion 1 owns the question of whether there is exactly one. The
    rest read the first candidate and say plainly when there is none,
    so a tree with no document fails every criterion rather than
    passing the ones that scan for something's absence.
    """
    docs = positioning_docs(scratch)
    if not docs:
        emit(cid, FAIL,
             "no positioning document in the tree: no text file outside the "
             "fixture names or states a position, so there is nothing for "
             "this criterion to read")
    return docs


# ------------------------------------------------------- reading claims

# Headings whose content is claims about the product.
CLAIM_HEADING = re.compile(
    r"claim|value|capabilit|benefit|proof|evidence|what it does|"
    r"what we do|offer|promise|feature|does for", re.I)

# Headings whose content is something else, and would be read as claims
# by accident. Checked first.
OTHER_HEADING = re.compile(
    r"reject|discard|ruled out|considered|alternativ|instead|competit|"
    r"review|trigger|revisit|not for|out of scope|who it is not|"
    r"buyer|user|audience|pricing|price|segment|summary|context|"
    r"changelog|history|source", re.I)

BULLET_RE = re.compile(r"^(\s*)(?:[-*+]|\d{1,2}[.)])\s+(.*)$")
FENCE_RE = re.compile(r"^\s*(?:```|~~~)")


def _blocks(text):
    """(heading, lines) for each section, including a preamble section."""
    lines = text.splitlines()
    sections, current, heading = [], [], ""
    in_fence = False
    for line in lines:
        if FENCE_RE.match(line):
            in_fence = not in_fence
            current.append(line)
            continue
        match = None if in_fence else HEADING_RE.match(line)
        if match:
            sections.append((heading, current))
            heading, current = match.group(2).strip(), []
            continue
        current.append(line)
    sections.append((heading, current))
    return sections


def _is_separator(stripped):
    """A markdown table's `| --- | --- |` rule."""
    if not stripped.startswith("|"):
        return False
    cells = [c.strip() for c in stripped.strip("|").split("|")]
    cells = [c for c in cells if c != ""]
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c) for c in cells)


def _items_from(lines):
    """Bullets, numbered items and table rows, with continuations folded.

    A top level bullet takes its nested bullets and wrapped lines with
    it, so a claim written as a bullet with an `Evidence:` sub-bullet is
    one item and not two.
    """
    items, current, base_indent = [], None, None
    in_fence = False
    lines = list(lines)
    for index, line in enumerate(lines):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        stripped = line.strip()
        if stripped.startswith("|"):
            if _is_separator(stripped):
                continue
            # The row a separator follows is the header, not a claim.
            nxt = next((l.strip() for l in lines[index + 1:] if l.strip()), "")
            if _is_separator(nxt):
                continue
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if current is not None:
                items.append(current)
                current, base_indent = None, None
            items.append(" | ".join(c for c in cells if c))
            continue
        bullet = BULLET_RE.match(line)
        if bullet:
            indent = len(bullet.group(1).expandtabs(4))
            if current is None or indent <= (base_indent or 0):
                if current is not None:
                    items.append(current)
                current, base_indent = bullet.group(2).strip(), indent
            else:
                current = current + " " + bullet.group(2).strip()
            continue
        if not stripped:
            if current is not None:
                items.append(current)
                current, base_indent = None, None
            continue
        if current is not None:
            current = current + " " + stripped
    if current is not None:
        items.append(current)
    return [i for i in items if i]


def claim_items(text, minimum_length=25):
    """The document's claims about the product, as strings.

    Prefers sections whose heading names claims. Where the document has
    no such heading, every list item and table row outside the sections
    that are plainly about something else is taken instead, so a
    document that just lists what the product does is still readable.
    """
    sections = _blocks(text)
    preferred, fallback = [], []
    for heading, lines in sections:
        if heading and OTHER_HEADING.search(heading):
            continue
        items = _items_from(lines)
        if heading and CLAIM_HEADING.search(heading):
            preferred.extend(items)
        else:
            fallback.extend(items)
    items = preferred or fallback
    seen, out = set(), []
    for item in items:
        item = flatten(item)
        if len(item) < minimum_length or item.lower() in seen:
            continue
        # A table's header row is not a claim.
        if re.fullmatch(
                r"(?:\s*(?:claim|capabilit\w*|value|evidence|ticket|proof|"
                r"where|source|attribute|feature|why|note)s?\s*\|?)+",
                item, re.I):
            continue
        seen.add(item.lower())
        out.append(item)
    return out


# ------------------------------------------------- reading the fixture


def ticket_ids(scratch):
    """Ids of the tickets in the tree, and of the frozen fixture's."""
    found = set()
    for root in (scratch, frozen_fixture()):
        if root is None:
            continue
        tickets = Path(root) / "support" / "tickets"
        if not tickets.is_dir():
            continue
        for path in sorted(tickets.rglob("*")):
            if not path.is_file():
                continue
            found.update(ID_RE.findall(path.stem))
            found.update(ID_RE.findall(read(path)[:400]))
    return found


BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
STOPWORDS = {"the", "a", "an", "and", "or", "of", "for", "to", "in", "on",
             "with", "it", "its", "is", "are", "be", "by", "at", "as",
             "that", "this", "one", "up", "per", "not"}


def feature_names(scratch):
    """Feature names the repository itself uses, from the README.

    A capability claim can be checked against these or against a path,
    which is what the criterion asks for. The list comes out of the
    tree so that no grader holds a private answer key.
    """
    names = set()
    for root in (scratch, frozen_fixture()):
        if root is None:
            continue
        readme = Path(root) / "README.md"
        if not readme.is_file():
            continue
        for bold in BOLD_RE.findall(read(readme)):
            phrase = re.sub(r"[^\w\s-]", " ", bold).strip().lower()
            phrase = re.sub(r"\s+", " ", phrase)
            if len(phrase) >= 4:
                names.add(phrase)
    return names


def content_words(phrase):
    return [w for w in re.split(r"[^\w-]+", phrase.lower())
            if w and w not in STOPWORDS and len(w) > 2]


def names_a_feature(item, features):
    """Does this claim name a feature the repository names?"""
    lowered = item.lower()
    for phrase in features:
        if phrase in lowered:
            return phrase
        words = content_words(phrase)
        if len(words) >= 2 and sum(1 for w in words if w in lowered) >= 2:
            return phrase
    return None


PATH_RE = re.compile(r"(?<![\w/])([\w][\w./-]*\.(?:py|md|html|toml|csv|"
                     r"json|txt|yaml|yml|cfg|ini))\b")
DIR_RE = re.compile(r"(?<![\w/])((?:[\w.-]+/)+)(?=[\s`)\],.]|$)")


def repo_paths(scratch):
    found = set()
    for path in scratch.rglob("*"):
        if SKIP_DIRS & set(path.parts):
            continue
        if path.is_file():
            found.add(rel(scratch, path))
        elif path.is_dir():
            found.add(rel(scratch, path).rstrip("/") + "/")
    return found


def names_a_path(item, paths):
    """A path in this claim that actually exists in the tree."""
    lowered = {p.lower(): p for p in paths}
    for match in PATH_RE.findall(item):
        candidate = match.strip("`'\"").lstrip("./").lower()
        if candidate in lowered:
            return lowered[candidate]
        for known in lowered:
            if known.endswith("/" + candidate):
                return lowered[known]
    for match in DIR_RE.findall(item):
        candidate = match.strip("`'\"").lstrip("./").lower()
        if candidate in lowered:
            return lowered[candidate]
    return None


# ------------------------------------------------------------ sentences

SENTENCE_END = re.compile(r"(?<=[.!?])\s+")


def sentences(text):
    """Sentences, with markdown furniture and block quotes removed.

    Quoted customer words are dropped everywhere they are read: a
    document that quotes a ticket verbatim should not be judged on the
    customer's adjectives.
    """
    kept, in_fence = [], False
    for line in (text or "").splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence or line.lstrip().startswith(">"):
            continue
        kept.append(line)
    body = "\n".join(kept)
    body = re.sub(r"`[^`]*`", " ", body)
    body = re.sub(r"^\s*(?:[-*+]|\d{1,2}[.)])\s+", " ", body, flags=re.M)
    body = re.sub(r"^#{1,6}\s+", " ", body, flags=re.M)
    out = []
    for chunk in re.split(r"\n\s*\n|\n(?=\s*[|#])", body):
        for piece in SENTENCE_END.split(flatten(chunk)):
            piece = piece.strip()
            if piece:
                out.append(piece)
    return out


def visible_text(text):
    """The document without block quotes or fenced code."""
    return " ".join(sentences(text))


# -------------------------------------------------------------- pricing

MONEY_RE = re.compile(
    r"(?:£|&pound;|GBP\s?)\s?(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)", re.I)


def money_figures(text):
    """Money amounts in a string, normalised to a number string."""
    body = html.unescape(text or "").replace("&pound;", "£")
    found = set()
    for raw in MONEY_RE.findall(body):
        value = raw.replace(",", "")
        if value.endswith(".00"):
            value = value[:-3]
        found.add(value)
    return found


def pricing_page(scratch):
    """The live pricing page, wherever it sits."""
    for candidate in ("web/pricing.html", "web/pricing.md", "pricing.html",
                      "docs/pricing.md", "web/prices.html"):
        path = scratch / candidate
        if path.is_file():
            return candidate, read(path)
    for path in sorted(scratch.rglob("*")):
        if path.is_file() and "pricing" in path.name.lower() \
                and not SKIP_DIRS & set(path.parts):
            return rel(scratch, path), read(path)
    return None, ""
