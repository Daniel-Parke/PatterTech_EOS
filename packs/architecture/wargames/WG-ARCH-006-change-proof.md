---
id: WG-ARCH-006
summary: What proves a change changed nothing, whether a green suite, behaviour pinned first, a byte-stable output canary, or a differential run against the old version
kind: wargame
type: wargame
tags: [arch, ci, eos, testing, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-ARCH-013]
applies_when: [has_server_code]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: decision
evidence_grade: observational
sources: [EV-0155, EV-0156, EV-0180, EV-0191]
review: 2027-07
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-ARCH-006: what proves a change changed nothing?

Carried forward from the v1 wargame of the same id, re-graded against
the 2026 evidence sweep. Two things changed. The v1 default pinned
behaviour first and reached for a hash where determinism allowed it;
D10 of `packs/architecture/PACK.md` puts the canary first wherever
output is deterministic. And the fork gained a fourth option v1 did
not carry, the differential run against the old version.

## Decision question and stakes

Restructures, moves, dependency bumps and rewrites all claim behaviour
is unchanged. The fork is the strength of proof demanded before that
claim is believed. "The tests pass" measures what the tests measure
and is silent about the rest, which is thin ground for a restructure.

## Doctrines or coverage gap under pressure

- `DOC-ARCH-013` (default): Proof of harmless change is a byte-stable output canary where output is deterministic.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Whether the output is a deterministic artefact, documents, exports,
  a build, or live behaviour that never repeats itself exactly.
- How thin the existing suite is over the paths being touched.
- Whether an agent is doing the restructuring. An agent needs a proof,
  not a sense that it went fine.
- Whether the old version is still runnable, and whether a corpus of
  real inputs exists to run it against.

Applicability is `has_server_code`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. The suite is the proof

**What it is.** Green before, green after, nothing added.

**Buys.** Nothing to build, nothing to maintain. Where the suite
covers the touched paths it is the honest answer and it is free.

**Costs.** As strong as what the suite detects, which is not what the
suite runs. Just et al. (EV-0191) found 73 per cent of real faults
coupled to at least one mutant, so 27 per cent were coupled to none,
and the correlation weakens once suite size is controlled.

### B. Behaviour pinned first

**What it is.** Characterisation or approval tests over the touched
surface, written before the change and landing in their own commit.
Capture current output, diff every later run against it, require a
person to approve any change to the approved artefact (EV-0180).

**Buys.** A fence around the actual blast radius, in minutes, over
code nobody can specify.

**Costs.** It records current bugs as if they were intent, so it is a
net and never a specification. Approvals rot into reflexive stamps,
and output that varies run to run needs scrubbers first.

### C. Byte-stable output canary

**What it is.** A hash of the composed output, content rather than
paths, pinned before the change and compared after. Re-baselining is a
reviewed event with the old and new hashes recorded.

**Buys.** The strongest claim on offer. Not that the tests still pass
but that the artefact is the same bytes, and it survives a file move.

**Costs.** Only possible where output is deterministic, and
determinism is bought rather than found. SOURCE_DATE_EPOCH (EV-0155)
clamps the timestamp non-determinism; hermeticity (EV-0156) buys the
rest by treating tools as versioned dependencies and identifying
inputs by content hash. A hash tells you something moved, never what.

### D. Differential run against the old version

**What it is.** Keep the version being replaced runnable, feed both it
and the new one the same corpus of real inputs, and diff the results.

**Buys.** Coverage of behaviour nobody ever wrote a test for, with no
baseline files to keep, which is what a surface too large to pin needs.

**Costs.** Two runnable versions, a representative corpus or the proof
is theatre, and suppressed side effects or the comparison writes
twice. It proves equivalence over the inputs you ran and no others.

## Failure premises

### Premortem for A. The suite is the proof

Assume `A. The suite is the proof` was selected and the outcome failed. Test this option's stated failure mechanism first: As strong as what the suite detects, which is not what the suite runs. Just et al. (EV-0191) found 73 per cent of real faults coupled to at least one mutant, so 27 per cent were coupled to none, and the correlation weakens once suite size is controlled.

### Premortem for B. Behaviour pinned first

Assume `B. Behaviour pinned first` was selected and the outcome failed. Test this option's stated failure mechanism first: It records current bugs as if they were intent, so it is a net and never a specification. Approvals rot into reflexive stamps, and output that varies run to run needs scrubbers first.

### Premortem for C. Byte-stable output canary

Assume `C. Byte-stable output canary` was selected and the outcome failed. Test this option's stated failure mechanism first: Only possible where output is deterministic, and determinism is bought rather than found. SOURCE_DATE_EPOCH (EV-0155) clamps the timestamp non-determinism; hermeticity (EV-0156) buys the rest by treating tools as versioned dependencies and identifying inputs by content hash. A hash tells you something moved, never what.

### Premortem for D. Differential run against the old version

Assume `D. Differential run against the old version` was selected and the outcome failed. Test this option's stated failure mechanism first: Two runnable versions, a representative corpus or the proof is theatre, and suppressed side effects or the comparison writes twice. It proves equivalence over the inputs you ran and no others.

## Decision rule

Deterministic artefact output: **C**, hashing composed content so the
canary survives a move, with re-baselining a reviewed event. Live
behaviour and a thin suite over the touched paths: **B**, pinned in
its own commit before anything moves, the ruling
`packs/coding/wargames/WG-COD-004-pin-then-change.md` reaches from the
code side. A large surface, no baselines, the old version runnable and
real inputs to hand: **D**, once the non-determinism is scrubbed.
**A** alone only where the suite demonstrably covers the touched
paths, and never for an agent-driven restructure.

## Safe default

**C** where the output is deterministic, **B** everywhere else. Pixels
count as artefacts, so visual regression at zero threshold inside a
pinned container is C for a user interface.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Whether the output is a deterministic artefact, documents, exports, a build, or live behaviour that never repeats itself exactly.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** **C** where the output is deterministic, **B** everywhere else. Pixels count as artefacts, so visual regression at zero threshold inside a pinned container is C for a user interface.

**Exit condition:** Stop or roll back the selected branch when As strong as what the suite detects, which is not what the suite runs. Just et al. (EV-0191) found 73 per cent of real faults coupled to at least one mutant, so 27 per cent were coupled to none, and the correlation weakens once suite size is controlled, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Whether the output is a deterministic artefact, documents, exports, a build, or live behaviour that never repeats itself exactly.

## Counter-evidence and transfer limits

The evidence grades the options and does not rank them. Nothing in the
ledger measures whether a canary catches regressions a suite misses,
at any scale, let alone at ours. EV-0155 states its own limit: the
variable is necessary and far from sufficient, and fresh issue classes
keep arriving, so C's precondition is a piece of work rather than a
switch. EV-0156 is vendor documentation with no effect sizes that does
not price the cheaper point most ventures sit on, lockfiles plus a
pinned image. EV-0180 is a tool, not a study. EV-0191 is Java, five
projects, faults drawn from version-control history and so biased
towards the ones that were found. D carries no ledger evidence at all:
it is what people reach for when there is no baseline, graded on
argument alone.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
