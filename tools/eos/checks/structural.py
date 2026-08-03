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
"""

from __future__ import annotations

import re
from datetime import date, datetime, timedelta
from pathlib import PurePosixPath

from ..findings import Finding
from ..repo import RepoModel
from . import register

DERIVED = {"INDEX.md", "packs/GUIDE_INDEX.md"}
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
SLOT_RE = re.compile(r"\{\{[A-Z_]+\}\}")


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


# --- derived index builders (byte-identical to v1 output) ---------------


def build_index(model: RepoModel) -> str:
    rows = ["---", "summary: Derived index of every file, one row each, grep the tag column",
            "type: index", "tags: [eos]", "derived: true", "---", "",
            "# INDEX", "",
            "Derived file. Edit front-matter, then run",
            "`python tools/eos_check.py --write-index`. One row per file.", "",
            "| path | type | tags | summary | review_by |",
            "| --- | --- | --- | --- | --- |"]
    for rec in model.files:
        if rec.path in DERIVED:
            continue
        if not rec.fm.present:
            continue
        fm = rec.fm.data
        tags = " ".join(fm.get("tags", [])) if isinstance(fm.get("tags"), list) else str(fm.get("tags", ""))
        rows.append("| {} | {} | {} | {} | {} |".format(
            rec.path, fm.get("type", ""), tags, fm.get("summary", ""), fm.get("review_by", "")))
    return "\n".join(rows) + "\n"


def build_wargame_index(model: RepoModel) -> str:
    rows = ["---", "summary: Derived index of every decision guide and archived wargame",
            "type: index", "tags: [eos, wargame]", "derived: true", "---", "",
            "# GUIDE_INDEX", "",
            "Derived file. Edit guide front-matter, then run",
            "`python -m tools.eos check --write-index`.", "",
            "| id | question | module | tags | status | review_by |",
            "| --- | --- | --- | --- | --- |  --- |"]
    for rec in model.files:
        if not rec.fm.present or rec.fm.data.get("type") != "wargame":
            continue
        fm = rec.fm.data
        p = PurePosixPath(rec.path)
        wid = p.stem
        m = re.match(r"(WG-[A-Z]+-\d{3})", wid)
        wid = m.group(1) if m else wid
        # v1: <module>/wargames/<id>.md. v2: packs/<pack>/guides/<id>.md.
        module = (p.parent.parent.name
                  if p.parent.name in ("wargames", "guides") else "")
        tags = " ".join(fm.get("tags", [])) if isinstance(fm.get("tags"), list) else ""
        rows.append("| {} | {} | {} | {} | {} | {} |".format(
            wid, fm.get("summary", ""), module, tags, fm.get("status", ""), fm.get("review_by", "")))
    return "\n".join(rows) + "\n"


# --- checks -------------------------------------------------------------


@register("E001")
def check_e001_index_drift(ctx: dict) -> list:
    model: RepoModel = ctx["model"]
    out = []
    want = {
        "INDEX.md": build_index(model),
        "packs/GUIDE_INDEX.md": build_wargame_index(model),
    }
    for rel, want_text in want.items():
        have = model.read(rel)
        if have is None:
            out.append(_err("E001", rel, "missing, run --write-index"))
        elif have != want_text:
            out.append(_err("E001", rel, "stale, run --write-index"))
    return out


def write_indexes(ctx: dict) -> list:
    """Write both derived indexes, then re-verify against a fresh model."""
    model: RepoModel = ctx["model"]
    (model.root / "INDEX.md").write_text(
        build_index(model), encoding="utf-8", newline="\n")
    guide_index = model.root / "packs" / "GUIDE_INDEX.md"
    guide_index.parent.mkdir(parents=True, exist_ok=True)
    guide_index.write_text(
        build_wargame_index(model), encoding="utf-8", newline="\n")
    fresh = RepoModel.load(model.root, today=model.today)
    reverify = dict(ctx)
    reverify["model"] = fresh
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
        if ftype in NEEDS_REVIEW and "review_by" not in fm:
            out.append(_err("E002", rec.path, "type requires review_by"))
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


@register("E005")
def check_e005_wargame_ids(ctx: dict) -> list:
    model: RepoModel = ctx["model"]
    out = []
    wg_defined: set = set()
    for rec in model.files:
        if not rec.fm.present:
            continue
        if rec.fm.data.get("type") != "wargame":
            continue
        stem = PurePosixPath(rec.path).stem
        m = WG_DEF.match(stem)
        if not m:
            out.append(_err("E005", rec.path, "wargame filename lacks a WG-<MOD>-NNN id"))
        else:
            wid = m.group(0)
            if wid in wg_defined:
                out.append(_err("E005", rec.path, f"duplicate wargame id {wid}"))
            wg_defined.add(wid)
    for rec in model.files:
        for ref in sorted(set(WG_REF.findall(strip_code(rec.text)))):
            if ref not in wg_defined and not ref.endswith("-000"):
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
        rb = rec.fm.data.get("review_by", "")
        if not rb:
            continue
        m = re.match(r"(\d{4})-(\d{2})", str(rb))
        if m:
            y, mo = int(m.group(1)), int(m.group(2))
            try:
                first, late = date(y, mo, 1), date(y, mo, 28)
            except ValueError:
                out.append(_err("E006", rec.path, f"review_by not YYYY-MM: {rb}"))
                continue
            if first <= today.replace(day=1) and (y, mo) != (today.year, today.month):
                if late < today:
                    out.append(_warn("E006", rec.path, f"past review_by {rb}, verify before relying"))
        else:
            out.append(_err("E006", rec.path, f"review_by not YYYY-MM: {rb}"))
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
