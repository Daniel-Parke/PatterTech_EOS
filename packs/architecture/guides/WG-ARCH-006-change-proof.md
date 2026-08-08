---
summary: What proves a change changed nothing, whether a green suite, behaviour pinned first, a byte-stable output canary, or a differential run against the old version
kind: guide
scope: estate
authority: default
basis: decision
evidence_grade: observational
sources: [EV-0155, EV-0156, EV-0180, EV-0191]
review: 2027-07
type: guide
tags: [arch, testing, ci]
review_by: 2027-07
---

# WG-ARCH-006: what proves a change changed nothing?

Carried forward from the v1 wargame of the same id, re-graded against
the 2026 evidence sweep. Two things changed. The v1 default pinned
behaviour first and reached for a hash where determinism allowed it;
D10 of `packs/architecture/PACK.md` puts the canary first wherever
output is deterministic. And the fork gained a fourth option v1 did
not carry, the differential run against the old version.

## The question

Restructures, moves, dependency bumps and rewrites all claim behaviour
is unchanged. The fork is the strength of proof demanded before that
claim is believed. "The tests pass" measures what the tests measure
and is silent about the rest, which is thin ground for a restructure.

## It depends on

- Whether the output is a deterministic artefact, documents, exports,
  a build, or live behaviour that never repeats itself exactly.
- How thin the existing suite is over the paths being touched.
- Whether an agent is doing the restructuring. An agent needs a proof,
  not a sense that it went fine.
- Whether the old version is still runnable, and whether a corpus of
  real inputs exists to run it against.

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

## Decision rule

Deterministic artefact output: **C**, hashing composed content so the
canary survives a move, with re-baselining a reviewed event. Live
behaviour and a thin suite over the touched paths: **B**, pinned in
its own commit before anything moves, the ruling
`packs/coding/guides/GD-COD-004-pin-then-change.md` reaches from the
code side. A large surface, no baselines, the old version runnable and
real inputs to hand: **D**, once the non-determinism is scrubbed.
**A** alone only where the suite demonstrably covers the touched
paths, and never for an agent-driven restructure.

## Default

**C** where the output is deterministic, **B** everywhere else. Pixels
count as artefacts, so visual regression at zero threshold inside a
pinned container is C for a user interface.

## Worked rulings

- **PatterTech_Business (2026-06, argued)**: C. An output-hash canary
  over composed kit output, its ADR-0004, which survived the physical
  ring move of its ADR-0007 with both hashes unchanged, and
  re-baselining governed as a reviewed event by its ADR-0011.
- **WiseWattage (2026, argued)**: C for pixels, Lost Pixel at zero
  threshold inside a pinned container, and B by policy for refactors
  where the suite is thin, its PB-012.
- **PatterStudio (2026-07, argued)**: C. A byte-stable build with
  nothing generative in the build step; `registry/LESSONS.md` records
  it becoming the estate principle that plan and build decouple.

## Counter-evidence

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
