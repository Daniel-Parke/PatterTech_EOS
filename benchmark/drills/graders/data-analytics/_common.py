"""Shared helpers for the DRILL-DATA-001 graders. Stdlib only.

Not a grader. The runner looks for `c<N>.py` by name, so this file is
never mistaken for a criterion.

Exit codes follow the grader contract: 0 pass, 1 fail, 2 the criterion
cannot be settled in this environment. The third exists because several
of these criteria drive the delivered pipeline, and a pipeline that
cannot start for want of a third-party library says nothing about the
work; reporting that as a fail would invent a finding against a tree
nobody managed to run.

Two things in here are worth knowing before reading a verdict.

**The answer surface.** Criteria 7, 8 and 9 grade "the written answer".
An attempt tree has no reserved filename for one, so the answer is
taken to be every Markdown or plain text file in the delivered tree
whose bytes differ from the scenario's copy of the same path, plus any
text file the scenario never had. The scenario's own prose is therefore
never read as the agent's argument, which matters: the scenario ships
an experiment log, and a grader that counted it would be marking the
fixture rather than the delivery.

**The seeded batch.** Criterion 3 needs the harness to drop it. It is
defined here as the rows of `raw/events.csv` that record a completed
purchase and carry no `order_total`, which is exactly the batch the
fixture seeds and nothing else in the file.
"""

import csv
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PASS, FAIL, UNSETTLED = 0, 1, 2

TEXT_SUFFIXES = (".md", ".txt", ".rst", ".markdown")
DATA_SUFFIXES = (".csv", ".tsv", ".json", ".jsonl", ".ndjson", ".parquet")
SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules",
             ".pytest_cache", ".ruff_cache", ".mypy_cache"}

# A raw event that carries money and so must carry a total.
MONEY_EVENT = re.compile(r"(?i)checkout[_ ]?complete|order[_ ]?placed|"
                         r"purchase[_ ]?complete")

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+|\n{2,}|\n\s*[-*+]\s+|\n\s*\d+[.)]\s+")


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


def scenario_root():
    """The frozen scenario this drill materialises from, if reachable."""
    here = Path(__file__).resolve()
    guess = here.parents[2] / "scenarios" / "data-analytics"
    return guess if guess.is_dir() else None


def walk(root, suffixes=None):
    """Every file under root, skipping build and VCS noise."""
    root = Path(root)
    for path in sorted(root.rglob("*")):
        if SKIP_DIRS.intersection(path.parts):
            continue
        if not path.is_file():
            continue
        if suffixes and path.suffix.lower() not in suffixes:
            continue
        yield path


def rel(root, path):
    return Path(path).relative_to(root).as_posix()


# ------------------------------------------------------ answer surface


def answer_files(scratch):
    """Text files the agent wrote or changed, as (rel, text) pairs.

    Files byte-identical to the scenario's copy are dropped: they are
    the fixture talking, not the delivery.
    """
    base = scenario_root()
    out = []
    for path in walk(scratch, TEXT_SUFFIXES):
        relative = rel(scratch, path)
        if base is not None:
            original = base / relative
            if original.is_file():
                try:
                    if original.read_bytes() == path.read_bytes():
                        continue
                except OSError:
                    pass
        out.append((relative, read(path)))
    return out


def sentences(text):
    """Rough sentence split, good enough to scope a negation to a clause."""
    flat = re.sub(r"[ \t]+", " ", text)
    return [s.strip() for s in _SENTENCE_SPLIT.split(flat) if s and s.strip()]


def flatten(text):
    return re.sub(r"\s+", " ", text).strip()


# -------------------------------------------------------- the pipeline

# Searched in order. The scenario ships pipeline/build.py and its README
# names that command, so a delivery that keeps the entry point is found
# first; the rest cover the usual places an agent moves it to.
ENTRY_POINTS = (
    "pipeline/build.py", "pipeline/run.py", "pipeline/main.py",
    "pipeline/__main__.py", "pipeline.py", "build.py", "run.py", "main.py",
    "scripts/build.py", "scripts/run.py", "scripts/pipeline.py",
    "etl/build.py", "src/pipeline/build.py", "src/build.py",
)
MAKE_TARGETS = ("validate", "pipeline", "build", "check", "all", "run")

_MISSING_DEP = re.compile(
    r"ModuleNotFoundError|ImportError|No module named|command not found|"
    r"is not recognized as an internal", re.I)


def find_pipeline(tree):
    """Return (argv, description) for the delivered pipeline command."""
    tree = Path(tree)
    for candidate in ENTRY_POINTS:
        path = tree / candidate
        if path.is_file():
            return [sys.executable, candidate], "python %s" % candidate
    makefile = tree / "Makefile"
    if makefile.is_file() and shutil.which("make"):
        text = read(makefile)
        for target in MAKE_TARGETS:
            if re.search(r"^%s\s*:" % re.escape(target), text, re.M):
                return ["make", target], "make %s" % target
    return None, None


def run_pipeline(tree, argv):
    """Run the command in `tree`. Returns (returncode, combined output)."""
    env = dict(os.environ)
    env["PYTHONPATH"] = str(tree) + os.pathsep + env.get("PYTHONPATH", "")
    env.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        proc = subprocess.run(argv, cwd=str(tree), capture_output=True,
                              text=True, encoding="utf-8", errors="replace",
                              timeout=900, env=env)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, str(exc)
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def looks_like_missing_dependency(output):
    return bool(_MISSING_DEP.search(output or ""))


def copy_tree(scratch, prefix):
    """A throwaway copy, so a grader never writes into the delivery."""
    work = Path(tempfile.mkdtemp(prefix=prefix))
    copy = work / "tree"
    shutil.copytree(scratch, copy,
                    ignore=shutil.ignore_patterns(*SKIP_DIRS))
    return work, copy


def drop_seeded_batch(tree):
    """Remove the seeded null-total rows from raw/events.csv in `tree`.

    Returns the number of rows dropped, or None when the export is not
    where the scenario put it.
    """
    path = Path(tree) / "raw" / "events.csv"
    if not path.is_file():
        return None
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames or []
        if "event_name" not in fields or "order_total" not in fields:
            return None
        kept, dropped = [], 0
        for row in reader:
            if (MONEY_EVENT.search(row.get("event_name") or "")
                    and not (row.get("order_total") or "").strip()):
                dropped += 1
                continue
            kept.append(row)
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields,
                                lineterminator="\n")
        writer.writeheader()
        writer.writerows(kept)
    return dropped


# ------------------------------------------------------- output tables


def output_data_files(tree):
    """Delivered data files that are not the raw exports."""
    out = []
    for path in walk(tree, DATA_SUFFIXES):
        parts = Path(rel(tree, path)).parts
        if parts and parts[0] in ("raw", "seeds", "source", "sources"):
            continue
        out.append(path)
    return out


def columns_of(path):
    """Column names of a data file, or None when the format is opaque."""
    suffix = Path(path).suffix.lower()
    if suffix in (".csv", ".tsv"):
        delim = "\t" if suffix == ".tsv" else ","
        try:
            with open(path, newline="", encoding="utf-8",
                      errors="replace") as handle:
                header = next(csv.reader(handle, delimiter=delim), None)
        except OSError:
            return None
        return [c.strip() for c in header] if header else []
    if suffix in (".jsonl", ".ndjson"):
        text = read(path)
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                doc = json.loads(line)
            except ValueError:
                return None
            return list(doc) if isinstance(doc, dict) else []
        return []
    if suffix == ".json":
        try:
            doc = json.loads(read(path))
        except ValueError:
            return None
        if isinstance(doc, list) and doc and isinstance(doc[0], dict):
            return list(doc[0])
        if isinstance(doc, dict):
            return list(doc)
        return []
    return None


def parquet_column_scan(path):
    """Best effort: parquet stores its column names as plain strings.

    Returns the decoded footer bytes, which is enough to answer "does a
    column called something-email exist" without a parquet reader. It is
    a scan, not a parse, and the graders say so when they lean on it.
    """
    try:
        return Path(path).read_bytes().decode("latin-1", errors="replace")
    except OSError:
        return ""


# ------------------------------------------------------------- YAML

# A deliberately small YAML reader. The graders must run on a stdlib
# Python, and every contract format the drill names is either JSON or a
# plain nested mapping of scalars and lists. Anything this cannot make
# sense of is reported as "does not parse" rather than guessed at, which
# is the honest direction for a criterion whose whole content is "and
# parses".


class YamlError(Exception):
    pass


_KEY = re.compile(r"^(?P<key>(?:\"[^\"]*\"|'[^']*'|[^:#]+?))\s*:"
                  r"(?:\s+(?P<val>.*?))?\s*$")
_BLOCK = re.compile(r"^[|>][-+]?\d*$")


def parse_yaml(text):
    """Return the parsed document, or None when it does not parse."""
    try:
        lines = _yaml_lines(text)
    except YamlError:
        return None
    if not lines:
        return {}
    try:
        value, index = _yaml_block(lines, 0, lines[0][0])
    except (YamlError, IndexError, RecursionError):
        return None
    if index != len(lines):
        return None
    return value


def _yaml_lines(text):
    out = []
    raw = text.replace("\r\n", "\n").split("\n")
    i = 0
    while i < len(raw):
        line = raw[i]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        if stripped in ("---", "..."):
            i += 1
            continue
        indent = len(line) - len(line.lstrip(" "))
        if "\t" in line[:indent]:
            raise YamlError("tab used for indentation")
        content = _strip_comment(stripped)
        if not content:
            i += 1
            continue
        match = _KEY.match(content)
        if match and match.group("val") and _BLOCK.match(match.group("val")):
            # Block scalar: swallow the indented body as one string.
            body, i = [], i + 1
            while i < len(raw):
                nxt = raw[i]
                if not nxt.strip():
                    body.append("")
                    i += 1
                    continue
                nxt_indent = len(nxt) - len(nxt.lstrip(" "))
                if nxt_indent <= indent:
                    break
                body.append(nxt.strip())
                i += 1
            key = _scalar(match.group("key"))
            out.append((indent, "%s: %s" % (key, " ".join(body).strip())))
            continue
        out.append((indent, content))
        i += 1
    return out


def _strip_comment(content):
    out, quote = [], None
    for i, ch in enumerate(content):
        if quote:
            out.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in "\"'":
            quote = ch
            out.append(ch)
            continue
        if ch == "#" and (i == 0 or content[i - 1] in " \t"):
            break
        out.append(ch)
    return "".join(out).strip()


def _yaml_block(lines, i, indent):
    if i >= len(lines):
        return None, i
    if lines[i][1].startswith("- ") or lines[i][1] == "-":
        return _yaml_seq(lines, i, indent)
    return _yaml_map(lines, i, indent)


def _yaml_map(lines, i, indent):
    out = {}
    while i < len(lines):
        cur_indent, content = lines[i]
        if cur_indent < indent:
            break
        if cur_indent > indent:
            raise YamlError("unexpected indent")
        if content.startswith("- "):
            break
        match = _KEY.match(content)
        if not match:
            raise YamlError("not a mapping entry: %r" % content[:60])
        key = _scalar(match.group("key"))
        val = match.group("val")
        i += 1
        if val is None or val == "":
            if i < len(lines) and lines[i][0] > cur_indent:
                out[key], i = _yaml_block(lines, i, lines[i][0])
            elif (i < len(lines) and lines[i][0] == cur_indent
                  and lines[i][1].startswith("- ")):
                out[key], i = _yaml_seq(lines, i, cur_indent)
            else:
                out[key] = None
        else:
            out[key] = _scalar(val)
    return out, i


def _yaml_seq(lines, i, indent):
    out = []
    while i < len(lines):
        cur_indent, content = lines[i]
        if cur_indent < indent or not (content.startswith("- ")
                                       or content == "-"):
            break
        if cur_indent > indent:
            raise YamlError("unexpected indent in sequence")
        rest = content[2:].strip() if content != "-" else ""
        if not rest:
            i += 1
            if i < len(lines) and lines[i][0] > cur_indent:
                item, i = _yaml_block(lines, i, lines[i][0])
            else:
                item = None
            out.append(item)
            continue
        if _KEY.match(rest):
            # `- name: x` then further keys indented under it.
            inner = [(cur_indent + 2, rest)] + lines[i + 1:]
            item, consumed = _yaml_map(inner, 0, cur_indent + 2)
            out.append(item)
            i += consumed
            continue
        out.append(_scalar(rest))
        i += 1
    return out, i


def _scalar(token):
    token = token.strip()
    if len(token) >= 2 and token[0] == token[-1] and token[0] in "\"'":
        return token[1:-1]
    low = token.lower()
    if low in ("null", "~", ""):
        return None
    if low in ("true", "yes", "on"):
        return True
    if low in ("false", "no", "off"):
        return False
    try:
        return int(token)
    except ValueError:
        pass
    try:
        return float(token)
    except ValueError:
        pass
    return token


# --------------------------------------------------------- contracts

NAME_KEYS = ("name", "column", "column_name", "field", "property",
             "logicalName", "physicalName")
CONTRACT_HINTS = ("contract", "expectation", "expectations", "suite",
                  "odcs", "quality", "schema")


def contract_files(scratch):
    """Candidate contract or expectation files, as (rel, kind, parsed).

    Recognises the three families the drill names, plus any YAML or JSON
    file whose path says it is a contract or an expectation suite. Every
    candidate has to actually parse to be returned; a file that does not
    is reported by criterion 1 as a near miss rather than silently
    dropped.
    """
    found, near = [], []
    for path in walk(scratch, (".yaml", ".yml", ".json")):
        relative = rel(scratch, path)
        lower = relative.lower()
        name = Path(lower).name
        text = read(path)
        if path.suffix.lower() == ".json":
            try:
                doc = json.loads(text)
            except ValueError:
                if any(h in lower for h in CONTRACT_HINTS):
                    near.append((relative, "JSON does not parse"))
                continue
            if isinstance(doc, dict) and (
                    "expectations" in doc or "expectation_suite_name" in doc):
                found.append((relative, "Great Expectations suite", doc))
            elif any(h in lower for h in CONTRACT_HINTS):
                found.append((relative, "JSON contract", doc))
            continue

        doc = parse_yaml(text)
        if doc is None:
            if (name.endswith(".odcs.yaml") or name.endswith(".odcs.yml")
                    or any(h in lower for h in CONTRACT_HINTS)):
                near.append((relative, "YAML does not parse"))
            continue
        if name.endswith(".odcs.yaml") or name.endswith(".odcs.yml"):
            found.append((relative, "ODCS data contract", doc))
            continue
        if isinstance(doc, dict) and "models" in doc:
            enforced = re.search(r"contract\s*:", text) and \
                re.search(r"enforced\s*:\s*true", text, re.I)
            if enforced:
                found.append((relative, "dbt schema.yml with contract "
                                        "enforced", doc))
            else:
                near.append((relative,
                             "a dbt models file without contract: enforced"))
            continue
        if isinstance(doc, dict) and ("schema" in doc or "quality" in doc) \
                and any(h in lower for h in ("contract", "odcs", "quality")):
            found.append((relative, "data contract", doc))
            continue
        if any(h in lower for h in ("contract", "expectation", "suite")):
            found.append((relative, "declared contract file", doc))
    return found, near


RULE_TOKENS = (
    "not_null", "not null", "notnull", "nonnull", "non_null",
    "nullable: false", "nullable:false", "nullable=false",
    "required: true", "required:true", "required=true",
    "expect_column_values_to_not_be_null",
    "expect_column_values_to_be_between",
    "accepted_range", "accepted_values", "valid_range",
    "min_value", "max_value", "minimum", "maximum",
    "min:", "max:", "between", "greater_than", "range",
)


def walk_docs(doc):
    """Yield every dict nested anywhere inside a parsed document."""
    if isinstance(doc, dict):
        yield doc
        for value in doc.values():
            yield from walk_docs(value)
    elif isinstance(doc, list):
        for value in doc:
            yield from walk_docs(value)


def subtree_text(doc):
    try:
        return json.dumps(doc, default=str).lower()
    except (TypeError, ValueError):
        return str(doc).lower()


def names_in(node):
    out = set()
    for key in NAME_KEYS:
        value = node.get(key)
        if isinstance(value, str):
            out.add(value.strip())
    kwargs = node.get("kwargs")
    if isinstance(kwargs, dict) and isinstance(kwargs.get("column"), str):
        out.add(kwargs["column"].strip())
    return out
