---
summary: The pass gate for a compiled seed, auto items keyed to check IDs, human items headed by the cold-start test
type: kernel
tags: [eos]
---

# SEED_RUBRIC

The gate a compiled seed must pass before Session 0 closes (and again
after every PB-E06 upgrade). Two halves: the auto items run as
`python tools/eos_check.py --seed <path>` and must be all green; the
human items are judgement, signed by the operator. A seed that fails
any auto item does not reach the human.

## Auto items (eos_check --seed)

| id | check | what passes |
| --- | --- | --- |
| A1 | E002 | every markdown file opens with parseable front-matter |
| A2 | E002 | the lock-book header carries eos_version, eos_commit, scale (S, M or L) and stack |
| A3 | E002 | every ruling row in the lock-book is marked argued or inherited |
| A4 | E008 | zero unfilled `{{SLOT}}` markers anywhere |
| A5 | E008 | zero leftover scale fences anywhere |
| A6 | E008 | every file the SCALE_MATRIX requires for the ruled scale is present |
| A7 | E008 | every file of every add-on named in the lock-book header is present |
| A8 | E008 | the compile report's ancestry table covers every matrix-required file, and names no file that is absent |
| A9 | E003 | CLAUDE.md is a byte-identical copy of AGENTS.md |
| A10 | E007 | the compiled AGENTS.md is at most 40 lines |

## Human items (signed, not delegated)

| id | item | how to judge |
| --- | --- | --- |
| H1 | **The cold-start test.** A fresh session, given only the seed and the first queue item, completes it with zero questions | run it; count the questions |
| H2 | The brief reads true: the operator recognises the venture in it, including the three cheapest deaths and the smaller-version verdict | read docs/VENTURE_BRIEF.md aloud |
| H3 | Rulings are honest: spot-check two argued rulings; each engaged its wargame's triggers rather than restating the default | open the wargame beside the ruling |
| H4 | Voice holds on the compiled surfaces a stranger reads first: router, brief, operators guide | read for tells; plain, spoken, no clichés |
| H5 | The operator can run their rhythm from the guide alone: launchers copy-paste, daily and weekly lists actionable | operator walks it without help |

Sign-off is recorded at the foot of the compile report: date, name,
items initialled. H1 failing blocks the gate outright; the fix is
better files, then a fresh cold session, never a warmer prompt.
