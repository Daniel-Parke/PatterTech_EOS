---
summary: Delegate authentication to a provider rather than storing passwords.
type: doctrine
tags: [eos]
id: DOC-IDENT-014
statement: Delegate authentication to a provider rather than storing passwords.
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
migration_sources: [packs/identity-access/PACK.md:defaults:004]
generated_by: tools.eos.migrate_doctrines
---

# DOC-IDENT-014

The `statement` field is the canonical standing proposition.

## Reasoning and limits

The provider ships the parts that are tedious and easy to get wrong, and the specification names them

RFC 9700, NIST SP 800-63B-4

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/identity-access/PACK.md:defaults:004`, lines 181-181, SHA-256 `ee36d04d67e80ee019c60fad7c39b8120551da94549f096813ab572a32ddb50e`.
