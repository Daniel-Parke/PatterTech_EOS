#!/usr/bin/env python3
"""Criterion 6: the contract suite catches the drifted fake.

Run against the recorded real-client responses, the suite has to go red
for `FakeGateway` as it was committed. That is the only thing that
proves the suite detects drift rather than describing it.

Three guards make the red run mean something:

- The authoritative recording is written into `.drill/oracle/` and any
  copy of it in the delivered tree is overwritten with it, so a suite
  that passes because the recording was edited to match the fake is
  caught.
- The suite has to be green first, with the fake the agent delivered.
  A suite that is red either way proves nothing.
- Only the contract paths are run, so an unrelated red test elsewhere
  cannot stand in for the drift being detected.
"""

import fnmatch
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, FAKES_FILE, PASS, RECORDING_NAME,  # noqa: E402
                     copy_tree, emit, install_oracle, read, relative,
                     require_pytest, restore_pristine, run_pytest,
                     scratch_dir, tail)

CID = "c6"

PATTERNS = ("tests/contract/test_*gateway*.py", "tests/contract/test_*.py")
REAL_KEYS = {"id", "state", "amount"}


def contract_paths(scratch):
    for pattern in PATTERNS:
        hits = sorted(relative(scratch, p) for p in scratch.rglob("*.py")
                      if fnmatch.fnmatch(relative(scratch, p), pattern))
        if hits:
            return hits
    return []


def overwrite_recordings(copy, authoritative):
    """Put the real recording back wherever the tree keeps a copy of it."""
    replaced = []
    for path in Path(copy).rglob("*.json"):
        if ".drill" in path.parts or ".git" in path.parts:
            continue
        try:
            doc = json.loads(read(path))
        except ValueError:
            continue
        if isinstance(doc, dict) and REAL_KEYS <= set(doc):
            if read(path) != authoritative:
                replaced.append(relative(copy, path))
            path.write_text(authoritative, encoding="utf-8")
    return replaced


def main():
    scratch = scratch_dir()
    require_pytest(CID)

    paths = contract_paths(scratch)
    if not paths:
        emit(CID, FAIL,
             "no contract suite under tests/contract/, so there is nothing "
             "to run against the recording")

    work, copy = copy_tree(scratch, "drill-dt-c6-")
    try:
        written, why = install_oracle(copy, RECORDING_NAME)
        if written is None:
            emit(CID, FAIL, why)
        authoritative = read(written[0])
        edited = overwrite_recordings(copy, authoritative)

        green, output = run_pytest(copy, *paths)
        if green is None:
            emit(CID, FAIL, "could not run the contract suite: %s"
                            % tail(output))
        if green == 5:
            emit(CID, FAIL,
                 "the contract suite collected no tests: %s"
                 % ", ".join(paths))
        if green != 0:
            emit(CID, FAIL,
                 "the contract suite is already red as delivered (exit %d), "
                 "so a red run with the original fake would prove nothing: "
                 "%s" % (green, tail(output, 300)))

        if not restore_pristine(copy, FAKES_FILE):
            emit(CID, FAIL, "the drill's own %s is missing; the drifted fake "
                            "could not be put back" % FAKES_FILE)

        red, output = run_pytest(copy, *paths)
        if red is None:
            emit(CID, FAIL, "could not rerun the contract suite: %s"
                            % tail(output))
        if red == 0:
            emit(CID, FAIL,
                 "the contract suite still passes with %s as committed, so "
                 "it does not detect the drift it was written for"
                 % FAKES_FILE)
        emit(CID, PASS,
             "the contract suite is green as delivered and exits %d with the "
             "committed %s restored%s"
             % (red, FAKES_FILE,
                "; the tree's recording was overwritten with the "
                "authoritative one first (%s)" % ", ".join(edited)
                if edited else ""))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
