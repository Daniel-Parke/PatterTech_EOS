---
summary: Human review is scoped by risk, not applied as a blanket.
type: doctrine
tags: [eos]
id: DOC-COD-007
statement: Human review is scoped by risk, not applied as a blanket.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [edits_source]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0166, EV-0167]
review: 2027-02
lifecycle: active
verification_refs: [packs/coding/CHECKS.md]
migration_sources: [packs/coding/PACK.md:defaults:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D1]
---

# DOC-COD-007

The `statement` field is the canonical standing proposition.

## Reasoning and limits

The
machine gate in B5 runs on everything. Human review is routed by the
tier that `kernel/POLICY_SPEC.md` rules for the task: R0 and R1 take
agent review plus sampled human review, R2 takes independent review at
acceptance, R3 always takes a human. Reason: review's measured product
is knowledge transfer and awareness rather than defect finding
(EV-0166), and a solo operator directing agents collects almost none of
that transfer, so blanket review buys ceremony. The reason a human
stays in the loop on high-risk changes is not defect yield, it is the
accountability gap: when an auto-approved change causes harm, no agent
is answerable for it, and that gap is named as unsolved by the strongest
argument for agent-led review (EV-0167), which is a preprint with no new
data and should be read as a hypothesis. Override by recording which
tier you moved and why. See
`packs/coding/guides/GD-COD-002-review-gate.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/coding/PACK.md:defaults:001`, lines 192-206, SHA-256 `88da49524cbee1b0ff73d9e325db395cc842d5f2f5ae332ef7c1d0298601e786`.
