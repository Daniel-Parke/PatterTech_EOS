---
summary: Venture C's read-only v2 migration plan, the pin normalisation and the nineteen queue rows
type: org
tags: [eos]
---

# Migration plan · Venture C

Read-only. Produced on 2026-08-03 by running, from the EOS repo:

`python -m tools.eos migrate plan --seed "Venture C"`

Nothing was written to Venture C. ADR-0002 reserves every sibling-repo
write for a later decision, so this file is a report and not a change.

## What the command reported

- venture: Venture C
- pin_current: v1.0.0@a9a0392ad5ae82a906365de264bcfbb2f9dbdde4
- route: recompile
- steps: pin-policy; roles-to-tier-note; queue-to-tasks (queue rows
  become task records); inventory, which came back "inventory complete"
- provenance_preserved: the lock-book rulings, the decisions directory,
  the logs directory
- report_path: org/reports/migration-Venture C.md

## The pin, and why it needs normalising

The lock-book records the pin as v1.0.0 at a9a0392. Both halves are
checkable and they disagree.

- The v1.0.0 tag is 819577f, dated 2026-07-07.
- a9a0392 is dated 2026-07-08 and its subject is an estate bookkeeping
  commit. It is a descendant of the v1.0.0 tag, so it is not that
  release.
- a9a0392 does resolve, and it is an ancestor of the pushed tag
  archive/v1-final, so the provenance holds and nothing is lost.

The label is therefore wrong and the commit is fine. The migration
normalises the pin to archive/v1-final, which is a pushed tag that
contains a9a0392, and check S010 then passes on the registry row
without a caveat.

## Why recompile rather than apply

The route heuristic reads eos_version as a bare semver. This header
writes it with a leading v, which parses as neither form, so the plan
falls through to recompile. The heavier route is the safe one, and in
this case it is also the honest one: the recorded version is not the
release it names, so treating the seed as a clean v1.0.0 compile would
be trusting a label the pin itself contradicts.

## Scale and rulings

Venture C is M, so it recompiles as ORG with no change of argument:
standing ops fires because the LAN rig deploys from the tree, and
personal data stays silent because the only recordings are the
operator's own.

The header is the estate's densest, and every row carries across
verbatim. Several rulings are worth flagging to the harvest rather than
to the migration: the WG-OPS-002 row records contrary evidence against
the container default, and the WG-ARCH-002 row rules "not applicable"
because the venture holds no relational store anywhere. Both are real
arguments and neither is affected by the kernel change.

## The nineteen queue rows

org/QUEUE.md holds nineteen work-order sections, and the plan's
queue-to-tasks step would turn each into a task record. That transform
does not read status, so it converts finished orders alongside open
ones. Before this runs for real, the closed rows want either filtering
or a status field on the created record; a migration that reopens
finished work is worse than one that leaves it in the queue.

## What changes

The three role charters swap for the tier policy note. A policy file
appears, filled from a risk surface the v1 interview never produced, so
The operator supplies it: which paths hold the recordings, which hold
the rig service, which are protected. Guard validated stays false, so
every guarded class is manual-only until a bypass-suite report exists.

## Gate

The recompiled seed passes the seed check with zero errors, then the operator
signs the human rubric items again, headed by the cold-start test. The
registry row then takes the normalised pin, the ORG scale and the packs
adopted.
