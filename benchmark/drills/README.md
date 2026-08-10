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
   scratch directory. **Built for all twenty-two.**
3. `graders/<drill>/cN.py`, one grader per numbered criterion. **Built
   for all twenty-two**, though not for every criterion: where a
   property is genuinely a matter of judgement the grader is absent on
   purpose and the criterion reports `manual`.

Each set was built by one agent and then attacked by another, whose job
was to break it: construct a tree that looks right and still carries
the defect, and a correct tree that solves the problem a different way,
then check the graders fail the first and pass the second. Three sets
failed that check on the first pass. One was a grader set in which a
document that negated every load-bearing claim still passed all eleven
criteria. Five graders were withdrawn outright and are listed in
`graders/DEMOTED.md` with the tree that beat each one.

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

Every drill now materialises its scenario and runs its graders, so a
criterion comes back `pass` or `fail`. A criterion with no grader, or
one whose grader exits 2 because the tool it drives is absent, reports
`manual`, and a manual criterion is never counted as a pass. Against
the untouched fixture all twenty-two come back `fail`, and the command
exits 1. That is a discrimination check, not evidence about a pack.
The rows already in `RESULTS.json` were written before any scenario or
grader existed and carry a `pass` of `null` with the reason stated.

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

No drill reports a verdict yet, because no cold agent has been handed a
scenario. Graders make a verdict possible; they are not one.

## Three specs name paths that have never existed

Found by the 2026-08-10 documentation pass. They are recorded here
rather than corrected, because the manifest above says a drill spec
never changes without an ADR amendment, and two of the three are Wave A
oracles whose worth is that they have not been written to since they
were frozen. Read the spec, then read this.

- `delivery-testing.md` says its checks run by
  `tools/drill_delivery_testing.py`. No such file has ever existed on
  any branch. Its ten graders are at
  `benchmark/drills/graders/delivery-testing/`.
- `legal-licensing.md` puts its fixture at
  `packs/legal-licensing/drill/fixture/`, and
  `security-privacy.md` puts its at
  `packs/security-privacy/drill/fixture/`. Neither path has ever
  existed. Both scenarios are at
  `benchmark/drills/scenarios/<pack>/`.

Nothing follows those paths at run time: `drills.py` resolves a
scenario from `scenarios/<pack>/` and graders from `graders/<pack>/`,
so the drills run correctly and only a reader is misled. Correcting
the specs needs an accepted ADR amendment and a re-hash of the drill
manifest.

## What the adversarial pass found, and what is still open

Worth reading before trusting any of these sets, because the same
weaknesses will be in the ones nobody has attacked yet:

- **Vocabulary is not meaning.** Several graders matched an expected
  phrase rather than the property. A stage described in different words
  went ungraded; changing a path to the words "the weekly report"
  flipped a verdict. Those graders are withdrawn.
- **Criteria are independent, so a document can contradict itself and
  pass.** Each grader checks one claim appears somewhere; none reads
  the record against itself.
- **A correct answer in an unexpected shape can fail.** Class-based
  `unittest` tests were invisible to three `coding` graders, which is a
  false failure for a mainstream style, and renaming a module failed
  four criteria that name the file.
- **Partial fixes can pass.** A tree that raised on one malformed field
  and silently swallowed another satisfied every `coding` grader.
- **The graders sit in the repository the drill sends an agent into.**
  `benchmark/fixtures` has a holdout exclusion; the drill graders have
  none, and a set spells out the exact mutation and probe strategy. What
  a cold-agent session can see is a harness decision and needs taking
  deliberately.

These are recorded rather than quietly fixed, because a partial fix
that leaves the reader believing the set is sound is the failure this
whole exercise is about.

## The results ledger

`RESULTS.json` is append-only: one entry per drill per run, holding the
date, the pack, the per-criterion verdicts and the reason. Rows are
never rewritten or removed, and a `pass` of `null` is recorded as
plainly as a `false`.
