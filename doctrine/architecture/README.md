---
summary: Architecture module, queued for Phase F, boundaries and ADR practice
type: doctrine
tags: [arch]
---

# Module: architecture (queued)

Lands in Phase F (see `org/QUEUE.md`). Will cover system boundaries as
records (import rings enforced by lint), ADR practice, deterministic
builds and plan/build decoupling, contracts with drift checks, and the
wargames for monolith versus services, sync versus queue, API style and
flag strategy.

Extraction sources: WiseWattage (ring architecture, OpenAPI drift
checks), PatterTech_Business (import-linter rings, byte-stable engine),
AutoWatt ADR-0001 and ADR-0002. Shape per `doctrine/MODULE_SHAPE.md`.

## Activation triggers

Any venture with server-side code, more than one deployable, or an API
boundary between languages.
