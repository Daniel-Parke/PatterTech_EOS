---
summary: Plural and gender selection resolves per locale through CLDR categories, never from the English pair.
type: doctrine
tags: [eos]
id: DOC-WRIT-002
statement: Plural and gender selection resolves per locale through CLDR categories, never from the English pair.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [ships_second_locale]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0443]
review: on-change-of:CLDR-plural-categories
lifecycle: active
verification_refs: [packs/writing-content/CHECKS.md]
migration_sources: [packs/writing-content/PACK.md:requirements:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B2]
---

# DOC-WRIT-002

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`ships_second_locale`. The
category `one` means "behaves like one in this language" and is not the
number one (EV-0443). Prevents a locale with four
plural forms being served two, and prevents a hardcoded switch on six
tags that is already wrong for some locales. Basis: standard. Binds for
the same reason as B1: the English pair is baked into the source, and
unpicking it is the rewrite.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/writing-content/PACK.md:requirements:002`, lines 165-172, SHA-256 `d910807587130d1aa3efc5629cd25acdeb594b9e05e149f940ccc6b3b9a637b3`.
