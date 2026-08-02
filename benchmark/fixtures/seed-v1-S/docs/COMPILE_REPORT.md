---
summary: Herbfield Lane compile report, the seed's ancestry proof and sign-off record
type: template
tags: [eos]
compiled_from: kernel/templates/COMPILE_REPORT.tpl.md
---

# Compile report · Herbfield Lane

Proof that this seed was compiled, not authored. Written by the
Session 0 compiler; validated by `eos_check.py --seed`; signed by the
operator against the human rubric items. A seed file that cannot be
traced to a row below is a compile failure.

## Seed identity

- venture: Herbfield Lane
- scale: S · add-ons: none
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
| docs/WORKLOG.md | kernel/templates/WORKLOG.tpl.md | 0 | 0 |
| docs/COMPILE_REPORT.md | kernel/templates/COMPILE_REPORT.tpl.md | 12 | 0 |

Fence counts are fenced blocks resolved: blocks kept for the ruled
scale have their fence lines removed, blocks for other scales are
removed whole.

Deferral fills (`set at first build`, COMPILE.md) count as fills and
are listed here by slot, with where each gets ruled. All seventeen are
in docs/LOCKBOOK.md and all get ruled at the first-build lock-in,
recorded in docs/WORKLOG.md: signature motif, signature animated
pieces, token home, code mirror, styleguide route, surface ladder,
accents, text tiers, reading measure, wide measure, full measure,
block gap, and the five QC gates (build, overflow at 375, page weight,
screenshots, regression smokes).

## Distillations

Standards or notes distilled into the seed from the doctrine the
rulings cite, each with the ruling that pulled it in. None is a valid
answer at S.

None.

## Deviations from the matrix

None expected. Anything here blocks the gate until ruled.

None. The venture-name override against the canned brief is recorded
in docs/EOS_FEEDBACK.md; it changes no matrix file.

## Check results

Paste the `eos_check.py --seed` summary line and date. All auto items
green before the human items are judged.

- 2026-08-02 · `python tools/eos_check.py --seed benchmark/fixtures/seed-v1-S` · `0 errors, 0 warnings`

## Sign-off (human rubric items)

- [ ] H1 cold-start test · - [ ] H2 brief reads true · - [ ] H3
  rulings honest · - [ ] H4 voice holds · - [ ] H5 operator can run it
- Signed: (awaiting operator) · date: (awaiting sign-off)
