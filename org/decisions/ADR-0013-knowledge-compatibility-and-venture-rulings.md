---
summary: One commit-aware resolver, pressure-selected Wargaming and structured venture-owned Rulings
type: decision
tags: [eos, wargame]
status: accepted
superseded_by: ADR-0015
decided_by: Daniel Parke
date: 2026-08-15
---

# ADR-0013: knowledge compatibility and venture Rulings

## Context

The current checks do not share an identity model. E005 recognises `WG-*`
definitions, S004 recognises a different set of schemes, and the seed checker
validates only delimiter rows beginning `WG-*`. One hundred live `GD-*`
procedures therefore sit outside ruling-shape and pinned-reference validation.
The lock-book template also cites four retired Wargames as though they were
live choices.

A semantic rename would deepen the problem. Historical pins, raw Markdown
links and archived provenance must resolve against the tree that actually
defined them, never against a convenient current fallback.

## Decision

**One. One resolver owns identity.** Checks, indexes, CLI discovery, Session 0,
migration and harvest use the same commit-aware resolver for DOC, GD, WG,
DREL and RUL identities. A requested Git ref is resolved once to a commit. A
valid historical ref never falls back to the worktree; an invalid ref is a
cannot-run result.

The resolver distinguishes live, aliased and retired definitions. It rejects
duplicate definitions, alias cycles, live reuse of retired IDs, missing
targets, invalid archived locations, self-relations and cycles in dependency
or supersession graphs. A retired ID may resolve for provenance and may not be
used for an active Ruling.

**Two. Compatibility is explicit.** Legacy pack anchors map to their DOC
targets. Existing GD and WG IDs remain canonical, not aliases. The generated
`WARGAME_INDEX.md` is the public view. `GUIDE_INDEX.md` remains a generated
compatibility pointer and is not a second catalogue. `eos id resolve ID
[--commit REF]` exposes the same answer the checks use.

**Three. Matching is tri-state and explains itself.** Facts are `true`,
`false` or `unknown`.

- True pressure requires its Wargame.
- False pressure records why the Wargame was omitted.
- Unknown high-consequence pressure asks the operator or includes the
  Wargame.
- Unknown routine pressure produces a candidate.

An operator may include or omit a candidate with a recorded reason. Scale,
repository shape and security floors remain always-walk decisions. Matching
returns applicable Doctrine summaries, required and candidate Wargames,
unresolved facts, uncovered pressure and selection reasons. It never chooses
an option or outcome. Full Doctrine atoms load on demand.

**Four. A Ruling is one venture executing one Wargame.** New ventures own
`docs/RULINGS.json`, referenced from their lock-book. The file records its EOS
pin, selection and omission reasons, and `RUL-*` executions. Inherited
Doctrines remain implicit through the pin, adopted packs and profiles. A
default departure needs a reason. A proposed change to binding scope needs an
ADR or operator reference.

Legacy delimiter rows remain readable only when the pinned schema predates
this decision or a migration state explicitly marks them legacy. `eos migrate
plan/apply` converts them losslessly and idempotently, retaining exact text and
provenance. It does not invent missing facts. The existing safety boundary
continues: migration writes only fixture seeds in this repository unless the
operator separately asks to migrate a venture.

**Five. Raw Rulings stay with the venture.** EOS harvest accepts only a
privacy-reviewed, sanitised summary. Commercial, household, legal,
authentication and personal context is never copied into this public tree.

## Consequences

Session 0 changes from walking every guide to inheriting applicable Doctrine
and running Wargames selected by pressure, conflict, gap or explicit request.
The always-walk decisions remain. Every candidate has a visible selection or
omission reason, so selectivity cannot become silent neglect.

Compatibility readers land before metadata migration. They remain until old
pins and explicit legacy migrations no longer need them; new current-head
seeds have one machine source, `RULINGS.json`. No venture is rewritten by this
decision.
