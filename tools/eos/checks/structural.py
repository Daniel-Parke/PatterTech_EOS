"""Structural checks E001-E009 and E011.

E010 warned that `active_session` in org/STATE.md was stale. The v2
state view has no such line, so the check could never fire and was
withdrawn. The id is not reused.

The tag vocabulary is parsed live from GOVERNANCE.md so governance
stays the single source. Fixture files (benchmark/fixtures/,
benchmark/holdout/) run the full E-series: they are v1-era by design
and exempt from the v2 semantics, not from structure.

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
from datetime import date
from pathlib import PurePosixPath

from ..findings import Finding
from ..repo import RepoModel
from . import register

DERIVED = {
    "INDEX.md", "packs/INDEX.md", "packs/GUIDE_INDEX.md",
    "packs/DOCTRINE_INDEX.md", "packs/WARGAME_INDEX.md",
    "registry/DOCTRINE_PRESSURE_MATRIX.md", "registry/ID_ALIASES.md",
}
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
NEEDS_STATUS = {"decision", "stack", "registry"}
NEEDS_REVIEW = {"wargame", "stack", "registry", "guide"}
CLICHES = [
    "delve", "empower", "seamless", "leverage", "unlock", "revolutioni",
    "supercharge", "game-chang", "cutting-edge", "elevat",
]
# Digits included: the kernel ships {{SUCCESS_90}}, and a pattern of
# [A-Z_]+ let it through a green seed check unfilled. Reported by
# Venture C's cold-start probe, 2026-07-15, and harvested 2026-08-08.
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
    return "\n".join([
        "---",
        "summary: Compatibility pointer from the retired Guide name to the unified Wargame index",
        "type: index",
        "tags: [eos, wargame]",
        "derived: true",
        "---",
        "",
        "# GUIDE_INDEX",
        "",
        "Guide is the retired public name for this surface. Existing `GD-*`",
        "identities and `guides/` paths remain stable, but every live decision",
        "procedure is a Wargame. Use [WARGAME_INDEX](WARGAME_INDEX.md).",
        "",
    ])


def build_doctrine_index(model: RepoModel, resolver=None) -> str:
    from ..ontology import KnowledgeResolver

    resolver = resolver or KnowledgeResolver.open(model.root)
    rows = ["---", "summary: Derived catalogue of every atomic Doctrine and its authority",
            "type: index", "tags: [eos]", "derived: true", "---", "",
            "# DOCTRINE_INDEX", "",
            "Derived from the atomic files under each pack. Edit a Doctrine",
            "record, then run `python -m tools.eos check --write-index`.", "",
            "| id | authority | standing statement | applies when | challenge triggers | pack | review |",
            "| --- | --- | --- | --- | --- | --- | --- |"]
    for row in resolver.list("doctrine"):
        data = row.metadata
        pack = PurePosixPath(row.path).parts[1]
        rows.append("| {} | {} | {} | {} | {} | {} | {} |".format(
            row.canonical_id, _cell(data.get("authority")),
            _cell(data.get("statement")), _cell(data.get("applies_when")),
            _cell(data.get("challenge_triggers")), pack,
            _cell(data.get("review"))))
    rows += ["", f"{len(resolver.list('doctrine'))} live Doctrine atoms."]
    return "\n".join(rows) + "\n"


def build_wargame_index(model: RepoModel, resolver=None) -> str:
    from ..ontology import KnowledgeResolver

    resolver = resolver or KnowledgeResolver.open(model.root)
    rows = ["---", "summary: Derived public index of every unified Wargame",
            "type: index", "tags: [eos, wargame]", "derived: true", "---", "",
            "# WARGAME_INDEX", "",
            "`GD-*` and `WG-*` are immutable identities of the same semantic",
            "type. New Wargames use `WG-*`; historical paths stay where they are.",
            "This view is derived from their metadata.", "",
            "| id | question | modes | Doctrine or gap | engages when | consequence | pack | review |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for row in resolver.list("wargame"):
        data = row.metadata
        parts = PurePosixPath(row.path).parts
        pack = parts[1] if parts and parts[0] == "packs" else "inception"
        doctrine_or_gap = data.get("applicable_doctrines") or data.get("gap_domain")
        rows.append("| {} | {} | {} | {} | {} | {} | {} | {} |".format(
            row.canonical_id, _cell(data.get("summary")),
            _cell(data.get("scenario_modes")), _cell(doctrine_or_gap),
            _cell(data.get("engages_when")), _cell(data.get("consequence")),
            pack, _cell(data.get("review"))))
    rows += ["", f"{len(resolver.list('wargame'))} live Wargames."]
    return "\n".join(rows) + "\n"


def build_pressure_matrix(model: RepoModel, resolver=None) -> str:
    from ..ontology import KnowledgeResolver

    resolver = resolver or KnowledgeResolver.open(model.root)
    coverage: dict[str, list[str]] = {}
    for row in resolver.list("wargame"):
        for pressure in row.metadata.get("engages_when") or []:
            coverage.setdefault(str(pressure), []).append(row.canonical_id)
    rows = ["---", "summary: Derived estate view of Doctrine relations and Wargame pressure coverage",
            "type: registry", "tags: [eos, wargame]", "status: active",
            "review_by: 2027-02", "derived: true", "---", "",
            "# DOCTRINE_PRESSURE_MATRIX", "",
            "Derived from Doctrine, DREL and Wargame metadata. It is a view, not",
            "a second relation registry.", "", "## Typed relations", ""]
    if not resolver.relations:
        rows += ["No live typed relations.", ""]
    else:
        rows += ["| id | owner | relation | target | conditions | status | Wargame | fallback |",
                 "| --- | --- | --- | --- | --- | --- | --- | --- |"]
        for relation in sorted(resolver.relations, key=lambda row: str(row.get("id"))):
            rows.append("| {} | {} | {} | {} | {} | {} | {} | {} |".format(
                _cell(relation.get("id")), _cell(relation.get("owner_doctrine")),
                _cell(relation.get("relation")), _cell(relation.get("target")),
                _cell(relation.get("conditions")), _cell(relation.get("status")),
                _cell(relation.get("wargame")), _cell(relation.get("fallback"))))
        rows.append("")
    rows += ["## Pressure coverage", "",
             "| pressure | covering Wargames |",
             "| --- | --- |"]
    for pressure in sorted(coverage):
        rows.append("| {} | {} |".format(
            pressure, _cell(sorted(coverage[pressure]))))
    challenged = {
        str(trigger): []
        for row in resolver.list("doctrine")
        for trigger in row.metadata.get("challenge_triggers") or []
    }
    for pressure, wargames in coverage.items():
        if pressure in challenged:
            challenged[pressure] = wargames
    uncovered = sorted(pressure for pressure, rows_ in challenged.items() if not rows_)
    rows += ["", "## Uncovered Doctrine challenge triggers", ""]
    rows += ([", ".join(uncovered)] if uncovered else ["None."])
    return "\n".join(rows).rstrip("\n") + "\n"


def build_alias_view(model: RepoModel) -> str:
    raw = model.read("registry/identifier-aliases.json") or "{}"
    try:
        aliases = json.loads(raw).get("aliases") or {}
    except (ValueError, AttributeError):
        aliases = {}
    rows = ["---", "summary: Derived readable view of immutable knowledge identity aliases",
            "type: registry", "tags: [eos]", "status: active",
            "review_by: 2027-02", "derived: true", "---", "",
            "# ID_ALIASES", "",
            "Derived from `registry/identifier-aliases.json`. Aliases preserve",
            "legacy anchors; they never create a second live definition.", "",
            "| legacy identity or anchor | canonical identity |",
            "| --- | --- |"]
    for old, new in sorted(aliases.items()):
        rows.append("| {} | {} |".format(_cell(old), _cell(new)))
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
                "- **Worked example**: " + ", ".join(f"`{e}`" for e in examples),
                f"- **Evaluation**: {_cell(r.get('evaluation_method'))}",
                f"- **Estate relevance**: {_cell(r.get('estate_relevance'))}",
                f"- **Owner**: {_cell(r.get('owner'))}",
                f"- **Review trigger**: {_cell(r.get('review_trigger'))}",
                "- **Evidence**: {} rows, {}".format(
                    len(r.get("evidence_sources") or []),
                    ", ".join(r.get("evidence_sources") or []) or "none"), ""]
    return "\n".join(out).rstrip("\n") + "\n"


LESSONS_JSON = "registry/lessons.json"
LESSONS_VIEW = "registry/LESSONS.md"

# The lesson row fields, in the order the view renders them, keyed by
# the names kernel/schemas/lesson.schema.json gives them. A key the
# ledger carries that is not listed here is still rendered, after
# these, under its own name: a view that silently drops a field it did
# not expect is how a derived file starts lying about its source.
LESSON_FIELDS = [
    ("lesson", "Lesson"),
    ("origin", "Origin"),
    ("sources", "Evidence"),
    ("lens", "Lens"),
    ("venture", "Venture"),
    ("source_note", "Source note"),
    ("evidence_class", "Evidence class"),
    ("disposition", "Disposition"),
    ("outcome", "Outcome"),
    ("scope", "Scope"),
    ("applicability_conditions", "Applies when"),
    ("informs", "Informs"),
    ("conflicts_with", "Conflicts with"),
    ("conflict_resolutions", "Conflict resolutions"),
    ("supersedes", "Supersedes"),
    ("superseded_by", "Superseded by"),
    ("decided", "Decided"),
    ("reasoning", "Reasoning"),
    ("review", "Review"),
    ("expires", "Expires"),
    ("revisit_trigger", "Revisit when"),
    ("pruned_on", "Pruned"),
]
# id and title are the heading, so they are not repeated as fields.
LESSON_SKIP = {"id", "title"}
# Sections. Rejections and deferrals are kept and shown, because a
# decline that leaves no trace can be re-proposed for ever, which is
# the gap ADR-0006 decision 3 closes. A pruned row is provenance: its
# rule text lives in the file named beside it and not here as well.
LESSON_SECTIONS = ("Live", "Rejected", "Deferred", "Pruned")


def _lesson_section(row: dict) -> str:
    if row.get("pruned_on"):
        return "Pruned"
    disposition = str(row.get("disposition") or "").strip()
    if disposition == "rejected":
        return "Rejected"
    if disposition == "deferred":
        return "Deferred"
    return "Live"


def _lesson_value(value) -> str:
    """One rendered field value: lists joined, mappings spelled out."""
    if isinstance(value, dict):
        return "; ".join(f"{k}: {_lesson_value(v)}" for k, v in value.items())
    if isinstance(value, list):
        return ", ".join(_lesson_value(v) for v in value)
    if value is None:
        return ""
    return " ".join(str(value).split())


def read_lessons(model: RepoModel) -> tuple:
    """(document, rows) from registry/lessons.json; ({}, []) when absent."""
    raw = model.read(LESSONS_JSON)
    if not raw:
        return {}, []
    try:
        doc = json.loads(raw)
    except ValueError:
        return {}, []
    if isinstance(doc, list):
        return {}, [r for r in doc if isinstance(r, dict)]
    if not isinstance(doc, dict):
        return {}, []
    rows = doc.get("rows") or doc.get("lessons") or doc.get("records") or []
    return doc, [r for r in rows if isinstance(r, dict)]


def build_lessons(model: RepoModel) -> str:
    """The readable view of registry/lessons.json.

    Sections rather than a table, for the reason build_capabilities
    gives: a row carries a dozen fields and a table that fits the page
    fits it by dropping columns. Rows sort by id inside their section,
    so regeneration is byte-stable for unchanged input.

    The ledger's own preamble is emitted verbatim, hard-wrapped by
    whoever wrote it, because the generator does not reflow. It lives
    in the canonical file for the obvious reason: prose that only
    existed here would make the view the only home for it, and the view
    would stop being derived.

    The ledger is canonical; this file is a view of it and is never
    hand-edited.
    """
    doc, rows = read_lessons(model)
    rows = sorted(rows, key=lambda r: str(r.get("id", "")))

    grouped = {name: [] for name in LESSON_SECTIONS}
    for row in rows:
        grouped[_lesson_section(row)].append(row)

    out = ["---",
           "summary: Derived view of the lessons ledger, every row with its disposition and reasoning",
           "type: registry", "tags: [eos]", "status: active",
           f"review: on-change-of:{LESSONS_JSON}",
           "derived: true", "---", "",
           "# LESSONS", "",
           f"Derived from `{LESSONS_JSON}` by",
           "`python -m tools.eos check --write-index`. Do not hand-edit.", "",
           "**Live: {}. Rejected: {}. Deferred: {}. Pruned: {}.** A rejected row"
           .format(*(len(grouped[name]) for name in LESSON_SECTIONS)),
           "stays here with its reason, so the same proposal cannot arrive",
           "twice unrecorded. A pruned row is provenance: its rule text now",
           "lives in the file named beside it.", ""]
    for paragraph in doc.get("preamble") or []:
        out += [str(paragraph).rstrip("\n"), ""]

    for name in LESSON_SECTIONS:
        out += [f"## {name}", ""]
        if not grouped[name]:
            out += [f"No {name.lower()} rows.", ""]
            continue
        for row in grouped[name]:
            title = _lesson_value(row.get("title"))
            heading = str(row.get("id", "(no id)"))
            if title:
                heading = f"{heading} · {title}"
            out += [f"### {heading}", ""]
            rendered = set(LESSON_SKIP)
            for key, label in LESSON_FIELDS:
                if key in row and row[key] not in (None, "", [], {}):
                    out.append(f"- **{label}**: {_lesson_value(row[key])}")
                rendered.add(key)
            for key in sorted(set(row) - rendered):
                if row[key] in (None, "", [], {}):
                    continue
                out.append(f"- **{key}**: {_lesson_value(row[key])}")
            out.append("")
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
    if any(rec.fm.present and rec.fm.data.get("kind") == "doctrine"
           for rec in model.files):
        from ..ontology import KnowledgeResolver
        resolver = KnowledgeResolver.open(model.root)
        want.update({
            "packs/DOCTRINE_INDEX.md": build_doctrine_index(model, resolver),
            "packs/WARGAME_INDEX.md": build_wargame_index(model, resolver),
            "registry/DOCTRINE_PRESSURE_MATRIX.md":
                build_pressure_matrix(model, resolver),
        })
        if model.read("registry/identifier-aliases.json") is not None:
            want["registry/ID_ALIASES.md"] = build_alias_view(model)
    # Only where the matrix exists: the minirepo fixture has no registry.
    if model.read("registry/coverage.json") is not None:
        want["registry/CAPABILITIES.md"] = build_capabilities(model)
    # Only where the ledger exists. registry/lessons.json is canonical
    # from v2.1 and LESSONS.md is its view; before the ledger lands
    # there is nothing to derive the view from and hand-written prose
    # is all there is.
    if model.read(LESSONS_JSON) is not None:
        want[LESSONS_VIEW] = build_lessons(model)
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
    """The shared resolver's identity and archive integrity findings.

    ``GD`` and ``WG`` are both Wargame identities.  The old check inferred
    semantic type from the WG prefix and therefore rejected a correctly
    reclassified GD file.  References are checked once by S004.
    """
    from ..ontology import KnowledgeResolver

    model: RepoModel = ctx["model"]
    resolver = ctx.get("ontology") or KnowledgeResolver.open(model.root)
    out = []
    for rec in model.files:
        if not rec.fm.present:
            continue
        fm = rec.fm.data
        if fm.get("type") != "wargame" and fm.get("kind") != "wargame":
            continue
        if GUIDE_ID.match(PurePosixPath(rec.path).stem) is None:
            out.append(_err(
                "E005", rec.path,
                "wargame filename lacks a GD-<PACK>-NNN or WG-<PACK>-NNN identity",
            ))
    for problem in resolver.problems:
        out.append(_err(
            "E005", problem.path or "registry/identifier-aliases.json",
            problem.message,
        ))
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
    """One budget binds, the rest are defaults (ADR-0008 decision 5).

    The forty-line cap on AGENTS.md and CLAUDE.md stays an error. That
    file sits in every agent's context and its cost is paid on every
    task, so a router over the cap is a bill the whole estate keeps
    paying. Everything else warns: length is caught by the pruning test
    in packs/PACK_SHAPE.md and by the review passes, so a long pack is a
    thing to look at rather than a build failure.

    Both over-budget cases warn, and their messages stay different on
    purpose. A `length_waiver` is no longer the downgrade from error to
    warning; it is the recorded reason for the departure, which is what
    a default asks for and what the monthly pass samples. The two
    messages let a reader tell an argued length from an unexamined one.
    """
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
                out.append(_warn("E007", rec.path,
                                 f"{n} lines under waiver: {fm['length_waiver']}"))
            else:
                out.append(_warn("E007", rec.path,
                                 f"{n} lines over the {BUDGET} budget, "
                                 f"prune it or record a length_waiver"))
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
    """The GOVERNANCE list is the known set, not a wall (ADR-0008 dec 6).

    An unknown tag warns. Either the file wants a tag that is already
    there, or the estate has grown a subject and the list should grow
    with it, and refusing the commit told a writer neither. The warning
    is the prompt to look, and hygiene in the monthly pass is where it
    is settled. The list is still parsed live from GOVERNANCE.md, so
    governance stays the single source for what is known.
    """
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
                    out.append(_warn("E009", rec.path,
                                     f"tag not in GOVERNANCE vocabulary: {t}"))
    return out


VIEWS = ("org/TASKS.md", "org/STATE.md")


@register("E011")
def check_e011_view_drift(ctx: dict) -> list:
    """The derived views agree with the generator that owns them.

    org/TASKS.md and org/STATE.md were declared derived, given a
    generator (`python -m tools.eos task views`) and then compared by
    nothing, which is the same hole packs/INDEX.md sat in: a file that
    says it is generated and is in fact hand-maintained drifts silently
    against a green build.

    The comparison is byte-for-byte up to the state view's machine-facts
    block, and stops there. That block records the branch and the commit
    the view was generated from, and that commit is behind HEAD the
    moment the view is committed, so equality can never hold in a
    repository that keeps moving. S007 already checks those facts, by
    ancestry rather than equality, and this check does not second-guess
    it.

    Only where the repository runs the v2 record model: with no
    org/tasks/ directory there are no canonical records for a view to
    be derived from.
    """
    from .. import taskops

    model: RepoModel = ctx["model"]
    if not (model.root / "org" / "tasks").is_dir():
        return []
    out = []
    texts, problems = taskops.build_views(model.root, git_facts=False)
    if problems:
        # A malformed record or claim file changes what the generator
        # would write, so a drift verdict against it would be noise.
        # Report the unreadable input instead and stop.
        return [_err("E011", f.path, f"cannot compare the derived views: {f.message}")
                for f in problems]
    for rel in VIEWS:
        have = model.read(rel)
        want = texts[rel]
        if have is None:
            out.append(_err("E011", rel, "missing, run task views"))
            continue
        if rel == "org/STATE.md":
            have = taskops.strip_machine_facts(have)
            want = taskops.strip_machine_facts(want)
        if have != want:
            out.append(_err("E011", rel,
                            "stale against its generator, run task views"))
    return out
