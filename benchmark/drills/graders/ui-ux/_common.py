"""Shared helpers for the ui-ux drill graders. Stdlib only.

Not a grader. The runner looks for `c<N>.py` by name, so this file is
never mistaken for a criterion.

Exit codes follow the grader contract: 0 pass, 1 fail, 2 the criterion
cannot be settled in this environment. The third is used sparingly and
only for a genuinely absent external tool, never to soften a finding.

Two ideas run through these graders.

The first is that a delivered tree is read on its own terms. The drill
brief names `surfaces/service/` and `surfaces/dashboard/` and
`tokens/tokens.json` and `DESIGN_DECISIONS.md`, so those paths are
fixed points. Everything else is discovered: the build entry point, the
test runner, the shared module path, the component files. A grader that
demanded one layout would be grading a guess about how the work was
organised rather than whether it was done.

The second is that presence is cheap and behaviour is not. Several of
these criteria are about tests that genuinely bite, and the only way to
settle that is to break the thing the test claims to cover and require
the suite to go red. Every mutation happens on a copy, so a grader that
dies midway cannot leave the delivered tree holding a probe.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PASS, FAIL, UNSETTLED = 0, 1, 2

SURFACES = ("service", "dashboard")

SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv",
             ".mypy_cache", ".pytest_cache", ".tox", ".idea", "site-packages"}

TEXT_EXTS = {".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".html",
             ".htm", ".css", ".scss", ".json", ".md", ".yml", ".yaml",
             ".txt", ".cfg", ".toml", ".ini", ".xml", ".svg"}

KEY_NAMES = ("Escape", "Enter", "ArrowDown", "ArrowUp", "ArrowLeft",
             "ArrowRight", "Home", "End", "Tab", "PageUp", "PageDown",
             "Space", "Spacebar")

STATE_NAMES = ("focus", "hover", "active", "disabled", "loading", "error")


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


def read(path):
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def rel(tree, path):
    try:
        return Path(path).relative_to(tree).as_posix()
    except ValueError:
        return str(path)


def iter_files(root, exts=None):
    root = Path(root)
    if not root.is_dir():
        return
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if exts and path.suffix.lower() not in exts:
            continue
        yield path


def copy_tree(tree, prefix="drill-uiux-"):
    """Copy the delivered tree somewhere a grader may vandalise it."""
    work = Path(tempfile.mkdtemp(prefix=prefix))
    copy = work / "tree"
    shutil.copytree(tree, copy,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    return work, copy


def run(argv, cwd, timeout=300):
    env = dict(os.environ)
    env["PYTHONPATH"] = str(cwd) + os.pathsep + env.get("PYTHONPATH", "")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        proc = subprocess.run(list(argv), cwd=str(cwd), capture_output=True,
                              text=True, encoding="utf-8", errors="replace",
                              timeout=timeout, env=env)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, str(exc)
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def short(text, limit=240):
    return " ".join(str(text or "").split())[:limit]


# ------------------------------------------------------- the build step


TOKEN_BUILD_CANDIDATES = (
    "tools/build_tokens.py", "tools/build-tokens.py", "tools/tokens.py",
    "scripts/build_tokens.py", "scripts/build-tokens.py",
    "tokens/build.py", "tokens/build_tokens.py", "build_tokens.py",
)

GENERAL_BUILD_CANDIDATES = (
    "tools/build.py", "scripts/build.py", "build.py", "make.py",
)


def build_commands(tree):
    """Every regeneration entry point this tree offers, in run order.

    Token-specific first, then the general build, because a repo that
    has both usually wires the first into the second and running them
    in that order is idempotent either way. Returns a list of
    (argv, label); empty means the tree offers no way to regenerate,
    which is a finding rather than a gap in this environment.
    """
    found = []
    for group in (TOKEN_BUILD_CANDIDATES, GENERAL_BUILD_CANDIDATES):
        for name in group:
            path = Path(tree) / name
            if path.is_file():
                found.append(([sys.executable, str(path)], name))
                break
    if not found:
        mk = Path(tree) / "Makefile"
        if mk.is_file() and shutil.which("make"):
            text = read(mk)
            for target in ("tokens", "build"):
                if re.search(r"^%s\s*:" % target, text, re.M):
                    found.append((["make", target], "make %s" % target))
                    break
        pkg = Path(tree) / "package.json"
        if pkg.is_file() and shutil.which("npm"):
            try:
                scripts = json.loads(read(pkg)).get("scripts", {})
            except ValueError:
                scripts = {}
            for name in ("build:tokens", "tokens", "build"):
                if name in scripts:
                    found.append((["npm", "run", name], "npm run %s" % name))
                    break
    return found


def run_build(tree):
    """Run every regeneration entry point. Returns (ok, label, output)."""
    commands = build_commands(tree)
    if not commands:
        return False, None, "no regeneration entry point in the tree"
    labels = []
    for argv, label in commands:
        labels.append(label)
        code, out = run(argv, tree)
        if code is None:
            return False, label, "could not run %s: %s" % (label, short(out))
        if code != 0:
            return False, label, "%s exited %d: %s" % (label, code, short(out))
    return True, ", ".join(labels), ""


# -------------------------------------------------------- the test suite


def suite_commands(tree):
    out = []
    tests = Path(tree) / "tests"
    if tests.is_dir() and any(tests.rglob("*.py")):
        out.append(([sys.executable, "-m", "unittest", "discover",
                     "-s", "tests", "-t", "."], "unittest discover -s tests"))
    if list(Path(tree).glob("test_*.py")) or (tests.is_dir()
                                              and any(tests.rglob("*.py"))):
        try:
            import pytest  # noqa: F401
            out.append(([sys.executable, "-m", "pytest", "-q"], "pytest -q"))
        except ImportError:
            pass
    pkg = Path(tree) / "package.json"
    if pkg.is_file() and shutil.which("npm"):
        try:
            scripts = json.loads(read(pkg)).get("scripts", {})
        except ValueError:
            scripts = {}
        if "test" in scripts:
            out.append((["npm", "test", "--silent"], "npm test"))
    return out


def green_suite(tree):
    """The first suite command that passes on this tree.

    Returns (argv, label, note). A suite that does not pass before a
    probe is applied cannot say anything about what the probe did, so
    callers treat a missing or red baseline as a finding.
    """
    commands = suite_commands(tree)
    if not commands:
        return None, None, "no test suite: nothing under tests/ and no npm test"
    last = ""
    for argv, label in commands:
        code, out = run(argv, tree)
        if code == 0:
            return argv, label, ""
        last = "%s exited %s: %s" % (label, code, short(out))
    return None, None, "the delivered test suite does not pass: %s" % last


def suite_fails_with(tree, mutate, prefix="drill-uiux-probe-"):
    """Apply `mutate` to a copy of the tree and report whether it goes red.

    `mutate(copy)` returns a description of what it broke, or None if
    it could not break anything, which is itself a finding: a probe
    with nothing to aim at means the thing the criterion is about is
    not there.

    Returns (went_red, description, detail).
    """
    work, copy = copy_tree(tree, prefix=prefix)
    try:
        argv, label, note = green_suite(copy)
        if argv is None:
            return None, None, note
        what = mutate(copy)
        if what is None:
            return None, None, "nothing to probe"
        code, out = run(argv, copy)
        return code != 0, what, short(out)
    finally:
        shutil.rmtree(work, ignore_errors=True)


# ----------------------------------------------------------- the tokens


TOKEN_SOURCE = "tokens/tokens.json"

DTCG_TYPES = {
    "color", "dimension", "fontFamily", "fontWeight", "duration",
    "cubicBezier", "number", "strokeStyle", "border", "transition",
    "shadow", "gradient", "typography", "string", "boolean",
}

RESERVED = {"$value", "$type", "$description", "$extensions", "$deprecated",
            "$schema"}

ALIAS = re.compile(r"^\{([^{}]+)\}$")


def token_source(tree):
    return Path(tree) / TOKEN_SOURCE


def _walk_tokens(node, path, inherited, tokens, errors):
    if not isinstance(node, dict):
        errors.append("%s is not a group or a token" % (".".join(path) or "root"))
        return
    own_type = node.get("$type", inherited)
    if "$value" in node:
        where = ".".join(path)
        if own_type is None:
            errors.append("%s has $value but no $type on it or any group "
                          "above it" % where)
        elif own_type not in DTCG_TYPES:
            errors.append("%s has an unknown $type %r" % (where, own_type))
        tokens[where] = {"type": own_type, "value": node["$value"]}
        for key in node:
            if key.startswith("$") and key not in RESERVED:
                errors.append("%s carries an unknown reserved key %r"
                              % (where, key))
        return
    for key, child in node.items():
        if key.startswith("$"):
            if key not in RESERVED:
                errors.append("%s carries an unknown reserved key %r"
                              % (".".join(path) or "root", key))
            continue
        if any(bad in key for bad in ".{}"):
            errors.append("%r is not a legal token or group name"
                          % ".".join(path + [key]))
            continue
        _walk_tokens(child, path + [key], own_type, tokens, errors)


def dtcg_check(doc):
    """Validate a parsed token document. Returns (tokens, errors)."""
    tokens, errors = {}, []
    _walk_tokens(doc, [], None, tokens, errors)
    for name, info in sorted(tokens.items()):
        value = info["value"]
        if isinstance(value, str):
            match = ALIAS.match(value.strip())
            if match:
                target = match.group(1).strip()
                if target not in tokens:
                    errors.append("%s aliases {%s}, which is not a token in "
                                  "this file" % (name, target))
                continue
        if info["type"] == "color" and isinstance(value, str):
            if not re.match(r"^#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|"
                            r"[0-9a-fA-F]{8})$", value.strip()):
                errors.append("%s is a color whose value %r is neither a hex "
                              "string nor an alias" % (name, short(value, 40)))
    return tokens, errors


def resolve_alias(tokens, name, seen=None):
    seen = seen or set()
    if name in seen or name not in tokens:
        return None
    value = tokens[name]["value"]
    if isinstance(value, str):
        match = ALIAS.match(value.strip())
        if match:
            return resolve_alias(tokens, match.group(1).strip(), seen | {name})
    return value


def generated_token_files(tree):
    """Files that look like generated token output, source excluded.

    A generated output is a file under a directory whose name marks it
    as built, or under `tokens/` and not the source, in a format a
    platform consumes. The set is confirmed by deleting it and building
    again, so a false positive here shows up as a build that does not
    reproduce it rather than as a silent pass.
    """
    tree = Path(tree)
    source = token_source(tree).resolve()
    built_markers = ("build", "generated", "gen", "dist", "_build", "out")
    found = []
    for path in iter_files(tree):
        if path.resolve() == source:
            continue
        parts = [p.lower() for p in path.relative_to(tree).parts]
        if path.suffix.lower() not in (".css", ".scss", ".less", ".js",
                                       ".mjs", ".ts", ".json", ".py", ".xml",
                                       ".swift", ".kt", ".dart", ".plist",
                                       ".h", ".yaml", ".yml"):
            continue
        under_tokens = "tokens" in parts[:-1]
        marked = any(m in parts[:-1] for m in built_markers)
        named = "token" in parts[-1] or parts[-1].startswith("_variables") \
            or parts[-1] in ("variables.css", "variables.scss")
        if (under_tokens and (marked or named)) or (marked and named):
            found.append(path)
    return sorted(found)


def platform_of(path):
    ext = Path(path).suffix.lower()
    return {".css": "css", ".scss": "css", ".less": "css", ".js": "js",
            ".mjs": "js", ".ts": "js", ".json": "json", ".py": "python",
            ".xml": "android", ".swift": "swift", ".kt": "android",
            ".dart": "dart", ".plist": "apple", ".h": "c",
            ".yaml": "yaml", ".yml": "yaml"}.get(ext, ext.lstrip("."))


# --------------------------------------------------------- the surfaces


def surface_dir(tree, name):
    return Path(tree) / "surfaces" / name


def missing_surfaces(tree):
    return [n for n in SURFACES if not surface_dir(tree, n).is_dir()]


def surface_files(tree, name, exts=None):
    return list(iter_files(surface_dir(tree, name), exts=exts))


def html_pages(tree, name):
    return [p for p in surface_files(tree, name, exts={".html", ".htm"})]


def built_pages(tree, name):
    """Built HTML for one surface, if the build wrote any."""
    out = []
    for path in iter_files(tree, exts={".html", ".htm"}):
        parts = [p.lower() for p in path.relative_to(Path(tree)).parts]
        if parts[0] in ("dist", "build", "_site", "public", "out") \
                and name in parts:
            out.append(path)
    return out


# --------------------------------------------------- references and imports


IMPORT_PATTERNS = (
    re.compile(r"""\bfrom\s+['"]([^'"]+)['"]"""),          # js: from '...'
    re.compile(r"""\brequire\(\s*['"]([^'"]+)['"]\s*\)"""),
    re.compile(r"""\bimport\(\s*['"]([^'"]+)['"]\s*\)"""),
    re.compile(r"""(?:src|href)\s*=\s*['"]([^'"]+)['"]"""),
    re.compile(r"""@import\s+(?:url\()?\s*['"]([^'"]+)['"]"""),
)

PY_FROM = re.compile(r"^\s*from\s+([\w.]+)\s+import\s+(.+)$", re.M)
PY_IMPORT = re.compile(r"^\s*import\s+([\w.]+(?:\s*,\s*[\w.]+)*)", re.M)


def _resolve_py(tree, dotted):
    parts = dotted.split(".")
    for cut in range(len(parts), 0, -1):
        base = Path(tree).joinpath(*parts[:cut])
        for candidate in (base.with_suffix(".py"), base / "__init__.py"):
            if candidate.is_file():
                return candidate
    return None


def referenced_files(tree, path):
    """Files inside the tree that `path` reaches for, resolved."""
    tree = Path(tree)
    text = read(path)
    found = set()
    for pattern in IMPORT_PATTERNS:
        for match in pattern.finditer(text):
            target = match.group(1).strip()
            if not target or target.startswith(("http:", "https:", "//",
                                                "data:", "mailto:", "#")):
                continue
            target = target.split("?")[0].split("#")[0]
            bases = [path.parent]
            if target.startswith("/"):
                bases = [tree]
                target = target.lstrip("/")
            for base in bases:
                for suffix in ("", ".js", ".mjs", ".ts", ".css", ".py"):
                    candidate = (base / (target + suffix)).resolve()
                    try:
                        candidate.relative_to(tree.resolve())
                    except ValueError:
                        continue
                    if candidate.is_file():
                        found.add(candidate)
                        break
    dotted_names = []
    for match in PY_FROM.finditer(text):
        package = match.group(1).strip()
        dotted_names.append(package)
        tail = match.group(2).replace("(", " ").replace(")", " ")
        for piece in tail.split(","):
            name = piece.strip().split(" as ")[0].strip()
            if name and name != "*" and re.match(r"^\w+$", name):
                dotted_names.append("%s.%s" % (package, name))
    for match in PY_IMPORT.finditer(text):
        for piece in match.group(1).split(","):
            dotted_names.append(piece.strip())
    for dotted in dotted_names:
        resolved = _resolve_py(tree, dotted)
        if resolved is not None:
            found.add(resolved.resolve())
    return found


def outward_references(tree, name):
    """What one surface reaches for outside its own directory."""
    tree = Path(tree)
    own = surface_dir(tree, name).resolve()
    out = set()
    for path in surface_files(tree, name):
        for target in referenced_files(tree, path):
            try:
                target.relative_to(own)
            except ValueError:
                out.add(target)
    return out


def shared_module_roots(tree, targets):
    """The top-level directories a set of referenced files sits under."""
    tree = Path(tree).resolve()
    roots = {}
    for target in targets:
        parts = target.relative_to(tree).parts
        if len(parts) < 2:
            continue
        if parts[0] in ("dist", "build", "docs", "tests", "tools",
                        "scripts", "_site"):
            continue
        roots.setdefault(parts[0], set()).add(target)
    return roots


# --------------------------------------------------------- state manifests


BRACKETED = re.compile(r"[\[\(]([^\[\]\(\)]{0,600})[\]\)]", re.S)


def states_manifest(text):
    """The bracketed literal in `text` that names the six states.

    Returns (whole_match, inner_text) or (None, None). Language
    agnostic on purpose: a Python list, a JS array and a JSON array all
    read the same way to a regex, and the criterion is about the six
    names being exported, not about the syntax carrying them.
    """
    for match in BRACKETED.finditer(text):
        inner = match.group(1)
        lowered = inner.lower()
        if all(('"%s"' % s) in lowered or ("'%s'" % s) in lowered
               for s in STATE_NAMES):
            return match.group(0), inner
    return None, None


def component_files(tree, roots):
    """Candidate component files under a shared root.

    A component file names a state, a key or an ARIA property, which is
    what separates a component from a helper or a constants module.
    """
    out = []
    for root in roots:
        for path in iter_files(root, exts={".py", ".js", ".mjs", ".ts",
                                           ".jsx", ".tsx"}):
            if path.name in ("__init__.py", "index.js", "index.ts"):
                if len(read(path).splitlines()) < 12:
                    continue
            text = read(path)
            if states_manifest(text)[0] is not None:
                out.append(path)
                continue
            if any(('"%s"' % k) in text or ("'%s'" % k) in text
                   for k in KEY_NAMES):
                out.append(path)
    return sorted(set(out))


# ------------------------------------------------------------- colour


def hex_to_rgb(value):
    value = value.strip().lstrip("#")
    if len(value) in (3, 4):
        value = "".join(c * 2 for c in value[:3])
    if len(value) >= 6:
        try:
            return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))
        except ValueError:
            return None
    return None


def luminance(rgb):
    out = []
    for channel in rgb:
        c = channel / 255.0
        out.append(c / 12.92 if c <= 0.04045
                   else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * out[0] + 0.7152 * out[1] + 0.0722 * out[2]


def contrast(rgb_a, rgb_b):
    a, b = luminance(rgb_a), luminance(rgb_b)
    lighter, darker = max(a, b), min(a, b)
    return (lighter + 0.05) / (darker + 0.05)
