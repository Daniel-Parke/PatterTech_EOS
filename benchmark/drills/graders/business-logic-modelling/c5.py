#!/usr/bin/env python3
"""Criterion 5: a stay that spans no night cannot be constructed.

The point is where the invariant sits. A type that builds happily and
offers `validate()` or `is_valid()` has moved the rule to a place a
caller can forget, so it fails here even though the rule is written
down somewhere. The reason says so when one of those methods is found,
because that is the specific mistake the drill is looking for.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (BOOKING_SETUP, require_implementation,  # noqa: E402
                     scratch_dir, settle)

CID = "c5"

PROBE = BOOKING_SETUP + '''
try:
    a_hold()
except Exception as exc:
    fail("a three night stay cannot be constructed at all: %s: %s"
         % (type(exc).__name__, exc))

built = []
cases = (
    ("on the check-in date", {"check_out": CHECK_IN}),
    ("a day before the check-in date",
     {"check_out": CHECK_IN - dt.timedelta(days=1)}),
)
for label, changes in cases:
    try:
        stay = a_hold(**changes)
    except Exception:
        continue
    built.append((label, stay))

if built:
    deferred = sorted({name for _, stay in built
                       for name in ("validate", "is_valid")
                       if hasattr(stay, name)})
    extra = ""
    if deferred:
        extra = (" The booking carries %s, so the rule exists but sits "
                 "where a caller has to remember it."
                 % " and ".join("%s()" % n for n in deferred))
    fail("a booking with check-out %s was constructed without raising.%s"
         % (" and one ".join(label for label, _ in built), extra))

ok("check-out on or before check-in raises at construction, and an "
   "ordinary three night stay still builds")
'''


def main():
    scratch = scratch_dir()
    require_implementation(CID, scratch)
    settle(CID, scratch, PROBE)


if __name__ == "__main__":
    main()
