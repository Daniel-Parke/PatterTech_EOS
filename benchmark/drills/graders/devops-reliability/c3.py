#!/usr/bin/env python3
"""Criterion 3: ordinals continue the history, cleanly.

Strictly increasing, no duplicates, no gaps, measured against the
migrations the repository already had. Two readings of that are worth
stating because they decide verdicts:

- A tree that adds no migration is not vacuously clean. There is
  nothing to check against the pre-existing history, so the criterion
  is not met.
- A migration that has already been applied may not be renamed or
  removed. Renumbering history is how a deployed database and a
  migrations table stop agreeing.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, baseline_migration_names, emit,  # noqa: E402
                     migration_files, non_sql_migrations, ordinal_of,
                     scratch_dir)

CID = "c3"


def main():
    scratch = scratch_dir()
    files = migration_files(scratch)
    if not files:
        emit(CID, FAIL, "no migration files under migrations/")

    unnumbered = [p.name for p in files if ordinal_of(p) < 0]
    if unnumbered:
        emit(CID, FAIL,
             "no leading ordinal on %s, so the order they apply in is "
             "whatever the filesystem says" % ", ".join(unnumbered))

    shipped = baseline_migration_names(CID)
    names = {p.name for p in files}
    lost = sorted(shipped - names)
    if lost:
        emit(CID, FAIL,
             "%s was in the pre-existing history and is no longer there. "
             "Migrations that have already run are not renamed or removed"
             % ", ".join(lost))

    added = [p for p in files if p.name not in shipped]
    if not added:
        others = non_sql_migrations(scratch)
        extra = (" (%s are present but are not .sql)" % ", ".join(others)
                 if others else "")
        emit(CID, FAIL,
             "no migration beyond the pre-existing %d, so there is nothing "
             "to check against the history%s" % (len(shipped), extra))

    ordinals = [ordinal_of(p) for p in files]
    duplicates = sorted({o for o in ordinals if ordinals.count(o) > 1})
    if duplicates:
        clashing = [p.name for p in files if ordinal_of(p) in duplicates]
        emit(CID, FAIL,
             "ordinal %s is used more than once: %s"
             % (", ".join(str(d) for d in duplicates), ", ".join(clashing)))

    low, high = min(ordinals), max(ordinals)
    missing = sorted(set(range(low, high + 1)) - set(ordinals))
    if missing:
        emit(CID, FAIL,
             "gap in the sequence: %s missing between %04d and %04d"
             % (", ".join("%04d" % m for m in missing), low, high))

    shipped_high = max(ordinal_of(Path(n)) for n in shipped)
    below = [p.name for p in added if ordinal_of(p) <= shipped_high]
    if below:
        emit(CID, FAIL,
             "%s is new but numbered at or below %04d, which has already "
             "been applied" % (", ".join(below), shipped_high))

    emit(CID, PASS,
         "%d migrations numbered %04d to %04d with no duplicate and no gap; "
         "%d of them continue the pre-existing history"
         % (len(files), low, high, len(added)))


if __name__ == "__main__":
    main()
