---
summary: Copyleft entering anything we ship or host takes a written decision before merge, not at release.
type: doctrine
tags: [eos]
id: DOC-LEGAL-004
statement: Copyleft entering anything we ship or host takes a written decision before merge, not at release.
kind: doctrine
authority: binding
basis: standard
evidence_grade: observational
scope: estate
applies_when: [adds_dependency]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0341, EV-0342]
review: 2027-04
lifecycle: active
verification_refs: [packs/legal-licensing/CHECKS.md]
migration_sources: [packs/legal-licensing/PACK.md:requirements:004]
generated_by: tools.eos.migrate_doctrines
legacy_anchors: [B4]
---

# DOC-LEGAL-004

The `statement` field is the canonical standing proposition.

## Reasoning and limits

`hosts_service`,
`publishes_code`, `adds_dependency`. The entry in `LICENCE_DECISION.md`
names the component, its exact identifier, the event that would fire the
obligation, in the words distribution, network interaction or
combination, and the disposition.

Where the same component also trips an escalation trigger under B7, and
copyleft entering something we host in modified form trips both, the
disposition is the single word `referred` plus the handover reference.
The entry is still written and still names the component, the identifier
and the event, because those are facts the agent can establish; what it
must not do is supply the answer. Read on its own, B4 asks for a
disposition and B7 forbids the agent from reaching one, and an agent
obeying each in turn fails whichever check it satisfies second. The
`referred` disposition is what satisfies both, and the lawyer's answer
replaces it when it arrives. A drill found the collision.

AGPL section 13 attaches to a modified
version reached by users remotely over a network, with nothing
distributed (EV-0341). Prevents
the standard miss: a policy written around source and binary
distribution is silent on a hosted service, which is the shape most
ventures ship (EV-0342, scoped to one foundation's
promise about its own releases). Authority: binding. Basis: standard.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/legal-licensing/PACK.md:requirements:004`, lines 168-192, SHA-256 `86d34771e47d724a42611f600d272136d0a695a5d2a9c12a7bee7812949ba4be`.
