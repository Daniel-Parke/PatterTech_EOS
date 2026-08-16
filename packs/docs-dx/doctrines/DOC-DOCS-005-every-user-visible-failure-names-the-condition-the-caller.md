---
summary: Every user-visible failure names the condition, the caller-relevant identity, and what to do next.
type: doctrine
tags: [eos]
id: DOC-DOCS-005
statement: Every user-visible failure names the condition, the caller-relevant identity, and what to do next.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [publishes_docs]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0175, EV-0327, EV-0328]
review: 2028-04
lifecycle: active
verification_refs: [packs/docs-dx/CHECKS.md]
migration_sources: [packs/docs-dx/PACK.md:requirements:005]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B5]
---

# DOC-DOCS-005

The `statement` field is the canonical standing proposition.

## Reasoning and limits

The message says what
was wrong, shows or names the offending input, and points at the
accepted alternative. Detail beyond that goes behind an explicit
request rather than inline (EV-0328). Which failures a caller may tell
apart is an interface decision and is declared, not inferred
(EV-0175). Reason: the dead stop. A user does the wrong thing, gets
`error` and exit 1, and cannot tell whether they mistyped, hit a bug or
lack a permission. Authority: default. Basis: empirical-evidence. Scope
note: the read-rate and time-to-fix evidence is an eye-tracking study
of 56 students fixing planted Java defects in Eclipse in 2017
(EV-0327). The direction transfers, the percentages are not a target,
and nothing there tested an agent reader. See
`packs/docs-dx/wargames/WG-DOCS-004-failure-messages.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/docs-dx/PACK.md:requirements:005`, lines 169-182, SHA-256 `021ebbf57934bba57c2760c3482f5768ae8089df93c4fe54f63a278433f3038f`.
