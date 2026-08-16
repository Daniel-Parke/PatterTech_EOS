---
summary: A three-bucket allowlist keyed on identifiers, with the reason written next to each bucket.
type: doctrine
tags: [eos]
id: DOC-LEGAL-008
statement: A three-bucket allowlist keyed on identifiers, with the reason written next to each bucket.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [adds_dependency]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0342]
review: 2027-04
lifecycle: active
verification_refs: [packs/legal-licensing/CHECKS.md]
migration_sources: [packs/legal-licensing/PACK.md:defaults:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D1]
---

# DOC-LEGAL-008

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Freely usable, usable under stated
conditions, never. Decided once, applied mechanically, enforced in CI.
Reason: high volume and low stakes per item is exactly what a standing
verdict is for (EV-0342). Import the shape, not the
categories: the published example bans a licence family outright to
keep a promise about permissive releases, and a venture that makes no
such promise inherits a rule that blocks safe dependencies. See
`packs/legal-licensing/references/LICENCE_CLASSES.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/legal-licensing/PACK.md:defaults:001`, lines 242-250, SHA-256 `f24aae1f2942a439bee191a300d5ba9a63f1a30be69f57e7ccb36fe695fbb13b`.
