---
summary: No user-facing sentence is assembled by string concatenation.
type: doctrine
tags: [eos]
id: DOC-WRIT-001
statement: No user-facing sentence is assembled by string concatenation.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [writes_user_facing_text]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0442, EV-0444]
review: on-change-of:CLDR-plural-categories
lifecycle: active
verification_refs: [packs/writing-content/CHECKS.md]
migration_sources: [packs/writing-content/PACK.md:requirements:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B1]
---

# DOC-WRIT-001

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`writes_user_facing_text`. One message, one message id, with any
variation selected inside the message
(EV-0442, EV-0444). Prevents the one
localisation defect a translator cannot repair downstream, because word
order, agreement and clause structure are decided by the source code
rather than by the language. Basis: standard. Binds on the
hard-to-reverse leg: the defect is structural, it is nearly free to
avoid beforehand, and after the fact it costs a rewrite of every call
site.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/writing-content/PACK.md:requirements:001`, lines 154-163, SHA-256 `340d45382e8fd34023cec5009ea7051bf9c822999bb6689c4f13b945e9b33aa6`.
