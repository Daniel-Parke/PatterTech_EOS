"""Shared helpers for the DRILL-UIUX-002 graders. Stdlib only.

Not a grader. The runner looks for `c<N>.py` by name, so this file is
never mistaken for a criterion.

Exit codes follow the grader contract: 0 pass, 1 fail, 2 the criterion
cannot be settled in this environment. The third is used by c7, which
measures contrast in a real browser engine and has nothing to say on a
machine with no engine installed.

Two fixed inputs live here as constants: Almsford's navy and their
typeface. They are copied from the scenario's `docs/brand.md`, which
the drill's freeze note names as a fixed input, and they are held here
rather than read from the tree so that an attempt cannot pass by
rewriting the client's brand book.
"""

import json
import re
import sys
from pathlib import Path

PASS, FAIL, UNSETTLED = 0, 1, 2

REPO_ROOT = Path(__file__).resolve().parents[4]
LEDGER = REPO_ROOT / "registry" / "evidence.json"

# Fixed inputs, mirroring benchmark/drills/scenarios/ui-ux-greenfield/docs/brand.md
CLIENT_NAVY = (0x0E, 0x2A, 0x47)
CLIENT_TYPEFACE = "Almsford Grotesk"

SKIP_DIRS = {".git", "node_modules", "dist", "build", "out", ".next",
             "coverage", "playwright-report", "test-results", "__pycache__",
             ".venv", "venv", ".cache", "vendor"}

STYLE_SUFFIXES = {".css", ".scss", ".sass", ".less"}
MARKUP_SUFFIXES = {".html", ".htm", ".vue", ".svelte", ".astro", ".jinja",
                   ".j2", ".hbs", ".ejs", ".njk"}
SCRIPT_SUFFIXES = {".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx"}
SOURCE_SUFFIXES = STYLE_SUFFIXES | MARKUP_SUFFIXES | SCRIPT_SUFFIXES
TEXT_SUFFIXES = {".md", ".markdown", ".json", ".yaml", ".yml", ".txt",
                 ".toml", ".rst"}


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


def walk(scratch, suffixes=None):
    """Every file under the tree, minus the noise directories."""
    out = []
    for path in sorted(Path(scratch).rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if suffixes is not None and path.suffix.lower() not in suffixes:
            continue
        out.append(path)
    return out


def rel(scratch, path):
    try:
        return Path(path).relative_to(scratch).as_posix()
    except ValueError:
        return str(path)


def source_files(scratch):
    return walk(scratch, SOURCE_SUFFIXES)


def text_files(scratch):
    return walk(scratch, TEXT_SUFFIXES)


# ---------------------------------------------------------------- colour

NAMED_COLOURS = {
    "white": (255, 255, 255), "black": (0, 0, 0), "navy": (0, 0, 128),
    "red": (255, 0, 0), "orange": (255, 165, 0), "gold": (255, 215, 0),
    "amber": (255, 191, 0), "tomato": (255, 99, 71), "coral": (255, 127, 80),
    "chocolate": (210, 105, 30), "peru": (205, 133, 63), "tan": (210, 180, 140),
    "khaki": (240, 230, 140), "wheat": (245, 222, 179),
    "beige": (245, 245, 220), "ivory": (255, 255, 240),
    "cornsilk": (255, 248, 220), "linen": (250, 240, 230),
    "seashell": (255, 245, 238), "oldlace": (253, 245, 230),
    "floralwhite": (255, 250, 240), "antiquewhite": (250, 235, 215),
    "blanchedalmond": (255, 235, 205), "bisque": (255, 228, 196),
    "moccasin": (255, 228, 181), "peachpuff": (255, 218, 185),
    "papayawhip": (255, 239, 213), "lemonchiffon": (255, 250, 205),
    "lightyellow": (255, 255, 224), "sienna": (160, 82, 45),
    "firebrick": (178, 34, 34), "darkorange": (255, 140, 0),
    "goldenrod": (218, 165, 32), "burlywood": (222, 184, 135),
    "sandybrown": (244, 164, 96), "salmon": (250, 128, 114),
}

_HEX_RE = re.compile(r"#([0-9a-fA-F]{3,8})\b")
_FUNC_RE = re.compile(r"\b(rgba?|hsla?)\(([^()]*)\)", re.I)
_NAME_RE = re.compile(r"\b(%s)\b" % "|".join(sorted(NAMED_COLOURS)), re.I)


def _hex_to_rgb(digits):
    if len(digits) in (3, 4):
        digits = "".join(c * 2 for c in digits[:3])
    elif len(digits) in (6, 8):
        digits = digits[:6]
    else:
        return None
    return tuple(int(digits[i:i + 2], 16) for i in (0, 2, 4))


def _hsl_to_rgb(h, s, lightness):
    h = (h % 360) / 360.0
    if s <= 0:
        v = int(round(lightness * 255))
        return (v, v, v)
    q = lightness * (1 + s) if lightness < 0.5 else lightness + s - lightness * s
    p = 2 * lightness - q

    def channel(t):
        t = t % 1.0
        if t < 1 / 6:
            return p + (q - p) * 6 * t
        if t < 1 / 2:
            return q
        if t < 2 / 3:
            return p + (q - p) * (2 / 3 - t) * 6
        return p
    return tuple(int(round(channel(h + off) * 255))
                 for off in (1 / 3, 0, -1 / 3))


def parse_colour(value):
    """One colour out of a CSS value string, or None."""
    value = (value or "").strip()
    m = _HEX_RE.fullmatch(value) or _HEX_RE.match(value)
    if m:
        return _hex_to_rgb(m.group(1))
    m = _FUNC_RE.search(value)
    if m:
        return _func_colour(m.group(1).lower(), m.group(2))
    m = _NAME_RE.fullmatch(value.strip())
    if m:
        return NAMED_COLOURS[m.group(1).lower()]
    return None


def _func_colour(kind, args):
    parts = [p for p in re.split(r"[,/\s]+", args.strip()) if p]
    if len(parts) < 3:
        return None
    try:
        if kind.startswith("rgb"):
            nums = []
            for part in parts[:3]:
                if part.endswith("%"):
                    nums.append(float(part[:-1]) * 255 / 100)
                else:
                    nums.append(float(part))
            return tuple(max(0, min(255, int(round(n)))) for n in nums)
        hue = float(re.sub(r"deg$", "", parts[0]))
        sat = float(parts[1].rstrip("%")) / 100.0
        lig = float(parts[2].rstrip("%")) / 100.0
        return _hsl_to_rgb(hue, sat, lig)
    except ValueError:
        return None


def colours_in(text):
    """Every colour literal in a blob of source, with its written form."""
    found = []
    for m in _HEX_RE.finditer(text):
        rgb = _hex_to_rgb(m.group(1))
        if rgb:
            found.append((m.group(0), rgb))
    for m in _FUNC_RE.finditer(text):
        rgb = _func_colour(m.group(1).lower(), m.group(2))
        if rgb:
            found.append((m.group(0), rgb))
    for m in _NAME_RE.finditer(text):
        found.append((m.group(0), NAMED_COLOURS[m.group(1).lower()]))
    return found


def hcl(rgb):
    """Hue in degrees, chroma 0 to 1, lightness 0 to 1. Not perceptual."""
    r, g, b = (c / 255.0 for c in rgb)
    hi, lo = max(r, g, b), min(r, g, b)
    chroma = hi - lo
    light = (hi + lo) / 2
    if chroma == 0:
        return 0.0, 0.0, light
    if hi == r:
        hue = 60 * (((g - b) / chroma) % 6)
    elif hi == g:
        hue = 60 * (((b - r) / chroma) + 2)
    else:
        hue = 60 * (((r - g) / chroma) + 4)
    return hue % 360, chroma, light


def luminance(rgb):
    def channel(v):
        v = v / 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg, bg):
    a, b = luminance(fg), luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def hex_of(rgb):
    return "#%02x%02x%02x" % rgb


# ------------------------------------------------------------------- css


def strip_css_comments(text):
    return re.sub(r"/\*.*?\*/", " ", text, flags=re.S)


def css_rules(text):
    """(selector, declarations, at-rule context) for every rule in a sheet.

    A hand-rolled scanner rather than a parser: the graders only ask
    which selectors carry which properties, and that survives the
    approximation. Declarations directly inside an at-rule block are
    dropped, which only loses `@font-face`-style blocks nothing here
    asks about.
    """
    text = strip_css_comments(text)
    rules, stack, buf = [], [], ""
    for ch in text:
        if ch == "{":
            stack.append(" ".join(buf.split()))
            buf = ""
        elif ch == "}":
            selector = stack.pop() if stack else ""
            body, buf = buf, ""
            if selector and not selector.startswith("@"):
                decls = css_declarations(body)
                if decls:
                    rules.append((selector, decls, list(stack)))
        else:
            buf += ch
    return rules


def css_declarations(body):
    out = {}
    for chunk in re.split(r";(?![^(]*\))", body):
        if ":" not in chunk:
            continue
        prop, value = chunk.split(":", 1)
        prop = prop.strip().lower()
        value = " ".join(value.split())
        if prop:
            out[prop] = value
    return out


def custom_properties(scratch):
    """Every `--name: value` declared anywhere in the delivered styles."""
    props = {}
    for path in walk(scratch, STYLE_SUFFIXES | MARKUP_SUFFIXES):
        for selector, decls, _ in css_rules(read(path)):
            for prop, value in decls.items():
                if prop.startswith("--"):
                    props.setdefault(prop, value)
    return props


def resolve(value, props, depth=0):
    """Resolve var() references against the collected custom properties."""
    if depth > 8 or not value:
        return value

    def swap(m):
        name, fallback = m.group(1), m.group(2)
        if name in props:
            return resolve(props[name], props, depth + 1)
        return (fallback or "").strip()
    return re.sub(r"var\(\s*(--[\w-]+)\s*(?:,([^()]*))?\)", swap, value)


def font_stacks(scratch):
    """(file, source line, families) for every font stack in the styles."""
    stacks = []
    files = walk(scratch, STYLE_SUFFIXES | MARKUP_SUFFIXES | SCRIPT_SUFFIXES)
    pattern = re.compile(
        r"(?:font-family|fontFamily|--[\w-]*(?:font|type|family)[\w-]*)\s*"
        r"[:=]\s*([^;{}\n]+)", re.I)
    for path in files:
        text = strip_css_comments(read(path))
        for m in pattern.finditer(text):
            raw = m.group(1).strip().strip(",").strip()
            families = split_families(raw)
            if families:
                stacks.append((path, raw, families))
    return stacks


def split_families(raw):
    raw = raw.strip().strip("'\"`").strip()
    out = []
    for part in raw.split(","):
        name = " ".join(part.split()).strip("'\" \t;")
        if not name or name.startswith("var("):
            continue
        if re.search(r"[{}()]", name):
            continue
        out.append(name)
    return out


# ------------------------------------------------------- philosophy record

PHILOSOPHIES = {
    "A": ("Content-first public service",
          [r"content[\s-]*first", r"public service"]),
    "B": ("Dense enterprise", [r"dense enterprise", r"enterprise (design )?"
                               r"system"]),
    "C": ("Consumer and lifestyle, expressive",
          [r"consumer (and|&) lifestyle", r"expressive consumer"]),
    "D": ("Editorial", [r"\beditorial\b"]),
    "E": ("Conversion-led landing",
          [r"conversion[\s-]*led", r"landing page philosophy"]),
    "F": ("Data-heavy dashboard",
          [r"data[\s-]*heavy", r"\bdashboard\b"]),
    "G": ("Mobile-native, platform-conformant",
          [r"mobile[\s-]*native", r"platform[\s-]*conformant"]),
    "H": ("Restrained minimal", [r"restrained minimal", r"minimal(ism)? "
                                 r"axis"]),
}

_LETTER_RE = re.compile(r"(?:^|\b)(?:option|philosophy)?\s*\(?\b([A-H])\b"
                        r"[).:\-–—]", re.I)

_FIELD_RE = re.compile(
    r"^\s*(?:[-*+>]\s*)?[\"'\*_]*\s*([A-Za-z][A-Za-z0-9 _\-]{0,48}?)"
    r"[\"'\*_]*\s*[:=–—]\s*(.+?)\s*,?\s*$")

_RUNNER_WORDS = ("runner", "alternative", "rejected", "considered",
                 "second choice", "not chosen", "instead of", "against")


def philosophies_in(value):
    """Which philosophies a written value names, as a set of letters."""
    found = set()
    low = value.lower()
    for letter, (_, patterns) in PHILOSOPHIES.items():
        for pattern in patterns:
            if re.search(pattern, low):
                found.add(letter)
                break
    m = _LETTER_RE.search(value.strip())
    if m:
        found.add(m.group(1).upper())
    return found


def philosophy_fields(text):
    """(chosen, runner_up) labelled fields naming a philosophy.

    A record is read through labelled fields rather than through prose,
    because a paragraph that mentions six philosophies has not chosen
    one. Accepted shapes are a key and a value on one line (markdown,
    front matter, JSON, YAML) and a two-column table row.

    A field counts when its label mentions a philosophy, or when the
    label is a runner-up label (`Runner-up:`, `Alternative considered:`)
    and the value names one.
    """
    chosen, runners = [], []
    for line in text.splitlines():
        label = value = None
        cells = [c.strip() for c in line.strip().strip("|").split("|")] \
            if line.strip().startswith("|") else []
        if len(cells) >= 2 and cells[0]:
            label, value = cells[0], cells[1]
        else:
            m = _FIELD_RE.match(line)
            if m:
                label, value = m.group(1), m.group(2)
        if label is None:
            continue
        value = value.strip().strip("\"'`,")
        if not value or value in ("|", "---"):
            continue
        label_low = label.lower()
        runner = (any(word in label_low for word in _RUNNER_WORDS)
                  or any(word in value.lower() for word in _RUNNER_WORDS))
        if "philosoph" in label_low and not runner:
            chosen.append((label.strip(), value))
        elif runner and philosophies_in(value):
            runners.append((label.strip(), value))
    return chosen, runners


_RUNNER_SENTENCE = re.compile(r"[^.?!]*\b(runner[\s-]?up|alternative|"
                              r"considered|rejected|second choice|"
                              r"gave (?:it |them )?up|not taken)\b[^.?!]*",
                              re.I)


def runner_up_letters(text, chosen):
    """Philosophies the record names as the road not taken."""
    letters = set()
    _, fields = philosophy_fields(text)
    for _, value in fields:
        letters |= philosophies_in(value)
    for match in _RUNNER_SENTENCE.finditer(text):
        letters |= philosophies_in(match.group(0))
    letters.discard(chosen)
    return letters


def records(scratch):
    """Every text file carrying a labelled chosen-philosophy field."""
    out = []
    for path in text_files(scratch):
        text = read(path)
        if "philosoph" not in text.lower():
            continue
        chosen, runners = philosophy_fields(text)
        if chosen:
            out.append((path, text, chosen, runners))
    return out


def evidence_ids(text):
    return sorted(set(re.findall(r"\bEV-\d{3,4}\b", text)))


def ledger_ids():
    """The evidence ids that resolve in the estate ledger, or None."""
    if not LEDGER.is_file():
        return None
    try:
        doc = json.loads(LEDGER.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    rows = doc.get("records")
    if not isinstance(rows, list):
        return None
    return {str(row.get("id")) for row in rows if isinstance(row, dict)}
