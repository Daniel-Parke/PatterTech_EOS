"""Shared helpers for the agentic development topology drill graders.

Not a grader. The runner looks for `c<N>.py` by name, so this file is
never mistaken for a criterion.

Every criterion in this drill is a claim about one delivered file,
`drill-out/TOPOLOGY_DECISION.md`, so the shared work is finding that
file, splitting it into its level-two sections, splitting a section
into clauses, and recognising the canonical strings the pack tells an
agent to use. Doing that once here keeps the eleven graders arguing
about their own criterion rather than about Markdown.

It also decides polarity, which is the one thing these graders got
wrong. A criterion asks whether the record *asserts* something. Finding
the words it would be asserted with is not the same question: "the
merged report is written by exactly one agent" and "the merged report
is not written by exactly one agent" carry the same tokens and mean
opposite things. `negated()` below answers, for a span of a clause,
whether an odd number of negations reaches it, so every grader can ask
for the claim rather than for the vocabulary. Where a criterion wants a
denial rather than an assertion, and c8 wants both, the same function
is read the other way round.

Exit codes follow the grader contract: 0 pass, 1 fail, 2 the criterion
cannot be settled in this environment. Only c10 can reach 2, and only
when the evidence registry it has to check ids against is not reachable
from where the grader is run. That is a gap in the environment, not a
finding against the delivered file.
"""

import json
import re
import sys
from pathlib import Path

PASS, FAIL, UNSETTLED = 0, 1, 2

# Where the drill says the file goes. Anywhere else is accepted and
# said out loud in the reason, because a criterion about the argument
# in a document should not turn on the folder it landed in.
OUTPUT_REL = "drill-out/TOPOLOGY_DECISION.md"
OUTPUT_NAME = "TOPOLOGY_DECISION.md"


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


def find_output(scratch):
    exact = Path(scratch) / "drill-out" / OUTPUT_NAME
    if exact.is_file():
        return exact
    hits = sorted(p for p in Path(scratch).rglob(OUTPUT_NAME)
                  if p.is_file() and ".git" not in p.parts)
    return hits[0] if hits else None


def require_output(cid):
    """Return (path, rel, raw_text, prose) or fail the criterion.

    `prose` has fenced code blocks removed and backticks dropped, so a
    canonical string written as `fan-out/fan-in` reads the same as one
    written plainly. `raw_text` is kept for the line count and the
    voice check, which are claims about the file as delivered.
    """
    scratch = scratch_dir()
    path = find_output(scratch)
    if path is None:
        emit(cid, FAIL,
             "no %s anywhere in the tree, so nothing to grade" % OUTPUT_REL)
    rel = path.relative_to(scratch).as_posix()
    raw = read(path)
    if not raw.strip():
        emit(cid, FAIL, "%s is empty" % rel)
    return path, rel, raw, prose_of(raw)


def prose_of(text):
    without_fences = re.sub(r"^```.*?^```", "\n", text,
                            flags=re.S | re.M)
    return without_fences.replace("`", "")


def strip_code(text):
    """Drop fenced blocks, inline code spans and indented blocks."""
    text = re.sub(r"^```.*?^```", "\n", text, flags=re.S | re.M)
    text = re.sub(r"`[^`\n]*`", " ", text)
    return "\n".join("" if re.match(r"^ {4,}\S", line) else line
                     for line in text.splitlines())


def flatten(text):
    return re.sub(r"\s+", " ", text).strip()


# ------------------------------------------------------------ structure


def split_front_matter(text):
    """Return (front_matter_text_or_None, body)."""
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    return text[3:end], text[end + 4:]


def parse_front_matter(block):
    """A deliberately small YAML reader: scalars and lists, nothing else.

    Enough for `summary`, `type` and `tags`, which is all any criterion
    here asks about. A real parser is not available to a stdlib-only
    grader and pulling one in would make the drill depend on a package.
    """
    data = {}
    key = None
    for line in (block or "").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        item = re.match(r"^\s+-\s*(.*)$", line)
        if item and key:
            data.setdefault(key, [])
            if isinstance(data[key], list):
                data[key].append(item.group(1).strip().strip("'\""))
            continue
        pair = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$", line)
        if not pair:
            continue
        key, value = pair.group(1).strip(), pair.group(2).strip()
        if value.startswith("[") and value.endswith("]"):
            data[key] = [v.strip().strip("'\"")
                         for v in value[1:-1].split(",") if v.strip()]
        elif value:
            data[key] = value.strip("'\"")
        else:
            data[key] = []
    return data


_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$", re.M)


def sections(body):
    """Every level-two section, as a list of (title, text)."""
    out = []
    marks = [(m.start(), len(m.group(1)), m.group(2), m.end())
             for m in _HEADING.finditer(body)]
    for i, (start, level, title, after) in enumerate(marks):
        if level != 2:
            continue
        stop = len(body)
        for later_start, later_level, _, _ in marks[i + 1:]:
            if later_level <= 2:
                stop = later_start
                break
        out.append((title, body[after:stop]))
    return out


def section(body, name):
    """The level-two section called `name`, or None.

    A heading of "Bounds and stop conditions" counts as Bounds: the
    criterion asks for the section, not for the absence of a subtitle.
    """
    wanted = name.strip().lower()
    for title, text in sections(body):
        cleaned = title.strip().strip("#").strip().lower()
        cleaned = re.sub(r"^[\d.\s]+", "", cleaned)
        if cleaned == wanted or re.match(r"^%s\b" % re.escape(wanted),
                                         cleaned):
            return text
    return None


_BULLET = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)")
# A clause ends at a full stop, a semicolon or a "then". Not at a colon:
# "Extraction: fan-out/fan-in" is one claim and splitting it would cut
# the stage away from the topology it was assigned.
_SPLIT = re.compile(r"(?<=[.?!])\s+|\s*;\s*|\s+then\s+")


def blocks(text):
    """List items and paragraphs, each flattened to one line."""
    out, current = [], []
    for line in (text or "").splitlines():
        stripped = line.strip()
        if not stripped:
            if current:
                out.append(" ".join(current))
                current = []
            continue
        if _BULLET.match(line) or stripped.startswith("|"):
            if current:
                out.append(" ".join(current))
            current = [stripped]
            continue
        current.append(stripped)
    if current:
        out.append(" ".join(current))
    return out


def clauses(text):
    """Blocks split into clauses. A table row is left whole.

    Splitting a row on its pipes would separate the stage from the
    topology sitting in the next cell, which is the one relationship
    two of these criteria are about.
    """
    out = []
    for block in blocks(text):
        if block.lstrip().startswith("|"):
            out.append(block)
            continue
        out.extend(part.strip() for part in _SPLIT.split(block)
                   if part and part.strip())
    return out


# ------------------------------------------------------------ polarity


# The words a record denies something with. Grouped only for reading.
_NEG_CUE = re.compile(
    r"\b(?:"
    r"not|n't|never|neither|nor|none|nothing|nobody|"
    r"without|lacks?|lacking|lacked|absent|absence|missing|"
    r"cannot|can't|won't|don't|doesn't|didn't|isn't|aren't|wasn't|weren't|"
    r"shouldn't|wouldn't|mustn't|needn't|"
    r"rather\s+than|instead\s+of|other\s+than|far\s+from|"
    r"avoid(?:s|ed|ing)?|forbid(?:s|den|ding)?|forbade|forbids|"
    r"rules?\s+out|ruled\s+out|"
    r"refus(?:e|es|ed|ing)|reject(?:s|ed|ing)?|declin(?:e|es|ed)|"
    r"omit(?:s|ted|ting)?|skip(?:s|ped|ping)?|drop(?:s|ped|ping)?|"
    r"fails?\s+to|failed\s+to|"
    r"(?:stops?|stopped|falls?|fell|stops)\s+short\s+of|"
    r"unbounded|unlimited|uncapped|ungated|unchecked|unapproved|"
    r"unvalidated|unreviewed|"
    r"optional|unnecessary|waived?|waives|bypass(?:es|ed)?|disabled?|"
    r"exclude(?:s|d)?|disallow(?:s|ed)?|prohibit(?:s|ed)?|"
    r"deny|denies|denied"
    r")\b"
    # `no` is a cue, but `no more than 60 turns` is a bound, not a denial.
    r"|\bno\b",
    re.I)

# A cue followed by one of these is a comparative bound, not a denial:
# "no more than 60 turns", "must not exceed 200k tokens".
_LIMIT_IDIOM = re.compile(
    r"\s*(?:\w+\s+){0,2}"
    r"(?:(?:more|less|fewer|greater|larger|longer|later|higher|bigger)"
    r"\s+than\b|exceed|surpass|above\b|beyond\b|over\s+\d)",
    re.I)

# Where a negation stops reaching. A comma, a semicolon, a colon, a
# contrast or a consequence starts a new assertion, and so does an `and`
# that opens a fresh predicate. That last one matters: "is not a
# sequential pipeline and it never reaches a human checkpoint" negates
# two things once each, and counting both cues against the checkpoint
# would read the sentence as a double negative and call it affirmed.
_ENDER = re.compile(
    r"[,;:]"
    r"|\b(?:but|however|whereas|although|though|yet|instead|rather|"
    r"so|therefore|hence|thus|because|since|which\s+is\s+why|"
    # `until` and `unless` open the condition a negation was waiting
    # for: in "the pull request is not opened until a human approves"
    # the approval is asserted, not denied.
    r"until|unless)\b"
    r"|\b(?:and|or)\s+(?:it|they|we|the|a|an|this|that|there|no|not|"
    r"nothing|each|every|its|their|his|her|one)\b",
    re.I)

_AUX = {
    "is", "are", "was", "were", "be", "been", "being", "am",
    "will", "would", "shall", "should", "can", "could", "may", "might",
    "must", "do", "does", "did", "has", "have", "had",
    "it", "they", "we", "that", "which", "there", "here", "then",
    "the", "a", "an", "of", "for", "on", "in", "to", "by", "with",
    "from", "as", "at", "its", "their", "this", "these", "those",
    "all", "any", "every", "one",
}
_MAX_LEXICAL = 2


def _cues(text):
    """Negation cues in `text`, comparative bounds left out."""
    for match in _NEG_CUE.finditer(text):
        if _LIMIT_IDIOM.match(text, match.end()):
            continue
        yield match


_CONJUNCTION = re.compile(r"\b(?:and|or|but)\b", re.I)
_AUX_TAIL = re.compile(
    r"\b(?:is|are|was|were|be|been|being|am|will|would|shall|should|can|"
    r"could|may|might|must|do|does|did|has|have|had)\s*$", re.I)


def _trailing_gap_binds(gap, cue):
    """Does a cue after the span still negate it?

    Two ways, and a conjunction blocks both, because "no oracle for it
    and no evaluator-optimizer loop" is two claims and the second one is
    not about the first one's subject:

    - the gap is short and nearly all function words, which covers "the
      validator carries nothing";
    - or the cue hangs off an auxiliary, which covers "idempotence of
      the resumed side effects is not something this job provides",
      where the subject is long and the negation is still its own.
    """
    if _ENDER.search(gap + cue) or _CONJUNCTION.search(gap):
        return False
    if len(gap) <= 80 and _AUX_TAIL.search(gap):
        return True
    if len(gap) > 40:
        return False
    lexical = 0
    for word in re.findall(r"[A-Za-z']+", gap):
        if word.lower() in _AUX:
            continue
        lexical += 1
    return lexical <= _MAX_LEXICAL


def negation_count(text, span):
    """How many negations reach `span`, which is a (start, end) in text."""
    start, end = span
    count = 0
    for cue in _cues(text):
        if cue.end() <= start:
            if not _ENDER.search(text, cue.end(), start):
                count += 1
        elif cue.start() >= end:
            if _trailing_gap_binds(text[end:cue.start()], cue.group(0)):
                count += 1
    return count


def negated(text, span):
    """True when the claim at `span` is denied rather than asserted.

    Odd parity, so "no pull request is opened without approval" reads
    as the gate it is and "does not lack an oracle" reads as the oracle
    it claims.
    """
    return negation_count(text, span) % 2 == 1


def affirmed(text, span):
    return not negated(text, span)


def spans_of(pattern, text):
    """Every (start, end) where `pattern` matches, case-insensitively."""
    if isinstance(pattern, str):
        pattern = re.compile(pattern, re.I)
    return [m.span() for m in pattern.finditer(text)]


def asserts(text, pattern):
    """The first span of `pattern` in `text` that is not negated."""
    for span in spans_of(pattern, text):
        if affirmed(text, span):
            return span
    return None


def denies(text, pattern):
    """The first span of `pattern` in `text` that is negated."""
    for span in spans_of(pattern, text):
        if negated(text, span):
            return span
    return None


# ------------------------------------------------------- pack strings


# The ten canonical names from packs/agentic-development/refs/
# TOPOLOGY_CARD.md. The patterns tolerate a hyphen where the card has a
# space and the other way round, and nothing else: the card exists so a
# reader and a checker see the same word.
TOPOLOGIES = [
    ("direct single-agent", r"direct\s+single[-\s]?agent"),
    ("sequential pipeline", r"sequential\s+pipeline"),
    ("bounded loop", r"bounded\s+loop"),
    ("router", r"\brouters?\b"),
    ("dependency graph (DAG)", r"dependency\s+graph|\bDAGs?\b"),
    ("fan-out/fan-in", r"fan[-\s]?out\s*/\s*fan[-\s]?in"),
    ("orchestrator-worker", r"orchestrator[-\s]?worker"),
    ("evaluator-optimizer", r"evaluator[-\s]?optimi[sz]er"),
    ("event-driven resumable", r"event[-\s]?driven\s+resumable"),
    ("human checkpoint", r"human[-\s]checkpoints?"),
]

# The eight pressures, same card. Irreversibility counts as
# reversibility: it is the same axis named from the other end.
PRESSURES = [
    ("decomposability", r"decomposab"),
    ("shared-state coupling", r"shared[-\s]state\s+coupling"),
    ("oracle quality", r"oracle\s+quality|quality\s+of\s+the\s+oracle"),
    ("reversibility", r"\b(?:ir)?reversib"),
    ("latency", r"\blatency\b"),
    ("cost", r"\bcosts?\b"),
    ("context pressure", r"context\s+pressure|context\s+window\s+pressure"),
    ("failure localisation", r"failure\s+locali[sz]ation"),
]


def topologies_in(text):
    """Every topology the text mentions, whatever it says about it."""
    found = []
    for name, pattern in TOPOLOGIES:
        if re.search(pattern, text, re.I):
            found.append(name)
    return found


def topologies_asserted(text):
    """Topologies the text picks, as against ones it rules out.

    An occurrence counts when that occurrence is not negated, so
    "fan-out/fan-in, not orchestrator-worker" names one choice and one
    refusal rather than a shortlist of two.
    """
    return [name for name, pattern in TOPOLOGIES
            if asserts(text, re.compile(pattern, re.I)) is not None]


def topologies_denied(text):
    mentioned = topologies_in(text)
    asserted = set(topologies_asserted(text))
    return [n for n in mentioned if n not in asserted]


def pressures_in(text):
    return [name for name, pattern in PRESSURES
            if re.search(pattern, text, re.I)]


def pressure_spans(text):
    """(name, span) for every pressure named, in the order they appear."""
    out = []
    for name, pattern in PRESSURES:
        for span in spans_of(re.compile(pattern, re.I), text):
            out.append((name, span))
    return sorted(out, key=lambda row: row[1][0])


EXTRACTION = re.compile(r"extract", re.I)
MERGE = re.compile(r"\bmerge|\bmerged\b|weekly report|report file|"
                   r"roll[-\s]?up|pull request|\bPR\b", re.I)


def stage_clauses(text):
    """(extraction clauses, merge clauses) inside a section."""
    extraction, merge = [], []
    for clause in clauses(text):
        if EXTRACTION.search(clause):
            extraction.append(clause)
        if MERGE.search(clause):
            merge.append(clause)
    return extraction, merge


def distinct(names):
    seen, out = set(), []
    for name in names:
        if name not in seen:
            seen.add(name)
            out.append(name)
    return out


# --------------------------------------------------------- repository


def repo_root():
    """The EOS checkout this grader lives in, or None.

    Walked upwards rather than assumed, so moving the graders one level
    does not silently turn a real check into a guess.
    """
    for parent in Path(__file__).resolve().parents:
        if (parent / "registry" / "evidence.json").is_file():
            return parent
    return None
