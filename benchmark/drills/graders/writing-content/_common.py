"""Shared helpers for the writing-content drill graders. Stdlib only.

Not a grader. The runner looks for `c<N>.py` by name, so this file is
never mistaken for a criterion.

Exit codes follow the grader contract: 0 pass, 1 fail, 2 the criterion
cannot be settled in this environment. The third is used where the thing
a criterion needs is missing from the machine rather than from the
delivered tree: a shell that cannot start the check command the tree
wires into CI, or a missing `git`.

What this module does and does not claim
----------------------------------------

The drill's fixture is a React and TypeScript app. Rendering it needs a
bundler, a browser and an installed dependency tree, and criterion 9
requires the criteria to run with no network. So four of the criteria
that the spec phrases as assertions about a rendered DOM are settled
here by a parse of the delivered source instead. Each grader says so in
its reason string, and none of them claims to have measured a layout.
Where a parse cannot settle a clause at all, the grader takes the third
exit rather than guessing.

The parsers are deliberately shallow and tolerant:

- `parse_jsx` is a tag scanner, not a JavaScript parser. It tracks
  strings and brace depth so an arrow function in an attribute does not
  end a tag early, and it flattens JSX nested inside a `{...}`
  expression into the surrounding element, which is what a reader means
  by "the error sits next to the input".
- the CSS reader understands rules, `@media` blocks and declarations,
  which is all the fixture and any reasonable fix contain.
- the CI reader pulls `run:` commands out of workflow YAML and
  `entry:` out of pre-commit, expands `npm run <script>` through
  package.json, and refuses to run anything that installs or fetches.

Nothing here mutates the tree it grades. The two graders that inject a
string work on a throwaway copy.
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

SKIP_DIRS = {".git", "node_modules", "dist", "build", "out", ".vite",
             ".next", "coverage", "__pycache__", ".venv", "venv",
             ".turbo", ".cache"}

CODE_EXT = (".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs")
VIEW_EXT = (".tsx", ".jsx", ".js", ".ts")

# Directory names a catalogue of copy tends to live in.
LOCALE_DIRS = {"locales", "locale", "lang", "langs", "i18n", "intl",
               "translations", "translation", "messages"}

# Locale tags that name a pseudo-locale rather than a language people
# read. `qps-ploc` is the Windows one, `en-XA`/`en-XB` the CLDR private
# use ones, `en-PS` the common hand-rolled one.
PSEUDO_TAGS = {"en-xa", "en-xb", "en-ps", "en-zz", "qps-ploc", "qps",
               "en-x-pseudo", "pseudo", "en-pseudo", "xx", "zz", "en-da"}

# A translation lookup, however the tree spells it.
T_CALL = re.compile(
    r"(?<![\w.$])(?:i18n\.t|intl\.formatMessage|formatMessage|translate|"
    r"__|t)\s*\(")


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


def rel(scratch, path):
    try:
        return Path(path).relative_to(scratch).as_posix()
    except ValueError:
        return str(path)


def walk(scratch, exts=None):
    """Every file under the tree, skipping build output and vendored code."""
    out = []
    for base, dirs, names in os.walk(scratch):
        dirs[:] = [d for d in sorted(dirs) if d not in SKIP_DIRS]
        for name in sorted(names):
            if exts and not name.endswith(tuple(exts)):
                continue
            out.append(Path(base) / name)
    return out


def app_files(scratch):
    """Application source: everything under src/, or the tree's code.

    Criterion 4 is about `src/`, so when the tree has one it is the
    boundary. A tree that renamed it falls back to all code outside the
    obvious tooling directories.
    """
    src = Path(scratch) / "src"
    if src.is_dir():
        return [p for p in walk(src, CODE_EXT)]
    out = []
    for path in walk(scratch, CODE_EXT):
        parts = set(Path(path).relative_to(scratch).parts[:-1])
        if parts & {"scripts", "tools", "bin", "config"}:
            continue
        if Path(path).name.startswith(("vite.config", "eslint.config")):
            continue
        out.append(path)
    return out


def view_files(scratch):
    """Source files that can carry JSX."""
    return [p for p in app_files(scratch) if p.name.endswith(VIEW_EXT)]


# ------------------------------------------------------------- catalogues


def load_json(path):
    try:
        return json.loads(read(path))
    except ValueError:
        return None


def flatten(doc, prefix=""):
    """Dotted keys to string values, so nested and flat read the same."""
    out = {}
    if not isinstance(doc, dict):
        return out
    for key, value in doc.items():
        name = "%s.%s" % (prefix, key) if prefix else str(key)
        if isinstance(value, str):
            out[name] = value
        elif isinstance(value, dict):
            out.update(flatten(value, name))
    return out


def _locale_code(path):
    stem = Path(path).stem
    return stem.lower().replace("_", "-")


def catalogue_files(scratch):
    """Every JSON file that reads as a catalogue of copy.

    A file counts when it sits in a locale directory, or its stem looks
    like a language tag and it holds mostly string values.
    """
    out = []
    for path in walk(scratch, (".json",)):
        parts = [p.lower() for p in Path(path).relative_to(scratch).parts]
        in_locale_dir = bool(set(parts[:-1]) & LOCALE_DIRS)
        stem = _locale_code(path)
        looks_tagged = bool(re.match(r"^[a-z]{2}(-[a-z0-9]{2,8})*$", stem))
        if not in_locale_dir and not looks_tagged:
            continue
        doc = load_json(path)
        flat = flatten(doc)
        if not flat:
            continue
        out.append((stem, path, flat))
    return out


def is_pseudo_tag(code):
    code = code.lower()
    if code in PSEUDO_TAGS:
        return True
    return "pseudo" in code or code.startswith("en-x")


def base_catalogue(scratch):
    """The source-language catalogue: (code, path, flat dict) or Nones."""
    files = [f for f in catalogue_files(scratch) if not is_pseudo_tag(f[0])]
    if not files:
        return None, None, None
    for code, path, flat in files:
        if code == "en":
            return code, path, flat
    for code, path, flat in files:
        if code.startswith("en"):
            return code, path, flat
    files.sort(key=lambda f: -len(f[2]))
    return files[0]


def other_catalogues(scratch, base_path):
    return [f for f in catalogue_files(scratch)
            if Path(f[1]) != Path(base_path)]


def expansion(base, other):
    """Mean length ratio of a catalogue against the base, over shared keys."""
    shared = [k for k in base if k in other and base[k]]
    if not shared:
        return 0.0
    src = sum(len(base[k]) for k in shared)
    dst = sum(len(other[k]) for k in shared)
    return dst / float(src) if src else 0.0


# ------------------------------------------------------------ JS scanning


def strip_comments(text):
    """Blank out // and /* */ comments, leaving strings and offsets alone."""
    out = []
    i, n = 0, len(text)
    quote = None
    while i < n:
        ch = text[i]
        if quote:
            out.append(ch)
            if ch == "\\" and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch in "'\"`":
            quote = ch
            out.append(ch)
            i += 1
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "/":
            while i < n and text[i] != "\n":
                out.append(" ")
                i += 1
            continue
        if ch == "/" and i + 1 < n and text[i + 1] == "*":
            end = text.find("*/", i + 2)
            end = n if end == -1 else end + 2
            out.append("".join(" " if c != "\n" else "\n"
                               for c in text[i:end]))
            i = end
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def match_bracket(text, start, open_ch="(", close_ch=")"):
    """Index just past the bracket opened at `start`, or -1."""
    depth = 0
    i, n = start, len(text)
    quote = None
    while i < n:
        ch = text[i]
        if quote:
            if ch == "\\":
                i += 2
                continue
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch in "'\"`":
            quote = ch
        elif ch == open_ch:
            depth += 1
        elif ch == close_ch:
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return -1


def t_calls(text):
    """Every translation lookup: (start, end, args_source, key_or_None)."""
    out = []
    for match in T_CALL.finditer(text):
        open_at = match.end() - 1
        end = match_bracket(text, open_at)
        if end == -1:
            continue
        args = text[open_at + 1:end - 1]
        key = None
        lit = re.match(r"""\s*(['"])(.*?)\1""", args)
        if lit:
            key = lit.group(2)
        out.append((match.start(), end, args, key))
    return out


ICU_PLURAL = re.compile(r"\{\s*(\w+)\s*,\s*(?:plural|selectordinal)\s*,",
                        re.I)
CATEGORY = re.compile(r"(=\d+|[A-Za-z]+)\s*\{")


def plural_blocks(value):
    """In-message plural selection in one message: [(arg, categories)]."""
    out = []
    for match in ICU_PLURAL.finditer(value):
        end = match_bracket(value, match.start(), "{", "}")
        if end == -1:
            continue
        body = value[match.end():end - 1]
        cats = set()
        i = 0
        while i < len(body):
            inner = CATEGORY.search(body, i)
            if not inner:
                break
            close = match_bracket(body, inner.end() - 1, "{", "}")
            if close == -1:
                break
            cats.add(inner.group(1).lower())
            i = close
        out.append((match.group(1), cats))
    return out


def plural_messages(flat):
    """Catalogue keys whose message selects a plural form inside itself."""
    out = {}
    for key, value in sorted(flat.items()):
        blocks = plural_blocks(value)
        cats = set()
        for _, block in blocks:
            cats |= block
        if blocks and "other" in cats:
            out[key] = cats
    return out


def function_body(text, start):
    """The `{...}` block that follows `start`, or ''."""
    brace = text.find("{", start)
    if brace == -1:
        return ""
    end = match_bracket(text, brace, "{", "}")
    return text[brace:end] if end != -1 else ""


def line_of(text, index):
    return text.count("\n", 0, index) + 1


def string_literals(text):
    """Every single or double quoted literal, as (index, value)."""
    out = []
    for match in re.finditer(r"""(['"])((?:\\.|(?!\1)[^\\\n])*)\1""", text):
        out.append((match.start(), match.group(2)))
    return out


# ---------------------------------------------------------------- the JSX


class Node(object):
    __slots__ = ("tag", "attrs", "children", "parent", "line", "file")

    def __init__(self, tag, attrs=None, parent=None, line=0, file=""):
        self.tag = tag
        self.attrs = attrs or {}
        self.children = []
        self.parent = parent
        self.line = line
        self.file = file

    def elements(self):
        for child in self.children:
            if isinstance(child, Node):
                yield child
                for grand in child.elements():
                    yield grand

    def ancestors(self):
        node = self.parent
        while node is not None:
            yield node
            node = node.parent

    def texts(self):
        """Plain text children, not expressions."""
        return [c[1] for c in self.children
                if isinstance(c, tuple) and c[0] == "text"]

    def exprs(self):
        return [c[1] for c in self.children
                if isinstance(c, tuple) and c[0] == "expr"]

    def source(self):
        """Everything under this node, expressions and text alike."""
        parts = []
        for child in self.children:
            if isinstance(child, Node):
                parts.append(child.source())
            else:
                parts.append(child[1])
        return " ".join(p for p in parts if p)

    def where(self):
        return "%s:%d <%s>" % (self.file, self.line, self.tag)


def _attrs(raw):
    """Parse an opening tag's attribute source into name -> (kind, value)."""
    out = {}
    i, n = 0, len(raw)
    while i < n:
        match = re.compile(r"([A-Za-z_$][-\w:$.]*)\s*").search(raw, i)
        if not match:
            break
        name = match.group(1)
        i = match.end()
        if i < n and raw[i] == "=":
            i += 1
            while i < n and raw[i].isspace():
                i += 1
            if i < n and raw[i] in "'\"":
                quote = raw[i]
                end = raw.find(quote, i + 1)
                end = n if end == -1 else end
                out[name] = ("string", raw[i + 1:end])
                i = end + 1
            elif i < n and raw[i] == "{":
                end = match_bracket(raw, i, "{", "}")
                end = n if end == -1 else end
                out[name] = ("expr", raw[i + 1:end - 1].strip())
                i = end
            else:
                match2 = re.compile(r"\S+").match(raw, i)
                out[name] = ("string", match2.group(0) if match2 else "")
                i = match2.end() if match2 else n
        else:
            out[name] = ("string", "true")
    return out


def _is_tag_start(text, i):
    """Tell a JSX element from a TypeScript generic.

    `useState<string>` and `Record<string, string>` follow an
    identifier, a closing paren or a closing bracket. JSX follows an
    operator, an opening bracket, a previous tag or nothing.
    """
    j = i - 1
    while j >= 0 and text[j].isspace():
        j -= 1
    if j < 0:
        return True
    prev = text[j]
    if prev.isalnum() or prev in "_$)]'\"`.":
        return False
    return True


def parse_jsx(text, name=""):
    """A tolerant tag scan of a JSX source file. Returns a root Node.

    Text is filed two ways. A chunk read while the scanner sits directly
    inside an element is JSX text, the words a user sees. A chunk read
    inside a `{...}` expression at that same element is expression
    source, which is code. The distinction is what lets a grader ask
    whether a literal was rendered rather than merely written.
    """
    text = strip_comments(text)
    root = Node("#root", file=name)
    stack = [root]
    frames = []  # (end_index, stack_depth_at_entry)
    i, n = 0, len(text)
    buf = []

    def kind():
        for _, depth in frames:
            if depth == len(stack):
                return "expr"
        return "text"

    def flush():
        if not buf:
            return
        chunk = "".join(buf)
        del buf[:]
        if chunk.strip():
            stack[-1].children.append((kind(), chunk))

    while i < n:
        while frames and i >= frames[-1][0]:
            flush()
            frames.pop()
        ch = text[i]
        if ch in "'\"`":
            end = match_string(text, i)
            buf.append(text[i:end])
            i = end
            continue
        if ch == "{":
            end = match_bracket(text, i, "{", "}")
            if end == -1:
                buf.append(ch)
                i += 1
                continue
            inner = text[i + 1:end - 1]
            if re.search(r"<[A-Za-z_$>]", inner):
                # JSX inside an expression: keep scanning so the nested
                # elements land in the surrounding element, and remember
                # that plain text at this depth is code, not copy.
                flush()
                frames.append((end, len(stack)))
                buf.append("{")
                i += 1
                continue
            flush()
            stack[-1].children.append(("expr", inner))
            i = end
            continue
        if ch == "<" and i + 1 < n:
            nxt = text[i + 1]
            if nxt == "/":
                end = text.find(">", i)
                if end == -1:
                    break
                tag = text[i + 2:end].strip()
                flush()
                for depth in range(len(stack) - 1, 0, -1):
                    if stack[depth].tag == tag or not tag:
                        del stack[depth:]
                        break
                i = end + 1
                continue
            if (nxt.isalpha() or nxt in "_$>") and _is_tag_start(text, i):
                end = _tag_end(text, i)
                if end == -1:
                    buf.append(ch)
                    i += 1
                    continue
                inner = text[i + 1:end - 1]
                closed = inner.rstrip().endswith("/")
                inner = inner.rstrip().rstrip("/")
                match = re.match(r"([A-Za-z_$][-\w:$.]*)", inner)
                tag = match.group(1) if match else ""
                attrs = _attrs(inner[match.end():] if match else "")
                flush()
                node = Node(tag or "fragment", attrs, stack[-1],
                            line_of(text, i), name)
                stack[-1].children.append(node)
                if not closed:
                    stack.append(node)
                i = end
                continue
        buf.append(ch)
        i += 1
    flush()
    return root


def match_string(text, start):
    quote = text[start]
    i = start + 1
    n = len(text)
    while i < n:
        if text[i] == "\\":
            i += 2
            continue
        if text[i] == quote:
            return i + 1
        i += 1
    return n


def _tag_end(text, start):
    """Index just past the `>` closing the tag opened at `start`."""
    i = start + 1
    n = len(text)
    depth = 0
    while i < n:
        ch = text[i]
        if ch in "'\"`":
            i = match_string(text, i)
            continue
        if ch == "{":
            end = match_bracket(text, i, "{", "}")
            if end == -1:
                return -1
            i = end
            continue
        if ch == "<":
            return -1
        if ch == ">" and depth == 0:
            return i + 1
        i += 1
    return -1


def jsx_roots(scratch):
    """(path, root Node) for every source file that carries JSX."""
    out = []
    for path in view_files(scratch):
        text = read(path)
        if "<" not in text:
            continue
        out.append((path, parse_jsx(text, rel(scratch, path))))
    return out


def password_input(scratch, roots=None):
    """The password field, wherever it lives. Returns a Node or None.

    Pass `roots` when the caller also walks the tree: node identity is
    only meaningful within one parse, and a second call to `jsx_roots`
    builds a second set of objects whose parents match nothing.
    """
    for _, root in (roots if roots is not None else jsx_roots(scratch)):
        for node in root.elements():
            if node.tag.lower() not in ("input", "textarea"):
                continue
            kinds = {k.lower(): v for k, v in node.attrs.items()}
            typ = kinds.get("type", ("", ""))[1].lower()
            ident = " ".join(
                kinds.get(a, ("", ""))[1].lower()
                for a in ("id", "name", "data-testid"))
            if typ == "password" or "password" in ident:
                return node
    return None


# ----------------------------------------------------------------- styles


def css_files(scratch):
    return walk(scratch, (".css", ".scss", ".sass", ".less"))


def _strip_at_blocks(css):
    """Return the CSS with @media/@supports wrappers removed, body kept."""
    out = []
    i, n = 0, len(css)
    while i < n:
        if css[i] == "@":
            head_end = css.find("{", i)
            if head_end == -1:
                break
            name = css[i:head_end].split()[0].lower()
            end = match_bracket(css, head_end, "{", "}")
            if end == -1:
                break
            if name in ("@media", "@supports", "@layer", "@container"):
                out.append(_strip_at_blocks(css[head_end + 1:end - 1]))
            i = end
            continue
        out.append(css[i])
        i += 1
    return "".join(out)


def css_rules(scratch):
    """(selector, declarations dict, file) for every rule in the tree."""
    rules = []
    for path in css_files(scratch):
        text = strip_comments_css(read(path))
        flat = _strip_at_blocks(text)
        i, n = 0, len(flat)
        while i < n:
            brace = flat.find("{", i)
            if brace == -1:
                break
            end = match_bracket(flat, brace, "{", "}")
            if end == -1:
                break
            selector = flat[i:brace].strip()
            body = flat[brace + 1:end - 1]
            if selector and "{" not in selector:
                for sel in selector.split(","):
                    sel = sel.strip()
                    if sel:
                        rules.append((sel, declarations(body), path))
            i = end
    return rules


def strip_comments_css(text):
    return re.sub(r"/\*.*?\*/", " ", text, flags=re.S)


def declarations(body):
    out = {}
    for part in body.split(";"):
        if ":" not in part:
            continue
        prop, value = part.split(":", 1)
        prop = prop.strip().lower()
        if prop and "{" not in prop:
            out[prop] = value.strip()
    return out


def class_names(node):
    out = set()
    for attr in ("className", "class"):
        if attr not in node.attrs:
            continue
        kind, value = node.attrs[attr]
        for token in re.findall(r"[\w-]+", value):
            out.add(token)
    return out


def selector_classes(selector):
    return set(re.findall(r"\.([\w-]+)", selector))


# --------------------------------------------------------------------- CI


CI_GLOBS = (".github/workflows", ".gitlab-ci.yml", ".pre-commit-config.yaml",
            ".pre-commit-config.yml", ".circleci/config.yml",
            "azure-pipelines.yml", "Jenkinsfile", ".husky")

INSTALL_RE = re.compile(
    r"\b(npm\s+(ci|install|i)\b|yarn(\s+install)?\s*$|pnpm\s+(i|install)\b|"
    r"pip\s+install|apt(-get)?\s|brew\s|curl\s|wget\s|docker\s|"
    r"playwright\s+install|npx\s+playwright\s+install)")


def ci_files(scratch):
    out = []
    workflows = Path(scratch) / ".github" / "workflows"
    if workflows.is_dir():
        out.extend(sorted(p for p in workflows.iterdir()
                          if p.suffix in (".yml", ".yaml")))
    for name in CI_GLOBS[1:]:
        path = Path(scratch) / name
        if path.is_file():
            out.append(path)
        elif path.is_dir():
            out.extend(sorted(p for p in path.iterdir() if p.is_file()))
    return out


def _yaml_commands(text):
    """`run:` scalars and blocks, plus pre-commit `entry:` lines."""
    out = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        match = re.match(r"^(\s*)(?:-\s*)?(run|entry|command)\s*:\s*(.*)$",
                         line)
        if not match:
            i += 1
            continue
        indent, rest = len(match.group(1)), match.group(3).strip()
        if rest in ("|", ">", "|-", ">-", "|+", "", "'|'"):
            i += 1
            while i < len(lines):
                nxt = lines[i]
                if nxt.strip() and (len(nxt) - len(nxt.lstrip())) <= indent:
                    break
                if nxt.strip():
                    out.append(nxt.strip())
                i += 1
            continue
        out.append(rest.strip("'\""))
        i += 1
    return out


def package_scripts(scratch):
    doc = load_json(Path(scratch) / "package.json") or {}
    scripts = doc.get("scripts")
    return scripts if isinstance(scripts, dict) else {}


def expand_script(cmd, scripts, depth=0):
    """Resolve `npm run x` to the script body, one or two levels deep."""
    if depth > 2:
        return cmd
    match = re.match(
        r"^\s*(?:npm|pnpm|yarn|bun)\s+(?:run(?:-script)?\s+)?"
        r"([\w:.-]+)\s*(?:--.*)?$", cmd)
    if not match:
        return cmd
    name = match.group(1)
    if name in ("ci", "install", "i", "test") and name not in scripts:
        return cmd
    body = scripts.get(name)
    if not body:
        return cmd
    return expand_script(body, scripts, depth + 1)


def ci_commands(scratch):
    """Every check command CI runs, minus installs. [(source, command)]."""
    scripts = package_scripts(scratch)
    out = []
    seen = set()
    for path in ci_files(scratch):
        text = read(path)
        raw = _yaml_commands(text) if path.suffix in (".yml", ".yaml") else \
            [ln.strip() for ln in text.splitlines()
             if ln.strip() and not ln.strip().startswith("#")]
        for cmd in raw:
            cmd = cmd.strip()
            if not cmd or cmd.startswith("#"):
                continue
            if INSTALL_RE.search(cmd):
                continue
            resolved = expand_script(cmd, scripts)
            if INSTALL_RE.search(resolved):
                continue
            key = (rel(scratch, path), resolved)
            if key in seen:
                continue
            seen.add(key)
            out.append((rel(scratch, path), resolved))
    return out


def set_message(doc, dotted, value):
    """Set a leaf by dotted key, whether the catalogue is flat or nested."""
    if isinstance(doc.get(dotted), str):
        doc[dotted] = value
        return True
    parts = dotted.split(".")
    for i in range(1, len(parts)):
        head, tail = ".".join(parts[:i]), ".".join(parts[i:])
        if isinstance(doc.get(head), dict) and set_message(doc[head], tail,
                                                           value):
            return True
    return False


def plain_keys(flat):
    """Keys whose message is prose: no placeholders, no markup."""
    return [k for k, v in flat.items()
            if "{" not in v and "<" not in v and "%" not in v]


def inject(path, dotted, value):
    """Rewrite one message in a catalogue file. Returns True on success."""
    doc = load_json(path)
    if not isinstance(doc, dict):
        return False
    if not set_message(doc, dotted, value):
        return False
    Path(path).write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    return True


def copy_tree(scratch):
    """A throwaway copy, so a grader that injects never marks the tree."""
    dest = Path(tempfile.mkdtemp(prefix="drill-wc-"))
    target = dest / "tree"
    shutil.copytree(str(scratch), str(target),
                    ignore=shutil.ignore_patterns(*SKIP_DIRS))
    return dest, target


NOT_FOUND = re.compile(
    r"(command not found|is not recognized|no such file or directory|"
    r"cannot find module|not found: )", re.I)


def run_command(cwd, cmd, timeout=180):
    """Run one CI command in `cwd`. Returns (returncode, output)."""
    env = dict(os.environ)
    env["CI"] = "1"
    env["NO_COLOR"] = "1"
    try:
        proc = subprocess.run(cmd, shell=True, cwd=str(cwd),
                              capture_output=True, text=True,
                              encoding="utf-8", errors="replace",
                              timeout=timeout, env=env)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, str(exc)
    return proc.returncode, ((proc.stdout or "") + (proc.stderr or "")).strip()


def looks_missing(output):
    return bool(output and NOT_FOUND.search(output))


def owns_script(scratch, cmd):
    """True when the command runs a file the tree itself ships.

    The difference matters for the third exit. A command that drives a
    checker committed in the tree and will not start is an environment
    gap. A command that drives a toolchain binary nobody installed is a
    build step, and a build step is not a check over the words.
    """
    for token in re.split(r"[\s;&|]+", cmd):
        token = token.strip("'\"")
        if not token or token.startswith("-"):
            continue
        candidate = Path(scratch) / token.replace("\\", "/")
        if candidate.is_file():
            return True
    return False
