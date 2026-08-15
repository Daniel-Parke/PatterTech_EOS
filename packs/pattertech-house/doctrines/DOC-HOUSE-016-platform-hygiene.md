---
summary: Platform hygiene.
type: doctrine
tags: [eos]
id: DOC-HOUSE-016
statement: Platform hygiene.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [adopts_pattertech_house]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0398, EV-0399]
review: on-change-of:WCAG-2.2
lifecycle: active
verification_refs: [packs/pattertech-house/CHECKS.md]
migration_sources: [packs/pattertech-house/PACK.md:defaults:008]
generated_by: tools.eos.migrate_doctrines
---

# DOC-HOUSE-016

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Line-break quality is a hint rather than a
  dependency, and balance belongs on short display lines rather than
  paragraphs (EV-0399). Animated custom properties are
  registered once in the token layer, because an unregistered angle or
  colour is untyped and the animation silently does nothing
  (EV-0398).

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/pattertech-house/PACK.md:defaults:008`, lines 210-215, SHA-256 `d8e2c1a6f743fcde25538f5333c5f6bb723b07b62b4f92fdf10d5c3c1bec6186`.
