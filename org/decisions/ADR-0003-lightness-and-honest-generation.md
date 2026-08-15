---
summary: Retained material that misleads an agent is a defect, the archive of record is a tag, and every derived file has a live generator
type: decision
tags: [eos]
status: accepted
decided_by: Daniel Parke
date: 2026-08-04
---

# ADR-0003: lightness, and honest generation

The operator ruled on 2026-08-04, during the pre-release review of
`feat/eos-v2-agentic-development`. Two changes to `GOVERNANCE.md`, which is
protected, plus the principle that governs both. This decision does not
supersede ADR-0002; it amends two clauses of the governance ADR-0002 put in
place, and everything else in ADR-0002 stands.

## Context

The pre-release review ran three independent antagonistic audits over the v2
branch. They agreed on a pattern: prose honesty is high and mechanical
enforcement is near zero. Nearly every narrative claim in the repository is
roughly true. Nearly every machine-readable artefact that nothing validates
has drifted.

Two findings are the reason for this record.

**The always-loaded surface was eight packs short.** `packs/INDEX.md` says
"Nothing else in `packs/` is loaded until a row here activates", and it listed
eight of the twenty packs that exist. The twelve Wave B packs, roughly nineteen
thousand lines, had no route in. The file was flagged `derived: true`, added to
the checker's generated-file allow-list, and then written by hand. The one
check that would have caught it, S005, was disabled by that allow-list entry,
and E001 never compared it because it was not in the compare set. It sat wrong
against a green build for the length of the build.

`GOVERNANCE.md` recorded the intent honestly: "Written by hand until the
generators are repointed, and flagged derived so the gap stays visible". The
gap did not stay visible. Flagging a hand-written file as derived does not make
the gap visible; it makes the checker skip it.

**Archived v1 material is being read as current law.** Forty-nine references
from live files point into `archive/v1/`, twenty-three of them from inside
`packs/`. The worst is `packs/architecture/PACK.md`, whose decision map routes
five of its forks into archived wargames. An agent following the architecture
pack's own table lands on a file stamped `status: archived` and treats it as
the argument of record. `INDEX.md` compounded it: seventy-five of its rows were
archived v1 files and sixty-four were benchmark fixtures, so a third of the
repository's index offered an agent material it must not act on. A benchmark
fixture's wargames, `WG-MINI-001` and `WG-MINI-002`, had reached the live guide
index and were being presented as EOS guidance.

`GOVERNANCE.md` said superseded material is "archived under `archive/`, never
silently deleted". The rule was written to protect history. In practice it
retained material that misleads, and the cost fell on every agent that reads
the repository.

## Decision

**1. Retained material that misleads an agent is a defect, not an asset.**

The EOS is to be as light as it can be while still doing its job. Where keeping
something costs an agent context or teaches it a superseded rule, keeping it is
the bug. This does not license losing history. It relocates history to where
history belongs.

**2. The archive of record is a git tag, not a directory.**

`archive/v1/` is retired from the working tree. The complete v1 tree, one
hundred and forty-two files, is preserved at the tag `archive/v1-final`, which
is pushed to origin and was created under ADR-0002's approved P0 branch
mechanics. `v1.0.0` is pushed likewise. A single pointer file records how to
retrieve any v1 file, and the retrieval is one `git show` away.

Nothing may be retired from the tree until every live reference to it is
resolved. Where a live pack delegates a decision into archived material, the
fix is to write the guide in the pack, not to delete the target and leave a
dangling link. This ordering is binding.

Amends `GOVERNANCE.md`, "Staleness and supersession": superseded material is
preserved at a pushed tag and removed from the working tree once nothing live
refers to it. It is never lost, and it is never left where an agent will read
it as current.

**3. Derived files are generated, or they are not derived.**

A file carrying `derived: true` must have a live generator and must be in the
checker's compare set. There is no third state. A file that is hand-written is
hand-written, and marking it otherwise hides it from the checks that would keep
it honest.

`packs/INDEX.md` now has a generator and is compared by E001. So does
`packs/GUIDE_INDEX.md`, whose generator selected `type: wargame` and therefore
omitted seventy-nine of the eighty-six guides on disk; it now indexes every
guide under a pack. `registry/CAPABILITIES.md` follows the same rule.

Every derived index is scoped to live material. Frozen trees are checked and
never indexed.

Amends `GOVERNANCE.md`, "Derived files": the registry of derived files names
`INDEX.md`, `packs/INDEX.md`, `packs/GUIDE_INDEX.md`, `registry/CAPABILITIES.md`,
`org/TASKS.md` and `org/STATE.md`, each with a generator that runs. The stale
entry naming the old doctrine wargame index is removed; it has not existed since
the pack restructure.

## Consequences

Accepted costs:

- A v1 file is no longer a path away. It is a `git show archive/v1-final:<path>`
  away. That is a real friction, paid rarely, by a person doing history, rather
  than paid on every read by every agent.
- Resolving the forty-nine live references is work, and five of them require
  writing architecture guides that should have been written in Wave A.

What this buys:

- `INDEX.md` falls from five hundred and six rows to three hundred and
  sixty-five, and from 89KB to 68KB. That is roughly five thousand tokens off
  the largest fixed boot cost in the repository.
- The twelve unreachable packs become reachable.
- The seventy-nine unindexed guides become findable.
- Three classes of drift that were invisible become checker findings.

## Scope

This decision authorises the two `GOVERNANCE.md` amendments named above and
nothing else in the protected set. Release of v2 remains a separate approval
under ADR-0002 and is not granted here. `main` is untouched.
