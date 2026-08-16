---
summary: Non-web accessibility conformance is stated per screen, declared in code, and gated by an automated audit with a written verdict on every undecided item.
type: doctrine
tags: [eos]
id: DOC-NAT-006
statement: Non-web accessibility conformance is stated per screen, declared in code, and gated by an automated audit with a written verdict on every undecided item.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [has_native_ui]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0027, EV-0235, EV-0370, EV-0371, EV-0387, EV-0388]
review: on-change-of:EN-301-549-v4-publication
lifecycle: active
verification_refs: [packs/native-client/CHECKS.md]
migration_sources: [packs/native-client/PACK.md:requirements:006]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B6]
---

# DOC-NAT-006

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`has_native_ui`. The unit of conformance is a
screen, not a page (EV-0370), and the reviewable artefact is the
semantics declaration, not a screenshot (EV-0387). The audit
runs inside the platform test runner over every screen and fails the
build on any violation (EV-0388); the verdict file's entry count
equals the audit's undecided count. Where EN 301 549 applies, the
target is clause 11 plus its WCAG mapping (EV-0371, EV-0027),
which adds assistive-technology interoperability and user preference
support. Prevents web conformance language being waved at an app, and a
green audit being read as proof, which the web census warns against
directly (EV-0235). Authority: binding, and the audit kept it there
because the failure is a person locked out of the product rather than a
line of text to correct. Basis: standard. See
`packs/native-client/wargames/WG-NAT-004-a11y-profile.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/native-client/PACK.md:requirements:006`, lines 173-188, SHA-256 `fd5e33ea49609f670d432dfef0e5d764a3986a89bb93098c1ce2b75101daee20`.
