"""Shared helpers for the devops-reliability drill graders. Stdlib only.

Not a grader. The runner looks for `c<N>.py` by name, so this file is
never mistaken for a criterion.

Exit codes follow the grader contract: 0 pass, 1 fail, 2 the criterion
cannot be settled in this environment. The third exists because some of
these criteria have to drive something the delivered tree supplies (a
migration linter, a restore script, a rollout evaluator) and a machine
that cannot run it must say so rather than report the work as broken.

Two things are worth knowing before reading a grader:

- The frozen scenario is reachable from here, so a grader can tell what
  the fixture shipped from what the agent added. That is how "added
  flag", "migration beyond the pre-existing history" and "the diff" are
  decided.
- Nothing is ever written into the tree being graded. Anything that
  needs to mutate a file works on a copy in a temporary directory.
"""

import difflib
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

PASS, FAIL, UNSETTLED = 0, 1, 2

PACK = "devops-reliability"

SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".venv", "venv",
             "node_modules", "var", ".mypy_cache", ".ruff_cache"}

# Names that say "this file exists to undo something".
ROLLBACK_TOKENS = {"down", "downs", "undo", "undos", "rollback", "rollbacks",
                   "revert", "reverts", "downgrade", "downgrades", "unapply"}

ORDINAL = re.compile(r"^(\d+)")


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


def frozen_scenario():
    """The fixture as it shipped, so "added" can mean something."""
    return Path(__file__).resolve().parents[2] / "scenarios" / PACK


def require_baseline(cid):
    base = frozen_scenario()
    if not base.is_dir():
        emit(cid, UNSETTLED,
             "the frozen scenario is not reachable at %s, so this grader "
             "cannot tell what the fixture shipped from what was added"
             % base)
    return base


def read(path):
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def iter_files(root, suffixes=None):
    root = Path(root)
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if suffixes and path.suffix.lower() not in suffixes:
            continue
        yield path


def copy_tree(scratch, prefix):
    """A scratch copy of the delivered tree. The caller removes it."""
    work = Path(tempfile.mkdtemp(prefix=prefix))
    copy = work / "tree"
    shutil.copytree(scratch, copy,
                    ignore=shutil.ignore_patterns(".git", "__pycache__",
                                                  "var", ".venv"))
    return work, copy


def run(cmd, cwd, env=None, timeout=180):
    """Run a command. Returns (returncode_or_None, combined_output)."""
    environ = dict(os.environ)
    environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
    if env:
        environ.update(env)
    try:
        proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True,
                              text=True, encoding="utf-8", errors="replace",
                              timeout=timeout, env=environ)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, str(exc)
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def path_tokens(rel):
    return set(t for t in re.split(r"[^A-Za-z]+", str(rel).lower()) if t)


# ------------------------------------------------------------ migrations


def migration_files(root):
    """Forward migrations, in ordinal order.

    Anything living under a rollback or down directory is not a forward
    migration and is left to the criterion that objects to it existing.
    """
    root = Path(root)
    folder = root / "migrations"
    if not folder.is_dir():
        return []
    found = []
    for path in folder.rglob("*.sql"):
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if path_tokens(rel) & ROLLBACK_TOKENS:
            continue
        found.append(path)
    return sorted(found, key=lambda p: (ordinal_of(p), p.name))


def ordinal_of(path):
    match = ORDINAL.match(Path(path).name)
    return int(match.group(1)) if match else -1


def non_sql_migrations(root):
    """Migration-shaped files this project's runner would not apply."""
    folder = Path(root) / "migrations"
    if not folder.is_dir():
        return []
    out = []
    for path in sorted(folder.rglob("*")):
        if not path.is_file() or path.suffix.lower() in (".sql", ".md"):
            continue
        rel = path.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if ORDINAL.match(path.name):
            out.append(rel.as_posix())
    return out


def baseline_migration_names(cid):
    base = require_baseline(cid)
    return {p.name for p in migration_files(base)}


def apply_migrations(db_file, files):
    """Apply SQL files in order to a fresh SQLite database.

    Returns (ok, message). The runner in the fixture does the same thing
    with bookkeeping; this does it without trusting a delivered script.
    """
    conn = sqlite3.connect(str(db_file))
    try:
        for path in files:
            sql = read(path)
            try:
                with conn:
                    conn.executescript(sql)
            except sqlite3.Error as exc:
                return False, "%s failed: %s" % (Path(path).name, exc)
    finally:
        conn.close()
    return True, "applied %d migration(s)" % len(files)


def table_names(db_file):
    conn = sqlite3.connect(str(db_file))
    try:
        rows = conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
    finally:
        conn.close()
    return {row[0] for row in rows}


def columns_of(db_file, table):
    conn = sqlite3.connect(str(db_file))
    try:
        rows = conn.execute("PRAGMA table_info(%s)" % table).fetchall()
    finally:
        conn.close()
    return [(row[1], (row[2] or "").upper()) for row in rows]


def query(db_file, sql, params=()):
    conn = sqlite3.connect(str(db_file))
    try:
        return conn.execute(sql, params).fetchall()
    finally:
        conn.close()


# ------------------------------------------------------------- SQL shape


_COMMENT_LINE = re.compile(r"--[^\n]*")
_COMMENT_BLOCK = re.compile(r"/\*.*?\*/", re.S)

_NAME = r"[`\"\[]?([A-Za-z_][\w$]*)[`\"\]]?"

ADDITIVE_RES = (
    (re.compile(r"\bCREATE\s+(?:TEMP\s+|TEMPORARY\s+)?TABLE\s+"
                r"(?:IF\s+NOT\s+EXISTS\s+)?" + _NAME, re.I), "create table"),
    (re.compile(r"\bALTER\s+TABLE\s+" + _NAME + r"\s+ADD\s+", re.I | re.S),
     "add column"),
    (re.compile(r"\bCREATE\s+(?:UNIQUE\s+)?INDEX\s+(?:IF\s+NOT\s+EXISTS\s+)?"
                r"[\w`\"\[\]]+\s+ON\s+" + _NAME, re.I | re.S), "create index"),
    (re.compile(r"\bINSERT\s+(?:OR\s+\w+\s+)?INTO\s+" + _NAME, re.I),
     "backfill insert"),
    (re.compile(r"\bCREATE\s+TRIGGER\s+(?:IF\s+NOT\s+EXISTS\s+)?[\w`\"\[\]]+"
                r"[\s\S]{0,80}?\bON\s+" + _NAME, re.I), "create trigger"),
    (re.compile(r"\bCREATE\s+VIEW\s+(?:IF\s+NOT\s+EXISTS\s+)?" + _NAME, re.I),
     "create view"),
)

DESTRUCTIVE_RES = (
    (re.compile(r"\bDROP\s+TABLE\s+(?:IF\s+EXISTS\s+)?" + _NAME, re.I),
     "DROP TABLE"),
    (re.compile(r"\bALTER\s+TABLE\s+" + _NAME + r"\s+DROP\s+COLUMN", re.I
                | re.S), "DROP COLUMN"),
)

RENAME_RE = re.compile(
    r"\bALTER\s+TABLE\s+" + _NAME + r"\s+RENAME\s+TO\s+" + _NAME,
    re.I | re.S)

# A backfill names both ends of the move in one statement, which is how
# a file that creates the new table and drops the old column can be
# caught even though the two statements name different tables.
LINK_RES = (
    re.compile(r"\bINSERT\s+(?:OR\s+\w+\s+)?INTO\s+" + _NAME
               + r"(?:(?!;)[\s\S])*?\bFROM\s+" + _NAME, re.I),
    re.compile(r"\bCREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?" + _NAME
               + r"(?:(?!;)[\s\S])*?\bAS\s+SELECT(?:(?!;)[\s\S])*?\bFROM\s+"
               + _NAME, re.I),
)


def strip_sql_comments(text):
    return _COMMENT_LINE.sub(" ", _COMMENT_BLOCK.sub(" ", text))


def sql_subjects(text):
    """(additive, destructive, links) for one migration file.

    `links` are pairs of table names the file itself ties together: a
    rename, or a backfill that reads one table and writes another. Two
    linked names are one subject, because create-copy-drop-rename and
    create-new-table-then-drop-the-old-column are both expand and
    contract in a single file, whatever the statements are called.
    """
    body = strip_sql_comments(text)
    additive, destructive, links = {}, {}, []
    for pattern, label in ADDITIVE_RES:
        for match in pattern.finditer(body):
            additive.setdefault(match.group(1).lower(), label)
    for pattern, label in DESTRUCTIVE_RES:
        for match in pattern.finditer(body):
            destructive.setdefault(match.group(1).lower(), label)
    for match in RENAME_RE.finditer(body):
        links.append((match.group(1).lower(), match.group(2).lower()))
    for pattern in LINK_RES:
        for match in pattern.finditer(body):
            links.append((match.group(1).lower(), match.group(2).lower()))
    return additive, destructive, links


def same_subject(additive, destructive, links):
    """Subjects touched additively and destructively in one file."""
    parent = {}

    def find(name):
        parent.setdefault(name, name)
        while parent[name] != name:
            parent[name] = parent[parent[name]]
            name = parent[name]
        return name

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for a, b in links:
        union(a, b)
    shared = set()
    for name in additive:
        for other in destructive:
            if find(name) == find(other):
                shared |= {name, other}
    return sorted(shared)


def is_destructive(path):
    _, destructive, _ = sql_subjects(read(path))
    return bool(destructive)


# --------------------------------------------------- structured config


def _strip_comment(line):
    out, quote = [], None
    for i, ch in enumerate(line):
        if quote:
            out.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in "\"'":
            quote = ch
            out.append(ch)
            continue
        if ch == "#" and (i == 0 or line[i - 1] in " \t"):
            break
        out.append(ch)
    return "".join(out)


def _scalar(text):
    text = text.strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'":
        return text[1:-1]
    low = text.lower()
    if low in ("true", "yes"):
        return True
    if low in ("false", "no"):
        return False
    if low in ("null", "~", ""):
        return None
    if text.startswith("{") or text.startswith("["):
        try:
            return json.loads(text)
        except ValueError:
            return text
    try:
        return int(text)
    except ValueError:
        pass
    try:
        return float(text)
    except ValueError:
        return text


def _yaml_lines(text):
    out = []
    for raw in text.splitlines():
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        if raw.strip() in ("---", "..."):
            continue
        line = _strip_comment(raw.rstrip())
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        out.append((indent, line.strip()))
    return out


def _sub_block(lines, i, indent):
    j = i
    sub = []
    while j < len(lines) and lines[j][0] > indent:
        sub.append(lines[j])
        j += 1
    return sub, j


def _block(lines):
    if not lines:
        return None
    indent = lines[0][0]
    if lines[0][1] == "-" or lines[0][1].startswith("- "):
        return _sequence(lines, indent)
    return _mapping(lines, indent)


def _sequence(lines, indent):
    items, i = [], 0
    while i < len(lines):
        level, text = lines[i]
        if level != indent or not (text == "-" or text.startswith("- ")):
            break
        inline = text[1:].strip()
        children, i = _sub_block(lines, i + 1, indent)
        if inline and ":" not in inline and not children:
            items.append(_scalar(inline))
            continue
        block = []
        if inline:
            block.append((indent + 2, inline))
        block.extend(children)
        items.append(_block(block) if block else None)
    return items


def _mapping(lines, indent):
    out, i = {}, 0
    while i < len(lines):
        level, text = lines[i]
        if level != indent:
            break
        if text.startswith("- "):
            break
        key, sep, rest = text.partition(":")
        if not sep:
            raise ValueError("not a mapping line: %r" % text)
        key = _scalar(key)
        rest = rest.strip()
        children, i = _sub_block(lines, i + 1, indent)
        if rest:
            out[key] = _scalar(rest)
        elif children:
            out[key] = _block(children)
        else:
            out[key] = None
    return out


def parse_yaml(text):
    """A small block-YAML reader: mappings, sequences and scalars.

    Enough for an OpenSLO document, a flag file or a rollout plan, and
    honest about the rest: anything it cannot read raises ValueError and
    the caller says so rather than guessing.
    """
    return _block(_yaml_lines(text))


def load_structured(path):
    """Parse a JSON or YAML file. Returns (value, error_or_None)."""
    text = read(path)
    if not text.strip():
        return None, "%s is empty" % Path(path).name
    suffix = Path(path).suffix.lower()
    if suffix == ".json":
        try:
            return json.loads(text), None
        except ValueError as exc:
            return None, "%s does not parse as JSON: %s" % (
                Path(path).name, exc)
    try:
        return parse_yaml(text), None
    except (ValueError, IndexError) as exc:
        try:
            return json.loads(text), None
        except ValueError:
            return None, "%s does not parse: %s" % (Path(path).name, exc)


def find_one(root, names, suffixes=(".json", ".yaml", ".yml")):
    """Files whose stem carries one of `names`, best candidates first."""
    found = []
    for path in iter_files(root, suffixes=set(suffixes)):
        rel = path.relative_to(root)
        tokens = path_tokens(rel)
        if tokens & set(names):
            found.append(path)
    return sorted(found, key=lambda p: (len(p.relative_to(root).parts),
                                        p.name))


# -------------------------------------------------------- change record

DOC_SUFFIXES = {".md", ".markdown", ".json", ".yaml", ".yml", ".toml",
                ".txt", ".rst"}


def document_files(root):
    """Prose and metadata files the agent may have written the record in.

    Migrations, tests and the app itself are excluded: a change record
    is a document, and scanning source for a phrase invites a match on
    a comment that was never a record.
    """
    root = Path(root)
    for path in iter_files(root, suffixes=DOC_SUFFIXES):
        rel = path.relative_to(root)
        head = rel.parts[0] if rel.parts else ""
        if head in ("migrations", "tests", "app", ".github"):
            continue
        yield path


# ------------------------------------------------------------- the diff


def added_lines(scratch, baseline):
    """Lines the delivered tree adds to or changes from the fixture.

    A new file contributes all of its lines. A changed file contributes
    only what changed, which is what "in the diff" means; a line the
    fixture already carried and the agent left alone is not part of the
    change and is not this criterion's business.
    """
    scratch, baseline = Path(scratch), Path(baseline)
    out = []
    for path in iter_files(scratch):
        rel = path.relative_to(scratch)
        old = baseline / rel
        try:
            new_text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if old.is_file():
            try:
                old_text = old.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                old_text = ""
            if old_text == new_text:
                continue
            diff = difflib.unified_diff(old_text.splitlines(),
                                        new_text.splitlines(), n=0)
            for line in diff:
                if line.startswith("+") and not line.startswith("+++"):
                    out.append((rel.as_posix(), line[1:]))
        else:
            for line in new_text.splitlines():
                out.append((rel.as_posix(), line))
    return out
