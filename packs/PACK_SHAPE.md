---
summary: The pack contract, invariant and optional organs, the definition of done, and what stays a registry row
type: governance
tags: [eos]
---

# PACK_SHAPE

The contract for a knowledge pack. Packs replace doctrine modules. A
pack is loaded in three levels: its first paragraph is always in
context, its `PACK.md` body loads on activation, and everything else
loads on demand. This file changes through the RFC path, not an ADR.

## Invariant organs

Every built pack has all three:

- `PACK.md`. The pack itself. Its **first paragraph is level-one
  metadata**: under eighty words, saying what the pack covers and when
  it activates, because that paragraph sits in every agent's context
  whether the pack loads or not. The body stays under five hundred
  lines and carries activation, outcomes and non-goals, binding
  requirements, defaults, preferences, a decision map, failure modes,
  counter-evidence and the evidence pointer.
- `guides/`. The arguments of record, one fork per guide, ids
  `GD-<PACK>-NNN`. Wargames inherited from v1 keep their `WG-` ids and
  live here unchanged.
- `CHECKS.md`. What a reviewer or a script can verify about work in
  this domain, split into executable today and judgement today. A check
  that needs a person is still a check.

## Optional organs

Add only what the domain earns:

- `refs/`. Mechanics, cards and tables too long for the body.
- `exemplars/`. Worked examples, ids `EX-<PACK>-NNN`.
- `recipes/`. Short repeatable procedures, four metadata fields each.
- `research/`. The synthesis notes and the drill proposal behind the
  pack.

A pack with three organs and no optional ones is a legitimate pack.

## Definition of done

A pack is "implemented" only when it contains all of:

1. Activation triggers and applicability predicates.
2. Desired outcomes and non-goals.
3. Binding requirements separated from defaults and preferences.
4. At least three materially different patterns or philosophies where
   genuine alternatives exist.
5. A decision guide stating when each pattern fits.
6. Trade-offs, failure modes and anti-patterns.
7. At least one worked example.
8. Evaluation criteria or executable checks where appropriate.
9. At least three maintained primary or official sources (published
   GitHub repositories where available), each an individual
   evidence-ledger row.
10. Counter-evidence or documented disagreement between sources.
11. Version/commit, licence, access date and review trigger for every
    source.

## The pruning test

For every line ask: would removing this cause an agent to make a
mistake? If not, cut it. Restating common knowledge is bloat, and bloat
is how instructions get ignored. Versioned facts belong in `registry/`
and are cited, never inlined. One fork per guide: a second independent
question is a new guide with a cross-link, never a sub-number.

## Activation triggers

Every pack declares its triggers in three tiers, and **at least one
must be a non-keyword trigger**: a path pattern or a task type. A pack
that can only be reached by keyword matching is not routable, because
routing has to be deterministic given the same inputs.

The declaration is machine-readable and lives in the pack's own
front-matter, so there is no second list to drift:

- `activation_paths`, a list of globs where `**` crosses directory
  separators and `*` does not.
- `applies_when`, the predicates.

`python -m tools.eos context` evaluates the globs and returns the
activated set with the paths that matched. Check S015 refuses a pack
that declares neither. Stating triggers in prose alone is what left
`activated_packs` an empty list while twenty packs sat on disk.

Applicability predicates are the real gate. A task that trips a path
trigger but satisfies no predicate loads nothing beyond the first
paragraph. Activation gives advice, never permission: no pack lowers a
tier floor set by `kernel/POLICY_SPEC.md` or converts a manual-only
action class into an autonomous one under `kernel/GUARD_SPEC.md`.

## A domain that cannot meet the bar

It stays a row in `registry/coverage.json` with status `registry-only`
and a recorded reason, and it is **never described as implemented**. No
stub directory, no placeholder `PACK.md`, no "coming in a later wave"
folder. A backlog row is not coverage, and the matrix says so.

The visible consequence: `packs/INDEX.md` lists built packs only, and
`registry/CAPABILITIES.md` lists every domain with its honest status.
An omission is a row, never a silence.
