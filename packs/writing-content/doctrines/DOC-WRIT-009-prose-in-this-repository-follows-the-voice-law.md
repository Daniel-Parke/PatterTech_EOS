---
summary: Prose in this repository follows the voice law.
type: doctrine
tags: [eos]
id: DOC-WRIT-009
statement: Prose in this repository follows the voice law.
kind: doctrine
authority: default
basis: decision
evidence_grade: observational
scope: eos-internal
applies_when: [writes_eos_internal_prose]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0027, EV-0062, EV-0063, EV-0122, EV-0233, EV-0335, EV-0433, EV-0434, EV-0435, EV-0436, EV-0437, EV-0438, EV-0439, EV-0440, EV-0441, EV-0442, EV-0443, EV-0444, EV-0445, EV-0446, EV-0447, EV-0448]
review: on-change-of:CLDR-plural-categories
lifecycle: active
verification_refs: [packs/writing-content/CHECKS.md]
migration_sources: [packs/writing-content/PACK.md:defaults:005, packs/writing-content/PACK.md:voice-scope:001]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B8]
---

# DOC-WRIT-009

The `statement` field is the canonical standing proposition.

## Reasoning and limits

### `packs/writing-content/PACK.md:defaults:005`

`writes_eos_internal_prose`. Plain, spoken, British spelling, no
em-dashes, no exclamation marks, no AI cliches, no two-fragment
antithesis. Scope eos-internal only. Prevents drift in the one
repository every agent reads. Basis: decision, ADR-0002. Failed the
basis leg: a house ruling about a house is not law, a standard or a
measured effect, and no study of a voice rule's effect was looked for
or found. It does not clear the seriousness leg either, because prose
that drifts is repaired by rewriting it.

Demoting it changes nothing an agent does. Check E004 fails the build
on an em-dash and warns on exclamation marks and cliches, so the
mechanical part is not departable in this repository whatever this pack
says about its authority, and `AGENTS.md` states the same law in the
file every session reads. What a task can record a reason against is
the judgement part, the register and the phrasing. The rule still
carries no authority over a venture's product copy or its brand.

### `packs/writing-content/PACK.md:voice-scope:001`

default, and E004 fails the build

every file in this repository

decision, ADR-0002

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/writing-content/PACK.md:defaults:005`, lines 246-262, SHA-256 `5fe1b8e982221f50d75f5fe7030e80d3eacf56c266ae094a8f496aec4cacfeee`.
- `packs/writing-content/PACK.md:voice-scope:001`, lines 102-102, SHA-256 `bc25cec86d0ad4dbafb7fa7bba9a1616ea3e0128237862220e696ede1e59668c`.
