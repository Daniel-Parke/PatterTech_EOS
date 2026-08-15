---
summary: An aggregate boundary is a transactional consistency boundary and nothing else.
type: doctrine
tags: [eos]
id: DOC-BLM-004
statement: An aggregate boundary is a transactional consistency boundary and nothing else.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [encodes_domain_rule]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0269, EV-0270]
review: 2027-09
lifecycle: active
verification_refs: [packs/business-logic-modelling/CHECKS.md]
migration_sources: [packs/business-logic-modelling/PACK.md:defaults:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D2]
---

# DOC-BLM-004

The `statement` field is the canonical standing proposition.

## Reasoning and limits

One aggregate per transaction, references to other
aggregates by identity only, small clusters preferred (EV-0269), and the
boundary written up in the field set of
`packs/business-logic-modelling/refs/BOUNDARY_WRITE_UP.md` (EV-0270).
Reason: the field set makes the design reviewable, and a long list of
corrective policies is the tell that logic leaked out of the boundary.
Both sources are consulting experience with no measurement behind them.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/business-logic-modelling/PACK.md:defaults:002`, lines 136-143, SHA-256 `71f866f418190d60618690c857664d39c939ec0a39815e4aaa920ec946305d35`.
