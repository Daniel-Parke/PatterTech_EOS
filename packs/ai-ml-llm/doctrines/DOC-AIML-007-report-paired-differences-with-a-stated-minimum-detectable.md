---
summary: Report paired differences with a stated minimum detectable effect.
type: doctrine
tags: [eos]
id: DOC-AIML-007
statement: Report paired differences with a stated minimum detectable effect.
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
migration_sources: [packs/ai-ml-llm/PACK.md:defaults:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D2]
---

# DOC-AIML-007

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Compare two variants on the same items, name the pairing in
the report, cluster the standard error where items share a source, and
state what difference the set can detect at its size (EV-0255). Reason:
a gate that cannot say what it can detect is a coin flip in a suit.
Override with a recorded reason only where the item set genuinely
differs between arms.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/ai-ml-llm/PACK.md:defaults:002`, lines 180-186, SHA-256 `5cce3685b1fd9aba9429dc837c90ca45df29166f40aca5dacdad331fe9d25da1`.
