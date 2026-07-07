---
summary: Architecture module, seven rules and eight wargames from the estate's ADRs
type: doctrine
tags: [arch]
---

# Architecture

The module that owns structural decisions: boundaries, seams, data
topology, proof of harmless change, vendor depth. Populated at F1 from
the estate's decision records (WiseWattage ADR-001 to 007,
PatterTech_Business ADR-0001 to 0014, Venture A ADR-0001 and 0002 and
its constitution's Part I).

## Activation triggers

Any venture with server-side code, more than one module or deployable,
a database, an API boundary between languages, or a vendor holding
identity or money. Walked at M and L; an S venture inherits the
defaults silently until a rescale trigger fires.

## What lives where

- The seven binding rules: `DOCTRINE.md`.
- The eight forks: `wargames/` (WG-ARCH-001 boundary enforcement, 002
  ORM or raw SQL, 003 derived state, 004 job execution, 005 the
  contract seam, 006 proof of harmless change, 007 vendor seams, 008
  database topology).
- The ADR format ventures compile: `templates/ADR_TEMPLATE.md`.
- Versioned facts (library choices, caps, hosting): the stack profiles
  in `registry/stacks/`, cited from rulings, never inlined here.
