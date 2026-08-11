"""Read-only git facts via subprocess. Never writes, never mutates.

Every fact helper degrades to a harmless default (None, empty dict or
empty list) when git is unavailable, the directory is not a repository,
or the ref does not exist, so checks can carry on and report what they
could not verify rather than crashing.

output() is the one exception and is deliberate. The router and the
context packet both read a diff against a base ref the caller named,
and a ref that does not resolve must stop the command: degraded to an
empty result it reads as a diff with nothing in it, which routes a
clean R0 and reports a change surface of nothing changed.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

_TIMEOUT = 20


def _run(root, args):
    """One invocation, so the timeout is set once for both readings."""
    return subprocess.run(
        ["git", "-C", str(Path(root)), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=_TIMEOUT,
    )


def _git(root, *args: str) -> str | None:
    try:
        proc = _run(root, args)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout


def output(root, *args: str) -> str:
    """Run git and return stdout, raising RuntimeError when it fails.

    The strict counterpart to the degrading helpers, for the callers
    named in the module docstring.
    """
    proc = _run(root, args)
    if proc.returncode != 0:
        raise RuntimeError("git %s failed: %s"
                           % (" ".join(args), proc.stderr.strip()))
    return proc.stdout


def remote_tracking_heads(root) -> dict:
    """Locally known remote-tracking heads (refs/remotes), no network.

    The remote's symbolic HEAD is skipped. It is filtered on the full
    refname, because %(refname:short) renders refs/remotes/origin/HEAD
    as plain "origin", so a filter on the short name never matches it
    and the pointer lands in the dict as a remote with no branch.
    """
    out = _git(
        root, "for-each-ref", "refs/remotes",
        "--format=%(refname)%00%(refname:short)%00%(objectname)",
    )
    heads: dict = {}
    for line in (out or "").splitlines():
        parts = line.split("\x00")
        if len(parts) != 3:
            continue
        full, name, sha = parts
        if full.endswith("/HEAD"):
            continue
        heads[name] = sha
    return heads


def tags(root) -> dict:
    """Tag name -> commit sha (annotated tags peeled)."""
    out = _git(
        root, "for-each-ref", "refs/tags",
        "--format=%(refname:short)%00%(objectname)%00%(*objectname)",
    )
    result: dict = {}
    for line in (out or "").splitlines():
        parts = line.split("\x00")
        if len(parts) == 3:
            name, obj, peeled = parts
            result[name] = peeled or obj
    return result


def remote_heads(root, offline: bool) -> dict | None:
    """Remote branch heads via ls-remote; None when offline or unreachable."""
    if offline:
        return None
    out = _git(root, "ls-remote", "--heads", "origin")
    if out is None:
        return None
    heads: dict = {}
    for line in out.splitlines():
        bits = line.split("\t")
        if len(bits) == 2 and bits[1].startswith("refs/heads/"):
            heads[bits[1][len("refs/heads/"):]] = bits[0]
    return heads


def is_ancestor(root, a: str, b: str) -> bool:
    """True when commit a is an ancestor of commit b."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(Path(root)), "merge-base", "--is-ancestor", a, b],
            capture_output=True,
            timeout=_TIMEOUT,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return proc.returncode == 0


def rev_parse(root, ref: str) -> str | None:
    out = _git(root, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")
    return out.strip() if out else None


def object_exists(root, spec: str) -> bool:
    """True when the object spec (e.g. 'sha:path' or a sha) resolves."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(Path(root)), "cat-file", "-e", spec],
            capture_output=True,
            timeout=_TIMEOUT,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return proc.returncode == 0


def ls_tree(root, ref: str) -> list:
    """Every file path in the tree at ref; [] when the ref is unknown."""
    out = _git(root, "ls-tree", "-r", "--name-only", ref)
    return (out or "").splitlines()


def commit_count(root, range_spec: str) -> int | None:
    """Number of commits in a rev range (e.g. 'v1.0.0..HEAD'); None unknown."""
    out = _git(root, "rev-list", "--count", range_spec)
    if out is None:
        return None
    try:
        return int(out.strip())
    except ValueError:
        return None
