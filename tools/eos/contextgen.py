"""Changed-surface context packet generator.

Builds the packet the context command emits: the changed files against
a merge base, their front-matter summaries, the files that reference
them, the packs the change activates, and the routed tier.

Pack activation is the whole point of progressive disclosure, and it
was a hardcoded empty list behind a comment reading "placeholder until
packs exist" while twenty packs sat on disk. That is why loading got
dearer rather than cheaper as the knowledge grew: with no working
activation an agent either reads broadly or guesses, and twenty dense
packs cost more than five thin modules ever did.
"""

from __future__ import annotations

import re
from pathlib import Path

from tools.eos import router
from tools.eos.frontmatter import parse as parse_front_matter
from tools.eos.gitfacts import output as _git

_SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "node_modules"}
_TEXT_SUFFIXES = {".md", ".txt", ".json", ".yml", ".yaml", ".py", ".toml", ".html", ".sql"}


def _read_front_matter(text):
    """Front-matter as a dict, via the canonical hardened parser."""
    fm = parse_front_matter(text)
    return fm.data if fm.present else {}


def _translate(pattern: str) -> re.Pattern:
    """Compile a path glob where `**` crosses separators and `*` does not.

    fnmatch is no use here: its `*` matches `/`, so `**/components/**`
    compiles to something that matches every path in the repository.
    That is not a near miss, it activates all twenty packs on any change
    and makes the whole exercise pointless, so the translation is done
    by hand and tested.
    """
    out, i = [], 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            out.append("(?:[^/]+/)*")   # zero or more whole segments
            i += 3
        elif pattern.startswith("/**", i):
            out.append("(?:/.*)?")      # the subtree, or nothing
            i += 3
        elif pattern[i] == "*":
            out.append("[^/]*")         # within one segment only
            i += 1
        elif pattern[i] == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(pattern[i]))
            i += 1
    return re.compile("^" + "".join(out) + "$", re.IGNORECASE)


_GLOB_CACHE: dict = {}


def _match(path: str, pattern: str) -> bool:
    """A glob against a repo-relative posix path."""
    rx = _GLOB_CACHE.get(pattern)
    if rx is None:
        rx = _GLOB_CACHE[pattern] = _translate(pattern)
    return bool(rx.match(path.replace("\\", "/")))


def pack_triggers(root) -> list:
    """Every built pack's declared triggers, read from the pack itself.

    Returns [{pack, path, paths, predicates, summary}]. The pack owns
    its triggers, so there is no second list to drift.
    """
    root = Path(root)
    out = []
    for pack_md in sorted((root / "packs").glob("*/PACK.md")):
        try:
            fm = _read_front_matter(pack_md.read_text(encoding="utf-8"))
        except OSError:
            continue
        paths = fm.get("activation_paths") or []
        if isinstance(paths, str):
            paths = [paths]
        preds = fm.get("applies_when") or []
        if isinstance(preds, str):
            preds = [preds]
        out.append({
            "pack": pack_md.parent.name,
            "path": pack_md.relative_to(root).as_posix(),
            "paths": list(paths),
            "predicates": list(preds),
            "summary": fm.get("summary", ""),
        })
    return out


def activated_packs(root, changed, *, declared_predicates=None) -> list:
    """Which packs a change activates, and what fired.

    Path triggers are deterministic and evaluated here. Predicates are
    the real gate under packs/PACK_SHAPE.md, but most of them are facts
    about the task rather than about the diff, so where the task record
    does not declare one it is returned unresolved for the agent to
    confirm. Narrowing twenty packs to a handful is the win; pretending
    to settle a predicate the diff cannot see would not be.
    """
    declared = set(declared_predicates or [])
    out = []
    for trigger in pack_triggers(root):
        hits = sorted({c for c in changed
                       for p in trigger["paths"] if _match(c, p)})
        by_predicate = sorted(set(trigger["predicates"]) & declared)
        if not hits and not by_predicate:
            continue
        unresolved = [p for p in trigger["predicates"] if p not in declared]
        out.append({
            "pack": trigger["pack"],
            "body": trigger["path"],
            "matched_paths": hits[:10],
            "matched_path_count": len(hits),
            "predicates_declared": by_predicate,
            "predicates_to_confirm": unresolved,
        })
    out.sort(key=lambda r: (-r["matched_path_count"], r["pack"]))
    return out


def _changed_files(root, base_ref):
    merge_base = _git(root, "merge-base", "HEAD", base_ref).strip() or base_ref
    out = _git(root, "diff", "--name-only", merge_base)
    return merge_base, [p.replace("\\", "/") for p in out.splitlines() if p.strip()]


def build_packet(root, base_ref=None, files=None, declared_predicates=None):
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
        "activated_packs": activated_packs(
            root, changed, declared_predicates=declared_predicates),
        "routed": {"tier": routed["tier"], "reasons": routed["reasons"]},
    }
