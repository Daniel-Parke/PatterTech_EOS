"""Shared helpers for the DRILL-HOUSE-001 graders. Stdlib only.

Not a grader. The runner looks for `c<N>.py` by name, so this file is
never mistaken for a criterion.

Exit codes follow the grader contract: 0 pass, 1 fail, 2 the criterion
cannot be settled in this environment. Seven of the ten criteria are
assertions about what a browser computed, and a machine with no
Playwright and no Chromium cannot settle them. Reporting that as a fail
would invent a finding against the delivered tree, so those graders
take the third exit instead.

Three things live here:

- a small HTML tree parser, for the criteria the spec calls a static
  parse of the built markup;
- a reader for the CSS the page actually loads, so a stylesheet nobody
  linked is never graded as if it were on the page;
- a driver for the browser probe. The probe source is held here as a
  string, written to a scratch file and run as a child process, exactly
  the way the architecture graders drive lint-imports. Playwright is
  imported inside that child and nowhere in this directory, so every
  file a grader imports stays stdlib only.

The services section is found by content rather than by a class or an
id the fixture planted: it is the deepest `<section>` whose text carries
all four offering titles from `fixtures/services.json`. An agent is free
to name and structure it however it likes.
"""

import hashlib
import html.parser
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

PASS, FAIL, UNSETTLED = 0, 1, 2

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}

# Tags that implicitly close an open tag of their own kind.
AUTO_CLOSE = {
    "li": {"li"}, "p": {"p"}, "td": {"td", "th"}, "th": {"td", "th"},
    "tr": {"tr", "td", "th"}, "dt": {"dt", "dd"}, "dd": {"dt", "dd"},
    "option": {"option"},
}
BLOCKS = {"address", "article", "aside", "blockquote", "div", "dl", "fieldset",
          "figcaption", "figure", "footer", "form", "h1", "h2", "h3", "h4",
          "h5", "h6", "header", "hr", "main", "nav", "ol", "p", "pre",
          "section", "table", "ul"}

FURNITURE = ("index", "rule", "kicker", "title")


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


def index_html(scratch):
    path = Path(scratch) / "index.html"
    return path if path.is_file() else None


def require_page(cid, scratch):
    path = index_html(scratch)
    if path is None:
        emit(cid, FAIL, "no index.html in the delivered tree, so there is no "
                        "page to grade")
    return path


def service_titles(scratch):
    """The four offering titles the brief fixes, from the fixture."""
    path = Path(scratch) / "fixtures" / "services.json"
    try:
        doc = json.loads(read(path))
    except ValueError:
        return []
    out = []
    for item in doc.get("services", []) or []:
        title = str(item.get("title", "")).strip()
        if title:
            out.append(title)
    return out


# ------------------------------------------------------------------- HTML


class Node:
    __slots__ = ("tag", "attrs", "children", "parent")

    def __init__(self, tag, attrs=None, parent=None):
        self.tag = tag
        self.attrs = attrs or {}
        self.children = []
        self.parent = parent

    def elements(self):
        for child in self.children:
            if isinstance(child, Node):
                yield child
                for sub in child.elements():
                    yield sub

    def text(self):
        """Rendered text. Script, style and template bodies are not text,
        so markup hidden in a script string never counts as content."""
        out = []
        for child in self.children:
            if isinstance(child, str):
                out.append(child)
            elif child.tag not in ("script", "style", "template"):
                out.append(child.text())
        return "".join(out)

    def own_text(self):
        return "".join(c for c in self.children if isinstance(c, str))

    def depth(self):
        n, node = 0, self
        while node.parent is not None:
            n += 1
            node = node.parent
        return n

    def path(self):
        bits, node = [], self
        while node is not None and node.tag != "#root":
            bit = node.tag
            if node.attrs.get("id"):
                bit += "#" + node.attrs["id"]
            elif node.attrs.get("class"):
                bit += "." + ".".join(node.attrs["class"].split())
            bits.append(bit)
            node = node.parent
        return ">".join(reversed(bits))

    def ancestors(self):
        node = self.parent
        while node is not None:
            yield node
            node = node.parent


class _Builder(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root")
        self.stack = [self.root]

    def _open_tags(self):
        return [n.tag for n in self.stack]

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        top = self.stack[-1].tag
        if tag in AUTO_CLOSE and top in AUTO_CLOSE[tag]:
            self.stack.pop()
        elif tag in BLOCKS and top == "p":
            self.stack.pop()
        node = Node(tag, {k.lower(): (v if v is not None else "")
                          for k, v in attrs}, self.stack[-1])
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        node = Node(tag.lower(), {k.lower(): (v if v is not None else "")
                                  for k, v in attrs}, self.stack[-1])
        self.stack[-1].children.append(node)

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in VOID or tag not in self._open_tags():
            return
        while len(self.stack) > 1:
            done = self.stack.pop().tag == tag
            if done:
                return

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def parse_html(text):
    builder = _Builder()
    builder.feed(text)
    builder.close()
    return builder.root


def normalise(text):
    return re.sub(r"\s+", " ", text or "").strip().lower()


def find_section(root, titles):
    """The deepest section whose text carries every offering title."""
    if not titles:
        return None
    wanted = [normalise(t) for t in titles]
    holders = []
    for node in root.elements():
        if node.tag in ("html", "head", "body", "script", "style", "template"):
            continue
        text = normalise(node.text())
        if all(w in text for w in wanted):
            holders.append(node)
    if not holders:
        return None
    sections = [n for n in holders if n.tag == "section"]
    pool = sections or holders
    return max(pool, key=lambda n: n.depth())


def section_header(section):
    """The section mark: a `header` if there is one, else the title's parent."""
    for node in section.elements():
        if node.tag == "header":
            return node
    for node in section.elements():
        if node.attrs.get("data-role") == "title" and node.parent is not None:
            return node.parent
    return None


# -------------------------------------------------------------------- CSS


def _strip_comments(text):
    return re.sub(r"/\*.*?\*/", " ", text, flags=re.S)


def page_css(scratch):
    """Every stylesheet the page actually loads, plus its inline styles.

    Returns a list of (label, text). A stylesheet sitting in the tree
    that nothing links is not on the page and is not graded.
    """
    path = index_html(scratch)
    if path is None:
        return []
    markup = read(path)
    out = []
    root = parse_html(markup)
    for node in root.elements():
        if node.tag == "link":
            rel = (node.attrs.get("rel") or "").lower()
            href = node.attrs.get("href") or ""
            if "stylesheet" not in rel or not href:
                continue
            if re.match(r"^[a-z]+:", href) or href.startswith("//"):
                continue
            target = (Path(scratch) / href.split("?")[0].split("#")[0]
                      .lstrip("/")).resolve()
            try:
                target.relative_to(Path(scratch).resolve())
            except ValueError:
                continue
            if target.is_file():
                out.append((str(target.relative_to(Path(scratch).resolve())
                                .as_posix()), _strip_comments(read(target))))
        elif node.tag == "style":
            out.append(("index.html <style>", _strip_comments(node.own_text())))
    return out


def all_css(scratch):
    return "\n".join(text for _, text in page_css(scratch))


def _match_block(text, open_index):
    """Index just past the brace-balanced block starting at open_index."""
    depth = 0
    for i in range(open_index, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return i
    return -1


def keyframe_blocks(text):
    """Every @keyframes block: (name, body). Vendor prefixes included."""
    out = []
    for match in re.finditer(r"@(?:-\w+-)?keyframes\s+([\w-]+)\s*\{", text):
        end = _match_block(text, match.end() - 1)
        if end == -1:
            continue
        out.append((match.group(1), text[match.end():end]))
    return out


def declarations(body):
    """(property, value) pairs in a declaration block, nested ones included."""
    out = []
    for inner in re.finditer(r"\{([^{}]*)\}", body):
        for part in inner.group(1).split(";"):
            if ":" not in part:
                continue
            prop, value = part.split(":", 1)
            prop = prop.strip().lower()
            if prop:
                out.append((prop, value.strip()))
    return out


def top_level_rules(text):
    """(selector, body) for rules outside @keyframes, at-rules unwrapped."""
    without_keyframes = re.sub(
        r"@(?:-\w+-)?keyframes\s+[\w-]+\s*\{", "@@KF@@{", text)
    out = []
    i = 0
    while True:
        brace = without_keyframes.find("{", i)
        if brace == -1:
            break
        selector = without_keyframes[i:brace].strip()
        end = _match_block(without_keyframes, brace)
        if end == -1:
            break
        body = without_keyframes[brace + 1:end]
        if selector.startswith("@@KF@@"):
            pass
        elif selector.startswith("@media") or selector.startswith("@supports") \
                or selector.startswith("@layer"):
            out.extend(top_level_rules(body))
        elif selector.startswith("@"):
            pass
        else:
            for one in selector.split(","):
                if one.strip():
                    out.append((one.strip(), body))
        i = end + 1
    return out


def reduced_motion_blocks(text):
    """Bodies of every @media block querying prefers-reduced-motion: reduce."""
    out = []
    for match in re.finditer(r"@media([^{]*)\{", text):
        query = " ".join(match.group(1).split()).lower()
        if "prefers-reduced-motion" not in query:
            continue
        if not re.search(r"prefers-reduced-motion\s*:\s*reduce", query) and \
                not re.search(r"\(\s*prefers-reduced-motion\s*\)", query):
            continue
        end = _match_block(text, match.end() - 1)
        if end == -1:
            continue
        out.append(text[match.end():end])
    return out


# ---------------------------------------------------------------- contrast


def _channel(value):
    value = value / 255.0
    return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4


def luminance(rgb):
    r, g, b = (_channel(c) for c in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg, bg):
    a, b = luminance(fg), luminance(bg)
    if a < b:
        a, b = b, a
    return (a + 0.05) / (b + 0.05)


def over(fg, bg):
    """Composite a possibly translucent foreground onto its backdrop."""
    alpha = fg[3] if len(fg) > 3 else 1.0
    return [fg[i] * alpha + bg[i] * (1 - alpha) for i in range(3)]


# ------------------------------------------------------------------- probe


PROBE_SOURCE = r'''
"""Browser probe for the DRILL-HOUSE-001 graders.

Run as a child process by the graders. This is the one file in the
chain that imports Playwright; the graders themselves are stdlib only
and treat it as an external tool, the way another drill treats
lint-imports. Prints one JSON object.

Usage: probe.py <index.html> <titles.json>
"""

import json
import sys

VIEWPORTS = (375, 768, 1280)

FIND = r"""
(titles) => {
  const norm = (s) => (s || '').replace(/\s+/g, ' ').trim().toLowerCase();
  const wanted = titles.map(norm).filter(Boolean);
  const holds = (el) => {
    const t = norm(el.textContent);
    return wanted.every((w) => t.includes(w));
  };
  const depth = (el) => { let d = 0; while (el.parentElement) { d++; el = el.parentElement; } return d; };
  const all = Array.from(document.querySelectorAll('body *')).filter(holds);
  if (!all.length) return null;
  const sections = all.filter((e) => e.tagName === 'SECTION');
  const pool = sections.length ? sections : all;
  let best = pool[0];
  for (const e of pool) { if (depth(e) > depth(best)) best = e; }
  return best;
}
"""

PATH = r"""
  const path = (el) => {
    const bits = [];
    while (el && el.nodeType === 1 && el.tagName !== 'HTML') {
      let bit = el.tagName.toLowerCase();
      if (el.id) bit += '#' + el.id;
      else if (el.classList.length) bit += '.' + Array.from(el.classList).join('.');
      bits.unshift(bit);
      el = el.parentElement;
    }
    return bits.join('>');
  };
"""

COLLECT = r"""
(titles) => {
  const find = FIND_SRC;
  PATH_SRC
  const section = find(titles);
  const ownText = (el) => Array.from(el.childNodes)
    .filter((n) => n.nodeType === 3).map((n) => n.textContent).join('');
  const parseRGB = (s) => {
    const m = /rgba?\(([^)]+)\)/.exec(s || '');
    if (!m) return null;
    const p = m[1].split(/[,\s/]+/).filter(Boolean).map(Number);
    return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1];
  };
  const backdrop = (el) => {
    let acc = null, image = null, node = el;
    while (node) {
      const cs = getComputedStyle(node);
      if (cs.backgroundImage && cs.backgroundImage !== 'none' && image === null) {
        image = path(node) + ' ' + cs.backgroundImage.slice(0, 60);
      }
      const c = parseRGB(cs.backgroundColor);
      if (c && c[3] > 0) {
        if (acc === null) acc = [c[0], c[1], c[2], c[3]];
        else {
          const a = acc[3];
          acc = [acc[0] + c[0] * c[3] * (1 - a), acc[1] + c[1] * c[3] * (1 - a),
                 acc[2] + c[2] * c[3] * (1 - a), a + c[3] * (1 - a)];
        }
        if (acc[3] >= 0.999) break;
      }
      node = node.parentElement;
    }
    if (acc === null) return { rgb: [255, 255, 255], image: image, opaque: false };
    const a = acc[3];
    const over = (v) => Math.round(v + 255 * (1 - a));
    return { rgb: [over(acc[0]), over(acc[1]), over(acc[2])],
             image: image, opaque: a >= 0.999 };
  };
  const bordered = (cs) => ['Top', 'Right', 'Bottom', 'Left'].every((s) =>
    cs['border' + s + 'Style'] !== 'none' && parseFloat(cs['border' + s + 'Width']) > 0);

  const out = {
    found: !!section,
    rootFontPx: parseFloat(getComputedStyle(document.documentElement).fontSize),
    section: null, header: null, elements: [], sectionText: null,
  };
  if (!section) return out;
  out.section = path(section);
  out.sectionText = section.textContent;

  let header = section.querySelector('header');
  if (!header) {
    const title = section.querySelector('[data-role="title"]');
    if (title && title.parentElement) header = title.parentElement;
  }
  out.header = header ? path(header) : null;

  const nodes = [section].concat(Array.from(section.querySelectorAll('*')));
  for (const el of nodes) {
    const cs = getComputedStyle(el);
    const fg = parseRGB(cs.color) || [0, 0, 0, 1];
    const bd = backdrop(el);
    out.elements.push({
      path: path(el),
      tag: el.tagName.toLowerCase(),
      role: el.getAttribute('data-role'),
      container: el.getAttribute('data-container'),
      isHeading: /^H[1-6]$/.test(el.tagName),
      isHeader: header ? (el === header) : false,
      textAlign: cs.textAlign,
      fontSizePx: parseFloat(cs.fontSize),
      textShadow: cs.textShadow,
      boxShadow: cs.boxShadow,
      borderAllFour: bordered(cs),
      color: fg,
      bg: bd.rgb,
      bgImage: bd.image,
      ownText: ownText(el),
      text: (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 240),
      visible: !!(el.getClientRects().length) && cs.visibility !== 'hidden',
    });
  }
  return out;
}
""".replace("FIND_SRC", FIND.strip()).replace("PATH_SRC", PATH.strip())

MOTION = r"""
() => {
  PATH_SRC
  const bad = [];
  let checked = 0;
  for (const el of Array.from(document.querySelectorAll('body, body *'))) {
    for (const pseudo of [null, '::before', '::after']) {
      const cs = getComputedStyle(el, pseudo);
      if (pseudo && (cs.content === 'none' || !cs.content)) continue;
      checked++;
      const name = cs.animationName;
      if (name && name !== 'none' && cs.animationPlayState !== 'paused') {
        bad.push({ path: path(el) + (pseudo || ''), animationName: name,
                   playState: cs.animationPlayState });
      }
    }
  }
  return { checked: checked, violations: bad.slice(0, 12),
           matches: matchMedia('(prefers-reduced-motion: reduce)').matches };
}
""".replace("PATH_SRC", PATH.strip())

SECTION_TEXT = r"""
(titles) => {
  const find = FIND_SRC;
  const el = find(titles);
  return el ? el.textContent : null;
}
""".replace("FIND_SRC", FIND.strip())


def main():
    if len(sys.argv) < 3:
        print(json.dumps({"ok": False, "unsettled": False,
                          "error": "usage: probe.py <index.html> <titles.json>"}))
        return 0
    with open(sys.argv[2], encoding="utf-8") as handle:
        titles = json.load(handle)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        print(json.dumps({"ok": False, "unsettled": True,
                          "error": "playwright is not importable here: %s" % exc}))
        return 0

    import pathlib
    url = pathlib.Path(sys.argv[1]).resolve().as_uri()
    out = {"ok": True, "url": url}
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            try:
                view = {"width": 1280, "height": 900}
                ctx = browser.new_context(viewport=view)
                page = ctx.new_page()
                page.goto(url, wait_until="load")
                page.wait_for_timeout(200)
                out["page"] = page.evaluate(COLLECT, titles)
                out["script_section_text"] = page.evaluate(SECTION_TEXT, titles)
                widths = []
                for w in VIEWPORTS:
                    page.set_viewport_size({"width": w, "height": 900})
                    page.wait_for_timeout(120)
                    row = page.evaluate(
                        "() => ({scrollWidth: document.documentElement.scrollWidth,"
                        " innerWidth: window.innerWidth})")
                    row["width"] = w
                    widths.append(row)
                out["widths"] = widths
                ctx.close()

                rm = browser.new_context(reduced_motion="reduce", viewport=view)
                rmp = rm.new_page()
                rmp.goto(url, wait_until="load")
                rmp.wait_for_timeout(200)
                out["reduced"] = rmp.evaluate(MOTION)
                rm.close()

                nojs = browser.new_context(java_script_enabled=False,
                                           viewport=view)
                njp = nojs.new_page()
                njp.goto(url, wait_until="load")
                njp.wait_for_timeout(200)
                out["noscript_section_text"] = njp.evaluate(SECTION_TEXT, titles)
                nojs.close()
            finally:
                browser.close()
    except Exception as exc:
        text = " ".join(str(exc).split())
        unsettled = ("Executable doesn" in text or "playwright install" in text
                     or "BrowserType.launch" in text
                     or "Target page, context or browser has been closed" in text)
        print(json.dumps({"ok": False, "unsettled": unsettled,
                          "error": "%s: %s" % (type(exc).__name__, text[:400])}))
        return 0
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''

_PROBE_TIMEOUT_S = 300


def _tree_key(scratch):
    digest = hashlib.sha256(str(Path(scratch).resolve()).encode("utf-8"))
    # The probe's own source is part of the key, so a changed probe is
    # never answered from a cache written by the old one.
    digest.update(hashlib.sha256(PROBE_SOURCE.encode("utf-8")).digest())
    for path in sorted(Path(scratch).rglob("*")):
        if not path.is_file() or "node_modules" in path.parts or \
                ".git" in path.parts:
            continue
        try:
            stat = path.stat()
        except OSError:
            continue
        digest.update(str(path.relative_to(scratch)).encode("utf-8"))
        digest.update(b"%d:%d" % (stat.st_size, int(stat.st_mtime)))
    return digest.hexdigest()[:16]


def probe(scratch):
    """Run the browser probe once per tree and cache what it saw.

    Each grader is its own process, so without the cache a full run
    launches Chromium seven times. The key covers every file in the
    tree, so a changed tree is never graded from a stale probe.
    """
    cache = Path(tempfile.gettempdir()) / (
        "eos-drill-house-%s.json" % _tree_key(scratch))
    if cache.is_file():
        try:
            return json.loads(cache.read_text(encoding="utf-8"))
        except ValueError:
            pass

    work = Path(tempfile.mkdtemp(prefix="eos-drill-house-"))
    try:
        script = work / "probe.py"
        script.write_text(PROBE_SOURCE, encoding="utf-8")
        titles = work / "titles.json"
        titles.write_text(json.dumps(service_titles(scratch)), encoding="utf-8")
        page = index_html(scratch)
        if page is None:
            return {"ok": False, "unsettled": False,
                    "error": "no index.html in the delivered tree"}
        env = dict(os.environ)
        env.pop("PYTHONPATH", None)
        try:
            proc = subprocess.run(
                [sys.executable, str(script), str(page), str(titles)],
                capture_output=True, text=True, encoding="utf-8",
                errors="replace", timeout=_PROBE_TIMEOUT_S, env=env)
        except (OSError, subprocess.TimeoutExpired) as exc:
            return {"ok": False, "unsettled": True,
                    "error": "the browser probe would not run: %s" % exc}
        doc = None
        for line in reversed((proc.stdout or "").splitlines()):
            line = line.strip()
            if line.startswith("{"):
                try:
                    doc = json.loads(line)
                except ValueError:
                    continue
                break
        if doc is None:
            tail = " ".join((proc.stderr or "").split())[-300:]
            return {"ok": False, "unsettled": True,
                    "error": "the browser probe printed no result: %s" % tail}
        try:
            cache.write_text(json.dumps(doc), encoding="utf-8")
        except OSError:
            pass
        return doc
    finally:
        import shutil
        shutil.rmtree(work, ignore_errors=True)


def require_probe(cid, scratch):
    """The probe result, or the honest exit when a browser is unavailable."""
    doc = probe(scratch)
    if doc.get("ok"):
        return doc
    if doc.get("unsettled"):
        emit(cid, UNSETTLED,
             "this criterion is a browser assertion and no browser could be "
             "driven here, so it was not settled: %s. That is a gap in the "
             "environment, not a finding against the delivered tree."
             % doc.get("error", "unknown"))
    emit(cid, FAIL, "the browser probe failed against the delivered tree: %s"
         % doc.get("error", "unknown"))
    return doc


def require_section(cid, doc):
    """The rendered services section, or the fail that says it was not built."""
    page = doc.get("page") or {}
    if not page.get("found"):
        emit(cid, FAIL,
             "no element on the page carries all four service offerings from "
             "fixtures/services.json, so the services section was never built "
             "and this criterion has nothing to measure")
    return page


def in_section(elements):
    return [e for e in elements if e.get("visible")]
