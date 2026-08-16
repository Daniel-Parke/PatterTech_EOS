---
summary: Reissue the session identifier whenever privilege changes.
type: doctrine
tags: [eos]
id: DOC-IDENT-007
statement: Reissue the session identifier whenever privilege changes.
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
migration_sources: [packs/identity-access/PACK.md:requirements:003]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B3]
---

# DOC-IDENT-007

The `statement` field is the canonical standing proposition.

## Reasoning and limits

An identity token is never accepted as an access token, and a session identifier is never forwarded as a bearer credential to another service. Session identifiers come from a cryptographic generator, are re-issued whenever the privilege level changes, and are invalidated on the server at logout. Prevents: an authentication system with no audience check where it matters, and a session that survives its own logout (OpenID Connect Core, RFC 9700, OWASP session guidance).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/identity-access/PACK.md:requirements:003`, lines 138-148, SHA-256 `4929467b35f7b06700c642a4c9ba4b7aa184b037d013628917b6993b4dfc18b5`.
