"""Structural checks E001-E010, ported from tools/eos_check.py v1.

Parity is a hard gate: over this repository these checks produce
exactly the findings the v1 checker produces (same ids, same paths,
same messages, same severities). Two sanctioned differences:

- E001 write mode (write_indexes) writes the derived indexes and then
  re-verifies them against a freshly loaded model, fixing the v1
  write-without-reverify bug.
- The hardened front-matter parser reports malformed blocks through
  E002 (v1 silently skipped what it could not parse). Well-formed
  repositories, this one included, see no difference.

The tag vocabulary is parsed live from GOVERNANCE.md so governance
stays the single source. Fixture files (benchmark/fixtures/,
benchmark/holdout/) run the full E-series exactly as v1 did.

The derived indexes are scoped to live material. Frozen trees are
checked but never indexed: a benchmark fixture's wargames are not EOS
guidance, and an index that mixes them with the real thing teaches an
agent the wrong law. The three indexes and their sources:

- INDEX.md, every live file with front-matter.
- packs/INDEX.md, the always-loaded activation surface, one row per
  built pack, sourced from PACK.md front-matter and its first
  paragraph.
- packs/GUIDE_INDEX.md, every decision guide under a pack, plus any
  remaining type: wargame file outside one.
"""

from __future__ import annotations

import json
import re
from datetime import date, datetime, timedelta
from pathlib import PurePosixPath

from ..findings import Finding
from ..repo import RepoModel
from . import register

DERIVED = {"INDEX.md", "packs/GUIDE_INDEX.md", "packs/INDEX.md"}
# Frozen trees: checked, never indexed. Indexing them puts archived law
# and benchmark fixtures in front of an agent as if they were current.
# Drill scenarios are fixture material in the same sense: a toy repo a
# cold agent is dropped into, whose files are deliberately incomplete
# and must not be read as EOS prose or held to the front-matter law.
NOT_INDEXED = ("archive/", "benchmark/fixtures/", "benchmark/holdout/",
               "benchmark/drills/scenarios/")
GUIDE_ID = re.compile(r"((?:WG|GD)-[A-Z]+-\d{3})")
ROUTERS = {"AGENTS.md", "CLAUDE.md"}
ROUTER_CAP = 40
BUDGET = 150
BUDGET_TYPES = {"doctrine", "foundation", "pattern", "ux", "implementation", "wargame"}
TYPES = {
    "root", "governance", "decision", "doctrine", "foundation", "pattern",
    "ux", "implementation", "wargame", "template", "example", "registry",
    "stack", "playbook", "org", "kernel", "guide", "index",
}
NEEDS_STATUS = {"wargame", "decision", "stack", "registry"}
NEEDS_REVIEW = {"wargame", "stack", "registry", "guide"}
CLICHES = [
    "delve", "empower", "seamless", "leverage", "unlock", "revolutioni",
    "supercharge", "game-chang", "cutting-edge", "elevat",
]
WG_DEF = re.compile(r"^WG-[A-Z]+-\d{3}")
WG_REF = re.compile(r"\bWG-[A-Z]+-\d{3}\b")
# Digits included: the kernel ships {{SUCCESS_90}}, and a pattern of
# [A-Z_]+ let it through a green seed check unfilled. Reported by Guth's
# cold-start probe, 2026-07-15, and harvested 2026-08-08.
SLOT_RE = re.compile(r"\{\{[A-Z0-9_]+\}\}")


def strip_code(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


def parse_tags_vocabulary(model: RepoModel) -> set | None:
    text = model.read("GOVERNANCE.md")
    if text is None:
        return None
    m = re.search(r"## Tag vocabulary(.*?)\n## ", text, flags=re.S)
    if not m:
        return None
    return set(re.findall(r"^- `([a-z0-9-]+)`", m.group(1), flags=re.M))


def _err(check, path, msg):
    return Finding(check, "error", path, msg)


def _warn(check, path, msg):
    return Finding(check, "warn", path, msg)


def indexable(rec) -> bool:
    """Live material. Frozen trees are checked but never indexed."""
    return not rec.path.startswith(NOT_INDEXED)


def _cell(value) -> str:
    """One table cell: single line, pipes escaped, never breaks the row."""
    if isinstance(value, list):
        value = " ".join(str(v) for v in value)
    return " ".join(str(value or "").split()).replace("|", "\\|")


def _first_paragraph(body: str) -> str:
    """A pack's level-one metadata: the first prose paragraph of PACK.md.

    This is the paragraph PACK_SHAPE.md keeps under eighty words because
    it sits in every agent's context whether the pack loads or not.
    """
    for block in body.split("\n\n"):
        block = block.strip()
        if block and not block.startswith("#"):
            return block
    return ""


def is_guide(rec) -> bool:
    """A decision guide: anything under a pack's guides/, plus any
    remaining type: wargame file that lives outside one."""
    p = PurePosixPath(rec.path)
    under_pack = (len(p.parts) == 4 and p.parts[0] == "packs"
                  and p.parts[2] == "guides")
    return under_pack or rec.fm.data.get("type") == "wargame"


# --- derived index builders ---------------------------------------------


def build_index(model: RepoModel) -> str:
    rows = ["---", "summary: Derived index of every live file, one row each, grep the tag column",
            "type: index", "tags: [eos]", "derived: true", "---", "",
            "# INDEX", "",
            "Derived file. Edit front-matter, then run",
            "`python -m tools.eos check --write-index`. One row per live",
            "file. Frozen trees are not indexed.", "",
            "| path | type | tags | summary | review |",
            "| --- | --- | --- | --- | --- |"]
    for rec in model.files:
        if rec.path in DERIVED or not rec.fm.present or not indexable(rec):
            continue
        fm = rec.fm.data
        rows.append("| {} | {} | {} | {} | {} |".format(
            rec.path, _cell(fm.get("type")), _cell(fm.get("tags")),
            _cell(fm.get("summary")),
            _cell(fm.get("review") or fm.get("review_by"))))
    return "\n".join(rows) + "\n"


def build_pack_index(model: RepoModel) -> str:
    """The always-loaded activation surface, one row per built pack.

    A pack directory holding a PACK.md is built by definition: the
    contract forbids stub packs, so presence on disk is the status.
    """
    rows = ["---", "summary: Derived index of every built pack, the always-loaded metadata surface",
            "type: index", "tags: [eos]", "derived: true", "---", "",
            "# PACK INDEX", "",
            "The always-loaded knowledge surface. One row per built pack: what",
            "it covers, the predicates that gate it, and how big its body is.",
            "Nothing else in `packs/` is loaded until a row here activates.", "",
            "Derived file. Edit `PACK.md` front-matter and its first paragraph,",
            "then run `python -m tools.eos check --write-index`.", "",
            "Domains without a pack are not omissions here. Every domain, built",
            "or not, carries an honest row in `registry/CAPABILITIES.md`,",
            "generated from `registry/coverage.json`.", "",
            "| Pack | What it covers, and when it activates | Predicates | Authority | Body lines |",
            "| --- | --- | --- | --- | --- |"]
    packs = []
    for rec in model.files:
        p = PurePosixPath(rec.path)
        if len(p.parts) != 3 or p.parts[0] != "packs" or p.parts[2] != "PACK.md":
            continue
        if not rec.fm.present or not indexable(rec):
            continue
        packs.append(rec)
    total = 0
    for rec in packs:
        fm = rec.fm.data
        body_lines = len(rec.fm.body.strip("\n").splitlines())
        total += body_lines
        rows.append("| `{}` | {} | {} | {} | {} |".format(
            rec.path, _cell(_first_paragraph(rec.fm.body)),
            _cell(fm.get("applies_when")), _cell(fm.get("authority")),
            body_lines))
    rows += ["",
             "{} built packs, {:,} body lines. The pack contract is".format(len(packs), total),
             "`packs/PACK_SHAPE.md`; a domain that cannot meet its definition of",
             "done stays a registry row and is never described as implemented."]
    return "\n".join(rows) + "\n"


def build_guide_index(model: RepoModel) -> str:
    rows = ["---", "summary: Derived index of every decision guide, one fork each",
            "type: index", "tags: [eos, wargame]", "derived: true", "---", "",
            "# GUIDE_INDEX", "",
            "Derived file. Edit guide front-matter, then run",
            "`python -m tools.eos check --write-index`.", "",
            "| id | question | pack | authority | review |",
            "| --- | --- | --- | --- | --- |"]
    for rec in model.files:
        if not rec.fm.present or not indexable(rec) or not is_guide(rec):
            continue
        fm = rec.fm.data
        p = PurePosixPath(rec.path)
        m = GUIDE_ID.match(p.stem)
        gid = m.group(1) if m else p.stem
        module = (p.parent.parent.name
                  if p.parent.name in ("wargames", "guides") else "")
        rows.append("| {} | {} | {} | {} | {} |".format(
            gid, _cell(fm.get("summary")), module,
            _cell(fm.get("authority")), _cell(fm.get("review"))))
    return "\n".join(rows) + "\n"


# --- checks -------------------------------------------------------------


def build_capabilities(model: RepoModel) -> str:
    """The readable view of the domain coverage matrix.

    Every one of the eight required fields is rendered in full. The
    previous view was a six-column table that dropped worked_example,
    evaluation_method, estate_relevance and owner, and truncated what
    was left mid-word. A matrix whose whole job is making omissions
    visible cannot be rendered by cutting four columns off it, so this
    is sections rather than a table: nothing here has to fit.
    """
    raw = model.read("registry/coverage.json")
    rows = []
    if raw:
        try:
            rows = json.loads(raw).get("rows") or []
        except ValueError:
            rows = []
    built = sorted((r for r in rows if r.get("status") == "built"),
                   key=lambda r: r.get("capability", ""))
    only = sorted((r for r in rows if r.get("status") != "built"),
                  key=lambda r: r.get("capability", ""))

    out = ["---", "summary: Derived view of the domain coverage matrix, every field in full",
           "type: registry", "tags: [eos]", "status: active", "review_by: 2027-02",
           "derived: true", "---", "",
           "# CAPABILITIES", "",
           "Derived from `registry/coverage.json` by",
           "`python -m tools.eos check --write-index`. Do not hand-edit.", "",
           f"**Built: {len(built)}. Registry-only: {len(only)}.** A registry-only",
           "row is not coverage, and this view says so first.", ""]

    out += ["## Not built", ""]
    if not only:
        out += ["Every charted capability has a pack.", ""]
    for r in only:
        out += [f"### {r.get('capability', '')}", "",
                f"- **Why not**: {_cell(r.get('reason_if_registry_only'))}",
                f"- **Would activate on**: {_cell(r.get('activation'))}",
                f"- **Estate relevance**: {_cell(r.get('estate_relevance'))}",
                f"- **Evaluation**: {_cell(r.get('evaluation_method'))}",
                f"- **Owner**: {_cell(r.get('owner'))}",
                f"- **Review trigger**: {_cell(r.get('review_trigger'))}", ""]

    out += ["## Built", ""]
    for r in built:
        examples = r.get("worked_example") or []
        out += [f"### {r.get('capability', '')}", "",
                f"- **Pack**: `{_cell(r.get('pack'))}`",
                f"- **Activation**: {_cell(r.get('activation'))}",
                f"- **Worked example**: " + ", ".join(f"`{e}`" for e in examples),
                f"- **Evaluation**: {_cell(r.get('evaluation_method'))}",
                f"- **Estate relevance**: {_cell(r.get('estate_relevance'))}",
                f"- **Owner**: {_cell(r.get('owner'))}",
                f"- **Review trigger**: {_cell(r.get('review_trigger'))}",
                "- **Evidence**: {} rows, {}".format(
                    len(r.get("evidence_sources") or []),
                    ", ".join(r.get("evidence_sources") or []) or "none"), ""]
    return "\n".join(out).rstrip("\n") + "\n"


def _wanted_indexes(model: RepoModel) -> dict:
    """Every derived index and the text it should hold.

    packs/INDEX.md is in here deliberately. It was flagged derived,
    whitelisted as generated and written by hand, so nothing compared it
    and it sat twelve packs short of reality against a green build.
    """
    want = {
        "INDEX.md": build_index(model),
        "packs/INDEX.md": build_pack_index(model),
        "packs/GUIDE_INDEX.md": build_guide_index(model),
    }
    # Only where the matrix exists: the minirepo fixture has no registry.
    if model.read("registry/coverage.json") is not None:
        want["registry/CAPABILITIES.md"] = build_capabilities(model)
    return want


@register("E001")
def check_e001_index_drift(ctx: dict) -> list:
    model: RepoModel = ctx["model"]
    out = []
    for rel, want_text in _wanted_indexes(model).items():
        have = model.read(rel)
        if have is None:
            out.append(_err("E001", rel, "missing, run --write-index"))
        elif have != want_text:
            out.append(_err("E001", rel, "stale, run --write-index"))
    return out


MAX_INDEX_PASSES = 5


def write_indexes(ctx: dict) -> list:
    """Write every derived index to a fixpoint, then re-verify.

    The indexes reference each other: INDEX.md carries one row per live
    file, and registry/CAPABILITIES.md is a live file whose front-matter
    INDEX.md indexes. Writing once in an arbitrary order can therefore
    leave the first file written stale against the last. Iterating to a
    fixpoint costs a few passes over an already-loaded model and removes
    a whole class of ordering bug.
    """
    model: RepoModel = ctx["model"]
    for _ in range(MAX_INDEX_PASSES):
        wrote = False
        for rel, text in _wanted_indexes(model).items():
            path = model.root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            # Compared as bytes, written as bytes. read_text applies
            # universal newlines, so a derived file that git checked
            # out with CRLF read back equal to the LF text we meant to
            # write and was left alone: the generator reported the file
            # correct while its bytes were not the bytes it generates.
            # Harmless for the checks, which normalise, but it makes
            # the derived set platform-dependent and it is exactly the
            # drift E001 exists to catch.
            want_bytes = text.encode("utf-8")
            if not path.is_file() or path.read_bytes() != want_bytes:
                path.write_bytes(want_bytes)
                wrote = True
        model = RepoModel.load(model.root, today=model.today)
        if not wrote:
            break
    reverify = dict(ctx)
    reverify["model"] = model
    return check_e001_index_drift(reverify)


@register("E002")
def check_e002_front_matter(ctx: dict) -> list:
    model: RepoModel = ctx["model"]
    out = []
    for rec in model.files:
        if not rec.fm.present:
            out.append(_err("E002", rec.path, "no front-matter block"))
            if rec.fm.errors:
                for lineno, msg in rec.fm.errors:
                    out.append(_err("E002", rec.path, f"front-matter line {lineno}: {msg}"))
            continue
        for lineno, msg in rec.fm.errors:
            out.append(_err("E002", rec.path, f"front-matter line {lineno}: {msg}"))
        fm = rec.fm.data
        for key in ("summary", "type", "tags"):
            if key not in fm or not fm[key]:
                out.append(_err("E002", rec.path, f"missing front-matter key: {key}"))
        ftype = fm.get("type", "")
        if ftype and ftype not in TYPES:
            out.append(_err("E002", rec.path, f"unknown type: {ftype}"))
        if ftype in NEEDS_STATUS and "status" not in fm:
            out.append(_err("E002", rec.path, "type requires status"))
        # Either spelling satisfies it. review is the v2 axis and the
        # one live files carry; review_by is v1's, still required by the
        # frozen seed fixtures, which must not be edited to suit a
        # checker. Demanding both put two hand-written fields on 149
        # files for one fact, 92 of them with the identical value.
        if ftype in NEEDS_REVIEW and not (fm.get("review") or fm.get("review_by")):
            out.append(_err("E002", rec.path, "type requires review"))
    return out


@register("E003")
def check_e003_router_parity(ctx: dict) -> list:
    root = ctx["model"].root
    a, c = root / "AGENTS.md", root / "CLAUDE.md"
    if a.exists() and c.exists():
        if a.read_bytes() != c.read_bytes():
            return [_err("E003", "AGENTS.md", "CLAUDE.md is not a byte-identical copy")]
        return []
    return [_err("E003", "AGENTS.md", "router file missing")]


@register("E004")
def check_e004_voice_tells(ctx: dict) -> list:
    model: RepoModel = ctx["model"]
    out = []
    for rec in model.files:
        if not rec.fm.present:
            continue
        prose = strip_code(rec.text)
        if "—" in prose:
            out.append(_err("E004", rec.path, "em-dash found"))
        if re.search(r"[A-Za-z]![\s\"')\]]|[A-Za-z]!$", prose, flags=re.M):
            out.append(_warn("E004", rec.path, "exclamation mark in prose"))
        low = prose.lower()
        for cliche in CLICHES:
            if cliche in low:
                out.append(_warn("E004", rec.path, f"possible cliche: {cliche}"))
    return out


def retired_ids(model: RepoModel) -> set:
    """Ids whose defining file was retired to a pushed tag (ADR-0003).

    The id still exists and is still locatable; it is simply not in the
    tree. Without this, retiring archive/v1 turned 33 real ids into 79
    dangling references overnight, and the only alternative was to
    reword every provenance line in the repository.
    """
    raw = model.read("archive/RETIRED_IDS.json")
    if not raw:
        return set()
    try:
        return set(json.loads(raw).get("ids") or {})
    except ValueError:
        return set()


@register("E005")
def check_e005_wargame_ids(ctx: dict) -> list:
    model: RepoModel = ctx["model"]
    out = []
    # Live definitions only, so duplicate detection stays honest. An id
    # that is both live and retired is not a duplicate of itself.
    wg_defined: set = set()
    for rec in model.files:
        if not rec.fm.present:
            continue
        stem = PurePosixPath(rec.path).stem
        m = WG_DEF.match(stem)
        if rec.fm.data.get("type") != "wargame" and not m:
            continue
        if not m:
            out.append(_err("E005", rec.path, "wargame filename lacks a WG-<MOD>-NNN id"))
        else:
            wid = m.group(0)
            if wid in wg_defined:
                out.append(_err("E005", rec.path, f"duplicate wargame id {wid}"))
            wg_defined.add(wid)
    # A reference resolves against live definitions plus ids retired to
    # the tag, which are still defined and still locatable.
    resolvable = wg_defined | retired_ids(model)
    for rec in model.files:
        for ref in sorted(set(WG_REF.findall(strip_code(rec.text)))):
            if ref not in resolvable and not ref.endswith("-000"):
                out.append(_warn("E005", rec.path, f"reference to undefined wargame {ref}"))
    return out


@register("E006")
def check_e006_review_expiry(ctx: dict) -> list:
    model: RepoModel = ctx["model"]
    today = ctx["today"]
    out = []
    for rec in model.files:
        if not rec.fm.present:
            continue
        fm = rec.fm.data
        # review is the v2 axis, review_by v1's. Whichever the file
        # carries is the one checked; carrying both is no longer asked
        # for. The v2 axis also accepts on-change-of:<source> and none,
        # neither of which is a month, so neither is an expiry.
        key = "review" if fm.get("review") else "review_by"
        rb = fm.get(key, "")
        if not rb:
            continue
        value = str(rb).strip()
        if value == "none" or value.startswith("on-change-of:"):
            continue
        m = re.match(r"(\d{4})-(\d{2})", value)
        if m:
            y, mo = int(m.group(1)), int(m.group(2))
            try:
                first, late = date(y, mo, 1), date(y, mo, 28)
            except ValueError:
                out.append(_err("E006", rec.path, f"{key} not YYYY-MM: {rb}"))
                continue
            if first <= today.replace(day=1) and (y, mo) != (today.year, today.month):
                if late < today:
                    out.append(_warn("E006", rec.path, f"past {key} {rb}, verify before relying"))
        else:
            out.append(_err("E006", rec.path, f"{key} not YYYY-MM: {rb}"))
    return out


@register("E007")
def check_e007_line_budgets(ctx: dict) -> list:
    model: RepoModel = ctx["model"]
    out = []
    for rec in model.files:
        if not rec.fm.present:
            continue
        fm = rec.fm.data
        n = rec.lines
        if rec.path in ROUTERS and n > ROUTER_CAP:
            out.append(_err("E007", rec.path, f"router is {n} lines, cap {ROUTER_CAP}"))
        if fm.get("type", "") in BUDGET_TYPES and n > BUDGET:
            if "length_waiver" in fm:
                out.append(_warn("E007", rec.path, f"{n} lines under waiver: {fm['length_waiver']}"))
            else:
                out.append(_err("E007", rec.path, f"{n} lines over the {BUDGET} budget, no length_waiver"))
    return out


@register("E008")
def check_e008_slots(ctx: dict) -> list:
    model: RepoModel = ctx["model"]
    out = []
    for rec in model.files:
        if not rec.fm.present:
            continue
        if rec.fm.data.get("template") or rec.path in DERIVED:
            continue
        if SLOT_RE.search(strip_code(rec.fm.body)):
            out.append(_err("E008", rec.path, "unfilled {{SLOT}} outside a template"))
    return out


@register("E009")
def check_e009_tag_vocabulary(ctx: dict) -> list:
    model: RepoModel = ctx["model"]
    vocab = parse_tags_vocabulary(model)
    if vocab is None:
        return []
    out = []
    for rec in model.files:
        if not rec.fm.present:
            continue
        tags = rec.fm.data.get("tags")
        if isinstance(tags, list):
            for t in tags:
                if t not in vocab:
                    out.append(_err("E009", rec.path, f"tag not in GOVERNANCE vocabulary: {t}"))
    return out


@register("E010")
def check_e010_stale_active_session(ctx: dict) -> list:
    model: RepoModel = ctx["model"]
    today = ctx["today"]
    text = model.read("org/STATE.md")
    if text is None:
        return []
    m = re.search(r"^active_session:\s*(.+)$", text, flags=re.M)
    if not m or m.group(1).strip().lower() == "none":
        return []
    d = re.search(r"(\d{4}-\d{2}-\d{2})", m.group(1))
    if d:
        when = datetime.strptime(d.group(1), "%Y-%m-%d").date()
        if when < today - timedelta(days=1):
            return [_warn("E010", "org/STATE.md", f"active_session set since {when}, likely stale")]
        return []
    return [_warn("E010", "org/STATE.md", "active_session set with no date")]
