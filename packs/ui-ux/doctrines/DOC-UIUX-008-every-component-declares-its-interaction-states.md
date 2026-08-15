---
summary: Every component declares its interaction states.
type: doctrine
tags: [eos]
id: DOC-UIUX-008
statement: Every component declares its interaction states.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [has_user_interface]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0027, EV-0232, EV-0234]
review: on-change-of:WCAG-2.2
lifecycle: active
verification_refs: [packs/ui-ux/CHECKS.md]
migration_sources: [packs/ui-ux/PACK.md:defaults:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B7]
---

# DOC-UIUX-008

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`has_user_interface`. Focus, hover, active, disabled, loading and error
are named in an exported states manifest, one entry per component per
state, and C9 walks that manifest with one render assertion per entry.
A state a component cannot enter is declared absent in the manifest
with a reason rather than left out of it, because a missing entry and
a deliberate omission are indistinguishable to the walk. Prevents a
control that gives no sign it is focused, busy or unavailable, which is
affordance a restrained visual style removed and never paid back. The
full six is an estate decision taken on that reasoning (EV-0234,
EV-0232, both weak). Basis: decision. Failed the basis leg on those two
weak sources.
Focus visibility does not move with it: it is a WCAG criterion
(EV-0027) and C8 asserts it under B4.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/ui-ux/PACK.md:defaults:002`, lines 183-196, SHA-256 `7a94869d80b621b584d5d4db0e9f514abb036c7049cc1fc27a8896908c067dd5`.
