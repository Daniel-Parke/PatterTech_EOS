---
summary: Who reviews a change and how hard, from machine gate only to independent human review at every merge
type: guide
tags: [delivery, ci, wargame]
kind: guide
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: observational
sources: [EV-0010, EV-0069, EV-0070, EV-0164, EV-0165, EV-0166, EV-0167, EV-0181]
review: 2027-02
review_by: 2027-02
---

# GD-COD-002: Who reviews this change, and how hard?

## The question

A change is written, mostly by a model, and something has to decide it
can merge. The fork is how much of that decision is machine, how much is
another model, and how much is a person. Getting it wrong in one
direction burns the operator's whole week on ceremony. Getting it wrong
in the other direction means nobody is answerable when a change causes
harm.

## It depends on

- What tier does the router rule for the task under
  `kernel/POLICY_SPEC.md`, and which factors are active?
- Is the harm reversible? Can you tell within an hour that it went
  wrong?
- Is there a second person at all, or is this a solo operator directing
  agents?
- Would a reviewer actually understand this change, or would they be
  approving a diff they cannot follow?

## Options

### A. Machine gate only, self-merge

Diff-aware policy and security rules plus the test suite, then merge.
Buys: the fastest loop available, and the gate is the part with the
strongest evidence behind it (EV-0070, EV-0069, EV-0181). Costs: it
catches classes, not intent. Nobody is answerable for the merge, and
architectural error passes untouched.

### B. Machine gate plus an agent reviewer

Add a second model reading the diff against the pack, kept separate from
the model that wrote it. Buys: cheap defect detection and style
enforcement, and it can run on every change. Costs: hallucinated
approvals, weak architectural judgement, and an unsolved prompt
injection surface, all conceded by the strongest argument for this
option (EV-0167).

### C. Machine gate, agent reviewer, sampled human review

As B, with a fraction of changes pulled for a person to read, the
fraction set by the capability profile. Buys: an accountability sample
and a feedback signal on how well B is doing, at a cost that scales with
trust rather than with volume. Costs: the sample can miss the change
that mattered.

### D. Independent human review at every merge

A person approves everything. Buys: a named human answerable for every
change. Costs: at scale this is 10 to 15 per cent of engineering hours
with feedback routinely over 24 hours (EV-0167), and its measured
product is knowledge transfer and awareness rather than defect finding
(EV-0166), which a solo operator with agent authors does not collect.

## Decision rule

Route by the tier the router rules, never by the size of the diff alone.

- R0, reversible local work: A. The machine gate is the whole gate.
- R1, the standard tier: C. Agent review on everything, human sample at
  the rate the capability profile sets.
- R2, auth surface, money, schema change, public contract, CI and
  stateful infrastructure, PII: D. Independent review at acceptance,
  with the oracle authored and frozen before implementation.
- R3, irreversible or externally consequential: D plus operator
  approval, always.
- Guarded actions are not review questions. `kernel/GUARD_SPEC.md`
  rules them, and no review verdict moves a guard verdict.

## Default

C at R1, which is where most work lands. The machine gate is binding
under every option and is not part of this fork.

## Why a human stays in the loop at all

Not for defect yield. The measured defect yield of human review is lower
than practitioners expect and most of the value shows up as knowledge
transfer (EV-0166), which a one-person venture directing agents mostly
does not receive. The reason is the accountability gap: when an
auto-approved change causes harm, there is no agent to hold answerable,
and that gap is named as unsolved by the paper arguing hardest for
agent-led review (EV-0167). Where the harm is real, a person signs.
Where it is not, ceremony is the only thing being bought.

## How to review when you do review

Approve once the change definitely improves overall code health even
when it is imperfect, and refuse only what definitely worsens it. Settle
style by the style guide and the formatter, never by taste (EV-0164).
Keep changes small, because that is the mechanism that makes review
affordable at all (EV-0165). Read the error paths first; that is where
the catastrophes live.

## Evidence boundary

EV-0165 and EV-0166 are single-company studies from 2018 and 2013,
predating machine authorship entirely, and EV-0164 is now an archived
read-only repository. EV-0167 is a preprint with no new data. Nothing
here is a controlled measurement of reviewing machine-written diffs,
because no such measurement exists yet. Note also that self-reported
speed is unreliable in this area: developers were measured 19 per cent
slower while believing they were 20 per cent faster (EV-0010), so do not
justify dropping a tier on how fast it feels.

## Worked rulings

- **PatterTech EOS coding pack (2026-08, argued)**: C at R1, D at R2 and
  above, with the machine gate binding everywhere. Argued from EV-0166
  for the ceremony claim and EV-0167 for the accountability gap.
- **Webhook signature verification (2026-08, argued)**: D. The auth
  surface factor puts the task at R2 regardless of the two-line diff.
  See `packs/coding/exemplars/EX-COD-001-webhook-silent-failure.md`.
- **Documentation and comment-only diffs (2026-08, inherited)**: A,
  inherited from the R0 routing in `kernel/POLICY_SPEC.md`.
