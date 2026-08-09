"""Shared helpers for the docs-dx drill graders. Stdlib only.

Not a grader. The runner looks for `c<N>.py` by name, so this file is
never mistaken for a criterion.

Exit codes follow the grader contract: 0 pass, 1 fail, 2 the criterion
cannot be settled in this environment. The third code carries real
weight here. Half of this drill is about what a continuous integration
run does, and a grader cannot watch a hosted CI run. What it can do is
pull the commands out of the committed configuration and run them
itself. Where a command names a third-party binary this machine does
not have, the honest answer is that nothing was settled, not that the
work is wrong.

Three ideas do most of the work:

- `ci_commands` reads shell commands out of whatever automation file
  the tree carries, so the graders reason about what CI actually runs
  rather than about which words appear in a YAML file.
- `run_command` executes one of those in a copy of the tree, and says
  plainly when it cannot.
- `broken_links` is a small fragment-aware link checker, used only as a
  substitute when the declared checker is not installed, and always
  named as a substitute in the reason.
"""

import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

PASS, FAIL, UNSETTLED = 0, 1, 2

TIMEOUT_S = 180

CI_GLOBS = (
    ".github/workflows/*.yml", ".github/workflows/*.yaml",
    ".gitlab-ci.yml", ".gitlab-ci.yaml",
    ".pre-commit-config.yaml", ".pre-commit-config.yml",
    ".circleci/config.yml", ".circleci/config.yaml",
    "azure-pipelines.yml", "azure-pipelines.yaml",
    "Makefile", "makefile", "GNUmakefile",
    "justfile", "Justfile",
    "noxfile.py", "tox.ini",
    "woodpecker.yml", ".drone.yml",
)

# Third-party checkers a solution might reach for. The list is for
# recognition and for deciding whether the invocation is pinned; it is
# not a whitelist, because a checker committed into the tree is also a
# checker and is pinned by definition.
CHECKERS = (
    "lychee", "markdown-link-check", "linkchecker", "linkcheck",
    "liche", "awesome_bot", "awesome-bot", "remark-validate-links",
    "urlchecker", "hyperlink", "mlc", "linkspector", "deadlink",
)

# Evidence that fragments, meaning the part after `#`, are checked.
FRAGMENT_TOKENS = (
    "--include-fragments", "include_fragments", "include-fragments",
    "--check-anchors", "check-anchors", "checkanchors", "check_anchors",
    "--fragments", "--anchors", "--anchor", "anchor",
)

# Evidence that external, network-reaching links are deliberately left
# alone. Criterion 7 turns on this when the checker cannot be run.
OFFLINE_TOKENS = (
    "--offline", "--no-external", "--exclude-all-external",
    "--exclude-external", "offline = true", "offline: true",
    "--local-only", "--internal-only", "--no-web",
)
ONLINE_TOKENS = (
    "--check-extern", "--external", "--online", "--check-external",
)

# Commands that install or fetch. Running them needs a network the
# drill forbids, and they are never the step under test.
SETUP_MARKERS = (
    "pip install", "pip3 install", "python -m pip", "uv pip", "uv sync",
    "npm install", "npm ci", "npm i ", "yarn ", "pnpm ", "npx ",
    "apt-get", "apt ", "sudo ", "brew ", "curl ", "wget ", "docker ",
    "cargo install", "go install", "gem install", "git clone",
    "actions/", "setup-python", "checkout@", "poetry install",
)

BLOCK_SCALARS = ("|", ">", "|-", ">-", "|+", ">+")


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


def frozen_fixture():
    """The scenario tree as it was before the agent touched it.

    Criterion 2 asks for the check to go red against the original
    fixture, so a grader needs the original. It sits two directories up
    from the graders, at a path the runner already relies on.
    """
    path = Path(__file__).resolve().parents[2] / "scenarios" / "docs-dx"
    return path if path.is_dir() else None


# ------------------------------------------------------------ CI files


def ci_files(scratch):
    """Every committed automation file, in a stable order."""
    found = []
    for pattern in CI_GLOBS:
        for path in sorted(Path(scratch).glob(pattern)):
            if path.is_file() and path not in found:
                found.append(path)
    return found


def rel(scratch, path):
    try:
        return Path(path).relative_to(scratch).as_posix()
    except ValueError:
        return str(path)


# ------------------------------------------------------ command reading


def _join_continuations(lines):
    out, buffer = [], ""
    for line in lines:
        if line.rstrip().endswith("\\"):
            buffer += line.rstrip()[:-1].strip() + " "
            continue
        out.append((buffer + line.strip()).strip())
        buffer = ""
    if buffer.strip():
        out.append(buffer.strip())
    return [o for o in out if o]


def _yaml_run_blocks(text, key):
    """Values of `key:` in a YAML-ish file, block scalars included."""
    lines = text.splitlines()
    found, i = [], 0
    pattern = re.compile(r"^(\s*)(?:-\s+)?%s:\s*(.*?)\s*$" % key)
    while i < len(lines):
        m = pattern.match(lines[i])
        if not m:
            i += 1
            continue
        indent = len(m.group(1))
        value = m.group(2)
        if value in BLOCK_SCALARS:
            body, j = [], i + 1
            while j < len(lines):
                nxt = lines[j]
                if nxt.strip():
                    if len(nxt) - len(nxt.lstrip()) <= indent:
                        break
                    body.append(nxt.strip())
                j += 1
            found.extend(_join_continuations(body))
            i = j
        else:
            if value:
                found.append(value.strip().strip("'\""))
            i += 1
    return found


def _yaml_list_under(text, key):
    """List items under `key:`, as GitLab's `script:` writes them."""
    lines = text.splitlines()
    found, i = [], 0
    pattern = re.compile(r"^(\s*)%s:\s*$" % key)
    while i < len(lines):
        m = pattern.match(lines[i])
        if not m:
            i += 1
            continue
        indent = len(m.group(1))
        j = i + 1
        while j < len(lines):
            nxt = lines[j]
            if not nxt.strip():
                j += 1
                continue
            if len(nxt) - len(nxt.lstrip()) <= indent:
                break
            item = re.match(r"^\s*-\s+(.*?)\s*$", nxt)
            if item:
                found.append(item.group(1).strip().strip("'\""))
            j += 1
        i = j
    return found


def make_targets(text):
    """Recipe lines per target in a Makefile."""
    targets, current = {}, None
    for line in text.splitlines():
        if line.startswith("\t"):
            if current is not None:
                body = line[1:].strip().lstrip("@-").strip()
                if body and not body.startswith("#"):
                    targets[current].append(body)
            continue
        m = re.match(r"^([A-Za-z0-9_.\-/]+)\s*:(?!=)", line)
        if m:
            current = m.group(1)
            targets.setdefault(current, [])
    return targets


def ci_commands(scratch):
    """Shell commands the committed automation would run.

    Returns a list of `(source, command)`. Install and checkout steps
    are dropped: they need the network the drill forbids and are never
    the step a criterion is about.
    """
    out = []
    for path in ci_files(scratch):
        where = rel(scratch, path)
        text = read(path)
        commands = []
        if path.name in ("Makefile", "makefile", "GNUmakefile"):
            for target, body in make_targets(text).items():
                commands.extend(body)
        elif path.name in ("justfile", "Justfile"):
            for line in text.splitlines():
                if line.startswith((" ", "\t")) and line.strip():
                    commands.append(line.strip())
        else:
            commands.extend(_yaml_run_blocks(text, "run"))
            commands.extend(_yaml_run_blocks(text, "entry"))
            commands.extend(_yaml_list_under(text, "script"))
            commands.extend(_yaml_list_under(text, "commands"))
        for command in commands:
            command = command.strip()
            if not command or command.startswith("#"):
                continue
            lowered = command.lower()
            if any(marker in lowered for marker in SETUP_MARKERS):
                continue
            out.append((where, command))
    return out


def expand_make(scratch, command):
    """`make docs` becomes the recipe lines, since make may be absent."""
    m = re.match(r"^make\s+([A-Za-z0-9_.\-/]+)\s*$", command.strip())
    if not m or shutil.which("make"):
        return [command]
    for name in ("Makefile", "makefile", "GNUmakefile"):
        path = Path(scratch) / name
        if path.is_file():
            body = make_targets(read(path)).get(m.group(1))
            if body:
                return body
    return [command]


# ------------------------------------------------------------- running


def _env(scratch):
    env = dict(os.environ)
    interpreter = str(Path(sys.executable).parent)
    env["PATH"] = interpreter + os.pathsep + env.get("PATH", "")
    env["PYTHONIOENCODING"] = "utf-8"
    env["CI"] = "true"
    return env


def run_command(command, cwd, timeout=TIMEOUT_S):
    """Run one command in `cwd`.

    Returns `(code, output)`, or `(None, why)` when this machine cannot
    run it at all. A Python invocation is run through this interpreter
    directly; anything else needs a shell, and where there is none the
    criterion is left unsettled rather than guessed at.
    """
    command = command.strip()
    argv = None
    if re.match(r"^(python3?|py)\s", command):
        try:
            parts = shlex.split(command, posix=True)
        except ValueError:
            parts = command.split()
        argv = [sys.executable] + parts[1:]
    elif re.match(r"^[\w./\\-]+\.py\s*", command):
        try:
            parts = shlex.split(command, posix=True)
        except ValueError:
            parts = command.split()
        argv = [sys.executable] + parts
    else:
        head = command.split()[0] if command.split() else ""
        head = head.strip("'\"")
        local = Path(cwd) / head
        if not shutil.which(head) and not local.is_file():
            return None, "no %r on this machine" % head
        shell = shutil.which("bash") or shutil.which("sh")
        if shell is None:
            return None, "no shell available to run %r" % command
        argv = [shell, "-c", command]
    try:
        proc = subprocess.run(argv, cwd=str(cwd), capture_output=True,
                              text=True, encoding="utf-8", errors="replace",
                              timeout=timeout, env=_env(cwd))
    except subprocess.TimeoutExpired:
        return 124, "timed out after %ds" % timeout
    except OSError as exc:
        return None, str(exc)
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def one_line(text, limit=240):
    return " ".join(str(text).split())[:limit]


# ------------------------------------------------------ link checking


def looks_like_link_checker(scratch, command):
    """Does this command run a link checker?

    Either it names one of the known tools, or it runs a file committed
    in the tree whose own source is about links. The second case
    matters: a checker written into the repository is pinned in the
    strongest sense available, because it cannot change under the
    project without a commit.
    """
    lowered = command.lower()
    for name in CHECKERS:
        if name in lowered:
            return name
    for path in named_files(scratch, command):
        body = read(path).lower()
        if "link" in path.name.lower() or "broken link" in body or (
                "link" in body and ".md" in body):
            return rel(scratch, path)
    return None


def named_files(scratch, command):
    """Files in the tree that a command names as arguments."""
    try:
        parts = shlex.split(command, posix=True)
    except ValueError:
        parts = command.split()
    found = []
    for part in parts:
        candidate = Path(scratch) / part.strip("'\"")
        if candidate.is_file():
            found.append(candidate)
    return found


def link_check_commands(scratch):
    """`(source, command, checker)` for every link-checking step."""
    out = []
    for where, command in ci_commands(scratch):
        checker = looks_like_link_checker(scratch, command)
        if checker:
            out.append((where, command, checker))
    return out


def markdown_files(root):
    skip = {".git", "node_modules", ".venv", "venv", "__pycache__"}
    found = []
    for path in Path(root).rglob("*.md"):
        if skip & set(path.parts):
            continue
        found.append(path)
    return sorted(found)


_LINK_RE = re.compile(r"(?<!\!)\[[^\]]*\]\(\s*<?([^)>\s]+)>?[^)]*\)")
_REFDEF_RE = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*<?([^\s>]+)>?", re.M)
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$", re.M)
_EXPLICIT_ANCHOR_RE = re.compile(
    r"""<a\s[^>]*(?:name|id)\s*=\s*["']([^"']+)["']|\{#([\w.-]+)\}""", re.I)
_EXTERNAL_RE = re.compile(r"^[a-z][a-z0-9+.-]*:", re.I)


def slug(text):
    """A heading's anchor, the way GitHub and most renderers make it."""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = text.replace("`", "").replace("*", "").replace("~", "")
    text = re.sub(r"[^\w\s-]", "", text.strip().lower(), flags=re.U)
    return re.sub(r"\s+", "-", text.strip())


def anchors_of(path):
    text = read(path)
    found, seen = set(), {}
    for _, title in _HEADING_RE.findall(text):
        base = slug(title)
        if not base:
            continue
        n = seen.get(base, 0)
        seen[base] = n + 1
        found.add(base if n == 0 else "%s-%d" % (base, n))
    for a, b in _EXPLICIT_ANCHOR_RE.findall(text):
        found.add(a or b)
    return found


def links_in(path):
    text = read(path)
    return _LINK_RE.findall(text) + _REFDEF_RE.findall(text)


def broken_links(root, include_external=False):
    """Relative links and fragments that do not resolve, as strings.

    A substitute for the project's own checker, used only when that
    checker cannot be run here. External links are ignored unless asked
    for, which is criterion 7's whole subject.
    """
    root = Path(root)
    problems = []
    for path in markdown_files(root):
        where = rel(root, path)
        for target in links_in(path):
            target = target.strip()
            if not target or target.startswith("#") and len(target) == 1:
                continue
            if _EXTERNAL_RE.match(target) and not target.startswith("#"):
                if include_external:
                    problems.append("%s: external link %s" % (where, target))
                continue
            path_part, _, fragment = target.partition("#")
            if path_part:
                if path_part.startswith("/"):
                    dest = root / path_part.lstrip("/")
                else:
                    dest = (path.parent / path_part).resolve()
                if not dest.exists():
                    problems.append("%s: %s does not exist" % (where, target))
                    continue
            else:
                dest = path
            if fragment and dest.is_file() and dest.suffix.lower() == ".md":
                if fragment.lower() not in {a.lower()
                                            for a in anchors_of(dest)}:
                    problems.append("%s: no heading matches #%s in %s"
                                    % (where, fragment,
                                       rel(root, dest) if dest != path
                                       else where))
    return problems


# ------------------------------------------------------------ injection


def docs_target(root):
    """The docs page a grader injects into: quickstart if it is there."""
    root = Path(root)
    preferred = root / "docs" / "quickstart.md"
    if preferred.is_file():
        return preferred
    candidates = [p for p in markdown_files(root)
                  if p.parent.name == "docs"]
    return candidates[0] if candidates else None
