---
summary: Secret protection is layered and audited.
type: doctrine
tags: [eos]
id: DOC-SEC-004
statement: Secret protection is layered and audited.
kind: doctrine
authority: binding
basis: decision
evidence_grade: observational
scope: estate
applies_when: [holds_credentials]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0220, EV-0221, EV-0222]
review: on-change-of:EV-0213
lifecycle: active
verification_refs: [packs/security-privacy/CHECKS.md]
migration_sources: [packs/security-privacy/PACK.md:requirements:004]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B4]
accepted_adr: ADR-0012
---

# DOC-SEC-004

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Credential files and
secret environment variables are named explicitly in the deny list;
there is no useful built-in default, so unnamed means unprotected
(EV-0220). Secret detection runs before the commit and again on the
push path (EV-0221, EV-0222). Any bypass carries a stated reason and
leaves an audit record. Emission of key material outside the sanctioned
store is a non-waivable deny in `kernel/GUARD_SPEC.md`. Predicate:
`holds_credentials`. Prevents: a leaked credential that rotation cannot
catch up with, because history is public the moment it is pushed.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/security-privacy/PACK.md:requirements:004`, lines 135-143, SHA-256 `9e33326eccbef67af9393a56b69f956bff8700c15f0b5d3196cfae700580449e`.
