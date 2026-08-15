---
summary: An authorisation change ships with the refusal that proves it.
type: doctrine
tags: [eos]
id: DOC-IDENT-010
statement: An authorisation change ships with the refusal that proves it.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [changes_authorisation_rule]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0517, EV-0518, EV-0519, EV-0520, EV-0521, EV-0522, EV-0523, EV-0524, EV-0525, EV-0526, EV-0527, EV-0528, EV-0529, EV-0530, EV-0531]
review: 2029-02
lifecycle: active
verification_refs: [packs/identity-access/CHECKS.md]
migration_sources: [packs/identity-access/PACK.md:requirements:005]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B5]
---

# DOC-IDENT-010

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Adding or changing a permission, a role, a policy or a tenant scope
lands with at least one test that the wrong actor is refused: the other
tenant's identifier returns nothing, the reader cannot write, the
support view cannot reach what it was not opened for. Predicate:
`changes_authorisation_rule`. Prevents: a permission model tested only
from the inside, which is how a model passes every test it has and still
lets the wrong person in (OWASP Top 10:2025).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/identity-access/PACK.md:requirements:005`, lines 162-169, SHA-256 `a501538dbd2bef9e0391b69116aea5a89d26efade933d706d3b53f4e7a766342`.
