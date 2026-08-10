---
summary: PatterTech_Website's read-only plan, fresh v2 S inception whenever the operator wants it
type: org
tags: [eos]
---

# Migration plan · PatterTech_Website

Read-only. Produced on 2026-08-03 by running, from the EOS repo:

`python -m tools.eos migrate plan --seed C:/Users/Daniel/Documents/Coding/Github/PatterTech_Website`

Nothing was written to PatterTech_Website. ADR-0002 reserves every
sibling-repo write for a later decision, so this file is a report and
not a change.

## What the command reported

- venture: PatterTech_Website
- pin_current: none
- route: fresh-inception
- steps: session-0, with the note "no lock-book found: run a fresh v2
  Session 0"
- provenance_preserved: empty
- report_path: org/reports/migration-PatterTech_Website.md

The empty provenance list is correct and is not a warning. There is
nothing to preserve from a v1 seed because there was never a v1 seed.
The site predates the EOS: it has its own AGENTS.md and CLAUDE.md, a
docs tree it wrote itself, and no org directory at all.

## Why nothing is urgent

The site is live and shipping. It has no pin, so it reads nothing from
this repository at runtime and a v2 release changes nothing about it.
The consent rule in org/migration/PLAYBOOK.md applies with full force
here: this venture moves when Daniel wants it to and not before.

The sensible moment is when the current foundations work settles. A
Session 0 run mid-pass would compile a lock-book against a tree that is
still moving, and the first-build lock-in would then be re-ruling
values the pass had already changed.

## The route when it comes

S scale, and Express inception is the right path. Test it against the
gate in inception/EXPRESS_INCEPTION.md:

- No money changes hands through the site.
- No personal or regulated data; there is no form that stores anything.
- Nothing authenticates and nothing holds server-side state.
- The deployment is a static export, so there is no state behind it.
- One human holds every decision.

Every answer is a no, so six questions and one challenge pass produce
the nine-file S seed. WG-EOS-001 already carries a worked S ruling for
this venture from 2026-07, argued, with its rescale condition written
down: any server-handled form or reader accounts.

## What the compile has to handle

This is a reseed of a repository with real content, so the compile
report uses its two extra row kinds. Files the venture already owns and
the compile leaves alone are marked preserved: the docs tree, the
design system, the architecture notes, the changelog. Files that gain
front-matter and nothing else are marked normalised. The seed's own
files are the only compiled rows.

Two collisions to rule at phase B rather than discover at phase D. The
repository already has an AGENTS.md and a CLAUDE.md kept in step by its
own lint script, and the compiled router replaces both, so the script
either goes or is repointed. The design system is the deepest
PatterTech house material in the estate, and the house pack activates
only by adoption, so the lock-book's packs_adopted list has to say so
explicitly.

## Gate

The compiled seed passes the seed check with zero errors, then Daniel
signs H1 and H4 per the Express path, with the sign-off block recording
that Express was used and which items were judged.
