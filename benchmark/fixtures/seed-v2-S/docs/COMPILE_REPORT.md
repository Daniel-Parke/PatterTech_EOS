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
- eos_version: 2.0.0-dev · eos_commit: 2c7468d
- compiled: 2026-08-03 · compiler session: EOS v2 build, lane P3

## Ancestry

One row per compiled file. Source is the kernel template path, `byte
copy of AGENTS.md` for CLAUDE.md, or `authored` for trigger add-ons
written at Session 0 from doctrine (name the doctrine). JSON seed
files carry ancestry rows like any other: the policy and cadence
files trace to their kernel templates with slots filled and no
fences, and the claims file's source is `seeded empty` per its
schema. Reseeds add two row kinds: `normalised` (pre-EOS venture
files that gained front-matter only, content untouched) and
`preserved` (venture content the compile did not touch).

| file | source | slots filled | fences pruned |
| --- | --- | --- | --- |
| AGENTS.md | kernel/templates/AGENTS.tpl.md | 2 | 2 |
| CLAUDE.md | byte copy of AGENTS.md | 0 | 0 |
| OPERATORS_GUIDE.md | kernel/templates/OPERATORS_GUIDE.tpl.md | 1 | 5 |
| docs/VENTURE_BRIEF.md | kernel/templates/VENTURE_BRIEF.tpl.md | 14 | 0 |
| docs/LOCKBOOK.md | kernel/templates/LOCKBOOK.tpl.md | 29 | 0 |
| docs/EOS_FEEDBACK.md | kernel/templates/EOS_FEEDBACK.tpl.md | 0 | 0 |
| docs/COMPILE_REPORT.md | kernel/templates/COMPILE_REPORT.tpl.md | 12 | 0 |
| docs/policy.json | kernel/templates/org/policy.tpl.json | 6 | 0 |
| docs/TASKS.md | kernel/templates/TASKS.tpl.md | 0 | 0 |

Fence counts are fenced blocks resolved: blocks kept for the ruled
scale have their fence lines removed, blocks for other scales are
removed whole. The policy row counts the six real slots
(`VENTURE_NAME`, `CAPABILITY_PROFILE_REF`, the three path lists and
`GUARD_MAPPING_REF`); the seventh `{{SLOT}}` occurrence sits inside
the template's own `_slots` note, which was deleted after filling per
that note. The risk factor table, the express thresholds, the mode
dials, the decision budget and the approvals list carry no slots, so
they ship exactly as the template holds them; the approvals block is
protected content and instantiates Article 8 of the v2 constitution
unchanged.

Deferral fills (`set at first build`, COMPILE.md) count as fills and
are listed here by slot, with where each gets ruled. All seventeen are
in docs/LOCKBOOK.md and all get ruled at the first-build lock-in, the
top open item in docs/TASKS.md: signature motif, signature animated
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

None in the file set: every file above is a row of the v2 matrix at
scale S and nothing else ships. Two compile-time notes that are not
deviations but must be read before the gate:

- The venture-name override against the canned brief is recorded in
  docs/EOS_FEEDBACK.md; it changes no matrix file.
- `guard.mapping_ref` names `docs/guard-mapping.json`, which does not
  exist yet. That is the fail-closed state the guard spec intends:
  `guard.validated` is false, so every guarded class is manual-only
  and the operator acts.

## Check results

Paste the `eos_check.py --seed` summary line and date. All auto items
green before the human items are judged.

- 2026-08-03 · `python -m tools.eos check --seed benchmark/fixtures/seed-v2-S`
  · not yet green, and not for a fault in this seed: the seed check
  resolves the governing matrix at the pinned `eos_commit`, and at
  2c7468d `kernel/SCALE_MATRIX.md` still holds the v1 S/M/L matrix
  while the v2 matrix waits at `kernel/SCALE_MATRIX_v2.staging.md`.
  Every finding traces to that. Against the v2 matrix the seed reports
  one error, D004, because the checker's queue-file map still points
  scale S at `docs/WORKLOG.md`, a file the v2 matrix deletes in favour
  of `docs/TASKS.md`. Both are recorded for the integrator; neither is
  fixable from inside a seed.

## Sign-off (human rubric items)

- [ ] H1 cold-start test · - [ ] H2 brief reads true · - [ ] H3
  rulings honest · - [ ] H4 voice holds · - [ ] H5 operator can run it
- Signed: (awaiting operator) · date: (awaiting sign-off)
