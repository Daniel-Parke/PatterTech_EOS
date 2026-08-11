---
summary: How lanes land, who decides the order, and the review topology that scales with lane count
kind: recipe
scope: estate
sources: [EV-0053, EV-0107, EV-0108, EV-0167, EV-0169, EV-0251, EV-0490]
type: guide
tags: [eos, delivery, arch]
review: on-change-of:agent-harness-major-release
---

# Merge and review

The mechanics behind B9, D7, D8 and D9 in
`packs/agentic-swarm/PACK.md`. Generation is not the constraint.
Landing is. Every measured pipeline in the research behind this pack
says the same thing, so this file is about the half of the run that the
fan-out made harder.

## Isolation

One lane, one worktree, one branch, one owned file set. Enforced by the
version control system or the harness, never by instruction: the same
vendor that ships enforced worktree isolation for sessions documents
plainly that its non-isolating surface produces overwrites when two
agents edit one file, and tells you to partition instead (EV-0108).

Two operational details that cost runs:

- **Serialise creation.** Concurrent worktree creation races on the git
  config lock, killing agents before they start and leaving orphaned
  branches. Create one at a time behind a lock, then run in parallel.
- **Carry the environment in.** A fresh worktree has no ignored
  configuration, so a lane that cannot run its own checks hands you
  unverified work and calls it done.

## Claims

A lane claims its scope by committing a claim file. Version control is
the mutex and the history is the audit trail. This is how sixteen
parallel agents coordinated on a real project with no message bus at
all: a claim file per task, with the second claimant losing the race at
the merge and picking something else (EV-0053).

## The merge gate

The integrator owns the order and records it before the first merge.
Order is a decision, not a consequence of who finished first. Left to
infer relations between queued changes, agents recalled 35 to 58 per
cent of them and committed unsafe merges in 69.8 per cent of runs;
handed the relations, they respected them 98 to 100 per cent of the
time. So the partition artefact is also the merge plan.

Per lane, at the gate:

1. **Diff against the claim.** Anything outside the lane's declared
   write set is a finding, not a bonus.
2. **Run the deterministic scanners.** Secrets, dependency resolution,
   types, build, licences. These classes are never delegated to a
   reviewer agent: of 74 validated genuine credentials in agent
   changes, 81.1 per cent reached integration with no comment from
   seven review tools or any human.
3. **Run the verifier that predates the lane**, plus the shared
   contract checks that cross the seam.
4. **Merge in the recorded order**, then run rolling integration checks
   before the next lane goes in.
5. **Regenerate every derived view.** Derived files are integrator-owned
   for exactly this reason.

Batch rather than merging strictly one at a time where the queue is
long, and bisect on failure. Batch size is tunable rather than
monotonic: in one benchmark most models improved as the batch grew and
one peaked at eight and then declined.

## Diff width

Cap it per work package in the packet, and land in dependency order,
one concern per landing. Agent changes are about 2.6 times larger than
unassisted ones, wait roughly five times longer to be picked up, and
land within thirty days at 32.7 per cent against 84.5 per cent.
Detection collapses on wide diffs, so the ceiling belongs on the
package, where it is enforceable, rather than on the reviewer, where it
is a wish.

## Review topology

Four layers, in cost order. Nothing below is a substitute for the layer
above it.

| Layer | What it is | Why it is here |
| --- | --- | --- |
| 0 | The specification | Restoring the full specification alone recovered the single-agent ceiling in a controlled factorial test, while conflict reports added nothing measurable. Spend here first |
| 1 | Deterministic scanners | The classes that escape reviewers entirely |
| 2 | Seam review | A distinct role whose remit is only the joins: shared representations, contract conformance, duplicated abstractions, ownership violations. No lane can see the seam, because no lane can see the seam |
| 3 | Clean-context reviewer per concern | One strong reviewer, not a panel |
| 4 | A person at the gate | Judgement and accountability, on a declared budget |

Rules that hold across layers 3 and 4:

- **The writer never reviews its own lane**, and no reviewer shares a
  context window with the writer.
- **Describe, then judge.** The reviewer states the behaviour and
  compares it against the requirement. It does not produce a fix in the
  same pass: asking for one collapsed a model's recognition of correct
  code from 52.4 to 11.0 per cent, and a compare-and-report prompt
  restored it to 85.4.
- **A reviewer weaker than the writer may not modify the writer's
  output.** A weaker cross-family reviewer regressed 11.2 per cent of
  already-passing solutions, which is worse than no review.
- **Two judgements, not N.** Measured inter-judge error correlation
  puts effective jury size at about two, however many judges are added,
  and a single well-specified judge with an explicit rubric is more
  consistent than a panel (EV-0251).
- **A refuter may lower confidence or route to a person. It may not
  close a finding.** Adversarial stages in one deployment unanimously
  killed a real defect that only a human override recovered.
- **Unverifiable is not refuted.** A claim that could not be checked is
  reported as unverified, and unverified blocks acceptance in the
  excluded classes.
- **Lane prose is untrusted.** Reviewers extract claims from the diff,
  never from the narrative. Framings claiming prior approval survive
  filtering most often, and they are cheap to write.
- **One integrator ranks and deduplicates findings.** Never merge
  findings by vote: consensus selection loses to diversity-based
  selection because models converge on the plausible wrong answer.

## The excluded classes

These never take a machine-only acceptance path, whatever the run
record says: authentication and authorisation, secrets handling,
payment and money movement, data deletion and migration, public API
contracts, licence-sensitive or externally published code, and any file
previously implicated in an incident. The list follows a production
deployment where automated acceptance was earned per authoring pattern
rather than granted, with a clean window before eligibility, daily
volume caps, revocation on a single incident and a permanent exclusion
list covering incident-prone paths (EV-0490, whose
revert-rate comparison carries a selection effect its authors
acknowledge).

## The human budget

Declare it before the swarm starts: minutes, maximum lines to be read,
and the sampling rule. It does not grow to fit the diff. If the run
produces more than the budget covers, land less. Review-quality
detection falls sharply on long sessions and wide changes, which is the
mechanism behind the credential escapes above.

## What to measure

Two numbers, published beside lane count: median time from lane-done to
merged, and the share of lane-authored code rewritten within fourteen
days of merging. These definitions come from one practitioner and are
unvalidated, so they are instrumentation to test rather than settled
practice. The failure they detect is not in doubt: throughput rises
while stability falls (EV-0169), the argument that agents supersede
human review is now made in the literature with its own authors listing
unresolved objections (EV-0167), and a practitioner who had argued
against multi-agent systems settled on a clean-context reviewer as one
of three patterns that work (EV-0107).
