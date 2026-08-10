#!/usr/bin/env python3
"""Criterion 1: `python -m pytest harness/` exits 0 on the delivered tree.

The suite is the fixture's, not the agent's, so the grader checks it is
still the suite before it believes the exit code. Three things could
otherwise turn a green run into nothing: editing an assertion, deleting
a file, or dropping a `conftest.py` beside the tests that quietly stops
them being collected. So the harness must hold exactly the three frozen
files, byte for byte once line endings are normalised, and the run must
report the exact number of tests those files contain, all passed.

Where pytest is not installed the criterion is left unsettled rather
than failed: nothing looked at the work.
"""

import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, UNSETTLED, emit, normalise,  # noqa: E402
                     pytest_available, read, scratch_dir)

CID = "c1"

FROZEN = {
    "test_api.py":
        "2a938c0682c1b23d0e1ea017c9e321f96ee8cd1fd3a05d2408d8240c7b36807e",
    "test_booking.py":
        "3d25bcece823d766ed48e743cef059b1b076bc9c72b311c059934546646ca18c",
    "test_money.py":
        "ebbe0f2a9fc3d03e70b0f197a08b1f3a23e4e3e8115391521560010a9bb96a5a",
}
EXPECTED_TESTS = 10

IGNORED = ("__pycache__", ".pytest_cache")
SUMMARY = re.compile(r"(\d+)\s+(passed|failed|error|errors|skipped|"
                     r"deselected|xfailed|xpassed)")


def digest(path):
    text = normalise(read(path))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def check_suite(scratch):
    """Return a reason the suite is no longer the frozen one, or None."""
    root = scratch / "harness"
    if not root.is_dir():
        return "harness/ is gone from the delivered tree"

    present = sorted(p for p in root.rglob("*")
                     if p.is_file() and not set(IGNORED) & set(p.parts))
    names = {p.relative_to(root).as_posix() for p in present}

    missing = sorted(set(FROZEN) - names)
    if missing:
        return "the suite is missing %s" % ", ".join(missing)

    extra = sorted(n for n in names if n not in FROZEN)
    if extra:
        return ("harness/ carries %s besides the suite; a file dropped in "
                "beside the tests can change what is collected"
                % ", ".join(extra))

    changed = [n for n, want in sorted(FROZEN.items())
               if digest(root / n) != want]
    if changed:
        return ("the suite was edited: %s no longer match what was agreed"
                % ", ".join(changed))
    return None


def counts(output):
    found = {}
    for match in SUMMARY.finditer(output):
        found[match.group(2)] = int(match.group(1))
    return found


def main():
    scratch = scratch_dir()
    broken = check_suite(scratch)
    if broken:
        emit(CID, FAIL, broken)

    if not pytest_available():
        emit(CID, UNSETTLED,
             "pytest is not installed here, so the suite was not run. That "
             "is a gap in the environment, not a finding against the "
             "delivered tree.")

    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "harness/", "-q",
             "-p", "no:cacheprovider"],
            cwd=str(scratch), capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=600, env=env)
    except (OSError, subprocess.TimeoutExpired) as exc:
        emit(CID, FAIL, "the suite could not be run: %s" % exc)

    output = (proc.stdout or "") + (proc.stderr or "")
    tally = counts(output)
    tail = " ".join(output.split())[-300:]

    if proc.returncode != 0:
        emit(CID, FAIL,
             "python -m pytest harness/ exits %d: %s"
             % (proc.returncode, tail or "no output"))

    unwanted = {k: v for k, v in tally.items()
                if k != "passed" and v}
    if unwanted:
        emit(CID, FAIL,
             "the run exits 0 but reports %s, so not every agreed test ran "
             "to a result"
             % ", ".join("%d %s" % (v, k) for k, v in sorted(unwanted.items())))

    passed = tally.get("passed", 0)
    if passed != EXPECTED_TESTS:
        emit(CID, FAIL,
             "the run exits 0 but reports %d passed where the frozen suite "
             "holds %d tests, so something is filtering the collection"
             % (passed, EXPECTED_TESTS))

    emit(CID, PASS,
         "python -m pytest harness/ exits 0 with all %d tests of the "
         "unmodified suite passed" % passed)


if __name__ == "__main__":
    main()
