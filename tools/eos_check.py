#!/usr/bin/env python3
"""eos_check: the EOS's single sanctioned executable. Stdlib only.

Modes:
  --repo         validate this repo (default)
  --seed PATH    validate a compiled seed pack
  --write-index  regenerate INDEX.md and doctrine/WARGAME_INDEX.md

Checks (stable IDs, cited by the three-strikes rule):
  E001 index drift          E002 front-matter schema   E003 AGENTS==CLAUDE
  E004 voice tells          E005 wargame IDs           E006 review_by expiry
  E007 line budgets         E008 slots and markers     E009 tag vocabulary
  E010 stale active_session

Exit codes: 0 clean or warnings only, 1 errors, 2 cannot run.
The artefact-type list mirrors GOVERNANCE.md; the tag vocabulary is
parsed from GOVERNANCE.md so governance stays the single source.
"""

import argparse
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DERIVED = {"INDEX.md", "doctrine/WARGAME_INDEX.md"}
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

errors, warnings = [], []


def err(check, path, msg):
    errors.append(f"{check} {path}: {msg}")


def warn(check, path, msg):
    warnings.append(f"{check} {path}: {msg}")


def md_files(root):
    for p in sorted(root.rglob("*.md")):
        if ".git" in p.parts:
            continue
        yield p


def read(path):
    return path.read_text(encoding="utf-8", errors="replace")


def front_matter(text):
    """Parse the leading YAML block. Returns (dict, body) or (None, text)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text
    fm, i = {}, 1
    while i < len(lines) and lines[i].strip() != "---":
        line = lines[i]
        m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            if val.startswith("[") and val.endswith("]"):
                items = [v.strip() for v in val[1:-1].split(",") if v.strip()]
                fm[key] = items
            else:
                fm[key] = val
        i += 1
    body = "\n".join(lines[i + 1:])
    return fm, body


def strip_code(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


def parse_tags_vocabulary():
    gov = REPO / "GOVERNANCE.md"
    if not gov.exists():
        return None
    text = read(gov)
    m = re.search(r"## Tag vocabulary(.*?)\n## ", text, flags=re.S)
    if not m:
        return None
    return set(re.findall(r"^- `([a-z0-9-]+)`", m.group(1), flags=re.M))


def rel(path):
    return path.relative_to(REPO).as_posix()


def collect(root):
    """Read every md file once: (path, fm, body, text, lines)."""
    out = []
    for p in md_files(root):
        text = read(p)
        fm, body = front_matter(text)
        out.append((p, fm, body, text, text.splitlines()))
    return out


def build_index(files):
    rows = ["---", "summary: Derived index of every file, one row each, grep the tag column",
            "type: index", "tags: [eos]", "derived: true", "---", "",
            "# INDEX", "",
            "Derived file. Edit front-matter, then run",
            "`python tools/eos_check.py --write-index`. One row per file.", "",
            "| path | type | tags | summary | review_by |",
            "| --- | --- | --- | --- | --- |"]
    for p, fm, _, _, _ in files:
        r = rel(p)
        if r in DERIVED:
            continue
        if fm is None:
            continue
        tags = " ".join(fm.get("tags", [])) if isinstance(fm.get("tags"), list) else str(fm.get("tags", ""))
        rows.append("| {} | {} | {} | {} | {} |".format(
            r, fm.get("type", ""), tags, fm.get("summary", ""), fm.get("review_by", "")))
    return "\n".join(rows) + "\n"


def build_wargame_index(files):
    rows = ["---", "summary: Derived index of every wargame, the surface inception walks",
            "type: index", "tags: [eos, wargame]", "derived: true", "---", "",
            "# WARGAME_INDEX", "",
            "Derived file. Edit wargame front-matter, then run",
            "`python tools/eos_check.py --write-index`.", "",
            "| id | question | module | tags | status | review_by |",
            "| --- | --- | --- | --- | --- |  --- |"]
    for p, fm, _, _, _ in files:
        if fm is None or fm.get("type") != "wargame":
            continue
        wid = p.stem
        m = re.match(r"(WG-[A-Z]+-\d{3})", wid)
        wid = m.group(1) if m else wid
        module = p.parent.parent.name if p.parent.name == "wargames" else ""
        tags = " ".join(fm.get("tags", [])) if isinstance(fm.get("tags"), list) else ""
        rows.append("| {} | {} | {} | {} | {} | {} |".format(
            wid, fm.get("summary", ""), module, tags, fm.get("status", ""), fm.get("review_by", "")))
    return "\n".join(rows) + "\n"


def check_repo(write_index=False):
    files = collect(REPO)
    vocab = parse_tags_vocabulary()
    today = date.today()

    # E003 router parity and caps
    a, c = REPO / "AGENTS.md", REPO / "CLAUDE.md"
    if a.exists() and c.exists():
        if a.read_bytes() != c.read_bytes():
            err("E003", "AGENTS.md", "CLAUDE.md is not a byte-identical copy")
    else:
        err("E003", "AGENTS.md", "router file missing")

    wg_defined = set()
    for p, fm, body, text, lines in files:
        r = rel(p)

        # E002 front-matter schema
        if fm is None:
            err("E002", r, "no front-matter block")
            continue
        for key in ("summary", "type", "tags"):
            if key not in fm or not fm[key]:
                err("E002", r, f"missing front-matter key: {key}")
        ftype = fm.get("type", "")
        if ftype and ftype not in TYPES:
            err("E002", r, f"unknown type: {ftype}")
        if ftype in NEEDS_STATUS and "status" not in fm:
            err("E002", r, "type requires status")
        if ftype in NEEDS_REVIEW and "review_by" not in fm:
            err("E002", r, "type requires review_by")

        # E009 tag vocabulary
        if vocab is not None and isinstance(fm.get("tags"), list):
            for t in fm["tags"]:
                if t not in vocab:
                    err("E009", r, f"tag not in GOVERNANCE vocabulary: {t}")

        # E004 voice tells (skip code)
        prose = strip_code(text)
        if "—" in prose:
            err("E004", r, "em-dash found")
        if re.search(r"[A-Za-z]![\s\"')\]]|[A-Za-z]!$", prose, flags=re.M):
            warn("E004", r, "exclamation mark in prose")
        low = prose.lower()
        for cliche in CLICHES:
            if cliche in low:
                warn("E004", r, f"possible cliche: {cliche}")

        # E005 wargame IDs
        if ftype == "wargame":
            m = WG_DEF.match(p.stem)
            if not m:
                err("E005", r, "wargame filename lacks a WG-<MOD>-NNN id")
            else:
                wid = m.group(0)
                if wid in wg_defined:
                    err("E005", r, f"duplicate wargame id {wid}")
                wg_defined.add(wid)

        # E006 review_by expiry
        rb = fm.get("review_by", "")
        if rb:
            m = re.match(r"(\d{4})-(\d{2})", str(rb))
            if m:
                y, mo = int(m.group(1)), int(m.group(2))
                if date(y, mo, 1) <= today.replace(day=1) and (y, mo) != (today.year, today.month):
                    if date(y, mo, 28) < today:
                        warn("E006", r, f"past review_by {rb}, verify before relying")
            else:
                err("E006", r, f"review_by not YYYY-MM: {rb}")

        # E007 line budgets
        n = len(lines)
        if r in ROUTERS and n > ROUTER_CAP:
            err("E007", r, f"router is {n} lines, cap {ROUTER_CAP}")
        if ftype in BUDGET_TYPES and n > BUDGET:
            if "length_waiver" in fm:
                warn("E007", r, f"{n} lines under waiver: {fm['length_waiver']}")
            else:
                err("E007", r, f"{n} lines over the {BUDGET} budget, no length_waiver")

        # E008 unfilled slots outside templates (repo mode; slots inside
        # code spans are documentation of the syntax, not unfilled slots)
        if not fm.get("template") and r not in DERIVED:
            if re.search(r"\{\{[A-Z_]+\}\}", strip_code(body)):
                err("E008", r, "unfilled {{SLOT}} outside a template")

    # E005 second pass: unresolved references
    for p, fm, body, text, lines in files:
        for ref in set(WG_REF.findall(strip_code(text))):
            if ref not in wg_defined and not ref.endswith("-000"):
                warn("E005", rel(p), f"reference to undefined wargame {ref}")

    # E010 stale active_session
    state = REPO / "org" / "STATE.md"
    if state.exists():
        m = re.search(r"^active_session:\s*(.+)$", read(state), flags=re.M)
        if m and m.group(1).strip().lower() != "none":
            d = re.search(r"(\d{4}-\d{2}-\d{2})", m.group(1))
            if d:
                when = datetime.strptime(d.group(1), "%Y-%m-%d").date()
                if when < today - timedelta(days=1):
                    warn("E010", "org/STATE.md", f"active_session set since {when}, likely stale")
            else:
                warn("E010", "org/STATE.md", "active_session set with no date")

    # E001 index drift
    idx, widx = REPO / "INDEX.md", REPO / "doctrine" / "WARGAME_INDEX.md"
    want_idx, want_widx = build_index(files), build_wargame_index(files)
    if write_index:
        idx.write_text(want_idx, encoding="utf-8", newline="\n")
        widx.write_text(want_widx, encoding="utf-8", newline="\n")
        print("indexes written")
        return finish()
    for path, want in ((idx, want_idx), (widx, want_widx)):
        if not path.exists():
            err("E001", rel(path), "missing, run --write-index")
        elif read(path) != want:
            err("E001", rel(path), "stale, run --write-index")
    return finish()


LOCKBOOK_KEYS = ("eos_version", "eos_commit", "scale", "stack")
RULING_ROW = re.compile(r"^\s*-\s+WG-[A-Z]+-\d{3}\s*·")
RULING_OK = re.compile(r"^\s*-\s+WG-[A-Z]+-\d{3}\s*·.+?·\s*(argued|inherited)\s*·")


def parse_matrix():
    """Parse kernel/SCALE_MATRIX.md. Returns (required, addons) where
    required maps scale -> [paths] and addons maps name -> [paths]."""
    path = REPO / "kernel" / "SCALE_MATRIX.md"
    if not path.exists():
        return None, None
    text = read(path)
    required = {"S": [], "M": [], "L": []}
    row = re.compile(
        r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(x?)\s*\|\s*(x?)\s*\|\s*(x?)\s*\|",
        re.M)
    for m in row.finditer(text):
        fpath = m.group(1)
        if fpath in ("path", "---") or fpath.startswith("-"):
            continue
        for scale, mark in zip(("S", "M", "L"), m.groups()[2:]):
            if mark == "x":
                required[scale].append(fpath)
    addons = {}
    addon_row = re.compile(
        r"^\|\s*([a-z][a-z0-9-]*)\s*\|\s*([^|]+?)\s*\|\s*[^|]+\|\s*[^|]+\|",
        re.M)
    for m in addon_row.finditer(text):
        name, fpath = m.group(1), m.group(2)
        if name in ("addon", "path"):
            continue
        # only enforce path-like cells; prose cells describe row edits
        if " " not in fpath and "/" in fpath:
            addons.setdefault(name, []).append(fpath)
        else:
            addons.setdefault(name, [])
    return required, addons


def check_seed(seed_root):
    seed = Path(seed_root).resolve()
    if not seed.exists():
        print(f"seed path not found: {seed}")
        return 2
    required, addon_files = parse_matrix()
    if required is None:
        print("kernel/SCALE_MATRIX.md missing; cannot check a seed")
        return 2

    def srel(p):
        return p.relative_to(seed).as_posix()

    seed_md = [p.relative_to(seed).as_posix() for p in md_files(seed)]

    # lock-book header (rubric A2, A3)
    scale, addons = None, []
    lb = seed / "docs" / "LOCKBOOK.md"
    if lb.exists():
        text = read(lb)
        fm, _ = front_matter(text)
        if fm is None:
            err("E002", "docs/LOCKBOOK.md", "no front-matter block")
        else:
            for key in LOCKBOOK_KEYS:
                if not fm.get(key):
                    err("E002", "docs/LOCKBOOK.md", f"header missing {key}")
            scale = fm.get("scale")
            if scale not in ("S", "M", "L"):
                err("E002", "docs/LOCKBOOK.md", f"scale must be S, M or L: {scale}")
                scale = None
            raw = re.match(r"\A---\n(.*?)\n---", text, flags=re.S)
            if raw:
                for line in raw.group(1).splitlines():
                    if RULING_ROW.match(line) and not RULING_OK.match(line):
                        err("E002", "docs/LOCKBOOK.md",
                            f"ruling row not marked argued or inherited: {line.strip()}")
            if isinstance(fm.get("addons"), list):
                addons = fm["addons"]

    # per-file checks (rubric A1, A4, A5)
    for p in md_files(seed):
        r = srel(p)
        text = read(p)
        fm, _ = front_matter(text)
        if fm is None:
            err("E002", r, "no front-matter block")
        if re.search(r"\{\{[A-Z_]+\}\}", text):
            err("E008", r, "unfilled {{SLOT}} in compiled seed")
        if re.search(r"<!--\s*scale:", text):
            err("E008", r, "leftover scale marker in compiled seed")

    # router parity and cap (rubric A9, A10)
    a, c = seed / "AGENTS.md", seed / "CLAUDE.md"
    if a.exists() and c.exists():
        if a.read_bytes() != c.read_bytes():
            err("E003", "AGENTS.md", "CLAUDE.md is not a byte-identical copy")
        n = len(read(a).splitlines())
        if n > ROUTER_CAP:
            err("E007", "AGENTS.md", f"compiled router is {n} lines, cap {ROUTER_CAP}")

    # required files per scale (rubric A6)
    if scale:
        for fpath in required[scale]:
            if not (seed / fpath).exists():
                err("E008", fpath, f"required at scale {scale}, missing")

    # add-ons named in the lock-book (rubric A7)
    for name in addons:
        if name not in (addon_files or {}):
            err("E008", "docs/LOCKBOOK.md", f"addon not in SCALE_MATRIX: {name}")
            continue
        for fpath in addon_files[name]:
            if "<" in fpath:
                import fnmatch
                pattern = re.sub(r"<[^>]+>", "*", fpath)
                if not fnmatch.filter(seed_md, pattern):
                    err("E008", fpath, f"addon {name} file missing (pattern)")
            elif not (seed / fpath).exists():
                err("E008", fpath, f"addon {name} file missing")

    # compile-report ancestry (rubric A8)
    cr = seed / "docs" / "COMPILE_REPORT.md"
    if cr.exists() and scale:
        text = read(cr)
        listed = set()
        for m in re.finditer(r"^\|\s*([^|]+?)\s*\|\s*[^|]+?\s*\|", text, flags=re.M):
            cell = m.group(1)
            if cell not in ("file", "---") and not cell.startswith("-"):
                listed.add(cell)
        for fpath in required[scale]:
            if fpath == "docs/COMPILE_REPORT.md":
                continue
            if fpath not in listed:
                err("E008", "docs/COMPILE_REPORT.md", f"ancestry missing for {fpath}")
        for cell in sorted(listed):
            if "/" in cell or cell.endswith(".md"):
                if not (seed / cell).exists():
                    err("E008", "docs/COMPILE_REPORT.md", f"report names absent file {cell}")
    return finish()


def finish():
    for e in errors:
        print(f"ERROR {e}")
    for w in warnings:
        print(f"warn  {w}")
    print(f"{len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


def main():
    ap = argparse.ArgumentParser(description="EOS repo and seed checks")
    ap.add_argument("--repo", action="store_true", help="check this repo (default)")
    ap.add_argument("--seed", metavar="PATH", help="check a compiled seed pack")
    ap.add_argument("--write-index", action="store_true", help="regenerate the indexes")
    args = ap.parse_args()
    if args.seed:
        return check_seed(args.seed)
    return check_repo(write_index=args.write_index)


if __name__ == "__main__":
    sys.exit(main())
