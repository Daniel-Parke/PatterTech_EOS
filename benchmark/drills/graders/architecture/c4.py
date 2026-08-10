#!/usr/bin/env python3
"""Criterion 4: the contract bites, and stops biting when reverted.

This is the criterion that separates a contract file from a boundary.
A config that parses, names the right direction and exits 0 can still
be enforcing nothing, because a rule aimed at a module outside the
graph reports clean. So the grader breaks the rule on purpose and
requires the run to go red, then puts it back and requires green.

The work happens on a copy, so a grader that dies midway cannot leave
the delivered tree holding an injected import.
"""

import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, catalogue_modules, emit,  # noqa: E402
                     require_lint, run_lint, scratch_dir)

CID = "c4"
INJECTED = "\nimport billing  # drill c4: injected boundary violation\n"


def main():
    scratch = scratch_dir()
    require_lint(CID)

    targets = catalogue_modules(scratch)
    if not targets:
        emit(CID, FAIL, "no catalogue module to inject into")

    work = Path(tempfile.mkdtemp(prefix="drill-arch-c4-"))
    try:
        copy = work / "tree"
        shutil.copytree(scratch, copy)

        before, out = run_lint(copy)
        if before is None:
            emit(CID, FAIL,
                 "could not run lint-imports: %s" % out.strip()[:300])
        if before != 0:
            emit(CID, FAIL,
                 "the tree is already failing before injection (exit %d), so "
                 "a red run after it would prove nothing" % before)

        victim = copy / targets[0].relative_to(scratch)
        original = victim.read_text(encoding="utf-8", errors="replace")
        victim.write_text(original + INJECTED, encoding="utf-8")

        during, out = run_lint(copy)
        if during == 0:
            emit(CID, FAIL,
                 "lint-imports still exits 0 after `import billing` was added "
                 "to %s, so the contract is not enforcing the boundary"
                 % victim.name)

        victim.write_text(original, encoding="utf-8")
        after, out = run_lint(copy)
        if after != 0:
            emit(CID, FAIL,
                 "lint-imports exits %d after the injection was reverted, so "
                 "the red run cannot be attributed to the injected import"
                 % after)

        emit(CID, PASS,
             "clean, then exit %d with `import billing` in %s, then clean "
             "again" % (during, victim.name))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
