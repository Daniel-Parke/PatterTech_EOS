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
  item scheduling the first-build lock-in. The queue surface follows
  the governing matrix: v1 uses docs/WORKLOG.md at S, org/QUEUE.md at
  M and org/work/NEXT.md at L; v2 uses docs/TASKS.md at S and the
  org/tasks/ records at ORG, because org/TASKS.md is a derived view
  and is never seeded.
- D005 the matrix's empty directories exist at the ruled scale. Only a
  v1 matrix declares any: the v2 matrix ships nothing empty, so a v2
  seed passes D005 vacuously. The check is kept because a seed pinned
  to a v1 commit resolves the v1 matrix, and seeds in the estate are
  pinned that way.
- D006 every WG id the lock-book cites resolves in the pinned EOS
  (worktree fallback when the commit is unavailable, with a warning).
- D007 the seed's policy file (per the matrix at the ruled scale)
  parses and validates against kernel/schemas/policy.schema.json.
- D008 the policy's guard section either ships a validated adapter
  mapping or declares every guarded class manual-only by leaving
  validated false or absent (fail closed); claiming autonomous guarded
  actions without a shipped mapping is an error.
- D009 org/claims.json, when the matrix requires it and it is present,
  validates against kernel/schemas/claims.schema.json and carries the
  seeded state: an empty lanes list.
- D010 an ORG seed carries the Genesis template set: one compiled file
  per template in GENESIS_TEMPLATES. Matched on the compiled_from
  source, not on a destination path, so the matrix decides where each
  one lands and this check does not have to agree with it twice. It
  engages only when the governing matrix names a Genesis template at
  all: a seed pinned before those templates existed could not have
  carried them, exactly as D007 to D009 stay quiet against v1 seeds.
- D011 the compiled acceptance spine still carries its expected-fail
  marking and a manifest table with a state column. Compile time is the
  only time this check runs, so it reads the form and nothing else: it
  cannot know whether a suite really fails, and it does not claim to.

The scale matrix that governs a seed is the one at the seed's pinned
eos_commit, read with git show; the working-tree matrix is only a
fallback, taken with a warning, when the pin or the blob at the pin is
unavailable. D007 to D009 run only when that governing matrix requires
the corresponding files, so v1 seeds are unaffected.

ctx is the standard check context: {root (the EOS repo), today,
offline}. A missing seed path or missing SCALE_MATRIX is reported as
an error finding, and cannot_run() names those two findings so the CLI
can map them to exit 2. The CLI used to look for the words "cannot
run" in the message text, which neither message contains, so the whole
exit-2 branch was unreachable and a seed path that does not exist
reported as findings (exit 1) rather than as a run that could not
happen.
"""

from __future__ import annotations

import fnmatch
import json
import re
import subprocess
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
# The file that carries scheduled work, per scale and matrix generation.
# v1: WORKLOG at S, QUEUE at M, NEXT at L. v2: task lists replace them.
QUEUE_FILE = {"S": "docs/WORKLOG.md", "M": "org/QUEUE.md",
              "L": "org/work/NEXT.md"}
# At ORG the scheduled work lives in task records; org/TASKS.md is a
# derived view and is never seeded, so the records are the surface.
QUEUE_FILE_V2 = {"S": "docs/TASKS.md", "ORG": "org/tasks/"}


def _queue_file(scale, required):
    """The queue surface for this seed, chosen by the governing matrix.

    A v2 matrix has an ORG column and ships task lists; a v1 matrix has
    M and L columns and ships a worklog or queue. Reading the scale set
    keeps D004 pointed at a file the seed is actually required to have.
    """
    if scale in QUEUE_FILE_V2 and ("ORG" in (required or {})
                                   or scale == "ORG"):
        return QUEUE_FILE_V2[scale]
    return QUEUE_FILE.get(scale)
LOCKIN_RE = re.compile(r"first[ -]build|lock-in", re.I)

MATRIX_PATH = "kernel/SCALE_MATRIX.md"
POLICY_FILES = ("docs/policy.json", "org/policy.json")
POLICY_SCHEMA = "kernel/schemas/policy.schema.json"
CLAIMS_SCHEMA = "kernel/schemas/claims.schema.json"

# The Genesis blueprint set (ADR-0006 decision 1), named by its kernel
# sources. A compiled seed file records the template it came from in
# compiled_from, so checking the sources leaves the destination paths
# to kernel/SCALE_MATRIX.md, which is where they are decided.
GENESIS_TEMPLATES = (
    "kernel/templates/PRODUCT_MAP.tpl.md",
    "kernel/templates/WORK_PACKAGE.tpl.md",
    "kernel/templates/RESEARCH_PACKET.tpl.md",
    "kernel/templates/ACCEPTANCE_SPINE.tpl.md",
    "kernel/templates/LENS.tpl.md",
)
SPINE_TEMPLATE = "kernel/templates/ACCEPTANCE_SPINE.tpl.md"
# Full-form Genesis is the ORG default; S takes the lite form, which is
# a build plan and a checklist rather than this file set.
GENESIS_SCALES = ("ORG",)
# What a compiled spine has to carry for a condition to be markable as
# outstanding: the marking itself, and a manifest table with a state
# column to put it in.
EXPECTED_FAIL_MARK = "expected-fail"
STATE_COLUMN = re.compile(r"^\|.*\|\s*state\s*\|", re.I)

# Same install command taskops names when jsonschema is missing.
_JSONSCHEMA_INSTALL = (
    "jsonschema is required for schema validation: install with "
    "python -m pip install --require-hashes -r tools/requirements.txt "
    "(or python -m pip install jsonschema)"
)

_GIT_TIMEOUT = 20


def _show_at_commit(root, commit: str, path: str):
    """Content of path at commit via git show, or None when unavailable.

    Read-only and degrading like gitfacts: any git failure returns None
    so the caller can fall back to the working tree with a warning.
    """
    try:
        proc = subprocess.run(
            ["git", "-C", str(Path(root)), "show", f"{commit}:{path}"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=_GIT_TIMEOUT,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout


# The two findings that mean the run never happened, rather than a
# seed that failed its rubric. Written once, here, beside the code that
# emits them, so the CLI does not have to recognise them by prose.
SEED_PATH_MISSING = "seed path not found"
MATRIX_MISSING = "missing; cannot check a seed"
CANNOT_RUN_PAIRS = frozenset({("D001", SEED_PATH_MISSING),
                              ("D003", MATRIX_MISSING)})


def cannot_run(findings) -> list:
    """The findings that mean this run could not happen at all."""
    return [f for f in findings
            if (f.check_id, f.message) in CANNOT_RUN_PAIRS]


def _cells(line: str) -> list:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def parse_matrix_text(text: str) -> tuple:
    """Parse SCALE_MATRIX content: (required, addons, empty_dirs).

    The scale columns come from the matrix table header row, so the v1
    layout (path, template, S, M, L) and the v2 layout (path, source,
    S, ORG) both parse. required maps scale -> [paths]; addons maps
    name -> [paths or patterns]; empty_dirs maps scale -> [dir paths]
    from the 'Directories created empty' section (L includes M's, per
    'L adds'). required is {} when no matrix table is found.
    """
    required: dict = {}
    scales: list = []
    addons: dict = {}
    mode = None
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = _cells(line)
        if not cells or not cells[0]:
            continue
        if cells[0] == "path":
            scales = [c for c in cells[2:] if c]
            required = {s: [] for s in scales}
            mode = "matrix"
            continue
        if cells[0] == "addon":
            mode = "addon"
            continue
        if cells[0].startswith("-"):
            continue
        if mode == "matrix" and len(cells) >= 2:
            marks = cells[2:2 + len(scales)]
            marks += [""] * (len(scales) - len(marks))
            for scale, mark in zip(scales, marks):
                if mark == "x":
                    required[scale].append(cells[0])
        elif mode == "addon" and len(cells) >= 2:
            name, fpath = cells[0], cells[1]
            if not re.match(r"^[a-z][a-z0-9-]*$", name):
                continue
            if " " not in fpath and "/" in fpath:
                addons.setdefault(name, []).append(fpath)
            else:
                addons.setdefault(name, [])
    empty_dirs = {s: [] for s in scales}
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


def parse_matrix_sources(text: str) -> set:
    """Every source cell the matrix table names.

    The second column says where a required file is compiled from. D010
    reads it to learn whether the matrix governing a seed knows about
    the Genesis templates at all. A seed pinned to a commit from before
    they existed could not have carried them and is not asked to.
    """
    sources: set = set()
    mode = None
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = _cells(line)
        if not cells or not cells[0]:
            continue
        if cells[0] == "path":
            mode = "matrix"
            continue
        if cells[0] == "addon":
            mode = "addon"
            continue
        if cells[0].startswith("-"):
            continue
        if mode == "matrix" and len(cells) >= 2 and cells[1]:
            sources.add(cells[1])
    return sources


def parse_matrix(eos_root) -> tuple:
    """Parse the working-tree kernel/SCALE_MATRIX.md.

    Returns (None, None, None) when the matrix file is absent.
    """
    path = Path(eos_root) / "kernel" / "SCALE_MATRIX.md"
    if not path.is_file():
        return None, None, None
    return parse_matrix_text(path.read_text(encoding="utf-8", errors="replace"))


def _scale_label(scales: list) -> str:
    if not scales:
        return "S, M or L"
    if len(scales) == 1:
        return scales[0]
    return ", ".join(scales[:-1]) + " or " + scales[-1]


def _schema_validate(eos_root, schema_rel: str, doc) -> tuple:
    """Validate doc against a kernel schema from the EOS working tree.

    Returns (messages, unavailable): messages are 'pointer: problem'
    strings; unavailable carries the jsonschema install command when
    the library is missing (consistent with taskops), else None.
    """
    try:
        import jsonschema
    except ImportError:
        return [], _JSONSCHEMA_INSTALL
    schema_path = Path(eos_root) / Path(schema_rel)
    if not schema_path.is_file():
        return [f"schema {schema_rel} not found in the EOS worktree"], None
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    messages = []
    for err in sorted(validator.iter_errors(doc), key=str):
        pointer = "/".join(str(p) for p in err.absolute_path) or "(root)"
        messages.append(f"{pointer}: {err.message}")
    return messages, None


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
        findings.add(Finding("D001", "error", str(seed_root), SEED_PATH_MISSING))
        return findings

    err = lambda check, path, msg: findings.add(Finding(check, "error", path, msg))
    warn = lambda check, path, msg: findings.add(Finding(check, "warn", path, msg))

    # --- lock-book pin first: it decides which matrix governs ----------
    eos_commit = None
    lockbook_text = None
    lb_fm = None
    lb = seed / "docs" / "LOCKBOOK.md"
    if lb.exists():
        lockbook_text = lb.read_text(encoding="utf-8", errors="replace")
        lb_fm = parse(lockbook_text)
        if lb_fm.present:
            eos_commit = lb_fm.data.get("eos_commit") or None

    pin_available = bool(eos_commit) and gitfacts.rev_parse(eos_root, eos_commit) is not None

    # --- the governing matrix: at the pin, worktree as a warned fallback
    required = addon_files = empty_dirs = None
    matrix_text = None
    if pin_available:
        pinned_matrix = _show_at_commit(eos_root, eos_commit, MATRIX_PATH)
        if pinned_matrix is not None:
            req, add, dirs = parse_matrix_text(pinned_matrix)
            if req:
                required, addon_files, empty_dirs = req, add, dirs
                matrix_text = pinned_matrix
    if required is None:
        required, addon_files, empty_dirs = parse_matrix(eos_root)
        worktree_matrix = Path(eos_root) / MATRIX_PATH
        if worktree_matrix.is_file():
            matrix_text = worktree_matrix.read_text(encoding="utf-8",
                                                    errors="replace")
        if required is None:
            findings.add(Finding("D003", "error", "kernel/SCALE_MATRIX.md",
                                 MATRIX_MISSING))
            return findings
        if pin_available:
            warn("D003", "kernel/SCALE_MATRIX.md",
                 f"absent or unparseable at eos_commit {eos_commit}, "
                 "matrix read from the working tree")
        elif eos_commit:
            warn("D003", "kernel/SCALE_MATRIX.md",
                 f"matrix read from the working tree, not the unavailable "
                 f"eos_commit {eos_commit}")

    def srel(p: Path) -> str:
        return p.relative_to(seed).as_posix()

    files = [(srel(p), p.read_text(encoding="utf-8", errors="replace")) for p in _md_files(seed)]
    parsed = [(r, text, parse(text)) for r, text in files]
    seed_md = [r for r, _ in files]

    # --- lock-book header (rubric A2, A3) ------------------------------
    scale, addons = None, []
    if lockbook_text is not None:
        if not lb_fm.present:
            err("E002", "docs/LOCKBOOK.md", "no front-matter block")
        else:
            for key in LOCKBOOK_KEYS:
                if not lb_fm.data.get(key):
                    err("E002", "docs/LOCKBOOK.md", f"header missing {key}")
            scale = lb_fm.data.get("scale")
            if scale not in required:
                err("E002", "docs/LOCKBOOK.md",
                    f"scale must be {_scale_label(list(required))}: {scale}")
                scale = None
            raw = re.match(r"\A---\n(.*?)\n---", lockbook_text, flags=re.S)
            if raw:
                for line in raw.group(1).splitlines():
                    if RULING_ROW.match(line) and not RULING_OK.match(line):
                        err("E002", "docs/LOCKBOOK.md",
                            f"ruling row not marked argued or inherited: {line.strip()}")
            if isinstance(lb_fm.data.get("addons"), list):
                addons = lb_fm.data["addons"]

    # --- pinned-commit availability (shared by D002 and D006) ----------
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
        # Directories a v1 matrix declares empty at compile: their
        # contents arrive later, so a file inside one is expected
        # rather than unaccounted for. v1 called those contents
        # Genesis outputs, in the older sense of that word; Genesis now
        # means only the blueprint phase of ADR-0006.
        first_use_dirs = tuple((empty_dirs or {}).get(scale, []))
        for r in seed_md:
            if r in required[scale] or r in addon_allowed or r in authored:
                continue
            if first_use_dirs and r.startswith(first_use_dirs):
                continue
            err("D003", r, f"not required at scale {scale}, "
                           "not an add-on, not marked authored in the compile report")

    # --- D004 deferrals need an open queue item ------------------------
    queue_rel = _queue_file(scale, required) if scale else None
    if scale and queue_rel:
        queue_path = seed / queue_rel
        if queue_rel.endswith("/"):
            # A record directory: any record scheduling the lock-in counts.
            records = sorted(queue_path.glob("*.json")) \
                if queue_path.is_dir() else []
            queue_text = "\n".join(
                r.read_text(encoding="utf-8", errors="replace")
                for r in records) if records else None
        else:
            queue_text = queue_path.read_text(
                encoding="utf-8", errors="replace") \
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

    # --- D007, D008 policy file and guard adapter (matrix-gated) -------
    if scale:
        for rel in POLICY_FILES:
            if rel not in required[scale]:
                continue
            policy_path = seed / rel
            if not policy_path.is_file():
                continue  # the required-file check (E008) already reports it
            try:
                policy = json.loads(policy_path.read_text(encoding="utf-8", errors="replace"))
            except ValueError as exc:
                err("D007", rel, f"malformed JSON: {exc}")
                continue
            messages, unavailable = _schema_validate(eos_root, POLICY_SCHEMA, policy)
            if unavailable:
                err("D007", rel, unavailable)
            for msg in messages:
                err("D007", rel, f"does not validate against {POLICY_SCHEMA}: {msg}")

            # D008: fail closed. Autonomy over guarded classes exists
            # only through a shipped, validated adapter mapping; with
            # validated false or absent every guarded class is
            # manual-only, which is the sanctioned declaration.
            guard = policy.get("guard") if isinstance(policy, dict) else None
            if not isinstance(guard, dict):
                err("D008", rel,
                    "policy has no guard section; guarded classes must ship "
                    "an adapter mapping or stay manual-only")
                continue
            adapter = guard.get("adapter")
            mapping_ref = guard.get("mapping_ref")
            if not adapter or not isinstance(adapter, str):
                err("D008", rel, "guard names no adapter")
            if not mapping_ref or not isinstance(mapping_ref, str):
                err("D008", rel, "guard names no mapping_ref")
            validated = guard.get("validated", False)
            if validated is True:
                if not mapping_ref or not isinstance(mapping_ref, str):
                    err("D008", rel,
                        "guard.validated true without an adapter mapping: "
                        "autonomous guarded actions fail closed")
                elif not (seed / mapping_ref).is_file():
                    err("D008", rel,
                        f"guard.validated true but the adapter mapping "
                        f"{mapping_ref} is not shipped in the seed; a policy "
                        "claiming autonomous guarded actions without an "
                        "adapter mapping fails closed")
            elif validated not in (False, None):
                err("D008", rel,
                    f"guard.validated must be boolean; any other value "
                    f"fails closed: {validated!r}")

    # --- D009 seeded claims validate (matrix-gated) --------------------
    if scale and "org/claims.json" in required[scale]:
        rel = "org/claims.json"
        claims_path = seed / rel
        if claims_path.is_file():
            try:
                claims = json.loads(claims_path.read_text(encoding="utf-8", errors="replace"))
            except ValueError as exc:
                err("D009", rel, f"malformed JSON: {exc}")
            else:
                messages, unavailable = _schema_validate(eos_root, CLAIMS_SCHEMA, claims)
                if unavailable:
                    err("D009", rel, unavailable)
                for msg in messages:
                    err("D009", rel, f"does not validate against {CLAIMS_SCHEMA}: {msg}")
                lanes = claims.get("lanes") if isinstance(claims, dict) else None
                if isinstance(lanes, list) and lanes:
                    err("D009", rel, "seeded claims must be an empty lanes list")

    # --- D010 the Genesis template set, D011 the spine's marking -------
    matrix_sources = parse_matrix_sources(matrix_text or "")
    governs_genesis = bool(matrix_sources.intersection(GENESIS_TEMPLATES))
    if scale in GENESIS_SCALES and governs_genesis:
        compiled = {}
        for r, _text, fm in parsed:
            if not fm.present:
                continue
            source = fm.data.get("compiled_from")
            if isinstance(source, str) and source:
                compiled.setdefault(source.strip(), []).append(r)
        for template in GENESIS_TEMPLATES:
            if not compiled.get(template):
                err("D010", template,
                    f"no file in this {scale} seed is compiled from it; the "
                    "Genesis blueprint set is compiled into every ORG seed "
                    "whether or not the operator runs the phase")

        # D011 reads the compiled form, and only the form. There is no
        # suite at compile time and no runtime to run one in, so this
        # cannot know that a spine fails; what it can see is whether the
        # compiled file still carries the marking the spine works by. A
        # spine compiled or edited without it has no way to say a
        # condition is outstanding, and a suite that cannot say that
        # reads as an acceptance walk already passed.
        for r in compiled.get(SPINE_TEMPLATE, []):
            text = next(t for rr, t, _f in parsed if rr == r)
            if EXPECTED_FAIL_MARK not in text:
                err("D011", r,
                    f"acceptance spine never says {EXPECTED_FAIL_MARK}: the "
                    "marking is how an unbuilt condition fails loudly "
                    "instead of skipping quietly. Structural check only; "
                    "nothing here runs the suite")
            if not any(STATE_COLUMN.match(line) for line in text.splitlines()):
                err("D011", r,
                    "acceptance spine has no manifest table with a state "
                    "column, so no condition can be marked outstanding")
    return findings
