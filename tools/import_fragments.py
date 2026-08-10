"""Import pack research fragments into the canonical evidence ledger.

Integrator-only (ADR-0002 clarification 3): pack lanes write validated
fragments under their claimed pack path; only this step deduplicates and
imports them into registry/evidence.json, assigning final EV ids and
resolving shared sources across packs.

Usage: python tools/import_fragments.py [--dry-run]
"""

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LEDGER = REPO / "registry" / "evidence.json"


def norm_url(url):
    u = (url or "").strip().lower().rstrip("/")
    for prefix in ("https://", "http://", "www."):
        if u.startswith(prefix):
            u = u[len(prefix):]
    if u.startswith("www."):
        u = u[4:]
    return u


CITE = re.compile(r"EV-\d{4}")

# Areas whose files can cite evidence on their own account.
CITING_AREAS = ("packs", "registry", "kernel", "org", "inception")

# Derived files are excluded. Each one mirrors text it did not write,
# so counting it as a citer double-counts the original and, for the
# ledger itself, makes every record look cited because every record
# names its own id. INDEX.md quotes first paragraphs, which is how a
# dead record acquires a citation it never earned.
NOT_A_CITER = frozenset({
    "registry/evidence.json",
    "registry/CAPABILITIES.md",
    "INDEX.md",
    "packs/INDEX.md",
    "packs/GUIDE_INDEX.md",
})

# Task records name evidence ids as work to be done, not as an argument
# resting on them. Counting them would mean that writing "decide the
# twelve records nothing cites" makes those twelve cited, and the
# problem disappears the moment somebody files a ticket about it.
NOT_A_CITING_TREE = ("org/tasks/",)


def scan_citations(repo_root=None):
    """Map every EV id to the areas that genuinely cite it.

    One implementation, shared with check S016. Two scans that were
    meant to agree and quietly did not is the defect this whole field
    already suffered once.
    """
    root = Path(repo_root) if repo_root else REPO
    citations = {}
    for base in CITING_AREAS:
        area = root / base
        if not area.is_dir():
            continue
        for path in area.rglob("*"):
            if not path.is_file() or path.suffix not in (".md", ".json"):
                continue
            rel = path.relative_to(root).as_posix()
            if rel in NOT_A_CITER or rel.startswith(NOT_A_CITING_TREE):
                continue
            parts = path.relative_to(area).parts
            # A pack cites as itself; anything else cites as its area,
            # so a pack's argument reads differently from a registry
            # cross-reference.
            citer = parts[0] if base == "packs" and len(parts) > 1 else base
            text = path.read_text(encoding="utf-8", errors="replace")
            for ev in CITE.findall(text):
                citations.setdefault(ev, set()).add(citer)
    return citations


def recount(records):
    """Rewrite cited_by from the citations that actually exist.

    It used to mean "a pack fragment contributed this record", which is
    a different fact from "a pack cites this record" and was recorded
    under the citing name. Every record imported from estate-wide
    research therefore carried an empty list while being cited by id in
    pack prose: 107 of 448 read as uncited when none of them were.

    Derived from the tree, so the answer cannot drift from the packs.

    Derived files are excluded; see NOT_A_CITER for why.
    """
    citations = scan_citations()
    for rec in records:
        rec["cited_by"] = sorted(citations.get(rec["id"], ()))
    uncited = [r["id"] for r in records if not r["cited_by"]]
    if uncited:
        print("cited_by: %d record(s) cited by nothing: %s"
              % (len(uncited), ", ".join(uncited)))
    return citations


def main():
    dry = "--dry-run" in sys.argv
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    records = ledger["records"]
    by_url = {norm_url(r.get("url")): r for r in records}
    next_id = max(int(r["id"].split("-")[1]) for r in records) + 1

    added, merged, skipped = [], [], []
    for frag_path in sorted(REPO.glob("packs/*/research/sources.fragment.json")):
        pack = frag_path.parts[-3]
        frag = json.loads(frag_path.read_text(encoding="utf-8"))
        for rec in frag.get("records", []):
            key = norm_url(rec.get("url"))
            if not key:
                skipped.append((pack, rec.get("id"), "no url"))
                continue
            existing = by_url.get(key)
            if existing:
                cited = existing.setdefault("cited_by", [])
                if pack not in cited:
                    cited.append(pack)
                merged.append((pack, existing["id"]))
                continue
            new = dict(rec)
            new["id"] = f"EV-{next_id:04d}"
            next_id += 1
            cited = new.setdefault("cited_by", [])
            if pack not in cited:
                cited.append(pack)
            records.append(new)
            by_url[key] = new
            added.append((pack, new["id"], rec.get("source", "")[:40]))

    print(f"fragments: {len(added)} new records, {len(merged)} merged into "
          f"existing sources, {len(skipped)} skipped")
    if skipped:
        for s in skipped[:5]:
            print("  skipped:", s)
    recount(records)

    if dry:
        return 0
    ledger["records"] = records
    ledger["generated"] = "2026-08-03"
    # The cutoff was dropped on import and the ledger could not say how
    # old its own reading was. It is the latest access_date across the
    # records, which is a fact the records already carry rather than a
    # number typed in beside them.
    dates = sorted(d for d in (r.get("access_date") for r in records) if d)
    ledger["research_cutoff"] = dates[-1] if dates else None
    tmp = LEDGER.with_suffix(".tmp")
    tmp.write_text(json.dumps(ledger, indent=1) + "\n", encoding="utf-8")
    tmp.replace(LEDGER)
    print(f"ledger now holds {len(records)} records")
    return 0


if __name__ == "__main__":
    sys.exit(main())
