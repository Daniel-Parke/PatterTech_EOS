---
summary: Animation stays on the compositor whitelist.
type: doctrine
tags: [eos]
id: DOC-HOUSE-003
statement: Animation stays on the compositor whitelist.
kind: doctrine
authority: preference
basis: standard
evidence_grade: observational
scope: estate
applies_when: [adopts_pattertech_house]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0395, EV-0396]
review: on-change-of:WCAG-2.2
lifecycle: active
verification_refs: [packs/pattertech-house/CHECKS.md]
migration_sources: [packs/pattertech-house/PACK.md:requirements:003]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [H3]
---

# DOC-HOUSE-003

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`adopts_pattertech_house`. Transform, opacity, one-shot filters, and
shadow transitions on small elements. The one sanctioned exception is
the heading sweep, which is a one-shot and is named as such. Prevents a
page that looks calm and repaints every frame
(EV-0395), and prevents layer promotion being sprinkled
rather than budgeted (EV-0396). Basis: standard, from
engine guidance. Scope note: compositing rules are engine-specific and
change, so the whitelist is conservative rather than exact, and a
measurement on target hardware beats it.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/pattertech-house/PACK.md:requirements:003`, lines 113-122, SHA-256 `33aef59d7cb071fd0b5b34a4ad1c9dcc8e14cbe633c64f2f38bf9fd91548ab25`.
