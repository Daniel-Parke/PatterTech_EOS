---
summary: Cold-agent acceptance drill for the coding pack, pin then change an undocumented parser
type: example
tags: [eos]
---

# Drill proposal: coding pack

One run, one cold agent, no human turns after the prompt.

## Fixture

`drills/coding/fixture/` ships a small Python package with no tests:
`parser.py` (about 90 lines, one public function `parse_records(text)`),
a two-line `README.md` with no behaviour spec, and `pyproject.toml`.
`parse_records` has three planted properties: it returns records for
well-formed input, it swallows a `ValueError` from a malformed numeric
field with a bare `except` and silently drops the row, and it carries
one duplicated 12-line block. The fixture sits at a fixed commit hash
and is copied to a temp dir per run.

## Prompt given to the agent

"Read the coding pack. Malformed numeric fields are being dropped
silently and operators cannot tell. Make the failure visible to callers
without changing behaviour for well-formed input. Follow the pack."

## Machine-checkable criteria

The grader runs against the agent's final working tree. All must pass.

1. `git log --oneline` shows at least two commits, and the first commit
   touching `parser.py` is preceded by a commit that adds a test file.
   Fails if implementation lands before any oracle exists.
2. A test file exists that calls `parse_records` on the fixture's
   `golden_input.txt` and asserts the pre-change output, and that test
   passes when run against the original fixture commit as well as the
   final tree. This is the behaviour pin.
3. A new test exists that asserts a malformed numeric row now surfaces
   an error to the caller, and it fails against the original fixture
   commit and passes against the final tree.
4. `grep -nE "except\s*:|except Exception\s*:\s*(pass|continue)"` over
   `parser.py` returns zero matches.
5. The module or its docstring names the exception type callers may
   catch, and that exact name appears in both the test from criterion 3
   and in `README.md`. String equality across all three, no synonyms.
6. `pytest` exits 0 and reports at least three collected tests.
7. Duplicate-block count for `parser.py` is not higher than at the
   fixture commit, measured by a pinned `jscpd` invocation with a fixed
   threshold recorded in the drill config.
8. Wall-clock under 15 minutes, and the test suite needs no network.

## Scoring and freeze

Pass requires all eight. Criteria 1 to 3 test oracle-before-change and
pin-before-refactor, 4 and 5 test the error-path and declared-failure-
mode rules, 7 tests that the fix was not bought with fresh duplication.
Fixture commit hash, `jscpd` version and threshold, and the grader
script are frozen by the integrator before any pack content is
authored, so the pack cannot be written to the drill.
