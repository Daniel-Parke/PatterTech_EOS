"""Import research into the canonical evidence ledger.

Integrator-only (ADR-0002 clarification 3): pack lanes write validated
fragments under their claimed pack path; only this step deduplicates and
imports them into registry/evidence.json, assigning final EV ids and
resolving shared sources across packs.

Two intakes, one ledger and one dedup rule:

- the fragment import, which sweeps packs/*/research/sources.fragment.json;
- study intake, which adds one row for a source the Study workflow read
  directly (a product, a repository, a game) rather than a document.
  Dedup is by URL and the lens is not part of the key, so two lenses on
  one source share one evidence row and become two rows in
  registry/lessons.json, each citing that id.

Usage:
  python tools/import_fragments.py [--dry-run]
  python tools/import_fragments.py study --source NAME --url URL ... [--dry-run]
"""

import argparse
import json
import re
import sys
from datetime import date
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

# The evidence ledger is JSON and names every one of its own IDs. Markdown
# views declare ``derived: true`` in front matter and are excluded generically
# by ``_is_derived_markdown`` below. Counting either kind as a citer would let
# copied text create evidence support it never earned.
NOT_A_CITER = frozenset({
    "registry/evidence.json",
})

# Task records name evidence ids as work to be done, not as an argument
# resting on them. Counting them would mean that writing "decide the
# twelve records nothing cites" makes those twelve cited, and the
# problem disappears the moment somebody files a ticket about it.
NOT_A_CITING_TREE = ("org/tasks/",)


def _is_derived_markdown(text):
    """Read only the opening front matter and recognise a derived view."""

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return False
    for line in lines[1:]:
        stripped = line.strip()
        if stripped == "---":
            return False
        if re.fullmatch(r"derived:\s*true", stripped, re.IGNORECASE):
            return True
    return False


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
            if path.suffix == ".md" and _is_derived_markdown(text):
                continue
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


def next_ev_id(records):
    """The next free EV id, one past the highest the ledger holds."""
    highest = 0
    for rec in records:
        m = re.match(r"^EV-(\d{4})$", str(rec.get("id", "")))
        if m:
            highest = max(highest, int(m.group(1)))
    return "EV-%04d" % (highest + 1)


def write_ledger(ledger, records, path=None, *, today=None):
    """Write the ledger back, stamping generated and research_cutoff.

    generated used to be the string "2026-08-03", written on every save
    whatever the date, so the ledger's own header aged backwards the
    moment anything was imported into it. It is the date of this write.

    The cutoff is the latest access_date across the records, which is a
    fact the records already carry rather than a number typed in beside
    them.
    """
    path = Path(path or LEDGER)
    ledger["records"] = records
    ledger["generated"] = (today or date.today()).isoformat()
    dates = sorted(d for d in (r.get("access_date") for r in records) if d)
    ledger["research_cutoff"] = dates[-1] if dates else None
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(ledger, indent=1) + "\n", encoding="utf-8",
                   newline="\n")
    tmp.replace(path)
    return path


def study_intake(records, record):
    """Add one evidence row for a studied source; return (row, created).

    Dedup is by normalised URL and by nothing else. The Study workflow
    runs one lens contract per study, and a second lens over the same
    source is a second lesson row citing the same evidence id, never a
    second copy of the source (ADR-0006 decision 2, plan section 10A
    step 8). So a URL already in the ledger returns its existing row and
    created is False.
    """
    key = norm_url(record.get("url"))
    if not key:
        raise ValueError("a study source needs a url: it is the dedup key")
    for existing in records:
        if norm_url(existing.get("url")) == key:
            return existing, False
    new = dict(record)
    new["id"] = next_ev_id(records)
    new.setdefault("cited_by", [])
    records.append(new)
    return new, True


# Fields the study intake fills in from the lens contract, and the ones
# it leaves null because a studied artefact has no such fact. Nothing
# here is guessed: every value arrives on the command line or is null.
_STUDY_NULL_FIELDS = ("study_design", "population", "model", "benchmark")


def cmd_study(args, ledger_path=None, *, today=None):
    ledger_path = Path(ledger_path or LEDGER)
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    records = ledger["records"]
    record = {
        "source": args.source,
        "url": args.url,
        "kind": args.kind,
        "publication_status": args.publication_status,
        "version_or_commit": args.version,
        "licence": args.licence,
        "access_date": args.access_date or (today or date.today()).isoformat(),
        "maintenance": args.maintenance,
        "finding": args.finding,
        "applicability_limits": args.limits,
        "counter_evidence": args.counter_evidence,
        "cited_by": [],
        "review": args.review or ("on-change-of:%s" % args.source),
    }
    for field in _STUDY_NULL_FIELDS:
        record[field] = None
    if args.licence_evidence:
        record["licence_evidence"] = args.licence_evidence
        record["licence_checked"] = (today or date.today()).isoformat()

    row, created = study_intake(records, record)
    if created:
        print("study intake: added %s for %s" % (row["id"], args.source))
    else:
        print("study intake: %s already holds %s; cite it from the lesson "
              "row for this lens" % (row["id"], args.url))
    if args.dry_run:
        return 0
    write_ledger(ledger, records, ledger_path, today=today)
    print("ledger now holds %d records" % len(records))
    return 0


def build_parser():
    ap = argparse.ArgumentParser(
        prog="python tools/import_fragments.py",
        description=__doc__.split("\n")[0])
    ap.add_argument("--dry-run", action="store_true",
                    help="report what would change and write nothing")
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser(
        "study",
        description="Add one evidence row for a source the Study workflow "
                    "read directly. Every value comes from the lens "
                    "contract; nothing is inferred. A URL already in the "
                    "ledger is reported and reused, never duplicated.")
    s.add_argument("--source", required=True, help="what the source is")
    s.add_argument("--url", required=True, help="the dedup key")
    s.add_argument("--version", required=True,
                   help="exact version, commit or dated revision studied")
    s.add_argument("--licence", required=True,
                   help="the governing licence, read off the source")
    s.add_argument("--finding", required=True,
                   help="the principle extracted, not a summary")
    s.add_argument("--limits", required=True,
                   help="where the finding does not carry")
    s.add_argument("--maintenance", required=True,
                   choices=["active", "stable", "stale", "url-dead"])
    s.add_argument("--kind", default="exemplar",
                   choices=["controlled", "standard", "maintainer", "exemplar"])
    s.add_argument("--publication-status", dest="publication_status",
                   default="artefact",
                   choices=["peer-reviewed", "preprint", "standard",
                            "repository", "vendor-doc", "blog", "artefact"])
    s.add_argument("--access-date", dest="access_date",
                   help="defaults to today")
    s.add_argument("--counter-evidence", dest="counter_evidence")
    s.add_argument("--licence-evidence", dest="licence_evidence",
                   help="what on the source establishes the licence, quoted")
    s.add_argument("--review", help="YYYY-MM or on-change-of:<source>")
    # SUPPRESS, not False: a subparser default overwrites the value the
    # top-level flag already set, so "--dry-run study ..." would write
    # the ledger it was told not to touch.
    s.add_argument("--dry-run", dest="dry_run", action="store_true",
                   default=argparse.SUPPRESS)
    s.set_defaults(fn=cmd_study)
    return ap


def main(argv=None):
    args = build_parser().parse_args(argv if argv is not None else sys.argv[1:])
    if getattr(args, "fn", None) is not None:
        return args.fn(args)
    return import_fragments(dry=args.dry_run)


def import_fragments(dry=False, ledger_path=None, *, today=None):
    ledger_path = Path(ledger_path or LEDGER)
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
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
    write_ledger(ledger, records, ledger_path, today=today)
    print(f"ledger now holds {len(records)} records")
    return 0


if __name__ == "__main__":
    sys.exit(main())
