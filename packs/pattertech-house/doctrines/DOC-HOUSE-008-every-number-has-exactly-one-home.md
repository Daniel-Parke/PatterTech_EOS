---
summary: Every number has exactly one home.
type: doctrine
tags: [eos]
id: DOC-HOUSE-008
statement: Every number has exactly one home.
kind: doctrine
authority: preference
basis: decision
evidence_grade: observational
scope: estate
applies_when: [adopts_pattertech_house]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0027, EV-0030, EV-0065, EV-0232, EV-0234, EV-0236, EV-0239, EV-0389, EV-0390, EV-0391, EV-0392, EV-0393, EV-0394, EV-0395, EV-0396, EV-0397, EV-0398, EV-0399, EV-0400, EV-0402]
review: on-change-of:WCAG-2.2
lifecycle: active
verification_refs: [packs/pattertech-house/CHECKS.md]
migration_sources: [packs/pattertech-house/PACK.md:requirements:008]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [H8]
---

# DOC-HOUSE-008

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`adopts_pattertech_house`. All house alphas, durations, duty cycles,
measures, layer counts and weight budgets live in
`packs/pattertech-house/refs/BUDGETS.md` and are cited, never restated.
Prevents the failure that produced this pack: two documents carrying the
same budget, drifting, and an agent picking whichever it read last.
Basis: decision.

**The conduit contradiction, resolved.** The v1 archive held one number
twice: `archive/v1-final:doctrine/web-design/foundations/LIGHT.md` and
`archive/v1-final:doctrine/web-design/foundations/MOTION.md` both stated a
conduit duty cycle of eighteen seconds or longer. The newer argued
ruling in WG-WEB-005, recorded against the v4 recalibration, relaxed it
after the verdict that v3 sat on the wrong side of the line between
elegant and invisible. The newer ruling wins, the relaxed figure is
written once in `packs/pattertech-house/refs/BUDGETS.md`, and the older
number is history.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/pattertech-house/PACK.md:requirements:008`, lines 157-173, SHA-256 `b50ee3ea306eb13cd29a8d44bf7fd37a0f8149290308c0556287e9c452a0ce34`.
