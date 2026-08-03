"""Import pack research fragments into the canonical evidence ledger.

Integrator-only (ADR-0002 clarification 3): pack lanes write validated
fragments under their claimed pack path; only this step deduplicates and
imports them into registry/evidence.json, assigning final EV ids and
resolving shared sources across packs.

Usage: python tools/import_fragments.py [--dry-run]
"""

import json
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
    if dry:
        return 0
    ledger["records"] = records
    ledger["generated"] = "2026-08-03"
    tmp = LEDGER.with_suffix(".tmp")
    tmp.write_text(json.dumps(ledger, indent=1) + "\n", encoding="utf-8")
    tmp.replace(LEDGER)
    print(f"ledger now holds {len(records)} records")
    return 0


if __name__ == "__main__":
    sys.exit(main())
