---
summary: Figures are positioned from data.
type: doctrine
tags: [eos]
id: DOC-HOUSE-007
statement: Figures are positioned from data.
kind: doctrine
authority: preference
basis: local-observation
evidence_grade: observational
scope: estate
applies_when: [adopts_pattertech_house]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0391]
review: on-change-of:WCAG-2.2
lifecycle: active
verification_refs: [packs/pattertech-house/CHECKS.md]
migration_sources: [packs/pattertech-house/PACK.md:requirements:007]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [H7]
---

# DOC-HOUSE-007

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`has_figures`. Scales place
every node, no label or box overlaps a line, connectors join labels to
their nodes, no glow sits on a line, and at most one endpoint accent
marks the datum that matters. Prevents a figure that lies about where a
value sits, which no recall gain buys back
(EV-0391). Basis: local-observation. See
`packs/pattertech-house/wargames/WG-HOUSE-004-figure-austerity.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/pattertech-house/PACK.md:requirements:007`, lines 149-155, SHA-256 `bf0eca63ee36efd6d719c1b3b3ec08a2fa7a1a36b8ce90bfd1225ba62c7e88b9`.
