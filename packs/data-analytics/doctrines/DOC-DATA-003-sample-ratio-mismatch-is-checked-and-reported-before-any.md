---
summary: Sample ratio mismatch is checked and reported before any experiment result is read, and a failed check voids the result.
type: doctrine
tags: [eos]
id: DOC-DATA-003
statement: Sample ratio mismatch is checked and reported before any experiment result is read, and a failed check voids the result.
kind: doctrine
authority: binding
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [runs_experiment]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0316]
review: 2027-11
lifecycle: active
verification_refs: [packs/data-analytics/CHECKS.md]
migration_sources: [packs/data-analytics/PACK.md:requirements:003]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B5]
---

# DOC-DATA-003

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`runs_experiment`. A gap between the assignment ratio you asked for and
the ratio you observed means something interfered, and whatever
interfered almost certainly also moved the metric, so the result is not
usable at any confidence level (EV-0316). Prevents the worst outcome in
this domain: computing the check, seeing it fail, and reporting the win
anyway. Basis: empirical-evidence.

Guarded actions sit outside this pack. Deletion of production data,
secret access and the rest keep their floors under
`kernel/GUARD_SPEC.md` whatever an analytics task concludes.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/data-analytics/PACK.md:requirements:003`, lines 130-141, SHA-256 `e942fa30f62e3c97ffc0f8399ab089e771b2dbb462b33d984e4029381a5ba4e8`.
