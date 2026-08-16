---
summary: The claim is evidenced by a real-browser run with pinned tags, plus a written verdict on every incomplete.
type: doctrine
tags: [eos]
id: DOC-UIUX-007
statement: The claim is evidenced by a real-browser run with pinned tags, plus a written verdict on every incomplete.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [has_user_interface]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0236]
review: on-change-of:WCAG-2.2
lifecycle: active
verification_refs: [packs/ui-ux/CHECKS.md]
migration_sources: [packs/ui-ux/PACK.md:defaults:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B2]
---

# DOC-UIUX-007

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`has_web_ui`. Automated
checks run in a real browser engine, rule tags pinned to WCAG 2.2 A and
AA, zero violations, and each `incomplete` result carries a human
verdict in a named file (EV-0236). Prevents a green build being read as
proof, and prevents best-practice rules being smuggled in as
conformance. Basis: decision. Failed the basis leg: the research graded
the pinned real-browser run a default and this pack promoted it, which
the Open questions section has always said. The conformance claim keeps
its evidence route regardless, because C5 is what settles B1 and C5 is
the pinned real-browser run. What became a default is the zero-violation
gate and the written verdict on every incomplete.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/ui-ux/PACK.md:defaults:001`, lines 170-181, SHA-256 `a4c17a26b6dee068db85bc79e3f1567f97065e31026e5256773ad686e27009d0`.
