---
summary: An eval run is reproducible without the network.
type: doctrine
tags: [eos]
id: DOC-AIML-013
statement: An eval run is reproducible without the network.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [calls_a_model]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0041, EV-0085, EV-0086, EV-0087, EV-0212, EV-0213, EV-0214, EV-0215, EV-0225, EV-0242, EV-0243, EV-0244, EV-0245, EV-0246, EV-0247, EV-0248, EV-0249, EV-0250, EV-0251, EV-0252, EV-0253, EV-0254, EV-0255, EV-0256, EV-0257, EV-0258, EV-0259, EV-0260, EV-0261, EV-0262, EV-0263, EV-0264, EV-0265, EV-0266, EV-0267, EV-0268]
review: 2027-02
lifecycle: active
verification_refs: [packs/ai-ml-llm/CHECKS.md]
migration_sources: [packs/ai-ml-llm/PACK.md:defaults:008]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [D8]
---

# DOC-AIML-013

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Two runs over
the same tree give the same accuracy and the same item count, achieved
by pinning the model id, fixing decoding parameters, recording the seed,
and holding recorded or stubbed responses for the offline path. Reason:
this one is a decision rather than a measured finding. A number nobody
can reproduce cannot be argued about, and a gate that costs real money
per run gets skipped. Override where the acceptance condition genuinely
needs live sampling, and report the run-to-run variance instead.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/ai-ml-llm/PACK.md:defaults:008`, lines 233-240, SHA-256 `041debf131a6981743f373965d266da7e410046531e3b828652d9c07c5e9f41c`.
