"""Freshness checks F001-F004.

The F-series watches decay: review dates that lapsed, evidence rows
past their look-again month, bulk-set review dates nobody will honour,
and content types the v1 contract never asked to carry a review date
at all.

Severity: staleness is a warning (the work list), a malformed or
illegal review value is an error (the contract). F001 overlaps E006 on
the v1 review_by field by design, exactly as S004 overlaps E005: the
E-series retires in P4 and the F-series is its successor surface.

Exemptions match the semantic series and for the same reasons:
benchmark/** is the frozen suite, archive/** is verbatim v1 history
and org/logs/** is the append-only session log. History is kept as it
was written, so a stale date inside it is a fact about the past rather
than a job for anyone; editing it to satisfy a checker would destroy
the record. template: true files are out of scope as syntax
documentation, and derived files carry their sources' dates and are
skipped where noted.
"""

from __future__ import annotations

import json
import re
from datetime import date

from ..findings import Finding
from ..repo import RepoModel
from . import register

MONTH_RE = re.compile(r"^(\d{4})-(\d{2})$")
ON_CHANGE_RE = re.compile(r"^on-change-of:\S+$")

BULK_THRESHOLD = 10

# v1 required review_by only on wargame, stack, registry and guide.
# These content-bearing types were exempt and now warrant coverage.
PREVIOUSLY_EXEMPT = {"doctrine", "foundation", "pattern", "ux", "implementation", "playbook"}


EXEMPT_PREFIXES = ("benchmark/", "archive/", "org/logs/")


def _in_scope(rec) -> bool:
    if rec.path.startswith(EXEMPT_PREFIXES):
        return False
    if not rec.fm.present:
        return False
    if rec.fm.data.get("template"):
        return False
    return True


def _month_passed(value: str, today: date) -> bool | None:
    """True past, False not past, None malformed."""
    m = MONTH_RE.match(value.strip())
    if not m:
        return None
    y, mo = int(m.group(1)), int(m.group(2))
    if not 1 <= mo <= 12:
        return None
    return (y, mo) < (today.year, today.month)


# --- F001 review_by / review expiry ------------------------------------


@register("F001")
def check_f001_review_expiry(ctx: dict) -> list:
    model: RepoModel = ctx["model"]
    today = ctx["today"]
    out = []
    for rec in model.files:
        if not _in_scope(rec):
            continue
        fm = rec.fm.data
        rb = fm.get("review_by")
        if isinstance(rb, str) and rb:
            passed = _month_passed(rb, today)
            if passed is None:
                out.append(Finding("F001", "error", rec.path,
                                   f"review_by not YYYY-MM: {rb}"))
            elif passed:
                out.append(Finding("F001", "warn", rec.path,
                                   f"review_by {rb} has passed, verify before relying"))
        review = fm.get("review")
        if isinstance(review, str) and review:
            value = review.strip()
            if value == "none":
                kind = fm.get("kind")
                lifecycle = fm.get("lifecycle")
                if kind != "record" and lifecycle != "archived":
                    out.append(Finding("F001", "error", rec.path,
                                       "review: none is legal only for records and archived items"))
            elif ON_CHANGE_RE.match(value):
                pass
            else:
                passed = _month_passed(value, today)
                if passed is None:
                    out.append(Finding("F001", "error", rec.path,
                                       f"review must be YYYY-MM, on-change-of:<source> or none: {value}"))
                elif passed:
                    out.append(Finding("F001", "warn", rec.path,
                                       f"review {value} has passed, verify before relying"))
    return out


# --- F002 evidence ledger review dates ---------------------------------


@register("F002")
def check_f002_evidence_review(ctx: dict) -> list:
    model: RepoModel = ctx["model"]
    today = ctx["today"]
    path = "registry/evidence.json"
    text = model.read(path)
    if text is None:
        return []
    try:
        doc = json.loads(text)
    except ValueError:
        return [Finding("F002", "error", path, "malformed JSON")]
    out = []
    records = doc.get("records") if isinstance(doc, dict) else None
    for row in records if isinstance(records, list) else []:
        if not isinstance(row, dict):
            continue
        rid = row.get("id", "?")
        review = str(row.get("review", ""))
        # METADATA_SPEC allows three review policies: a YYYY-MM date, an
        # event trigger (on-change-of: <source>), or none for records and
        # archives. Event-triggered rows fire on their source changing, so
        # there is no date for expiry to compare against.
        stripped = review.strip().lower()
        if stripped.startswith("on-change-of") or stripped == "none":
            continue
        passed = _month_passed(review, today)
        if passed is None:
            out.append(Finding("F002", "error", path,
                               f"{rid}: review must be YYYY-MM, "
                               f"on-change-of:<source> or none: {review}"))
        elif passed:
            out.append(Finding("F002", "warn", path,
                               f"{rid}: review {review} has passed"))
    return out


# --- F003 bulk-identical review dates ----------------------------------


@register("F003")
def check_f003_bulk_review_dates(ctx: dict) -> list:
    """More than BULK_THRESHOLD files sharing one review date is a smell:
    the date was bulk-set, so no one scheduled the actual re-reads.

    A file counts once. Most v2 files carry the same month in both
    review and review_by, the v2 axis and its v1 compatibility twin,
    and counting both doubled every group: one file is one re-read, not
    two.
    """
    model: RepoModel = ctx["model"]
    groups: dict = {}
    for rec in model.files:
        if not _in_scope(rec):
            continue
        for key in ("review_by", "review"):
            value = rec.fm.data.get(key)
            if isinstance(value, str) and MONTH_RE.match(value.strip()):
                groups.setdefault(value.strip(), set()).add(rec.path)
    out = []
    for value in sorted(groups):
        paths = sorted(groups[value])
        if len(paths) > BULK_THRESHOLD:
            out.append(Finding("F003", "warn", paths[0],
                               f"review date {value} shared by {len(paths)} files, bulk-set smell"))
    return out


# --- F004 review coverage for previously exempt types ------------------


@register("F004")
def check_f004_exempt_coverage(ctx: dict) -> list:
    model: RepoModel = ctx["model"]
    out = []
    for rec in model.files:
        if not _in_scope(rec):
            continue
        fm = rec.fm.data
        if fm.get("derived"):
            continue
        if fm.get("type") not in PREVIOUSLY_EXEMPT:
            continue
        if fm.get("review_by") or fm.get("review"):
            continue
        out.append(Finding("F004", "warn", rec.path,
                           f"type {fm['type']} carries no review_by or review date"))
    return out
