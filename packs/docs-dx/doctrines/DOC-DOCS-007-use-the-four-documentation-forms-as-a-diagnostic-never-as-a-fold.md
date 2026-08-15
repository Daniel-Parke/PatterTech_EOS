---
summary: Use the four documentation forms as a diagnostic, never as a folder layout.
type: doctrine
tags: [eos]
id: DOC-DOCS-007
statement: Use the four documentation forms as a diagnostic, never as a folder layout.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [publishes_docs]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0322, EV-0323]
review: 2028-04
lifecycle: active
verification_refs: [packs/docs-dx/CHECKS.md]
migration_sources: [packs/docs-dx/PACK.md:defaults:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D1]
---

# DOC-DOCS-007

The `statement` field is the canonical standing proposition.

## Reasoning and limits

When a page has become confusing, ask which of
tutorial, how-to, reference and explanation it is trying to be, and
split it (EV-0322). Reason: the load-bearing claim is that mixing forms
inside one page is what makes it unusable, because a reader trying to
get something done cannot use a page that keeps stopping to teach. The
framework has no research base beyond its author's practice, and four
empty directories on day one produce a tutorial nobody wrote (EV-0323).
See `packs/docs-dx/refs/DOC_FORMS.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/docs-dx/PACK.md:defaults:001`, lines 199-207, SHA-256 `f51d4dd6cf09de0243a329e48759ec72c153a4db8386e4b21e4d15bb879f0444`.
