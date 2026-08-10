---
summary: FieldKit compile report, the seed's ancestry proof and sign-off record
type: template
tags: [eos]
compiled_from: kernel/templates/COMPILE_REPORT.tpl.md
---

# Compile report · FieldKit

Proof that this seed was compiled, not authored. Written by the
Session 0 compiler; validated by `eos_check.py --seed`; signed by the
operator against the human rubric items. A seed file that cannot be
traced to a row below is a compile failure.

## Seed identity

- venture: FieldKit
- scale: M · add-ons: none
- eos_version: 1.0.0 · eos_commit: 6590a82
- compiled: 2026-08-02 · compiler session: EOS v2 build, lane E

## Ancestry

One row per compiled file. Source is the kernel template path, `byte
copy of AGENTS.md` for CLAUDE.md, or `authored` for trigger add-ons
written at Session 0 from doctrine (name the doctrine). Reseeds add two
row kinds: `normalised` (pre-EOS venture files that gained front-matter
only, content untouched) and `preserved` (venture content the compile
did not touch).

| file | source | slots filled | fences pruned |
| --- | --- | --- | --- |
| AGENTS.md | kernel/templates/AGENTS.tpl.md | 2 | 3 |
| CLAUDE.md | byte copy of AGENTS.md | 0 | 0 |
| OPERATORS_GUIDE.md | kernel/templates/OPERATORS_GUIDE.tpl.md | 1 | 8 |
| docs/VENTURE_BRIEF.md | kernel/templates/VENTURE_BRIEF.tpl.md | 15 | 0 |
| docs/LOCKBOOK.md | kernel/templates/LOCKBOOK.tpl.md | 28 | 0 |
| docs/EOS_FEEDBACK.md | kernel/templates/EOS_FEEDBACK.tpl.md | 0 | 0 |
| docs/COMPILE_REPORT.md | kernel/templates/COMPILE_REPORT.tpl.md | 12 | 0 |
| org/CONSTITUTION.md | kernel/templates/org/CONSTITUTION.tpl.md | 4 | 3 |
| org/START.md | kernel/templates/org/START.tpl.md | 0 | 3 |
| org/OPERATING_MODEL.md | kernel/templates/org/OPERATING_MODEL.tpl.md | 0 | 12 |
| org/STATE.md | kernel/templates/org/STATE.tpl.md | 0 | 1 |
| org/TEMPLATES.md | kernel/templates/org/TEMPLATES.tpl.md | 0 | 4 |
| org/CADENCE.md | kernel/templates/org/CADENCE.tpl.md | 0 | 2 |
| org/QUESTIONS.md | kernel/templates/org/QUESTIONS.tpl.md | 0 | 0 |
| org/QUEUE.md | kernel/templates/org/QUEUE.tpl.md | 0 | 0 |
| org/roles/PLAN.md | kernel/templates/org/roles/PLAN.tpl.md | 0 | 2 |
| org/roles/WORK.md | kernel/templates/org/roles/WORK.tpl.md | 0 | 2 |
| org/roles/VERIFY.md | kernel/templates/org/roles/VERIFY.tpl.md | 0 | 1 |

Fence counts are fenced blocks resolved: blocks kept for the ruled
scale have their fence lines removed, blocks for other scales are
removed whole. The Q-001 row in org/QUESTIONS.md transcribes the
brief's open spend-budget question; it is transcription, not
authoring. The empty directories the matrix lists at M,
`org/decisions/` and `org/logs/`, are created with `.gitkeep` files.

Deferral fills (`set at first build`, COMPILE.md) count as fills and
are listed here by slot, with where each gets ruled. All seventeen are
in docs/LOCKBOOK.md and all get ruled at the first-build lock-in,
recorded via org/QUEUE.md: signature motif, signature animated pieces,
token home, code mirror, styleguide route, surface ladder, accents,
text tiers, reading measure, wide measure, full measure, block gap,
and the five QC gates (build, overflow at 375, page weight,
screenshots, regression smokes).

## Distillations

Standards or notes distilled into the seed from the doctrine the
rulings cite, each with the ruling that pulled it in. None is a valid
answer at S.

None.

## Deviations from the matrix

None expected. Anything here blocks the gate until ruled.

None. The lock-book ships `addons: []` because nothing is deployed at
Session 0; the ops-runbook add-on attaches at first deploy and the
restore-test add-on at first production data, both noted in the
lock-book and the brief.

## Check results

Paste the `eos_check.py --seed` summary line and date. All auto items
green before the human items are judged.

- 2026-08-02 · `python tools/eos_check.py --seed benchmark/fixtures/seed-v1-M` · `0 errors, 0 warnings`

## Sign-off (human rubric items)

- [ ] H1 cold-start test · - [ ] H2 brief reads true · - [ ] H3
  rulings honest · - [ ] H4 voice holds · - [ ] H5 operator can run it
- Signed: (awaiting operator) · date: (awaiting sign-off)
