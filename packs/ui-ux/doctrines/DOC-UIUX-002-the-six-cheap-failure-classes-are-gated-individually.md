---
summary: The six cheap failure classes are gated individually.
type: doctrine
tags: [eos]
id: DOC-UIUX-002
statement: The six cheap failure classes are gated individually.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [has_user_interface]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0235, EV-0236]
review: on-change-of:WCAG-2.2
lifecycle: active
verification_refs: [packs/ui-ux/CHECKS.md]
migration_sources: [packs/ui-ux/PACK.md:requirements:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B3]
---

# DOC-UIUX-002

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`has_web_ui`. Contrast, image alternative text, form labels, empty
links, empty buttons and declared page language each get their own
assertion (EV-0235, EV-0236); C7 is those six assertions and settles
it. Prevents the defects that the 2026 census
found on the majority of home pages shipping again here. Basis:
standard. Binds because each of the six stops somebody using the
surface at all, which is serious whether or not it is also unlawful.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/ui-ux/PACK.md:requirements:002`, lines 116-123, SHA-256 `14ec3b382d21f53312881d21f61ad20046bb7b81f5322bf93e037ec906b56248`.
