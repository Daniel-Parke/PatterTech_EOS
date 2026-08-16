---
summary: A remote update channel changes presentation and content, never capability.
type: doctrine
tags: [eos]
id: DOC-NAT-005
statement: A remote update channel changes presentation and content, never capability.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [ships_a_binary]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0372, EV-0377]
review: on-change-of:EN-301-549-v4-publication
lifecycle: active
verification_refs: [packs/native-client/CHECKS.md]
migration_sources: [packs/native-client/PACK.md:requirements:005]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B5]
---

# DOC-NAT-005

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`has_remote_update_channel`. Copy, styling, assets and
layout may ship out of band. Native code, native dependencies,
permissions, SDK levels and anything a reasonable person would call a
new feature may not. Prevents rejection or removal: the technical
boundary sits at native code (EV-0377) and the review rule sits
tighter still, at introducing or changing features (EV-0372).
Authority: binding. Basis: standard, taking the narrower of two
documented lines.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/native-client/PACK.md:requirements:005`, lines 163-171, SHA-256 `004d4a884dc1f66c59e5c2e35a352c4aef552c7ab772561b0b057c557ac9177b`.
