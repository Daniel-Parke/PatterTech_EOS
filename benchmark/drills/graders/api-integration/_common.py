"""Shared helpers for the api-integration drill graders. Stdlib only.

Not a grader. The runner looks for `c<N>.py` by name, so this file is
never mistaken for a criterion.

Exit codes follow the grader contract: 0 pass, 1 fail, 2 the criterion
cannot be settled in this environment. The third exists because two of
these criteria reach for tools that may not be installed (an OpenAPI
diff tool, the repository's own check script), and a machine without
them would otherwise report the agent's work as broken when the truth
is that nothing looked at it.

There is no YAML parser in the standard library, so one lives here. It
reads the block subset OpenAPI documents are written in, plus flow
sequences and mappings, quoted keys and block scalars. PyYAML is used
instead when it happens to be installed, because it is more complete;
the bundled reader is the floor, not the preference. Anchors, aliases,
merge keys and multi-document streams are not supported by the bundled
reader and raise, which surfaces as an honest parse failure rather than
a wrong verdict.

Two known differences from PyYAML, both checked against these fixtures
and neither reachable by any criterion here, because no criterion reads
prose out of the document:

- inside a block scalar, blank lines are dropped and the trailing
  newline is not kept, so a description reads as its non-empty lines;
- bare `on`, `yes` and `off` stay strings, which is YAML 1.2 and
  OpenAPI 3.1, where PyYAML follows YAML 1.1 and returns booleans.
"""

import ast
import io
import json
import os
import re
import sys
import tokenize
from pathlib import Path

PASS, FAIL, UNSETTLED = 0, 1, 2

SPEC_REL = "api/openapi.yaml"
BASELINE_REL = "api/baseline/openapi.yaml"

SOURCE_EXTS = (".py", ".js", ".mjs", ".cjs", ".ts", ".rb", ".go", ".java")
SKIP_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv", "env",
    "dist", "build", ".tox", ".mypy_cache", ".pytest_cache", ".ruff_cache",
    "site-packages", ".idea", ".gradle", "target",
}


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


# ------------------------------------------------------------------ yaml


class YamlError(Exception):
    """The document could not be read as YAML."""


_TRUE = {"true", "yes", "on"}
_FALSE = {"false", "no", "off"}
_NULL = {"null", "~"}
_BLOCK = {"|", ">", "|-", ">-", "|+", ">+"}


class _Line(object):
    __slots__ = ("indent", "text", "n")

    def __init__(self, indent, text, n):
        self.indent = indent
        self.text = text
        self.n = n


def _strip_comment(text):
    quote = None
    for i, ch in enumerate(text):
        if quote:
            if ch == quote:
                quote = None
            continue
        if ch in "'\"":
            quote = ch
            continue
        if ch == "#" and (i == 0 or text[i - 1] in " \t"):
            return text[:i]
    return text


def _prepare(text):
    lines = []
    for n, raw in enumerate(text.splitlines(), 1):
        body = _strip_comment(raw).rstrip()
        if not body.strip():
            continue
        stripped = body.lstrip(" ")
        if "\t" in body[:len(body) - len(stripped)]:
            raise YamlError("tab in the indentation at line %d" % n)
        if stripped in ("---", "..."):
            continue
        lines.append(_Line(len(body) - len(stripped), stripped, n))
    return lines


def _find_colon(text):
    """Index of the key separator, or None when the line carries no key."""
    quote = None
    depth = 0
    for i, ch in enumerate(text):
        if quote:
            if ch == quote:
                quote = None
            continue
        if ch in "'\"":
            quote = ch
            continue
        if ch in "[{":
            depth += 1
            continue
        if ch in "]}":
            depth -= 1
            continue
        if ch == ":" and depth == 0 and (i + 1 == len(text)
                                         or text[i + 1] in " \t"):
            return i
    return None


def _unquote(text):
    text = text.strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "'\"":
        inner = text[1:-1]
        if text[0] == "'":
            return inner.replace("''", "'")
        return inner.replace('\\"', '"').replace("\\n", "\n")
    return text


def _scalar(text):
    text = text.strip()
    if not text:
        return None
    if text[0] in "[{":
        value, end = _flow(text, 0)
        return value
    if text[0] in "'\"":
        return _unquote(text)
    if text[0] in "&*":
        raise YamlError("anchors and aliases are not supported: %r" % text)
    low = text.lower()
    if low in _TRUE:
        return True
    if low in _FALSE:
        return False
    if low in _NULL:
        return None
    try:
        return int(text)
    except ValueError:
        pass
    try:
        return float(text)
    except ValueError:
        pass
    return text


def _skip_space(text, i):
    while i < len(text) and text[i] in " \t":
        i += 1
    return i


def _flow(text, i):
    i = _skip_space(text, i)
    if i >= len(text):
        raise YamlError("empty flow value")
    if text[i] == "[":
        out = []
        i += 1
        while True:
            i = _skip_space(text, i)
            if i >= len(text):
                raise YamlError("unterminated flow sequence")
            if text[i] == "]":
                return out, i + 1
            value, i = _flow(text, i)
            out.append(value)
            i = _skip_space(text, i)
            if i < len(text) and text[i] == ",":
                i += 1
    if text[i] == "{":
        out = {}
        i += 1
        while True:
            i = _skip_space(text, i)
            if i >= len(text):
                raise YamlError("unterminated flow mapping")
            if text[i] == "}":
                return out, i + 1
            key, i = _flow_token(text, i, ":,}")
            i = _skip_space(text, i)
            if i < len(text) and text[i] == ":":
                i += 1
                value, i = _flow(text, i)
            else:
                value = None
            out[str(key)] = value
            i = _skip_space(text, i)
            if i < len(text) and text[i] == ",":
                i += 1
    return _flow_token(text, i, ",]}")


def _flow_token(text, i, stops):
    if text[i] in "'\"":
        quote = text[i]
        j = i + 1
        while j < len(text) and text[j] != quote:
            j += 1
        if j >= len(text):
            raise YamlError("unterminated quoted scalar")
        return _unquote(text[i:j + 1]), j + 1
    if text[i] in "[{":
        return _flow(text, i)
    j = i
    while j < len(text) and text[j] not in stops:
        j += 1
    return _scalar(text[i:j]), j


def _node(lines, i):
    base = lines[i].indent
    text = lines[i].text
    if text == "-" or text.startswith("- "):
        return _sequence(lines, i, base)
    if _find_colon(text) is not None:
        return _mapping(lines, i, base)
    if len(lines) - i == 1:
        return _scalar(text), i + 1
    parts = []
    while i < len(lines) and lines[i].indent >= base:
        parts.append(lines[i].text)
        i += 1
    return " ".join(parts), i


def _sequence(lines, i, base):
    out = []
    while (i < len(lines) and lines[i].indent == base
           and (lines[i].text == "-" or lines[i].text.startswith("- "))):
        text = lines[i].text
        rest = text[1:].lstrip(" ")
        column = base + 1 + (len(text) - 1 - len(rest))
        n = lines[i].n
        i += 1
        sub = [_Line(column, rest, n)] if rest else []
        while i < len(lines) and lines[i].indent > base:
            sub.append(lines[i])
            i += 1
        if not sub:
            out.append(None)
            continue
        value, used = _node(sub, 0)
        if used != len(sub):
            raise YamlError("could not read the list item at line %d" % n)
        out.append(value)
    return out, i


def _mapping(lines, i, base):
    out = {}
    while i < len(lines) and lines[i].indent == base:
        line = lines[i]
        at = _find_colon(line.text)
        if at is None:
            raise YamlError("expected a key at line %d: %r"
                            % (line.n, line.text[:60]))
        key = _unquote(line.text[:at])
        rest = line.text[at + 1:].strip()
        i += 1
        if rest in _BLOCK:
            block = []
            while i < len(lines) and lines[i].indent > base:
                block.append(lines[i].text)
                i += 1
            out[key] = ("\n" if rest.startswith("|") else " ").join(block)
            continue
        if rest == "":
            sub = []
            while i < len(lines) and lines[i].indent > base:
                sub.append(lines[i])
                i += 1
            if not sub:
                out[key] = None
                continue
            value, used = _node(sub, 0)
            if used != len(sub):
                raise YamlError("could not read the block under %r at line %d"
                                % (key, line.n))
            out[key] = value
            continue
        out[key] = _scalar(rest)
        if i < len(lines) and lines[i].indent > base:
            raise YamlError("unexpected indented block after %r at line %d"
                            % (key, line.n))
    if i < len(lines) and lines[i].indent > base:
        raise YamlError("unexpected indentation at line %d" % lines[i].n)
    return out, i


def parse_yaml(text):
    """Read the block YAML subset OpenAPI documents are written in."""
    lines = _prepare(text)
    if not lines:
        return None
    value, used = _node(lines, 0)
    if used != len(lines):
        raise YamlError("unexpected content at line %d" % lines[used].n)
    return value


def load_yaml(path):
    """Parse a YAML file, preferring PyYAML when it is installed."""
    text = read(path)
    if not text.strip():
        raise YamlError("the file is empty")
    try:
        import yaml
    except ImportError:
        return parse_yaml(text)
    try:
        return yaml.safe_load(text)
    except Exception as exc:  # yaml.YAMLError, but keep the import optional
        raise YamlError(" ".join(str(exc).split())[:300])


# ------------------------------------------------------------------ spec


def spec_path(scratch):
    return Path(scratch) / SPEC_REL


def load_spec(cid, scratch):
    """The delivered API document, or a failed criterion saying why not."""
    path = spec_path(scratch)
    if not path.is_file():
        emit(cid, FAIL, "no %s in the delivered tree" % SPEC_REL)
    try:
        doc = load_yaml(path)
    except YamlError as exc:
        emit(cid, FAIL, "%s does not parse: %s" % (SPEC_REL, exc))
    if not isinstance(doc, dict):
        emit(cid, FAIL, "%s is not a mapping at the top level" % SPEC_REL)
    return doc


def walk(node):
    """Every mapping and list in the document, depth first."""
    yield node
    if isinstance(node, dict):
        for value in node.values():
            for item in walk(value):
                yield item
    elif isinstance(node, list):
        for value in node:
            for item in walk(value):
                yield item


def resolve(doc, node, seen=None):
    """Follow a local $ref chain. Foreign refs are returned untouched."""
    seen = seen or set()
    while isinstance(node, dict) and isinstance(node.get("$ref"), str):
        ref = node["$ref"]
        if not ref.startswith("#/") or ref in seen:
            return node
        seen.add(ref)
        target = doc
        for part in ref[2:].split("/"):
            part = part.replace("~1", "/").replace("~0", "~")
            if isinstance(target, dict) and part in target:
                target = target[part]
            elif isinstance(target, list) and part.isdigit():
                target = target[int(part)]
            else:
                return node
        node = target
    return node


def paths_of(doc):
    paths = doc.get("paths")
    return paths if isinstance(paths, dict) else {}


def orders_path(doc):
    """The path item for the order collection, whatever it is prefixed by.

    `/orders` is the name in the change request. A tree that versions by
    URL may serve it at `/v2/orders`, so the collection is found by its
    tail rather than by an exact match, and the exact match wins when
    both are present.
    """
    paths = paths_of(doc)
    if "/orders" in paths:
        return "/orders", paths["/orders"]
    for key in sorted(paths):
        if re.match(r"^(/v\d+)?/orders/?$", str(key)):
            return key, paths[key]
    return None, None


def collection_paths(doc):
    """Every order collection path, so a versioned pair is not missed."""
    out = []
    for key, item in sorted(paths_of(doc).items()):
        if re.match(r"^(/v\d+)?/orders/?$", str(key)):
            out.append((key, item))
    return out


def operation(item, method):
    if not isinstance(item, dict):
        return None
    op = item.get(method)
    return op if isinstance(op, dict) else None


def parameters(doc, item, op):
    """Path level and operation level parameters, refs resolved."""
    out = []
    for holder in (item, op):
        if not isinstance(holder, dict):
            continue
        for param in holder.get("parameters") or []:
            param = resolve(doc, param)
            if isinstance(param, dict):
                out.append(param)
    return out


def media_types(doc):
    """Every media type key that appears under a `content` mapping."""
    out = set()
    for node in walk(doc):
        if isinstance(node, dict) and isinstance(node.get("content"), dict):
            out.update(str(k) for k in node["content"])
    return out


VERSION_PARAM = re.compile(
    r"^(x[-_])?(api[-_]?)?(accept[-_]?)?version$", re.I)
VERSIONED_MEDIA = re.compile(r"vnd\.[^;]*[.+\-]v\d+|version\s*=", re.I)
VERSIONED_SCHEMA = re.compile(r"[a-z0-9]v(\d+)$", re.I)


def version_signals(doc):
    """Ways the document tells a caller which version it is talking to.

    Returned as a list of (kind, detail). The order is the order of
    strength: a URL prefix or a version header discriminates a request,
    a versioned schema name only labels a shape, and the reason string
    says which one was found so a reader can weigh it.
    """
    out = []
    for key in sorted(paths_of(doc)):
        if re.match(r"^/v\d+(/|$)", str(key)):
            out.append(("URL version prefix", str(key)))
            break
    for node in walk(doc):
        if not isinstance(node, dict):
            continue
        name = node.get("name")
        if (node.get("in") in ("header", "query") and isinstance(name, str)
                and VERSION_PARAM.match(name.strip())):
            out.append(("%s parameter" % node["in"], name.strip()))
            break
    for media in sorted(media_types(doc)):
        if VERSIONED_MEDIA.search(media):
            out.append(("versioned media type", media))
            break
    for node in walk(doc):
        if isinstance(node, dict) and isinstance(node.get("discriminator"),
                                                 dict):
            prop = str(node["discriminator"].get("propertyName", ""))
            if "version" in prop.lower():
                out.append(("schema discriminator", prop))
                break
    schemas = (doc.get("components") or {}).get("schemas")
    if isinstance(schemas, dict):
        versioned = sorted(n for n in schemas
                           if VERSIONED_SCHEMA.search(str(n)))
        if len(versioned) >= 2:
            out.append(("versioned schema names", ", ".join(versioned[:4])))
    return out


def properties_maps(doc):
    """Every `properties` mapping in the document, with its owner."""
    for node in walk(doc):
        if isinstance(node, dict) and isinstance(node.get("properties"), dict):
            yield node, node["properties"]


def required_lists(doc):
    for node in walk(doc):
        if isinstance(node, dict) and isinstance(node.get("required"), list):
            yield node, [str(v) for v in node["required"]]


# --------------------------------------------------------------- sources


def is_test_path(rel):
    lowered = rel.lower()
    parts = lowered.split("/")
    if any(p in ("test", "tests", "spec", "specs", "__tests__")
           for p in parts[:-1]):
        return True
    name = parts[-1]
    return (name.startswith("test_") or name.startswith("test.")
            or "_test." in name or ".test." in name or ".spec." in name
            or name.startswith("conftest"))


def source_files(scratch, exts=SOURCE_EXTS, include_tests=False):
    out = []
    root = Path(scratch)
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in sorted(filenames):
            path = Path(dirpath) / name
            if path.suffix.lower() not in exts:
                continue
            rel = path.relative_to(root).as_posix()
            if not include_tests and is_test_path(rel):
                continue
            out.append((rel, path))
    return sorted(out)


WEBHOOK_HINT = re.compile(
    r"webhook|signature|\bhmac\b|x-hub-signature|payment[_-]?event", re.I)


def handler_sources(scratch):
    """Source files that plausibly carry the webhook receiver.

    Test files are excluded on purpose. A test asserting that signatures
    are compared in constant time is not a handler that compares them,
    and a criterion satisfied by its own test measures nothing.
    """
    out = []
    for rel, path in source_files(scratch):
        text = read(path)
        if WEBHOOK_HINT.search(rel) or WEBHOOK_HINT.search(text):
            out.append((rel, path, text))
    return out


CI_GLOBS = (
    ".github/workflows/*.yml", ".github/workflows/*.yaml",
    ".gitlab-ci.yml", ".gitlab-ci.yaml",
    ".pre-commit-config.yaml", ".pre-commit-config.yml",
    "Makefile", "makefile", "justfile", "Justfile",
    "noxfile.py", "tox.ini", "package.json",
    ".circleci/config.yml", "azure-pipelines.yml", "Jenkinsfile",
    "scripts/*", "ci/*", "bin/*", ".buildkite/*.yml",
)


def ci_files(scratch):
    """Committed automation files, as (relative path, text) pairs.

    The text is returned as written. Callers that ask whether something
    is invoked strip the comments first, with `strip_comments`, because
    a tool named in a TODO is not a tool that runs."""
    out = []
    seen = set()
    root = Path(scratch)
    for pattern in CI_GLOBS:
        for path in sorted(root.glob(pattern)):
            if not path.is_file():
                continue
            rel = path.relative_to(root).as_posix()
            # Case-insensitive filesystems answer both Makefile and
            # makefile with the same file, so identity is the resolved
            # path rather than the spelling the glob was written in.
            key = str(path.resolve()).lower()
            if key in seen:
                continue
            seen.add(key)
            out.append((rel, read(path)))
    return out


# -------------------------------------------------------------- comments


def _line_offsets(text):
    out = [0]
    for line in text.splitlines(True):
        out.append(out[-1] + len(line))
    return out


_LITERAL_TOKENS = {tokenize.COMMENT, tokenize.STRING}
for _name in ("FSTRING_START", "FSTRING_MIDDLE", "FSTRING_END"):
    if hasattr(tokenize, _name):
        _LITERAL_TOKENS.add(getattr(tokenize, _name))


def strip_python_literals(text):
    """Blank comments and string literals, every other column kept.

    A docstring saying the signature is compared in constant time is a
    claim about the code, not the code. Returns None when the file does
    not tokenise, so the caller can say it could not look rather than
    grade what it could not read.
    """
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(text).readline))
    except (tokenize.TokenError, IndentationError, SyntaxError, ValueError):
        return None
    chars = list(text)
    starts = _line_offsets(text)
    for tok in tokens:
        if tok.type not in _LITERAL_TOKENS:
            continue
        if tok.start[0] - 1 >= len(starts) or tok.end[0] - 1 >= len(starts):
            continue
        begin = starts[tok.start[0] - 1] + tok.start[1]
        end = min(starts[tok.end[0] - 1] + tok.end[1], len(chars))
        for i in range(begin, end):
            if chars[i] != "\n":
                chars[i] = " "
    return "".join(chars)


def strip_hash_comments(text):
    """`#` comments removed, quoting respected, layout kept."""
    return "\n".join(_strip_comment(line) for line in text.splitlines())


_SLASH_BLOCK = re.compile(r"/\*.*?\*/", re.S)


def strip_slash_comments(text):
    text = _SLASH_BLOCK.sub(
        lambda m: re.sub(r"[^\n]", " ", m.group(0)), text)
    out = []
    for line in text.splitlines():
        quote = None
        cut = None
        for i, ch in enumerate(line):
            if quote:
                if ch == quote:
                    quote = None
                continue
            if ch in "'\"`":
                quote = ch
                continue
            if ch == "/" and line[i + 1:i + 2] == "/":
                cut = i
                break
        out.append(line if cut is None else line[:cut])
    return "\n".join(out)


SLASH_EXTS = (".js", ".mjs", ".cjs", ".ts", ".go", ".java", ".groovy")
SLASH_NAMES = ("jenkinsfile",)


def strip_comments(rel, text):
    """Comment and string prose removed, so a hit has to be code.

    JSON has no comments and is returned as written. A Python file that
    will not tokenise is returned as written too, and the caller is told
    by `python_literals_read` whether the stripping happened.
    """
    name = rel.rsplit("/", 1)[-1].lower()
    suffix = ("." + name.rsplit(".", 1)[-1]) if "." in name else ""
    if suffix == ".json":
        return text
    if suffix == ".py":
        return strip_python_literals(text) or text
    if suffix in SLASH_EXTS or name in SLASH_NAMES:
        return strip_slash_comments(text)
    return strip_hash_comments(text)


def python_literals_read(text):
    return strip_python_literals(text) is not None


# -------------------------------------------------------- reading python
#
# Two criteria turn on what a webhook handler does and in what order, so
# the handler is read as a syntax tree and its calls are followed into
# the functions they name. Everything below is about one question: was a
# signature actually compared with something, and where. Computing a
# digest is not comparing it, and a function nothing calls is not a
# check the handler performs.


CONST_TIME_CALL = re.compile(
    r"(^|\.)(compare_digest|timingsafeequal|timing_safe_equal|"
    r"secure_compare|hash_equals|constant_time_compare|"
    r"constant_time_bytes_eq|constanttimecompare)$", re.I)

DIGEST_PRODUCER = re.compile(
    r"(^|\.)(hexdigest|digest|hmac_hex|new_hmac)$|(^|\.)hmac\.new$|"
    r"createhmac|(^|\.)hmac\.New$", re.I)

DIGESTY_NAME = re.compile(
    r"(^|_)(sig|sigs|signature|signatures|digest|digests|hmac|mac|checksum)"
    r"(_|$)|signature|digest|hmac", re.I)

# Names that read like "this call decides whether the signature is good".
# Used only to say a verdict cannot be settled, never to award a pass.
VERIFY_NAME = re.compile(
    r"(verify|check|validate|authenticate|assert|ensure)[_a-z0-9]*"
    r"(sig|signature|hmac|webhook|payload|event|header)|"
    r"(sig|signature|hmac|webhook)[_a-z0-9]*"
    r"(verify|verified|valid|check|checked|ok)|construct_event", re.I)

HANDLER_HINT = re.compile(
    r"webhook|payment[_-]?event|receive[_a-z]*event|handle[_a-z]*event|"
    r"signature", re.I)

PRE_HOOK = re.compile(r"before_(app_)?request|middleware|before_serving", re.I)

# What makes a function the thing an event arrives at, rather than a
# helper with a suggestive name. `signature` is deliberately absent: a
# function called `_verify_signature` is a helper, and treating it as an
# entry point would make every helper reachable from itself and dead
# code indistinguishable from wired-up code.
ROUTE_DECORATOR = re.compile(
    r"\.(route|post|get|put|patch|delete|add_api_route|on_event)\s*\(|"
    r"@(app|bp|blueprint|router|api|server)\b|functions_framework|"
    r"lambda_handler", re.I)
RECEIVER_NAME = re.compile(
    r"(receive|recv|handle|process|on)[_a-z0-9]*"
    r"(event|webhook|payment|hook|callback)|"
    r"webhook[_a-z0-9]*(handler|receiver|endpoint|view)?$|"
    r"(handler|handle)$", re.I)

_FUNCS = (ast.FunctionDef, ast.AsyncFunctionDef)


def dotted(node):
    """`a.b.c` for a name or attribute chain, else the empty string."""
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
    return ".".join(reversed(parts))


def unparse(node):
    try:
        return ast.unparse(node)
    except Exception:
        return ""


def position(node):
    return (getattr(node, "lineno", 0), getattr(node, "col_offset", 0))


def own_nodes(fn):
    """Every node inside a function, minus the bodies of nested ones.

    The decorators and the signature count as the function's own, and
    they come before its first statement, which is what a decorator and
    a dependency are for.
    """
    out = []
    stack = list(fn.decorator_list) + [fn.args]
    stack += [s for s in fn.body if not isinstance(s, _FUNCS)]
    while stack:
        node = stack.pop()
        out.append(node)
        for child in ast.iter_child_nodes(node):
            if isinstance(child, _FUNCS):
                continue
            stack.append(child)
    return out


def python_files(scratch, include_tests=False):
    """(rel, tree, text) for each Python file that parses, plus the rest.

    Returns (parsed, broken). A file that does not parse is named rather
    than skipped in silence.
    """
    parsed, broken = [], []
    for rel, path in source_files(scratch, exts=(".py",),
                                  include_tests=include_tests):
        text = read(path)
        try:
            parsed.append((rel, ast.parse(text), text))
        except SyntaxError as exc:
            broken.append((rel, str(exc)))
    return parsed, broken


def function_index(files):
    """Every function in the tree, by bare name, as name -> [(rel, node)]."""
    index = {}
    for rel, tree, _text in files:
        for node in ast.walk(tree):
            if isinstance(node, _FUNCS):
                index.setdefault(node.name, []).append((rel, node))
    return index


def calls_in(fn):
    """(position, dotted name, node) for every call the function makes."""
    out = []
    for node in own_nodes(fn):
        if isinstance(node, ast.Call):
            name = dotted(node.func)
            if name:
                out.append((position(node), name, node))
    return sorted(out, key=lambda row: row[0])


def tail(name):
    return name.rsplit(".", 1)[-1]


def operand_name(node):
    """The name a comparison operand carries, when it carries one."""
    if isinstance(node, (ast.Name, ast.Attribute)):
        return dotted(node)
    if isinstance(node, ast.Call):
        name = dotted(node.func)
        return name if DIGEST_PRODUCER.search(name or "") else None
    if isinstance(node, ast.Subscript):
        return operand_name(node.value)
    return None


def digest_names(fn):
    """Local names holding the result of a digest computation.

    `expected = hmac.new(...).hexdigest()` makes `expected` a digest,
    whatever it is called, so comparing it with `==` is the defect even
    though the name says nothing.
    """
    out = set()
    for node in own_nodes(fn):
        if isinstance(node, ast.Assign):
            targets, value = node.targets, node.value
        elif isinstance(node, (ast.AnnAssign, ast.NamedExpr)):
            targets, value = [node.target], node.value
        else:
            continue
        if not isinstance(value, ast.Call):
            continue
        if not DIGEST_PRODUCER.search(dotted(value.func) or ""):
            continue
        for target in targets:
            if isinstance(target, ast.Name):
                out.add(target.id)
    return out


def _is_empty_constant(node):
    return (isinstance(node, ast.Constant)
            and (node.value is None or node.value == ""
                 or node.value == b""))


def digest_compares(fn):
    """`==` and `!=` applied to a signature or a digest, in order.

    A signature compared against `None` or an empty string is a presence
    check, not a comparison of two digests, and is not counted.
    """
    local = digest_names(fn)
    out = []
    for node in own_nodes(fn):
        if not isinstance(node, ast.Compare):
            continue
        if not any(isinstance(op, (ast.Eq, ast.NotEq)) for op in node.ops):
            continue
        sides = [node.left] + list(node.comparators)
        if any(_is_empty_constant(s) for s in sides):
            continue
        for side in sides:
            label = operand_name(side)
            if not label:
                continue
            if (DIGESTY_NAME.search(label) or DIGEST_PRODUCER.search(label)
                    or label in local or label.split(".")[0] in local):
                out.append((position(node), label))
                break
    return sorted(out)


def const_time_calls(fn):
    """Calls to a constant-time comparison, in order."""
    out = []
    for pos, name, _node in calls_in(fn):
        if CONST_TIME_CALL.search(name):
            out.append((pos, name))
    return out


def digest_computations(fn):
    """Calls that compute a digest, in order. Computing is not checking."""
    out = []
    for pos, name, _node in calls_in(fn):
        if DIGEST_PRODUCER.search(name):
            out.append((pos, name))
    return out


def direct_verification(fn):
    """Earliest point where this function compares a signature, or None.

    Two shapes count, and only two: a constant-time comparison call, and
    an equality comparison of a digest. The second is the wrong way to
    do it, which is criterion 8's business, but it is still a check, so
    the ordering criterion has to see it.
    """
    events = [(pos, "a call to %s()" % name)
              for pos, name in const_time_calls(fn)]
    events += [(pos, "an equality comparison of %s" % label)
               for pos, label in digest_compares(fn)]
    return min(events) if events else None


def nested_functions(fn):
    """Functions defined inside this one, at any depth."""
    return [node for node in ast.walk(fn)
            if node is not fn and isinstance(node, _FUNCS)]


def verifying_names(index, limit=8):
    """Function names that compare a signature, directly or downstream.

    Downstream means three things: the function calls one that compares,
    or it wraps one that does, which is the shape every decorator takes,
    or it hands one back to be called later.
    """
    verifying = {}
    for name, defs in index.items():
        for rel, node in defs:
            found = direct_verification(node)
            if found:
                verifying[name] = ("compares the signature in %s line %d with "
                                   "%s" % (rel, found[0][0], found[1]))
                break
    for _ in range(limit):
        grown = False
        for name, defs in index.items():
            if name in verifying:
                continue
            for _rel, node in defs:
                for _pos, called, _node in calls_in(node):
                    if tail(called) in verifying and tail(called) != name:
                        verifying[name] = "calls %s()" % tail(called)
                        grown = True
                        break
                if name in verifying:
                    break
                for inner in nested_functions(node):
                    if inner.name in verifying and inner.name != name:
                        verifying[name] = "wraps %s()" % inner.name
                        grown = True
                        break
                if name in verifying:
                    break
        if not grown:
            break
    return verifying


def wiring_refs(fn):
    """Names the decorators and the signature bring in, with positions.

    `@require_signature` and `_=Depends(verify_signature)` never call
    anything in the function body, and both run before the first
    statement of it. A name mentioned here is wiring; a name mentioned
    in the body still has to be called.
    """
    out = []
    for root in list(fn.decorator_list) + [fn.args]:
        for node in ast.walk(root):
            if isinstance(node, (ast.Name, ast.Attribute)):
                name = dotted(node)
                if name:
                    out.append((position(node), name))
    return sorted(out)


def verification_event(fn, verifying):
    """Where this function's signature check happens, or None.

    Either the comparison is in the function, or the function calls
    something that performs it.
    """
    events = []
    found = direct_verification(fn)
    if found:
        events.append(found)
    for pos, name, _node in calls_in(fn):
        if tail(name) in verifying and tail(name) != fn.name:
            events.append((pos, "%s(), which %s" % (name,
                                                    verifying[tail(name)])))
    for pos, name in wiring_refs(fn):
        if tail(name) in verifying and tail(name) != fn.name:
            events.append((pos, "%s, wired in before the body, which %s"
                           % (name, verifying[tail(name)])))
    return min(events) if events else None


def opaque_verifiers(fn, index):
    """Calls that read like a signature check and cannot be followed.

    A handler that hands the raw bytes to a library verifier is doing
    the right thing, and no amount of reading this tree will show the
    comparison, because it is not in this tree. Criteria say so rather
    than guessing.
    """
    out = []
    seen = set()
    for pos, name in ([(p, n) for p, n, _node in calls_in(fn)]
                      + wiring_refs(fn)):
        if tail(name) in index or (pos, name) in seen:
            continue
        seen.add((pos, name))
        if VERIFY_NAME.search(name) and not DIGEST_PRODUCER.search(name):
            out.append((pos, name))
    return sorted(out)


def handler_functions(tree, text):
    """Functions that look like the webhook receiver, with decorators."""
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, _FUNCS):
            continue
        decorators = " ".join(unparse(d) for d in node.decorator_list)
        body = ast.get_source_segment(text, node) or ""
        if (HANDLER_HINT.search(node.name) or HANDLER_HINT.search(decorators)
                or HANDLER_HINT.search(body)):
            out.append((node, decorators))
    return out


def route_handlers(tree):
    """Functions an event actually arrives at, with their decorators.

    Narrower than `handler_functions` on purpose. That one asks which
    function might be the receiver so its statements can be ordered.
    This one asks where the request enters, so that what the receiver
    reaches can be told apart from what it does not.
    """
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, _FUNCS):
            continue
        decorators = " ".join(unparse(d) for d in node.decorator_list)
        if ROUTE_DECORATOR.search(decorators) or RECEIVER_NAME.search(
                node.name):
            out.append((node, decorators))
    return out


def pre_hook_functions(tree):
    """Functions wired to run before the handler does."""
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, _FUNCS):
            continue
        decorators = " ".join(unparse(d) for d in node.decorator_list)
        if PRE_HOOK.search(decorators):
            out.append(node)
    return out


def module_level_names(files):
    """Names read outside any function, which is how hooks get wired in.

    `app.before_request(verify_signature)` never calls the function in
    any file, so a reachability walk that only followed calls would call
    a wired-in verifier dead.
    """
    out = set()
    for _rel, tree, _text in files:
        inner = set()
        for node in ast.walk(tree):
            if isinstance(node, _FUNCS):
                for sub in ast.walk(node):
                    inner.add(id(sub))
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and id(node) not in inner:
                out.add(node.id)
            elif isinstance(node, ast.Attribute) and id(node) not in inner:
                out.add(node.attr)
    return out


def reachable_functions(roots, index, limit=400):
    """Function names the handler path can reach, following calls and refs."""
    seen = set()
    queue = list(roots)
    while queue and len(seen) < limit:
        name = queue.pop()
        if name in seen:
            continue
        seen.add(name)
        for _rel, node in index.get(name, []):
            for _pos, called, _node in calls_in(node):
                if tail(called) not in seen:
                    queue.append(tail(called))
            for sub in own_nodes(node):
                if isinstance(sub, ast.Name) and sub.id in index:
                    if sub.id not in seen:
                        queue.append(sub.id)
    return seen
