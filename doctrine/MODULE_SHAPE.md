---
summary: What every doctrine module must have, may have, and must never become
type: governance
tags: [eos]
---

# MODULE_SHAPE

The contract for a doctrine module. The invariant core is in the
protected set; the optional organs are chosen per domain.

## Invariant core

Every module has:

- `README.md`: what the module covers, its status, and an **Activation
  triggers** section naming the venture conditions that pull this module
  into a Session 0 walk (e.g. "any public web surface" for web-design).
- `DOCTRINE.md`: the binding rules. A young module writes "No doctrine
  yet, see the wargames" rather than inventing rules to look finished.
- `wargames/`: the module's decision procedures, IDs `WG-<MOD>-NNN`,
  written from `doctrine/web-design/templates/WG_TEMPLATE.md`.
- Front-matter on every file per GOVERNANCE.md, so the indexes stay
  derived and honest.

## Optional organs

Add only what the domain earns: `foundations/` (derivation methods),
`patterns/` (the execution vocabulary), `ux/`, `implementation/`
(profiles and gates), `templates/`, `examples/`. A module with two
wargames and a README is a legitimate module.

## Rules that keep modules lean

- **The pruning test.** For every line ask: would removing this cause an
  agent to make a mistake? If not, cut it. Restating common knowledge is
  bloat, and bloat is how instructions get ignored.
- **Line budgets.** Doctrine, foundation, pattern, ux, implementation
  and wargame files carry the 150-line budget from GOVERNANCE.md.
- **One fork per wargame; split, don't nest.** If a second independent
  question grows inside a wargame, file it as a new wargame and
  cross-link. No sub-numbering.
- **New wargame or ruling note?** If an existing wargame covers the
  fork, append a worked ruling. If none does, file a draft wargame with
  your ruling as its first worked entry. A single technical finding
  (a better constant, a sharper phrasing) is a note inside the existing
  wargame, not a new one.
- **Doctrine argues; registries date.** Versioned facts (package names,
  platform behaviour, prices) belong in `registry/`, cited from the
  module, never inlined into doctrine.
- **Cross-module decisions** live in the module that owns the decision;
  the wargame index carries every domain tag so inception still finds
  them.
