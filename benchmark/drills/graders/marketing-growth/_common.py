"""Shared helpers for the marketing-growth drill graders. Stdlib only.

Not a grader. The runner looks for `c<N>.py` by name, so this file is
never mistaken for a criterion.

Exit codes follow the grader contract: 0 pass, 1 fail, 2 the criterion
cannot be settled in this environment. The third is used where the thing
a criterion needs is missing from the machine rather than from the
delivered tree: the hosted structured-data validator criterion 1 names,
a YAML parser for a funnel configuration written in YAML, the pack guide
criterion 9 reads its option lists from. In each of those the honest
answer is that nothing was looked at, and reporting that as a fail
invents a finding against work nobody inspected.

Three things this module deliberately does not do.

It does not carry its own copy of the pack's philosophy or measurement
lists. Criterion 9 says "one philosophy from the pack list", so the
grader reads the pack's guide. A second copy here would drift, and the
drill would then be grading a list no venture ever sees.

It does not execute the delivered tree in place. Criterion 6 writes to a
suppression store and criterion 8 writes a synthetic contact record, so
everything that mutates works on a throwaway copy. A grader that leaves
marks on the tree it graded cannot be run twice.

It does not accept a redirect chain as a missing page or a directory
listing as a page. The static server it runs for criterion 3 answers 404
for a directory with no index, because a host that lists a directory is
not serving a page.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import xml.etree.ElementTree as ET
from contextlib import contextmanager
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import urlopen

PASS, FAIL, UNSETTLED = 0, 1, 2

SITE = "site"
LIFECYCLE = "lifecycle"

# Directory names that never hold a published page, a live robots profile
# or a message in the sequence. Negative fixtures live in some of these
# on purpose, and counting them as delivered content would fail a tree
# for doing the right thing.
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv",
             "fixtures", "fixture", "tests", "test", "staging", "partials",
             "_partials", "drafts", "draft", "examples", "samples"}

MESSAGE_DIRS = {"emails", "email", "messages", "sequence", "mail",
                "welcome"}
MESSAGE_SUFFIXES = {".eml", ".msg", ".email", ".mime", ".txt"}


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
    benchmark -> root. The graded tree is somewhere else entirely, which
    is the point: the pack's guides belong to the pack being tested, not
    to the agent's delivery.
    """
    return Path(__file__).resolve().parents[4]


def skipped(scratch, path):
    parts = [p.lower() for p in Path(path).relative_to(scratch).parts[:-1]]
    return any(p in SKIP_DIRS for p in parts)


def walk(scratch, pattern="*"):
    """Files that are delivered content: no fixtures, no test trees."""
    for path in sorted(Path(scratch).rglob(pattern)):
        if path.is_file() and not skipped(scratch, path):
            yield path


NEVER = {".git", "__pycache__", "node_modules", ".venv", "venv"}


def all_files(scratch, pattern="*"):
    """Every file in the tree, machinery aside.

    Used where a fixture or a test tree is the thing being looked for,
    which `walk` deliberately hides.
    """
    for path in sorted(Path(scratch).rglob(pattern)):
        if not path.is_file():
            continue
        rel = path.relative_to(scratch)
        if any(p in NEVER for p in rel.parts[:-1]):
            continue
        yield path


# ------------------------------------------------------------------- site


def site_dir(scratch):
    path = Path(scratch) / SITE
    return path if path.is_dir() else None


def html_pages(scratch):
    """Every published page under site/.

    A page whose name starts with an underscore, or that is the 404
    document, is not published content and is left out.
    """
    root = site_dir(scratch)
    if root is None:
        return []
    out = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in (".html", ".htm"):
            continue
        rel = path.relative_to(root)
        if any(p.lower() in SKIP_DIRS for p in rel.parts[:-1]):
            continue
        if path.name.startswith("_") or path.stem in ("404", "500"):
            continue
        out.append(path)
    return out


class _Text(HTMLParser):
    """Rendered text plus the JSON-LD blocks, in one pass."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.chunks = []
        self.blocks = []
        self._stack = []
        self._ld = None

    def handle_starttag(self, tag, attrs):
        self._stack.append(tag)
        if tag == "script":
            kind = dict(attrs).get("type", "").strip().lower()
            if kind == "application/ld+json":
                self._ld = []

    def handle_endtag(self, tag):
        if tag == "script" and self._ld is not None:
            self.blocks.append("".join(self._ld))
            self._ld = None
        while self._stack:
            if self._stack.pop() == tag:
                break

    def handle_data(self, data):
        if self._ld is not None:
            self._ld.append(data)
            return
        if any(t in ("script", "style") for t in self._stack):
            return
        self.chunks.append(data)


def _parsed(html):
    parser = _Text()
    try:
        parser.feed(html)
        parser.close()
    except Exception:  # noqa: BLE001 - a broken page still yields what it had
        pass
    return parser


def visible_text(html):
    """What a reader sees, whitespace collapsed.

    The title is included: it is rendered, in the tab and in the result
    listing, and a name property that only matches the title is not an
    orphan.
    """
    return re.sub(r"\s+", " ", " ".join(_parsed(html).chunks)).strip()


def jsonld_blocks(html):
    """Return (parsed_documents, unparseable_block_count)."""
    docs, broken = [], 0
    for raw in _parsed(html).blocks:
        try:
            docs.append(json.loads(raw))
        except ValueError:
            broken += 1
    return docs, broken


def url_path(scratch, page):
    """The path a page is served at, as a sitemap would spell it."""
    rel = Path(page).relative_to(site_dir(scratch)).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def path_forms(path):
    """Every spelling of one URL path that means the same document.

    A host may serve `/pricing.html`, `/pricing` or `/pricing/` for the
    same file, and a sitemap written in any of the three is not wrong.
    """
    path = path or "/"
    if not path.startswith("/"):
        path = "/" + path
    forms = {path}
    if path.endswith("/index.html"):
        forms.add(path[: -len("index.html")])
    if path.endswith(".html"):
        stem = path[: -len(".html")]
        forms.add(stem)
        forms.add(stem + "/")
    if path.endswith("/") and path != "/":
        forms.add(path[:-1])
        forms.add(path[:-1] + ".html")
        forms.add(path + "index.html")
    if path == "/":
        forms.add("/index.html")
    return forms


# ----------------------------------------------------------------- robots


def robots_files(scratch):
    """Every robots profile in the tree, live one first.

    The live profile is the one the deploy copies, which is the file at
    site/robots.txt. Anything else called robots is a fixture, and
    criterion 2 wants one of those to exist and to be refused.
    """
    live = None
    others = []
    for path in sorted(Path(scratch).rglob("*")):
        if not path.is_file():
            continue
        name = path.name.lower()
        if "robots" not in name or path.suffix.lower() not in (".txt", ""):
            continue
        if ".git" in path.parts:
            continue
        rel = path.relative_to(scratch).as_posix()
        if rel == "site/robots.txt":
            live = path
        else:
            others.append(path)
    return live, others


def parse_robots(text):
    """RFC 9309 parse. Returns {"groups", "sitemaps", "errors"}.

    Unknown fields are ignored rather than rejected, which the RFC
    requires. A line that is not a comment, is not blank and carries no
    colon is a parse error, and so is a rule that belongs to no group.
    """
    groups, sitemaps, errors = [], [], []
    current = None
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if ":" not in line:
            errors.append("line %d is not a field: %r" % (n, raw.strip()))
            continue
        field, value = line.split(":", 1)
        field = field.strip().lower()
        value = value.strip()
        if field == "user-agent":
            if current is None or current["rules"]:
                current = {"agents": [], "rules": []}
                groups.append(current)
            current["agents"].append(value.lower())
        elif field in ("allow", "disallow"):
            if current is None:
                errors.append("line %d: %s with no user-agent above it"
                              % (n, field))
                continue
            current["rules"].append((field, value))
        elif field == "sitemap":
            sitemaps.append(value)
    return {"groups": groups, "sitemaps": sitemaps, "errors": errors}


def group_for(parsed, agent="*"):
    agent = agent.lower()
    exact = [g for g in parsed["groups"] if agent in g["agents"]]
    if exact:
        return exact[0]
    star = [g for g in parsed["groups"] if "*" in g["agents"]]
    return star[0] if star else None


def blanket_disallow(parsed, agent="*"):
    """Does the group that applies to everyone shut the whole site?"""
    group = group_for(parsed, agent)
    if group is None:
        return False
    for kind, value in group["rules"]:
        if kind == "disallow" and value.strip() in ("/", "/*"):
            return True
    return False


def _rule_re(pattern):
    out = ["^"]
    for ch in pattern:
        if ch == "*":
            out.append(".*")
        elif ch == "$":
            out.append("$")
        else:
            out.append(re.escape(ch))
    return re.compile("".join(out))


def robots_allows(parsed, path, agent="*"):
    """Longest match wins, allow wins a tie. RFC 9309 section 2.2.2."""
    group = group_for(parsed, agent)
    if group is None:
        return True
    best_len, best_kind = -1, "allow"
    for kind, value in group["rules"]:
        if not value:
            continue
        if not _rule_re(value).match(path):
            continue
        length = len(value.replace("*", "").replace("$", ""))
        if length > best_len or (length == best_len and kind == "allow"):
            best_len, best_kind = length, kind
    return best_kind == "allow"


# ---------------------------------------------------------------- sitemap


def sitemap_path(scratch):
    root = site_dir(scratch)
    if root is None:
        return None
    for candidate in sorted(root.rglob("sitemap*.xml")):
        return candidate
    return None


def sitemap_locs(path):
    """Every <loc> in a sitemap, or None if the document will not parse."""
    try:
        tree = ET.parse(str(path))
    except (ET.ParseError, OSError):
        return None
    out = []
    for node in tree.getroot().iter():
        if node.tag.rsplit("}", 1)[-1] == "loc" and (node.text or "").strip():
            out.append(node.text.strip())
    return out


class _Static(SimpleHTTPRequestHandler):
    """A plain static host: no directory listings, pretty URLs resolved."""

    def log_message(self, *args):
        pass

    def list_directory(self, path):
        self.send_error(404, "no index in this directory")
        return None

    def translate_path(self, path):
        resolved = super().translate_path(path)
        if os.path.isdir(resolved) or os.path.exists(resolved):
            return resolved
        if os.path.exists(resolved + ".html"):
            return resolved + ".html"
        return resolved


@contextmanager
def serve(directory):
    """Serve a directory on localhost and yield its base URL."""
    handler = type("_Bound", (_Static,),
                   {"__init__": lambda s, *a, **k: _Static.__init__(
                       s, *a, directory=str(directory), **k)})
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield "http://127.0.0.1:%d" % server.server_address[1]
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def status_of(base, path):
    try:
        with urlopen(base + path, timeout=10) as response:
            return response.status
    except HTTPError as exc:
        return exc.code
    except (URLError, OSError):
        return None


# -------------------------------------------------------------- lifecycle


def find_script(scratch, stem, keyword=None):
    """The delivered script for one command, wherever it was put."""
    keyword = keyword or stem
    exact, loose = [], []
    for path in sorted(Path(scratch).rglob("*.py")):
        if ".git" in path.parts or "__pycache__" in path.parts:
            continue
        if path.stem == stem:
            exact.append(path)
        elif keyword in path.stem.lower():
            loose.append(path)
    found = exact or loose
    if not found:
        return None
    found.sort(key=lambda p: (0 if p.parts[-2:-1] == (LIFECYCLE,) else 1,
                              len(p.parts)))
    return found[0]


def run(script, args, cwd, timeout=180):
    """Run a delivered script. Returns (returncode, output)."""
    try:
        proc = subprocess.run(
            [sys.executable, str(script), *[str(a) for a in args]],
            cwd=str(cwd), capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, str(exc)
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


@contextmanager
def work_copy(scratch):
    """A throwaway copy of the delivered tree, for graders that write."""
    tmp = tempfile.mkdtemp(prefix="mktg-drill-")
    dest = Path(tmp) / "tree"
    shutil.copytree(str(scratch), str(dest),
                    ignore=shutil.ignore_patterns(".git", "__pycache__"))
    try:
        yield dest
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def messages(scratch):
    """The delivered sequence messages, in name order."""
    out = []
    for path in Path(scratch).rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(scratch)
        if any(p.lower() in SKIP_DIRS for p in rel.parts[:-1]):
            continue
        if path.suffix.lower() not in MESSAGE_SUFFIXES:
            continue
        if path.parent.name.lower() not in MESSAGE_DIRS:
            continue
        if path.stem.lower() in ("readme", "notes", "index"):
            continue
        out.append(path)
    # A tree that ships real messages beside the drafts they came from is
    # judged on the messages. A plain draft left in the send directory is
    # untidy; it is not a message missing its headers.
    rich = [p for p in out if p.suffix.lower() != ".txt"]
    return sorted(rich or out)


def headers_of(path):
    """Parse one message and return its header map, names lowercased."""
    import email
    from email import policy
    try:
        with open(path, "rb") as handle:
            msg = email.message_from_binary_file(handle,
                                                 policy=policy.default)
    except Exception:  # noqa: BLE001 - an unparseable message has no headers
        return {}
    out = {}
    for name, value in msg.items():
        out.setdefault(name.lower(), []).append(str(value).strip())
    return out


ADDRESS_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")


def contact_files(scratch):
    """Candidate contact stores, the delivered one first."""
    out = []
    for path in walk(scratch):
        name = path.name.lower()
        if path.suffix.lower() not in (".json", ".jsonl", ".ndjson"):
            continue
        if "suppress" in name:
            continue
        if "contact" in name or "consent" in name or "subscriber" in name:
            out.append(path)
    return sorted(out, key=lambda p: (len(p.parts), p.name))


def load_records(path):
    """Contact records from a JSON list, a JSON object or JSON lines."""
    text = read(path)
    if not text.strip():
        return None
    try:
        doc = json.loads(text)
    except ValueError:
        rows = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except ValueError:
                return None
        return rows or None
    if isinstance(doc, list):
        return [r for r in doc if isinstance(r, dict)]
    if isinstance(doc, dict):
        for key in ("contacts", "records", "subscribers", "rows"):
            if isinstance(doc.get(key), list):
                return [r for r in doc[key] if isinstance(r, dict)]
    return None


def suppression_files(scratch):
    return [p for p in walk(scratch) if "suppress" in p.name.lower()]
