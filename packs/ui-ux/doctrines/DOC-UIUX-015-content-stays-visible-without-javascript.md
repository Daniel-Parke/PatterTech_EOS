---
summary: Content stays visible without JavaScript.
type: doctrine
tags: [eos]
id: DOC-UIUX-015
statement: Content stays visible without JavaScript.
kind: doctrine
authority: default
basis: standard
evidence_grade: observational
scope: estate
applies_when: [has_user_interface]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0027, EV-0028, EV-0029, EV-0030, EV-0062, EV-0063, EV-0064, EV-0065, EV-0066, EV-0067, EV-0103, EV-0104, EV-0227, EV-0228, EV-0229, EV-0230, EV-0232, EV-0234, EV-0235, EV-0236, EV-0237, EV-0238, EV-0239, EV-0240, EV-0241]
review: on-change-of:WCAG-2.2
lifecycle: active
verification_refs: [packs/ui-ux/CHECKS.md]
migration_sources: [packs/ui-ux/PACK.md:defaults:009]
generated_by: tools.eos.migrate_doctrines
---

# DOC-UIUX-015

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Reveal patterns hide
  content only where scripting is known to be on.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/ui-ux/PACK.md:defaults:009`, lines 230-231, SHA-256 `c53268e5cdeecb3e1b1fc258f4f182796422c178b928bef688a1cb6051946546`.
