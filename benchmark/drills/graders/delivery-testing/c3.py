#!/usr/bin/env python3
"""Criterion 3: a new test that fails against the original pricing.py.

The check the spec names is: put the shipped pricing module back, rerun
the agent's own tests, and require a non-zero exit. Done once that is
not safe here, because the scenario also ships a test that goes red
about one run in four for reasons that have nothing to do with pricing,
and a lucky flake would be read as a regression test that does not
exist.

So the tree is run four times as delivered and four times with
`pricing.py` reverted, and the criterion asks for a node id that fails
in every reverted run and in none of the delivered ones. A flake would
have to land four times running and miss four times running to fool
that, which is about one attempt in eight hundred. It also makes the
verdict say which test caught the defect, rather than only that
something did.
"""

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, copy_tree, emit, failing_nodes,  # noqa: E402
                     require_pytest, restore_pristine, run_pytest,
                     scratch_dir, tail)

CID = "c3"
RUNS = 4


def collect(copy, runs):
    """(list of exit codes, per-run sets of failing node ids)."""
    codes, nodes = [], []
    for _ in range(runs):
        code, output = run_pytest(copy)
        if code is None:
            emit(CID, FAIL, "could not run pytest: %s" % tail(output))
        codes.append(code)
        nodes.append(failing_nodes(output))
    return codes, nodes


def main():
    scratch = scratch_dir()
    require_pytest(CID)

    work, copy = copy_tree(scratch, "drill-dt-c3-")
    try:
        after_codes, after_nodes = collect(copy, RUNS)
        if 5 in after_codes:
            emit(CID, FAIL, "pytest collected no tests in the delivered tree")
        flaky_or_red = set().union(*after_nodes)

        if not restore_pristine(copy, "pricing.py"):
            emit(CID, FAIL, "the drill's own pricing.py is missing; the "
                            "revert could not be performed")

        before_codes, before_nodes = collect(copy, RUNS)
        always_red = set.intersection(*before_nodes) if before_nodes else set()
        caught = sorted(always_red - flaky_or_red)

        if all(c == 0 for c in before_codes):
            emit(CID, FAIL,
                 "the agent's tests still exit 0 with the original "
                 "pricing.py restored, over %d runs, so nothing in the suite "
                 "would have caught the defect" % RUNS)
        if not caught:
            emit(CID, FAIL,
                 "reverting pricing.py gives exit codes %s, but no test "
                 "fails on every reverted run while passing on every "
                 "delivered one, so nothing here reliably pins the defect. "
                 "Failures seen: %s"
                 % (before_codes,
                    ", ".join(sorted(set().union(*before_nodes))[:5]) or
                    "none"))
        emit(CID, PASS,
             "%d test(s) fail on all %d runs with the original pricing.py "
             "and pass on all %d runs without it: %s"
             % (len(caught), RUNS, RUNS, ", ".join(caught[:5])))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
