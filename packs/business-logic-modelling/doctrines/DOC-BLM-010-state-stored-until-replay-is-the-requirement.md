---
summary: State-stored until replay is the requirement.
type: doctrine
tags: [eos]
id: DOC-BLM-010
statement: State-stored until replay is the requirement.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [encodes_domain_rule]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0276]
review: 2027-09
lifecycle: active
verification_refs: [packs/business-logic-modelling/CHECKS.md]
migration_sources: [packs/business-logic-modelling/PACK.md:defaults:008]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D8]
---

# DOC-BLM-010

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Event sourcing
charges in three places: replay must not re-fire external effects, must
not re-read external data at today's values, and old event shapes must
stay readable (EV-0276). Reason: audit alone is a bad reason to adopt
it, because a log is cheaper.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/business-logic-modelling/PACK.md:defaults:008`, lines 184-188, SHA-256 `09c22c39277bdfa390753e22967037c5ab2edf5f296a8afa7f2cf2cc0b5cf799`.
