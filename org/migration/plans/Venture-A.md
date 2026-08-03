---
summary: Venture A's read-only v2 migration plan, the recompile route and what the engine does not yet cover
type: org
tags: [eos]
---

# Migration plan · Venture A

Read-only. Produced on 2026-08-03 by running, from the EOS repo:

`python -m tools.eos migrate plan --seed C:/Users/Daniel/Documents/Coding/Github/Venture A`

Nothing was written to Venture A. ADR-0002 reserves every sibling-repo
write for a later decision, so this file is a report and not a change.

## What the command reported

- venture: Venture A
- pin_current: pre-1.0.0@0a2a044
- route: recompile
- steps: pin-policy (the lock-book header gains the v2 policy pin);
  roles-to-tier-note (role charters swap for the tier policy note);
  inventory, which came back "inventory complete"
- provenance_preserved: the lock-book rulings, the decisions directory,
  the logs directory
- report_path: org/reports/migration-Venture A.md

"inventory complete" means every file the v1 matrix requires at scale L
is present in the seed, so nothing is missing before the migration
starts.

## Why recompile

The pin is 0a2a044, an EOS commit of 2026-07-07 that is an ancestor of
both pushed tags, so it resolves and the provenance is sound. It
predates the v1.0.0 kernel freeze, which is the condition for recompile
in org/migration/PLAYBOOK.md: the templates that produced this seed no
longer describe the system, so the transforms cannot be purely
mechanical.

One honest note on the engine. The route heuristic reads the
eos_version string, and "pre-1.0.0" parses as neither a zero-point nor
a bare one-point version, so it lands on recompile through the fallback
rather than through the pre-1.0.0 rule. The route is right; the reason
it is right is worth knowing before anyone tunes the heuristic.

## Scale and rulings

Venture A is the estate's only L venture, so it recompiles as ORG. The
scale ruling itself does not change: all six WG-EOS-001 triggers fire,
and ORG is where L now lands.

The header carries seventeen rulings, nine argued and eight inherited.
All seventeen carry across verbatim, marks included, because a v1
ruling is an argument of record. The argued ones stay promotion
evidence and the harvest can count them; the eight inherited ones are
the walk's cheapest rows and stay exactly that. Each one re-homes under
the pack that owns its decision, keeping its WG- id.

## What the plan does not yet cover

The engine's queue transform looks for a single queue file. Venture A
runs the L work-order shape instead: forty-eight order files under
org/work/items/, three suggestions, and a next file. No step in the
plan mentions them, so the recompile has to convert them to task
records by hand or the engine needs an L path before it runs here.
That is the largest piece of work in this migration and the plan
currently understates it.

Two smaller items the recompile fixes on the way through:

- The lock-book header names an eos_root that no longer exists, from
  before this repository was renamed. A recompiled header carries the
  current root.
- The v1 header has no policy_profile and no packs_adopted keys, so
  both are new fills, and the risk-surface map has to be taken from the
  operator because the v1 interview never produced one.

## Add-ons

The lock-book names the compliance add-on. Under v1 that file was
`org/knowledge/registry/REG-COMP-<JURIS>-001.md`; the v2 matrix names
org/COMPLIANCE.md, authored from the registry pattern the adopted
compliance pack gives. The live UK duty behind it is unchanged, so this
is a move rather than a rewrite, and the recompile records the old file
as preserved.

## Gate

The recompiled seed passes the seed check with zero errors, then Daniel
signs the human rubric items again, headed by the cold-start test.
Only then does the row in registry/PROJECTS.md take the new pin.
