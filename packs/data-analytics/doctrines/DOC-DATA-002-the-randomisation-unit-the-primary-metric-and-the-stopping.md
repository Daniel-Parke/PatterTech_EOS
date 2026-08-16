---
summary: The randomisation unit, the primary metric and the stopping rule are written down before traffic starts.
type: doctrine
tags: [eos]
id: DOC-DATA-002
statement: The randomisation unit, the primary metric and the stopping rule are written down before traffic starts.
kind: doctrine
authority: binding
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [runs_experiment]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0313]
review: 2027-11
lifecycle: active
verification_refs: [packs/data-analytics/CHECKS.md]
migration_sources: [packs/data-analytics/PACK.md:requirements:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B4]
---

# DOC-DATA-002

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`runs_experiment`. Prevents
the failure that no later analysis can repair: choosing the metric and
the stopping point after seeing the data. The dominant experimentation
errors are interpretive rather than computational, and monitoring a
fixed-horizon test continuously can push the false positive rate far
above its nominal five per cent (EV-0313). Scope note: that finding
comes from platforms running hundreds of concurrent experiments for
millions of users. The mechanism transfers to one experiment; the base
rates do not. Basis: empirical-evidence.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/data-analytics/PACK.md:requirements:002`, lines 119-128, SHA-256 `4e1fa1df4db860b1f263d46ad7cce072b86c7daed53695b3b30ae0a327e9d175`.
