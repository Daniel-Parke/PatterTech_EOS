---
summary: What a pack acceptance drill is, how the runner grades one, and what is still missing before most of them can return a verdict
type: example
tags: [eos, testing]
---

# Pack acceptance drills

A drill is one cold-agent scenario with deterministic criteria. The
spec is frozen with its sha256 in `MANIFEST.json` and never changes
without an ADR amendment. A failed drill routes to fixing the pack and
re-running; it never routes to editing the spec.

Run them with `python -m tools.eos drills`. The contract is the drills
section of `tools/CLI_CONTRACTS.md`.

## What is frozen, and how strongly

Twenty-two specs. Read `frozen_before_authoring` on every entry in
`MANIFEST.json` before you read a result:

- The **Wave A eight** were frozen before any of their pack content was
  authored. Their spec could not have been written to the pack, so they
  are independent oracles.
- The **Wave B twelve** were frozen on 2026-08-03, after their packs
  were authored and in the same commit as them. That is a weaker
  guarantee: the spec could have been written to suit the pack. A pass
  on a Wave B drill is worth less than a pass on a Wave A drill, and the
  manifest says so on each entry rather than leaving a reader to guess.
- The **Wave C two** were written at the 2026-08-08 pre-release review
  to cover gaps the first twenty left: a greenfield brief the house
  style is wrong for, which is the only condition the pluralism
  contract is testable under, and positioning, which the marketing
  drill never touched. Both were written after their packs, so they
  carry the Wave B guarantee, and neither has a pack-local proposal
  behind it.

Each Wave A and Wave B spec began as the pack's own
`research/DRILL_PROPOSAL.md`. The spec here is now the only copy: the
pack organ used to hold a byte-identical second one that nothing
compared, so it points here instead. The manifest keeps the source path
and its first commit as provenance.

## The three things a drill needs to run

The runner grades; it does not think. For a drill to return anything
other than `manual` it needs all three:

1. `<drill>.md`, the frozen spec, matching its recorded hash. Present
   for all twenty-two.
2. `scenarios/<drill>/`, the fixture tree the drill materialises into a
   scratch directory. **Built for `architecture` only.** Every spec
   describes one; twenty-one were never built.
3. `graders/<drill>/cN.py`, one grader per numbered criterion. **Built
   for `architecture` only**, all ten. Every spec calls its criteria
   machine-checkable; for the other twenty-one the scripts that would
   check them are still unwritten.

A grader follows the frozen benchmark criteria contract: `argv[1]` is
the scratch directory, it prints one JSON object
`{"id", "pass", "reason"}` and exits 0 on pass, non-zero on fail. Exit
2 is reserved and means the grader ran and could not settle the
criterion here, usually because the tool it drives is absent. That is
recorded as manual, not as a fail: a grader has no way to tell "the
work is wrong" from "I could not look" through a boolean, and reporting
the second as the first invents findings on any machine without the
toolchain. Three of the architecture graders drive `lint-imports` and
take that path where import-linter is not installed.

A scenario tree is not held to the repository's front-matter law and is
not indexed. It is a toy project a cold agent works inside, so it has
to read as an ordinary repository: EOS metadata in one of its files is
a tell that the run is a test.

## Why the drills currently report no verdict

With no scenario and no graders, every criterion is prose a human must
judge. The runner reports it as `manual`, does not count it as a pass,
and gives the drill a `pass` of `null` with the reason stated. It exits
1, because a drill that did not run is not a drill that passed.

There is also a fourth thing a drill needs that no command supplies:
the cold-agent session that does the work. `drills run` materialises the
scenario and grades a tree. Handing the scenario to an agent and
capturing what it delivers is the harness's job, and the graded tree
comes back through `--attempt DIR`. Running the command with no
`--attempt` grades the untouched fixture, which is worth doing once per
drill to prove the criteria discriminate, and is worth nothing as
evidence about a pack.

The architecture drill has had that discrimination check both ways, and
it is a test rather than a claim: `tests/test_drills.py` asserts the
untouched fixture fails every criterion that can be settled without
import-linter, and that a correct tree passes them. A grader that
cannot fail is not a grader, and neither is one that cannot pass.
`architecture` still reports no verdict, because no cold agent has been
handed the scenario yet.

## The results ledger

`RESULTS.json` is append-only: one entry per drill per run, holding the
date, the pack, the per-criterion verdicts and the reason. Rows are
never rewritten or removed, and a `pass` of `null` is recorded as
plainly as a `false`.
