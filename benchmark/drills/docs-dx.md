---
summary: Cold-agent acceptance drill for the docs-dx pack, make a stale documented flag fail the build
type: example
tags: [eos, testing]
---

# Drill proposal: docs-dx pack

One run, one cold agent, no human turns after the prompt.

## Fixture

`drills/docs-dx/fixture/` ships a small Python CLI at a fixed commit,
copied to a temp dir per run: `cli.py` exposing `--out-dir`, plus
`README.md`, `docs/quickstart.md`, `docs/reference.md` and a
`CHANGELOG.md` with an `Unreleased` section. No CI configuration. Three
planted defects: `docs/quickstart.md` has a fenced `bash` block calling
the removed flag `--outdir` and nothing runs it; `README.md` links to
`docs/setup.md`, renamed to `docs/quickstart.md`, and
`docs/reference.md` links to `docs/quickstart.md#install-it` where the
heading is now `## Installing`; `cli.py` rejects an unknown flag with
`print("error")` and exit 1.

## Prompt given to the agent

"Read the docs-dx pack. A user followed the quickstart and it did not
work, and they could not tell why. Fix the documentation and make this
class of failure impossible to reintroduce silently. Follow the pack."

## Machine-checkable criteria

Grader runs against the final tree. All must pass.

1. A CI configuration exists and invokes a pinned link checker with
   fragment checking over the repository.
2. That pinned invocation exits 0 on the final tree and exits 2 against
   the original fixture commit. Both broken links fixed, checker
   configured to catch anchors.
3. CI executes fenced shell blocks under `docs/` or asserts each
   carries an explicit skip marker. The grader injects a block calling
   the CLI with `--bogus`; that step must then exit non-zero. Drift
   oracle.
4. `grep -r -- "--outdir" docs README.md` returns no matches, and
   `--out-dir` appears in `docs/quickstart.md`.
5. `python cli.py --outdir /tmp/x` exits non-zero and its combined
   output contains the literal string `--out-dir` and is at least 20
   characters long.
6. `CHANGELOG.md` still has a heading matching `^## \[?Unreleased` with
   a line containing `--out-dir` beneath it.
7. Injecting a link to `https://example.invalid/` does not fail any CI
   step. External link checking must be absent or non-blocking.
8. `git log --oneline` shows at least one commit, nothing under
   `drills/` is modified, wall-clock under 15 minutes, and criteria 2
   and 3 run with no network access.

## Scoring and freeze

Pass requires all eight. Criteria 1 to 3 test that the fix was made
structural rather than textual, 4 and 5 the error-message rule, 6
changelog practice, 7 that the agent knew which checks must not block.
Fixture hash, pinned checker version and invocation, injected blocks
and the grader script are frozen by the integrator before any pack
content is authored, so the pack cannot be written to the drill.
