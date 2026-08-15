---
summary: No readability formula gates a merge, a release or a review.
type: doctrine
tags: [eos]
id: DOC-WRIT-010
statement: No readability formula gates a merge, a release or a review.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: estate
applies_when: [writes_user_facing_text]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0436]
review: on-change-of:CLDR-plural-categories
lifecycle: active
verification_refs: [packs/writing-content/CHECKS.md]
migration_sources: [packs/writing-content/PACK.md:defaults:006]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B10]
---

# DOC-WRIT-010

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`writes_user_facing_text`. A score may be reported on a diff and may
never block one. Formulas measure sentence length and syllable counts,
which sit downstream of difficulty rather than being difficulty
(EV-0436). Prevents copy being chopped into fragments
to satisfy a number while the reader learns nothing new. Basis:
decision. The study behind the doubt is narrow, and the ruling is the
estate's, not the study's. Failed the basis leg. A venture that wants
to gate on a formula now records why, which is a fair place for that
argument to happen.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/writing-content/PACK.md:defaults:006`, lines 264-273, SHA-256 `d5e66123c8aef44f1ec168d8522311ed7439ca354bf09314fde5dc2609f7167b`.
