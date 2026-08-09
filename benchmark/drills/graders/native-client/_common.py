"""Shared helpers for the native-client drill graders. Stdlib only.

Not a grader. The runner looks for `c<N>.py` by name, so this file is
never mistaken for a criterion.

Exit codes follow the grader contract: 0 pass, 1 fail, 2 the criterion
cannot be settled in this environment. The third exists because most of
these criteria are claims about behaviour rather than about text, and
the behaviour lives in a JavaScript core that only runs if Node is
installed. A machine without Node has not found the work broken; it has
not looked.

Two habits run through every grader here.

- **Nothing is written into the tree being graded.** Anything that has
  to mutate a file, and several of these criteria are only settled by
  mutating one, works on a copy in a temporary directory.
- **A probe drives the delivered core rather than reading it.** The
  probe imports the same surface the fixture's own committed tests
  import, `src/core/index.js`, so a tree that keeps its own suite green
  is not then tripped up by a grader inventing an API. Where that
  surface has gone the grader says so, and says it as a fact about the
  delivered tree.

The mutation habit is worth naming separately, because it is what
separates these graders from a grep. Several criteria say "a test
asserts X". A grader cannot read a test and know what it asserts, but it
can break X on a copy of the tree and require the suite to notice. A
suite that stays green when the booking policy is switched to
last-writer-wins is not asserting anything about the booking policy.
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

PACK = "native-client"

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".tern-data", "build",
             ".gradle", "Pods", ".venv", "venv", ".expo", "coverage"}

MARKER = "@@drill-nat-verdict@@"

# The write classes the brief names, and the policies it allows.
WRITE_CLASSES = ("notes", "preferences", "bookings")
POLICIES = ("converge", "last-writer-wins", "reserve-then-commit",
            "reject-offline")

DECISIONS = "CLIENT_DECISIONS.md"

_SUITE_TIMEOUT_S = 240


# ------------------------------------------------------------- plumbing


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


def repo_root():
    """The EOS repository this grader ships inside.

    graders/<pack>/_common.py -> graders/<pack> -> graders -> drills ->
    benchmark -> root.
    """
    return Path(__file__).resolve().parents[4]


def frozen_scenario():
    """The fixture as it shipped, so "added" can mean something."""
    return Path(__file__).resolve().parents[2] / "scenarios" / PACK


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


def find_named(root, basename):
    """Every file with this exact name, shallowest first."""
    root = Path(root)
    found = [p for p in iter_files(root) if p.name == basename]
    return sorted(found, key=lambda p: (len(p.relative_to(root).parts),
                                        p.as_posix()))


def rel(root, path):
    return Path(path).relative_to(root).as_posix()


def copy_tree(scratch, prefix):
    """A scratch copy of the delivered tree. The caller removes it."""
    work = Path(tempfile.mkdtemp(prefix=prefix))
    copy = work / "tree"
    shutil.copytree(
        scratch, copy,
        ignore=shutil.ignore_patterns(*sorted(SKIP_DIRS)))
    return work, copy


# --------------------------------------------------------------- node


def node_available():
    return shutil.which("node") is not None


def require_node(cid):
    if not node_available():
        emit(cid, UNSETTLED,
             "Node is not installed here, so the delivered client could "
             "not be run and this criterion was not settled. That is a gap "
             "in the environment, not a finding against the tree.")


def run(cmd, cwd, timeout=_SUITE_TIMEOUT_S):
    """Run a command. Returns (returncode_or_None, combined output)."""
    env = dict(os.environ)
    env["NO_COLOR"] = "1"
    env["FORCE_COLOR"] = "0"
    try:
        proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True,
                              text=True, encoding="utf-8", errors="replace",
                              timeout=timeout, env=env)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, str(exc)
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


_COUNT = re.compile(r"^#?\s*(?:ℹ\s*)?(tests|pass|fail)\s+(\d+)\s*$",
                    re.M)


def suite_counts(output):
    """The node test runner's own tally, as a dict."""
    return {name: int(value) for name, value in _COUNT.findall(output)}


def run_suite(tree, timeout=_SUITE_TIMEOUT_S):
    """Run the project's test suite. Returns (code, output, counts).

    `node --test` and nothing else: the fixture declares exactly that as
    `npm test`, the core has no dependencies, and running it through npm
    would need an install this grader has no right to perform.
    """
    node = shutil.which("node")
    code, output = run([node, "--test"], tree, timeout=timeout)
    return code, output, suite_counts(output)


def require_green_suite(cid, tree, what="this criterion"):
    """The delivered suite must pass before a mutation means anything.

    A tree whose tests are already red cannot be used to show that a
    broken invariant turns them red, so the grader reports the red suite
    rather than drawing a conclusion from it.
    """
    code, output, counts = run_suite(tree)
    if code is None:
        emit(cid, UNSETTLED,
             "the test suite could not be run here (%s), so %s was not "
             "settled" % (" ".join(output.split())[:200], what))
    if counts.get("tests", 0) == 0:
        emit(cid, FAIL,
             "`node --test` found no tests in the delivered tree, so there "
             "is nothing asserting anything")
    if code != 0:
        emit(cid, FAIL,
             "the delivered test suite is already failing (%d of %d tests), "
             "so %s cannot be settled against it: %s"
             % (counts.get("fail", 0), counts.get("tests", 0), what,
                " ".join(output.split())[-300:]))
    return counts


# --------------------------------------------------------------- probes


def core_entry(tree):
    """The core's public surface inside a tree, or None.

    The fixture puts it at `src/core/index.js` and its own tests import
    from there, so this is the surface a delivered tree is expected to
    keep. A moved core is still found; a deleted one is not, and the
    caller reports that as a fact about the tree.
    """
    tree = Path(tree)
    first = tree / "src" / "core" / "index.js"
    if first.is_file():
        return "./src/core/index.js"
    for path in iter_files(tree, suffixes={".js", ".mjs"}):
        parts = path.relative_to(tree).parts
        if path.stem == "index" and "core" in parts:
            return "./" + path.relative_to(tree).as_posix()
    return None


PROBE_PREAMBLE = '''\
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const MARKER = %(marker)r;

function report(good, reason, extra) {
  process.stdout.write(
    MARKER + JSON.stringify({ ok: !!good, reason: String(reason),
                              extra: extra || {} }) + "\\n");
  process.exit(0);
}

function ok(reason, extra) { report(true, reason, extra); }
function fail(reason, extra) { report(false, reason, extra); }

function scratch(tag) {
  return fs.mkdtempSync(path.join(os.tmpdir(), "drill-nat-" + tag + "-"));
}

function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }

let core;
try {
  core = await import(%(entry)r);
} catch (error) {
  fail("the core at %(entry)s did not import: " + (error && error.message));
}

function need(names) {
  const missing = names.filter((n) => typeof core[n] !== "function");
  if (missing.length) {
    fail("the core no longer exports " + missing.join(", ") +
         "; the fixture's own tests import these from %(entry)s, so a " +
         "tree that dropped them has changed the surface the app is on");
  }
  return names.map((n) => core[n]);
}
'''


def build_probe(entry, body):
    preamble = PROBE_PREAMBLE % {"marker": MARKER, "entry": entry}
    return (
        preamble
        + "\ntry {\n"
        + body.strip("\n")
        + "\n  fail('the probe ran to the end without reaching a verdict');\n"
        + "} catch (error) {\n"
        + "  fail('the delivered tree raised while being exercised: ' +\n"
        + "       (error && (error.stack || error.message) || error));\n"
        + "}\n"
    )


def run_probe(cid, scratch, body, timeout=180):
    """Drive the delivered core from outside. Returns (ok, reason, extra).

    The probe is written into a copy of the tree, never into the tree.
    `None` for ok means the probe reached no verdict at all, which is a
    fact about the delivered tree: it did not import, or it killed the
    interpreter.
    """
    require_node(cid)
    work, tree = copy_tree(scratch, "drill-nat-probe-")
    try:
        entry = core_entry(tree)
        if entry is None:
            return (None,
                    "no core entry point: the fixture ships one at "
                    "src/core/index.js and the delivered tree has none, so "
                    "there is nothing to drive", {})
        script = tree / "__drill_probe.mjs"
        script.write_text(build_probe(entry, body), encoding="utf-8")
        code, output = run([shutil.which("node"), str(script)], tree,
                           timeout=timeout)
        for line in reversed((output or "").splitlines()):
            if line.startswith(MARKER):
                try:
                    doc = json.loads(line[len(MARKER):])
                except ValueError:
                    continue
                return (bool(doc.get("ok")), str(doc.get("reason", "")),
                        doc.get("extra") or {})
        tail = " ".join((output or "").split())[-300:]
        return (None,
                "the probe reached no verdict (exit %s): %s"
                % (code, tail or "no output at all"), {})
    finally:
        shutil.rmtree(work, ignore_errors=True)


def settle(cid, scratch, body, timeout=180):
    good, reason, _ = run_probe(cid, scratch, body, timeout=timeout)
    if good is None:
        emit(cid, FAIL, reason)
    emit(cid, PASS if good else FAIL, reason)


# ------------------------------------------------------ the policy file


def policy_pairs(doc):
    """Every (json path, write class, policy) the document names.

    The brief fixes the class names and the policy vocabulary and says
    nothing about the file's shape, so this walks for the pairing rather
    than insisting on one layout. Three shapes turn up in practice: a
    class name keyed straight to a policy string, a class name keyed to
    an object carrying one, and a list of records naming both.
    """
    found = []

    def walk(node, path):
        if isinstance(node, dict):
            for key, value in node.items():
                here = path + (key,)
                if key in WRITE_CLASSES:
                    if isinstance(value, str) and value.strip() in POLICIES:
                        found.append((here, key, value.strip()))
                    elif isinstance(value, dict):
                        for sub, subvalue in value.items():
                            if (isinstance(subvalue, str)
                                    and subvalue.strip() in POLICIES):
                                found.append((here + (sub,), key,
                                              subvalue.strip()))
                walk(value, here)
            _record(node, path, found)
        elif isinstance(node, list):
            for i, value in enumerate(node):
                walk(value, path + (i,))

    walk(doc, ())
    # The same pair can be reached twice through nested shapes; keep one
    # entry per (class, json path).
    unique = {}
    for path, name, policy in found:
        unique.setdefault((name, path), (path, name, policy))
    return sorted(unique.values(), key=lambda row: (row[1], row[0]))


def _record(node, path, found):
    """A record naming its own class and its own policy."""
    if not isinstance(node, dict):
        return
    name = None
    for key in ("class", "write_class", "writeClass", "name", "id"):
        value = node.get(key)
        if isinstance(value, str) and value.strip() in WRITE_CLASSES:
            name = value.strip()
            break
    if name is None:
        return
    for key, value in node.items():
        if isinstance(value, str) and value.strip() in POLICIES:
            found.append((path + (key,), name, value.strip()))


def set_at(doc, path, value):
    node = doc
    for step in path[:-1]:
        node = node[step]
    node[path[-1]] = value


# ------------------------------------------------------ the JSON schema


class Unsupported(Exception):
    """A schema keyword this validator does not implement.

    Raised rather than ignored. A validator that skips what it does not
    understand reports a document as valid that it never checked, which
    is the one failure mode a grader must not have.
    """


_KNOWN = {
    "type", "enum", "const", "required", "properties", "additionalProperties",
    "patternProperties", "items", "minItems", "maxItems", "minProperties",
    "maxProperties", "minLength", "maxLength", "minimum", "maximum",
    "exclusiveMinimum", "exclusiveMaximum", "pattern", "uniqueItems",
    "$schema", "$id", "title", "description", "default", "examples",
    "$comment",
}

_TYPES = {"object": dict, "array": list, "string": str, "boolean": bool,
          "null": type(None)}


def looks_like_schema(doc):
    if not isinstance(doc, dict):
        return False
    if "$schema" in doc:
        return True
    return "properties" in doc and doc.get("type") in (None, "object")


def _is_type(value, name):
    if name == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if name == "boolean":
        return isinstance(value, bool)
    expected = _TYPES.get(name)
    if expected is None:
        raise Unsupported("type %r" % name)
    if expected is not bool and isinstance(value, bool):
        return False
    return isinstance(value, expected)


def validate(doc, schema, where="$"):
    """Violations of a draft 2020-12 subset, as readable strings."""
    if not isinstance(schema, dict):
        raise Unsupported("a non-object schema at %s" % where)
    unknown = set(schema) - _KNOWN
    if unknown:
        raise Unsupported("keyword(s) %s at %s"
                          % (", ".join(sorted(unknown)), where))

    errors = []

    if "type" in schema:
        names = schema["type"]
        names = names if isinstance(names, list) else [names]
        if not any(_is_type(doc, n) for n in names):
            return ["%s should be %s, found %s"
                    % (where, " or ".join(names), type(doc).__name__)]

    if "const" in schema and doc != schema["const"]:
        errors.append("%s should be %r" % (where, schema["const"]))
    if "enum" in schema and doc not in schema["enum"]:
        errors.append("%s should be one of %s, found %r"
                      % (where, ", ".join(repr(v) for v in schema["enum"]),
                         doc))

    if isinstance(doc, str):
        if "minLength" in schema and len(doc) < schema["minLength"]:
            errors.append("%s is shorter than %d characters"
                          % (where, schema["minLength"]))
        if "maxLength" in schema and len(doc) > schema["maxLength"]:
            errors.append("%s is longer than %d characters"
                          % (where, schema["maxLength"]))
        if "pattern" in schema and not re.search(schema["pattern"], doc):
            errors.append("%s does not match %s" % (where, schema["pattern"]))

    if isinstance(doc, (int, float)) and not isinstance(doc, bool):
        for key, test, word in (
                ("minimum", lambda a, b: a < b, "below"),
                ("maximum", lambda a, b: a > b, "above")):
            if key in schema and test(doc, schema[key]):
                errors.append("%s is %s %s" % (where, word, schema[key]))
        if ("exclusiveMinimum" in schema
                and doc <= schema["exclusiveMinimum"]):
            errors.append("%s must be above %s"
                          % (where, schema["exclusiveMinimum"]))
        if ("exclusiveMaximum" in schema
                and doc >= schema["exclusiveMaximum"]):
            errors.append("%s must be below %s"
                          % (where, schema["exclusiveMaximum"]))

    if isinstance(doc, dict):
        for name in schema.get("required", []):
            if name not in doc:
                errors.append("%s is missing required field %r"
                              % (where, name))
        if "minProperties" in schema and len(doc) < schema["minProperties"]:
            errors.append("%s has fewer than %d properties"
                          % (where, schema["minProperties"]))
        if "maxProperties" in schema and len(doc) > schema["maxProperties"]:
            errors.append("%s has more than %d properties"
                          % (where, schema["maxProperties"]))
        properties = schema.get("properties", {})
        patterns = schema.get("patternProperties", {})
        for name, value in doc.items():
            handled = False
            if name in properties:
                errors += validate(value, properties[name],
                                   "%s.%s" % (where, name))
                handled = True
            for pattern, subschema in patterns.items():
                if re.search(pattern, str(name)):
                    errors += validate(value, subschema,
                                       "%s.%s" % (where, name))
                    handled = True
            extra = schema.get("additionalProperties", True)
            if not handled and extra is False:
                errors.append("%s.%s is not allowed by the schema"
                              % (where, name))
            elif not handled and isinstance(extra, dict):
                errors += validate(value, extra, "%s.%s" % (where, name))

    if isinstance(doc, list):
        if "minItems" in schema and len(doc) < schema["minItems"]:
            errors.append("%s has fewer than %d items"
                          % (where, schema["minItems"]))
        if "maxItems" in schema and len(doc) > schema["maxItems"]:
            errors.append("%s has more than %d items"
                          % (where, schema["maxItems"]))
        if schema.get("uniqueItems") and len(doc) != len(
                {json.dumps(v, sort_keys=True) for v in doc}):
            errors.append("%s has repeated items" % where)
        if "items" in schema:
            for i, value in enumerate(doc):
                errors += validate(value, schema["items"],
                                   "%s[%d]" % (where, i))

    return errors


# -------------------------------------------------------- the ledger


EV = re.compile(r"\bEV-\d{3,5}\b")
FRAG = re.compile(r"\bFRAG-[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+\b")

LEDGER = "registry/evidence.json"
FRAGMENTS = "packs/*/research/*.fragment.json"


def _ids_in(doc):
    records = doc.get("records") if isinstance(doc, dict) else doc
    if not isinstance(records, list):
        return set()
    return {str(r.get("id")).strip() for r in records
            if isinstance(r, dict) and r.get("id")}


def resolvable_ids():
    """Every id the estate can resolve, and where the set came from.

    Read out of the repository this grader ships inside, not out of the
    tree being graded. A venture cannot make an id resolve by writing it
    down twice.
    """
    root = repo_root()
    found, sources = set(), []
    path = root / LEDGER
    if path.is_file():
        try:
            found |= _ids_in(json.loads(path.read_text(encoding="utf-8")))
            sources.append(LEDGER)
        except ValueError:
            pass
    for fragment in sorted(root.glob(FRAGMENTS)):
        try:
            found |= _ids_in(json.loads(fragment.read_text(encoding="utf-8")))
        except (OSError, ValueError):
            continue
        sources.append(fragment.relative_to(root).as_posix())
    return found, sources


# ------------------------------------------------------------- markup


TAG_START = re.compile(r"<([A-Z][A-Za-z0-9_.]*)")


def jsx_elements(text):
    """(tag, attribute text, body) for every capitalised JSX element.

    A scanner rather than a parser: it walks from the tag name to the
    `>` that closes the opening tag, counting braces, brackets and
    quotes so an expression containing a `>` does not end the tag early.
    The body is the source up to the matching close tag, which is enough
    to answer "does this control contain a Text child".
    """
    out = []
    for match in TAG_START.finditer(text):
        tag = match.group(1)
        i = match.end()
        depth, quote = 0, None
        self_closing = False
        while i < len(text):
            ch = text[i]
            if quote:
                if ch == quote:
                    quote = None
                i += 1
                continue
            if ch in "\"'`":
                quote = ch
            elif ch in "{[(":
                depth += 1
            elif ch in "}])":
                depth -= 1
            elif ch == ">" and depth <= 0:
                self_closing = text[i - 1] == "/"
                break
            i += 1
        attrs = text[match.end():i].rstrip("/")
        if self_closing or i >= len(text):
            out.append((tag, attrs, ""))
            continue
        close = text.find("</%s" % tag, i)
        body = text[i + 1:close] if close != -1 else text[i + 1:]
        out.append((tag, attrs, body))
    return out


def has_prop(attrs, name):
    return re.search(r"(?<![\w-])%s\s*=" % re.escape(name), attrs) is not None
