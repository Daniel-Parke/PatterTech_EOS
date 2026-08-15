---
summary: A diff-aware machine gate runs before every merge.
type: doctrine
tags: [eos]
id: DOC-COD-006
statement: A diff-aware machine gate runs before every merge.
kind: doctrine
authority: binding
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [edits_source]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0069, EV-0070, EV-0181]
review: 2027-02
lifecycle: active
verification_refs: [packs/coding/CHECKS.md]
migration_sources: [packs/coding/PACK.md:requirements:005]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B5]
---

# DOC-COD-006

The `statement` field is the canonical standing proposition.

## Reasoning and limits

Security and
policy rules run against the diff, not the whole repository, and
blocking findings are separated from monitoring findings (EV-0070).
Repository health checks read the repo's actual state (EV-0069).
Prevents shipping generated code on trust: roughly 40 per cent of
generated programs in security-relevant scenarios contained a
vulnerability, and the rate varied with prompt and domain in ways the
author cannot see (EV-0181). Scope note: that was a 2021 model on
deliberately security-loaded prompts. The finding that survives is the
necessity of a gate, not the size of the number. Whole-repo-only gates
are themselves an anti-pattern: they produce alert fatigue and then get
turned off. See `packs/coding/refs/REVIEW_GATE.md`.

Guarded actions are outside review entirely. Deployment, deletion,
force-push, secret access, money movement and the rest are ruled by
`kernel/GUARD_SPEC.md` and its non-waivable floors. No review verdict,
machine or human, changes a guard verdict.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/coding/PACK.md:requirements:005`, lines 149-165, SHA-256 `6dc099fe169ddb0951425d2f4a025fbeb8422d1a6fb324f0e12db4178850952a`.
