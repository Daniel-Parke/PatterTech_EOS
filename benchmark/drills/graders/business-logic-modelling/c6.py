#!/usr/bin/env python3
"""Criterion 6: every ordered pair of statuses, and only five succeed.

held to confirmed, held to cancelled, held to expired, confirmed to
cancelled, confirmed to completed. Everything else raises, including a
status moving to itself.

Two things are checked on each refusal, not one. The call must raise,
and the booking must still be in the status it started in, because a
transition that returns quietly having changed nothing is the silent
no-op the drill names.

Each pair starts from a booking built fresh and walked into place
through legal moves only, so an implementation that mutates in place
and one that returns a new booking are both driven correctly. Any
status the model has invented beyond the five is driven as a
destination too: it cannot be reached legally, so every move into it
must raise.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (BOOKING_SETUP, require_implementation,  # noqa: E402
                     scratch_dir, settle)

CID = "c6"

PROBE = BOOKING_SETUP + '''
REQUIRED = ("HELD", "CONFIRMED", "CANCELLED", "COMPLETED", "EXPIRED")
ALLOWED = {
    ("HELD", "CONFIRMED"),
    ("HELD", "CANCELLED"),
    ("HELD", "EXPIRED"),
    ("CONFIRMED", "CANCELLED"),
    ("CONFIRMED", "COMPLETED"),
}
ROUTE = {
    "HELD": (),
    "CONFIRMED": ("CONFIRMED",),
    "CANCELLED": ("CANCELLED",),
    "EXPIRED": ("EXPIRED",),
    "COMPLETED": ("CONFIRMED", "COMPLETED"),
}

absent = [name for name in REQUIRED if not hasattr(Status, name)]
if absent:
    fail("Status has no %s, so the transition table cannot be driven"
         % ", ".join(absent))

names = list(REQUIRED)
try:
    for member in Status:
        if getattr(member, "name", None) not in names:
            names.append(member.name)
except TypeError:
    pass


def status_name(thing):
    return getattr(getattr(thing, "status", None), "name", None)


def landed(returned, original):
    """Where the booking ended up, whether the API returns or mutates."""
    if status_name(returned) is not None:
        return status_name(returned)
    return status_name(original)


def reach(name):
    stay = a_hold()
    for step in ROUTE.get(name, ()):
        moved = stay.transition_to(getattr(Status, step))
        if status_name(moved) is not None:
            stay = moved
    return stay


for name in REQUIRED:
    try:
        stay = reach(name)
    except Exception as exc:
        fail("no booking can be put into %s by legal moves alone: %s: %s"
             % (name, type(exc).__name__, exc))
    if status_name(stay) != name:
        fail("walking a booking into %s left it in %r, so the table cannot "
             "be driven from a known starting point"
             % (name, status_name(stay)))

wrong = []
pairs = 0
for source in names:
    if source not in ROUTE:
        continue
    for destination in names:
        pairs += 1
        stay = reach(source)
        legal = (source, destination) in ALLOWED
        try:
            moved = stay.transition_to(getattr(Status, destination))
        except Exception as exc:
            if legal:
                wrong.append("%s to %s should be allowed but raised %s"
                             % (source, destination, type(exc).__name__))
            continue
        where = landed(moved, stay)
        if legal:
            if where != destination:
                wrong.append("%s to %s did not raise but left the booking "
                             "in %r" % (source, destination, where))
        elif where == source:
            wrong.append("%s to %s did not raise and changed nothing: a "
                         "silent no-op" % (source, destination))
        else:
            wrong.append("%s to %s did not raise and moved the booking to %r"
                         % (source, destination, where))

if wrong:
    fail("%d of %d ordered pairs are wrong: %s"
         % (len(wrong), pairs, "; ".join(wrong[:6])))
ok("all %d ordered pairs behave: the five legal moves succeed and the "
   "other %d raise without changing the booking" % (pairs, pairs - 5))
'''


def main():
    scratch = scratch_dir()
    require_implementation(CID, scratch)
    settle(CID, scratch, PROBE)


if __name__ == "__main__":
    main()
