---
summary: A README answers five questions: what it is, why it exists, how to use it, what state it is in, and where to go next.
type: doctrine
tags: [eos]
id: DOC-DOCS-008
statement: A README answers five questions: what it is, why it exists, how to use it, what state it is in, and where to go next.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [publishes_docs]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0329]
review: 2028-04
lifecycle: active
verification_refs: [packs/docs-dx/CHECKS.md]
migration_sources: [packs/docs-dx/PACK.md:defaults:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D2]
---

# DOC-DOCS-008

The `statement` field is the canonical standing proposition.

## Reasoning and limits

The wording and
the order sit in `packs/docs-dx/references/DOC_FORMS.md`, which owns the set,
and C-18 checks against that file rather than against this sentence.
Reason: sampled READMEs cluster on what and how and systematically omit
why and state, which are the questions a reader cannot answer any other
way (EV-0329). Scope note: that is a descriptive study of open-source
READMEs sampled before 2018, and it never linked section presence to an
outcome.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/docs-dx/PACK.md:defaults:002`, lines 209-217, SHA-256 `4a52627aaca8314dd0a148545ae37ecf05738577bbaa85f70525eb8275821e10`.
