#!/usr/bin/env python3
"""Criterion 4: arithmetic between a GBP and a JPY amount raises.

A type with no `__add__` at all would raise a TypeError and look like a
pass, so the same-currency case is required to work first. Only then is
the mixed case evidence of anything.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import settle, require_implementation, scratch_dir  # noqa: E402

CID = "c4"

PROBE = '''
from booking.api import Money

try:
    same = Money(1099, "GBP") + Money(401, "GBP")
except Exception as exc:
    fail("adding two GBP amounts raises %s: %s. Money that cannot add is "
         "not evidence that mixing currencies is refused"
         % (type(exc).__name__, exc))

if getattr(same, "amount", None) != 1500 or getattr(same, "currency", None) != "GBP":
    fail("Money(1099, 'GBP') + Money(401, 'GBP') gives amount %r in %r, "
         "wanted 1500 in GBP"
         % (getattr(same, "amount", None), getattr(same, "currency", None)))

mixed = []
try:
    got = Money(1099, "GBP") + Money(1099, "JPY")
except Exception:
    pass
else:
    mixed.append("GBP + JPY returned %r instead of raising" % (got,))

try:
    got = Money(1099, "JPY") + Money(1099, "GBP")
except Exception:
    pass
else:
    mixed.append("JPY + GBP returned %r instead of raising" % (got,))

try:
    got = Money(1099, "GBP") - Money(1099, "JPY")
except Exception:
    pass
else:
    mixed.append("GBP - JPY returned %r instead of raising" % (got,))

if mixed:
    fail("; ".join(mixed))
ok("same currency arithmetic works and every mixed GBP/JPY operation raises")
'''


def main():
    scratch = scratch_dir()
    require_implementation(CID, scratch)
    settle(CID, scratch, PROBE)


if __name__ == "__main__":
    main()
