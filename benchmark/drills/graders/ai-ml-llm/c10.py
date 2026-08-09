#!/usr/bin/env python3
"""Criterion 10: the eval finishes inside the budget with the network shut off.

Networking is disabled in-process rather than by an OS sandbox: the run
gets a `sitecustomize` that makes connecting, resolving a name or
wrapping a socket in TLS raise. That covers every outbound path the
standard library and the usual HTTP clients take, and it is the
strongest enforcement available to a stdlib-only grader that has to run
on any machine. A run that reaches for the network fails here with the
marker in its traceback, which is the finding the criterion is after.

The spec allows twenty minutes. The runner kills a grader at ten, so
the cap enforced here is four, and the reason says so rather than
quoting a limit that was not applied.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, NETWORK_MARKER, PASS, RUN_TIMEOUT_S,  # noqa: E402
                     UNSETTLED, emit, evaluate, run_entry, scratch_dir)

CID = "c10"


def main():
    scratch = scratch_dir()
    # The entry point is chosen with the network up, then that same file
    # is run again with it down. Choosing under the block would let a
    # tree whose eval calls out pass by falling through to some other
    # script that happens to exit 0.
    chosen, _ = evaluate(scratch)
    if chosen is None:
        emit(CID, FAIL,
             "no eval entry point in the tree, so there is nothing to time "
             "and nothing to watch for outbound calls")
    run = run_entry(scratch, chosen.entry, block_network=True)
    if run.missing_module:
        emit(CID, UNSETTLED,
             "%s needs %r, which is not installed here, so the offline run "
             "could not be made. That is a gap in this environment, not a "
             "finding against the delivered tree."
             % (run.rel, run.missing_module))
    if run.rc is None:
        emit(CID, FAIL,
             "%s did not finish inside %ds with the network disabled"
             % (run.rel, RUN_TIMEOUT_S))
    if run.rc != 0:
        if NETWORK_MARKER in (run.stderr or ""):
            emit(CID, FAIL,
                 "%s tries to call out: it exits %d once connecting, name "
                 "resolution and TLS are blocked, so the eval is not "
                 "reproducible offline" % (run.rel, run.rc))
        last = (run.stderr or "").strip().splitlines()
        emit(CID, FAIL,
             "%s exits %d with the network disabled: %s"
             % (run.rel, run.rc, last[-1][:200] if last else "no stderr"))

    emit(CID, PASS,
         "%s exits 0 in %.1fs with connecting, DNS and TLS blocked, well "
         "inside the twenty minutes the spec allows"
         % (run.rel, run.seconds))


if __name__ == "__main__":
    main()
