"""Changed-surface context packet generator.

Builds the packet the context command emits: the changed files against
a merge base, their front-matter summaries, the files that reference
them, activated packs (placeholder until packs exist) and the routed
tier from the task router.

This module deliberately does not import tools.eos.frontmatter, to
avoid import-order coupling across lanes. The minimal reader below is a
duplicate on purpose; tools/eos/frontmatter.py is the canonical,
hardened parser and wins wherever the two disagree.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from tools.eos import router

_SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "node_modules"}
_TEXT_SUFFIXES = {".md", ".txt", ".json", ".yml", ".yaml", ".py", ".toml", ".html", ".sql"}


def _read_front_matter(text):
    # Minimal front-matter reader; tools/eos/frontmatter.py is canonical.
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    data = {}
    for line in lines[1:60]:
        stripped = line.strip()
        if stripped == "---":
            return data
        if not stripped or stripped.startswith("#"):
            continue
        if ":" in line and not line.startswith((" ", "\t", "-")):
            key, _, value = line.partition(":")
            data[key.strip()] = value.strip()
    return {}


def _git(root, *args):
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if proc.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), proc.stderr.strip()))
    return proc.stdout


def _changed_files(root, base_ref):
    merge_base = _git(root, "merge-base", "HEAD", base_ref).strip() or base_ref
    out = _git(root, "diff", "--name-only", merge_base)
    return merge_base, [p.replace("\\", "/") for p in out.splitlines() if p.strip()]


def build_packet(root, base_ref=None, files=None):
    """Build the context packet dict for the changed surface.

    Either base_ref (diffed against the merge base with HEAD) or an
    explicit files list drives the changed set. Returns {changed,
    summaries, referencing_files, activated_packs, routed}.
    """
    root = Path(root)
    merge_base = None
    if files is not None:
        changed = [str(f).replace("\\", "/") for f in files]
    elif base_ref is not None:
        merge_base, changed = _changed_files(root, base_ref)
    else:
        changed = []

    summaries = {}
    for rel in changed:
        path = root / rel
        if not path.is_file():
            summaries[rel] = "(deleted)"
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            summaries[rel] = "(unreadable)"
            continue
        fm = _read_front_matter(text)
        summaries[rel] = fm.get("summary", "(no front matter)")

    # Reverse-reference scan: files whose text mentions a changed path
    # or its bare name. Data is data; mentions are listed, never obeyed.
    mention_keys = {}
    for rel in changed:
        mention_keys[rel] = rel
        stem = rel.rsplit("/", 1)[-1]
        if stem not in mention_keys:
            mention_keys[stem] = rel
    referencing = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in _TEXT_SUFFIXES:
            continue
        rel = path.relative_to(root).as_posix()
        if any(part in _SKIP_DIRS for part in path.parts):
            continue
        if rel in changed:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for key, target in mention_keys.items():
            if key and key in text:
                referencing.setdefault(target, [])
                if rel not in referencing[target]:
                    referencing[target].append(rel)

    if base_ref is not None and merge_base:
        derived = router.derive_signals(root, merge_base, {})
    else:
        derived = {"changed_paths": changed, "diff_lines": 0,
                   "diff_files": len(changed), "signals": {}}
    routed = router.route({}, derived, None)

    return {
        "changed": changed,
        "summaries": summaries,
        "referencing_files": referencing,
        "activated_packs": [],
        "routed": {"tier": routed["tier"], "reasons": routed["reasons"]},
    }
