---
summary: A constraint expressible in the constructor or the type is expressed there.
type: doctrine
tags: [eos]
id: DOC-BLM-011
statement: A constraint expressible in the constructor or the type is expressed there.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [encodes_domain_rule]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0285]
review: 2027-09
lifecycle: active
verification_refs: [packs/business-logic-modelling/CHECKS.md]
migration_sources: [packs/business-logic-modelling/PACK.md:defaults:009]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D9]
---

# DOC-BLM-011

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`encodes_domain_rule`. A value that cannot legally
exist cannot be constructed, and narrowing happens at the boundary as
early as possible, so nothing downstream re-checks and nothing forgets
(EV-0285). A separate `validate` or `is_valid` method a caller may skip
does not satisfy it. Reason: scattered checking is how inconsistent
state gets in. This is a default rather than binding because EV-0285 is
a practitioner essay whose own author states it as an ideal, and because
the failure it names is a structural weakness rather than a serious or
irreversible event. Where the language cannot restrict construction, a
constructor-enforced value object is the equivalent; where neither is
available, record what checks instead.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/business-logic-modelling/PACK.md:defaults:009`, lines 190-201, SHA-256 `639b178ac296f18f049ea04d450158c1990ac4df2f738d49557f635c4a99a650`.
