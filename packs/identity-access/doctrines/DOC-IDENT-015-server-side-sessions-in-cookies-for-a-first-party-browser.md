---
summary: Server-side sessions in cookies for a first-party browser surface; tokens for anything else.
type: doctrine
tags: [eos]
id: DOC-IDENT-015
statement: Server-side sessions in cookies for a first-party browser surface; tokens for anything else.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [authenticates_people]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0517, EV-0518, EV-0519, EV-0520, EV-0521, EV-0522, EV-0523, EV-0524, EV-0525, EV-0526, EV-0527, EV-0528, EV-0529, EV-0530, EV-0531]
review: 2029-02
lifecycle: active
verification_refs: [packs/identity-access/CHECKS.md]
migration_sources: [packs/identity-access/PACK.md:defaults:005]
generated_by: tools.eos.migrate_doctrines
---

# DOC-IDENT-015

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Session credentials do not belong where page script can read them

OWASP session guidance

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/identity-access/PACK.md:defaults:005`, lines 182-182, SHA-256 `e2e1e70b437fb0f07e621def1e9e4e7c87a4443cbb10f62b8282f5a550a016c4`.
