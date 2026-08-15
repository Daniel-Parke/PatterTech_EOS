---
summary: No dependency enters without a recorded licence expression, and absence is a blocking finding.
type: doctrine
tags: [eos]
id: DOC-LEGAL-002
statement: No dependency enters without a recorded licence expression, and absence is a blocking finding.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [adds_dependency]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0338, EV-0348]
review: 2027-04
lifecycle: active
verification_refs: [packs/legal-licensing/CHECKS.md]
migration_sources: [packs/legal-licensing/PACK.md:requirements:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B2]
---

# DOC-LEGAL-002

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`adds_dependency`, `vendors_code`. Each
component in the inventory carries an SPDX expression. A value of
`NOASSERTION`, `NONE` or empty blocks the merge until it is resolved or
named in `LICENCE_DECISION.md` (EV-0338). The entry
names the path, states that no licence was found, and states that this
means exclusive copyright rather than an unknown to fill in later
(EV-0348). Authority: binding. Basis: standard.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/legal-licensing/PACK.md:requirements:002`, lines 149-156, SHA-256 `0b3b2dfa7ad32951ca803f69abea4a8c38bdc902e7686ffc4f7dc6d58bb03f40`.
