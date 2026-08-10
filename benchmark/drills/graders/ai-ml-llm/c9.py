#!/usr/bin/env python3
"""Criterion 9: every model identifier in the source is pinned to a build date.

The dated-id rule frozen with this drill: an identifier has to end in a
build date, either eight digits or an ISO date, and the date has to be
a real one. `support-classifier-latest` is the alias the fixture ships
with, and the point of the criterion is that it is gone from the code
that calls out.

`stub_client.py` is exempt. It is the vendored client and its alias
table mirrors what the endpoint publishes; deleting the vendor's menu
is not what pinning means. What is graded is the string this repository
hands over when it makes a call.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, is_dated_id,  # noqa: E402
                     is_moving_alias, model_identifiers, scratch_dir)

CID = "c9"


def main():
    scratch = scratch_dir()
    found = model_identifiers(scratch)
    if not found:
        emit(CID, FAIL,
             "no model identifier anywhere in the source, so which model "
             "produced the results cannot be told from the tree")

    moving = [(w, v) for w, v in found if is_moving_alias(v)]
    undated = [(w, v) for w, v in found if not is_dated_id(v)]

    if moving:
        emit(CID, FAIL,
             "%d moving alias(es) still in the source: %s. An alias the "
             "vendor repoints means yesterday's numbers describe a model "
             "nobody is running today"
             % (len(moving),
                "; ".join("%s in %s" % (v, w) for w, v in moving[:3])))
    if undated:
        emit(CID, FAIL,
             "%d model identifier(s) carry no build date: %s"
             % (len(undated),
                "; ".join("%s in %s" % (v, w) for w, v in undated[:3])))

    emit(CID, PASS,
         "all %d model identifier(s) are dated: %s"
         % (len(found),
            "; ".join("%s in %s" % (v, w) for w, v in found[:3])))


if __name__ == "__main__":
    main()
