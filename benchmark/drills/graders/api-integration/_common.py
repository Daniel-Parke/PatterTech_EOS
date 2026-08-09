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
"""

import json
import os
import re
import sys
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
    """Committed automation files, as (relative path, text) pairs."""
    out = []
    seen = set()
    root = Path(scratch)
    for pattern in CI_GLOBS:
        for path in sorted(root.glob(pattern)):
            if not path.is_file():
                continue
            rel = path.relative_to(root).as_posix()
            if rel in seen:
                continue
            seen.add(rel)
            out.append((rel, read(path)))
    return out
