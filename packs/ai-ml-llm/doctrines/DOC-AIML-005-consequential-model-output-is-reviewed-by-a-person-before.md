---
summary: Consequential model output is reviewed by a person before it takes effect.
type: doctrine
tags: [eos]
id: DOC-AIML-005
statement: Consequential model output is reviewed by a person before it takes effect.
kind: doctrine
authority: binding
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [calls_a_model]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0214, EV-0215, EV-0251, EV-0267]
review: 2027-02
lifecycle: active
verification_refs: [packs/ai-ml-llm/CHECKS.md]
migration_sources: [packs/ai-ml-llm/PACK.md:requirements:005]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B7]
---

# DOC-AIML-005

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Where output moves money, changes access, contacts a customer,
alters production data or produces a legal, medical or safety claim, a
person approves it before it lands. The action classes and their floors
are ruled by `kernel/GUARD_SPEC.md` and `kernel/POLICY_SPEC.md`, and no
eval score lowers them. Prevents treating an aggregate pass rate as
permission for each individual case: judge-human agreement around eighty
per cent is far too coarse to gate a safety property (EV-0251), a good
safety grade is evidence about one prompt distribution (EV-0267), and
adaptive attackers break defences that pass static evaluation (EV-0214,
EV-0215). This requirement rests on the guard decision as much as on the
measurements, and the ADR-0008 audit left it alone for that reason:
approval for a consequential external action is a safety floor, and a
floor stays binding whatever its basis field says.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/ai-ml-llm/PACK.md:requirements:005`, lines 153-166, SHA-256 `abbe3e2edb3fc49d3f1d16043279c76e19bbb26d46b7149ebdc2f3479db5be86`.
