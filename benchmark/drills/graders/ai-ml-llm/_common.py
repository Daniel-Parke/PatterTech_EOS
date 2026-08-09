"""Shared helpers for the ai-ml-llm drill graders. Stdlib only.

Not a grader. The runner looks for `c<N>.py` by name, so this file is
never mistaken for a criterion.

Exit codes follow the grader contract: 0 pass, 1 fail, 2 the criterion
cannot be settled in this environment. The third exists because most of
these criteria are settled by running the agent's eval entry point, and
an entry point that dies on `import numpy` on a machine with no numpy
tells us nothing about the work. That is recorded as manual, never as a
finding against the delivered tree.

Everything here is drill-specific by design. The fixture's own file
names, and the eighteen tickets its two annotators read differently,
are frozen in this module so a grader keeps working when the agent
reshapes the tree around them.
"""

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from collections import namedtuple
from pathlib import Path

PASS, FAIL, UNSETTLED = 0, 1, 2

# The spec allows twenty minutes of wall clock. The runner kills a
# grader at ten, and several graders run the eval more than once, so
# the cap here is tighter than the spec's and is stated wherever it
# decides an outcome.
RUN_TIMEOUT_S = 240

FIXTURE_FILES = ("classify.py", "stub_client.py", "prompt.txt",
                 "prompt_b.txt", "labelled.jsonl", "README.md")

SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "env", "node_modules",
             ".mypy_cache", ".pytest_cache", ".ruff_cache", ".tox", "dist",
             "build", ".idea", ".eggs"}

DATA_SUFFIXES = {".jsonl", ".json", ".csv", ".tsv", ".ndjson"}
DOC_SUFFIXES = {".md", ".rst", ".txt", ".toml", ".cfg", ".ini", ".yml",
                ".yaml", ".json", ".sh", ".mk"}

NETWORK_MARKER = "outbound network is blocked for this run"

# The eighteen tickets the second annotator read differently. Frozen
# here rather than read from the tree: the agent is expected to split
# and reshape the sample, and a criterion about abstention must survive
# that.
AMBIGUOUS = (
    "I was charged twice because the payment page threw an error and I "
    "clicked again.",
    "The invoice total does not match the rows on the statement, one of "
    "them is wrong.",
    "The upgrade went through but we were charged the old price, the "
    "checkout looked broken.",
    "The card was declined with a 500 error and then the money left the "
    "account anyway.",
    "The receipt downloads as a zero byte file every time.",
    "We were billed for a seat belonging to someone who left and I cannot "
    "remove them.",
    "Adding two more seats put us on a new plan we did not ask for.",
    "My login stopped working the day the subscription lapsed.",
    "Invoices are going to a colleague who left and I cannot change the "
    "email address.",
    "Sorting is wrong, or perhaps it was never meant to sort by owner.",
    "The export drops the last column, could you add it back?",
    "The filter only takes one value, which makes it useless for us.",
    "There is no way to undo, so one misclick loses the whole board.",
    "Dark mode hides half the icons, so we cannot use it.",
    "Guests can see everything, we need read only access for them.",
    "Please add a way to invite people in bulk from a CSV.",
    "Permissions are all or nothing, we want access per project.",
    "Could new starters be added automatically from our directory?",
)


# ---------------------------------------------------------------- basics


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


def walk(root, suffixes=None):
    """Every file under root, skipping the noise directories."""
    root = Path(root)
    out = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if SKIP_DIRS.intersection(path.parts):
            continue
        if suffixes and path.suffix.lower() not in suffixes:
            continue
        out.append(path)
    return sorted(out)


def rel(scratch, path):
    try:
        return Path(path).relative_to(scratch).as_posix()
    except ValueError:
        return str(path)


def digests(path):
    """Hashes of a file, both as stored and with line endings normalised.

    The second form exists because a tree checked out on Windows carries
    CRLF, and a solution that hashes the text it read rather than the
    bytes on disk is not wrong for it.
    """
    try:
        raw = Path(path).read_bytes()
    except OSError:
        return set()
    out = set()
    for blob in (raw, raw.replace(b"\r\n", b"\n")):
        for algo in ("sha256", "sha1", "md5"):
            out.add(hashlib.new(algo, blob).hexdigest())
    return out


def load_jsonl(path):
    rows = []
    for line in read(path).splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except ValueError:
            return []
    return rows


# ------------------------------------------------------------ json shape


def norm_key(key):
    return re.sub(r"[^a-z0-9]+", "_", str(key).lower()).strip("_")


def walk_json(obj, path="$"):
    """Yield (path, key, value) for every mapping entry in a document."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            here = "%s.%s" % (path, key)
            yield here, key, value
            yield from walk_json(value, here)
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            yield from walk_json(value, "%s[%d]" % (path, i))


def find_keys(obj, predicate):
    """Every (path, key, value) whose normalised key satisfies predicate."""
    return [(p, k, v) for p, k, v in walk_json(obj)
            if predicate(norm_key(k))]


def json_strings(obj):
    """Every string value in a document."""
    out = []

    def visit(node):
        if isinstance(node, str):
            out.append(node)
        elif isinstance(node, dict):
            for key, value in node.items():
                visit(value)
        elif isinstance(node, list):
            for value in node:
                visit(value)

    visit(obj)
    return out


def flat_text(obj):
    try:
        return json.dumps(obj, ensure_ascii=False)
    except (TypeError, ValueError):
        return str(obj)


def is_accuracy_key(norm):
    return norm == "acc" or "accuracy" in norm


N_KEYS = {"n", "n_items", "n_examples", "n_total", "n_scored", "n_eval",
          "num_items", "num_examples", "count", "items", "sample_size",
          "size", "total", "n_samples", "evaluated"}


def is_n_key(norm):
    return norm in N_KEYS


INTERVAL_TOKENS = {"ci", "se", "stderr", "sem", "interval", "moe", "wilson",
                   "bootstrap", "halfwidth"}
INTERVAL_PHRASES = ("confidence_interval", "standard_error", "std_err",
                    "margin_of_error", "error_bar", "conf_int", "ci_low",
                    "ci_high", "interval")
# ci95, ci_95, se_95 and the like, which read as one token but are not.
INTERVAL_SHORT = re.compile(r"(?:^|_)(?:ci|se)_?\d{0,3}(?:_|$)")


def is_interval_key(norm):
    tokens = set(norm.split("_"))
    if tokens & INTERVAL_TOKENS:
        return True
    if INTERVAL_SHORT.search(norm):
        return True
    return any(phrase in norm for phrase in INTERVAL_PHRASES)


def is_abstain_rate_key(norm):
    return ("abstain" in norm or "abstention" in norm) and (
        "rate" in norm or "fraction" in norm or "share" in norm
        or "pct" in norm or "percent" in norm or "proportion" in norm)


def numeric(value):
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.strip().rstrip("%"))
        except ValueError:
            return None
    return None


# -------------------------------------------------------- the entry point


Run = namedtuple("Run", "entry rel rc stdout stderr seconds report source "
                        "missing_module")

ENTRY_RANK = ("run_eval", "evaluate", "eval", "run_evaluation", "score",
              "bench", "benchmark", "report", "main", "run")


def _rank(path):
    stem = path.stem.lower()
    for i, hint in enumerate(ENTRY_RANK):
        if stem == hint:
            return (0, i, str(path))
    for i, hint in enumerate(ENTRY_RANK):
        if hint in stem:
            return (1, i, str(path))
    return (2, 99, str(path))


def candidate_entries(scratch):
    """Python files that plausibly are the eval entry point.

    A file qualifies on its name or on mentioning accuracy, which an
    eval that reports one has to. The fixture's own two modules are
    never candidates: `classify.py` is the thing under test.
    """
    out = []
    for path in walk(scratch, {".py"}):
        name = path.name
        if name in ("classify.py", "stub_client.py", "conftest.py",
                    "setup.py", "_common.py"):
            continue
        if name.startswith("test_") or name.endswith("_test.py"):
            continue
        if "tests" in path.parts:
            continue
        text = read(path)
        hinted = any(h in path.stem.lower() for h in ENTRY_RANK)
        if not hinted and "accuracy" not in text.lower():
            continue
        if "__main__" not in text and "print" not in text and not hinted:
            continue
        out.append(path)
    return sorted(out, key=_rank)[:8]


_SITECUSTOMIZE = """\
import socket


def _deny(*args, **kwargs):
    raise OSError(%r)


socket.socket.connect = _deny
socket.socket.connect_ex = _deny
socket.create_connection = _deny
socket.getaddrinfo = _deny
try:
    import ssl
    ssl.SSLContext.wrap_socket = _deny
except Exception:
    pass
""" % NETWORK_MARKER


def _copy_tree(scratch, dest):
    shutil.copytree(scratch, dest,
                    ignore=shutil.ignore_patterns(*sorted(SKIP_DIRS)))


def _stdlib_names():
    return set(getattr(sys, "stdlib_module_names", ()) or ())


def _missing_module(stderr, tree):
    match = re.search(r"No module named ['\"]([\w.]+)['\"]", stderr or "")
    if not match:
        return None
    name = match.group(1).split(".")[0]
    if name in _stdlib_names():
        return None
    if (Path(tree) / (name + ".py")).exists() or (Path(tree) / name).is_dir():
        return None
    return name


def _json_objects(text):
    """Every top level JSON object printed in a blob of stdout."""
    found = []
    decoder = json.JSONDecoder()
    i = 0
    while True:
        start = text.find("{", i)
        if start == -1:
            break
        try:
            obj, end = decoder.raw_decode(text, start)
        except ValueError:
            i = start + 1
            continue
        if isinstance(obj, dict):
            found.append(obj)
        i = end
    return found


def _has_accuracy(obj):
    return bool(find_keys(obj, is_accuracy_key))


def _pick_report(stdout, written):
    """The best report from stdout and from any JSON the run wrote."""
    seen = [("stdout", obj) for obj in _json_objects(stdout or "")]
    seen += written
    with_accuracy = [s for s in seen if _has_accuracy(s[1])]
    if with_accuracy:
        # The richest one, so a one-line summary does not shadow a full
        # report written beside it.
        return max(with_accuracy, key=lambda s: len(flat_text(s[1])))
    if seen:
        return seen[0]
    return None, None


def run_entry(scratch, entry, block_network=False, timeout=RUN_TIMEOUT_S):
    """Run one candidate entry point on a copy of the tree.

    A copy, because the eval writes reports and the delivered tree is
    the thing being graded: a grader must not leave its own artefacts
    in it, nor let one grader's run change what the next one sees.
    """
    work = Path(tempfile.mkdtemp(prefix="drill-aiml-"))
    try:
        tree = work / "tree"
        _copy_tree(scratch, tree)
        target = tree / Path(entry).relative_to(scratch)

        before = {}
        for path in walk(tree, {".json"}):
            before[path] = path.stat().st_mtime_ns, path.stat().st_size

        env = dict(os.environ)
        env["PYTHONPATH"] = os.pathsep.join(
            [str(tree)] + ([str(work / "block")] if block_network else [])
            + [env.get("PYTHONPATH", "")]).strip(os.pathsep)
        env.pop("PYTHONHOME", None)
        if block_network:
            (work / "block").mkdir(exist_ok=True)
            (work / "block" / "sitecustomize.py").write_text(
                _SITECUSTOMIZE, encoding="utf-8")

        if target.name == "__main__.py":
            cmd = [sys.executable, "-m", target.parent.name]
        else:
            cmd = [sys.executable, str(target)]

        started = time.time()
        try:
            proc = subprocess.run(cmd, cwd=str(tree), capture_output=True,
                                  text=True, encoding="utf-8",
                                  errors="replace", timeout=timeout, env=env)
            rc, out, err = proc.returncode, proc.stdout, proc.stderr
        except subprocess.TimeoutExpired:
            return Run(entry, rel(scratch, entry), None, "", "", timeout,
                       None, None, None)
        except OSError as exc:
            return Run(entry, rel(scratch, entry), None, "", str(exc),
                       time.time() - started, None, None, None)
        seconds = time.time() - started

        written = []
        for path in walk(tree, {".json"}):
            stamp = (path.stat().st_mtime_ns, path.stat().st_size)
            if before.get(path) == stamp:
                continue
            try:
                doc = json.loads(read(path))
            except ValueError:
                continue
            if isinstance(doc, dict):
                written.append((rel(tree, path), doc))

        source, report = _pick_report(out, written)
        return Run(entry, rel(scratch, entry), rc, out, err, seconds,
                   report, source, _missing_module(err, tree))
    finally:
        shutil.rmtree(work, ignore_errors=True)


def evaluate(scratch, block_network=False, timeout=RUN_TIMEOUT_S):
    """Find and run the eval entry point. Returns (run, tried).

    The chosen run is the first candidate that exits 0 and yields a
    report carrying an accuracy. Failing that, the most informative
    failure, so the reason a grader prints names what actually went
    wrong rather than the last thing tried.
    """
    tried = candidate_entries(scratch)
    best = None
    for entry in tried:
        run = run_entry(scratch, entry, block_network, timeout)
        if run.rc == 0 and run.report is not None and _has_accuracy(
                run.report):
            return run, tried
        rank = (
            0 if (run.rc == 0 and run.report is not None) else
            1 if run.rc == 0 else
            2 if run.missing_module else
            3 if run.rc is None else 4)
        if best is None or rank < best[0]:
            best = (rank, run)
    return (best[1] if best else None), tried


def require_run(cid, scratch, block_network=False):
    """The eval run, or an emitted verdict explaining why there is none."""
    run, tried = evaluate(scratch, block_network=block_network)
    if run is None:
        emit(cid, FAIL,
             "no eval entry point in the tree: no Python file is named for "
             "one or reports an accuracy, so there is nothing to run")
    if run.missing_module:
        emit(cid, UNSETTLED,
             "%s needs %r, which is not installed here, so the eval could "
             "not be run. That is a gap in this environment, not a finding "
             "against the delivered tree."
             % (run.rel, run.missing_module))
    if run.rc is None:
        emit(cid, FAIL,
             "%s did not finish inside %ds" % (run.rel, RUN_TIMEOUT_S))
    if run.rc != 0:
        last = (run.stderr or "").strip().splitlines()
        emit(cid, FAIL,
             "%s exits %d: %s" % (run.rel, run.rc,
                                  last[-1][:200] if last else "no stderr"))
    return run


def require_report(cid, scratch):
    run = require_run(cid, scratch)
    if run.report is None:
        emit(cid, FAIL,
             "%s exits 0 but prints no JSON object and writes no JSON "
             "report, so there is no machine readable output to check"
             % run.rel)
    return run


# --------------------------------------------------------- model ids


DATE_TAIL = re.compile(r"(?:^|[-_@:./])(\d{8}|\d{4}-\d{2}-\d{2})$")
MOVING = re.compile(
    r"^[A-Za-z][\w.]*(?:-[\w.]+)*-(?:latest|preview|stable|current|newest|"
    r"snapshot|edge)$", re.I)


def is_dated_id(value):
    """True when an identifier is pinned to a build date."""
    match = DATE_TAIL.search(str(value).strip())
    if not match:
        return False
    stamp = match.group(1).replace("-", "")
    year, month, day = stamp[:4], stamp[4:6], stamp[6:]
    return (2000 <= int(year) <= 2099 and 1 <= int(month) <= 12
            and 1 <= int(day) <= 31)


def is_moving_alias(value):
    return bool(MOVING.match(str(value).strip()))


MODEL_ASSIGN = re.compile(
    r"""(?ix)
    \b (?: [a-z0-9_]* model [a-z0-9_]* | deployment | engine )
    ["']? \s* [:=] \s*
    (?P<q>["']) (?P<value>[^"'\n]{2,80}) (?P=q)
    """)
MODEL_BARE = re.compile(
    r"""(?im)^ \s* [-\s]* (?:[a-z0-9_]*model[a-z0-9_]*|deployment)
    \s* : \s* (?P<value>[A-Za-z0-9][\w.:/@-]{2,80}) \s* $""",
    re.X)


def model_identifiers(scratch):
    """Every string the source hands over as a model identifier.

    `stub_client.py` is exempt. It is the vendored client, and the alias
    table in it mirrors what the endpoint publishes; the criterion is
    about what this repository pins when it calls out, which is the
    caller's string, not the vendor's menu.
    """
    found = []
    for path in walk(scratch, {".py", ".json", ".yaml", ".yml", ".toml",
                               ".cfg", ".ini", ".env", ".sh"}):
        if path.name == "stub_client.py":
            continue
        text = read(path)
        for match in MODEL_ASSIGN.finditer(text):
            found.append((rel(scratch, path), match.group("value")))
        for match in MODEL_BARE.finditer(text):
            found.append((rel(scratch, path), match.group("value")))
    out, seen = [], set()
    for where, value in found:
        value = value.strip()
        if not value or " " in value or value.lower() in (
                "none", "null", "true", "false"):
            continue
        if value.endswith((".txt", ".py", ".json", ".jsonl", ".md")):
            continue
        if (where, value) in seen:
            continue
        seen.add((where, value))
        out.append((where, value))
    return out


# ------------------------------------------------------------- classify


_CALL = """\
import json, sys
sys.path.insert(0, sys.argv[1])
mod = __import__(sys.argv[2])
fn = getattr(mod, "classify", None)
if fn is None or not callable(fn):
    print(json.dumps({"error": "no callable classify in %s" % sys.argv[2]}))
    sys.exit(3)
texts = json.loads(sys.stdin.read())
out = []
for text in texts:
    try:
        out.append(fn(text))
    except Exception as exc:
        out.append({"error": "%s: %s" % (type(exc).__name__, exc)})
print(json.dumps({"results": out}))
"""


def classify_modules(scratch):
    """Modules that define a public `classify` function."""
    out = []
    for path in walk(scratch, {".py"}):
        if re.search(r"^\s*def\s+classify\s*\(", read(path), re.M):
            out.append(path)
    out.sort(key=lambda p: (p.name != "classify.py", len(p.parts), str(p)))
    return out


ClassifyResult = namedtuple("ClassifyResult", "module results error missing")


def call_classify(scratch, texts):
    """Call the delivered `classify` on some tickets, on a copy of the tree."""
    modules = classify_modules(scratch)
    if not modules:
        return ClassifyResult(None, None, "no module defines a classify "
                                          "function", None)
    work = Path(tempfile.mkdtemp(prefix="drill-aiml-cls-"))
    try:
        tree = work / "tree"
        _copy_tree(scratch, tree)
        script = work / "call.py"
        script.write_text(_CALL, encoding="utf-8")
        last = None
        for module in modules:
            target = tree / Path(module).relative_to(scratch)
            env = dict(os.environ)
            env["PYTHONPATH"] = os.pathsep.join(
                [str(tree), env.get("PYTHONPATH", "")]).strip(os.pathsep)
            try:
                proc = subprocess.run(
                    [sys.executable, str(script), str(target.parent),
                     target.stem],
                    input=json.dumps(list(texts)), cwd=str(tree),
                    capture_output=True, text=True, encoding="utf-8",
                    errors="replace", timeout=RUN_TIMEOUT_S, env=env)
            except (OSError, subprocess.TimeoutExpired) as exc:
                last = ClassifyResult(rel(scratch, module), None, str(exc),
                                      None)
                continue
            missing = _missing_module(proc.stderr, tree)
            if proc.returncode != 0:
                err = (proc.stderr or "").strip().splitlines()
                last = ClassifyResult(rel(scratch, module), None,
                                      err[-1][:200] if err else "exit %d"
                                      % proc.returncode, missing)
                continue
            objects = _json_objects(proc.stdout)
            payload = objects[-1] if objects else {}
            if "results" not in payload:
                last = ClassifyResult(rel(scratch, module), None,
                                      payload.get("error", "no results"),
                                      missing)
                continue
            return ClassifyResult(rel(scratch, module), payload["results"],
                                  None, None)
        return last
    finally:
        shutil.rmtree(work, ignore_errors=True)
