---
summary: Deny unless something permitted, and decide at one layer.
type: doctrine
tags: [eos]
id: DOC-IDENT-001
statement: Deny unless something permitted, and decide at one layer.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [authenticates_people]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0517, EV-0518, EV-0519, EV-0520, EV-0521, EV-0522, EV-0523, EV-0524, EV-0525, EV-0526, EV-0527, EV-0528, EV-0529, EV-0530, EV-0531]
review: 2029-02
lifecycle: active
verification_refs: [packs/identity-access/CHECKS.md]
migration_sources: [packs/identity-access/PACK.md:requirements:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B1]
---

# DOC-IDENT-001

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Every
request that reads or changes data resolves an authorisation decision
before it touches the data, and the decision is made on the server from
the authenticated identity, never from a value the caller supplied. The
check runs at one layer every request passes through, not per handler. A
decision that cannot be evaluated is a denial, not a gap. Predicate:
`authenticates_people`. Prevents: the largest measured defect class in
web software, whose named shapes are a missing check rather than a
clever bypass (OWASP Top 10:2025, OWASP authorization guidance). Getting
it right on most requests is the same as getting it wrong.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/identity-access/PACK.md:requirements:001`, lines 112-121, SHA-256 `f954480bd688664cd10b1d14e41f5cf2e61ed8a3b55362478703517f4273fdd5`.
