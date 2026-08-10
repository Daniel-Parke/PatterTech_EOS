#!/usr/bin/env python3
"""Criterion 5: every number in the record is traceable.

Pull every integer and decimal out of `discovery.md`. A value passes if
it appears somewhere in the frozen fixture, or if it is the number of
exported tickets matching a filter the record states. Anything else is a
figure with no base, which is the failure this criterion exists for.

What counts as a stated filter, exactly:

- one column of the ticket export equal to one value, for any column and
  value in it, and the total row count. Conjunctions of two filters are
  not offered. Pairs of filters over this export reach most small
  integers, and an allowed set holding most small integers is not a
  check.
- a term the record quotes, matched as a substring against the whole
  exported row. The pack says the filter is part of the claim, so a
  record that quotes its search term gets counted against the export;
  one that does not, does not.

Three limits, stated rather than hidden.

Dates, times and bare years are blanked before extraction. Without that,
every day of the month in the ticket export enters the allowed set and
any integer up to thirty-one passes untraced. The cost is that a
fabricated four-digit figure in the year range would pass.

A derived percentage fails. "14 of 120, which is 12 per cent" is
traceable to a reader and not to this grader, because admitting one
count divided by another would open the allowed set wide enough to
launder most invented figures. The frozen criterion says a value is a
source figure or a count, with no third category, and this follows it.

Small integers that happen to appear in the fixture's own source code
are allowed, because the criterion says the fixture and does not carve
out its Python. That is a real hole and it is narrow: it admits the
handful of literals in `app/` and `tests/`.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, RECORD, SUPPORT, canon, clip,  # noqa: E402
                     emit, filter_counts, fixture_literals, keyword_counts,
                     numbers_with_context, quoted_terms, record_text,
                     scratch_dir)

CID = "c5"

REPORT = 5


def main():
    scratch = scratch_dir()
    text = record_text(CID, scratch)

    found = numbers_with_context(text)
    if not found:
        emit(CID, PASS,
             "%s carries no integer or decimal at all, so nothing is "
             "untraceable; note that a record with no numbers has also not "
             "counted anything" % RECORD)

    literals = fixture_literals(CID)
    counts = filter_counts(CID)
    allowed = literals | counts

    unexplained = [(v, ctx) for v, ctx in found if v not in allowed]
    if unexplained:
        terms = quoted_terms(text)
        by_term = keyword_counts(CID, terms)
        from_terms = {canon(v) for v in by_term.values()}
        unexplained = [(v, ctx) for v, ctx in unexplained
                       if v not in from_terms]

    if unexplained:
        seen = []
        for value, ctx in unexplained:
            if value not in [v for v, _ in seen]:
                seen.append((value, ctx))
        emit(CID, FAIL,
             "%d untraceable figure(s) in %s: %s. Each is absent from every "
             "fixture file and is not the count of any single filter over "
             "%s, nor of any term the record quotes."
             % (len(unexplained), RECORD,
                "; ".join("%s in %r" % (v, clip(c, 90))
                          for v, c in seen[:REPORT]), SUPPORT))

    distinct = sorted({v for v, _ in found}, key=lambda s: float(s))
    emit(CID, PASS,
         "all %d figure(s) in %s trace to the fixture or to a stated "
         "filter: %s" % (len(distinct), RECORD, ", ".join(distinct)))


if __name__ == "__main__":
    main()
