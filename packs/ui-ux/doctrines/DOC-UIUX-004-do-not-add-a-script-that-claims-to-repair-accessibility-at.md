---
summary: Do not add a script that claims to repair accessibility at runtime.
type: doctrine
tags: [eos]
id: DOC-UIUX-004
statement: Do not add a script that claims to repair accessibility at runtime.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [has_user_interface]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0237]
review: on-change-of:WCAG-2.2
lifecycle: active
verification_refs: [packs/ui-ux/CHECKS.md]
migration_sources: [packs/ui-ux/PACK.md:requirements:004]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B5]
---

# DOC-UIUX-004

The `statement` field is the canonical standing proposition.

## Reasoning and limits

No script that claims to repair accessibility at runtime, and no assistive-technology sniffing (EV-0237). C12 settles it against a written list of vendor names and runtime-patching patterns kept beside the scan and reviewed when it changes "no overlay" with no list behind it is an assertion rather than a check, and a scan of built output finds nothing it was not told to look for.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/ui-ux/PACK.md:requirements:004`, lines 134-147, SHA-256 `64eba8a0e0184a3ed910325f14fc12970606adfb9428227dab3978fcb073b1c5`.
