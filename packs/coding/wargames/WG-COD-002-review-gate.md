---
id: WG-COD-002
summary: Who reviews a change and how hard, from machine gate only to independent human review at every merge
kind: wargame
type: wargame
tags: [ci, delivery, eos, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-COD-006, DOC-COD-007]
applies_when: [edits_source]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: observational
sources: [EV-0010, EV-0069, EV-0070, EV-0164, EV-0165, EV-0166, EV-0167, EV-0181]
review: 2027-02
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-COD-002: Who reviews this change, and how hard?

## Decision question and stakes

A change is written, mostly by a model, and something has to decide it
can merge. The fork is how much of that decision is machine, how much is
another model, and how much is a person. Getting it wrong in one
direction burns the operator's whole week on ceremony. Getting it wrong
in the other direction means nobody is answerable when a change causes
harm.

## Doctrines or coverage gap under pressure

- `DOC-COD-006` (binding): A diff-aware machine gate runs before every merge.
- `DOC-COD-007` (default): Human review is scoped by risk, not applied as a blanket.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- What tier does the router rule for the task under
  `kernel/POLICY_SPEC.md`, and which factors are active?
- Is the harm reversible? Can you tell within an hour that it went
  wrong?
- Is there a second person at all, or is this a solo operator directing
  agents?
- Would a reviewer actually understand this change, or would they be
  approving a diff they cannot follow?

Applicability is `edits_source`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

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

## Failure premises

### Premortem for A. Machine gate only, self-merge

Assume `A. Machine gate only, self-merge` was selected and the outcome failed. Test this option's stated failure mechanism first: it catches classes, not intent. Nobody is answerable for the merge, and architectural error passes untouched.

### Premortem for B. Machine gate plus an agent reviewer

Assume `B. Machine gate plus an agent reviewer` was selected and the outcome failed. Test this option's stated failure mechanism first: hallucinated approvals, weak architectural judgement, and an unsolved prompt injection surface, all conceded by the strongest argument for this option (EV-0167).

### Premortem for C. Machine gate, agent reviewer, sampled human review

Assume `C. Machine gate, agent reviewer, sampled human review` was selected and the outcome failed. Test this option's stated failure mechanism first: that scales with trust rather than with volume. Costs: the sample can miss the change that mattered.

### Premortem for D. Independent human review at every merge

Assume `D. Independent human review at every merge` was selected and the outcome failed. Test this option's stated failure mechanism first: at scale this is 10 to 15 per cent of engineering hours with feedback routinely over 24 hours (EV-0167), and its measured product is knowledge transfer and awareness rather than defect finding (EV-0166), which a solo operator with agent authors does not collect.

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

## Safe default

C at R1, which is where most work lands. The machine gate is binding
under every option and is not part of this fork.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **What tier does the router rule for the task under `kernel/POLICY_SPEC.md`, and which factors are active?** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** C at R1, which is where most work lands. The machine gate is binding under every option and is not part of this fork.

**Exit condition:** Stop or roll back the selected branch when it catches classes, not intent. Nobody is answerable for the merge, and architectural error passes untouched, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: What tier does the router rule for the task under `kernel/POLICY_SPEC.md`, and which factors are active?

## Counter-evidence and transfer limits

### Evidence boundary

EV-0165 and EV-0166 are single-company studies from 2018 and 2013,
predating machine authorship entirely, and EV-0164 is now an archived
read-only repository. EV-0167 is a preprint with no new data. Nothing
here is a controlled measurement of reviewing machine-written diffs,
because no such measurement exists yet. Note also that self-reported
speed is unreliable in this area: developers were measured 19 per cent
slower while believing they were 20 per cent faster (EV-0010), so do not
justify dropping a tier on how fast it feels.
### Preserved reasoning: Why a human stays in the loop at all

Not for defect yield. The measured defect yield of human review is lower
than practitioners expect and most of the value shows up as knowledge
transfer (EV-0166), which a one-person venture directing agents mostly
does not receive. The reason is the accountability gap: when an
auto-approved change causes harm, there is no agent to hold answerable,
and that gap is named as unsolved by the paper arguing hardest for
agent-led review (EV-0167). Where the harm is real, a person signs.
Where it is not, ceremony is the only thing being bought.
### Preserved reasoning: How to review when you do review

Approve once the change definitely improves overall code health even
when it is imperfect, and refuse only what definitely worsens it. Settle
style by the style guide and the formatter, never by taste (EV-0164).
Keep changes small, because that is the mechanism that makes review
affordable at all (EV-0165). Read the error paths first; that is where
the catastrophes live.
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
