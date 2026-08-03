"""Seed checks: the v1 A-rubric port plus the D-series.

run_seed(seed_root, ctx) validates a compiled seed pack. The A-rubric
half is a semantic port of tools/eos_check.py check_seed and keeps the
v1 check ids (E002, E003, E007, E008) so the rubric table in
kernel/SEED_RUBRIC.md still reads true. The D-series is new in v2:

- D001 schema-level front-matter: summary, type and tags present,
  compiled_from present, template and extracted_from keys absent.
- D002 every compiled_from target exists at the pinned eos_commit
  (gitfacts against the EOS repo); when the commit is unavailable the
  check degrades to a worktree existence check and warns once.
- D003 negative matrix: a file the ruled scale does not require, that
  no named add-on supplies, that the compile report does not mark
  authored, normalised or preserved, and that sits outside the Genesis
  directories, is an error.
- D004 every 'set at first build' deferral must have an open queue
  item scheduling the first-build lock-in (the queue file is
  docs/WORKLOG.md at S, org/QUEUE.md at M, org/work/NEXT.md at L).
- D005 the matrix's empty directories exist at the ruled scale.
- D006 every WG id the lock-book cites resolves in the pinned EOS
  (worktree fallback when the commit is unavailable, with a warning).

ctx is the standard check context: {root (the EOS repo), today,
offline}. A missing seed path or missing SCALE_MATRIX is reported as
an error finding; the CLI maps that shape to exit 2.
"""

from __future__ import annotations

import fnmatch
import re
from pathlib import Path, PurePosixPath

from .. import gitfacts
from ..findings import Finding, Findings
from ..frontmatter import parse
from ..repo import SKIP_DIRS

LOCKBOOK_KEYS = ("eos_version", "eos_commit", "scale", "stack")
ROUTER_CAP = 40
RULING_ROW = re.compile(r"^\s*-\s+WG-[A-Z]+-\d{3}\s*·")
RULING_OK = re.compile(r"^\s*-\s+WG-[A-Z]+-\d{3}\s*·.+?·\s*(argued|inherited)\s*·")
SLOT_RE = re.compile(r"\{\{[A-Z_]+\}\}")
SCALE_FENCE_RE = re.compile(r"<!--\s*scale:")
WG_REF = re.compile(r"\bWG-[A-Z]+-\d{3}\b")
DEFERRAL = "set at first build"
QUEUE_FILE = {"S": "docs/WORKLOG.md", "M": "org/QUEUE.md", "L": "org/work/NEXT.md"}
LOCKIN_RE = re.compile(r"first[ -]build|lock-in", re.I)


def parse_matrix(eos_root) -> tuple:
    """Parse kernel/SCALE_MATRIX.md: (required, addons, empty_dirs).

    required maps scale -> [paths]; addons maps name -> [paths or
    patterns]; empty_dirs maps scale -> [dir paths] from the
    'Directories created empty' section (L includes M's, per 'L adds').
    Returns (None, None, None) when the matrix file is absent.
    """
    path = Path(eos_root) / "kernel" / "SCALE_MATRIX.md"
    if not path.is_file():
        return None, None, None
    text = path.read_text(encoding="utf-8", errors="replace")
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
    addons: dict = {}
    addon_row = re.compile(
        r"^\|\s*([a-z][a-z0-9-]*)\s*\|\s*([^|]+?)\s*\|\s*[^|]+\|\s*[^|]+\|",
        re.M)
    for m in addon_row.finditer(text):
        name, fpath = m.group(1), m.group(2)
        if name in ("addon", "path"):
            continue
        if " " not in fpath and "/" in fpath:
            addons.setdefault(name, []).append(fpath)
        else:
            addons.setdefault(name, [])
    empty_dirs = {"S": [], "M": [], "L": []}
    dm = re.search(r"## Directories created empty\n(.*?)(?=\n## |\Z)", text, re.S)
    if dm:
        section = dm.group(1)
        cut = section.find("L adds:")
        m_part = section if cut < 0 else section[:cut]
        l_part = "" if cut < 0 else section[cut:]
        m_dirs = re.findall(r"`([^`]+/)`", m_part)
        l_dirs = re.findall(r"`([^`]+/)`", l_part)
        empty_dirs["M"] = m_dirs
        empty_dirs["L"] = m_dirs + l_dirs
    return required, addons, empty_dirs


def _md_files(seed: Path) -> list:
    out = []
    for p in sorted(seed.rglob("*.md")):
        if SKIP_DIRS.intersection(p.parts):
            continue
        out.append(p)
    return out


def _ancestry(report_text: str) -> dict:
    """Compile-report ancestry rows: file -> source cell."""
    rows: dict = {}
    for m in re.finditer(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|", report_text, flags=re.M):
        cell = m.group(1)
        if cell not in ("file", "---") and not cell.startswith("-"):
            rows[cell] = m.group(2).strip()
    return rows


def run_seed(seed_root, ctx: dict) -> Findings:
    findings = Findings()
    seed = Path(seed_root).resolve()
    eos_root = Path(ctx["root"])
    if not seed.exists():
        findings.add(Finding("D001", "error", str(seed_root), "seed path not found"))
        return findings
    required, addon_files, empty_dirs = parse_matrix(eos_root)
    if required is None:
        findings.add(Finding("D003", "error", "kernel/SCALE_MATRIX.md",
                             "missing; cannot check a seed"))
        return findings

    def srel(p: Path) -> str:
        return p.relative_to(seed).as_posix()

    err = lambda check, path, msg: findings.add(Finding(check, "error", path, msg))
    warn = lambda check, path, msg: findings.add(Finding(check, "warn", path, msg))

    files = [(srel(p), p.read_text(encoding="utf-8", errors="replace")) for p in _md_files(seed)]
    parsed = [(r, text, parse(text)) for r, text in files]
    seed_md = [r for r, _ in files]

    # --- lock-book header (rubric A2, A3) ------------------------------
    scale, addons, eos_commit = None, [], None
    lockbook_text = None
    lb = seed / "docs" / "LOCKBOOK.md"
    if lb.exists():
        lockbook_text = lb.read_text(encoding="utf-8", errors="replace")
        fm = parse(lockbook_text)
        if not fm.present:
            err("E002", "docs/LOCKBOOK.md", "no front-matter block")
        else:
            for key in LOCKBOOK_KEYS:
                if not fm.data.get(key):
                    err("E002", "docs/LOCKBOOK.md", f"header missing {key}")
            scale = fm.data.get("scale")
            if scale not in ("S", "M", "L"):
                err("E002", "docs/LOCKBOOK.md", f"scale must be S, M or L: {scale}")
                scale = None
            eos_commit = fm.data.get("eos_commit") or None
            raw = re.match(r"\A---\n(.*?)\n---", lockbook_text, flags=re.S)
            if raw:
                for line in raw.group(1).splitlines():
                    if RULING_ROW.match(line) and not RULING_OK.match(line):
                        err("E002", "docs/LOCKBOOK.md",
                            f"ruling row not marked argued or inherited: {line.strip()}")
            if isinstance(fm.data.get("addons"), list):
                addons = fm.data["addons"]

    # --- pinned-commit availability (shared by D002 and D006) ----------
    pin_available = bool(eos_commit) and gitfacts.rev_parse(eos_root, eos_commit) is not None
    if eos_commit and not pin_available:
        warn("D002", "docs/LOCKBOOK.md",
             f"eos_commit {eos_commit} not in the EOS history, degrading to worktree checks")

    # --- per-file checks (rubric A1, A4, A5; D001; D002) ---------------
    for r, text, fm in parsed:
        if not fm.present:
            err("E002", r, "no front-matter block")
        if SLOT_RE.search(text):
            err("E008", r, f"unfilled {{{{SLOT}}}} in compiled seed")
        if SCALE_FENCE_RE.search(text):
            err("E008", r, "leftover scale marker in compiled seed")

        if fm.present:
            for key in ("summary", "type", "tags"):
                if key not in fm.data or not fm.data[key]:
                    err("D001", r, f"missing front-matter key: {key}")
            if not fm.data.get("compiled_from"):
                err("D001", r, "missing compiled_from")
            for forbidden in ("template", "extracted_from"):
                if forbidden in fm.data:
                    err("D001", r, f"forbidden key in a compiled seed: {forbidden}")
            source = fm.data.get("compiled_from", "")
            if isinstance(source, str) and "/" in source:
                if pin_available:
                    if not gitfacts.object_exists(eos_root, f"{eos_commit}:{source}"):
                        err("D002", r,
                            f"compiled_from {source} absent at eos_commit {eos_commit}")
                elif not (eos_root / source).is_file():
                    err("D002", r, f"compiled_from {source} absent from the EOS worktree")

    # --- router parity and cap (rubric A9, A10) ------------------------
    a, c = seed / "AGENTS.md", seed / "CLAUDE.md"
    if a.exists() and c.exists():
        if a.read_bytes() != c.read_bytes():
            err("E003", "AGENTS.md", "CLAUDE.md is not a byte-identical copy")
        n = len(a.read_text(encoding="utf-8", errors="replace").splitlines())
        if n > ROUTER_CAP:
            err("E007", "AGENTS.md", f"compiled router is {n} lines, cap {ROUTER_CAP}")

    # --- required files per scale (rubric A6) --------------------------
    if scale:
        for fpath in required[scale]:
            if not (seed / fpath).exists():
                err("E008", fpath, f"required at scale {scale}, missing")

    # --- add-ons named in the lock-book (rubric A7) --------------------
    addon_allowed: set = set()
    for name in addons:
        if name not in (addon_files or {}):
            err("E008", "docs/LOCKBOOK.md", f"addon not in SCALE_MATRIX: {name}")
            continue
        for fpath in addon_files[name]:
            if "<" in fpath:
                pattern = re.sub(r"<[^>]+>", "*", fpath)
                hits = fnmatch.filter(seed_md, pattern)
                if not hits:
                    err("E008", fpath, f"addon {name} file missing (pattern)")
                addon_allowed.update(hits)
            else:
                if not (seed / fpath).exists():
                    err("E008", fpath, f"addon {name} file missing")
                addon_allowed.add(fpath)

    # --- compile-report ancestry (rubric A8) ---------------------------
    ancestry: dict = {}
    cr = seed / "docs" / "COMPILE_REPORT.md"
    if cr.exists():
        report_text = cr.read_text(encoding="utf-8", errors="replace")
        ancestry = _ancestry(report_text)
        if scale:
            for fpath in required[scale]:
                if fpath == "docs/COMPILE_REPORT.md":
                    continue
                if fpath not in ancestry:
                    err("E008", "docs/COMPILE_REPORT.md", f"ancestry missing for {fpath}")
            for cell in sorted(ancestry):
                if "/" in cell or cell.endswith(".md"):
                    if not (seed / cell).exists():
                        err("E008", "docs/COMPILE_REPORT.md", f"report names absent file {cell}")

    # --- D003 negative matrix ------------------------------------------
    if scale:
        authored = {f for f, source in ancestry.items()
                    if source.split()[0].lower() in ("authored", "normalised", "preserved")}
        genesis = tuple((empty_dirs or {}).get(scale, []))
        for r in seed_md:
            if r in required[scale] or r in addon_allowed or r in authored:
                continue
            if genesis and r.startswith(genesis):
                continue
            err("D003", r, f"not required at scale {scale}, "
                           "not an add-on, not marked authored in the compile report")

    # --- D004 deferrals need an open queue item ------------------------
    if scale:
        queue_rel = QUEUE_FILE[scale]
        queue_path = seed / queue_rel
        queue_text = queue_path.read_text(encoding="utf-8", errors="replace") \
            if queue_path.is_file() else None
        scheduled = bool(queue_text) and bool(LOCKIN_RE.search(queue_text))
        for r, text, _fm in parsed:
            if r == "docs/COMPILE_REPORT.md":
                continue
            if DEFERRAL not in text:
                continue
            if queue_text is None:
                err("D004", r, f"'{DEFERRAL}' deferrals but the queue file {queue_rel} is missing")
            elif not scheduled:
                err("D004", r, f"'{DEFERRAL}' deferral has no open queue item "
                               f"for the first-build lock-in in {queue_rel}")

    # --- D005 matrix empty directories exist ---------------------------
    if scale:
        for d in (empty_dirs or {}).get(scale, []):
            if not (seed / d).is_dir():
                err("D005", d, f"directory required empty at scale {scale}, missing")

    # --- D006 lock-book WG ids resolve in the pinned EOS ---------------
    if lockbook_text:
        if pin_available:
            names = {PurePosixPath(p).name for p in gitfacts.ls_tree(eos_root, eos_commit)}
            where = f"eos_commit {eos_commit}"
        else:
            names = {p.name for p in eos_root.rglob("WG-*.md")
                     if not SKIP_DIRS.intersection(p.parts)}
            where = "the EOS worktree"
            if lockbook_text and WG_REF.search(lockbook_text) and eos_commit is None:
                warn("D006", "docs/LOCKBOOK.md",
                     "no eos_commit pin, resolving WG ids against the worktree")
        for wid in sorted(set(WG_REF.findall(lockbook_text))):
            if not any(name.startswith(wid) for name in names):
                err("D006", "docs/LOCKBOOK.md",
                    f"ruling cites {wid}, which does not resolve in {where}")
    return findings
