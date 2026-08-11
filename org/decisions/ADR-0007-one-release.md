---
summary: Hold v2, fold v2.1 into it, release once, strike the two efficiency gates with reasons and retire the sealed suite unopened
type: decision
tags: [eos]
status: accepted
decided_by: Daniel Parke
date: 2026-08-10
---

# ADR-0007: one release

Daniel decided on 2026-08-10 that v2 is not released on its own. The
v2.1 work folds into the unreleased line and the two versions ship as
one. This record settles what the release gate is, because the gate set
ADR-0002 approved can no longer be computed.

## Context

v2 has been merged and unreleased since 2026-08-10. Of the eight release
gates in `benchmark/PROTOCOL.md`, the reproducible 2026-08-08 batch of
103 sessions passes three, fails two and leaves three uncomputed:

| Gate | Threshold | Result |
| --- | --- | --- |
| Ceremony lines | 60 per cent fewer | 77.3 per cent fewer, pass |
| Aggregate pass rate | no regression | 73.6 to 100 per cent, pass |
| Completeness | three trials a slot | 12 slots, none short, pass |
| Context tokens | 30 per cent fewer | 9.1 per cent fewer, fail |
| Wall clock | 25 per cent faster | 4.6 per cent faster, fail |
| Per-task no-regression | sealed suite | uncomputed |
| Safety gates | sealed suite | uncomputed |
| Pack drills | a verdict each | uncomputed, 22 of 22 null |

The result that is not on the gate list is the one that matters: 53 v1
runs produced fully passing work 39 times, and 50 v2 runs produced it 50
times.

Daniel has also decided that no further benchmark runs are made as part
of this work. That decision is deliberate and it has a consequence this
record must state plainly: **no measurement of the evolved system will
exist.** The two efficiency gates cannot be re-tested against v2.1, and
amending their thresholds to match the figures already achieved would be
tuning the target to the result, which is the exact dishonesty this
repository spent its pre-release review removing.

## Decision

1. **The 2026-08-08 figures are the final measured state of the line.**
   They are recorded as achieved, not as passed.

2. **The context-token and wall-clock gates are struck**, with the reason
   recorded here: they were authored to compare two kernels under a
   frozen harness, the system they were to judge has since changed shape,
   and the instrument that would re-judge it is not being run. A struck
   gate is not a met gate and no document may describe it as one.

3. **The sealed suite `SEALED-BENCH-2026-08` is retired unopened.** It
   runs once, it needs Daniel's private key, and it was authored for a
   frozen-v1 against final-v2 comparison that this decision supersedes.
   Spending it now would answer a question nobody is asking. The key
   stays with Daniel; the suite is not deleted; a future sealed
   evaluation is authored fresh against whatever it is meant to judge.

4. **The pack-drill gate is not a release blocker.** Twenty-two drills
   have scenarios and graders and no cold-agent verdicts. Running them is
   a spend decision Daniel has deferred, and it moves to the optional
   post-release list along with the three designed-but-never-run policy
   comparison runs.

5. **The release gate for this line is therefore:** the checker green
   with the semantic and freshness series, the full test suite green, the
   CHANGELOG written, no false statement about the tree surviving the
   final review, and Daniel's explicit approval under PB-E05. Delivery
   quality, measured at 50 of 50 against 39 of 53, is the evidence
   offered for the release; efficiency is offered as unmeasured.

## What this costs

The line ships without an independent evaluation of its safety and
per-task regression behaviour, because those two gates depended on the
sealed suite. That is a real reduction in assurance against the plan
ADR-0002 approved, and it is accepted knowingly rather than papered
over. What replaces it is weaker and is named as weaker: the visible
criteria in the reproducible batch, the checker's semantic series, and
the review passes at the end of the v2.1 build.

## Reversal

If Daniel later wants the comparison, nothing here prevents authoring a
new sealed suite against the released line and running it once. The
retired suite stays in the tree with its hashes, so the decision is
auditable and reversible in the only sense that matters: the evidence
about what was and was not measured survives.
