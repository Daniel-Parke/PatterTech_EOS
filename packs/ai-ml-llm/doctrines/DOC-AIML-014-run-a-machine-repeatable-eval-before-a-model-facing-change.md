---
summary: Run a machine-repeatable eval before a model-facing change ships.
type: doctrine
tags: [eos]
id: DOC-AIML-014
statement: Run a machine-repeatable eval before a model-facing change ships.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [calls_a_model]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0255]
review: 2027-02
lifecycle: active
verification_refs: [packs/ai-ml-llm/CHECKS.md]
migration_sources: [packs/ai-ml-llm/PACK.md:defaults:009]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D9]
---

# DOC-AIML-014

The `statement` field is the canonical standing proposition.

## Reasoning and limits

A prompt, model, retriever or decoding change goes through a
headless eval entry point at a recorded path, run against the acceptance
set, reporting a result. Reason: the alternative is the demo-driven
change, where someone tries six examples by hand, likes the sixth, and
ships a regression nobody can name, and an eval is an experiment that
has to be reported like one (EV-0255). This is a default rather than
binding because the failure it names is a quality regression a revert
undoes, and because no source measures that gating on an eval prevents
one. Override for a change no acceptance set covers, and record why.
Overriding does not soften B2 or B3: those govern any result offered as
acceptance, however it was produced. See
`packs/ai-ml-llm/wargames/WG-AIML-002-acceptance-evidence.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/ai-ml-llm/PACK.md:defaults:009`, lines 242-254, SHA-256 `f749fda1c6dcca784f2b52ac15a6ef9dd29291888261dc8b82014bbc6b2f1f14`.
