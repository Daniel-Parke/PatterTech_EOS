---
summary: The pass gate for a compiled seed, auto items keyed to v2 checker ids, human items headed by cold-start
type: kernel
tags: [eos]
---

# SEED_RUBRIC

The gate a compiled seed must pass before Session 0 closes, and again
after every upgrade recompile. Two halves: the auto items run as
`python -m tools.eos check --seed <path>` and must be all green; the
human items are judgement, signed by the operator. A seed that fails
any auto item does not reach the human.

## Auto items (check --seed)

| id | check | what passes |
| --- | --- | --- |
| A1 | E002 | every markdown file opens with parseable front-matter |
| A2 | E002 | the lock-book header carries eos_version, eos_commit, scale (S or ORG) and stack |
| A3 | E002 | every ruling row in the lock-book is marked argued or inherited |
| A4 | E008 | zero unfilled `{{SLOT}}` markers and zero leftover scale fences anywhere |
| A5 | E003 | CLAUDE.md is a byte-identical copy of AGENTS.md |
| A6 | E007 | the compiled AGENTS.md is at most 40 lines |
| A7 | D001 | compiled front-matter carries compiled_from; template and extracted_from keys are absent |
| A8 | D002 | every compiled_from target exists at the pinned eos_commit |
| A9 | D003 | negative matrix: no file outside the matrix, the named add-ons and the report's authored, normalised or preserved rows |
| A10 | D004 | every set-at-first-build deferral has an open task scheduling the lock-in |
| A11 | D006 | every WG id the lock-book cites resolves in the pinned EOS |
| A12 | D007 | the policy file parses and validates against kernel/schemas/policy.schema.json, with /risk and /approvals among its protected pointers |
| A13 | D008 | the guard block names an adapter and mapping_ref, and either validated is true with the named mapping shipped in the seed, or validated is false and guarded actions are declared manual-only |
| A14 | D009 | org/claims.json parses and validates against kernel/schemas/claims.schema.json; the seeded state is an empty lanes list (ORG only) |
| A15 | D010 | one compiled file per Genesis template, matched on compiled_from and not on a destination path (ORG only; quiet against a seed pinned before the templates existed) |
| A16 | D011 | the compiled acceptance spine still says expected-fail and still carries a manifest table with a state column. Form only: nothing here runs a suite, so this cannot say a spine fails |

## Human items (signed, not delegated)

| id | item | how to judge |
| --- | --- | --- |
| H1 | **The cold-start test.** A fresh session, given only the seed and the first open task, completes it with zero questions | run it; count the questions |
| H2 | The brief reads true: the operator recognises the venture in it, including the three cheapest deaths and the smaller-version verdict | read docs/VENTURE_BRIEF.md aloud |
| H3 | Rulings are honest: spot-check two argued rulings; each engaged its wargame's triggers rather than restating the default | open the wargame beside the ruling |
| H4 | Voice holds on the surfaces a stranger reads first: router, brief, operators guide | read for tells; plain, spoken, no clichés |
| H5 | The operator can run their rhythm from the guide alone: launchers copy-paste, approval duties clear, daily and weekly lists actionable | operator walks it without help |

Sign-off is recorded at the foot of the compile report: date, name,
items initialled. H1 failing blocks the gate outright; the fix is
better files, then a fresh cold session, never a warmer prompt.
