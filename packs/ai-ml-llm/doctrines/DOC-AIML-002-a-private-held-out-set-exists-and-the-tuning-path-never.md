---
summary: A private held-out set exists, and the tuning path never reads it.
type: doctrine
tags: [eos]
id: DOC-AIML-002
statement: A private held-out set exists, and the tuning path never reads it.
kind: doctrine
authority: binding
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [calls_a_model]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0257, EV-0258, EV-0267]
review: 2027-02
lifecycle: active
verification_refs: [packs/ai-ml-llm/CHECKS.md]
migration_sources: [packs/ai-ml-llm/PACK.md:requirements:002]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B3]
---

# DOC-AIML-002

The `statement` field is the canonical standing proposition.

## Reasoning and limits

The venture holds an acceptance set the providers have never seen,
split so that the portion used to select prompts is separate from the
portion used to accept them, and no prompt-selection or optimiser code
reads the held-out file. Prevents scoring your own homework: accuracy
dropped by up to eight points on a fresh set matched for style and
difficulty, with systematic overfitting across whole model families
(EV-0257), and a public leaderboard distorts under the same pressure,
with relative gains of up to 112 per cent on the arena distribution from
modest arena-shaped data (EV-0258). The same split is the design choice
behind the public practice set and private official set of a published
safety benchmark (EV-0267). Scope note: the eight-point figure is
grade-school arithmetic on 2024 models.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/ai-ml-llm/PACK.md:requirements:002`, lines 103-115, SHA-256 `184e82152eb75cd257ba930126bf6bca8871297eb74b46203b1c35bf17b69d49`.
