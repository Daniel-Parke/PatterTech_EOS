---
summary: Do not infer assistive-technology use without the person's consent.
type: doctrine
tags: [eos]
id: DOC-UIUX-005
statement: Do not infer assistive-technology use without the person's consent.
kind: doctrine
authority: binding
basis: law
evidence_grade: observational
scope: estate
applies_when: [handles_personal_data]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0237]
review: on-change-of:WCAG-2.2
lifecycle: active
verification_refs: [packs/ui-ux/CHECKS.md]
migration_sources: [packs/ui-ux/PACK.md:requirements:004]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B5]
---

# DOC-UIUX-005

The `statement` field is the canonical standing proposition.

## Reasoning and limits

No script that claims to repair accessibility at runtime, and no assistive-technology sniffing (EV-0237). Prevents a non-conforming product being marketed as conforming, and prevents disability status being detected without consent. law on the sniffing half, because inferring assistive-technology use infers disability, which is special-category personal data that `packs/security-privacy` B5 already binds.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/ui-ux/PACK.md:requirements:004`, lines 134-147, SHA-256 `64eba8a0e0184a3ed910325f14fc12970606adfb9428227dab3978fcb073b1c5`.
