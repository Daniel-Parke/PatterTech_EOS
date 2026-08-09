"""Shared helpers for the coding drill graders. Stdlib only.

Not a grader. The runner looks for `c<N>.py` by name, so this file is
never mistaken for a criterion.

Exit codes follow the grader contract: 0 pass, 1 fail, 2 the criterion
cannot be settled in this environment. The third code carries the
weight here, because four of these criteria drive `pytest`, three need
`git` history, and one needs `jscpd`. A machine without one of those
would otherwise report the agent's work as broken when the truth is
that nothing looked at it.

Several criteria are stated against "the original fixture commit". The
runner materialises the scenario and commits it as the first commit in
the scratch repository, so that commit is the root of the history and
is recovered here with `git archive`, never by touching the delivered
tree.
"""

import ast
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

PASS, FAIL, UNSETTLED = 0, 1, 2

SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__",
             ".pytest_cache", ".tox", "site-packages", ".mypy_cache"}

PYTEST_TIMEOUT_S = 300


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


def walk(root):
    """Every file in the tree, minus the noise directories."""
    root = Path(root)
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if SKIP_DIRS & set(path.parts):
            continue
        yield path


def parser_files(scratch):
    """Every `parser.py` the delivered tree carries."""
    return sorted(p for p in walk(scratch) if p.name == "parser.py")


def is_test_file(path):
    name = Path(path).name
    if not name.endswith(".py"):
        return False
    return name.startswith("test_") or name.endswith("_test.py")


def test_files(scratch):
    return sorted(p for p in walk(scratch) if is_test_file(p))


def rel(scratch, path):
    return Path(path).relative_to(scratch).as_posix()


# ------------------------------------------------------------------- git


def git_available():
    return shutil.which("git") is not None


def git(cwd, *args):
    proc = subprocess.run(["git", "-C", str(cwd), *args],
                          capture_output=True, text=True,
                          encoding="utf-8", errors="replace")
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def require_git(cid):
    if not git_available():
        emit(cid, UNSETTLED,
             "git is not on PATH here, so this criterion was not settled. "
             "That is a gap in the environment, not a finding against the "
             "delivered tree.")


def has_history(scratch):
    code, _ = git(scratch, "rev-parse", "--git-dir")
    if code != 0:
        return False
    code, _ = git(scratch, "rev-parse", "--verify", "HEAD")
    return code == 0


def commits(scratch):
    """Every commit reachable from HEAD, oldest first."""
    code, out = git(scratch, "rev-list", "--reverse", "HEAD")
    if code != 0:
        return []
    return [line.strip() for line in out.splitlines() if line.strip()]


def root_commit(scratch):
    """The fixture commit: the oldest root of the delivered history."""
    code, out = git(scratch, "rev-list", "--max-parents=0", "HEAD")
    if code != 0:
        return None
    roots = [line.strip() for line in out.splitlines() if line.strip()]
    return roots[-1] if roots else None


def commit_files(scratch, sha):
    """[(status, path)] for one commit, against its first parent."""
    code, out = git(scratch, "show", "--first-parent", "--name-status",
                    "--pretty=format:", "-M", sha)
    if code != 0:
        return []
    rows = []
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        rows.append((parts[0].strip(), parts[-1].strip()))
    return rows


def tree_at(scratch, sha, dest, name="tree"):
    """Unpack one commit's tree into `dest/name`. Returns (path, why)."""
    if sha is None:
        return None, "there is no commit to unpack"
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    archive = dest / ("%s.tar" % name)
    code, out = git(scratch, "archive", "--format=tar",
                    "-o", str(archive), sha)
    if code != 0:
        return None, "git archive of %s failed: %s" % (sha[:8],
                                                       " ".join(out.split())[:200])
    tree = dest / name
    tree.mkdir(parents=True, exist_ok=True)
    try:
        with tarfile.open(archive) as tar:
            try:
                tar.extractall(tree, filter="data")
            except TypeError:  # Python without extraction filters
                tar.extractall(tree)
    except (tarfile.TarError, OSError) as exc:
        return None, "could not unpack commit %s: %s" % (sha[:8], exc)
    return tree, "commit %s" % sha[:8]


def fixture_tree(scratch, dest):
    """Extract the fixture commit's tree into `dest`. Returns (path, why)."""
    sha = root_commit(scratch)
    if sha is None:
        return None, "the delivered tree has no git history to recover the fixture commit from"
    tree, why = tree_at(scratch, sha, dest, name="fixture")
    if tree is None:
        return None, why
    return tree, "fixture commit %s" % sha[:8]


def copy_tests_into(scratch, tree):
    """Put the delivered tests, and only those, beside the fixture code.

    Test files, `conftest.py` and everything under a `tests/` directory
    are copied. Nothing else is, so the fixture's own `parser.py` and
    `golden_input.txt` stay exactly as they were frozen.
    """
    copied = []
    for path in walk(scratch):
        relative = Path(rel(scratch, path))
        wanted = (is_test_file(path)
                  or path.name == "conftest.py"
                  or "tests" in relative.parts)
        if not wanted:
            continue
        if path.suffix not in (".py", ".ini", ".cfg", ".txt", ".json"):
            continue
        target = Path(tree) / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        copied.append(relative.as_posix())
    return copied


# ---------------------------------------------------------------- pytest


def pytest_available():
    try:
        import pytest  # noqa: F401
    except ImportError:
        return False
    return True


def require_pytest(cid):
    if not pytest_available():
        emit(cid, UNSETTLED,
             "pytest is not installed here, so this criterion was not "
             "settled. That is a gap in the environment, not a finding "
             "against the delivered tree.")


def run_pytest(cwd, args=()):
    """Run pytest in `cwd`. Returns (returncode_or_None, output)."""
    env = dict(os.environ)
    env["PYTHONPATH"] = str(cwd) + os.pathsep + env.get("PYTHONPATH", "")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    cmd = [sys.executable, "-m", "pytest", "-p", "no:cacheprovider",
           "--no-header", *args]
    try:
        proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True,
                              text=True, encoding="utf-8", errors="replace",
                              timeout=PYTEST_TIMEOUT_S, env=env)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, str(exc)
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


_COLLECTED = re.compile(r"collected\s+(\d+)\s+item")
_TOTALS = re.compile(r"(\d+)\s+(passed|failed|error|errors|skipped)")


def collected_count(output):
    match = _COLLECTED.search(output)
    if match:
        return int(match.group(1))
    total = 0
    seen = False
    for match in _TOTALS.finditer(output):
        total += int(match.group(1))
        seen = True
    return total if seen else None


# ------------------------------------------------------------ test bodies


def test_functions(path):
    """[(name, source)] for the module level test functions in a file.

    Class based tests are not read here. The criteria this feeds are
    about running one named test in two trees, and a plain function is
    the only shape that has a stable node id without importing the
    module, which a grader must not do.
    """
    text = read(path)
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []
    out = []
    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if not node.name.startswith("test"):
            continue
        source = ast.get_source_segment(text, node) or ""
        out.append((node.name, source))
    return out


def node_ids(scratch):
    """[(node_id, file_text, function_source)] for every test function."""
    found = []
    for path in test_files(scratch):
        text = read(path)
        for name, source in test_functions(path):
            found.append(("%s::%s" % (rel(scratch, path), name), text, source))
    return found


def run_one(tree, node_id):
    """Run a single test node id. Returns True when it passed."""
    code, output = run_pytest(tree, ["-q", node_id])
    return code == 0, output


# ------------------------------------------------------------------ probe
#
# The criteria are about what a caller of `parse_records` sees, not about
# what the source looks like, so the graders call it. A tree can carry
# every code shape a grep looks for and still drop a malformed numeric
# row on the floor: only the call settles that.
#
# The call happens in a subprocess with the delivered tree on the path.
# A grader never imports the tree it is grading into its own process.

GOLDEN_FALLBACK = (
    "# meter export\n"
    "2024-04-01 | North-Gate | 118.4 | kWh\n"
    "2024-04-02 | Yard Tap | 8.2 | m3\n"
    "2024-04-03 | Depot | 1,204.0 | kWh | 0.5\n"
)

# Both carry a field that is shaped like a number and is not one. The
# first breaks the value, the second the correction. Appended at the end
# of the text so that every earlier row keeps its line number, which is
# what makes "the row was dropped" a clean comparison.
MALFORMED_VALUE_ROW = "2024-04-05 | Depot | twelve | kWh"
MALFORMED_CORRECTION_ROW = "2024-04-05 | Depot | 100.0 | kWh | oops"

PROBE_TIMEOUT_S = 120

PROBE_SOURCE = '''\
"""Call parse_records in a delivered tree and report what came back."""

import importlib
import json
import sys


def load(candidates):
    for root, names in candidates:
        if root not in sys.path:
            sys.path.insert(0, root)
        for name in names:
            try:
                module = importlib.import_module(name)
            except BaseException:
                continue
            func = getattr(module, "parse_records", None)
            if callable(func):
                return name, func
    return None, None


def call(func, text):
    try:
        out = func(text)
    except BaseException as exc:
        return {"raised": type(exc).__name__,
                "mro": [cls.__name__ for cls in type(exc).__mro__],
                "message": str(exc)[:300]}
    try:
        shown = repr(out)
    except BaseException:
        shown = "<no repr>"
    try:
        size = len(out)
    except BaseException:
        size = None
    return {"raised": None, "repr": shown[:6000], "count": size}


def main():
    with open(sys.argv[1], encoding="utf-8") as handle:
        spec = json.load(handle)
    name, func = load(spec["candidates"])
    if func is None:
        print(json.dumps({"ok": False,
                          "error": "parse_records could not be imported"}))
        return
    calls = {}
    for key, text in spec["texts"].items():
        calls[key] = call(func, text)
    print(json.dumps({"ok": True, "module": name, "calls": calls}))


main()
'''


def defines_parse_records(path):
    text = read(path)
    if "parse_records" not in text:
        return False
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return False
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name == "parse_records":
                return True
    return False


def import_candidates(tree):
    """[(sys.path root, [module names])] that may hold `parse_records`.

    Found by structure, so a tree that renamed the module or moved it
    into a package is still called rather than failed.
    """
    tree = Path(tree)
    found = []
    seen = set()
    sources = [p for p in walk(tree)
               if p.suffix == ".py" and not is_test_file(p)
               and defines_parse_records(p)]
    sources.sort(key=lambda p: (p.name != "parser.py", str(p)))
    for path in sources:
        package = path.parent
        while (package / "__init__.py").is_file() and package != tree \
                and package.parent != package:
            package = package.parent
        try:
            dotted = ".".join(path.relative_to(package).with_suffix("").parts)
        except ValueError:
            continue
        names = [dotted]
        if "." in dotted:
            names.append(dotted.rsplit(".", 1)[0])
        key = (str(package), tuple(names))
        if key in seen:
            continue
        seen.add(key)
        found.append([str(package), names])
    return found


def golden_text(tree):
    """The well-formed export, as this tree carries it."""
    for path in walk(tree):
        if path.name == "golden_input.txt":
            text = read(path)
            if text.strip():
                return text
    return GOLDEN_FALLBACK


def frozen_golden(scratch):
    """The export as it was frozen, not as the delivered tree left it.

    A tree that added a bad row to `golden_input.txt` would otherwise
    make its own well-formed input malformed, and the probe would read
    the resulting raise as a change in behaviour for good input.
    """
    if git_available() and has_history(scratch):
        work = Path(tempfile.mkdtemp(prefix="drill-coding-golden-"))
        try:
            tree, _ = fixture_tree(scratch, work)
            if tree is not None:
                for path in walk(tree):
                    if path.name == "golden_input.txt":
                        text = read(path)
                        if text.strip():
                            return text
        finally:
            shutil.rmtree(work, ignore_errors=True)
    return golden_text(scratch)


def probe(tree, texts):
    """Call `parse_records` in `tree` on each named text. Returns a dict."""
    candidates = import_candidates(tree)
    if not candidates:
        return {"ok": False,
                "error": "no module in the tree defines parse_records"}
    work = Path(tempfile.mkdtemp(prefix="drill-coding-probe-"))
    try:
        spec = work / "spec.json"
        spec.write_text(json.dumps({"candidates": candidates,
                                    "texts": texts}), encoding="utf-8")
        script = work / "probe.py"
        script.write_text(PROBE_SOURCE, encoding="utf-8")
        env = dict(os.environ)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        try:
            proc = subprocess.run(
                [sys.executable, str(script), str(spec)], cwd=str(tree),
                capture_output=True, text=True, encoding="utf-8",
                errors="replace", timeout=PROBE_TIMEOUT_S, env=env)
        except (OSError, subprocess.TimeoutExpired) as exc:
            return {"ok": False, "error": "calling parse_records failed: %s" % exc}
        for line in reversed((proc.stdout or "").splitlines()):
            line = line.strip()
            if line.startswith("{"):
                try:
                    return json.loads(line)
                except ValueError:
                    continue
        noise = " ".join(((proc.stdout or "") + (proc.stderr or "")).split())
        return {"ok": False,
                "error": "the call printed nothing readable: %s" % noise[:300]}
    finally:
        shutil.rmtree(work, ignore_errors=True)


def malformed_probe(tree):
    """Call `parse_records` on clean text and on the same text plus a bad row."""
    clean = frozen_golden(tree)
    if not clean.endswith("\n"):
        clean += "\n"
    return probe(tree, {
        "clean": clean,
        "bad_value": clean + MALFORMED_VALUE_ROW + "\n",
        "bad_correction": clean + MALFORMED_CORRECTION_ROW + "\n",
    })


BAD_ROWS = {"bad_value": MALFORMED_VALUE_ROW,
            "bad_correction": MALFORMED_CORRECTION_ROW}


def read_malformed(result):
    """Sort a probe into (raised, dropped, unclear). Each is a list of keys.

    `raised`   the call put an exception in front of the caller.
    `dropped`  the call returned exactly what it returns without the bad
               row, which is the defect the drill exists to detect.
    `unclear`  the call returned something else. Whether that counts as
               telling the caller is not a thing a script can judge.
    """
    calls = result.get("calls", {})
    clean = calls.get("clean", {})
    raised, dropped, unclear = [], [], []
    for key in BAD_ROWS:
        call = calls.get(key, {})
        if call.get("raised"):
            raised.append(key)
        elif call.get("repr") is not None and call.get("repr") == clean.get("repr"):
            dropped.append(key)
        else:
            unclear.append(key)
    return raised, dropped, unclear


def raised_names(result):
    """Every exception name a caller could catch, from the probe's own MRO."""
    names = []
    for key in BAD_ROWS:
        call = result.get("calls", {}).get(key, {})
        for name in call.get("mro") or []:
            if name in ("object", "BaseException"):
                continue
            if name not in names:
                names.append(name)
    return names
