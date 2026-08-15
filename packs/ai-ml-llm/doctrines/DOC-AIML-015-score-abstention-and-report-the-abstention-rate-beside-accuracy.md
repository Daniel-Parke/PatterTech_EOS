---
summary: Score abstention, and report the abstention rate beside accuracy.
type: doctrine
tags: [eos]
id: DOC-AIML-015
statement: Score abstention, and report the abstention rate beside accuracy.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [calls_a_model]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0250]
review: 2027-02
lifecycle: active
verification_refs: [packs/ai-ml-llm/CHECKS.md]
migration_sources: [packs/ai-ml-llm/PACK.md:defaults:010]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D10]
---

# DOC-AIML-015

The `statement` field is the canonical standing proposition.

## Reasoning and limits

The output contract of a model-backed component includes a
way to decline, and the eval report carries the abstention rate as a
first-class field. Reason: a rubric that pays a guess the same as an
admission of uncertainty selects for confident error, which is the
actionable half of the hallucination argument (EV-0250), and a system
optimised without it goes fluently wrong. This is a default rather than
binding because EV-0250 is a theoretical argument from a model vendor
rather than an experiment, and it does not tell you the right threshold.
Override where the output has no defensible way to decline, and say so
in the report.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/ai-ml-llm/PACK.md:defaults:010`, lines 256-266, SHA-256 `cb82ff3d6147176d102a8adbbf186290d28aa400e4d896359c68d6f59c4417fc`.
