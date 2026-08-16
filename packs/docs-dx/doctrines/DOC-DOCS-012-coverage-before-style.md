---
summary: Coverage before style.
type: doctrine
tags: [eos]
id: DOC-DOCS-012
statement: Coverage before style.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [publishes_docs]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0326]
review: 2028-04
lifecycle: active
verification_refs: [packs/docs-dx/CHECKS.md]
migration_sources: [packs/docs-dx/PACK.md:defaults:006]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D6]
---

# DOC-DOCS-012

The `statement` field is the canonical standing proposition.

## Reasoning and limits

When attention is scarce, a missing
install or deployment instruction outranks every style finding.
Practitioners rate absence as both the most damaging and the most
frequent documentation problem, ahead of prose quality (EV-0326).
Reason: a linter that consumes the attention which would have written
the missing runbook is a net loss. Scope note: that is perception data
from 146 practitioners across two surveys, a ranking of felt pain
rather than a measured defect rate.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/docs-dx/PACK.md:defaults:006`, lines 243-250, SHA-256 `54ee3dfd47cabdd7a74644a0dfb34bfce679135e70cf4522b3e05154dbf85fe1`.
