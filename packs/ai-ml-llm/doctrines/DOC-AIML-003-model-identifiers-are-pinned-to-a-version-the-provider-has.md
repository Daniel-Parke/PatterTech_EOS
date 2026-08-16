---
summary: Model identifiers are pinned to a version the provider has undertaken not to move, with the retirement date recorded beside the call site.
type: doctrine
tags: [eos]
id: DOC-AIML-003
statement: Model identifiers are pinned to a version the provider has undertaken not to move, with the retirement date recorded beside the call site.
kind: doctrine
authority: binding
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [calls_a_model]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0259, EV-0260]
review: 2027-02
lifecycle: active
verification_refs: [packs/ai-ml-llm/CHECKS.md]
migration_sources: [packs/ai-ml-llm/PACK.md:requirements:003]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B4]
---

# DOC-AIML-003

The `statement` field is the canonical standing proposition.

## Reasoning and limits

No "latest", no bare family name. Pinned is a property, not
a shape: some providers express it as a dated snapshot, some as a
version-numbered id carrying no date at all, and the test is whether the
id keeps resolving to the same weights. Requiring a date fails that test
today, because a major vendor's current ids are undated and its own
guidance is to send them exactly as published rather than append a date.
The pinned id and its published retirement date live next to the code
that calls it, and a migration eval runs on the candidate before the
switch. Prevents both silent drift and a hard outage: the same endpoint
name changed behaviour substantially inside months, one task falling
from 84 per cent to 51 per cent between two snapshots (EV-0259, whose
arithmetic result is contested as partly a formatting artefact), while
the provider lifecycle gives sixty days' notice as a floor and retired
models fail outright (EV-0260). Scope note: EV-0260 is one vendor's
policy, and platform resellers run their own clocks. See
`packs/ai-ml-llm/wargames/WG-AIML-006-model-lifecycle-and-cost.md`.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/ai-ml-llm/PACK.md:requirements:003`, lines 117-134, SHA-256 `20d23c94dd91ae711a452972c9db1f3ebd688bd4670fe1cf6c262c17ff037ed5`.
