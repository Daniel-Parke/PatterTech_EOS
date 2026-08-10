"""B001: the frozen benchmark still matches its manifest.

benchmark/FREEZE_MANIFEST.json says "Changes after freeze require an
ADR-0002 amendment". Nothing verified it. When the pre-release review
finally hashed the 164 entries it found the manifest failing its own
check on fifteen, holding thirty-four Windows-path duplicates of paths
it already had, recording two conflicting hashes for fourteen files,
and one file matching neither of its two recorded hashes.

A freeze nobody checks is not a freeze. This makes it a check.
"""

from __future__ import annotations

import json

from ..findings import Finding
from ..repo import RepoModel, content_sha256
from . import register

MANIFEST = "benchmark/FREEZE_MANIFEST.json"


def verify(model: RepoModel) -> list:
    """Return findings against the frozen set. Empty means intact."""
    raw = model.read(MANIFEST)
    if raw is None:
        return []
    try:
        doc = json.loads(raw)
    except ValueError as exc:
        return [Finding("B001", "error", MANIFEST, f"not valid JSON: {exc}")]

    files = doc.get("files") or {}
    out = []

    # A manifest keyed by two spellings of one path cannot verify
    # anything: for fourteen files it recorded two different hashes.
    seen: dict = {}
    for key in files:
        norm = key.replace("\\", "/")
        if norm in seen and seen[norm] != key:
            out.append(Finding(
                "B001", "error", MANIFEST,
                f"duplicate entry for {norm}: recorded as {seen[norm]!r} and "
                f"{key!r}, so the manifest holds two hashes for one file"))
        seen.setdefault(norm, key)

    amended = set()
    for entry in doc.get("amendments") or []:
        for f in entry.get("files") or []:
            amended.add(f.replace("\\", "/"))

    for key, want in files.items():
        rel = key.replace("\\", "/")
        path = model.root / rel
        if not path.is_file():
            out.append(Finding("B001", "error", MANIFEST,
                               f"frozen file is missing: {rel}"))
            continue
        got = content_sha256(path)
        if got == want:
            continue
        note = (" It is listed in an amendment, so re-hash the manifest."
                if rel in amended else
                " It is in no amendment: this is an unrecorded change to "
                "frozen benchmark material.")
        out.append(Finding("B001", "error", MANIFEST,
                           f"{rel} does not match its recorded hash "
                           f"({want[:12]} recorded, {got[:12]} found).{note}"))
    return out


@register("B001")
def check_b001_freeze(ctx: dict) -> list:
    return verify(ctx["model"])
