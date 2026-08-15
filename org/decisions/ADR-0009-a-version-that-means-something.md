---
summary: Re-designate the current line to 0.x, and define the checkable gate that 1.0 has to pass
type: decision
tags: [eos]
status: accepted
decided_by: Daniel Parke
date: 2026-08-15
---

# ADR-0009: a version that means something

The operator, 2026-08-15: "If we have previously tagged this as v2.1 I am not
sure that was wise, as I am not 100% happy even with this release. We
are happy for it to be used, but to me V1.0 is when we can walk away
from it if we so choose and it is OK. I don't feel like we are there yet
until we have a much more expanded knowledge base to draw from to seed a
wider range of project types."

The operator accepted this on 2026-08-15, in the session that raised it, and
the renumber is applied: `tools/pyproject.toml`,
`tools/eos/__init__.py`, `README.md` and `TOUR.md` now read 0.4.0.
No tag is cut, so nothing is released and `CHANGELOG.md` gains no new
heading, which is what keeps check S011 quiet. Whether to cut a tag at
all remains PB-E05 and the operator's.

## Context

The tree currently disagrees with itself about what it is. `git tag -l`
returns `v1.0.0`, cut 2026-07-07, which released the v1 architecture.
That architecture has since been entirely replaced: v1's `doctrine/`,
`GUIDE.md`, `START.md` and `VISION.md` are gone from the working tree
and preserved at `archive/v1-final`. Meanwhile `tools/pyproject.toml`
and `tools/eos/__init__.py` both declare `2.1.0`, and roughly 360 of
`CHANGELOG.md`'s 395 lines sit under `## Unreleased`.

So a reader cloning at the newest tag gets v1, and a reader cloning
`main` gets an unreleased 2.1.0. ADR-0007 made that deliberate rather
than accidental, and it is documented. What it is not is a number that
tells anyone how far along this is.

The audit that opened this branch is the evidence for the gap. It is not
that the system is unsound. `python -m tools.eos check` reports no
errors, the suite is green across four platform and version pairs, and
the honesty scaffolding through the router, the guard and the drills is
the best engineering in the repository. It is that several things a
walk-away-ready system needs are specified and unexercised:

- The routing layer ruled a tier from an empty fact set on 21 of the
  first 25 task records, and on 22 the ruled tier came out below the
  tier the author proposed.
- All 22 pack drills carried a null verdict until 2026-08-15, and what
  they carry now is a discrimination check, not a pack verdict.
- Genesis is fully specified and has never run on a venture.
- `packs_adopted` is empty in both seed fixtures and in all three
  ventures, so the pack-adoption path has never run end to end.
- Every count in the prose is hand-written and unchecked.

A 2.1.0 sitting on top of that reads as a mature second major line. It
is a promising first one.

## Decision

**One.** Re-designate the current line as 0.x. The v2 overhaul becomes
`0.2.0`, v2.1 becomes `0.3.0`, and the work on this branch ships as
`0.4.0`. Touch points are `tools/pyproject.toml`,
`tools/eos/__init__.py`, which a test holds equal, `CHANGELOG.md`,
`README.md` and `TOUR.md`.

**Two.** Leave the `v1.0.0` tag exactly where it is, and explain it
rather than move it. It released a real architecture that is archived
and retrievable. Deleting or moving a published tag to make a number
tidy is the kind of history rewrite this repository refuses elsewhere.
The discontinuity is recorded in the changelog: the 0.x line is the
rewrite, and `v1.0.0` belongs to the system it replaced.

**Three.** Venture pins are unaffected. A pin resolves a commit, not a
version string, and S010 checks it that way, so no seeded venture
changes because a number did.

**Four.** 1.0 means walk-away ready, and the gate is checkable rather
than felt. Every item below is a thing somebody can run or read and get
a yes or a no:

1. Every documented control is classified against what enforces it, and
   nothing described as enforced turns out to be procedural.
   `org/reports/CONTROL_ENFORCEMENT.md` is the first pass and the format
   the gate reads.
2. The 22 pack drills carry real verdicts. Where one cannot, its row
   says why, individually, rather than a blanket note.
3. Genesis has run end to end on at least one real venture.
4. A cold agent given only a compiled seed and the first open task
   completes it with no questions, rubric item H1, across the
   representative seed corpus rather than on one example.
5. Pack activation is measured, with precision and recall per pack and
   at least one negative case each. A system that never misses a pack
   because it activates everything has not solved activation.
6. Every count in the prose is generated or checked. Today "513 tests"
   appears four times and "504 rows" five, all accurate, none held by
   anything.
7. The release gates in `benchmark/PROTOCOL.md` are met or struck with
   reasons, and a struck gate is never reported as a met one.
8. The knowledge base covers the project types the estate actually
   seeds, with each capability admitted through the pack gate rather
   than asserted.

**Five.** Until every item passes, the number stays below 1.0 and the
release notes carry the open ones by name. A version is not a mood.

## Counter-evidence and what argues against this

**Numbers going backwards is user-hostile.** A consumer pinning
`eos-tools>=2.1` finds 0.4.0 does not satisfy it. The mitigation is that
there is no such consumer: the package is not published, the only
governed ventures pin commits, and ADR-0007 already established that
nothing has been released from this line.

**It relabels finished work as unfinished.** The v2 overhaul and v2.1
were real and are not diminished by the number. The argument for doing
it anyway is that the number is read by people deciding whether to
depend on this, and it currently overstates. The changelog keeps every
word of what was built.

**ADR-0007 said one release, carrying the v2.1 number.** This changes
that clause and nothing else in it. No `supersedes` pair is declared,
deliberately: ADR-0007 also strikes two benchmark gates, retires the
sealed suite unopened and defers the drill spend, and all of that still
stands. A `superseded_by` stamp says the whole record is done, which
would be a larger and false claim, and S002 would then hold the tree to
it. The narrower truth is in this paragraph, where a reader of either
record will find it.

**A gate with eight items may never be met.** Items 3 and 4 need a real
venture and a real cold agent, which are not things a repository can do
to itself. That is the honest cost of the definition the operator gave: if
walking away has to be safe, something has to have walked.

## What this does not decide

Whether to cut a tag at all, and when. That is PB-E05 and the operator's.
