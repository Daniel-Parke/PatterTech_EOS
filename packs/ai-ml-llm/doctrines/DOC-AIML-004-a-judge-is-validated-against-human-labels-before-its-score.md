---
summary: A judge is validated against human labels before its score decides anything.
type: doctrine
tags: [eos]
id: DOC-AIML-004
statement: A judge is validated against human labels before its score decides anything.
kind: doctrine
authority: binding
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [calls_a_model]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0251, EV-0252, EV-0253]
review: 2027-02
lifecycle: active
verification_refs: [packs/ai-ml-llm/CHECKS.md]
migration_sources: [packs/ai-ml-llm/PACK.md:requirements:004]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B5]
---

# DOC-AIML-004

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Where a model grades output and the score selects between
candidates or gates a release, the judge is never the same model as the
one under test, pairwise protocols run both orderings with
order-inconsistent pairs reported as disagreement, and agreement against
a human-labelled sample is measured and reported. Where a family-mate
judge is unavoidable, the measured self-preference offset is reported
rather than assumed to be zero. Prevents a scoreboard that moves with
slot position and family loyalty: position bias varies by judge and by
task and is largest where the answers are close (EV-0252), and
self-recognition causally drives models to score their own output above
others' that humans rate equal (EV-0253). The roughly eighty per cent
judge-human agreement that makes judging defensible at all is a
general-chat number and does not transfer to domain correctness
(EV-0251). See
`packs/ai-ml-llm/wargames/WG-AIML-004-who-grades-the-output.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/ai-ml-llm/PACK.md:requirements:004`, lines 136-151, SHA-256 `4b15ac4d890f173073f6c4bfe32cab7110e4207b66bbc6b025969a32057f54bc`.
